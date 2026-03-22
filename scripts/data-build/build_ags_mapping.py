# -*- coding: utf-8 -*-
"""
build_ags_mapping.py — Exportiert Gemeinde→Kreis-Mapping aus BKG VG250
Erzeugt: geonames_data/ags_gemeinde_kreis.csv

Spalten:
  ags8      - AGS 8-stellig (Gemeinde)
  ags5      - AGS 5-stellig (Kreis)
  gen       - Gemeindename
  kreis_gen - Kreisname
  lon       - Längengrad (Dezimal)
  lat       - Breitengrad (Dezimal)

Aufruf: python build_ags_mapping.py
"""
import zipfile, geopandas as gpd
from pathlib import Path

DEST    = Path("geonames_data/vg250.zip")
OUT_CSV = Path("geonames_data/ags_gemeinde_kreis.csv")
GPKG_PATH = Path("geonames_data/vg250_12-31.utm32s.gpkg.ebenen/vg250_ebenen_1231/DE_VG250.gpkg")

print("=== VG250 → AGS-Mapping ===\n")

# GeoPackage extrahieren falls nötig
if not GPKG_PATH.exists():
    print("Extrahiere GeoPackage...")
    GPKG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DEST) as zf:
        gpkg_name = next(n for n in zf.namelist() if n.endswith('.gpkg'))
        zf.extract(gpkg_name, 'geonames_data/')
    print(f"  Extrahiert: {gpkg_name}")
else:
    print(f"  GeoPackage vorhanden: {GPKG_PATH}")

# Layer vgtb_vz_gem laden (Gemeinde→Kreis Zuordnung, ohne Geometrie)
print("\nLade vgtb_vz_gem (Gemeinde→Kreis-Mapping)...")
df = gpd.read_file(str(GPKG_PATH), layer='vgtb_vz_gem')
print(f"  {len(df)} Einträge geladen")
print(f"  Spalten: {list(df.columns)}")

# Koordinaten aus vg250_pk (Verwaltungssitz-Punkte)
print("\nLade vg250_pk (Koordinaten)...")
pk = gpd.read_file(str(GPKG_PATH), layer='vg250_pk')
print(f"  {len(pk)} Punkte geladen")

# Koordinaten-Map: ARS → (lon, lat)
koord = {}
for _, row in pk.iterrows():
    ars = str(row['ARS']).zfill(12)
    koord[ars] = (float(row['LON_DEZ']), float(row['LAT_DEZ']))

# Mapping aufbauen
print("\nErstelle Mapping...")
rows = []
kein_ars_k = 0

for _, row in df.iterrows():
    ars_g = str(row['ARS_G']).zfill(12)  # 12-stellig
    ags_g = str(row['AGS_G']).zfill(8)   # 8-stellig
    ars_k = str(row['ARS_K']).zfill(5)   # 5-stellig = Kreis-AGS
    gen_g = str(row['GEN_G'])
    kreis_gen = str(row['GEN_K'])

    # Koordinaten
    lon, lat = koord.get(ars_g, (None, None))

    # AGS5 = erste 5 Stellen von AGS8
    ags5 = ags_g[:5]

    # Plausibilitätsprüfung
    if ars_k == '-----' or ars_k == '00000':
        kein_ars_k += 1
        continue

    rows.append({
        'ags8':      ags_g,
        'ags5':      ags5,
        'ars_k':     ars_k,  # Kreis-ARS (identisch mit AGS5 für Kreise)
        'gen':       gen_g,
        'kreis_gen': kreis_gen,
        'lon':       lon,
        'lat':       lat,
    })

import pandas as pd
result = pd.DataFrame(rows)
result.to_csv(OUT_CSV, index=False, encoding='utf-8')

print(f"\n✓ {len(result)} Gemeinden exportiert")
print(f"  {kein_ars_k} ohne Kreis-ARS übersprungen")
print(f"  Mit Koordinaten: {result['lon'].notna().sum()}")
print(f"  Gespeichert: {OUT_CSV}")

# Stichprobe
print("\nStichprobe:")
for name in ['Flensburg', 'München', 'Freiburg', 'Heidelberg', 'Berlin']:
    hit = result[result['gen'] == name]
    if len(hit) > 0:
        r = hit.iloc[0]
        print(f"  {name:25s} ags8={r['ags8']} ags5={r['ags5']} kreis={r['ars_k']} ({r['kreis_gen']})")
    else:
        print(f"  {name:25s} → NICHT GEFUNDEN")
