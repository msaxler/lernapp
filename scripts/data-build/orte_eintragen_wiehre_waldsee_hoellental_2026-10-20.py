"""Lücken der Strecke Freiburg–Breitnau (Mike 2026-10-20): Wiehre und Waldsee (Freiburger Stadtteile, km 0–4,6) und das
Höllental als eigener Ort (km 14–31, Muster Kloster Marienhaus: Wohnplatz/Tal mit Einheit „Ortsteil von Breitnau“, Standort
Wikidata Q301685). Quellen: LEO-BW-Ortslexikon (Wiehre 7749, Waldsee 7745) als Landesportal; Höllental über die
Breitnauer Seiten (Hirschsprung, Ravennaschlucht) und Wikipedia „Höllental (Schwarzwald)“.
Aufruf: python -X utf8 scripts/data-build/orte_eintragen_wiehre_waldsee_hoellental_2026-10-20.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
# slug, Name, Wikipedia-Titel, Einheit, (vor|nach), Anker
NEU = [('439-wiehre', 'Wiehre', 'Wiehre', 'Ortsteil von Freiburg im Breisgau', 'vor', '387-ebnet'),
       ('440-waldsee', 'Waldsee', 'Waldsee (Freiburg im Breisgau)', 'Ortsteil von Freiburg im Breisgau', 'vor', '387-ebnet'),
       ('441-hoellental', 'Höllental', 'Höllental (Schwarzwald)', 'Ortsteil von Breitnau', 'nach', '73-buchenbach')]
Q = {
    '439-wiehre': {'webseite': 'https://www.freiburg.de/pb/206688.html', 'seiten': [],
                   'portal': ['https://www.leo-bw.de/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/7749/Wiehre']},
    '440-waldsee': {'webseite': 'https://www.freiburg.de/pb/206688.html', 'seiten': [],
                    'portal': ['https://www.leo-bw.de/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/7745/Waldsee']},
    '441-hoellental': {'webseite': 'https://www.gemeinde-breitnau.de/',
                       'seiten': ['https://www.gemeinde-breitnau.de/freizeit-in-breitnau/sehenswertes/hoellental/hirschsprung',
                                  'https://www.gemeinde-breitnau.de/freizeit-in-breitnau/sehenswertes/ravennaschlucht/st-oswald',
                                  'https://www.gemeinde-breitnau.de/freizeit-in-breitnau/sehenswertes/uebersicht',
                                  'https://www.gemeinde-breitnau.de/gemeinde-breitnau/dorfchronik'],
                       'portal': []},
}
DOC = (' Lücken Freiburg–Breitnau (Mike 2026-10-20): Wiehre, Waldsee (Stadtteile, Höllentalbahn ab Hbf) vor Ebnet; Höllental als'
       ' eigener Ort zwischen Buchenbach und Hinterzarten (Hirschsprung, Ravennaschlucht, Hofgut Sternen).')
with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
orte = o['orte']
vorhanden = {e[0] for e in orte}
for slug, name, titel, einheit, lage, anker in NEU:
    if slug in vorhanden:
        print('schon da:', slug); continue
    i = next(i for i, e in enumerate(orte) if e[0] == anker)
    orte.insert(i if lage == 'vor' else i + 1, [slug, 'ziel', name, titel, einheit])
    o['laender'][slug] = 'BW'
    print(slug, lage, anker)
o['quellen_amtlich'].update(Q)
if DOC.strip() not in o['_doc']:
    o['_doc'] += DOC
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte:', len(orte), '| Reihe:', [e[0] for e in orte if e[0] in ('439-wiehre', '440-waldsee', '387-ebnet', '388-littenweiler', '73-buchenbach', '441-hoellental', '74-hinterzarten')])
