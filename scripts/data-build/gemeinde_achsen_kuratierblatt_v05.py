"""Gemeinde-Achsen Iteration 1, zweiter Volllauf: Kuratierblatt aus den Karten des Prompts v0.5 bauen.

Liest data/gemeinde-achsen/iter1/karten-v0.5/*.md und karten-v0.5-pruefung.json und schreibt
docs/konzepte/quizaway-stufe2-kuratierblatt-v2-2026-10-01.md: je Zielort der Vorrat von sieben Karten mit
Vorderseite, Rückseite, Wortzahl, Bekanntheit und Wegen der Negativnachweise, dazu die Orts-Anschlüsse.
Kuratiert wird durch Streichen: Was nicht angekreuzt ist, bleibt im Vorrat.

Aufruf:  python -X utf8 scripts/check/gemeinde_achsen_karten_pruefen_v05.py
         python -X utf8 scripts/data-build/gemeinde_achsen_kuratierblatt_v05.py
"""
import glob
import io
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'iter1')
# Nach dem Faktencheck: geprüfte Fassung (Korrekturen eingearbeitet, Status je Karte)
KARTEN = os.path.join(ITER, 'karten-geprueft', 'v0.5')
PRUEFUNG = os.path.join(ITER, 'karten-v0.5-geprueft-pruefung.json')
ZIEL = os.path.join(WURZEL, 'docs', 'konzepte', 'quizaway-stufe2-kuratierblatt-v2-2026-10-01.md')
FELDER = 'FAKTENCHECK|SORTE|FAMILIE|GEWÄHLTER FAKT|BEKANNTHEIT|VORDERSEITE|RÜCKSEITE|WÖRTER RÜCKSEITE|NEGATIVNACHWEISE|## '


def feld(v, name):
    m = re.search(r'^%s:?[ \t]*(.*?)(?=^(?:%s))' % (name, FELDER), v + '\n## ENDE', flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def zitat(text):
    # Eine Zeile "STELLE: n" gehört in den PLAN, nicht auf die Karte (Kirchzarten, Karte 2)
    return '\n'.join('> ' + z if z.strip() else '>' for z in text.strip().split('\n') if not z.strip().startswith('STELLE:'))


def main():
    with io.open(os.path.join(ITER, 'grunddaten.json'), encoding='utf-8') as f:
        name = {o['slug']: o['name'] for o in json.load(f)['orte']}
    with io.open(PRUEFUNG, encoding='utf-8') as f:
        pruefung = json.load(f)
    geprueft = {(k['ort'], k['karte']): k for k in pruefung['karten']}
    orte = {o['ort']: o for o in pruefung['orte']}
    aus = ['# QuizAway — Stufe 2, Kuratierblatt zum zweiten Volllauf (Raum Freiburg)',
           '',
           '**Erzeugt am 2026-10-01** aus `data/gemeinde-achsen/iter1/karten-v0.5/` mit '
           '`scripts/data-build/gemeinde_achsen_kuratierblatt_v05.py`. Karten-Prompt v0.5, Spielkonzept v0.2.6: '
           'je Ort ein Vorrat von sieben Karten (Geschichten und Klassiker), Bekanntheit sperrt nicht. '
           'Bericht dazu: `quizaway-stufe2-volllauf2-2026-10-01.md`.',
           '',
           '**Faktencheck (2026-10-02):** Jede Karte ist gegen den Wikipedia-Artikel, gegen eine zweite Quelle im Netz und auf '
           'zufällig wahre falsche Optionen geprüft (`data/gemeinde-achsen/iter1/faktencheck/`). **bestätigt:** nichts zu ändern. '
           '**korrigiert:** Die Karte steht hier schon in der berichtigten Fassung, der Grund steht dabei. '
           '**unsicher:** Die Auflösung steht nur in Wikipedia; spielbar, aber ohne zweiten Beleg. '
           '**gesperrt:** so nicht spielbar; bleibt bis zu einer Neufassung aus dem Vorrat.',
           '',
           '**So geht es:** Was im Vorrat bleiben soll, bleibt unangekreuzt. Nur ankreuzen, was gestrichen werden soll; '
           'wer eine Karte umformulieren will, schreibt es dazu. Je Ort eine Zahl: welche Karte im Feldtest zuerst gespielt wird. '
           'Die vollständigen Ausgaben mit allen Negativnachweisen stehen in den Kartendateien.',
           '']
    for pfad in sorted(glob.glob(os.path.join(KARTEN, '*.md'))):
        slug = os.path.splitext(os.path.basename(pfad))[0]
        with io.open(pfad, encoding='utf-8') as f:
            text = f.read()
        o = orte[slug]
        aus += ['---', '', '## %s · %s · %d Karten (%d Geschichten, %d Klassiker)' % (
            slug[:2], name[slug], o['karten'], o['geschichten'], o['klassiker']), '']
        teile = re.split(r'^##\s*Karte\s*(\d)\s*$', text, flags=re.M)
        for i in range(1, len(teile), 2):
            v = re.split(r'^##\s*(?:ORTS-ANSCHLUSS|NICHT VERWENDET|UNGEREGELT)', teile[i + 1], flags=re.M)[0]
            nr = int(teile[i])
            p = geprueft[(slug, nr)]
            rueck = re.split(r'^\s*Quelle:', feld(v, 'RÜCKSEITE'), flags=re.M)[0].strip()
            gesperrt = p['faktencheck'] == 'gesperrt'
            aus += ['### Karte %d · %s · Familie %s    %s' % (
                        nr, p['sorte'], p['familie'], '**gesperrt nach Faktencheck**' if gesperrt else '[ ] streichen'), '',
                    zitat(feld(v, 'VORDERSEITE')), '', zitat(rueck), '',
                    '%d Wörter · Bekanntheit %s · Negativnachweis Weg %s%s' % (
                        p['woerter_rueckseite'], p['bekanntheit'], p['wege'] or '?',
                        ' · **Prüfung: %s**' % '; '.join(p['fehler']) if p['fehler'] else ''),
                    '',
                    'Faktencheck: **%s**%s' % (p['faktencheck'], '' if p['faktencheck'] == 'bestätigt' else ' – ' + p['faktencheck_grund']),
                    '']
        if o['anschluesse']:
            aus += ['**Orts-Anschluss** (an den Ort davor, passt hinter jede Karte):', ''] + ['- ' + a for a in o['anschluesse']] + ['']
        if o['anschluss_kandidaten']:
            aus += ['**Anschluss-Kandidat über einen Namensteil** (nicht verwendet, wartet auf Entscheid):', ''] + [
                '- ' + a for a in o['anschluss_kandidaten']] + ['']
        aus += ['**Zuerst spielen:** Karte ___', '']
    aus += ['---', '', '*Ende Kuratierblatt.*', '']
    with io.open(ZIEL, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(aus))
    print('geschrieben:', ZIEL, len(aus), 'Zeilen')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
