# -*- coding: utf-8 -*-
"""
fix_kfz_rest.py — Allerletzte echte Fehler.

python fix_kfz_rest.py       → Vorschau
python fix_kfz_rest.py --fix → Schreibt in DB
"""
import sqlite3, os, sys

DRY_RUN = '--fix' not in sys.argv
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
conn = sqlite3.connect(os.path.join(BASE, 'data', 'geo.sqlite'))
c    = conn.cursor()

KORREKTUREN = [
    # A = Augsburg (nicht München!)
    ('A',    '09162', '09761', 'Augsburg Stadt statt München'),
    # HD = Rhein-Neckar-Kreis für Sinsheim/Heidelberg-Umland
    ('HD',   '08125', '08226', 'Rhein-Neckar-Kreis statt Heilbronn'),
    # HVL = Havelland für Rathenow
    ('HVL',  '12061', '12063', 'Havelland statt Dahme-Spreewald'),
    # OPR = Ostprignitz-Ruppin für Neuruppin
    ('OPR',  '12063', '12068', 'Ostprignitz-Ruppin statt Havelland'),
    # WUN = Wunsiedel i.Fichtelgebirge
    ('WUN',  '09476', '09478', 'Wunsiedel i.Fichtelgebirge statt Kronach'),
]

# Diese bleiben als bekannte Ausnahmen (strukturell korrekt):
AUSNAHMEN = [
    ('AA',  'Ostalbkreis',     'Aalen = Kreisstadt'),
    ('AW',  'Ahrweiler',       'Bad Neuenahr-Ahrweiler = Kreisstadt'),
    ('BB',  'Böblingen',       'Herrenberg liegt im Kreis Böblingen'),
    ('BIR', 'Birkenfeld',      'Idar-Oberstein liegt im Kreis Birkenfeld'),
    ('BM',  'Rhein-Erft',      'Erftstadt liegt im Rhein-Erft-Kreis'),
    ('COE', 'Coesfeld',        'Dülmen liegt im Kreis Coesfeld'),
    ('DLG', 'Dillingen',       'Nur Schreibweise (Punkt)'),
    ('EA',  'Wartburgkreis',   'Eisenach seit 2021 eingemeindet'),
    ('EL',  'Emsland',         'Papenburg liegt in Emsland'),
    ('ERB', 'Odenwaldkreis',   'Erbach = Kreisstadt'),
    ('ES',  'Esslingen',       'Nur "am Neckar" fehlt'),
    ('ESW', 'Werra-Meißner',   'Eschwege = Kreisstadt'),
    ('FN',  'Bodenseekreis',   'Friedrichshafen = Kreisstadt'),
    ('FÜS', 'Ostallgäu',       'Füssen liegt in Ostallgäu'),
    ('GM',  'Oberberg.',       'Wiehl/Gummersbach liegt im Kreis'),
    ('GR',  'Görlitz',         'Weißwasser liegt im Kreis Görlitz'),
    ('GT',  'Gütersloh',       'Versmold liegt im Kreis'),
    ('HDH', 'Heidenheim',      'Giengen liegt im Kreis'),
     ('HEI', 'Dithmarschen',    'Heide = Kreisstadt'),
    ('HG',  'Hochtaunus',      'Bad Homburg = Kreisstadt'),
    ('HOM', 'Saarpfalz',       'Homburg = Kreisstadt'),
    ('HR',  'Schwalm-Eder',    'Homberg/Efze = Kreisstadt'),
    ('HX',  'Höxter',          'Warburg liegt im Kreis'),
    ('LDS', 'Dahme-Spreewald', 'Königs Wusterhausen = Kreisstadt'),
    ('LM',  'Limburg-Weilburg','Limburg = Kreisstadt'),
    ('MOS', 'Neckar-Odenwald', 'Mosbach = Kreisstadt'),
    ('MR',  'Marburg-Bieden.', 'Marburg = Kreisstadt'),
    ('MSE', 'Meckl.Seenplatte','Neustrelitz liegt im Kreis'),
    ('MSH', 'Mansfeld-Südharz','Sangerhausen liegt im Kreis'),
    ('MÜ',  'München Land',    'Waldkraiburg liegt im Landkreis'),
    ('NEW', 'Neustadt/Waldnaab','Nur Schreibweise'),
    ('NI',  'Nienburg/Weser',  'Nur Slash-Unterschied'),
    ('NOH', 'Grafsch.Bentheim','Nordhorn = Kreisstadt'),
    ('OG',  'Ortenaukreis',    'Offenburg = Kreisstadt'),
    ('OHA', 'Göttingen',       'Osterode seit 2016 in LK Göttingen'),
    ('PIR', 'Sächs.Schweiz',   'Pirna = Kreisstadt Sächs.Schweiz-Osterzgeb.'),
    ('TF',  'Teltow-Fläming',  'Luckenwalde = Kreisstadt'),
    ('UM',  'Uckermark',       'Schwedt liegt in Uckermark'),
    ('VG',  'Vogelsbergkreis', 'Vorderer Vogelsberg liegt im Kreis'),
    ('WEN', 'Weiden i.d.OPf.', 'Nur ausgeschrieben'),
    ('WT',  'Waldshut',        'Waldshut-Tiengen = Kreisstadt'),
    ('HGW', 'kreis_id 13009',  'Greifswald — Kreisname fehlt in translations'),
]

print("=" * 70)
print(f"fix_kfz_rest.py  {'[VORSCHAU]' if DRY_RUN else '[SCHREIB-MODUS]'}")
print("=" * 70)
print(f"\nEchte Korrekturen: {len(KORREKTUREN)}")
print(f"{'KFZ':6s}  {'Alt':10s}  {'Neu':10s}  Begründung")
print("-" * 65)
for kfz, alt, neu, grund in KORREKTUREN:
    print(f"{kfz:6s}  {alt:10s}  {neu:10s}  {grund}")

print(f"\nBekannte Ausnahmen (korrekt, kein Fix nötig): {len(AUSNAHMEN)}")
print(f"{'KFZ':6s}  {'Kreis':20s}  Grund")
print("-" * 55)
for kfz, kreis, grund in AUSNAHMEN:
    print(f"{kfz:6s}  {kreis:20s}  {grund}")

if DRY_RUN:
    print("\nVorschau-Modus. Zum Anwenden: python fix_kfz_rest.py --fix")
else:
    print(f"\nSchreibe {len(KORREKTUREN)} Korrekturen...")
    ok = fehler = skip = 0
    for kfz, alt_id, neu_id, grund in KORREKTUREN:
        row = c.execute(
            "SELECT staat_id, aktiv FROM kfz_kennzeichen WHERE id=? AND kreis_id=?",
            (kfz, alt_id)).fetchone()
        if not row:
            print(f"  SKIP {kfz} {alt_id} — nicht in DB")
            skip += 1
            continue
        staat_id, aktiv = row
        try:
            c.execute("DELETE FROM kfz_kennzeichen WHERE id=? AND kreis_id=?",
                      (kfz, alt_id))
            c.execute("""INSERT OR IGNORE INTO kfz_kennzeichen
                         (id, kreis_id, staat_id, aktiv) VALUES (?,?,?,?)""",
                      (kfz, neu_id, staat_id, aktiv if aktiv is not None else 1))
            ok += 1
        except Exception as e:
            print(f"  FEHLER {kfz} {alt_id}→{neu_id}: {e}")
            fehler += 1
    conn.commit()
    print(f"Fertig: {ok} OK, {skip} nicht gefunden, {fehler} Fehler.")
    print("Bitte check_kfz_luecken.py zur Verifikation ausführen.")

conn.close()
