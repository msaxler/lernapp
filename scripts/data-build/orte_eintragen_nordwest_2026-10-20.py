"""Mike 2026-10-20: „Freiburg nordwestliche Umgebung: Gündlingen, Ihringen, Vogtsburg, Teningen, Emmendingen, Holzhausen, March …“,
Zuschnitt A Kern. Neu im Raum bahn: Vogtsburg, Merdingen, Denzlingen (Gemeinden) und Gündlingen (Ortsteil von Breisach am Rhein,
eigener Wikipedia-Artikel). Wasenweiler, Holzhausen, Hugstetten, Buchheim, Neuershausen leiten auf Ihringen bzw. March weiter
und bleiben im Porträt der Gemeinde (wie Zarten in Kirchzarten). Die 10 bestehenden Gemeinden (March, Gottenheim, Bötzingen,
Eichstetten, Ihringen, Breisach, Teningen, Emmendingen, Vörstetten, Reute) werden nur neu gerechnet.
Reihenfolge: Merdingen nach Gottenheim (Tuniberg), Gündlingen nach Breisach, Vogtsburg nach Ihringen, Denzlingen nach Gundelfingen.
Aufruf: python -X utf8 scripts/data-build/orte_eintragen_nordwest_2026-10-20.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
# slug, Name, Wikipedia-Titel, Einheit, Anker (eingefügt danach)
NEU = [('465-merdingen', 'Merdingen', 'Merdingen', 'Gemeinde', '66-gottenheim'),
       ('466-guendlingen', 'Gündlingen', 'Gündlingen', 'Ortsteil von Breisach am Rhein', '70-breisach'),
       ('467-vogtsburg', 'Vogtsburg', 'Vogtsburg im Kaiserstuhl', 'Stadt', '69-ihringen'),
       ('468-denzlingen', 'Denzlingen', 'Denzlingen', 'Gemeinde', '438-gundelfingen')]
Q = {'466-guendlingen': {'webseite': 'https://www.breisach.de/', 'seiten': [], 'portal': []}}
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
    print(slug, 'nach', anker)
o['quellen_amtlich'].update(Q)
o['_doc'] += ' Nordwest A Kern (Mike 2026-10-20): Merdingen, Gündlingen (Ortsteil Breisach), Vogtsburg, Denzlingen neu; March-/Ihringen-Ortsteile ohne eigenen Artikel bleiben in der Gemeinde.'
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte:', len(orte))
