# -*- coding: utf-8 -*-
"""
fix_kfz_manuell.py — Manuelle Korrekturen für die verbleibenden Fehler
die fix_kfz_zuordnung.py nicht automatisch lösen konnte.

Analyse:
  A    → München (09161) — Landshut(09261) und Aichach-Friedberg(09771) falsch
  AB   → Aschaffenburg Stadt (09661) — Kitzingen falsch
  AN   → Ansbach Stadt (09561) — Amberg falsch
  AW   → Ahrweiler ist kreis_id 07131, Altenkirchen(Westerwald) 07132 falsch
  BA   → Bamberg Stadt (09461) korrekt, Bayreuth(09462) ist Duplikat-Fehler
  BM   → Erftstadt liegt in Rhein-Erft-Kreis (05362) — Düren falsch
  BT   → Bayreuth Stadt (09462) — Bamberg(09471) falsch
  COE  → Coesfeld (05558) korrekt — kein Fehler
  DLG  → Dillingen a.d.Donau (09773) korrekt, Straubing(09263) falsch
  EA   → Eisenach Stadt (16056) — Kyffhäuserkreis falsch
  FÜS  → Ostallgäu (09777) für Füssen — Landshut falsch
  GM   → Oberbergischer Kreis (05374) für Gummersbach/Wiehl — Euskirchen falsch
  GR   → Görlitz (14626) für Weißwasser/Görlitz — beide falsch
  GT   → Gütersloh (05754) korrekt
  HD   → Rhein-Neckar-Kreis (08226) für Sinsheim/Heidelberg Umland falsch
         Heidelberg Stadt (08221) und Heilbronn (08125) beide falsch
  HDH  → Heidenheim (08135) korrekt
  HEI  → Dithmarschen (01051) korrekt (Heide ist Kreisstadt)
  HG   → Hochtaunuskreis (06434) korrekt (Bad Homburg = Kreisstadt)
  HGW  → Greifswald Stadt (13009) — Rostock falsch
  HO   → Hof Stadt (09464) korrekt, Bayreuth(09472) falsch
  HOM  → Saarpfalz-Kreis (10045) für Homburg/Saar — Donnersbergkreis falsch
  HR   → Schwalm-Eder-Kreis (06634) korrekt (Homberg/Efze = Kreisstadt)
  HX   → Höxter (05762) korrekt
  LA   → Landshut Stadt (09261) — Ansbach falsch
  P    → Potsdam Stadt (12054) — Frankfurt(Oder) falsch
  PA   → Passau Stadt (09262) korrekt, Nürnberger Land(09574) falsch
  R    → Regensburg Stadt (09362) — Ansbach falsch
  SW   → Schweinfurt Stadt (09662) — Aschaffenburg falsch
  TR   → Trier Stadt (07211) — beide aktuellen Einträge falsch
  WEN  → Weiden i.d.OPf. Stadt (09363) korrekt, Schweinfurt(09662) falsch
  WÜ   → Würzburg Stadt (09663) korrekt, Augsburg(09761)+Kempten(09763) falsch

python fix_kfz_manuell.py       → Vorschau
python fix_kfz_manuell.py --fix → Schreibt in DB
"""
import sqlite3, os, sys

DRY_RUN = '--fix' not in sys.argv
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
conn = sqlite3.connect(os.path.join(BASE, 'data', 'geo.sqlite'))
c    = conn.cursor()

