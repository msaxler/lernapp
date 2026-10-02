"""Gemeinde-Achsen Iteration 1: Kartensatz für den Feldtest Stufe 2 (generierte Karten) bauen.

Nimmt je Zielort die Karte, die Mike im Kuratierblatt zum zweiten Lauf als erste gewählt hat
(data/gemeinde-achsen/iter1/kuratierung.json, blatt2.orte.<ort>.zuerst), in der geprüften Fassung
(karten-geprueft/v0.5) und schreibt docs/konzepte/quizaway-feldtest-stufe2-kartensatz-freiburg-2026-10-02.md
im Aufbau des handgeschriebenen Kartensatzes: Vorderseite, Rückseite, Anschluss, Quelle, Protokollbogen.
Steht in kuratierung.json ein Block "kartensatz": {"reihe": {<ort>: <Karte>}}, gilt der statt "zuerst".

Aufruf:  python -X utf8 scripts/data-build/gemeinde_achsen_kartensatz_stufe2.py
"""
import io
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
KARTEN = os.path.join(ITER, 'karten-geprueft', 'v0.5')
ZIEL = os.path.join(WURZEL, 'docs', 'konzepte', 'quizaway-feldtest-stufe2-kartensatz-freiburg-2026-10-02.md')
FELDER = 'FAKTENCHECK|SORTE|FAMILIE|FAKT-ID|GEWÄHLTER FAKT|BEKANNTHEIT|VORDERSEITE|RÜCKSEITE|WÖRTER RÜCKSEITE|NEGATIVNACHWEISE|## '
LAUF = 'v0.5'
# ein weiterer Raum (GA_RAUM=neuwied): jüngster Lauf und Name des Kartensatzes aus <raum>/orte.json; die Reihe steht
# in <raum>/kuratierung.json unter kartensatz.reihe
RAUM = {}
if os.path.exists(os.path.join(ITER, 'orte.json')):
    with io.open(os.path.join(ITER, 'orte.json'), encoding='utf-8') as _f:
        RAUM = json.load(_f)
    LAUF = RAUM['laeufe'][0][0]
    KARTEN = os.path.join(ITER, 'karten-geprueft', LAUF)
    ZIEL = os.path.join(WURZEL, 'docs', 'konzepte', RAUM['kartensatz'])


