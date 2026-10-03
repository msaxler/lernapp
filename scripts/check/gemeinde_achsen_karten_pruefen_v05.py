"""Gemeinde-Achsen Iteration 1, zweiter Volllauf: Karten des Prompts v0.5 mechanisch prüfen.

Liest data/gemeinde-achsen/iter1/karten-v0.5/*.md und den PLAN aus eingabe-v0.5/<slug>.txt. Prüft je Karte:
Wörter der Rückseite (<= 60), der Frage (<= 25), je Option (<= 8), Zahl der Optionen, Stelle der Lösung gegen
den PLAN, Sorte, Familie, Bekanntheit, Wege der Negativnachweise. Je Ort: Zahl der Karten, Orts-Anschlüsse
(<= 10 Wörter). Schreibt karten-v0.5-pruefung.json und druckt eine Tabelle.

Aufruf:  python -X utf8 scripts/check/gemeinde_achsen_karten_pruefen_v05.py
"""
import glob
import io
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
GEPRUEFT = '--geprueft' in sys.argv  # Fassung nach dem Faktencheck (karten-geprueft/<lauf>)
# --lauf v0.6 prüft die Karten des Prompts v0.6 (gleiches Format, dazu das Feld PRÜFHINWEIS)
LAUF = sys.argv[sys.argv.index('--lauf') + 1] if '--lauf' in sys.argv else 'v0.5'
KARTEN = os.path.join(ITER, 'karten-geprueft', LAUF) if GEPRUEFT else os.path.join(ITER, 'karten-' + LAUF)
FELDER = 'FAKTENCHECK|SORTE|FAMILIE|FAKT-ID|GEWÄHLTER FAKT|BEKANNTHEIT|VORDERSEITE|RÜCKSEITE|WÖRTER RÜCKSEITE|NEGATIVNACHWEISE|PRÜFHINWEIS|PRÜFSTUFE|ERFUNDEN|## '


def feld(text, name):
    m = re.search(r'^%s:?[ \t]*(.*?)(?=^(?:%s))' % (name, FELDER), text + '\n## ENDE', flags=re.S | re.M)
    return m.group(1).strip() if m else ''


_INDEX = {}


def fakten_index():
    if not _INDEX:
        with io.open(os.path.join(ITER, 'fakten', 'index.json'), encoding='utf-8') as f:
            _INDEX.update(json.load(f))
    return _INDEX


def plan_lesen(slug):
    """Je Karte: (Sorte laut Plan, erlaubte Stellen)."""
    with io.open(os.path.join(ITER, 'eingabe-' + LAUF, slug + '.txt'), encoding='utf-8') as f:
        text = f.read()
    plan = {}
    for nr, rest in re.findall(r'^\s*Karte (\d+): (.*)$', text, flags=re.M):
        plan[int(nr)] = (rest.split(',')[0].split()[0], [int(x) for x in re.findall(r'(?:Stelle|"höher":) (\d)', rest)])
    return plan


def familie_kurz(text):
    t = text.upper()
    if 'LEITER' in t:
        return 'C-LEITER'
    m = re.match(r'\s*([ABC])\b', t)
    return m.group(1) if m else '?'


def pruefe(karte, nr, plan):
    vorn = feld(karte, 'VORDERSEITE')
    rueck = re.split(r'^\s*Quelle:', feld(karte, 'RÜCKSEITE'), flags=re.M)[0].strip()
    # Die Läufe schreiben Optionen als "1. …", "1) …" oder "1 …"
    optionen = re.findall(r'^\s*(\d)[.):]?\s+(.+)$', vorn, flags=re.M)
    zeilen = [z.strip() for z in vorn.split('\n') if z.strip() and not re.match(r'^\s*\d[.):]?\s', z)
              and not z.strip().startswith('STELLE:')]
    frage = ' '.join(zeilen[2:]) if len(zeilen) > 2 else (zeilen[-1] if zeilen else '')
    fam = familie_kurz(feld(karte, 'FAMILIE'))
    m = re.search(r'(?:Richtig war|Die Lüge war|Höher bis Stufe)\s*(\d)', rueck)
    stelle = int(m.group(1)) if m else None
    soll_optionen = {'A': 4, 'C': 4, 'B': 3}.get(fam)
    p = {
        'karte': nr,
        'faktencheck': (feld(karte, 'FAKTENCHECK').split() or ['ungeprüft'])[0],
        'faktencheck_grund': feld(karte, 'FAKTENCHECK').partition(' – ')[2],
        'sorte': (feld(karte, 'SORTE').split() or ['?'])[0],
        'sorte_plan': plan.get(nr, ('?', []))[0],
        'familie': fam,
        'fakt': ' '.join(feld(karte, 'GEWÄHLTER FAKT').split())[:160],
        'bekanntheit': (feld(karte, 'BEKANNTHEIT').split() or ['?'])[0].strip('–-:.,').lower(),
        'woerter_rueckseite': len(rueck.split()),
        'woerter_frage': len(frage.split()),
        'optionen': len(optionen),
        'max_woerter_option': max([len(o.split()) for _, o in optionen] or [0]),
        'loesung_stelle': stelle,
        'stelle_plan': plan.get(nr, ('?', []))[1],
        'wege': ''.join(sorted(set(re.findall(r'\(([abc])\)', feld(karte, 'NEGATIVNACHWEISE'))))),
        'frage': frage,
    }
    fehler = []
    if p['woerter_rueckseite'] > 60:
        fehler.append('Rückseite %d Wörter' % p['woerter_rueckseite'])
    if p['woerter_frage'] > 25:
        fehler.append('Frage %d Wörter' % p['woerter_frage'])
    if p['max_woerter_option'] > 8:
        fehler.append('Option %d Wörter' % p['max_woerter_option'])
    if soll_optionen and p['optionen'] != soll_optionen:
        fehler.append('%d Optionen statt %d' % (p['optionen'], soll_optionen))
    if fam == 'C-LEITER' and p['optionen'] < 4:
        fehler.append('Leiter mit %d Stufen' % p['optionen'])
    if stelle is None:
        fehler.append('Schlusssatz fehlt')
    elif p['stelle_plan'] and stelle not in p['stelle_plan']:
        fehler.append('Stelle %d, Plan %s' % (stelle, p['stelle_plan']))
    if not p['wege']:
        fehler.append('kein Weg genannt')
    if LAUF not in ('v0.5', 'v0.6'):
        # ab Prompt v0.7 nennt jede Karte die Kennung ihres Fakts (fakten/index.json) oder GRUNDDATEN.<eigenschaft>
        kennung = (feld(karte, 'FAKT-ID').split() or [''])[0]
        p['fakt_id'] = kennung
        if not kennung:
            fehler.append('FAKT-ID fehlt')
        elif not kennung.startswith('GRUNDDATEN.') and kennung.partition('.')[0] not in fakten_index():
            fehler.append('FAKT-ID unbekannt: ' + kennung)
        elif (p['sorte'].lower().startswith('klass')) != kennung.startswith('GRUNDDATEN.'):
            fehler.append('FAKT-ID passt nicht zur Sorte: ' + kennung)
    p['fehler'] = fehler
    return p


