# -*- coding: utf-8 -*-
"""
bench_fragen.py — Misst Ladezeit der Fragengeratoren direkt in Python
Simuliert was der Browser in JS macht, aber schneller messbar.
Aufruf: python bench_fragen.py
"""
import sqlite3, time

DB = 'geo.sqlite'
c = sqlite3.connect(DB)
c.row_factory = sqlite3.Row

def t(label, fn):
    start = time.perf_counter()
    result = fn()
    ms = (time.perf_counter() - start) * 1000
    n = len(result) if hasattr(result, '__len__') else '?'
    print(f"  {label:35s} {ms:7.1f} ms  ({n} Einträge)")
    return result

print("=== Fragengerator Benchmark ===\n")

# 1. DB laden (Datei lesen)
start = time.perf_counter()
c2 = sqlite3.connect(DB)
ms = (time.perf_counter() - start) * 1000
print(f"  {'DB öffnen':35s} {ms:7.1f} ms")

# 2. Geo-Fragen
def geo():
    return c.execute("""
        SELECT s.id, t.value, s.bundesland_id, s.einwohner
        FROM stadt s
        JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name'
        WHERE s.staat_id='DE' AND s.bundesland_id IS NOT NULL AND s.einwohner IS NOT NULL
        ORDER BY s.einwohner DESC, s.id ASC LIMIT 2000
    """).fetchall()

# 3. BL-Namen
def bl_namen():
    return c.execute("""
        SELECT b.id, t.value FROM bundesland b
        JOIN translations t ON t.objekt_id=b.id AND t.lang='de' AND t.pool='bundesland'
        WHERE b.staat_id='DE'
    """).fetchall()

# 4. Höhe-Fragen
def hoehe():
    return c.execute("""
        SELECT s.id, t.value, s.hoehe_m, s.bundesland_id, s.einwohner
        FROM stadt s
        JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name'
        WHERE s.staat_id='DE' AND s.hoehe_m IS NOT NULL AND s.hoehe_m>0 AND s.einwohner>10000
        ORDER BY s.id ASC
    """).fetchall()

# 5. EW-Fragen
def ew():
    return c.execute("""
        SELECT s.id, t.value, s.einwohner, s.bundesland_id
        FROM stadt s
        JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name'
        WHERE s.staat_id='DE' AND s.einwohner>50000
        ORDER BY s.id ASC LIMIT 200
    """).fetchall()

# 6. KFZ-Fragen
def kfz():
    return c.execute("""
        SELECT s.id, t.value, k.id AS kfz, s.einwohner, s.bundesland_id
        FROM stadt s
        JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name'
        JOIN kfz_kennzeichen k ON k.kreis_id=s.kreis_id
        WHERE s.staat_id='DE' AND s.einwohner IS NOT NULL AND s.einwohner > 0
        ORDER BY s.einwohner DESC, s.id ASC LIMIT 2000
    """).fetchall()

# 7. PLZ gesamt
def plz_alle():
    return c.execute("SELECT stadt_id, plz_id FROM plz_stadt ORDER BY plz_id ASC").fetchall()

# 8. PLZ-Städte
def plz_staedte():
    return c.execute("""
        SELECT DISTINCT s.id, t.value, s.einwohner, s.bundesland_id,
               (SELECT ps2.plz_id FROM plz_stadt ps2
                WHERE ps2.stadt_id=s.id
                ORDER BY ps2.plz_id ASC LIMIT 1) AS plz_min
        FROM stadt s
        JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name'
        JOIN plz_stadt ps ON ps.stadt_id=s.id
        WHERE s.staat_id='DE' AND s.einwohner IS NOT NULL AND s.einwohner > 0
        ORDER BY s.einwohner DESC, s.id ASC LIMIT 1500
    """).fetchall()

# 9. Schablonen
def schablonen():
    return c.execute("SELECT fragetyp, attribut_id, template, attribut_label FROM schablonen WHERE lang='de'").fetchall()

print("\nEinzelne Queries:")
t("BL-Namen",      bl_namen)
t("Geo-Query",     geo)
t("Höhe-Query",    hoehe)
t("EW-Query",      ew)
t("KFZ-Query",     kfz)
t("PLZ alle",      plz_alle)
t("PLZ-Städte",    plz_staedte)
t("Schablonen",    schablonen)

print("\nGesamtzeit simuliert:")
start = time.perf_counter()
bl_namen(); geo(); hoehe(); ew(); kfz(); plz_alle(); plz_staedte(); schablonen()
ms = (time.perf_counter() - start) * 1000
print(f"  {'Alle Queries zusammen':35s} {ms:7.1f} ms")

# 10. geo.sqlite Dateigröße
import os
size_mb = os.path.getsize(DB) / 1024 / 1024
print(f"\n  geo.sqlite: {size_mb:.1f} MB")
print("\nHinweis: Browser lädt zusätzlich die gesamte Datei über HTTP (fetch)")
print("         Das erklärt den Großteil der 20s wenn geo.sqlite 17MB hat!")