def feld(v, name):
    m = re.search(r'^%s:?[ \t]*(.*?)(?=^(?:%s))' % (name, FELDER), v + '\n## ENDE', flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def lies_json(name):
    with io.open(os.path.join(ITER, name), encoding='utf-8') as f:
        return json.load(f)


def main():
    kur = lies_json('kuratierung.json')
    reihe = kur.get('kartensatz', {}).get('reihe') or {o: v['zuerst'] for o, v in kur['blatt2']['orte'].items()}
    gewaehlt = {o: v['zuerst'] for o, v in kur['blatt2']['orte'].items()}
    pruefung = lies_json('karten-%s-geprueft-pruefung.json' % LAUF)
    geprueft = {(k['ort'], k['karte']): k for k in pruefung['karten']}
    anschluss = {o['ort']: o['anschluesse'] for o in pruefung['orte']}
    name = {o['slug']: o['name'] for o in lies_json('grunddaten.json')['orte']}
    orte = sorted(reihe)
    familien = [geprueft[(o, reihe[o])]['familie'] for o in orte]
    doppelt = sum(1 for a, b in zip(familien, familien[1:]) if a[0] == b[0])

    aus = ['# QuizAway — Feldtest Stufe 2, Solo am Tisch: Kartensatz Raum Freiburg (generierte Karten)',
           '',
           '**Erzeugt am 2026-10-02** mit `scripts/data-build/gemeinde_achsen_kartensatz_stufe2.py` aus dem Vorrat des zweiten '
           'Volllaufs (Karten-Prompt v0.5), in der Fassung nach dem Faktencheck. '
           + ('Reihe nach Entscheid Mike (2026-10-02): gemischt, damit die Varianzregel hält; seine ersten Karten aus dem Kuratierblatt '
              '`quizaway-stufe2-kuratierblatt-v2-2026-10-01.md` stehen in der Reihe oder unter Nachschlag.'
              if kur.get('kartensatz', {}).get('reihe') else
              'Je Ort die Karte, die Mike im Kuratierblatt `quizaway-stufe2-kuratierblatt-v2-2026-10-01.md` als erste gewählt hat.'),
           '',
           '**Zweck:** Stufe 2 nach Spielkonzept v0.2.6 §10: dieselben zehn Orte wie der handgeschriebene Kartensatz, aber Karten '
           'aus der Pipeline (Extraktion, Kartenlauf, Faktencheck, Kuratieren). Gemessen wird, ob generierte Karten am Tisch eine '
           'Theorie hervorrufen, mit denselben Größen wie in Stufe 1 (T0/T1/T2/W, K1 dreiteilig).',
           '',
           '**Zusammensetzung:** 10 Orte · Familien %s · %s' % (
               ' '.join(familien),
               'Varianzregel eingehalten.' if not doppelt else
               '**Varianzregel nicht eingehalten:** %d-mal folgt dieselbe Familie auf sich selbst (§1 Schritt 2 verlangt Wechsel). '
               'Der Satz misst so die Karten, nicht die Abwechslung.' % doppelt),
           '',
           '**Testperson:** kennt den Raum Freiburg nicht gut und hat den handgeschriebenen Kartensatz nicht gespielt. '
           'Die Orte sind dieselben; wer Stufe 1 kennt, erkennt Umkirch, Glottertal und Staufen wieder (Kürzel W).',
           '',
           '**Ablauf, Instruktion und Unterbrechungen** wie im handgeschriebenen Kartensatz '
           '(`quizaway-feldtest-solo-kartensatz-freiburg-v2-2026-10-01.md`, Abschnitt Vorbereitung): Karten auf A6, Think-Aloud, '
           'der Beobachter fragt nicht nach.',
           '',
           '**Anschluss:** Er hängt am Ortspaar und steht unter der Rückseite. Er gilt nur, wenn der Ort davor wirklich gespielt wurde.',
           '', '---', '', '## Die Karten', '']
    if RAUM:
        aus = ['# QuizAway — Feldtest Stufe 2, Solo am Tisch: Kartensatz Raum %s (generierte Karten)' % RAUM['raum'],
               '',
               '**Erzeugt am 2026-10-02** mit `scripts/data-build/gemeinde_achsen_kartensatz_stufe2.py` (GA_RAUM=%s) aus dem '
               'Vorrat des Raums (Karten-Prompt %s), in der Fassung nach dem Faktencheck. %s' % (
                   os.path.basename(ITER), LAUF, kur.get('kartensatz', {}).get('_doc', '')),
               '',
               '**Zweck:** Stufe 2 nach Spielkonzept v0.2.7 §10 in einem zweiten Raum: Karten aus der Pipeline (Extraktion, '
               'Kartenlauf, Faktencheck, Kuratieren). Gemessen wird, ob generierte Karten am Tisch eine Theorie hervorrufen, '
               'mit denselben Größen wie in Stufe 1 (T0/T1/T2/W, K1 dreiteilig).',
               '',
               '**Zusammensetzung:** %d Orte · Familien %s · %s' % (
                   len(orte), ' '.join(familien),
                   'Varianzregel eingehalten.' if not doppelt else
                   '**Varianzregel nicht eingehalten:** %d-mal folgt dieselbe Familie auf sich selbst.' % doppelt),
               '',
               '**Testperson:** kennt den Raum %s nicht gut.' % RAUM['raum'],
               '',
               '**Ablauf, Instruktion und Unterbrechungen** wie im handgeschriebenen Kartensatz '
               '(`quizaway-feldtest-solo-kartensatz-freiburg-v2-2026-10-01.md`, Abschnitt Vorbereitung): Karten auf A6, '
               'Think-Aloud, der Beobachter fragt nicht nach.',
               '',
               '**Anschluss:** Er hängt am Ortspaar und steht unter der Rückseite. Er gilt nur, wenn der Ort davor wirklich '
               'gespielt wurde.',
               '', '---', '', '## Die Karten', '']
    def block(ort, nr, titel, vorgaenger, vermerk):
        """Eine Karte im Aufbau des handgeschriebenen Satzes; vorgaenger = Name des Orts davor oder None."""
        p = geprueft[(ort, nr)]
        with io.open(os.path.join(KARTEN, ort + '.md'), encoding='utf-8') as f:
            teile = re.split(r'^##\s*Karte\s*(\d+)\s*$', f.read(), flags=re.M)
        v = next(teile[i + 1] for i in range(1, len(teile), 2) if int(teile[i]) == nr)
        v = re.split(r'^##\s*(?:ORTS-ANSCHLUSS|NICHT VERWENDET|UNGEREGELT)', v, flags=re.M)[0]
        vorn = [z.strip() for z in feld(v, 'VORDERSEITE').split('\n') if z.strip() and not z.strip().startswith('STELLE:')]
        optionen = [re.sub(r'^(\d)[.):]?\s+', r'\1. ', z) for z in vorn if re.match(r'^\d[.):]?\s', z)]
        text = [z for z in vorn if not re.match(r'^\d[.):]?\s', z)]
        rueck_feld = feld(v, 'RÜCKSEITE')
        rueck = re.split(r'^\s*Quelle:', rueck_feld, flags=re.M)[0].strip()
        rueck = rueck.replace('Du hattest [Option] getippt.', '*Du hattest [Option] getippt.*', 1)
        rueck = re.sub(r'((?:Richtig war|Die Lüge war) \d\.|Höher bis Stufe \d, dann raus\.)', r'**\1**', rueck)
        quelle = re.search(r'^\s*Quelle:\s*(.+)$', rueck_feld, flags=re.M)
        z = ['### %s — %s · Familie %s · %s' % (titel, name[ort], p['familie'], p['sorte']), '',
             '**Vorderseite**', '',
             '> **%s.** %s' % (text[0], text[1] if len(text) > 1 else ''), '>',
             '> ' + ' '.join(text[2:]), '>'] + ['> ' + o for o in optionen] + ['',
             '**Rückseite**', '',
             '> ' + rueck]
        if vorgaenger and anschluss.get(ort):
            z += ['>', '> *Anschluss an %s:* %s' % (vorgaenger, anschluss[ort][0])]
        z += ['>', '> *Quelle: %s*' % (quelle.group(1).strip() if quelle else '?'), '',
              'Vorrat %s, Karte %d%s · %d Wörter · Bekanntheit %s · Faktencheck: %s%s' % (
                  name[ort], nr, vermerk, p['woerter_rueckseite'], p['bekanntheit'], p['faktencheck'],
                  '' if p['faktencheck'] == 'bestätigt' else ' (%s)' % p['faktencheck_grund']),
              '', '---', '']
        return z

    for n, ort in enumerate(orte, 1):
        anders = '' if gewaehlt.get(ort) in (None, reihe[ort]) else ' · Mikes erste Wahl, Karte %d, steht unter Nachschlag' % gewaehlt[ort]
        aus += block(ort, reihe[ort], 'Karte %d' % n, name[orte[n - 2]] if n > 1 else None, anders)
    nachschlag = [o for o in orte if gewaehlt.get(o) and gewaehlt[o] != reihe[o]]
    if nachschlag:
        aus += ['## Nachschlag', '',
                'Die Karten, die Mike je Ort als erste gewählt hat und die wegen der Varianzregel nicht in der Reihe stehen. '
                'Sie bleiben im Vorrat des Orts und sind die nächste Karte, wenn jemand zu einem Ort mehr wissen will. '
                'Nach Spielkonzept §1 Schritt 5 wird Nachschlag nie angeboten: Der Beobachter legt die Karte nur hin, '
                'wenn die Person von selbst danach fragt, und vermerkt es im Bogen.', '']
        for ort in nachschlag:
            aus += block(ort, gewaehlt[ort], 'Nachschlag %s' % ort[:2], None, ' · Mikes erste Wahl')
    aus += ['## Protokollbogen', '',
            'Vor Beginn: Kennt die Person den Raum %s? ______%s' % (
                RAUM.get('raum', 'Freiburg'), '' if RAUM else ' · Hat sie den handgeschriebenen Kartensatz gespielt? ______'),
            '',
            '| Karte | Ort | vor dem Umdrehen: T0 / T1 / T2 / W | Theorie in Stichworten | nach dem Umdrehen: nennt eigene Theorie / nennt den Grund / sagt, warum die Theorie plausibel oder falsch war | getippt | Anmerkung |',
            '|---|---|---|---|---|---|---|']
    aus += ['| %d | %s | | | | | |' % (n, name[o]) for n, o in enumerate(orte, 1)]
    aus += ['', 'T0 keine Theorie · T1 Auswahl ohne Begründung · T2 Theorie mit Begründung · W gewusst oder wiedererkannt (woher?). '
            'Nach Karte 3, 6 und 8 eine kurze Unterbrechung; notieren, ob die Person von selbst weitermacht.',
            '', '*Ende Kartensatz.*', '']
    with io.open(ZIEL, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(aus))
    print('geschrieben:', ZIEL)
    print('Familien:', ' '.join(familien), '· gleiche Familie hintereinander:', doppelt)
    for n, o in enumerate(orte, 1):
        p = geprueft[(o, reihe[o])]
        print('  %2d %-14s Karte %d %-8s %-10s %-11s %s' % (n, name[o], reihe[o], p['familie'], p['sorte'], p['faktencheck'], p['frage'][:70]))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