def main():
    alle, orte = [], []
    print('%-16s %1s %-10s %-8s %4s %5s %3s %3s %-6s %-4s  %s' % ('Ort', 'K', 'Sorte', 'Familie', 'Rück', 'Frage', 'Opt', 'St.', 'Bek.', 'Wege', 'Fehler'))
    for pfad in sorted(glob.glob(os.path.join(KARTEN, '*.md'))):
        slug = os.path.splitext(os.path.basename(pfad))[0]
        with io.open(pfad, encoding='utf-8') as f:
            text = f.read()
        plan = plan_lesen(slug)
        teile = re.split(r'^##\s*Karte\s*(\d+)\s*$', text, flags=re.M)
        karten = []
        for i in range(1, len(teile), 2):
            rest = re.split(r'^##\s*(?:ORTS-ANSCHLUSS|NICHT VERWENDET|UNGEREGELT)', teile[i + 1], flags=re.M)[0]
            p = pruefe(rest, int(teile[i]), plan)
            p['ort'] = slug
            karten.append(p)
            print('%-16s %1d %-10s %-8s %4d %5d %3d %3s %-6s %-4s  %s' % (
                slug, p['karte'], p['sorte'], p['familie'], p['woerter_rueckseite'], p['woerter_frage'], p['max_woerter_option'],
                p['loesung_stelle'], p['bekanntheit'], p['wege'], '; '.join(p['fehler'])))
        m = re.search(r'^##\s*ORTS-ANSCHLUSS\s*\n(.*?)(?=^##\s|\Z)', text, flags=re.S | re.M)
        block = m.group(1) if m else ''
        anschluesse = [z.strip().lstrip('-•0123456789. ').strip() for z in block.split('\n')
                       if z.strip() and not z.strip().upper().startswith('ANSCHLUSS-KANDIDAT') and z.strip().lower() != 'keiner']
        kandidaten = [k for k in re.findall(r'ANSCHLUSS-KANDIDAT:?\s*(.+)', block) if not k.lower().startswith('keiner')]
        orte.append({'ort': slug, 'karten': len(karten), 'geschichten': sum(1 for k in karten if k['sorte'].lower().startswith('gesch')),
                     'klassiker': sum(1 for k in karten if k['sorte'].lower().startswith('klass')),
                     'anschluesse': anschluesse, 'anschluss_woerter': [len(a.split()) for a in anschluesse],
                     'anschluss_kandidaten': kandidaten, 'keine_karte': text.count('KEINE KARTE')})
        alle += karten
    with io.open(os.path.join(ITER, 'karten-%s-%spruefung.json' % (LAUF, 'geprueft-' if GEPRUEFT else '')), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'karten': alle, 'orte': orte}, f, ensure_ascii=False, indent=1)
    print()
    for o in orte:
        print('%-16s %d Karten (%d Geschichte, %d Klassiker) · Anschlüsse %s Wörter · Kandidaten %d' % (
            o['ort'], o['karten'], o['geschichten'], o['klassiker'], o['anschluss_woerter'], len(o['anschluss_kandidaten'])))
    zaehle = lambda fn: sum(1 for a in alle if fn(a))
    print('\nKarten: %d · mit Fehler: %d · Rückseite über 60: %d · Stelle abweichend: %d' % (
        len(alle), zaehle(lambda a: a['fehler']), zaehle(lambda a: a['woerter_rueckseite'] > 60),
        zaehle(lambda a: any(f.startswith('Stelle') for f in a['fehler']))))
    print('Bekanntheit: ' + ', '.join('%s %d' % (b, zaehle(lambda a, b=b: a['bekanntheit'] == b)) for b in ('niedrig', 'mittel', 'hoch')))
    print('Familien: ' + ', '.join('%s %d' % (b, zaehle(lambda a, b=b: a['familie'] == b)) for b in ('A', 'B', 'C', 'C-LEITER')))
    print('Wege: ' + ', '.join('(%s) %d' % (w, zaehle(lambda a, w=w: w in a['wege'])) for w in 'abc'))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
