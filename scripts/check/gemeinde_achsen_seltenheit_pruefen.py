"""Gemeinde-Achsen: Faktencheck der Seltenheits-Karten (Lauf s0.1) als unabhängige Rechenprüfung.

Liest die Kartentexte aus <raum>/karten-s0.1/, zieht Zahl, Vergleichsmenge, Richtung, Werte und Optionen heraus und rechnet
sie ohne den Code des Generators aus dem Gemeindeverzeichnis (Destatis) bzw. der Wahlbezirksstatistik nach: Zählung,
Median, Platz eins im Kreis mit Abstand, jede falsche Option, Lösungsstelle, Wortgrenzen. Der Zusatzsatz auf der Rückseite
ist von Hand im Netz geprüft (Beleg in <raum>/seltenheit-zusatz.json) und wird hier nur auf Wortgleichheit verglichen.
Schreibt <raum>/faktencheck-s0.1/<slug>.md im Format des Faktenchecks.

Aufruf:  python -X utf8 scripts/check/gemeinde_achsen_seltenheit_pruefen.py      (GA_RAUM=<raum>)
"""
import glob
import io
import json
import os
import re
import sys

import openpyxl

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
OPTION = {'Den Frauenanteil': 'fr', 'Die Fläche der Gemarkung': 'fl', 'Die Einwohnerzahl': 'ew', 'Die Einwohner je Quadratkilometer': 'di'}


def verzeichnis():
    tabelle = openpyxl.load_workbook(os.path.join(WURZEL, 'data', 'raw', 'gv_auszug.xlsx'), read_only=True, data_only=True)
    gemeinden = {}
    for zeile in tabelle['Onlineprodukt_Gemeinden31122025'].iter_rows(values_only=True):
        if zeile[0] != '60' or not isinstance(zeile[9], (int, float)) or zeile[9] <= 0 or not zeile[8]:
            continue
        schluessel = '%s%s%s%s' % (zeile[2], zeile[3], zeile[4], zeile[6])
        gemeinden[schluessel] = {'ew': zeile[9], 'fl': zeile[8], 'di': zeile[9] / zeile[8], 'fr': zeile[11] * 100.0 / zeile[9], 'w': zeile[11]}
    return gemeinden


def zahl(text):
    return float(text.replace('.', '').replace(',', '.'))


