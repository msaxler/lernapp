"""Mike 2026-10-20: alle noch fehlenden Freiburger Stadtteile als Ortsporträt. 20 neu im Raum bahn (444–463), Hochdorf (397)
besteht schon; Zähringen und Günterstal lagen bisher nur im Raum iter1 (Zähringen hier neu, Günterstal 436 läuft).
Quellen: LEO-BW-Ortslexikon als Landesportal, wo es eine Altgemeinde-Seite gibt; Ortschaften mit eigener Verwaltung über
ihre freiburg.de-Seite (Krabbler findet Ortschronik/Geschichtliches); Wikipedia immer. Reihenfolge: nach Waldsee, grob vom
Zentrum nach außen. Aufruf: python -X utf8 scripts/data-build/orte_eintragen_freiburg_stadtteile_2026-10-20.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
LEO = 'https://www.leo-bw.de/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/%d/%s'
E = 'Ortsteil von Freiburg im Breisgau'
# slug, Name, Wikipedia-Titel, LEO-BW-Nummer (0 = keine), Ortschaftsseite freiburg.de (None = keine)
NEU = [('444-altstadt-freiburg', 'Altstadt', 'Altstadt (Freiburg im Breisgau)', 7705, None),
       ('445-stuehlinger', 'Stühlinger', 'Stühlinger', 7742, None),
       ('446-neuburg-freiburg', 'Neuburg', 'Neuburg (Freiburg im Breisgau)', 7728, None),
       ('447-herdern', 'Herdern', 'Herdern (Freiburg im Breisgau)', 7716, None),
       ('448-zaehringen', 'Zähringen', 'Zähringen (Freiburg im Breisgau)', 7751, None),
       ('449-bruehl-freiburg', 'Brühl', 'Brühl (Freiburg im Breisgau)', 7709, None),
       ('450-oberau', 'Oberau', 'Oberau (Freiburg im Breisgau)', 7730, None),
       ('451-haslach-freiburg', 'Haslach', 'Haslach (Freiburg im Breisgau)', 7715, None),
       ('452-sankt-georgen', 'Sankt Georgen', 'Sankt Georgen (Freiburg im Breisgau)', 7738, None),
       ('453-vauban', 'Vauban', 'Vauban (Freiburg im Breisgau)', 7744, None),
       ('454-weingarten-freiburg', 'Weingarten', 'Weingarten (Freiburg im Breisgau)', 7747, None),
       ('455-betzenhausen', 'Betzenhausen', 'Betzenhausen', 7708, None),
       ('456-mooswald', 'Mooswald', 'Mooswald (Freiburg im Breisgau)', 7725, None),
       ('457-landwasser', 'Landwasser', 'Landwasser (Freiburg im Breisgau)', 7721, None),
       ('458-lehen-freiburg', 'Lehen', 'Lehen (Freiburg im Breisgau)', 7722, 'https://www.freiburg.de/pb/207752.html'),
       ('459-rieselfeld', 'Rieselfeld', 'Rieselfeld (Freiburg im Breisgau)', 0, None),
       ('460-dietenbach', 'Dietenbach', 'Dietenbach (Freiburg im Breisgau)', 0, None),
       ('461-opfingen', 'Opfingen', 'Opfingen', 7731, 'https://www.freiburg.de/pb/207840.html'),
       ('462-tiengen-freiburg', 'Tiengen', 'Tiengen (Freiburg im Breisgau)', 7743, 'https://www.freiburg.de/pb/207636.html'),
       ('463-munzingen', 'Munzingen', 'Munzingen', 7727, 'https://www.freiburg.de/pb/207600.html'),
       ('464-waltershofen', 'Waltershofen', 'Waltershofen (Freiburg im Breisgau)', 7746, 'https://www.freiburg.de/pb/207848.html')]
with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
orte = o['orte']
vorhanden = {e[0] for e in orte}
i = next(i for i, e in enumerate(orte) if e[0] == '440-waldsee') + 1
for slug, name, titel, leo, web in NEU:
    if slug in vorhanden:
        print('schon da:', slug); continue
    orte.insert(i, [slug, 'ziel', name, titel, E]); i += 1
    o['laender'][slug] = 'BW'
    q = {'webseite': web or 'https://www.freiburg.de/pb/206688.html', 'seiten': [web] if web else [],
         'portal': [LEO % (leo, name)] if leo else []}
    o['quellen_amtlich'][slug] = q
# Hochdorf (397) besteht: Ortschaftsseite und LEO-BW nachtragen
o['quellen_amtlich']['397-hochdorf-freiburg'] = {'webseite': 'https://www.freiburg.de/pb/207672.html', 'seiten': ['https://www.freiburg.de/pb/207672.html'],
                                                 'portal': [LEO % (7717, 'Hochdorf')]}
o['_doc'] += ' Alle Freiburger Stadtteile (Mike 2026-10-20): 444–464 neu nach Waldsee, Hochdorf 397 mit LEO-BW; Quellen LEO-BW + Ortschaftsseiten + Wikipedia.'
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte:', len(orte))
