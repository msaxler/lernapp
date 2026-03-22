#!/usr/bin/env python3
"""
fetch_staedte.py  —  Baut staedte.json mit ALLEN deutschen Städten (Stadtrecht)
================================================================================
Quellen:
  1. deutsche-staedte.xlsx  (Destatis) — Name, Fläche, Einwohner, Bundesland
  2. DE.txt                 (GeoNames) — Koordinaten, Höhe
  3. kfz_kennzeichen.csv               — KFZ-Kennzeichen
  4. staedte.json (bestehend)          — Flüsse, manuelle Korrekturen

Beide Dateien in denselben Ordner legen wie dieses Skript.

Aufruf:
  python fetch_staedte.py
  python fetch_staedte.py --dry-run
"""
import openpyxl, json, csv, re, os, sys, shutil, argparse

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
XLSX_FILE    = os.path.join(SCRIPT_DIR, 'deutsche-staedte.xlsx')
DE_TXT       = os.path.join(SCRIPT_DIR, 'DE.txt')
KFZ_CSV      = os.path.join(SCRIPT_DIR, 'kfz_kennzeichen.csv')
OUT_FILE     = os.path.join(SCRIPT_DIR, 'staedte.json')
BACKUP_FILE  = os.path.join(SCRIPT_DIR, 'staedte_backup.json')

BL_MAP = {
    '01':'Schleswig-Holstein','02':'Hamburg','03':'Niedersachsen',
    '04':'Bremen','05':'Nordrhein-Westfalen','06':'Hessen',
    '07':'Rheinland-Pfalz','08':'Baden-Württemberg','09':'Bayern',
    '10':'Saarland','11':'Berlin','12':'Brandenburg',
    '13':'Mecklenburg-Vorpommern','14':'Sachsen','15':'Sachsen-Anhalt',
    '16':'Thüringen',
}
GN_KORREKTUREN = {
    'Munich':'München','Nuremberg':'Nürnberg','Cologne':'Köln',
    'Hanover':'Hannover','Aix-la-Chapelle':'Aachen',
}

