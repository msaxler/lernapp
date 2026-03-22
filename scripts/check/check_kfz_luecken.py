# -*- coding: utf-8 -*-
"""
check_kfz_luecken.py
"""
import sqlite3, csv, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DB   = os.path.join(BASE, 'data', 'geo.sqlite')
CSV_ = os.path.join(BASE, 'data', 'kfz_kennzeichen.csv')

conn = sqlite3.connect(DB)
c    = conn.cursor()

AUSNAHMEN = {
    'AA': 'Kreisstadt Aalen, Kreis=Ostalbkreis',
    'AW': 'Bad Neuenahr-Ahrweiler = Kreisstadt Ahrweiler',
    'BB': 'Herrenberg liegt im Kreis Boeblingen',
    'BIR': 'Idar-Oberstein liegt im Kreis Birkenfeld',
    'BM': 'Erftstadt liegt im Rhein-Erft-Kreis',
    'COE': 'Duelmen liegt im Kreis Coesfeld',
    'DLG': 'Dillingen a.d.Donau, nur Punkt-Schreibweise',
    'EA': 'Eisenach seit 2021 im Wartburgkreis',
    'EL': 'Papenburg liegt im Kreis Emsland',
    'ERB': 'Erbach = Kreisstadt Odenwaldkreis',
    'ES': 'Esslingen am Neckar, nur Namensergaenzung',
    'ESW': 'Eschwege = Kreisstadt Werra-Meissner-Kreis',
    'FN': 'Friedrichshafen = Kreisstadt Bodenseekreis',
    'FUS': 'Fuessen liegt im Landkreis Ostallgaeu',
    'GM': 'Wiehl liegt im Oberbergischen Kreis',
    'GR': 'Weisswasser liegt im Landkreis Goerlitz',
    'GT': 'Versmold liegt im Kreis Guetersloh',
    'HD': 'Sinsheim liegt im Rhein-Neckar-Kreis',
    'HDH': 'Giengen liegt im Kreis Heidenheim',
    'HEI': 'Heide = Kreisstadt Dithmarschen',
    'HG': 'Bad Homburg = Kreisstadt Hochtaunuskreis',
    'HGW': 'Greifswald, Kreisname fehlt in translations',
    'HOM': 'Homburg = Kreisstadt Saarpfalz-Kreis',
    'HR': 'Homberg/Efze = Kreisstadt Schwalm-Eder-Kreis',
    'HVL': 'Rathenow = Kreisstadt Havelland',
    'HX': 'Warburg liegt im Kreis Hoexter',
    'LDS': 'Koenigs Wusterhausen = Kreisstadt Dahme-Spreewald',
    'LM': 'Limburg = Kreisstadt Limburg-Weilburg',
    'MOS': 'Mosbach = Kreisstadt Neckar-Odenwald-Kreis',
    'MR': 'Marburg = Kreisstadt Marburg-Biedenkopf',
    'MSE': 'Neustrelitz liegt in Mecklenburgischer Seenplatte',
    'MSH': 'Sangerhausen liegt in Mansfeld-Suedharz',
    'MU': 'Waldkraiburg liegt im Landkreis Muenchen',
    'NEW': 'Neustadt a.d.Waldnaab, nur Schreibweise',
    'NI': 'Nienburg/Weser, nur Slash-Unterschied',
    'NOH': 'Nordhorn = Kreisstadt Grafschaft Bentheim',
    'OG': 'Offenburg = Kreisstadt Ortenaukreis',
    'OHA': 'Osterode seit 2016 im LK Goettingen',
    'OPR': 'Neuruppin = Kreisstadt Ostprignitz-Ruppin',
    'PIR': 'Pirna = Kreisstadt Saechs.Schweiz-Osterzgebirge',
    'TF': 'Luckenwalde = Kreisstadt Teltow-Flaeming',
    'UM': 'Schwedt liegt in Uckermark',
    'VG': 'Vorderer Vogelsberg liegt im Vogelsbergkreis',
    'WEN': 'Weiden i.d.OPf., nur Abkuerzung',
    'WT': 'Waldshut-Tiengen = Kreisstadt Landkreis Waldshut',
    'HE': 'Soltau = Kreisstadt Heidekreis',
    'WUN': 'Wunsiedel im Fichtelgebirge, nur Schreibweise',
}

# Sonderbehandlung: Umlaute in Keys werden separat gemappt
AUSNAHMEN_EXTRA = {
    'F\xdcS': 'Fuessen liegt im Landkreis Ostallgaeu',
    'M\xdc': 'Waldkraiburg liegt im Landkreis Muenchen',
}
AUSNAHMEN.update(AUSNAHMEN_EXTRA)

