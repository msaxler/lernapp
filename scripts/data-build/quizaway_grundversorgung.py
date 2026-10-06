"""QuizAway Grundversorgung: alle Gemeinden Deutschlands als Ziele mit Klassiker-Karten, ohne Modell (Mike 2026-10-07).

Damit pingt der GPS-Modus überall, auch abseits der Strecken mit Geschichten-Karten. Die Karten selbst rechnet der
Prototyp aus diesen Daten (apps/quizaway-reise/grund-de.js); hier werden nur die amtlichen Werte kompakt abgelegt.

Quellen:
  - Statistisches Bundesamt, Gemeindeverzeichnis (GV-ISys, Auszug 31.12.2024): Gemeindeschlüssel, Name, Stadtrecht,
    Fläche, Bevölkerung (Zensus 2022 fortgeschrieben), Mittelpunktkoordinaten, Kreise, Länder.
  - Bundeswahlleiterin, Bundestagswahl 2025, Wahlbezirksergebnisse (über gemeinde_achsen_grunddaten.wahl_laden):
    Zweitstimmen je Gemeinde; zählt die Gemeinde ihre Briefwahl nicht selbst aus (Verbandsgemeinden, Ämter), gilt das
    Ergebnis der Verbandsgemeinde, und die Karte sagt das (Regel Mike: nur Gesamtergebnis, Urne und Brief).
  - Kfz-Unterscheidungszeichen je Kreis: Wikidata P395 an Kreisen mit Kreisschlüssel P440 (mehrere Zeichen je Kreis
    möglich, keines als Haupt markiert); das Zeichen des Orts selbst über data/kfz_kennzeichen.csv (Kürzel → Ort).

Aufruf:  python -X utf8 scripts/data-build/quizaway_grundversorgung.py
"""
import collections
import importlib.util
import io
import json
import os
import sqlite3
import sys
import urllib.parse
import urllib.request

import openpyxl

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROH = os.path.join(WURZEL, 'data', 'raw')
GV_URL = ('https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/'
          'GVAuszugJ/31122024_Auszug_GV.xlsx?__blob=publicationFile')
GV = os.path.join(ROH, 'gv_auszug_31122024.xlsx')
KFZ_WD = os.path.join(ROH, 'kfz_kreise_wikidata.json')
ZIEL = os.path.join(WURZEL, 'apps', 'quizaway-reise', 'grund-de.js')
UA = {'User-Agent': 'LernApp-GemeindeAchsen/0.1 (https://github.com/msaxler/lernapp)'}
STADT_TK = {'61', '62', '63', '67'}            # kreisfreie Stadt, Stadtkreis, Stadt, große Kreisstadt
KREISFREI_TK = {'41', '42'}                    # kreisfreie Stadt, Stadtkreis
# Kreise ohne Kfz-Zeichen in Wikidata (2026-10-07), Hauptzeichen zuerst
KFZ_HAND = {'01057': ['PLÖ'], '10045': ['HOM', 'IGB'], '16063': ['WAK', 'SLZ', 'EA'], '16070': ['IK', 'ARN', 'IL']}
PARTEIEN = ['CDU', 'CSU', 'SPD', 'AfD', 'GRÜNE', 'Die Linke', 'FDP', 'BSW', 'FREIE WÄHLER', 'SSW']


def holen(url, pfad):
    if not os.path.exists(pfad):
        os.makedirs(os.path.dirname(pfad), exist_ok=True)
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=120) as r, \
                open(pfad, 'wb') as f:
            f.write(r.read())
    return pfad


def zahl(s):
    return float(str(s).replace(',', '.'))


def gv_lesen():
    ws = openpyxl.load_workbook(holen(GV_URL, GV), read_only=True)['Onlineprodukt_Gemeinden31122024']
    laender, kreise, gemeinden = {}, {}, []
    for r in ws.iter_rows(min_row=7, values_only=True):
        sa, tk = str(r[0] or ''), str(r[1] or '')
        if sa == '10':
            laender[r[2]] = r[7]
        elif sa == '40':
            kreise[r[2] + r[3] + r[4]] = {'name': r[7], 'tk': tk}
        elif sa == '60' and r[9]:
            gemeinden.append({'ags': r[2] + r[3] + r[4] + r[6], 'vb': r[5], 'name': r[7].split(',')[0].strip(),
                              'stadt': tk in STADT_TK, 'tk': tk, 'fl': r[8], 'ew': int(r[9]),
                              'lon': round(zahl(r[14]), 5), 'lat': round(zahl(r[15]), 5)})
    return laender, kreise, gemeinden


