"""Gemeinde-Achsen Iteration 1, Raum Freiburg: Quelltexte und Schicht 0 holen.

Je Ort:
  - Klartext des deutschsprachigen Wikipedia-Artikels (MediaWiki-API, prop=extracts)
    -> data/gemeinde-achsen/iter1/quellen/<slug>.txt   (Schicht-1-Quelle für die LLM-Extraktion)
  - Grunddaten aus Wikidata (Einwohner P1082, Höhe P2044, Fläche P2046, Koordinaten P625,
    Verwaltungseinheit P131) -> data/gemeinde-achsen/iter1/schicht0.json

Aufruf:  python scripts/data-fetch/gemeinde_achsen_quellen.py
Ortsliste: docs/konzepte/quizaway-stufe2-vorbereitung-2026-10-01.md §1.
"""
import datetime
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUS = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'iter1')
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
    os.makedirs(os.path.join(AUS, 'quellen'), exist_ok=True)
    heute = datetime.date.today().isoformat()
    schicht0 = []
    for slug, rolle, name, titel, einheit in ORTE:
        s = artikel(titel)
        text = s.get('extract', '')
        if not text:
            print('LEER:', titel)
            sys.exit(1)
        kopf = ('# Quelle: %s\n# Titel: %s\n# Abruf: %s\n# Lizenz: Wikipedia, CC BY-SA 4.0\n\n'
                % (s.get('fullurl', ''), s.get('title', titel), heute))
        with io.open(os.path.join(AUS, 'quellen', slug + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(kopf + text + '\n')
        eintrag = {'slug': slug, 'rolle': rolle, 'name': name, 'einheit': einheit,
                   'dewiki': s.get('title', titel), 'url': s.get('fullurl', ''), 'abruf': heute,
                   'zeichen': len(text), 'woerter': len(text.split())}
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