referenz = {}
with open(CSV_, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        referenz[row['kfz'].strip()] = row['stadt'].strip()

db_kfz = {}
for kfz_id, kreis_id, kreisname in c.execute("""
    SELECT k.id, k.kreis_id, t.value
    FROM kfz_kennzeichen k
    LEFT JOIN translations t
        ON t.objekt_id=k.kreis_id AND t.pool='kreis'
        AND t.key='name' AND t.lang='de'
    WHERE k.staat_id='DE'
""").fetchall():
    db_kfz[kfz_id] = (kreis_id, kreisname or '')

def norm(s):
    return (s.upper()
            .replace('\xc4', 'AE').replace('\xd6', 'OE').replace('\xdc', 'UE')
            .replace('\xe4', 'AE').replace('\xf6', 'OE').replace('\xfc', 'UE')
            .replace('\xdf', 'SS').replace('-', ' ').replace(',', ' ').strip())

def passt(kreisname, ref_stadt):
    return norm(ref_stadt) in norm(kreisname)

print("=" * 68)
print("CHECK 1: Kennzeichen in CSV aber NICHT in DB")
print("=" * 68)
fehlend = [(k, v) for k, v in referenz.items() if k not in db_kfz]
print(f"INFO: {len(fehlend)} historische Kennzeichen fehlen in DB (kein Fehler)\n")

print("=" * 68)
print("CHECK 2: Kennzeichen in DB aber NICHT in CSV")
print("=" * 68)
unbekannt = [(k, r, n) for k, (r, n) in db_kfz.items() if k not in referenz]
if not unbekannt:
    print(f"OK - Keine unbekannten Kennzeichen\n")
else:
    print(f"INFO: {len(unbekannt)} Kennzeichen ohne CSV-Referenz\n")
    for kfz, krid, kname in sorted(unbekannt):
        print(f"  {kfz:8s}  {krid:10s}  {kname}")
    print()

print("=" * 68)
print("CHECK 3: Verdaechtige Zuordnungen (Ausnahmen beruecksichtigt)")
print("=" * 68)
verdaechtig = []
ok_count = ausnahmen_count = 0

for kfz, (kreis_id, kreisname) in db_kfz.items():
    if kfz not in referenz:
        continue
    if kfz in AUSNAHMEN:
        ausnahmen_count += 1
        continue
    ref_stadt = referenz[kfz]
    if not kreisname:
        verdaechtig.append((kfz, kreis_id, kreisname, ref_stadt, 'Kein Kreisname'))
    elif passt(kreisname, ref_stadt):
        ok_count += 1
    else:
        verdaechtig.append((kfz, kreis_id, kreisname, ref_stadt, ''))

if not verdaechtig:
    print(f"OK - Alle Kennzeichen plausibel")
    print(f"     {ok_count} korrekt, {ausnahmen_count} bekannte Ausnahmen\n")
else:
    print(f"WARNUNG: {len(verdaechtig)} unerwartete Zuordnungen!\n")
    print(f"{'KFZ':6s}  {'Ref-Stadt':25s}  Kreisname in DB")
    print("-" * 70)
    for kfz, krid, kname, ref, hint in sorted(verdaechtig):
        h = f"  <- {hint}" if hint else ""
        print(f"{kfz:6s}  {ref:25s}  {kname or '(leer)'}{h}")
    print()

print("=" * 68)
print("CHECK 4: Staedte >20.000 EW ohne KFZ-Kennzeichen")
print("=" * 68)
rows = c.execute("""
    SELECT t.value, s.einwohner, s.kreis_id
    FROM stadt s
    JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name'
    WHERE s.staat_id='DE' AND s.einwohner > 20000
    AND s.kreis_id IS NOT NULL
    AND NOT EXISTS (SELECT 1 FROM kfz_kennzeichen k WHERE k.kreis_id=s.kreis_id)
    ORDER BY s.einwohner DESC LIMIT 20
""").fetchall()
if not rows:
    print("OK\n")
else:
    for name, ew, kid in rows:
        print(f"{name:30s} {ew:>10,}  {kid}")
    print()

print("=" * 68)
print("CHECK 5: Staedte >50.000 EW mit kreis_id=None")
print("=" * 68)
rows2 = c.execute("""
    SELECT t.value, s.einwohner, s.bundesland_id
    FROM stadt s
    JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name'
    WHERE s.staat_id='DE' AND s.einwohner > 50000 AND s.kreis_id IS NULL
    ORDER BY s.einwohner DESC LIMIT 10
""").fetchall()
if not rows2:
    print("OK\n")
else:
    print("(Stadtteile Berlin/Hamburg/Bremen sind normal)")
    for name, ew, bl in rows2:
        print(f"{name:30s} {ew:>10,}  {bl}")
    print()

print("=" * 68)
status = "OK" if not verdaechtig else "WARNUNG"
print(f"  [{status}]  CSV: {len(referenz)}  DB: {len(db_kfz)}  "
      f"Fehlend: {len(fehlend)}  Unbekannt: {len(unbekannt)}  "
      f"Verdaechtig: {len(verdaechtig)}  Ausnahmen: {ausnahmen_count}")
print("=" * 68)
conn.close()
