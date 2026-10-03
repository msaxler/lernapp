"""Gemeinde-Achsen Iteration 1: Vorrat je Ort aus den drei Kartenläufen zusammenführen.

Im Vorrat ist jede Karte der geprüften Fassungen (karten-geprueft/v0.4, v0.5, v0.6), die
  - der Faktencheck nicht gesperrt hat,
  - nicht durch eine jüngere Karte zum selben Fakt ersetzt ist (Abfrage über karten-fakt.json: gleicher
    Schlüssel, es bleibt die Karte des jüngsten Laufs; Regel Mike 2026-10-02),
  - in vorrat.json nicht als raus geführt ist,
  - Mike nicht gestrichen hat (kuratierung.json, Abschnitt "vorrat").
Schreibt vorrat-liste.json (aufgelöste Liste) und das Vorrats-Blatt
docs/konzepte/quizaway-stufe2-vorrat-2026-10-02.md: je Ort alle Karten des Vorrats mit Vorderseite, Rückseite,
Urteil des Faktenchecks und Mikes bisherigen Einträgen; kuratiert wird durch Streichen.

Aufruf:  python -X utf8 scripts/data-build/gemeinde_achsen_karten_fakt.py
         python -X utf8 scripts/data-build/gemeinde_achsen_vorrat.py [--kreuze]
--kreuze liest vor dem Neuaufbau die Kreuze "[x] streichen" aus dem Blatt und legt sie in kuratierung.json ab.
"""
import io
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
ZIEL = os.path.join(WURZEL, 'docs', 'konzepte', 'quizaway-stufe2-vorrat-2026-10-02.md')
LAEUFE = [('v0.6', 'Karte', 'dritter Lauf'), ('v0.5', 'Karte', 'zweiter Lauf'), ('v0.4', 'Vorschlag', 'erster Lauf'),
          ('a0.1', 'Karte', 'Ausreißer'), ('s0.1', 'Karte', 'Seltenheit')]  # a0.1 hinten: LAEUFE[0] bleibt der jüngste Kartenlauf (Übersicht, Kartensatz)
# ein weiterer Raum (GA_RAUM=neuwied) bringt Läufe (jüngster zuerst) und Blattnamen in <raum>/orte.json mit
RAUM = {}
if os.path.exists(os.path.join(ITER, 'orte.json')):
    with io.open(os.path.join(ITER, 'orte.json'), encoding='utf-8') as _f:
        RAUM = json.load(_f)
    ZIEL = os.path.join(WURZEL, 'docs', 'konzepte', RAUM['vorratsblatt'])
    LAEUFE = [(l[0], l[1], l[2]) for l in RAUM['laeufe']]
HEUTE = '2026-10-02'
GRUNDDATEN_NAME = {'einwohner': 'Einwohnerzahl', 'landkreis': 'Landkreis', 'kfz': 'Kennzeichen', 'ersterwaehnung': 'Jahr der ersten Erwähnung',
                   'eingemeindung': 'Jahr der Eingemeindung', 'partnerstaedte': 'Partnerstadt', 'hoehe_m': 'Höhe des Orts',
                   'flaeche_km2': 'Fläche der Gemarkung', 'dichte_ew_km2': 'Einwohner je Quadratkilometer',
                   'km_landeshauptstadt': 'Luftlinie zur Landeshauptstadt', 'wahl_btw25.zweite': 'Bundestagswahl 2025, zweitstärkste Partei',
                   'wahl_btw25.erste': 'Bundestagswahl 2025, Anteil der stärksten Partei',
                   'wahl_btw25.beteiligung': 'Bundestagswahl 2025, Wahlbeteiligung',
                   'ausreisser_kreis': 'Bundestagswahl 2025, Ausreißer gegen den Kreis',
                   'ausreisser_wahlkreis': 'Bundestagswahl 2025, Ausreißer des Wahlkreises',
                   'seltenheit_frauenanteil': 'Seltenheit: Frauenanteil', 'seltenheit_dichte': 'Seltenheit: Einwohner je km²',
                   'seltenheit_flaeche': 'Seltenheit: Fläche', 'seltenheit_einwohner': 'Seltenheit: Einwohnerzahl'}
DOC_VORRAT = ('Mikes Streichungen im Vorrats-Blatt, je Ort eine Liste [Lauf, Karte]. Gestrichen heißt: die Karte ist raus; '
              'eine ältere Karte zum selben Fakt kommt dadurch nicht zurück.')
FELDER = 'FAKTENCHECK|SORTE|FAMILIE|FAKT-ID|GEWÄHLTER FAKT|BEKANNTHEIT|VORDERSEITE|RÜCKSEITE|WÖRTER RÜCKSEITE|ANSCHLUSS|NEGATIVNACHWEISE|PRÜFHINWEIS|## '


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


