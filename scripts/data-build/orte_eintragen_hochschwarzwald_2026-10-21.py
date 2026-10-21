"""Mike 2026-10-21: „erst mal anfangen mit Südost, Hochschwarzwald jetzt“. Neu im Raum bahn: Glottertal (nach Denzlingen),
St. Peter und St. Märgen (nach Stegen – Straße Stegen–St. Peter–St. Märgen), Feldberg, Schluchsee, Lenzkirch, Eisenbach,
Friedenweiler (nach Titisee-Neustadt, vor Löffingen). Löffingen (76) wird nur neu gerechnet (hat seit 10/2026 handgesetzte Seiten).
Damit ist der Hochschwarzwald im Landkreis Breisgau-Hochschwarzwald vollständig.
Aufruf: python -X utf8 scripts/data-build/orte_eintragen_hochschwarzwald_2026-10-21.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
# slug, Name, Wikipedia-Titel, Einheit, Anker (eingefügt danach, in dieser Reihenfolge)
NEU = [('482-glottertal', 'Glottertal', 'Glottertal', 'Gemeinde', '468-denzlingen'),
       ('483-sankt-peter', 'St. Peter', 'St. Peter (Hochschwarzwald)', 'Gemeinde', '71-stegen'),
       ('484-sankt-maergen', 'St. Märgen', 'St. Märgen', 'Gemeinde', '483-sankt-peter'),
       ('485-feldberg', 'Feldberg', 'Feldberg (Schwarzwald)', 'Gemeinde', '75-titisee-neustadt'),
       ('486-schluchsee', 'Schluchsee', 'Schluchsee (Gemeinde)', 'Gemeinde', '485-feldberg'),
       ('487-lenzkirch', 'Lenzkirch', 'Lenzkirch', 'Gemeinde', '486-schluchsee'),
       ('488-eisenbach', 'Eisenbach', 'Eisenbach (Hochschwarzwald)', 'Gemeinde', '487-lenzkirch'),
       ('489-friedenweiler', 'Friedenweiler', 'Friedenweiler', 'Gemeinde', '488-eisenbach')]
with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
orte = o['orte']
vorhanden = {e[0] for e in orte}
for slug, name, titel, einheit, anker in NEU:
    if slug in vorhanden:
        print('schon da:', slug); continue
    i = next(i for i, e in enumerate(orte) if e[0] == anker)
    orte.insert(i + 1, [slug, 'ziel', name, titel, einheit])
    o['laender'][slug] = 'BW'
o['_doc'] += ' Hochschwarzwald (Mike 2026-10-21): Glottertal, St. Peter, St. Märgen, Feldberg, Schluchsee, Lenzkirch, Eisenbach, Friedenweiler (482–489); Löffingen neu gerechnet.'
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte:', len(orte), '|', [e[0] for e in orte if e[0][:2] in ('71', '75', '76', '48')])
