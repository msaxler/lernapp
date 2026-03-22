# -*- coding: utf-8 -*-
import sqlite3, csv
from pathlib import Path

DB = 'geo.sqlite'
CSV = 'geonames_data/ags_gemeinde_kreis.csv'

c = sqlite3.connect(DB)

# 1. VG250-Map laden
import csv as csv_mod
name_map = {}
with open(CSV, encoding='utf-8', newline='') as f:
    reader = csv_mod.DictReader(f)
    for row in reader:
        ags5 = str(row.get('ags5','')).strip().zfill(5)
        gen  = str(row.get('gen','')).strip().lower()
        if gen and ags5 and gen not in name_map:
            name_map[gen] = ags5

print(f"VG250 name_map: {len(name_map)} Einträge")

# 2. Stichprobe: was steht für bekannte Städte in name_map?
for name in ['münchen', 'stuttgart', 'freiburg im breisgau', 'heidelberg', 'berlin']:
    print(f"  name_map[{name!r}] = {name_map.get(name, 'NICHT GEFUNDEN')}")

# 3. Was liefert translations für München?
print("\nTranslations für München (GeoNames 2867714):")
rows = c.execute(
    "SELECT pool, objekt_id, key, lang, value FROM translations "
    "WHERE objekt_id='2867714' AND lang='de'"
).fetchall()
for r in rows:
    print(f"  {r}")

# 4. Städte ohne kreis_id — erste 5
print("\nErste 5 Städte ohne kreis_id:")
rows = c.execute(
    "SELECT s.id, t.value, s.kreis_id FROM stadt s "
    "JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name' "
    "WHERE s.kreis_id IS NULL AND s.staat_id='DE' AND s.einwohner > 100000 "
    "ORDER BY s.einwohner DESC LIMIT 5"
).fetchall()
for r in rows:
    name_norm = r[1].split(',')[0].strip().lower()
    in_map = name_map.get(name_norm, 'NICHT GEFUNDEN')
    print(f"  id={r[0]} name={r[1]!r} norm={name_norm!r} → map={in_map!r}")
