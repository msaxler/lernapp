"""Gemeinde-Achsen: Wappen als eigene Quelle je Zielort (Fragenfamilie Wappen, Entscheid Mike 2026-10-02).

Mike: Kartenform ist die Warum-Frage („Woher stammt der Löwe im Wappen?“); ohne belegte Wappenbegründung keine
Wappen-Karte. Ortsartikel tragen die Begründung oft nur in einer Tabelle oder gar nicht, deshalb sammelt dieses
Skript je Ort, was es gibt:
  - Abschnitt „Wappen“ des Ortsartikels und Absätze anderer Abschnitte über Stadtwappen oder Siegel
  - Wappen-Tabellen des Ortsartikels (Blasonierung, Wappenbegründung)
  - Eintrag der Wappenliste des Landkreises oder der Stadt (nur Blasonierung; dient als Gegenprobe)
  - Nachrecherche außerhalb von Wikipedia aus <raum>/wappen-nachrecherche.json (von Hand, mit URL und Zitat)
-> data/gemeinde-achsen/<raum>/quellen/<slug>+w.txt, Übersicht in <raum>/wappen.json.

Bewusst NICHT in zweitquellen.json: Die Eingaben der bisherigen Kartenläufe bleiben damit, wie sie waren; die
Wappen-Karten entstehen in einem eigenen Lauf.

Aufruf:  python -X utf8 scripts/data-fetch/gemeinde_achsen_wappen.py [slugs]     (GA_RAUM=<raum>)
"""
import datetime
import html
import io
import json
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemeinde_achsen_quellen import AUS, ORTE, _klartext, _tabellen, TABELLE_WEG, artikel, hole  # noqa: E402

# Wappenlisten je Raum (dewiki). Stadtteile stehen in der Liste ihrer Stadt oder ihres Landkreises.
LISTEN = {
    'iter1': ['Liste der Wappen im Landkreis Breisgau-Hochschwarzwald', 'Liste der Wappen in Freiburg im Breisgau',
              'Liste der Wappen im Landkreis Emmendingen'],  # Denzlingen
    'neuwied': ['Liste der Wappen im Landkreis Neuwied', 'Liste der Wappen im Landkreis Mayen-Koblenz'],  # Bendorf
}
# Absatz außerhalb des Wappen-Abschnitts zählt nur, wenn er vom Wappen des Orts handelt (nicht „Wappen des Kurfürsten“)
ABSATZ_WAPPEN = re.compile(r'Stadtwappen|Gemeindewappen|Ortswappen|Stadtsiegel|im Wappen')
TABELLE_WAPPEN = re.compile(r'Blasonierung|Wappenbegründung')


