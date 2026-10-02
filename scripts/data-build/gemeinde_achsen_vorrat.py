"""Gemeinde-Achsen Iteration 1: Vorrat je Ort aus den drei Kartenläufen zusammenführen.

Im Vorrat ist jede Karte der geprüften Fassungen (karten-geprueft/v0.4, v0.5, v0.6), die der Faktencheck nicht
gesperrt hat und die in data/gemeinde-achsen/iter1/vorrat.json nicht als ersetzt oder raus geführt ist.
Schreibt vorrat-liste.json (aufgelöste Liste) und das Vorrats-Blatt
docs/konzepte/quizaway-stufe2-vorrat-2026-10-02.md: je Ort alle Karten des Vorrats mit Vorderseite, Rückseite,
Urteil des Faktenchecks und Mikes bisherigen Einträgen; kuratiert wird durch Streichen.

Aufruf:  python -X utf8 scripts/data-build/gemeinde_achsen_vorrat.py
"""
import io
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'iter1')
ZIEL = os.path.join(WURZEL, 'docs', 'konzepte', 'quizaway-stufe2-vorrat-2026-10-02.md')
LAEUFE = [('v0.6', 'Karte', 'dritter Lauf'), ('v0.5', 'Karte', 'zweiter Lauf'), ('v0.4', 'Vorschlag', 'erster Lauf')]
FELDER = 'FAKTENCHECK|SORTE|FAMILIE|GEWÄHLTER FAKT|BEKANNTHEIT|VORDERSEITE|RÜCKSEITE|WÖRTER RÜCKSEITE|ANSCHLUSS|NEGATIVNACHWEISE|PRÜFHINWEIS|## '


