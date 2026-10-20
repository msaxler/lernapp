"""Umkreis Freiburg Süd/West als Ortsporträt (Mike 2026-10-20, „weitere 10 Orte“): die fünf Orte des Raums Freiburg (iter1),
die im Raum bahn fehlen, dort neu eintragen – Staufen, Günterstal, Horben, Umkirch, Gundelfingen (Wikipedia-Titel aus
iter1/schicht0.json). Günterstal ist Stadtteil: LEO-BW-Ortslexikon als Landesportal. Dazu laufen aus bahn: Merzhausen 389,
Au 390, Ebringen 391, Schallstadt 392, Bad Krozingen 393 (bestehende Orte, Karten werden ersetzt).
Aufruf: python -X utf8 scripts/data-build/orte_eintragen_freiburg_sued_2026-10-20.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BAHN = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
ITER1 = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'iter1', 'schicht0.json')
# slug neu, slug iter1, Name, Einheit, Anker (danach einfügen)
NEU = [('434-staufen', '10-staufen', 'Staufen', 'Stadt', '393-bad-krozingen'),
       ('435-horben', '09-horben', 'Horben', 'Gemeinde', '390-au-breisgau'),
       ('436-guenterstal', '08-guenterstal', 'Günterstal', 'Ortsteil von Freiburg im Breisgau', '435-horben'),
       ('437-umkirch', '01-umkirch', 'Umkirch', 'Gemeinde', '65-march'),
       ('438-gundelfingen', '02-gundelfingen', 'Gundelfingen', 'Gemeinde', '397-hochdorf-freiburg')]
DOC = (' Umkreis Freiburg Süd/West als Ortsporträt (Mike 2026-10-20): Merzhausen, Au, Ebringen, Schallstadt, Bad Krozingen (bestehend)'
       ' und neu im Raum bahn Staufen, Horben, Günterstal, Umkirch, Gundelfingen (bisher nur Raum iter1).')

with open(ITER1, encoding='utf-8') as f:
    titel = {o['slug']: o['dewiki'] for o in json.load(f)}
with open(BAHN, encoding='utf-8') as f:
    o = json.load(f)
orte = o['orte']
vorhanden = {e[0] for e in orte}
for slug, alt, name, einheit, anker in NEU:
    if slug in vorhanden:
        print('schon da:', slug); continue
    i = next(i for i, e in enumerate(orte) if e[0] == anker)
    orte.insert(i + 1, [slug, 'ziel', name, titel[alt], einheit])
    o['laender'][slug] = 'BW'
    print(slug, '→', titel[alt], 'nach', anker)
o['quellen_amtlich']['436-guenterstal'] = {
    'webseite': 'https://www.freiburg.de/pb/206688.html',
    'seiten': [],
    'portal': ['https://www.leo-bw.de/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/7714/Günterstal'],
}
if DOC.strip() not in o['_doc']:
    o['_doc'] += DOC
with open(BAHN, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte:', len(orte))
