"""Gemeinde-Achsen Iteration 1, Raum Freiburg: Quelltexte und Schicht 0 holen.

Je Ort:
  - Klartext des deutschsprachigen Wikipedia-Artikels (MediaWiki-API, prop=extracts)
    -> data/gemeinde-achsen/iter1/quellen/<slug>.txt   (Schicht-1-Quelle für die LLM-Extraktion)
  - Grunddaten aus Wikidata (Einwohner P1082, Höhe P2044, Fläche P2046, Koordinaten P625,
    Verwaltungseinheit P131) -> data/gemeinde-achsen/iter1/schicht0.json

Seit 2026-10-02 hängt das Skript den Text der Inhaltstabellen an (Wappen, Ortsteile, Einwohner, Wahlen), weil der
Auszug Tabellen weglässt; die Quelltexte der bisherigen Läufe sind ohne ihn entstanden (Feldkirchen von Hand ergänzt).

Aufruf:  python scripts/data-fetch/gemeinde_achsen_quellen.py [slugs]      (GA_RAUM=<raum> für einen weiteren Raum)
         python scripts/data-fetch/gemeinde_achsen_quellen.py --probe "<Artikel>"   zeigt nur den Tabellentext
Ortsliste: docs/konzepte/quizaway-stufe2-vorbereitung-2026-10-01.md §1, weitere Räume in <raum>/orte.json.
"""
import datetime
import html
import io
import json
import re
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUS = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
UA = {'User-Agent': 'LernApp-GemeindeAchsen/0.1 (https://github.com/msaxler/lernapp)'}

# (slug, Rolle, Anzeigename, dewiki-Titel, Einheit)
ORTE = [
    ('01-umkirch', 'ziel', 'Umkirch', 'Umkirch', 'Gemeinde'),
    ('02-gundelfingen', 'ziel', 'Gundelfingen', 'Gundelfingen (Breisgau)', 'Gemeinde'),
    ('03-denzlingen', 'ziel', 'Denzlingen', 'Denzlingen', 'Gemeinde'),
    ('04-zaehringen', 'ziel', 'Zähringen', 'Zähringen (Freiburg im Breisgau)', 'Ortsteil von Freiburg im Breisgau'),
    ('05-st-peter', 'ziel', 'St. Peter', 'St. Peter (Hochschwarzwald)', 'Gemeinde'),
    ('06-glottertal', 'ziel', 'Glottertal', 'Glottertal', 'Gemeinde'),
    ('07-kirchzarten', 'ziel', 'Kirchzarten', 'Kirchzarten', 'Gemeinde'),
    ('08-guenterstal', 'ziel', 'Günterstal', 'Günterstal', 'Ortsteil von Freiburg im Breisgau'),
    ('09-horben', 'ziel', 'Horben', 'Horben', 'Gemeinde'),
    ('10-staufen', 'ziel', 'Staufen', 'Staufen im Breisgau', 'Stadt'),
    ('s1-oberkirch', 'spender', 'Oberkirch', 'Oberkirch (Baden)', 'Stadt'),
    ('s2-renchen', 'spender', 'Renchen', 'Renchen', 'Stadt'),
    ('s3-rheinau', 'spender', 'Rheinau', 'Rheinau (Baden)', 'Stadt'),
    ('s4-dornstetten', 'spender', 'Dornstetten', 'Dornstetten', 'Stadt'),
    ('s5-sulz', 'spender', 'Sulz am Neckar', 'Sulz am Neckar', 'Stadt'),
    ('s6-oberndorf', 'spender', 'Oberndorf am Neckar', 'Oberndorf am Neckar', 'Stadt'),
    ('s7-spaichingen', 'spender', 'Spaichingen', 'Spaichingen', 'Stadt'),
    ('s8-muehlheim', 'spender', 'Mühlheim an der Donau', 'Mühlheim an der Donau', 'Stadt'),
    ('s9-engen', 'spender', 'Engen', 'Engen', 'Stadt'),
    ('s10-tengen', 'spender', 'Tengen', 'Tengen', 'Stadt'),
]


# Ein weiterer Raum (GA_RAUM=neuwied) bringt seine Ortsliste in <raum>/orte.json mit
if os.path.exists(os.path.join(AUS, 'orte.json')):
    with io.open(os.path.join(AUS, 'orte.json'), encoding='utf-8') as _f:
        ORTE = [tuple(o) for o in json.load(_f)['orte']]


def hole(url):
    """GET mit Wartezeit bei HTTP 429 (Wikimedia drosselt dichte Anfragen)."""
    for versuch in range(6):
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code != 429 or versuch == 5:
                raise
            warte = int(e.headers.get('Retry-After') or 0) or 10 * (versuch + 1)
            print('  429, warte %d s' % warte)
            time.sleep(warte)


