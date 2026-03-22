# -*- coding: utf-8 -*-
"""
fix_kfz_final.py — Letzte Korrekturrunde für verbleibende echte Fehler.

python fix_kfz_final.py       → Vorschau
python fix_kfz_final.py --fix → Schreibt in DB
"""
import sqlite3, os, sys

DRY_RUN = '--fix' not in sys.argv
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
conn = sqlite3.connect(os.path.join(BASE, 'data', 'geo.sqlite'))
c    = conn.cursor()

# Format: (kfz, falsche_kreis_id, richtige_kreis_id, begründung)
# Nur echte Fehler — Fälle wo Kreisstadt korrekt im Kreis liegt werden NICHT korrigiert
KORREKTUREN = [
    # A = München — Ingolstadt ist falsch
    ('A',    '09161', '09162', 'München Stadtkreis statt Ingolstadt'),
    # AP = Weimar
    ('AP',   '16066', '16055', 'Weimar Stadt statt Schmalkalden-Meiningen'),
    # EA = Eisenach — 16056 existiert nicht mehr (Eingemeindung 2021)
    # Eisenach gehört jetzt zum Wartburgkreis 16063
    ('EA',   '16056', '16063', 'Wartburgkreis (Eisenach eingemeindet 2021)'),
    # EL = Emsland für Papenburg (Papenburg liegt in Emsland)
    ('EL',   '03456', '03454', 'Emsland statt Grafschaft Bentheim'),
    # ERB = Odenwaldkreis für Erbach (Erbach = Kreisstadt Odenwaldkreis — korrekt!)
    # SKIP
    # ESW = Werra-Meißner für Eschwege (Eschwege = Kreisstadt — korrekt!)
    # SKIP
    # FÜS = Ostallgäu für Füssen (Füssen liegt in Ostallgäu ✓ — korrekt!)
    # SKIP
    # GR = Görlitz für Weißwasser — Weißwasser liegt im Landkreis Görlitz ✓
    # SKIP
    # HE = Soltau → Heidekreis
    ('HE',   '03153', '03358', 'Heidekreis statt Goslar'),
    # HVL = Havelland für Rathenow (Rathenow = Kreisstadt Havelland ✓ — korrekt!)
    # SKIP
    # LDS = Dahme-Spreewald für Königs Wusterhausen
    ('LDS',  '12068', '12061', 'Dahme-Spreewald statt Ostprignitz-Ruppin'),
    # MOS = Mosbach → Neckar-Odenwald-Kreis (nicht Rhein-Neckar)
    ('MOS',  '08226', '08225', 'Neckar-Odenwald-Kreis statt Rhein-Neckar'),
    # MSE = Mecklenburgische Seenplatte für Neustrelitz (Neustrelitz liegt drin ✓)
    # SKIP — beide korrekt
    # MSH = Mansfeld-Südharz für Sangerhausen
    ('MSH',  '15086', '15087', 'Mansfeld-Südharz statt Jerichower Land'),
    # NEW = Neustadt an der Waldnaab → Neustadt a.d. Waldnaab Kreis
    ('NEW',  '09478', '09374', 'Neustadt a.d.Waldnaab statt Lichtenfels'),
    ('NEW',  '09663', '09374', 'Neustadt a.d.Waldnaab statt Würzburg'),
    # NI = Nienburg → Nienburg(Weser) Kreis
    ('NI',   '03257', '03256', 'Nienburg(Weser) statt Schaumburg'),
    # NOH = Grafschaft Bentheim für Nordhorn (Nordhorn liegt in Grafschaft Bentheim)
    ('NOH',  '03455', '03456', 'Grafschaft Bentheim statt Friesland'),
    # OG = Ortenaukreis für Offenburg (Offenburg = Kreisstadt ✓ — korrekt!)
    # SKIP
    # OHA = Northeim für Osterode (Osterode liegt in Göttingen seit 2016)
    ('OHA',  '03155', '03159', 'Göttingen statt Northeim'),
    # OPR = Ostprignitz-Ruppin für Neuruppin (Neuruppin = Kreisstadt ✓ — korrekt!)
    # SKIP
    # PIR = Görlitz für Pirna — Pirna liegt in Sächsische Schweiz-Osterzgebirge
    ('PIR',  '14626', '14628', 'Sächs.Schweiz-Osterzgebirge statt Görlitz'),
    # TF = Teltow-Fläming für Luckenwalde (Luckenwalde = Kreisstadt ✓ — korrekt!)
    # SKIP
    # UM = Uckermark für Schwedt (Schwedt liegt in Uckermark ✓ — korrekt!)
    # SKIP — 12073 korrekt, 12067 (Oder-Spree) falsch
    ('UM',   '12067', '12073', 'Uckermark statt Oder-Spree'),
    # VG = Vogelsbergkreis für Vorderer Vogelsberg
    ('VG',   '13076', '06535', 'Vogelsbergkreis statt Ludwigslust-Parchim'),
]

print("=" * 70)
print(f"fix_kfz_final.py  {'[VORSCHAU]' if DRY_RUN else '[SCHREIB-MODUS]'}")
print("=" * 70)
print(f"\n{'KFZ':6s}  {'Alt':10s}  {'Neu':10s}  Begründung")
print("-" * 65)
for kfz, alt, neu, grund in KORREKTUREN:
    print(f"{kfz:6s}  {alt:10s}  {neu:10s}  {grund}")

print(f"\nGesamt: {len(KORREKTUREN)} Korrekturen")

if DRY_RUN:
    print("\nVorschau-Modus. Zum Anwenden: python fix_kfz_final.py --fix")
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
