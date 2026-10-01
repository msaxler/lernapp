"""Gemeinde-Achsen Iteration 1: Faktencheck-Dateien auswerten.

Liest data/gemeinde-achsen/iter1/faktencheck/<slug>.md (je Ort zehn Abschnitte mit URTEIL und BEFUND,
Format siehe faktencheck/auftrag.txt) und schreibt faktencheck/urteile.json. Druckt je Ort die Zahl der
Urteile und alle Befunde.

Aufruf:  python -X utf8 scripts/check/gemeinde_achsen_faktencheck_auswerten.py [--befunde]
"""
import glob
import io
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FC = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'iter1', 'faktencheck')
FELDER = 'URTEIL|KERNAUSSAGE|ARTIKEL|ZWEITE QUELLE|FALSCHE OPTIONEN|BEFUND|## '


def feld(text, name):
    m = re.search(r'^%s:[ \t]*(.*?)(?=^(?:%s))' % (name, FELDER), text + '\n## ENDE', flags=re.S | re.M)
    return ' '.join(m.group(1).split()) if m else ''


def main():
    alle = []
    for pfad in sorted(glob.glob(os.path.join(FC, '[0-9]*.md'))):
        slug = os.path.splitext(os.path.basename(pfad))[0]
        with io.open(pfad, encoding='utf-8') as f:
            text = f.read()
        teile = re.split(r'^##\s*(v0\.[45])\s+(Karte|Vorschlag)\s+(\d)\s*$', text, flags=re.M)
        zahl = {'OK': 0, 'KORRIGIEREN': 0, 'UNSICHER': 0}
        for i in range(1, len(teile), 4):
            rest = re.split(r'^##\s*(?:ANSCHLÜSSE|ZUSAMMENFASSUNG)', teile[i + 3], flags=re.M)[0]
            urteil = (feld(rest, 'URTEIL').split() or ['?'])[0].strip('*')
            zahl[urteil] = zahl.get(urteil, 0) + 1
            alle.append({'ort': slug, 'lauf': teile[i], 'karte': int(teile[i + 2]), 'urteil': urteil,
                         'kernaussage': feld(rest, 'KERNAUSSAGE'), 'artikel': feld(rest, 'ARTIKEL'),
                         'zweite_quelle': feld(rest, 'ZWEITE QUELLE'), 'falsche_optionen': feld(rest, 'FALSCHE OPTIONEN'),
                         'befund': feld(rest, 'BEFUND')})
        print('%-16s %s' % (slug, ' · '.join('%s %d' % kv for kv in zahl.items())))
    with io.open(os.path.join(FC, 'urteile.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(alle, f, ensure_ascii=False, indent=1)
    gesamt = {}
    for a in alle:
        gesamt[a['urteil']] = gesamt.get(a['urteil'], 0) + 1
    print('gesamt: %d Karten · %s' % (len(alle), ' · '.join('%s %d' % kv for kv in sorted(gesamt.items()))))
    print('ohne zweite Quelle:', sum(1 for a in alle if a['zweite_quelle'].lower().startswith('keine')))
    if '--befunde' in sys.argv:
        for a in alle:
            if a['urteil'] != 'OK':
                print('\n%s %s %d [%s]\n  %s\n  Falsche Optionen: %s' % (a['ort'], a['lauf'], a['karte'], a['urteil'], a['befund'], a['falsche_optionen'][:300]))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