def artikel(titel):
    q = urllib.parse.urlencode({
        'action': 'query', 'format': 'json', 'redirects': 1, 'titles': titel,
        'prop': 'extracts|pageprops|info', 'explaintext': 1, 'exsectionformat': 'wiki',
        'ppprop': 'wikibase_item', 'inprop': 'url'})
    d = hole('https://de.wikipedia.org/w/api.php?' + q)
    return next(iter(d['query']['pages'].values()))


# ── Text aus Tabellen ───────────────────────────────────────────────────────
# Der Auszug (prop=extracts) lässt Tabellen weg. In Ortsartikeln stehen dort Wappenbeschreibungen, Listen der
# Bürgermeister, Einwohnerentwicklung und Wahlergebnisse; in Feldkirchen (Neuwied) die ganze Geschichte der Ortsteile
# (Befund Raum Neuwied, 2026-10-02, Bericht N14). Infobox, Navigationsleisten und Bildtabellen bleiben draußen.
TABELLE_WEG = re.compile(r'infobox|navbox|erw-nav|toccolours|metadata|sisterproject|hintergrundfarbe|noprint|mbox|vertical-navbox|'
                         r'gallery|thumb', flags=re.I)
TABELLE_MIN_WOERTER = 12


def _tabellen(h):
    """Äußere Tabellen eines HTML-Texts: Liste (Klasse, Anfang, Ende)."""
    aus, pos = [], 0
    for m in re.finditer(r'<table([^>]*)>', h):
        if m.start() < pos:
            continue
        tiefe, i = 1, m.end()
        while tiefe and i < len(h):
            a, z = h.find('<table', i), h.find('</table>', i)
            if z == -1:
                i = len(h)
                break
            if a != -1 and a < z:
                tiefe, i = tiefe + 1, a + 6
            else:
                tiefe, i = tiefe - 1, z + 8
        pos = i
        k = re.search(r'class="([^"]*)"', m.group(1))
        aus.append((k.group(1) if k else '', m.start(), i))
    return aus


def _klartext(h):
    # Zeilenumbrüche des HTML-Quelltexts tragen nichts; eine Textzeile je Tabellenzeile, Absatz oder Listenpunkt
    h = h.replace('\n', ' ')
    h = re.sub(r'<sup[^>]*class="reference".*?</sup>', '', h, flags=re.S)
    h = re.sub(r'<(style|script)[^>]*>.*?</\1>', '', h, flags=re.S)
    h = re.sub(r'</(td|th)>', ' | ', h)
    h = re.sub(r'<(tr|p|li|br|div)[^>]*>', '\n', h)
    t = html.unescape(re.sub(r'<[^>]+>', '', h))
    zeilen = []
    for z in t.split('\n'):
        z = re.sub(r'\s+', ' ', z).strip(' |')
        z = re.sub(r'(\s*\|\s*)+', ' | ', z)
        if z and z not in ('Wappen',):
            zeilen.append(z)
    return '\n'.join(zeilen)