def parse_html(titel):
    d = hole('https://de.wikipedia.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'parse', 'format': 'json', 'page': titel, 'prop': 'text', 'redirects': 1, 'disableeditsection': 1}))
    return d['parse']['text']['*']


def wappen_tabellen(h):
    aus = []
    for klasse, a, z in _tabellen(h):
        if TABELLE_WEG.search(klasse):
            continue
        text = _klartext(h[a:z])
        if TABELLE_WAPPEN.search(text):
            aus.append(text)
    return aus


def wappen_fliesstext(text):
    """Abschnitt mit „Wappen“ in der Überschrift (bis zur nächsten Überschrift gleicher oder höherer Ebene) und
    Absätze anderer Abschnitte über Stadtwappen oder Siegel."""
    teile, im = [], None
    abschnitt, absaetze = [], []
    for zeile in text.split('\n'):
        m = re.match(r'^(=+) *(.*?) *=+$', zeile)
        if m:
            ebene = len(m.group(1))
            if im is not None and ebene <= im:
                im = None
            if im is None and 'Wappen' in m.group(2):
                im = ebene
                abschnitt.append(zeile)
            continue
        if im is not None:
            if zeile.strip():
                abschnitt.append(zeile.strip())
        elif ABSATZ_WAPPEN.search(zeile):
            absaetze.append(zeile.strip())
    if len(abschnitt) > 1:
        teile.append('\n'.join(abschnitt))
    teile += absaetze
    return teile


def listen_eintraege(listen, namen):
    aus = []
    for titel, text in listen:
        for zeile in text.split('\n'):
            m = re.match(r'^↑ (.+?): (.*)$', zeile)
            if m and m.group(1) in namen:
                aus.append((titel, m.group(2)))
    return aus


def main():
    raum = os.path.basename(AUS)
    nur = sys.argv[1:]
    heute = datetime.date.today().isoformat()
    pfad_nach = os.path.join(AUS, 'wappen-nachrecherche.json')
    nach = {}
    if os.path.exists(pfad_nach):
        with io.open(pfad_nach, encoding='utf-8') as f:
            nach = json.load(f)['orte']
    listen = []
    for titel in LISTEN.get(raum, []):
        listen.append((titel, _klartext(parse_html(titel))))
        time.sleep(1)
    pfad_ueb = os.path.join(AUS, 'wappen.json')
    uebersicht = []
    if nur and os.path.exists(pfad_ueb):
        with io.open(pfad_ueb, encoding='utf-8') as f:
            uebersicht = [u for u in json.load(f) if u['slug'] not in nur]
    for slug, rolle, name, titel, einheit in ORTE:
        if rolle != 'ziel' or (nur and slug not in nur):
            continue
        s = artikel(titel)
        url = s.get('fullurl', '')
        fliess = wappen_fliesstext(s.get('extract', ''))
        tab = wappen_tabellen(parse_html(s.get('title', titel)))
        namen = {name, titel, re.sub(r' \(.*\)$', '', titel)}
        eintr = listen_eintraege(listen, namen)
        recherche = nach.get(slug, [])
        quellen, teile = [], []
        if fliess or tab:
            quellen.append(url)
            if fliess:
                teile.append('== Aus dem Ortsartikel „%s“ ==\n\n%s' % (s.get('title', titel), '\n\n'.join(fliess)))
            if tab:
                teile.append('== Aus Tabellen des Ortsartikels „%s“ ==\n\n%s' % (s.get('title', titel), '\n\n'.join(tab)))
        for lt, zeile in eintr:
            quellen.append('https://de.wikipedia.org/wiki/' + urllib.parse.quote(lt.replace(' ', '_')))
            teile.append('== Aus der Wikipedia-Liste „%s“ (nur Blasonierung) ==\n\n%s' % (lt, zeile))
        for r in recherche:
            quellen.append(r['url'])
            teile.append('== Aus %s (%s, abgerufen %s) ==\n\n%s' % (r['quelle'], r['url'], r['abruf'], r['text']))
        # Die Wappenliste gibt nur die Blasonierung; eine Begründung kommt aus dem Artikel oder der Nachrecherche
        # (Stichwortsuche griff daneben: Horben, Feldkirchen). Ob sie die Figuren wirklich erklärt, prüft der Kartenlauf.
        hat_begruendung = bool(fliess or tab or recherche)
        datei = slug + '+w.txt'
        ziel = os.path.join(AUS, 'quellen', datei)
        if not teile:
            if os.path.exists(ziel):
                os.remove(ziel)
            print('%-18s nichts' % slug)
            continue
        kopf = ('# Wappen-Quelle zu: %s (%s)\n# Quellen: %s\n# Abruf: %s\n# Lizenz der Wikipedia-Teile: CC BY-SA 4.0\n\n'
                % (name, einheit, ' · '.join(dict.fromkeys(quellen)), heute))
        text = kopf + '\n\n'.join(teile) + '\n'
        with io.open(ziel, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        uebersicht.append({'slug': slug, 'ort': name, 'datei': datei, 'quellen': list(dict.fromkeys(quellen)),
                           'woerter': len(text.split()), 'begruendung': hat_begruendung, 'abruf': heute})
        print('%-18s %4d Wörter  Artikel %d/%d  Liste %d  Nachrecherche %d  Begründung %s' % (
            slug, len(text.split()), len(fliess), len(tab), len(eintr), len(recherche), 'ja' if hat_begruendung else 'NEIN'))
        time.sleep(1.5)
    uebersicht.sort(key=lambda u: u['slug'])
    with io.open(pfad_ueb, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(uebersicht, f, ensure_ascii=False, indent=1)
    print('fertig: %d Orte mit Wappen-Quelle, davon %d mit Begründung' % (
        len(uebersicht), sum(u['begruendung'] for u in uebersicht)))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
