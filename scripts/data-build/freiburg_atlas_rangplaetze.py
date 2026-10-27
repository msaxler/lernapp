"""Vertiefung Freiburg (Mike 2026-10-27): Ranglisten aus dem Stadtbezirksatlas 2025 der Stadt Freiburg (CC BY 4.0,
Amt für Bürgerservice und Informationsmanagement) lesen und je Stadtteil die auffälligen Plätze ausgeben.

Die Seiten „Stadtbezirke im Vergleich“ (PDF-Seiten 7–20) zeigen je Kennzahl alle 42 Stadtbezirke absteigend: Zeilen
„Nummer Name Wert“. Gelesen wird über die Lage der Wörter (pdfplumber), nicht über den Fließtext, damit Name und Wert
sicher in derselben Zeile stehen. Schreibt
  data/gemeinde-achsen/freiburg-vertiefung/atlas/ranglisten.json   je Kennzahl Titel, Einheit, Plätze, Wert für Freiburg
  data/gemeinde-achsen/freiburg-vertiefung/atlas/<slug>.txt         je Stadtteil die Plätze 1–3 und 40–42 seiner Bezirke
Aufruf:  python -X utf8 scripts/data-build/freiburg_atlas_rangplaetze.py
"""
import io
import json
import os
import re
import sys

import pdfplumber

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUS = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'freiburg-vertiefung', 'atlas')
PDF = os.path.join(AUS, 'stadtbezirksatlas-2025.pdf')
QUELLE = ('https://www.freiburg.de/pb/site/Freiburg/get/params_E-369397302/2463694/Stadtbezirksatlas%202025.pdf | '
          'Gemeinde-Webseite (Stadt Freiburg, Stadtbezirksatlas 2025)')
# Stadtbezirk (Nummer im Atlas) → Stadtteil im Raum bahn; Mundenhof (570) zählt der Atlas zu Rieselfeld
BEZIRK = {'111': '444-altstadt-freiburg', '112': '444-altstadt-freiburg', '120': '446-neuburg-freiburg',
          '211': '447-herdern', '212': '447-herdern', '220': '448-zaehringen', '231': '449-bruehl-freiburg',
          '232': '449-bruehl-freiburg', '233': '449-bruehl-freiburg', '240': '397-hochdorf-freiburg', '310': '440-waldsee',
          '320': '388-littenweiler', '330': '387-ebnet', '340': '442-kappel', '410': '450-oberau', '421': '439-wiehre',
          '422': '439-wiehre', '423': '439-wiehre', '424': '439-wiehre', '430': '436-guenterstal', '512': '445-stuehlinger',
          '513': '445-stuehlinger', '521': '456-mooswald', '522': '456-mooswald', '531': '455-betzenhausen',
          '532': '455-betzenhausen', '540': '457-landwasser', '550': '458-lehen-freiburg', '560': '464-waltershofen',
          '570': '459-rieselfeld', '611': '451-haslach-freiburg', '612': '451-haslach-freiburg', '613': '451-haslach-freiburg',
          '614': '451-haslach-freiburg', '621': '452-sankt-georgen', '622': '452-sankt-georgen', '630': '461-opfingen',
          '640': '462-tiengen-freiburg', '650': '463-munzingen', '660': '454-weingarten-freiburg', '670': '459-rieselfeld',
          '680': '453-vauban'}
ZAHL = re.compile(r'^-?\d{1,3}(?:\.\d{3})*(?:,\d+)?$')
RAND = 3   # Plätze 1–3 und die letzten drei
# Nicht in die Quiz-Quelle: Kennzahlen, die einen Stadtteil abstempeln (Armut, Transferleistungen, Herkunft …), und
# Wahlanteile (Regel QuizAway: Wahl nur Gesamtergebnis aus den Grunddaten). Umfragewerte nur mit den Spitzenplätzen.
AUSGESCHLOSSEN = ('Ausländer', 'Deutsche mit Migrationshintergrund', 'Wohngeld', 'Mietbelastung', 'Wohnkosten Eigentum',
                  'Alleinerziehende', 'Frauenbeschäftigtenquote', 'Armutsgefährdung', 'Arbeitslose', 'Transferleistung',
                  'Wahlbeteiligung', 'GRÜNE', 'SPD', 'CDU', 'DIE LINKE', 'FDP', 'AfD')


def zeilen(seite):
    """Wörter einer Seite zu Zeilen (gleiche Höhe ±2 pt), je Zeile nach x sortiert."""
    aus = []
    for w in sorted(seite.extract_words(), key=lambda w: (round(w['top']), w['x0'])):
        if aus and abs(aus[-1][0] - w['top']) <= 2.5:
            aus[-1][1].append(w)
        else:
            aus.append([w['top'], [w]])
    return [(t, sorted(ws, key=lambda w: w['x0'])) for t, ws in aus]


