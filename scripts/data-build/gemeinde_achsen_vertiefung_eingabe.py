"""Gemeinde-Achsen, Raum bahn: Eingaben für die Vertiefung (Prompt prompt-karten-v0.9-tief.txt; Freiburg, Mike 2026-10-27).

Ein Ort mit Ortsporträt-Karten (karten-geprueft/v0.9) bekommt zusätzliche Karten aus neuen Quellen. Je Ort eine Datei
eingabe-v0.9-tief/<slug>.txt:
  Kopf wie in eingabe-v0.9 (ZIELORT, LAGE, ARTIKEL, GRUNDDATEN, ZEUGEN),
  BISHERIGE KARTEN (Charakteristikum, Frage, FAKT-ID; gesperrte mit Vermerk),
  PLAN für N neue Karten (Facetten im Wechsel, RANG ab der Zahl der bisherigen Karten + 1),
  FAHRT, NEUE FAKTEN (fakten/<slug>-tief.txt), BISHERIGE FAKTEN (fakten/<slug>.txt).
Aufruf:  GA_RAUM=bahn python -X utf8 scripts/data-build/gemeinde_achsen_vertiefung_eingabe.py [--karten N] [slug=N ...] slugs
         ohne Zahl: 6 neue Karten, Altstadt 15
"""
import io
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAUM = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'bahn'))
# weitere Runde (GA_TIEF=tief2): eigene Fakten und Eingaben; die Karten früherer Runden zählen als bisherige
TIEF = os.environ.get('GA_TIEF', 'tief')
AUS = os.path.join(RAUM, 'eingabe-v0.9-' + TIEF)
# Mike 2026-10-27: „Altstadt mit deutlich mehr Karten“
ZAHL = {'444-altstadt-freiburg': 15}
STANDARD = 6
REIHE = ['FREIZEIT', 'GESCHICHTE', 'ALLTAG', 'LAGE', 'GESCHICHTE', 'INFRA']
ERSATZ = {'FREIZEIT': 'ALLTAG', 'ALLTAG': 'FREIZEIT', 'LAGE': 'GESCHICHTE', 'INFRA': 'LAGE', 'GESCHICHTE': 'FREIZEIT'}


def lies(p):
    with io.open(p, encoding='utf-8') as f:
        return f.read()


def feld(text, name):
    m = re.search(r'^%s:[ \t]*(.*?)(?=^[A-ZÄÖÜ][A-ZÄÖÜ0-9 -]*:|\Z)' % name, text, flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def bisherige(slug):
    """Zeilen „- Charakteristikum | Frage | FAKT-ID“ aus der geprüften v0.9-Fassung und früheren Vertiefungsrunden."""
    laeufe = ['v0.9'] + sorted(d for d in os.listdir(os.path.join(RAUM, 'karten-geprueft'))
                               if d.startswith('v0.9-tief') and d != 'v0.9-' + TIEF)
    karten = []
    for lauf in laeufe:
        pfad = os.path.join(RAUM, 'karten-geprueft', lauf, slug + '.md')
        if os.path.exists(pfad):
            text = re.split(r'^## (?:STECKBRIEF|ORTS-ANSCHLUSS)', lies(pfad), flags=re.M)[0]
            karten += re.split(r'^## Karte \d+\s*$', text, flags=re.M)[1:]
    zeilen = []
    for k in karten:
        vorn = [z.strip() for z in feld(k, 'VORDERSEITE').split('\n') if z.strip()]
        frage = ' '.join(z for z in vorn[2:] if not re.match(r'^\d[.):]?\s', z))
        status = feld(k, 'FAKTENCHECK').split(' – ')[0].strip()
        zeilen.append('- %s | %s | %s%s' % (feld(k, 'CHARAKTERISTIKUM') or '?', frage, feld(k, 'FAKT-ID'),
                                             ' (gesperrt, Inhalt war nicht haltbar)' if status == 'gesperrt' else ''))
    return zeilen


def plan(i, n, rang_ab):
    a = lambda k: ((i * 3 + k * 5) % 4) + 1
    b = lambda k: ((i + k) % 3) + 1
    z = []
    for k in range(1, n + 1):
        fac = REIHE[(i + k - 1) % len(REIHE)]
        if k % 4 == 0:
            z.append('  Karte %d: FACETTE %s (Ersatz: %s), Geschichte, B, Lüge an Stelle %d' % (k, fac, ERSATZ[fac], b(k)))
        elif fac in ('FREIZEIT', 'ALLTAG', 'INFRA') and k % 2 == 1:
            z.append('  Karte %d: FACETTE %s (Ersatz: %s), Geschichte, D, wahre Option an Stelle %d' % (k, fac, ERSATZ[fac], a(k)))
        else:
            z.append('  Karte %d: FACETTE %s (Ersatz: %s), Geschichte, A, wahre Option an Stelle %d' % (k, fac, ERSATZ[fac], a(k)))
    z.append('  RANG der neuen Karten ab %d' % rang_ab)
    return '\n'.join(z)


def main():
    zahl, args = dict(ZAHL), []
    for a in sys.argv[1:]:
        # „slug=N“ setzt die Zahl der neuen Karten; der Ort gehört trotzdem zur Liste (bis 2026-10-27 14:05 fiel er heraus)
        s, _, n = a.partition('=')
        if n:
            zahl[s] = int(n)
        args.append(s)
    os.makedirs(AUS, exist_ok=True)
    for i, slug in enumerate(args):
        alt = lies(os.path.join(RAUM, 'eingabe-v0.9', slug + '.txt'))
        kopf = alt.split('\nPLAN:', 1)[0].rstrip()
        fahrt = re.search(r'^FAHRT:.*$', alt, flags=re.M).group(0)
        bis = bisherige(slug)
        n = zahl.get(slug, STANDARD)
        neu = os.path.join(RAUM, 'fakten', slug + '-' + TIEF + '.txt')
        if not os.path.exists(neu):
            sys.exit('keine neuen Fakten für %s (Extraktion mit GA_VERTIEFUNG=1 und gemeinde_achsen_fakten.py zuerst)' % slug)
        frueher = [os.path.join(RAUM, 'fakten', slug + '.txt')] + sorted(
            os.path.join(RAUM, 'fakten', f) for f in os.listdir(os.path.join(RAUM, 'fakten'))
            if f.startswith(slug + '-tief') and f != slug + '-' + TIEF + '.txt')
        teile = [kopf, '', 'BISHERIGE KARTEN (%d):' % len(bis)] + bis + ['', 'PLAN:', plan(i, n, len(bis) + 1), '', fahrt, '',
                 'NEUE FAKTEN (Zielort, aus den neuen Quellen):', lies(neu).strip(), '',
                 'BISHERIGE FAKTEN (Zielort):'] + [lies(p).strip() for p in frueher] + ['']
        text = '\n'.join(teile)
        with io.open(os.path.join(AUS, slug + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text + '\n')
        print('%-24s %7d Zeichen, %d bisherige Karten, %d neue geplant' % (slug, len(text), len(bis), n))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
