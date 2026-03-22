# -*- coding: utf-8 -*-
"""
explore_vg250.py — Erkundet die BKG VG250 GeoPackage-Datei
Aufruf: python explore_vg250.py
"""
import zipfile, os
from pathlib import Path

DEST = Path("geonames_data/vg250.zip")

print("=== VG250 Explorer ===\n")

# 1. ZIP-Inhalt
with zipfile.ZipFile(DEST) as zf:
    print("Dateien im ZIP:")
    for name in sorted(zf.namelist()):
        info = zf.getinfo(name)
        print(f"  {name:60s} {info.file_size//1024:6d} KB")

# 2. GeoPackage laden und Layer auflisten
print("\nVersuche GeoPackage zu lesen...")
try:
    import geopandas as gpd

    # GeoPackage aus ZIP extrahieren
    with zipfile.ZipFile(DEST) as zf:
        gpkg_name = next(n for n in zf.namelist() if n.endswith('.gpkg'))
        print(f"Extrahiere {gpkg_name}...")
        zf.extract(gpkg_name, 'geonames_data/')
        gpkg_path = f"geonames_data/{gpkg_name}"

    # Layer auflisten mit pyogrio
    import pyogrio
    layers = pyogrio.list_layers(gpkg_path)
    print(f"\nLayer im GeoPackage ({len(layers)} Stück):")
    for layer_name, geom_type in layers:
        gdf = gpd.read_file(gpkg_path, layer=layer_name, max_features=3)
        print(f"\n  Layer: {layer_name!r} ({geom_type})")
        print(f"  Spalten: {[c for c in gdf.columns if c != 'geometry']}")
        if len(gdf) > 0:
            row = gdf.iloc[0]
            for col in gdf.columns:
                if col != 'geometry':
                    print(f"    {col}: {row[col]!r}")

except Exception as e:
    print(f"Fehler: {e}")
    import traceback
    traceback.print_exc()