def kreisname(k):
    n, tk = k['name'], k['tk']
    n = n.split(',')[0].strip()
    if tk in KREISFREI_TK:
        return n
    if tk == '44' and not n.lower().endswith('kreis') and not n.startswith(('Landkreis', 'Region', 'Städteregion')):
        return 'Landkreis ' + n
    if tk == '43' and not n.lower().endswith('kreis') and not n.startswith('Kreis'):
        return 'Kreis ' + n
    return n


def kfz_lesen():
    if not os.path.exists(KFZ_WD):
        q = ('SELECT ?ks ?kfz WHERE { ?k wdt:P440 ?ks . ?k wdt:P395 ?kfz . '
             'OPTIONAL { ?k wdt:P576 ?aufg } FILTER(!BOUND(?aufg)) }')
        u = 'https://query.wikidata.org/sparql?' + urllib.parse.urlencode({'query': q, 'format': 'json'})
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=180))
        with io.open(KFZ_WD, 'w', encoding='utf-8') as f:
            json.dump([[b['ks']['value'], b['kfz']['value']] for b in d['results']['bindings']], f, ensure_ascii=False)
    je = collections.defaultdict(list)
    with io.open(KFZ_WD, encoding='utf-8') as f:
        for ks, k in json.load(f):
            if k not in je[ks]:
                je[ks].append(k)
    ort = collections.defaultdict(set)   # Ortsname → Kürzel (data/kfz_kennzeichen.csv)
    with io.open(os.path.join(WURZEL, 'data', 'kfz_kennzeichen.csv'), encoding='utf-8') as f:
        for z in f.read().splitlines()[1:]:
            if ',' in z:
                k, n = z.split(',', 1)
                ort[n.strip()].add(k.strip())
    return je, ort


def wahl_modul():
    pfad = os.path.join(WURZEL, 'scripts', 'data-fetch', 'gemeinde_achsen_grunddaten.py')
    spec = importlib.util.spec_from_file_location('grunddaten', pfad)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def wahl_kurz(s, kurzname):
    """[Beteiligung %, [Partei, %], …] der drei stärksten nach Zweitstimmen."""
    if not s or not s['gueltig']:
        return None
    p = sorted(((kurzname.get(k, k), v) for k, v in s['p'].items()), key=lambda kv: -kv[1])[:3]
    return [round(100.0 * s['waehlende'] / s['berechtigt'], 1) if s['berechtigt'] else None] + \
           [[k, round(100.0 * v / s['gueltig'], 1)] for k, v in p]


