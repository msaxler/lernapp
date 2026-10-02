"""Gemeinde-Achsen Iteration 1: Gegenprobe der Bindung Karte → Fakt.

Vergleicht die Abfrage "derselbe Fakt" (gleicher schluessel in karten-fakt.json) mit den 49 Zuordnungen,
die am 2026-10-02 von Hand getroffen wurden (vorrat-von-hand-2026-10-02.json, die alte vorrat.json):
  A  von Hand ersetzt, Abfrage sagt: verschiedene Fakten
  B  Abfrage sagt: derselbe Fakt, von Hand nicht als ersetzt geführt
Beides muss leer sein oder in karten-fakt-von-hand.json / fakten-gleich.json begründet aufgelöst.

Aufruf:  python -X utf8 scripts/check/gemeinde_achsen_fakt_gegenprobe.py
"""
import io
import json
import os
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))


def lies_json(name):
    with io.open(os.path.join(ITER, name), encoding='utf-8') as f:
        return json.load(f)


def main():
    bindung = {(b['ort'], b['lauf'], b['karte']): b for b in lies_json('karten-fakt.json')}
    hand = lies_json('vorrat-von-hand-2026-10-02.json')
    gesperrt = set((s['ort'], s['lauf'], s['karte']) for s in lies_json(os.path.join('faktencheck', 'status.json'))
                   if s['status'] == 'gesperrt')
    # was heute aus anderem Grund raus ist, muss die Abfrage nicht finden (Günterstal v0.5 4: Wahlergebnis der ganzen Stadt)
    heute_raus = set((ort, e['lauf'], e['karte']) for ort, p in lies_json('vorrat.json')['orte'].items() for e in p['raus'])
    paare_hand, a, anders = set(), [], 0
    for ort, p in sorted(hand['orte'].items()):
        for e in p['ersetzt']:
            alt, neu = (ort, e['lauf'], e['karte']), (ort, e['durch'][0], e['durch'][1])
            paare_hand.add(frozenset((alt, neu)))
            if alt in heute_raus:
                anders += 1
            elif bindung[alt]['schluessel'] != bindung[neu]['schluessel']:
                a.append('%s %s %d → %s %d „%s“: %s (%s) ≠ %s (%s)' % (
                    ort, e['lauf'], e['karte'], e['durch'][0], e['durch'][1], e['fakt'],
                    bindung[alt]['schluessel'], bindung[alt]['bezeichnung'][:30],
                    bindung[neu]['schluessel'], bindung[neu]['bezeichnung'][:30]))
    # von Hand ersetzte Karten hängen in Ketten (v0.4 → v0.6 und v0.5 → v0.6): Gruppen bilden
    gruppe = {}
    for paar in paare_hand:
        x, y = tuple(paar)
        gx, gy = gruppe.get(x, {x}), gruppe.get(y, {y})
        neu = gx | gy
        for k in neu:
            gruppe[k] = neu
    raus = set((ort, e['lauf'], e['karte']) for ort, p in hand['orte'].items() for e in p['raus'])
    b, je_schluessel = [], {}
    for k, v in bindung.items():
        if k not in gesperrt and k not in raus:
            je_schluessel.setdefault(v['schluessel'], []).append(k)
    for s, ks in sorted(je_schluessel.items()):
        for i, x in enumerate(ks):
            for y in ks[i + 1:]:
                if y not in gruppe.get(x, {x}):
                    b.append('%s: %s %d und %s %d (%s)' % (s, x[1], x[2], y[1], y[2], bindung[x]['bezeichnung'][:40]))
    print('von Hand: %d Zuordnungen · heute als raus geführt: %d · A (Abfrage findet sie nicht): %d · B (Abfrage findet mehr): %d' % (
        sum(len(p['ersetzt']) for p in hand['orte'].values()), anders, len(a), len(b)))
    for z in a:
        print('  A', z)
    for z in b:
        print('  B', z)
    return 1 if a or b else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