def main():
    gemeinden = verzeichnis()
    with io.open(os.path.join(ITER, 'grunddaten.json'), encoding='utf-8') as f:
        orte = {o['slug']: o for o in json.load(f)['orte']}
    zusatz = {}
    if os.path.exists(os.path.join(ITER, 'seltenheit-zusatz.json')):
        with io.open(os.path.join(ITER, 'seltenheit-zusatz.json'), encoding='utf-8') as f:
            zusatz = json.load(f)['orte']
    os.makedirs(os.path.join(ITER, 'faktencheck-s0.1'), exist_ok=True)
    for pfad in sorted(glob.glob(os.path.join(ITER, 'karten-s0.1', '[0-9]*.md'))):
        slug = os.path.basename(pfad)[:-3]
        text = io.open(pfad, encoding='utf-8').read().split('## ORTS-ANSCHLUSS')[0]
        ags = orte[slug]['gemeindeschluessel'][:8]
        befund = []
        vorn = text.split('VORDERSEITE:')[1].split('RÜCKSEITE:')[0].strip().split('\n')
        rueck = text.split('RÜCKSEITE:')[1].split('\nQuelle:')[0].strip()
        frage = vorn[2]
        optionen = [re.sub(r'^\d\.\s+', '', z) for z in vorn[3:]]
        if 'Bundestagswahl' in frage:
            befund.append('Wahl-Seltenheit: Prüfung noch nicht gebaut')
        m = re.search(r'nur (\d+) der ([\d.]+) Gemeinden Deutschlands (übertreffen|unterbieten)', frage)
        if not m:
            befund.append('Frage nicht lesbar')
        else:
            n, gesamt, hoch = int(m.group(1)), int(m.group(2).replace('.', '')), m.group(3) == 'übertreffen'
            if gesamt != len(gemeinden):
                befund.append('Vergleichsmenge %d statt %d' % (gesamt, len(gemeinden)))
            richtig = int(re.search(r'Richtig war (\d)\.', rueck).group(1))
            merkmal = OPTION[optionen[richtig - 1]]
            eigen = gemeinden[ags][merkmal]
            zaehl = lambda mk: sum(1 for g in gemeinden.values() if (g[mk] > gemeinden[ags][mk] if hoch else g[mk] < gemeinden[ags][mk]))
            if zaehl(merkmal) != n:
                befund.append('Zählung %d statt %d' % (zaehl(merkmal), n))
            if n > 0.01 * len(gemeinden):
                befund.append('mehr als ein Prozent')
            for o in optionen:
                if OPTION[o] != merkmal and zaehl(OPTION[o]) <= n:
                    befund.append('falsche Option %s ist nicht falsch' % o)
            werte = sorted(g[merkmal] for g in gemeinden.values())
            median = werte[len(werte) // 2]
            kreis = sorted((g[merkmal] for s, g in gemeinden.items() if s[:5] == ags[:5] and s != ags), reverse=hoch)
            zweiter = kreis[0]
            if (hoch and zweiter >= eigen) or (not hoch and zweiter <= eigen) or abs(eigen - zweiter) < 1.0:
                befund.append('nicht mit Abstand Platz eins im Kreis')
            if merkmal == 'fr':
                mm = re.search(r'Von ([\d.]+) Einwohnern sind ([\d.]+) Frauen, ([\d,]+) Prozent', rueck)
                if not mm or zahl(mm.group(1)) != gemeinden[ags]['ew'] or zahl(mm.group(2)) != gemeinden[ags]['w'] \
                        or zahl(mm.group(3)) != round(eigen, 1):
                    befund.append('Werte auf der Rückseite stimmen nicht')
            mm = re.search(r'Median liegt bei ([\d,]+)\. .* kommt keine andere Gemeinde (?:über|unter) ([\d,]+)\.', rueck)
            if not mm or zahl(mm.group(1)) != round(median, 1) or zahl(mm.group(2)) != round(zweiter, 1):
                befund.append('Median oder Kreiszweiter stimmen nicht (gerechnet %.1f / %.1f)' % (median, zweiter))
            if slug in zusatz and zusatz[slug]['satz'] not in rueck:
                befund.append('Zusatzsatz weicht vom geprüften Satz ab')
        if len(frage.split()) > 25 or len(rueck.split()) > 60 or any(len(o.split()) > 8 for o in optionen):
            befund.append('Wortgrenze')
        ok = not befund
        zweite = ('Rechenprüfung aus dem Gemeindeverzeichnis des Statistischen Bundesamts (unabhängig nachgerechnet)' +
                  ('; Zusatzsatz: ' + zusatz[slug]['beleg'] if slug in zusatz else ''))
        aus = ['## s0.1 Karte 1', 'URTEIL: %s' % ('OK' if ok else 'KORRIGIEREN'),
               'KERNAUSSAGE: %s' % (frage.split('. Welchen')[0] + '.'), 'ARTIKEL: steht so da (Rechenprüfung)',
               'ZWEITE QUELLE: %s' % zweite, 'FALSCHE OPTIONEN: %s' % ('alle sicher falsch (nachgerechnet)' if ok else 'siehe Befund'),
               'BEFUND: %s' % ('keiner' if ok else '; '.join(befund)), '', '## ZUSAMMENFASSUNG', 'Rechenprüfung, 1 Karte.', '']
        with io.open(os.path.join(ITER, 'faktencheck-s0.1', slug + '.md'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(aus))
        print('%-18s %s' % (slug, 'OK' if ok else '; '.join(befund)))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
