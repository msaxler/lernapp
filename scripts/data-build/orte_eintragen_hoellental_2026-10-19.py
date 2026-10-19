"""Strecke Freiburg–Breitnau (Mike 2026-10-19: Tochter fährt sie regelmäßig mit Bahn, Auto, Rad – Breitnauer Hof):
Breitnau und Kirchzarten in data/gemeinde-achsen/bahn/orte.json eintragen. Pilotregion für das Ortsporträt.
Kirchzarten liegt bisher nur im Raum iter1 (Freiburg, erster Feldtest); im Raum bahn neu, damit die Ortsporträt-Kette
dort läuft. Aufruf: python -X utf8 scripts/data-build/orte_eintragen_hoellental_2026-10-19.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
NEU = [('432-breitnau', 'Breitnau', 'Breitnau', 'Gemeinde'), ('433-kirchzarten', 'Kirchzarten', 'Kirchzarten', 'Gemeinde')]
DOC = (' Strecke Freiburg–Breitnau (Mike 2026-10-19, Tochter: Bahn Höllentalbahn, Auto B31, Rad; Breitnauer Hof): Breitnau neu,'
       ' Kirchzarten neu im Raum bahn (bisher iter1). Pilotregion Ortsporträt: Ebnet, Littenweiler, Kirchzarten, Stegen,'
       ' Buchenbach, Oberried, Hinterzarten, Breitnau, Titisee-Neustadt.')

with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
vorhanden = {e[0] for e in o['orte']}
for slug, name, titel, einheit in NEU:
    if slug in vorhanden:
        print('schon da:', slug); continue
    o['orte'].append([slug, 'ziel', name, titel, einheit])
    o['laender'][slug] = 'BW'
if DOC.strip() not in o['_doc']:
    o['_doc'] += DOC
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte:', len(o['orte']))