# Format: (kfz, falsche_kreis_id, richtige_kreis_id, begründung)
KORREKTUREN = [
    # A = München
    ('A',   '09261', '09161', 'München Stadt statt Landshut'),
    ('A',   '09771', '09161', 'München Stadt statt Aichach-Friedberg'),
    ('A',   '09772', '09161', 'München Stadt statt Augsburg-Land'),
    # AB = Aschaffenburg
    ('AB',  '09675', '09661', 'Aschaffenburg Stadt statt Kitzingen'),
    # AN = Ansbach
    ('AN',  '09361', '09561', 'Ansbach Stadt statt Amberg'),
    # AW = Ahrweiler
    ('AW',  '07132', '07131', 'Ahrweiler statt Altenkirchen (Westerwald)'),
    # BA = Bamberg — Bayreuth-Eintrag entfernen
    ('BA',  '09462', '09461', 'Bamberg Stadt statt Bayreuth'),
    # BM = Erftstadt → Rhein-Erft-Kreis
    ('BM',  '05358', '05362', 'Rhein-Erft-Kreis statt Düren'),
    # BT = Bayreuth
    ('BT',  '09471', '09462', 'Bayreuth Stadt statt Bamberg'),
    # DLG = Dillingen — Straubing entfernen
    ('DLG', '09263', '09773', 'Dillingen a.d.Donau statt Straubing'),
    # EA = Eisenach
    ('EA',  '16065', '16056', 'Eisenach Stadt statt Kyffhäuserkreis'),
    # FÜS = Füssen → Ostallgäu
    ('FÜS', '09274', '09777', 'Ostallgäu statt Landshut'),
    # GM = Gummersbach → Oberbergischer Kreis
    ('GM',  '05366', '05374', 'Oberbergischer Kreis statt Euskirchen'),
    # GR = Weißwasser/Görlitz → Görlitz Kreis
    ('GR',  '14524', '14626', 'Görlitz statt Zwickau'),
    ('GR',  '14628', '14626', 'Görlitz statt Sächs.Schweiz-Osterzgebirge'),
    # HGW = Greifswald
    ('HGW', '13003', '13009', 'Greifswald Stadt statt Rostock'),
    # HO = Hof — Bayreuth-Eintrag korrigieren
    ('HO',  '09472', '09464', 'Hof Stadt statt Bayreuth'),
    # HOM = Homburg/Saar → Saarpfalz-Kreis
    ('HOM', '07333', '10045', 'Saarpfalz-Kreis statt Donnersbergkreis'),
    # LA = Landshut
    ('LA',  '09571', '09261', 'Landshut Stadt statt Ansbach'),
    # P = Potsdam
    ('P',   '12053', '12054', 'Potsdam Stadt statt Frankfurt(Oder)'),
    # PA = Passau — Nürnberger Land entfernen
    ('PA',  '09574', '09262', 'Passau Stadt statt Nürnberger Land'),
    # R = Regensburg
    ('R',   '09561', '09362', 'Regensburg Stadt statt Ansbach'),
    # SW = Schweinfurt
    ('SW',  '09671', '09662', 'Schweinfurt Stadt statt Aschaffenburg'),
    # TR = Trier
    ('TR',  '07141', '07211', 'Trier Stadt statt Rhein-Lahn-Kreis'),
    ('TR',  '07235', '07211', 'Trier Stadt statt Trier-Saarburg'),
    # WEN = Weiden — Schweinfurt-Eintrag entfernen
    ('WEN', '09662', '09363', 'Weiden i.d.OPf. statt Schweinfurt'),
    # WÜ = Würzburg
    ('WÜ',  '09761', '09663', 'Würzburg Stadt statt Augsburg'),
    ('WÜ',  '09763', '09663', 'Würzburg Stadt statt Kempten'),
]

print("=" * 70)
print(f"fix_kfz_manuell.py  {'[VORSCHAU]' if DRY_RUN else '[SCHREIB-MODUS]'}")
print("=" * 70)
print(f"\n{'KFZ':6s}  {'Alt':10s}  {'Neu':10s}  Begründung")
print("-" * 65)
for kfz, alt, neu, grund in KORREKTUREN:
    print(f"{kfz:6s}  {alt:10s}  {neu:10s}  {grund}")

# Nicht korrigierte Fälle (korrekt oder unklar)
print("""
Nicht korrigiert (bereits korrekt):
  AA  → Ostalbkreis     (Kreisstadt Aalen, kein Fehler)
  COE → Coesfeld        (korrekt)
  GT  → Gütersloh       (korrekt)
  HD  → Heidelberg/Heilbronn  (HD=Heidelberg, beide Einträge behalten)
  HDH → Heidenheim      (korrekt)
  HEI → Dithmarschen    (Heide = Kreisstadt, korrekt)
  HG  → Hochtaunuskreis (Bad Homburg = Kreisstadt, korrekt)
  HR  → Schwalm-Eder    (Homberg/Efze = Kreisstadt, korrekt)
  HX  → Höxter          (korrekt)
""")

if DRY_RUN:
    print("Vorschau-Modus. Zum Anwenden: python fix_kfz_manuell.py --fix")
else:
    print(f"\nSchreibe {len(KORREKTUREN)} Korrekturen...")
    ok = fehler = 0
    for kfz, alt_id, neu_id, grund in KORREKTUREN:
        # Aktuellen staat_id und aktiv-Wert holen
        row = c.execute(
            "SELECT staat_id, aktiv FROM kfz_kennzeichen WHERE id=? AND kreis_id=?",
            (kfz, alt_id)).fetchone()
        if not row:
            print(f"  SKIP {kfz} {alt_id} — nicht in DB")
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
    print(f"Fertig: {ok} OK, {fehler} Fehler.")
    print("Bitte check_kfz_luecken.py zur Verifikation ausführen.")

conn.close()
