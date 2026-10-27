"""Mike 2026-10-26: Essen um Heisingen als Ortsporträt v0.9 (16 vorhandene Orte) plus sechs Nachbar-Stadtteile neu.
Wikipedia-Titel am 26.10. geprüft: vorhanden, keine Begriffsklärung (Kray wäre Begriffsklärung, nicht gewählt).
Einfügen nach 431-kettwig, grob von Südwest nach Ost. Einheit „Ortsteil von Essen“ (grunddaten erkennt nur diese Form).
Aufruf: python -X utf8 scripts/data-build/orte_eintragen_essen_ring3_2026-10-26.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
E = 'Ortsteil von Essen'
NEU = [('490-schuir', 'Schuir', 'Schuir'),
       ('491-heidhausen', 'Heidhausen', 'Heidhausen (Essen)'),
       ('492-haarzopf', 'Haarzopf', 'Haarzopf'),
       ('493-margarethenhoehe', 'Margarethenhöhe', 'Margarethenhöhe'),
       ('494-suedostviertel', 'Südostviertel', 'Südostviertel'),
       ('495-freisenbruch', 'Freisenbruch', 'Freisenbruch')]
with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
orte = o['orte']
vorhanden = {e[0] for e in orte}
i = next(i for i, e in enumerate(orte) if e[0] == '431-kettwig') + 1
for slug, name, titel in NEU:
    if slug in vorhanden:
        print('schon da:', slug); continue
    orte.insert(i, [slug, 'ziel', name, titel, E]); i += 1
    o['laender'][slug] = 'NW'
o['_doc'] += (' Essen Ring 3 (Mike 2026-10-26): Schuir, Heidhausen, Haarzopf, Margarethenhöhe, Südostviertel, Freisenbruch'
              ' (490–495) nach Kettwig; die 16 Essener Orte als Ortsporträt v0.9.')
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte:', len(orte))
