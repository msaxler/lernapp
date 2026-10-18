"""Essener Stadtteile um Heisingen in data/gemeinde-achsen/bahn/orte.json eintragen (Mike 2026-10-18, beide Ringe).
Einmal-Skript, Muster für spätere Regionen. Aufruf: python -X utf8 scripts/data-build/orte_eintragen_essen_2026-10-18.py
"""
import json, os, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')

NEU = [
    # slug, Name, Wikipedia-Titel (geprüft 2026-10-18: vorhanden, keine Begriffsklärung)
    ('418-kupferdreh', 'Kupferdreh', 'Kupferdreh'),
    ('419-ueberruhr', 'Überruhr', 'Überruhr'),
    ('420-bergerhausen', 'Bergerhausen', 'Bergerhausen (Essen)'),
    ('421-rellinghausen', 'Rellinghausen', 'Rellinghausen'),
    ('422-stadtwald-essen', 'Stadtwald', 'Stadtwald (Essen)'),
    ('423-fischlaken', 'Fischlaken', 'Fischlaken'),
    ('424-werden', 'Werden', 'Werden'),
    ('425-burgaltendorf', 'Burgaltendorf', 'Burgaltendorf'),
    ('426-steele', 'Steele', 'Steele (Essen)'),
    ('427-byfang', 'Byfang', 'Byfang'),
    ('428-ruettenscheid', 'Rüttenscheid', 'Rüttenscheid'),
    ('429-bredeney', 'Bredeney', 'Bredeney'),
    ('430-huttrop', 'Huttrop', 'Huttrop'),
    ('431-kettwig', 'Kettwig', 'Kettwig'),
]
EINHEIT = 'Ortsteil von Essen'  # Konvention: grunddaten.py erkennt Stadtteile nur an „Ortsteil von …“ (Fehlschlag 18.10. mit „Stadtteil“)
DOC = (' Essen um Heisingen (Mike 2026-10-18, Zielregion wie Pfäffingen, beide Ringe): erster Ring Kupferdreh, Überruhr'
       ' (Hinsel und Holthausen, ein Artikel), Bergerhausen, Rellinghausen, Stadtwald, Fischlaken, Werden, Burgaltendorf;'
       ' zweiter Ring Steele, Byfang, Rüttenscheid, Bredeney, Huttrop, Kettwig. Heisingen (360) und Essen (199) vorhanden.')

with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
vorhanden = {e[0] for e in o['orte']}
vorher = len(o['orte'])
for slug, name, titel in NEU:
    if slug in vorhanden:
        print('schon da:', slug); continue
    o['orte'].append([slug, 'ziel', name, titel, EINHEIT])
    o['laender'][slug] = 'NW'
if DOC.strip() not in o['_doc']:
    o['_doc'] += DOC
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte', vorher, '->', len(o['orte']))