def feld(v, name):
    m = re.search(r'^%s:?[ \t]*(.*?)(?=^(?:%s))' % (name, FELDER), v + '\n## ENDE', flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def lies_json(name):
    with io.open(os.path.join(ITER, name), encoding='utf-8') as f:
        return json.load(f)


def karten(lauf, kopf, ort):
    pfad = os.path.join(ITER, 'karten-geprueft', lauf, ort + '.md')
    if not os.path.exists(pfad):
        return {}
    with io.open(pfad, encoding='utf-8') as f:
        teile = re.split(r'^##\s*%s\s*(\d+)\s*$' % kopf, f.read(), flags=re.M)
    aus = {}
    for i in range(1, len(teile), 2):
        aus[int(teile[i])] = re.split(r'^##\s*(?:ORTS-ANSCHLUSS|NICHT VERWENDET|UNGEREGELT)', teile[i + 1], flags=re.M)[0]
    return aus


def zitat(text):
    return '\n'.join('> ' + z if z.strip() else '>' for z in text.strip().split('\n') if not z.strip().startswith('STELLE:'))


def familie(v):
    t = feld(v, 'FAMILIE').upper()
    if 'LEITER' in t:
        return 'C-Leiter'
    m = re.match(r'\s*([ABC])\b', t)
    return m.group(1) if m else '?'


def main():
    plan = lies_json('vorrat.json')
    status = {(s['ort'], s['lauf'], s['karte']): s for s in lies_json(os.path.join('faktencheck', 'status.json'))}
    kur = lies_json('kuratierung.json')
    name = {o['slug']: o['name'] for o in lies_json('grunddaten.json')['orte']}
    reihe = kur.get('kartensatz', {}).get('reihe', {})
    liste, aus = [], []
    aus += ['# QuizAway — Stufe 2, Vorrat Raum Freiburg nach drei Läufen',
            '',
            '**Erzeugt am 2026-10-02** mit `scripts/data-build/gemeinde_achsen_vorrat.py` aus den geprüften Fassungen der drei '
            'Kartenläufe (`data/gemeinde-achsen/iter1/karten-geprueft/`). Regel (Mike, 2026-10-02): Tragen zwei Läufe denselben '
            'Fakt, bleibt die Karte aus dem dritten Lauf; gesperrte Karten sind nicht im Vorrat. Welche Karte welche ersetzt, '
            'steht in `data/gemeinde-achsen/iter1/vorrat.json` und hier am Ende jedes Orts.',
            '',
            '**So geht es:** wie beim Blatt davor. Was im Vorrat bleiben soll, bleibt unangekreuzt; nur ankreuzen, was gestrichen '
            'werden soll. Neu sind die Karten mit dem Vermerk „dritter Lauf"; die übrigen kennst du aus den beiden ersten Blättern. '
            'Der Kartensatz für den Tisch bleibt, wie er ist.',
            '',
            '**Faktencheck:** bestätigt = nichts zu ändern · korrigiert = steht hier in der berichtigten Fassung · '
            'unsicher = Auflösung nur durch Wikipedia belegt.',
            '']
    uebersicht = []
    for ort in sorted(plan['orte']):
        p = plan['orte'][ort]
        ersetzt = {(e['lauf'], e['karte']): e for e in p['ersetzt']}
        raus = {(e['lauf'], e['karte']): e for e in p['raus']}
        drin, gesperrt = [], []
        for lauf, kopf, lauf_text in LAEUFE:
            for nr, v in sorted(karten(lauf, kopf, ort).items()):
                s = status.get((ort, lauf, nr))
                if not s:
                    continue
                if s['status'] == 'gesperrt':
                    gesperrt.append((lauf_text, nr, s['grund']))
                elif (lauf, nr) not in ersetzt and (lauf, nr) not in raus:
                    drin.append((lauf, kopf, lauf_text, nr, v, s))
        assert len(drin) <= plan['grenze_je_ort'], (ort, len(drin))
        sorten = [feld(v, 'SORTE').split()[0] if feld(v, 'SORTE') else 'Geschichte' for _, _, _, _, v, _ in drin]
        uebersicht.append((name[ort], len(drin), sum(1 for s in sorten if s.lower().startswith('klass')),
                           sum(1 for d in drin if d[0] == 'v0.6'), len(ersetzt), len(raus), len(gesperrt)))
        aus += ['---', '', '## %s · %s · %d Karten im Vorrat' % (ort[:2], name[ort], len(drin)), '']
        for lauf, kopf, lauf_text, nr, v, s in drin:
            vermerke = []
            if lauf == 'v0.4' and nr in kur['blatt1']['wahl'].get(ort, []):
                vermerke.append('von dir im ersten Blatt angekreuzt')
            if lauf == 'v0.5' and kur['blatt2']['orte'].get(ort, {}).get('zuerst') == nr:
                vermerke.append('deine erste Karte im zweiten Blatt')
            if lauf == 'v0.5' and reihe.get(ort) == nr:
                vermerke.append('im Kartensatz für den Tisch')
            rueck = re.split(r'^\s*Quelle:', feld(v, 'RÜCKSEITE'), flags=re.M)[0].strip()
            sorte = feld(v, 'SORTE').split()[0] if feld(v, 'SORTE') else 'Geschichte'
            liste.append({'ort': ort, 'lauf': lauf, 'karte': nr, 'sorte': sorte, 'familie': familie(v), 'faktencheck': s['status']})
            aus += ['### %s, %s %d · %s · Familie %s    [ ] streichen' % (lauf_text, kopf, nr, sorte, familie(v)), '',
                    zitat(feld(v, 'VORDERSEITE')), '', zitat(rueck), '',
                    '%d Wörter · Faktencheck: **%s**%s%s' % (
                        len(rueck.split()), s['status'],
                        '' if s['status'] == 'bestätigt' else ' – ' + s['grund'],
                        ' · ' + '; '.join(vermerke) if vermerke else ''),
                    '']
        if ersetzt:
            aus += ['**Ersetzt** (derselbe Fakt steht in einer neueren Karte):', '']
            aus += ['- %s %d → %s %d: %s' % (dict((l, t) for l, _, t in LAEUFE)[e['lauf']], e['karte'],
                                             dict((l, t) for l, _, t in LAEUFE)[e['durch'][0]], e['durch'][1], e['fakt'])
                    for e in p['ersetzt']] + ['']
        if raus:
            aus += ['**Aus dem Vorrat genommen:**', ''] + [
                '- %s %d: %s' % (dict((l, t) for l, _, t in LAEUFE)[e['lauf']], e['karte'], e['grund']) for e in p['raus']] + ['']
        if gesperrt:
            aus += ['**Gesperrt nach Faktencheck:**', ''] + ['- %s %d: %s' % g for g in gesperrt] + ['']
    kopf_tab = ['## Übersicht', '', '| Ort | im Vorrat | davon Klassiker | davon dritter Lauf | ersetzt | herausgenommen | gesperrt |', '|---|---|---|---|---|---|---|']
    kopf_tab += ['| %s | %d | %d | %d | %d | %d | %d |' % u for u in uebersicht]
    kopf_tab += ['| **zusammen** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** |' % tuple(sum(u[i] for u in uebersicht) for i in range(1, 7)), '']
    einschub = aus.index('---')
    aus = aus[:einschub] + kopf_tab + aus[einschub:] + ['---', '', '*Ende Vorrat.*', '']
    with io.open(ZIEL, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(aus))
    with io.open(os.path.join(ITER, 'vorrat-liste.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(liste, f, ensure_ascii=False, indent=1)
    for u in uebersicht:
        print('%-14s Vorrat %2d · Klassiker %d · dritter Lauf %2d · ersetzt %d · raus %d · gesperrt %d' % u)
    print('zusammen: %d Karten im Vorrat' % len(liste))
    print('geschrieben:', ZIEL)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