# Abweichende Namen: Destatis → GeoNames
MANUAL_GN = {
    'Freiburg im Breisgau':'Freiburg',
    'Mülheim an der Ruhr':'Mülheim',
    'Offenbach am Main':'Offenbach',
    'Esslingen am Neckar':'Esslingen',
    'Dessau-Roßlau':'Dessau',
    'Marburg':'Marburg an der Lahn',
    'Bad Homburg v. d. Höhe':'Bad Homburg vor der Höhe',
    'Greifswald':'Universitäts- und Hansestadt Greifswald',
    'Rottenburg am Neckar':'Rottenburg',
    'Weiden i.d.OPf.':'Weiden',
    'Neumarkt i.d.OPf.':'Neumarkt in der Oberpfalz',
    'St. Ingbert':'Sankt Ingbert',
    'Emmerich am Rhein':'Emmerich',
    'Radolfzell am Bodensee':'Radolfzell',
    'Geestland':'Lehe',
    'Neuburg a.d.Donau':'Neuburg an der Donau',
    'Schwandorf':'Schwandorf in Bayern',
    'Hattersheim am Main':'Hattersheim',
    'Wangen im Allgäu':'Wangen',
    'Pfaffenhofen a.d.Ilm':'Pfaffenhofen an der Ilm',
    'Lauf a.d.Pegnitz':'Lauf an der Pegnitz',
    'St. Wendel':'Sankt Wendel',
    'Leutkirch im Allgäu':'Leutkirch',
    'Hann. Münden':'Hannoversch Münden',
    'Weilheim i.OB':'Weilheim',
    'Eisleben':'Eisleben Lutherstadt',
    'Mühldorf a.Inn':'Mühldorf',
    'Flörsheim am Main':'Flörsheim',
    'Moosburg a.d.Isar':'Moosburg',
    'Bad Friedrichshall':'Bad Friedrichshall',
    'Dillingen a.d.Donau':'Dillingen an der Donau',
    'Haldensleben':'Haldensleben',
    'Weißenburg i.Bay.':'Weißenburg in Bayern',
    'Vilshofen an der Donau':'Vilshofen',
    'Alzenau':'Alzenau in Unterfranken',
    'Garching b.München':'Garching bei München',
    'Eltville am Rhein':'Eltville',
    'Altdorf b.Nürnberg':'Altdorf bei Nürnberg',
    'Bad Neustadt a.d.Saale':'Bad Neustadt an der Saale',
    'Isny im Allgäu':'Isny',
    'Lohr a.Main':'Lohr am Main',
    'Oberndorf am Neckar':'Oberndorf',
    'Neustadt b.Coburg':'Neustadt bei Coburg',
    'Landau a.d.Isar':'Landau an der Isar',
    'Neustadt a.d.Donau':'Neustadt an der Donau',
    'Immenstadt i.Allgäu':'Immenstadt',
    'Grafing b.München':'Grafing bei München',
    'Höchstadt a.d.Aisch':'Höchstadt an der Aisch',
    'Neustadt a.d.Aisch':'Neustadt an der Aisch',
    'Röthenbach a.d.Pegnitz':'Röthenbach an der Pegnitz',
    'Wasserburg a.Inn':'Wasserburg am Inn',
    'St. Georgen im Schwarzwald':'Sankt Georgen im Schwarzwald',
    'Lindenberg i.Allgäu':'Lindenberg im Allgäu',
    'Simbach a.Inn':'Simbach am Inn',
    'Gemünden a.Main':'Gemünden am Main',
    'Töging a.Inn':'Töging am Inn',
    'Bad Griesbach i.Rottal':'Bad Griesbach im Rottal',
    'Vohburg a.d.Donau':'Vohburg an der Donau',
    'Auerbach i.d.OPf.':'Auerbach in der Oberpfalz',
    'Obernburg a.Main':'Obernburg am Main',
    'Furtwangen im Schwarzwald':'Furtwangen',
    'Gundelfingen a.d.Donau':'Gundelfingen',
    'Höchstädt a.d.Donau':'Höchstädt an der Donau',
    'Bonndorf im Schwarzwald':'Bonndorf',
    'Schwarzenbach a.d.Saale':'Schwarzenbach an der Saale',
    'Dietfurt a.d.Altmühl':'Dietfurt',
    'Klingenberg a.Main':'Klingenberg am Main',
    'Neustadt a.d.Waldnaab':'Neustadt an der Waldnaab',
    'Bad Königshofen i.Grabfeld':'Bad Königshofen im Grabfeld',
    'Zeil a.Main':'Zeil am Main',
    'Wörth a.d.Donau':'Wörth an der Donau',
    'Oettingen i.Bay.':'Oettingen in Bayern',
    'Hofheim i.UFr.':'Hofheim in Unterfranken',
    'Wörth a.Main':'Wörth am Main',
    'Bischofsheim i.d.Rhön':'Bischofsheim in der Rhön',
    'Triberg im Schwarzwald':'Triberg',
    'Bad Berneck i.Fichtelgebirge':'Bad Berneck im Fichtelgebirge',
    'Eschenbach i.d.OPf.':'Eschenbach in der Oberpfalz',
    'St. Blasien':'Sankt Blasien',
    'Königsberg i.Bay.':'Königsberg in Bayern',
    'Lübbenau/Spreewald / Lubnjow/Błota':'Lübbenau',
    'Lübben (Spreewald) / Lubin (Błota)':'Lübben',
    'Calau/Kalawa':'Calau',
    'Aue-Bad Schlema':'Aue',
    'Lauter-Bernsbach':'Lauter',
    'Grünhain-Beierfeld':'Beierfeld',
    'Pockau-Lengefeld':'Lengefeld',
    'Roßleben-Wiehe':'Roßleben',
    'Ebersbach-Neugersdorf':'Ebersbach',
    'Wanzleben-Börde':'Wanzleben',
    'Oebisfelde-Weferlingen':'Oebisfelde',
    'Sandersdorf-Brehna':'Brehna',
    'Wettin-Löbejün':'Wettin',
    'Raguhn-Jeßnitz':'Raguhn',
    'Oranienbaum-Wörlitz':'Oranienbaum',
    'Belgern-Schildau':'Belgern',
    'Am Ettersberg':'Berlstedt',
    'Werra-Suhl-Tal':'Barchfeld',
    'An der Schmücke':'Heldrungen',
    'Schirgiswalde-Kirschau':'Schirgiswalde',
    'Berga-Wünschendorf':'Berga',
    'Nottertal-Heilinger Höhen':'Heringen',
    'Brotterode-Trusetal':'Brotterode',
    'Bad Gottleuba-Berggießhübel':'Bad Gottleuba',
    'Dornburg-Camburg':'Dornburg',
    'Uebigau-Wahrenbrück':'Wahrenbrück',
    'Pausa-Mühltroff':'Pausa',
    'Schwarzenbach a.Wald':'Schwarzenbach am Wald',
    'Auma-Weidatal':'Auma',
    'Eisleben':'Eisleben Lutherstadt',
    'Schwarzatal':'Schwarzburg',
    'Saalburg-Ebersdorf':'Saalburg',
    'Havelsee':'Pritzerbe',
    'Laucha an der Unstrut':'Laucha',
    'Oestrich-Winkel':'Oestrich-Winkel',
    'Trostberg':'Trostberg',
    'Kronberg im Taunus':'Kronberg im Taunus',
    'Müllheim im Markgräflerland':'Müllheim',
    'Reichenbach im Vogtland':'Reichenbach',
    'Korntal-Münchingen':'Korntal-Münchingen',
    'Südliches Anhalt':'Südliches Anhalt',
    'Wachenheim an der Weinstraße':'Wachenheim',
    'Ostheim v.d.Rhön':'Ostheim vor der Rhön',
    'Schloß Holte-Stukenbrock':'Schloß Holte-Stukenbrock',
    'Schwentinental':'Raisdorf',
    'Pohlheim':'Pohlheim',
    'Niddatal':'Niddatal',
    'Erlenbach a.Main':'Erlenbach am Main',
    'Vogtsburg im Kaiserstuhl':'Vogtsburg im Kaiserstuhl',
    'Endingen am Kaiserstuhl':'Endingen',
    'Dissen am Teutoburger Wald':'Dissen',
    'Marienmünster':'Marienmünster',
    'Heppenheim (Bergstraße)':'Heppenheim',
    'Weinstadt':'Weinstadt',
    'Stutensee':'Stutensee',
    'Neubukow':'Neubukow',
    'Rerik':'Rerik',
    'Lauterstein':'Lauterstein',
    'Oberwiesenthal':'Kurort Oberwiesenthal',
    'Hohenberg a.d.Eger':'Hohenberg an der Eger',
}

