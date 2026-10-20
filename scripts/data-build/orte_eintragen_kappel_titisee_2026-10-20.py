"""Mike 2026-10-20: Kappel (Freiburger Stadtteil, Ortschaft) und Titisee (Ortsteil von Titisee-Neustadt, Wikipedia-Artikel = der See)
als Orte der Strecke. Zarten, Burg am Wald und Oberbirken haben keinen eigenen Wikipedia-Artikel (Weiterleitung auf Kirchzarten)
und bleiben im Ortsporträt Kirchzarten. Kappel vor Ebnet (Ortschaft am Dreisamtal-Südrand), Titisee vor Titisee-Neustadt.
Aufruf: python -X utf8 scripts/data-build/orte_eintragen_kappel_titisee_2026-10-20.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
NEU = [('442-kappel', 'Kappel', 'Kappel (Freiburg im Breisgau)', 'Ortsteil von Freiburg im Breisgau', 'nach', '388-littenweiler'),
       ('443-titisee', 'Titisee', 'Titisee', 'Ortsteil von Titisee-Neustadt', 'vor', '75-titisee-neustadt')]
Q = {
    '442-kappel': {'webseite': 'https://www.freiburg.de/pb/206688.html', 'seiten': [],
                   'portal': ['https://www.leo-bw.de/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/7718/Kappel']},
    '443-titisee': {'webseite': 'https://www.titisee-neustadt.de/', 'seiten': [], 'portal': []},
}
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
o['_doc'] += ' Kappel (Ortschaft) und Titisee (Ortsteil, Artikel = See) dazu (Mike 2026-10-20); Zarten, Burg am Wald, Oberbirken ohne eigenen Artikel bleiben in Kirchzarten.'
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte:', len(orte))