def main():
    laender, kreise, gemeinden = gv_lesen()
    kfz_je, kfz_ort = kfz_lesen()
    kfz_je.update(KFZ_HAND)
    # Hauptzeichen der Vorgänger-App (data/geo.sqlite, je Kreisschlüssel; Mike 2026-10-07) – nur, wo Wikidata es für
    # denselben Kreis führt: 52 von 346 Zuordnungen dort sind verrutscht (ABI beim Altmarkkreis, IN bei Altötting, RP bei
    # Mainz-Bingen)
    vorgaenger = collections.defaultdict(list)
    with sqlite3.connect(os.path.join(WURZEL, 'data', 'geo.sqlite')) as db:
        for k, ks in db.execute('select id, kreis_id from kfz_kennzeichen'):
            if k in kfz_je.get(ks, []):
                vorgaenger[ks].append(k)
    # Hauptzeichen nach vorn: Zeichen, dessen Ort (kfz_kennzeichen.csv) der Kreisname ist, sonst der größte Ort des Kreises
    # mit eigenem Zeichen (Ortenaukreis: OG für Offenburg vor LR, KEL, WOL, BH)
    ew_name = collections.defaultdict(dict)
    for g in gemeinden:
        ew_name[g['ags'][:5]][g['name']] = max(g['ew'], ew_name[g['ags'][:5]].get(g['name'], 0))
    for ks, kz in kfz_je.items():
        if len(kz) < 2 or ks not in kreise:
            continue
        kn = kreisname(kreise[ks]).replace('Landkreis ', '').replace('Kreis ', '')
        def wert(k):
            if k in vorgaenger.get(ks, []):
                return 10 ** 10
            orte = [n for n, z in kfz_ort.items() if k in z]
            if kn in orte or kreise[ks]['name'].split(',')[0] in orte or kn.split('-')[0] in orte:
                return 10 ** 9
            return max([ew_name[ks].get(n, 0) for n in orte] or [0])
        if ks not in KFZ_HAND:
            kfz_je[ks] = sorted(kz, key=lambda k: -wert(k))
    m = wahl_modul()
    wahl = m.wahl_laden()
    kurz = dict(m.KURZNAME, **{'Christlich-Soziale Union in Bayern e.V.': 'CSU', 'Südschleswigscher Wählerverband': 'SSW'})

    # Schwerpunkt je Kreis (für Nachbarkreise als Antwortoptionen)
    sp = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for g in gemeinden:
        s = sp[g['ags'][:5]]
        s[0] += g['lat'] * g['ew']; s[1] += g['lon'] * g['ew']; s[2] += g['ew']
    aus_kreise = {}
    for ks, k in kreise.items():
        s = sp.get(ks)
        if not s or not s[2]:
            continue
        aus_kreise[ks] = [kreisname(k), 1 if k['tk'] in KREISFREI_TK else 0, kfz_je.get(ks, []),
                          round(s[0] / s[2], 4), round(s[1] / s[2], 4)]

    orte_je_kz = collections.defaultdict(set)
    for n, z in kfz_ort.items():
        for k in z:
            orte_je_kz[k].add(n)
    aus_wahl, aus_g, ohne_wahl, ohne_kfz = {}, [], 0, set()
    for g in gemeinden:
        s = wahl.get(g['ags'])
        schluessel = g['ags']
        if s and s.get('briefwahl_bei') and wahl.get(s['briefwahl_bei']):
            schluessel = s['briefwahl_bei']
            s = wahl[schluessel]
        w = wahl_kurz(s, kurz)
        if w:
            if schluessel not in aus_wahl:
                aus_wahl[schluessel] = ([s['name']] if schluessel.startswith('VG') else [None]) + w
        else:
            schluessel = None
            ohne_wahl += 1
        kz = kfz_je.get(g['ags'][:5], [])
        # eigenes Zeichen nur, wenn die CSV das Kürzel genau diesem einen Ort gibt: sie ordnet oft irgendeinen Ort des
        # Zulassungsbezirks zu (Prüfung 2026-10-07: 8 von 25 falsch, Ahaus BOR statt AH, Herrenberg BB, Norden AUR)
        eigen = [k for k in kz if k in kfz_ort.get(g['name'], set()) and orte_je_kz[k] == {g['name']}]
        if not kz:
            ohne_kfz.add(g['ags'][:5])
        aus_g.append([g['ags'], g['name'], 1 if g['stadt'] else 0, g['lat'], g['lon'], g['ew'], g['fl'], schluessel,
                      eigen[0] if eigen else None])

    daten = {'stand': 'Gemeindeverzeichnis 31.12.2024; Bundestagswahl 2025; Kfz-Zeichen Wikidata',
             'laender': laender, 'kreise': aus_kreise, 'wahl': aus_wahl, 'g': aus_g}
    with io.open(ZIEL, 'w', encoding='utf-8', newline='\n') as f:
        f.write('// erzeugt von scripts/data-build/quizaway_grundversorgung.py – nicht von Hand ändern\n')
        f.write('window.QA_GRUND = ' + json.dumps(daten, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print('%d Gemeinden, %d Kreise, %d Wahlergebnisse (%d Gemeinden ohne), Kreise ohne Kfz: %s' % (
        len(aus_g), len(aus_kreise), len(aus_wahl), ohne_wahl, sorted(ohne_kfz)))
    print('geschrieben:', ZIEL, os.path.getsize(ZIEL), 'Bytes')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