# Direkte Koordinaten für Städte die in GeoNames gar nicht vorhanden
COORDS_FALLBACK = {
    'Hanau':                     (50.13303, 8.91526,  100),
    'Ibbenbüren':                (52.27712, 7.72428,  80),
    'Weinstadt':                 (48.81441, 9.37736,  240),
    'Stutensee':                 (49.06910, 8.46010,  110),
    'Eisleben':                  (51.52781, 11.55285, 115),
    'Bad Friedrichshall':        (49.23333, 9.21667,  155),
    'Haldensleben':              (52.28547, 11.40803, 65),
    'Garching bei München':      (48.24876, 11.65220, 480),
    'Immenstadt':                (47.56085, 10.21600, 730),
    'Lindenberg im Allgäu':      (47.60067, 9.88451,  720),
    'Bad Griesbach im Rottal':   (48.45030, 13.19810, 360),
    'Auerbach in der Oberpfalz': (49.69229, 11.63540, 490),
    'Kühlungsborn':              (54.14776, 11.74310, 5),
    'Zeil am Main':              (50.00254, 10.59025, 230),
    'Schloß Holte-Stukenbrock':  (51.88444, 8.63583,  125),
    'Lübbenau':                  (51.86453, 13.96370, 55),
    'Lübben':                    (51.94261, 13.89834, 55),
    'Calau':                     (51.75541, 13.94453, 75),
    'Aue':                       (50.58920, 12.70460, 345),
    'Lauter':                    (50.56490, 12.73770, 415),
    'Beierfeld':                 (50.60630, 12.87030, 340),
    'Lengefeld':                 (50.72550, 13.17520, 490),
    'Roßleben':                  (51.29920, 11.40070, 130),
    'Ebersbach':                 (51.00920, 14.59420, 240),
    'Wanzleben':                 (52.03890, 11.43960, 80),
    'Oebisfelde':                (52.42680, 10.97900, 65),
    'Brehna':                    (51.55890, 12.14650, 90),
    'Wettin':                    (51.61530, 11.80860, 95),
    'Raguhn':                    (51.71100, 12.32260, 75),
    'Oranienbaum':               (51.79650, 12.39700, 75),
    'Belgern':                   (51.47040, 13.13260, 80),
    'Berlstedt':                 (51.08420, 11.30250, 280),
    'Barchfeld':                 (50.81060, 10.28680, 320),
    'Heldrungen':                (51.30270, 11.22220, 150),
    'Schirgiswalde':             (51.05110, 14.41450, 310),
    'Berga':                     (50.65680, 11.98800, 320),
    'Heringen':                  (50.86820, 10.20470, 260),
    'Brotterode':                (50.76550, 10.34100, 540),
    'Bad Gottleuba':             (50.87560, 13.97540, 320),
    'Dornburg':                  (50.95620, 11.63860, 210),
    'Wahrenbrück':               (51.67600, 13.27380, 85),
    'Pausa':                     (50.57850, 11.98510, 415),
    'Schwarzenbach am Wald':     (50.27720, 11.57260, 660),
    'Neubukow':                  (54.03550, 11.68730, 25),
    'Auma':                      (50.70030, 11.93340, 370),
    'Schwarzburg':               (50.61100, 11.17550, 420),
    'Saalburg':                  (50.53390, 11.70640, 510),
    'Pritzerbe':                 (52.51580, 12.50040, 32),
    'Laucha':                    (51.21300, 11.72330, 125),
    'Lauterstein':               (48.69760, 9.76660,  550),
    'Rerik':                     (54.10230, 11.61400, 5),
    'Kurort Oberwiesenthal':     (50.41840, 12.95900, 900),
    'Hohenberg an der Eger':     (50.09870, 12.21500, 450),
    'Raisdorf':                  (54.32760, 10.19570, 25),
    'Pohlheim':                  (50.53050, 8.75960,  190),
    'Niddatal':                  (50.27810, 8.87830,  175),
    'Erlenbach am Main':         (49.79810, 9.16310,  140),
    'Vogtsburg im Kaiserstuhl':  (48.06810, 7.67180,  210),
    'Endingen':                  (48.13720, 7.70110,  195),
    'Dissen':                    (52.10960, 8.19620,  85),
    'Oestrich-Winkel':           (49.99780, 8.01730,  90),
    'Trostberg':                 (48.02850, 12.55880, 490),
    'Kronberg im Taunus':        (50.17830, 8.51560,  230),
    'Müllheim':                  (47.81270, 7.62930,  285),
    'Marienmünster':             (51.78760, 9.19280,  170),
    'Wachenheim':                (49.44280, 8.17750,  130),
    'Ostheim vor der Rhön':      (50.45870, 10.22840, 375),
    'Reichenbach':               (50.62010, 12.29470, 310),
    'Korntal-Münchingen':        (48.84690, 9.11760,  290),
    'Landau an der Isar':        (48.68210, 12.69560, 345),
    'Neustadt an der Donau':     (48.80630, 11.76310, 360),
    'Südliches Anhalt':          (51.77780, 11.93890, 105),
    'Heppenheim':                (49.64360, 8.63680,  105),
    'Weinstadt':                 (48.81441, 9.37736,  240),
    'Stutensee':                 (49.06910, 8.46010,  110),
    'Schloß Holte-Stukenbrock':  (51.88444, 8.63583,  125),
    'Eisleben':                  (51.52781, 11.55285, 115),
    'Oberharz am Brocken':       (51.72310, 10.88060, 400),
    'Zahna-Elster':              (51.91220, 12.77830,  80),
    'Rottenburg a.d.Laaber':     (48.70080, 12.03240, 370),
    'Amt Creuzburg':             (51.04710, 10.24660, 230),
}

