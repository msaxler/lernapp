"""Breitnau (432) und Kirchzarten (433) in data/gemeinde-achsen/bahn/orte.json an ihren Platz auf der Strecke
Freiburg–Breitnau rücken (Mike 2026-10-19): Kirchzarten vor Stegen, Breitnau zwischen Hinterzarten und Titisee-Neustadt.
Die Reihenfolge bestimmt „Strecke durchtippen“, LETZTER_PIN der Karteneingabe und den Orts-Anschluss im Export.
Aufruf: python -X utf8 scripts/data-build/orte_umsortieren_hoellental_2026-10-19.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
ZIEL = [('433-kirchzarten', 'vor', '71-stegen'), ('432-breitnau', 'nach', '74-hinterzarten')]

with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
orte = o['orte']
for slug, lage, anker in ZIEL:
    eintrag = next(e for e in orte if e[0] == slug)
    orte.remove(eintrag)
    i = next(i for i, e in enumerate(orte) if e[0] == anker)
    orte.insert(i if lage == 'vor' else i + 1, eintrag)
reihe = [e[0] for e in orte]
start = reihe.index('387-ebnet')
print('Strecke:', [s for s in reihe if s in ('387-ebnet', '388-littenweiler', '433-kirchzarten', '71-stegen', '72-oberried', '73-buchenbach',
                                             '74-hinterzarten', '432-breitnau', '75-titisee-neustadt')])
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte:', len(orte))
