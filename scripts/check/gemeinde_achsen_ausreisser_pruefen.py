"""Gemeinde-Achsen: Faktencheck der Ausreißer-Karten (Lauf a0.1) als unabhängige Rechenprüfung.

Die Karten schreibt data-build/gemeinde_achsen_ausreisser.py aus der Wahlbezirksstatistik. Dieses Skript teilt keinen
Code mit ihm: Es liest die Kartentexte, zieht jede Zahl und jede Partei heraus, rechnet sie aus der amtlichen
Wahlbezirksstatistik (bzw. dem Stadtteilergebnis der Grunddaten) neu und prüft Schwellen, Rangfolgen, Optionen und
Wortgrenzen. Schreibt <raum>/faktencheck-a0.1/<slug>.md im Format des Faktenchecks ("## a0.1 Karte N", URTEIL …),
das check/gemeinde_achsen_faktencheck_auswerten.py liest.

Gegen die amtlichen Endergebnisse abgeglichen (2026-10-03, bundeswahlleiterin.de): Land Baden-Württemberg, Land
Rheinland-Pfalz, Wahlkreis 281 Freiburg, Wahlkreis 196 Neuwied – die Summen aus der Wahlbezirksstatistik stimmen.

Aufruf:  python -X utf8 scripts/check/gemeinde_achsen_ausreisser_pruefen.py      (GA_RAUM=<raum>)
"""
import csv
import glob
import io
import json
import os
import re
import sys
import zipfile

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
PARTEI = {'die cdu': 'CDU', 'der cdu': 'CDU', 'die afd': 'AfD', 'der afd': 'AfD', 'die spd': 'SPD', 'der spd': 'SPD',
          'die grünen': 'GRÜNE', 'den grünen': 'GRÜNE', 'die linke': 'Die Linke', 'der linken': 'Die Linke',
          'die fdp': 'FDP', 'der fdp': 'FDP', 'das bsw': 'BSW', 'dem bsw': 'BSW'}
ABGLEICH = ('Rechenprüfung aus der amtlichen Wahlbezirksstatistik der Bundeswahlleiterin (unabhängig nachgerechnet); '
            'Methode abgeglichen mit den Endergebnissen auf bundeswahlleiterin.de (Länder BW und RLP, Wahlkreise 281 und 196)')


def statistik():
    """Je Gebiet die Zweitstimmen je Partei; Gebiete: ('L',land) ('K',kreis) ('G',ags) ('W',wk); dazu Erststimmen je Wahlkreis."""
    with zipfile.ZipFile(os.path.join(WURZEL, 'data', 'raw', 'btw25_wbz.zip')) as z:
        reader = csv.reader(io.StringIO(z.read('btw25_wbz_ergebnisse.csv').decode('utf-8-sig')), delimiter=';')
        zeilen = list(reader)
    kopf = zeilen[4]
    sp = {name: nr for nr, name in enumerate(kopf)}
    zweit = {name[:-15]: nr for name, nr in sp.items() if name.endswith(' - Zweitstimmen') and name[:-15] not in ('Ungültige', 'Gültige')}
    erst = {name[:-14]: nr for name, nr in sp.items() if name.endswith(' - Erststimmen') and name[:-14] not in ('Ungültige', 'Gültige')}
    gebiete, erststimmen, briefwahl_fremd, land_des_wk, wk_der_gemeinde = {}, {}, set(), {}, {}
    for zeile in zeilen[5:]:
        if len(zeile) != len(kopf) or not zeile[sp['Land']].isdigit():
            continue
        land = zeile[sp['Land']]
        ags = land + zeile[sp['Regierungsbezirk']] + zeile[sp['Kreis']] + zeile[sp['Gemeinde']]
        wk = zeile[sp['Wahlkreis']]
        land_des_wk[wk] = land
        wk_der_gemeinde[ags] = wk
        if zeile[sp['Kennziffer Briefwahlzugehörigkeit']].strip() not in ('', '00'):
            briefwahl_fremd.add(ags)
        for gebiet in (('L', land), ('K', ags[:5]), ('G', ags), ('W', wk)):
            ziel = gebiete.setdefault(gebiet, {})
            for partei, nr in zweit.items():
                ziel[partei] = ziel.get(partei, 0) + (int(zeile[nr]) if zeile[nr].strip().isdigit() else 0)
        ziel = erststimmen.setdefault(wk, {})
        for partei, nr in erst.items():
            ziel[partei] = ziel.get(partei, 0) + (int(zeile[nr]) if zeile[nr].strip().isdigit() else 0)
    return gebiete, erststimmen, briefwahl_fremd, land_des_wk, wk_der_gemeinde


def prozent(stimmen):
    gesamt = sum(stimmen.values())
    return {p: round(100.0 * v / gesamt, 1) for p, v in stimmen.items()}, {p: 100.0 * v / gesamt for p, v in stimmen.items()}