def ranglisten(seite):
    """Je Spalte die Blöcke „Titel, Einheit, Zeilen Nummer Name Wert“."""
    eintraege = []   # (x der Nummer, top, nummer, name, wert)
    freiburg = []    # (x, top, wert)
    for top, ws in zeilen(seite):
        i = 0
        while i < len(ws):
            w = ws[i]
            if re.fullmatch(r'\d{3}', w['text']) and w['text'] in BEZIRK:
                j = i + 1
                name = []
                while j < len(ws) and not ZAHL.match(ws[j]['text']) and ws[j]['text'] != 'k.A.':
                    name.append(ws[j]['text']); j += 1
                # „k.A.“ (keine Angabe, zu wenige Befragte): kein Platz; sonst nähme die Zeile die Nummer der Nachbarspalte
                if j < len(ws) and ws[j]['text'] == 'k.A.':
                    i = j + 1
                    continue
                if j < len(ws) and ZAHL.match(ws[j]['text']) and name and ws[j]['x0'] - w['x0'] < 120:
                    eintraege.append((round(w['x0']), top, w['text'], ' '.join(name), ws[j]['text']))
                    i = j + 1
                    continue
            if w['text'] == 'Freiburg' and i + 2 < len(ws) and ws[i + 1]['text'] == 'insgesamt' and ZAHL.match(ws[i + 2]['text']):
                freiburg.append((round(w['x0']), top, ws[i + 2]['text']))
            i += 1
    bloecke = []
    for x in sorted(set(e[0] for e in eintraege)):
        spalte = sorted([e for e in eintraege if abs(e[0] - x) <= 3], key=lambda e: e[1])
        block = []
        for e in spalte:
            # Zeilenabstand 7 pt; die Zeile „Freiburg insgesamt“ dazwischen macht 14 pt, ein neuer Block beginnt weit darunter
            if block and e[1] - block[-1][1] > 25:
                bloecke.append((x, block)); block = []
            block.append(e)
        if block:
            bloecke.append((x, block))
    aus = []
    for x, block in bloecke:
        if len(block) < 30:
            continue
        oben = block[0][1]
        # Titel: Zeilen über dem Block in derselben Spalte, bis zu 40 pt darüber
        titel = []
        for top, ws in zeilen(seite):
            if oben - 40 < top < oben - 1:
                t = ' '.join(w['text'] for w in ws if x - 25 <= w['x0'] <= x + 130)
                if t and t not in ('STADTBEZIRKE IM VERGLEICH',):
                    titel.append(t)
        fr = [f for f in freiburg if abs(f[0] - (x + 11)) <= 15 and block[0][1] <= f[1] <= block[-1][1] + 8]
        aus.append({'titel': ' '.join(titel), 'freiburg': fr[0][2] if fr else None,
                    'plaetze': [{'platz': n + 1, 'bezirk': e[2], 'name': e[3], 'wert': e[4]} for n, e in enumerate(block)]})
    return aus


def main():
    alle = []
    with pdfplumber.open(PDF) as pdf:
        for nr in range(6, 21):
            for r in ranglisten(pdf.pages[nr]):
                r['seite'] = nr + 1
                alle.append(r)
    with io.open(os.path.join(AUS, 'ranglisten.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(alle, f, ensure_ascii=False, indent=1)
    print(len(alle), 'Ranglisten;', sum(1 for r in alle if len(r['plaetze']) == 42), 'mit allen 42 Bezirken')
    for r in alle:
        if len(r['plaetze']) != 42 or not r['freiburg']:
            print('  prüfen: S.%d %s – %d Plätze, Freiburg %s' % (r['seite'], r['titel'][:70], len(r['plaetze']), r['freiburg']))
    je_ort = {}
    for r in alle:
        if r['titel'].startswith(AUSGESCHLOSSEN):
            continue
        n = len(r['plaetze'])
        umfrage = 'Kommunalbarometer' in r['titel'] or 'Freiburg-Umfrage' in r['titel']
        for p in r['plaetze']:
            if p['platz'] <= RAND or (p['platz'] > n - RAND and not umfrage):
                je_ort.setdefault(BEZIRK[p['bezirk']], []).append((r, p, n))
    for slug, liste in sorted(je_ort.items()):
        z = ['=== QUELLE: %s ===' % QUELLE,
             'Stadtbezirksatlas 2025 der Stadt Freiburg: Rangplätze der Stadtbezirke im Vergleich der Freiburger Stadtbezirke '
             '(Platz 1 = höchster Wert; Rieselfeld und Mundenhof zählt der Atlas zusammen, Bezirke ohne Angabe fehlen). '
             'Werte mit „Kommunalbarometerwerte 0-100“ sind Zufriedenheitswerte aus der Freiburg-Umfrage 2024, keine Messwerte. '
             'Aufgeführt sind nur Plätze unter den ersten oder letzten drei.']
        for r, p, n in liste:
            z.append('- %s: Stadtbezirk %s %s auf Platz %d von %d mit %s (Freiburg insgesamt: %s)%s'
                     % (r['titel'], p['bezirk'], p['name'], p['platz'], n, p['wert'], r['freiburg'] or 'nicht angegeben',
                        ' – höchster Wert der Stadt' if p['platz'] == 1 else ' – niedrigster Wert der Stadt' if p['platz'] == n else ''))
        with io.open(os.path.join(AUS, slug + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(z) + '\n')
        print('%-24s %2d Rangplätze' % (slug, len(liste)))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
