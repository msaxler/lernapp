"""Mike 2026-10-26: Autostrecke Neuwied–Essen-Heisingen (OSRM: B256–A3–A46/A535–A44) als Ortsporträt v0.9.
Neu im Raum bahn: Neuwied (bisher gar kein Ort), Altwied und Rengsdorf (bisher nur Raum neuwied, wie Günterstal/Kirchzarten
aus iter1) und die Westerwald-Lücke an der B256/A3 zwischen Hardert und Breitscheid (Gemeinden <= 1 km neben der Route,
dazu Horhausen 2,3 km als größter Ort). Wikipedia-Titel am 26.10. geprüft. Reihenfolge = Hinfahrt.
Aufruf: python -X utf8 scripts/data-build/orte_eintragen_autostrecke_neuwied_essen_2026-10-26.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
VOR_NIEDERBIEBER = [('496-neuwied', 'Neuwied', 'Neuwied', 'Stadt'),
                    ('497-altwied', 'Altwied', 'Altwied', 'Ortsteil von Neuwied'),
                    ('498-rengsdorf', 'Rengsdorf', 'Rengsdorf', 'Gemeinde')]
VOR_BREITSCHEID = [('499-bonefeld', 'Bonefeld', 'Bonefeld', 'Gemeinde'),
                   ('500-strassenhaus', 'Straßenhaus', 'Straßenhaus', 'Gemeinde'),
                   ('501-oberhonnefeld-gierend', 'Oberhonnefeld-Gierend', 'Oberhonnefeld-Gierend', 'Gemeinde'),
                   ('502-willroth', 'Willroth', 'Willroth', 'Gemeinde'),
                   ('503-horhausen', 'Horhausen', 'Horhausen (Westerwald)', 'Gemeinde'),
                   ('504-huemmerich', 'Hümmerich', 'Hümmerich', 'Gemeinde'),
                   ('505-krunkel', 'Krunkel', 'Krunkel', 'Gemeinde')]
with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
orte = o['orte']
vorhanden = {e[0] for e in orte}
for vor, neu in (('404-niederbieber', VOR_NIEDERBIEBER), ('415-breitscheid-westerwald', VOR_BREITSCHEID)):
    i = next(i for i, e in enumerate(orte) if e[0] == vor)
    for slug, name, titel, einheit in neu:
        if slug in vorhanden:
            print('schon da:', slug); continue
        orte.insert(i, [slug, 'ziel', name, titel, einheit]); i += 1
        o['laender'][slug] = 'RP'
# Altwied: Stadtteilseite wie Niederbieber/Segendorf/Oberbieber
o['quellen_amtlich']['497-altwied'] = {'webseite': 'https://www.neuwied.de/stadtleben/standort/stadtteile/altwied',
                                       'seiten': ['https://www.neuwied.de/stadtleben/standort/stadtteile/altwied']}
o['_doc'] += (' Autostrecke Neuwied–Heisingen als Ortsporträt (Mike 2026-10-26): Neuwied, Altwied, Rengsdorf (496–498) vor'
              ' Niederbieber; Westerwald-Lücke B256/A3 Bonefeld, Straßenhaus, Oberhonnefeld-Gierend, Willroth, Horhausen,'
              ' Hümmerich, Krunkel (499–505) vor Breitscheid.')
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte:', len(orte))