def kreuze_lesen(kur):
    """Kreuze aus dem Blatt nach kuratierung.json übernehmen; gibt die Zahl der neuen Kreuze zurück."""
    lauf_von = dict((t, l) for l, _, t in LAEUFE)
    slug = sorted(lies_json('vorrat.json')['orte'])
    streichen = kur.setdefault('vorrat', {'_doc': DOC_VORRAT, 'stand': None, 'streichen': {}})['streichen']
    ort, neu = None, 0
    with io.open(ZIEL, encoding='utf-8') as f:
        for z in f:
            m = re.match(r'^## (\d\d) · ', z)
            if m:
                ort = next(s for s in slug if s.startswith(m.group(1)))
            m = re.match(r'^### (.+?), \w+ (\d+) · .*\[\s*[xX]\s*\] streichen', z)
            if m and [lauf_von[m.group(1)], int(m.group(2))] not in streichen.setdefault(ort, []):
                streichen[ort].append([lauf_von[m.group(1)], int(m.group(2))])
                neu += 1
    if neu:
        kur['vorrat']['stand'] = HEUTE
        with io.open(os.path.join(ITER, 'kuratierung.json'), 'w', encoding='utf-8', newline='\n') as f:
            json.dump(kur, f, ensure_ascii=False, indent=1)
    return neu


def ersetzt_je_ort(bindung, status, raus_alle):
    """Abfrage "derselbe Fakt": je Schlüssel bleibt die Karte des jüngsten Laufs, die übrigen sind ersetzt."""
    rang = dict((l, i) for i, (l, _, _) in enumerate(LAEUFE))
    je_schluessel = {}
    for b in bindung:
        k = (b['ort'], b['lauf'], b['karte'])
        if status.get(k, {}).get('status') in (None, 'gesperrt') or k in raus_alle:
            continue
        je_schluessel.setdefault(b['schluessel'], []).append(b)
    aus = {}
    for s, karten_ in je_schluessel.items():
        karten_.sort(key=lambda b: (rang[b['lauf']], b['karte']))
        bleibt = karten_[0]
        for b in karten_[1:]:
            if b['lauf'] == bleibt['lauf']:
                sys.exit('zwei Karten desselben Laufs auf einem Fakt: %s %s %d und %d (%s)' % (
                    b['ort'], b['lauf'], bleibt['karte'], b['karte'], s))
            if '/G.' in s:
                sache = GRUNDDATEN_NAME.get(s.split('/G.')[1], s.split('/G.')[1])
            else:
                sache = b['bezeichnung'] + (': ' + b['eigenschaft'].replace('_', ' ') if b['eigenschaft'] and '.' in s else '')
            aus.setdefault(b['ort'], []).append({'lauf': b['lauf'], 'karte': b['karte'], 'durch': [bleibt['lauf'], bleibt['karte']],
                                                 'fakt': '%s (`%s`)' % (sache, s)})
    return aus


