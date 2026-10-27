"""Vertiefung Freiburg (Mike 2026-10-27): Quellenpaket je Freiburger Stadtteil für die Extraktion (GA_VERTIEFUNG=1).

Schreibt data/gemeinde-achsen/bahn/quellen-vertiefung/<slug>.txt mit Abschnitten „=== QUELLE: <Adresse> | Gemeinde-Webseite ===“:
  1. Orte von visit.freiburg.de (Tourismus-Gesellschaft der Stadt), deren Koordinaten in der Stadtteilgrenze liegen
     (freiburg-vertiefung/grenzen/<slug>.geojson). Sehenswürdigkeiten, Kultur, Natur, Freizeit, Infrastruktur immer;
     Läden und Lokale nur, wenn der Text von Geschichte erzählt; öffentliche Toiletten nie.
  2. Rangplätze aus dem Stadtbezirksatlas 2025 (freiburg-vertiefung/atlas/<slug>.txt, freiburg_atlas_rangplaetze.py).
  3. Stadtteilleitlinien der Stadt (Seitentext, ohne Protokoll-PDFs) für Innenstadt, Wiehre, Stühlinger, St. Georgen, Landwasser.
Gibt je Stadtteil die Zahl der Orte und Zeichen aus und schreibt freiburg-vertiefung/uebersicht.json.
Aufruf:  python -X utf8 scripts/data-build/freiburg_vertiefung_quellen.py [--runde2 <slug>]
"""
import html
import io
import json
import os
import re
import sys
import time
import urllib.request

from shapely.geometry import Point, shape

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FV = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'freiburg-vertiefung')
RAUM = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn')
AUS = os.path.join(RAUM, 'quellen-vertiefung')
IMMER = ('Sehenswürdigkeit', 'Kultur', 'Natur', 'Freizeiteinrichtung', 'Jederzeit frei zugänglich', 'Infrastruktur', 'Bildung',
         'Hersteller')
# Läden und Lokale nur mit Geschichte (Zum Roten Bären, Großer Meyerhof); die Altstadt hätte sonst 389.000 Zeichen
# (eine Jahreszahl vor 1900; „gegründet“ allein ließ die Bäckerei von 2022 durch)
GESCHICHTE = re.compile(r'Jahrhundert|ältest|\b1[0-8]\d\d\b')
LAENGE, LAENGE_LADEN = 3000, 1500
LEITLINIEN = {'444-altstadt-freiburg': '434942', '439-wiehre': '435018', '445-stuehlinger': '435056',
              '452-sankt-georgen': '435497', '457-landwasser': '468809'}
UA = {'User-Agent': 'Mozilla/5.0 (QuizAway-Recherche)'}


def lies(p):
    with io.open(p, encoding='utf-8') as f:
        return f.read()