def tabellentext(titel):
    """Text der Inhaltstabellen eines dewiki-Artikels, je Tabelle mit dem Abschnitt, in dem sie steht."""
    d = hole('https://de.wikipedia.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'parse', 'format': 'json', 'page': titel, 'prop': 'text', 'redirects': 1, 'disableeditsection': 1}))
    h = d['parse']['text']['*']
    teile = []
    for klasse, a, z in _tabellen(h):
        if TABELLE_WEG.search(klasse):
            continue
        text = _klartext(h[a:z])
        if len(text.split()) < TABELLE_MIN_WOERTER:
            continue
        ueber = re.findall(r'<h[234][^>]*>(.*?)</h[234]>', h[:a], flags=re.S)
        abschnitt = html.unescape(re.sub(r'<[^>]+>', '', ueber[-1])).strip() if ueber else 'Einleitung'
        teile.append('=== Tabelle im Abschnitt „%s“ ===\n%s' % (abschnitt, text))
    return '\n\n'.join(teile)


def bester_wert(claims, prop):
    """Neuester Wert nach Zeitpunkt-Qualifier P585, sonst bevorzugter Rang, sonst erster."""
    kand = []
    for c in claims.get(prop, []):
        snak = c.get('mainsnak', {})
        if snak.get('snaktype') != 'value':
            continue
        zeit = ''
        for q in c.get('qualifiers', {}).get('P585', []):
            if q.get('snaktype') == 'value':
                zeit = q['datavalue']['value']['time']
        kand.append((c.get('rank') == 'preferred', zeit, snak['datavalue']['value']))
    if not kand:
        return None, None
    kand.sort(key=lambda k: (k[0], k[1]))
    _, zeit, wert = kand[-1]
    return wert, zeit[1:11] if zeit else None


def wikidata(qid):
    d = hole('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'wbgetentities', 'format': 'json', 'ids': qid, 'props': 'claims', 'languages': 'de'}))
    claims = d['entities'][qid]['claims']
    aus = {'wikidata': qid}
    w, z = bester_wert(claims, 'P1082')
    if w:
        aus['einwohner'] = int(float(w['amount']))
        aus['einwohner_stand'] = z
    w, _ = bester_wert(claims, 'P2044')
    if w:
        aus['hoehe_m'] = float(w['amount'])
    w, _ = bester_wert(claims, 'P2046')
    if w:
        aus['flaeche_km2'] = float(w['amount'])
    w, _ = bester_wert(claims, 'P625')
    if w:
        aus['lat'], aus['lon'] = round(w['latitude'], 5), round(w['longitude'], 5)
    einheiten = []
    for c in claims.get('P131', []):
        snak = c.get('mainsnak', {})
        if snak.get('snaktype') == 'value' and c.get('rank') != 'deprecated' and 'P582' not in c.get('qualifiers', {}):
            einheiten.append(snak['datavalue']['value']['id'])
    if einheiten:
        lab = hole('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({
            'action': 'wbgetentities', 'format': 'json', 'ids': '|'.join(einheiten), 'props': 'labels', 'languages': 'de'}))
        aus['verwaltungseinheit'] = [lab['entities'][e]['labels'].get('de', {}).get('value', e) for e in einheiten]
    return aus


def main():
    if sys.argv[1:2] == ['--probe']:
        # nur ansehen, nichts schreiben: python … gemeinde_achsen_quellen.py --probe "Feldkirchen (Neuwied)"
        print(tabellentext(sys.argv[2]))
        return
    os.makedirs(os.path.join(AUS, 'quellen'), exist_ok=True)
    heute = datetime.date.today().isoformat()
    schicht0 = []
    # Mit Slugs als Argument werden nur diese Orte geholt (Ort nachziehen); die übrigen Einträge und
    # Quelltexte bleiben, wie sie die bisherigen Läufe gelesen haben.
    nur = sys.argv[1:]
    alt = {}
    if nur:
        with io.open(os.path.join(AUS, 'schicht0.json'), encoding='utf-8') as f:
            alt = {e['slug']: e for e in json.load(f)}
    for slug, rolle, name, titel, einheit in ORTE:
        if nur and slug not in nur:
            schicht0.append(alt[slug])
            continue
        s = artikel(titel)
        text = s.get('extract', '')
        if not text:
            print('LEER:', titel)
            sys.exit(1)
        tab = tabellentext(s.get('title', titel))
        kopf = ('# Quelle: %s\n# Titel: %s\n# Abruf: %s\n# Lizenz: Wikipedia, CC BY-SA 4.0\n# Tabellen: %d Wörter, am Ende angehängt\n\n'
                % (s.get('fullurl', ''), s.get('title', titel), heute, len(tab.split())))
        with io.open(os.path.join(AUS, 'quellen', slug + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(kopf + text + ('\n\n\n== Aus Tabellen des Artikels ==\n\n' + tab if tab else '') + '\n')
        # "woerter" zählt nur den Fließtext: Daran hängt die Grenze für die zweite Quelle (unter 1.000 Wörtern)
        eintrag = {'slug': slug, 'rolle': rolle, 'name': name, 'einheit': einheit,
                   'dewiki': s.get('title', titel), 'url': s.get('fullurl', ''), 'abruf': heute,
                   'zeichen': len(text), 'woerter': len(text.split()), 'woerter_tabellen': len(tab.split())}
        qid = s.get('pageprops', {}).get('wikibase_item')
        if qid:
            eintrag.update(wikidata(qid))
        schicht0.append(eintrag)
        print('%-16s %6d Wörter  %s  Einw. %s  Höhe %s  %s' % (
            slug, eintrag['woerter'], eintrag.get('wikidata', '-'), eintrag.get('einwohner', '-'),
            eintrag.get('hoehe_m', '-'), ', '.join(eintrag.get('verwaltungseinheit', []))))
        time.sleep(2)
    with io.open(os.path.join(AUS, 'schicht0.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(schicht0, f, ensure_ascii=False, indent=1)
    print('fertig:', len(schicht0), 'Orte')


if __name__ == '__main__':
    main()