def normiere(name):
    n = name.lower()
    n = re.sub(r'\s*\(.*?\)', '', n)
    n = re.sub(r'\s*/.*$', '', n)
    n = re.sub(r'\s+v\.\s+d\.\s+.*$', '', n)
    n = re.sub(r'\s+a\.\s+.*$', '', n)
    n = n.replace('ß','ss').strip()
    return n

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    for f, label in [(XLSX_FILE,'deutsche-staedte.xlsx'),(DE_TXT,'DE.txt')]:
        if not os.path.exists(f):
            print(f'❌  {label} nicht gefunden in {SCRIPT_DIR}'); sys.exit(1)

    # 1. Destatis XLSX
    print('📂  Lese deutsche-staedte.xlsx ...')
    wb = openpyxl.load_workbook(XLSX_FILE)
    ws = wb.active
    destatis = {}
    for row in ws.iter_rows(min_row=3, max_row=2061, values_only=True):
        nr, ars, name_roh, plz, flaeche, ew = row[:6]
        if not ars or not name_roh: continue
        try: int(str(nr))
        except: continue
        ars_str = str(ars).zfill(12)
        name = str(name_roh).split(',')[0].strip()
        destatis[name] = {
            'bundesland': BL_MAP.get(ars_str[:2],'?'),
            'flaeche':    round(float(flaeche),2) if flaeche else 0.0,
            'einwohner':  int(ew) if ew else 0,
            'ars':        ars_str,
        }
    print(f'   {len(destatis)} Städte')

    # 2. GeoNames DE.txt
    print('📂  Lese DE.txt ...')
    geonames = {}
    with open(DE_TXT, encoding='utf-8') as f:
        for line in f:
            cols = line.rstrip('\n').split('\t')
            if len(cols) < 17: continue
            if cols[6] != 'P' or cols[7] == 'PPLX': continue
            name = GN_KORREKTUREN.get(cols[1], cols[1])
            pop = int(cols[14]) if cols[14] else 0
            hoehe = abs(int(cols[15])) if cols[15] else (abs(int(cols[16])) if cols[16] else 0)
            if name not in geonames or pop > geonames[name].get('pop',0):
                geonames[name] = {'lat':round(float(cols[4]),5),'lon':round(float(cols[5]),5),'hoehe':hoehe,'pop':pop}
    gn_index = {normiere(n):(n,g) for n,g in geonames.items()}
    print(f'   {len(geonames)} Orte')

    # 3. KFZ
    kfz_map = {}
    if os.path.exists(KFZ_CSV):
        with open(KFZ_CSV, encoding='utf-8') as f:
            for row in csv.DictReader(f): kfz_map[row['stadt'].strip()] = row['kfz'].strip()
    print(f'   {len(kfz_map)} KFZ-Einträge')

    # 4. Bestehende staedte.json
    alt = {}
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE, encoding='utf-8') as f:
            for s in json.load(f): alt[s['name']] = s

    # 5. Zusammenführen
    ergebnis = []
    ohne_coords = []
    for d_name, d in destatis.items():
        # Koordinaten suchen
        geo = None
        gn_name = MANUAL_GN.get(d_name, d_name)
        if gn_name in geonames:
            geo = geonames[gn_name]
        elif normiere(d_name) in gn_index:
            geo = gn_index[normiere(d_name)][1]
        elif gn_name in COORDS_FALLBACK:
            lat,lon,h = COORDS_FALLBACK[gn_name]
            geo = {'lat':lat,'lon':lon,'hoehe':h}
        else:
            ohne_coords.append(d_name)
            geo = {'lat':0.0,'lon':0.0,'hoehe':0}

        a = alt.get(d_name, alt.get(gn_name, {}))
        ergebnis.append({
            'name':       d_name,
            'lat':        geo['lat'],
            'lon':        geo['lon'],
            'bundesland': d['bundesland'],
            'einwohner':  d['einwohner'],
            'flaeche':    d['flaeche'],
            'hoehe':      a.get('hoehe') or geo.get('hoehe',0),
            'kfz':        a.get('kfz','') or kfz_map.get(d_name,'') or kfz_map.get(gn_name,''),
            'ars':        d['ars'],
            'fluesse':    a.get('fluesse',[]),
        })

    ergebnis.sort(key=lambda x: -x['einwohner'])

    # Bericht
    ohne_coords_n = sum(1 for s in ergebnis if s['lat']==0)
    mit_kfz = sum(1 for s in ergebnis if s['kfz'])
    print(f'\n✅  {len(ergebnis)} Städte')
    print(f'   Ohne Koordinaten: {ohne_coords_n}')
    print(f'   Mit KFZ:          {mit_kfz}/{len(ergebnis)}')
    if ohne_coords:
        print(f'   ⚠️  Fehlende Coords: {", ".join(ohne_coords[:10])}')

    bl = {}
    for s in ergebnis: bl[s['bundesland']] = bl.get(s['bundesland'],0)+1
    print('\n   Bundesland-Verteilung:')
    for b,n in sorted(bl.items(),key=lambda x:-x[1]):
        print(f'     {n:4d}×  {b}')

    print('\n   Top-10:')
    for s in ergebnis[:10]:
        print(f'     {s["einwohner"]:>10,}  {s["name"]:<35} {s["bundesland"]:<25} kfz:{s["kfz"]}')

    if args.dry_run:
        print('\n⚠️  --dry-run: nicht gespeichert.'); return

    if os.path.exists(OUT_FILE):
        shutil.copy2(OUT_FILE, BACKUP_FILE)
        print(f'\n💾  Backup: {BACKUP_FILE}')
    with open(OUT_FILE,'w',encoding='utf-8') as f:
        json.dump(ergebnis, f, ensure_ascii=False, indent=2)
    print(f'✅  {OUT_FILE} — {len(ergebnis)} Städte')
    print('\nNächste Schritte:\n  python generate_questions.py\n  python inject_questions.py')

if __name__ == '__main__': main()