def seitentext(roh):
    t = re.sub(r'(?s)<(script|style|nav|header|footer)\b.*?</\1>', ' ', roh)
    m = re.search(r'(?s)<main\b.*?</main>', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', m.group(0) if m else t))
    return re.sub(r'\s+', ' ', t).strip()


def leitlinie(pb):
    """Seitentext einer Leitlinien-Seite, einmal geholt und abgelegt."""
    pfad = os.path.join(FV, 'leitlinien', pb + '.txt')
    if not os.path.exists(pfad):
        os.makedirs(os.path.dirname(pfad), exist_ok=True)
        with urllib.request.urlopen(urllib.request.Request('https://www.freiburg.de/pb/%s.html' % pb, headers=UA), timeout=60) as r:
            t = seitentext(r.read().decode('utf-8', 'replace'))
        # Navigation vor der Überschrift und der Fuß „Fehler auf Webseite gefunden?“ gehören nicht dazu
        t = re.split(r'Fehler auf Webseite gefunden\?', t)[0]
        with io.open(pfad, 'w', encoding='utf-8', newline='\n') as f:
            f.write(t)
        time.sleep(1)
    return lies(pfad)


def poi_text(p):
    """Fließtext eines visit-Orts ohne Kopfzeile (Bildnachweis, Öffnungszeit) und ohne alles ab „weiterlesen“."""
    t = p['text'][len(p['kopf']):].strip()
    t = re.split(r'\s+weiterlesen weniger anzeigen', t)[0]
    if t.startswith(p['name']):
        t = t[len(p['name']):].strip()
    return t


def laden(p):
    return not any(k in p['kopf'] for k in IMMER)


def nehmen(p):
    # Toiletten und die 15 Trinkwasserbrunnen der Stadtwerke tragen keine Geschichte
    if re.search(r'toilette|^trinkwasser', p['name'].lower()) or not p['lat']:
        return False
    if any(k in p['kopf'] for k in IMMER):
        return True
    return bool(GESCHICHTE.search(poi_text(p)))


def runde2(slug):
    """Quellen für eine zweite Runde (Altstadt, Mike 2026-10-27): die Abschnitte von quellen-vertiefung/<slug>.txt, aus
    denen die erste Extraktion (fakten/<slug>-tief.txt) keinen Fakt gezogen hat. Schreibt quellen-vertiefung/<slug>-tief2.txt."""
    text = lies(os.path.join(AUS, slug + '.txt'))
    genutzt = set(re.findall(r'QUELLE:\s*(\S+)', lies(os.path.join(RAUM, 'fakten', slug + '-tief.txt'))))
    kopf, *abschnitte = re.split(r'(?=^=== QUELLE: )', text, flags=re.M)
    rest = [a for a in abschnitte if re.match(r'=== QUELLE: (\S+)', a).group(1) not in genutzt]
    with io.open(os.path.join(AUS, slug + '-tief2.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(kopf + ''.join(rest))
    print('%s Runde 2: %d von %d Abschnitten ohne Fakt aus Runde 1, %d Zeichen' % (slug, len(rest), len(abschnitte), len(kopf + ''.join(rest))))


def main():
    if sys.argv[1:2] == ['--runde2']:
        return runde2(sys.argv[2])
    pois = json.loads(lies(os.path.join(FV, 'visit', 'pois.json')))
    grenzen = {}
    for datei in os.listdir(os.path.join(FV, 'grenzen')):
        g = json.loads(lies(os.path.join(FV, 'grenzen', datei)))
        grenzen[datei[:-8]] = shape(g['features'][0]['geometry'])
    with io.open(os.path.join(RAUM, 'orte.json'), encoding='utf-8') as f:
        stadtteile = [(o[0], o[2]) for o in json.load(f)['orte'] if o[4] == 'Ortsteil von Freiburg im Breisgau']
    os.makedirs(AUS, exist_ok=True)
    uebersicht, zugeordnet = {}, set()
    for slug, name in stadtteile:
        teile, liste = [], []
        if slug in grenzen:
            for p in pois:
                if nehmen(p) and grenzen[slug].contains(Point(p['lon'], p['lat'])):
                    zugeordnet.add(p['url'])
                    text = poi_text(p)
                    if len(text) < 120:
                        continue
                    grenze = LAENGE_LADEN if laden(p) else LAENGE
                    if len(text) > grenze:
                        text = text[:grenze].rsplit('. ', 1)[0] + '. […]'
                    adresse = ', '.join(x for x in (p['strasse'], p['plz']) if x)
                    # Der Stadtteil steht nicht auf der Seite, er ist aus den Koordinaten und der OSM-Grenze berechnet (die
                    # Prüfstufe zitierte ihn in der Probe sonst als Aussage der Stadt)
                    teile.append('=== QUELLE: %s | Gemeinde-Webseite ===\n%s (visit.freiburg.de, Tourismus der Stadt Freiburg; '
                                 'Adresse: %s; liegt nach den Koordinaten der Seite und der OpenStreetMap-Grenze im Stadtteil %s)\n%s'
                                 % (p['url'], p['name'], adresse or 'keine', name, text))
                    liste.append(p['name'])
        atlas = os.path.join(FV, 'atlas', slug + '.txt')
        if os.path.exists(atlas):
            teile.append(lies(atlas).strip())
        if slug in LEITLINIEN:
            teile.append('=== QUELLE: https://www.freiburg.de/pb/%s.html | Gemeinde-Webseite ===\n%s'
                         % (LEITLINIEN[slug], leitlinie(LEITLINIEN[slug])))
        text = 'ORT: %s (Stadtteil von Freiburg im Breisgau)\n\n' % name + '\n\n'.join(teile)
        with io.open(os.path.join(AUS, slug + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text + '\n')
        uebersicht[slug] = {'name': name, 'visit_orte': liste, 'atlas': os.path.exists(atlas), 'leitlinie': slug in LEITLINIEN,
                            'zeichen': len(text)}
        print('%-24s %3d visit-Orte  Atlas %-4s Leitlinie %-4s %7d Zeichen' % (slug, len(liste), 'ja' if os.path.exists(atlas) else '-',
              'ja' if slug in LEITLINIEN else '-', len(text)))
    ohne = [p['name'] for p in pois if nehmen(p) and p['url'] not in zugeordnet]
    print('visit-Orte ohne Stadtteil (außerhalb aller Grenzen, etwa Umland):', len(ohne))
    with io.open(os.path.join(FV, 'uebersicht.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'stadtteile': uebersicht, 'ohne_stadtteil': ohne}, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