def vorn(stimmen):
    return sorted(stimmen.items(), key=lambda kv: -kv[1])[0][0]


def zahl(s):
    return float(s.replace(',', '.'))


def feld(text, name):
    m = re.search(r'^%s:[ \t]*(.*?)(?=^[A-ZÄÖÜ][A-ZÄÖÜ -]+:|^## |\Z)' % name, text, flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def pruefe(slug, ort, karte, st):
    gebiete, erststimmen, fremd, land_des_wk, wk_der_gemeinde = st
    befunde, kern = [], ''
    vorne = [z for z in feld(karte, 'VORDERSEITE').split('\n') if z.strip()]
    optionen = [PARTEI[re.sub(r'^\d\.\s+', '', z).strip().lower()] for z in vorne if re.match(r'^\d\.\s', z)]
    frage = ' '.join(z for z in vorne[2:] if not re.match(r'^\d\.\s', z))
    rueck = feld(karte, 'RÜCKSEITE').split('\nQuelle:')[0].strip()
    if len(frage.split()) > 25:
        befunde.append('Frage %d Wörter' % len(frage.split()))
    if any(len(o.split()) > 8 for o in vorne if re.match(r'^\d\.\s', o)):
        befunde.append('Option über 8 Wörter')
    if len(rueck.split()) > 60:
        befunde.append('Rückseite %d Wörter' % len(rueck.split()))
    richtig = int(re.search(r'Richtig war (\d)\.', rueck).group(1))
    ags = ort['gemeindeschluessel'][:8]
    land = ags[:2]
    if 'ausreisser_wahlkreis' in feld(karte, 'FAKT-ID'):
        wk = wk_der_gemeinde[ags]
        rund, genau = prozent(gebiete[('W', wk)])
        p, zweite = sorted(genau, key=lambda q: -genau[q])[:2]
        m = re.search(r'Hier (?:lag|lagen) (.+?) vorn, mit ([\d,]+) Prozent vor (.+?) mit ([\d,]+)\.', rueck)
        if not m or PARTEI[m.group(1).lower()] != p or zahl(m.group(2)) != rund[p] or PARTEI[m.group(3).lower()] != zweite or zahl(m.group(4)) != rund[zweite]:
            befunde.append('Wahlkreis-Ergebnis stimmt nicht: Karte „%s“, gerechnet %s %s vor %s %s' % (m.group(0) if m else '?', p, rund[p], zweite, rund[zweite]))
        wks_land = [w for w, l in land_des_wk.items() if l == land]
        gleich = [w for w in wks_land if vorn(gebiete[('W', w)]) == p]
        sieger = vorn(gebiete[('L', land)])
        if p == sieger or len(gleich) > 3:
            befunde.append('kein Ausreißer nach (a): %s vorn in %d Wahlkreisen des Landes, Landessieger %s' % (p, len(gleich), sieger))
        m = re.search(r'Im Land lag in (\d+) von (\d+) Wahlkreisen (.+?) vorn\.', rueck)
        if not m or int(m.group(1)) != sum(1 for w in wks_land if vorn(gebiete[('W', w)]) == sieger) or int(m.group(2)) != len(wks_land) \
                or PARTEI[m.group(3).lower()] != sieger:
            befunde.append('Satz über das Land stimmt nicht')
        m = re.search(r'bundesweit in (\d+) von (\d+) Wahlkreisen', rueck)
        if not m or int(m.group(1)) != sum(1 for w in land_des_wk if vorn(gebiete[('W', w)]) == p) or int(m.group(2)) != len(land_des_wk):
            befunde.append('bundesweite Zahl stimmt nicht')
        weitere = {1: 'nur in einem weiteren Wahlkreis', 0: 'in keinem Wahlkreis'}.get(len(gleich) - 1, 'nur in %d weiteren' % (len(gleich) - 1))
        if weitere not in frage:
            befunde.append('Zahl der weiteren Wahlkreise in der Frage stimmt nicht (gerechnet %d)' % (len(gleich) - 1))
        m = re.search(r'Bei den Erststimmen (?:lag|lagen) dort (.+?) vorn\.', rueck)
        if not m or PARTEI[m.group(1).lower()] != vorn(erststimmen[wk]):
            befunde.append('Erststimmen-Sieger stimmt nicht (gerechnet %s)' % vorn(erststimmen[wk]))
        for q in optionen:
            if q != p and any(vorn(gebiete[('W', w)]) == q for w in wks_land):
                befunde.append('falsche Option %s lag in einem Wahlkreis des Landes vorn' % q)
        if optionen[richtig - 1] != p:
            befunde.append('„Richtig war %d“ trifft nicht %s' % (richtig, p))
        kern = 'Im Wahlkreis %s lagen bei den Zweitstimmen 2025 %s vorn (%s %%), als einer von %d Wahlkreisen im Land.' % (wk, p, rund[p], len(gleich))
    else:
        if ort['einheit'].startswith('Ortsteil'):
            wahl = ort['eigenschaften']['wahl_btw25'][0]
            if 'nur ungefähr' in wahl.get('hinweis', ''):
                befunde.append('Stadtteilergebnis nur ungefähr')
            ort_rund = {q: v for q, v in wahl['wert']['anteile_prozent'].items()}
            ort_genau = dict(ort_rund)
        else:
            if ags in fremd:
                befunde.append('kein Gesamtergebnis (Briefwahl bei der Verbandsgemeinde)')
            ort_rund, ort_genau = prozent(gebiete[('G', ags)])
        kreis_rund, kreis_genau = prozent(gebiete[('K', ags[:5])])
        abw = sorted(((ort_genau[q] - kreis_genau[q], q) for q in ('CDU', 'AfD', 'SPD', 'GRÜNE', 'Die Linke') if q in ort_genau), key=lambda t: -abs(t[0]))
        (d, p), (d2, q2) = abw[0], abw[1]
        m = re.search(r'gab (.+?) ([\d,]+) Prozent der Zweitstimmen, (?:im|in der) .+? waren es ([\d,]+): ([\d,]+) Punkte (mehr|weniger)\. '
                      r'Die nächstgrößte Abweichung hatte (.+?) mit ([\d,]+) Punkten\.', rueck)
        if not m:
            befunde.append('Rückseite nicht lesbar')
        else:
            if PARTEI[m.group(1).lower()] != p or zahl(m.group(2)) != round(ort_genau[p], 1) or zahl(m.group(3)) != kreis_rund[p] \
                    or zahl(m.group(4)) != round(abs(d), 1) or (m.group(5) == 'mehr') != (d > 0):
                befunde.append('Zahlen stimmen nicht: Karte %s %s/%s/%s, gerechnet %s %.1f/%.1f/%.1f' % (
                    m.group(1), m.group(2), m.group(3), m.group(4), p, ort_genau[p], kreis_rund[p], abs(d)))
            if PARTEI[m.group(6).lower()] != q2 or zahl(m.group(7)) != round(abs(d2), 1):
                befunde.append('nächstgrößte Abweichung stimmt nicht (gerechnet %s %.1f)' % (q2, abs(d2)))
        if abs(d) < 8.0 or abs(d) - abs(d2) < 1.5:
            befunde.append('Schwelle nicht erreicht: %.2f Punkte, Abstand %.2f' % (abs(d), abs(d) - abs(d2)))
        for q in optionen:
            if q != p and q in ort_genau and abs(ort_genau[q] - kreis_genau[q]) >= abs(d):
                befunde.append('falsche Option %s weicht nicht weniger ab' % q)
        if optionen[richtig - 1] != p:
            befunde.append('„Richtig war %d“ trifft nicht %s' % (richtig, p))
        kern = '%s wich bei der Bundestagswahl 2025 bei %s am stärksten vom Kreis ab (%.1f gegen %.1f %%).' % (ort['name'], p, ort_genau[p], kreis_genau[p])
    return kern, befunde


def main():
    st = statistik()
    with io.open(os.path.join(ITER, 'grunddaten.json'), encoding='utf-8') as f:
        orte = {o['slug']: o for o in json.load(f)['orte']}
    aus_ordner = os.path.join(ITER, 'faktencheck-a0.1')
    os.makedirs(aus_ordner, exist_ok=True)
    zahl_ok = zahl_k = 0
    for pfad in sorted(glob.glob(os.path.join(ITER, 'karten-a0.1', '[0-9]*.md'))):
        slug = os.path.basename(pfad)[:-3]
        text = io.open(pfad, encoding='utf-8').read()
        teile = re.split(r'^## Karte (\d+)\s*$', text.split('## ORTS-ANSCHLUSS')[0], flags=re.M)
        aus = []
        for i in range(1, len(teile), 2):
            kern, befunde = pruefe(slug, orte[slug], teile[i + 1], st)
            ok = not befunde
            zahl_ok += ok
            zahl_k += not ok
            aus += ['## a0.1 Karte %s' % teile[i], 'URTEIL: %s' % ('OK' if ok else 'KORRIGIEREN'), 'KERNAUSSAGE: %s' % kern,
                    'ARTIKEL: steht so da (Rechenprüfung)', 'ZWEITE QUELLE: %s' % ABGLEICH,
                    'FALSCHE OPTIONEN: %s' % ('alle sicher falsch (nachgerechnet)' if ok else 'siehe Befund'),
                    'BEFUND: %s' % ('keiner' if ok else '; '.join(befunde)), '']
            print('%-18s Karte %s: %s' % (slug, teile[i], 'OK' if ok else '; '.join(befunde)))
        aus += ['## ZUSAMMENFASSUNG', 'Rechenprüfung, %d Karten.' % ((len(teile) - 1) // 2), '']
        with io.open(os.path.join(aus_ordner, slug + '.md'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(aus))
    print('OK %d · KORRIGIEREN %d' % (zahl_ok, zahl_k))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