def main():
    plan = lies_json('vorrat.json')
    status = {(s['ort'], s['lauf'], s['karte']): s for s in lies_json(os.path.join('faktencheck', 'status.json'))}
    kur = lies_json('kuratierung.json') if os.path.exists(os.path.join(ITER, 'kuratierung.json')) else {
        '_doc': 'Mikes Kuratierung als Daten (Raum %s).' % RAUM.get('raum', ''), 'blatt1': {'wahl': {}}, 'blatt2': {'orte': {}}}
    if '--kreuze' in sys.argv:
        print('Kreuze aus dem Blatt übernommen: %d' % kreuze_lesen(kur))
    gestrichen_alle = kur.get('vorrat', {}).get('streichen', {})
    raus_alle = set((ort, e['lauf'], e['karte']) for ort, p in plan['orte'].items() for e in p['raus'])
    ersetzt_alle = ersetzt_je_ort(lies_json('karten-fakt.json'), status, raus_alle)
    name = {o['slug']: o['name'] for o in lies_json('grunddaten.json')['orte']}
    reihe = kur.get('kartensatz', {}).get('reihe', {})
    liste, aus = [], []
    aus += ['# QuizAway — Stufe 2, Vorrat Raum Freiburg nach drei Läufen',
            '',
            '**Erzeugt am 2026-10-02** mit `scripts/data-build/gemeinde_achsen_vorrat.py` aus den geprüften Fassungen der drei '
            'Kartenläufe (`data/gemeinde-achsen/iter1/karten-geprueft/`). Regel (Mike, 2026-10-02): Tragen zwei Läufe denselben '
            'Fakt, bleibt die Karte aus dem dritten Lauf; gesperrte Karten sind nicht im Vorrat. Welche Karte welche ersetzt, '
            'ergibt die Abfrage über `data/gemeinde-achsen/iter1/karten-fakt.json` (jede Karte ist an ihren Fakt gebunden) '
            'und steht hier am Ende jedes Orts.',
            '',
            '**So geht es:** wie beim Blatt davor. Was im Vorrat bleiben soll, bleibt unangekreuzt; nur ankreuzen, was gestrichen '
            'werden soll. Neu sind die Karten mit dem Vermerk „dritter Lauf"; die übrigen kennst du aus den beiden ersten Blättern. '
            'Der Kartensatz für den Tisch bleibt, wie er ist.',
            '',
            '**Faktencheck:** bestätigt = nichts zu ändern · korrigiert = steht hier in der berichtigten Fassung · '
            'unsicher = Auflösung nur durch Wikipedia belegt.',
            '']
    if RAUM:
        aus = ['# QuizAway — Stufe 2, Vorrat Raum %s' % RAUM['raum'],
               '',
               '**Erzeugt am %s** mit `scripts/data-build/gemeinde_achsen_vorrat.py` (GA_RAUM=%s) aus den geprüften Fassungen '
               'der Kartenläufe (`data/gemeinde-achsen/%s/karten-geprueft/`). Gesperrte Karten sind nicht im Vorrat. Tragen zwei '
               'Läufe denselben Fakt, bleibt die Karte des jüngeren Laufs (Mike, 2026-10-02); die Abfrage läuft über '
               '`karten-fakt.json`.' % (HEUTE, os.path.basename(ITER), os.path.basename(ITER)),
               '',
               '**So geht es:** Was im Vorrat bleiben soll, bleibt unangekreuzt; nur ankreuzen, was gestrichen werden soll '
               '(`[x] streichen`).',
               '',
               '**Faktencheck:** bestätigt = nichts zu ändern · korrigiert = steht hier in der berichtigten Fassung · '
               'unsicher = Auflösung nur durch Wikipedia belegt.',
               '']
    uebersicht = []
    for ort in sorted(plan['orte']):
        p = plan['orte'][ort]
        p_ersetzt = sorted(ersetzt_alle.get(ort, []), key=lambda e: (e['durch'][1], e['lauf'], e['karte']))
        ersetzt = {(e['lauf'], e['karte']): e for e in p_ersetzt}
        raus = {(e['lauf'], e['karte']): e for e in p['raus']}
        mike = [tuple(x) for x in gestrichen_alle.get(ort, [])]
        drin, gesperrt, gestrichen = [], [], []
        for lauf, kopf, lauf_text in LAEUFE:
            for nr, v in sorted(karten(lauf, kopf, ort).items()):
                s = status.get((ort, lauf, nr))
                if not s:
                    continue
                if s['status'] == 'gesperrt':
                    gesperrt.append((lauf_text, nr, s['grund']))
                elif (lauf, nr) in ersetzt or (lauf, nr) in raus:
                    continue
                elif (lauf, nr) in mike:
                    frage = [z for z in feld(v, 'VORDERSEITE').split('\n') if z.strip() and not re.match(r'\s*\d[.):]?\s', z)]
                    gestrichen.append((lauf_text, nr, frage[-1].strip() if frage else ''))
                else:
                    drin.append((lauf, kopf, lauf_text, nr, v, s))
        fehlt = [m for m in mike if not any(g[0] == dict((l, t) for l, _, t in LAEUFE)[m[0]] and g[1] == m[1] for g in gestrichen)]
        if fehlt:
            sys.exit('Streichung trifft keine Karte des Vorrats: %s %s' % (ort, fehlt))
        assert len(drin) <= plan['grenze_je_ort'], (ort, len(drin))
        sorten = [feld(v, 'SORTE').split()[0] if feld(v, 'SORTE') else 'Geschichte' for _, _, _, _, v, _ in drin]
        uebersicht.append((name[ort], len(drin), sum(1 for s in sorten if s.lower().startswith('klass')),
                           sum(1 for d in drin if d[0] == LAEUFE[0][0]), len(ersetzt), len(raus), len(gesperrt)))
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
                    for e in p_ersetzt] + ['']
        if gestrichen:
            aus += ['**Von dir gestrichen:**', ''] + ['- %s %d: %s' % g for g in gestrichen] + ['']
        if raus:
            aus += ['**Aus dem Vorrat genommen:**', ''] + [
                '- %s %d: %s' % (dict((l, t) for l, _, t in LAEUFE)[e['lauf']], e['karte'], e['grund']) for e in p['raus']] + ['']
        if gesperrt:
            aus += ['**Gesperrt nach Faktencheck:**', ''] + ['- %s %d: %s' % g for g in gesperrt] + ['']
    kopf_tab = ['## Übersicht', '', '| Ort | im Vorrat | davon Klassiker | davon %s | ersetzt | herausgenommen | gesperrt |' % LAEUFE[0][2], '|---|---|---|---|---|---|---|']
    kopf_tab += ['| %s | %d | %d | %d | %d | %d | %d |' % u for u in uebersicht]
    kopf_tab += ['| **zusammen** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** |' % tuple(sum(u[i] for u in uebersicht) for i in range(1, 7)), '']
    einschub = aus.index('---')
    aus = aus[:einschub] + kopf_tab + aus[einschub:] + ['---', '', '*Ende Vorrat.*', '']
    with io.open(ZIEL, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(aus))
    with io.open(os.path.join(ITER, 'vorrat-liste.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(liste, f, ensure_ascii=False, indent=1)
    for u in uebersicht:
        print('%-14s Vorrat %2d · Klassiker %d · jüngster Lauf %2d · ersetzt %d · raus %d · gesperrt %d' % u)
    print('zusammen: %d Karten im Vorrat' % len(liste))
    print('geschrieben:', ZIEL)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
