# -*- coding: utf-8 -*-
"""
fix_kfz_zuordnung.py — Repariert falsch zugeordnete KFZ-Kennzeichen
Strategie: DELETE alter Eintrag + INSERT OR REPLACE neuer Eintrag
           (statt UPDATE, weil kreis_id Teil des Primary Keys ist)

python fix_kfz_zuordnung.py          → Vorschau
python fix_kfz_zuordnung.py --fix    → Schreibt in DB
"""
import sqlite3, csv, os, sys

DRY_RUN = '--fix' not in sys.argv
BASE    = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DB      = os.path.join(BASE, 'data', 'geo.sqlite')
CSV_    = os.path.join(BASE, 'data', 'kfz_kennzeichen.csv')

conn = sqlite3.connect(DB)
c    = conn.cursor()

print("=" * 70)
print(f"fix_kfz_zuordnung.py  {'[VORSCHAU]' if DRY_RUN else '[SCHREIB-MODUS]'}")
print("=" * 70)

ref = {}
with open(CSV_, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        ref[row['kfz'].strip()] = row['stadt'].strip()

def norm(s):
    return (s.upper()
            .replace('Ä','AE').replace('Ö','OE').replace('Ü','UE')
            .replace('ß','SS').replace('-',' ').replace(',',' ').strip())

db_entries = c.execute("""
    SELECT k.id, k.kreis_id, k.staat_id, k.aktiv, t.value
    FROM kfz_kennzeichen k
    LEFT JOIN translations t ON t.objekt_id=k.kreis_id AND t.pool='kreis'
        AND t.key='name' AND t.lang='de'
    WHERE k.staat_id='DE' ORDER BY k.id
""").fetchall()

def find_kreis_id(stadtname):
    n = norm(stadtname)
    treffer = c.execute("""
        SELECT DISTINCT objekt_id, value FROM translations
        WHERE pool='kreis' AND key='name' AND lang='de'
    """).fetchall()
    exact   = [(kid, kn) for kid, kn in treffer if norm(kn) == n]
    if exact: return exact
    partial = [(kid, kn) for kid, kn in treffer if n in norm(kn)]
    return partial

korrekturen   = []
nicht_loesbar = []
bereits_ok    = 0

for kfz_id, kreis_id, staat_id, aktiv, kreisname in db_entries:
    if kfz_id not in ref:
        continue
    ref_stadt = ref[kfz_id]
    if norm(ref_stadt) in norm(kreisname or ''):
        bereits_ok += 1
        continue
    kandidaten = find_kreis_id(ref_stadt)
    if len(kandidaten) == 1:
        neue_id, neuer_name = kandidaten[0]
        if neue_id != kreis_id:
            korrekturen.append((kfz_id, kreis_id, neue_id, neuer_name,
                                ref_stadt, staat_id, aktiv))
        else:
            bereits_ok += 1
    elif len(kandidaten) == 0:
        nicht_loesbar.append((kfz_id, kreis_id, kreisname or '', ref_stadt,
                              'Kein Kreis gefunden'))
    else:
        exakt = [k for k in kandidaten if norm(k[1]) == norm(ref_stadt)]
        if len(exakt) == 1:
            neue_id, neuer_name = exakt[0]
            korrekturen.append((kfz_id, kreis_id, neue_id, neuer_name,
                                ref_stadt, staat_id, aktiv))
        else:
            namen = ', '.join(f"{kid}({kn})" for kid, kn in kandidaten[:3])
            nicht_loesbar.append((kfz_id, kreis_id, kreisname or '', ref_stadt,
                                  f"{len(kandidaten)} Kandidaten: {namen}"))

print(f"\nBereits korrekt:  {bereits_ok}")
print(f"Korrigierbar:     {len(korrekturen)}")
print(f"Nicht lösbar:     {len(nicht_loesbar)}")

if korrekturen:
    print(f"\n{'KFZ':6s}  {'Ref-Stadt':25s}  {'Alt':15s}  Neu")
    print("-" * 75)
    for kfz, alt, neu, neu_name, ref_s, _, _ in korrekturen:
        print(f"{kfz:6s}  {ref_s:25s}  {alt:15s}  → {neu} ({neu_name})")

if nicht_loesbar:
    print(f"\n--- NICHT LÖSBAR ---")
    print(f"{'KFZ':6s}  {'Ref-Stadt':25s}  {'Aktuell':30s}  Grund")
    print("-" * 85)
    for kfz, kid, kname, ref_s, grund in nicht_loesbar:
        print(f"{kfz:6s}  {ref_s:25s}  {kname:30s}  {grund}")

if DRY_RUN:
    print(f"\nVorschau-Modus. Zum Anwenden: python fix_kfz_zuordnung.py --fix")
else:
    print(f"\nSchreibe {len(korrekturen)} Korrekturen...")
    ok = 0
    fehler = 0
    for kfz, alt_id, neu_id, neu_name, ref_s, staat_id, aktiv in korrekturen:
        try:
            # 1. Alten Eintrag löschen
            c.execute("DELETE FROM kfz_kennzeichen WHERE id=? AND kreis_id=?",
                      (kfz, alt_id))
            # 2. Neuen Eintrag einfügen (INSERT OR IGNORE falls schon vorhanden)
            c.execute("""INSERT OR IGNORE INTO kfz_kennzeichen
                         (id, kreis_id, staat_id, aktiv) VALUES (?,?,?,?)""",
                      (kfz, neu_id, staat_id, aktiv if aktiv is not None else 1))
            ok += 1
        except Exception as e:
            print(f"  FEHLER bei {kfz} {alt_id}→{neu_id}: {e}")
            fehler += 1
    conn.commit()
    print(f"Fertig: {ok} OK, {fehler} Fehler.")
    print("Bitte check_kfz_luecken.py erneut ausführen zur Verifikation.")

conn.close()
