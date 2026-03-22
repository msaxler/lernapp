#!/usr/bin/env python3
"""
AP1 — GeoNames Basispools (Pareto-Minimalversion)
Baut: staat (DE only+Nachbarn), bundesland, kreis, stadt
Quelle: GeoNames allCountries.zip + admin1CodesASCII.txt + admin2Codes.txt

Starten: python ap1_build_pools.py
Output:  geo.sqlite
"""

import sqlite3, urllib.request, zipfile, io, os, sys, csv, re, ssl
from pathlib import Path

DB_PATH   = "geo.sqlite"
DATA_DIR  = Path("geonames_data")
DATA_DIR.mkdir(exist_ok=True)

# SSL-Kontext ohne Zertifikatsprüfung (nötig für destatis.de)
_SSL_NO_VERIFY = ssl.create_default_context()
_SSL_NO_VERIFY.check_hostname = False
_SSL_NO_VERIFY.verify_mode = ssl.CERT_NONE

# ─── Download-Hilfsfunktion ──────────────────────────────────
def download(url, dest):
    if dest.exists():
        print(f"  Vorhanden: {dest.name}")
        return
    print(f"  Lade: {dest.name} ...", end=" ", flush=True)
    # Behörden-Websites (destatis.de etc.) haben oft Self-Signed-Certs
    try:
        urllib.request.urlretrieve(url, dest)
    except Exception:
        opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=_SSL_NO_VERIFY))
        with opener.open(url) as r, open(dest, 'wb') as f:
            f.write(r.read())
    print("fertig")

# ─── SQLite aufbauen ─────────────────────────────────────────
def create_schema(con):
    con.executescript("""
    CREATE TABLE IF NOT EXISTS staat (
        id              TEXT PRIMARY KEY,  -- ISO 3166-1 alpha-2
        iso3            TEXT,
        einwohner       INTEGER,
        flaeche_km2     REAL,
        kontinent_code  TEXT,
        tld             TEXT,
        kfz_code        TEXT,
        lat             REAL,
        lon             REAL
    );

    CREATE TABLE IF NOT EXISTS bundesland (
        id              TEXT PRIMARY KEY,  -- ISO 3166-2 z.B. DE-BY
        staat_id        TEXT REFERENCES staat(id),
        kuerzel         TEXT,              -- BY, NW ...
        geonames_code   TEXT,              -- admin1 code in GeoNames
        lat             REAL,
        lon             REAL
    );

    CREATE TABLE IF NOT EXISTS kreis (
        id              TEXT PRIMARY KEY,  -- AGS 5-stellig z.B. '09162'
        bundesland_id   TEXT REFERENCES bundesland(id),
        staat_id        TEXT REFERENCES staat(id),
        geonames_code   TEXT,
        typ             TEXT,              -- 'Landkreis','kreisfreie Stadt','Stadtkreis'
        einwohner       INTEGER,
        flaeche_km2     REAL,
        lat             REAL,
        lon             REAL
    );

    CREATE TABLE IF NOT EXISTS stadt (
        id              TEXT PRIMARY KEY,  -- GeoNames ID
        staat_id        TEXT REFERENCES staat(id),
        bundesland_id   TEXT,
        kreis_id        TEXT,
        parent_id       TEXT,
        ebene           TEXT DEFAULT 'stadt',
        lat             REAL NOT NULL,
        lon             REAL NOT NULL,
        einwohner       INTEGER,
        hoehe_m         INTEGER,
        ist_kuestenstadt INTEGER DEFAULT 0,
        feature_code    TEXT
    );

    CREATE TABLE IF NOT EXISTS translations (
        pool        TEXT NOT NULL,
        objekt_id   TEXT NOT NULL,
        key         TEXT NOT NULL,
        lang        TEXT NOT NULL,
        value       TEXT NOT NULL,
        PRIMARY KEY (pool, objekt_id, key, lang)
    );

    CREATE INDEX IF NOT EXISTS idx_stadt_staat    ON stadt(staat_id);
    CREATE INDEX IF NOT EXISTS idx_stadt_bl       ON stadt(bundesland_id);
    CREATE INDEX IF NOT EXISTS idx_trans_lookup   ON translations(pool, objekt_id, lang);

    CREATE TABLE IF NOT EXISTS kfz_kennzeichen (
        id              TEXT NOT NULL,     -- z.B. 'M', 'B', 'HH', 'LPP'
        kreis_id        TEXT REFERENCES kreis(id),
        staat_id        TEXT REFERENCES staat(id),
        aktiv           INTEGER DEFAULT 1, -- 1=aktiv, 0=historisch/reaktiviert
        PRIMARY KEY (id, kreis_id)         -- ein Kennzeichen kann mehrere Kreise haben
    );

    CREATE TABLE IF NOT EXISTS plz (
        id              TEXT PRIMARY KEY,  -- 5-stellige PLZ z.B. '80331'
        staat_id        TEXT REFERENCES staat(id),
        osm_id          TEXT               -- OSM-Relation-ID
    );

    CREATE TABLE IF NOT EXISTS schablonen (
        fragetyp        TEXT NOT NULL,
        lang            TEXT NOT NULL,
        attribut_id     TEXT,
        template        TEXT NOT NULL,
        attribut_label  TEXT NOT NULL,
        antwort_prefix  TEXT DEFAULT '',
        PRIMARY KEY (fragetyp, lang, attribut_id)
    );
    """)
    con.commit()
    print("  Schema erstellt")

# ─── Staat befüllen (nur DE + direkte Nachbarn) ──────────────
NACHBARN_DE = {'DE','AT','CH','FR','LU','BE','NL','DK','PL','CZ'}

def load_staat(con):
    url  = "https://download.geonames.org/export/dump/countryInfo.txt"
    dest = DATA_DIR / "countryInfo.txt"
    download(url, dest)

    inserted = 0
    with open(dest, encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('#'): continue
            parts = line.strip().split('\t')
            if len(parts) < 9: continue  # mindestens 9 Felder nötig
            iso2 = parts[0].strip()
            if len(iso2) != 2: continue  # nur gültige ISO-Codes
            if iso2 not in NACHBARN_DE: continue
            try:
                einw      = int(parts[7])    if len(parts) > 7  and parts[7]  else None
                flaeche   = float(parts[6])  if len(parts) > 6  and parts[6]  else None
                kontinent = parts[8]         if len(parts) > 8  else ''
                tld       = parts[9]         if len(parts) > 9  else ''
                kfz       = parts[12]        if len(parts) > 12 else ''
                name_en   = parts[4]         if len(parts) > 4  else iso2
                iso3      = parts[1]         if len(parts) > 1  else ''
                # lat/lon stehen nicht in countryInfo.txt — auf None setzen
                lat = None
                lon = None
            except Exception as ex:
                print(f"    Warnung {iso2}: {ex}")
                continue
            con.execute("""INSERT OR REPLACE INTO staat
                (id, iso3, einwohner, flaeche_km2, kontinent_code, tld, kfz_code, lat, lon)
                VALUES (?,?,?,?,?,?,?,?,?)""",
                (iso2, iso3, einw, flaeche, kontinent, tld, kfz, lat, lon))
            con.execute("""INSERT OR REPLACE INTO translations
                (pool, objekt_id, key, lang, value) VALUES (?,?,?,?,?)""",
                ('staat', iso2, 'name', 'de', name_en))
            con.execute("""INSERT OR REPLACE INTO translations
                (pool, objekt_id, key, lang, value) VALUES (?,?,?,?,?)""",
                ('staat', iso2, 'name', 'en', name_en))
            inserted += 1
    con.commit()
    print(f"  staat: {inserted} Einträge")

# ─── Bundesland (admin1) für DE ───────────────────────────────
# ISO 3166-2 Mapping: GeoNames admin1-Code → ISO-Kürzel
BUNDESLAND_MAP = {
    '01': ('DE-BW', 'BW', 'Baden-Württemberg'),
    '02': ('DE-BY', 'BY', 'Bayern'),
    '03': ('DE-HB', 'HB', 'Bremen'),
    '04': ('DE-HH', 'HH', 'Hamburg'),
    '05': ('DE-HE', 'HE', 'Hessen'),
    '06': ('DE-NI', 'NI', 'Niedersachsen'),
    '07': ('DE-NW', 'NW', 'Nordrhein-Westfalen'),
    '08': ('DE-RP', 'RP', 'Rheinland-Pfalz'),
    '09': ('DE-SL', 'SL', 'Saarland'),
    '10': ('DE-SH', 'SH', 'Schleswig-Holstein'),
    '11': ('DE-BB', 'BB', 'Brandenburg'),
    '12': ('DE-MV', 'MV', 'Mecklenburg-Vorpommern'),
    '13': ('DE-SN', 'SN', 'Sachsen'),
    '14': ('DE-ST', 'ST', 'Sachsen-Anhalt'),
    '15': ('DE-TH', 'TH', 'Thüringen'),
    '16': ('DE-BE', 'BE', 'Berlin'),
}

def load_bundesland(con):
    url  = "https://download.geonames.org/export/dump/admin1CodesASCII.txt"
    dest = DATA_DIR / "admin1CodesASCII.txt"
    download(url, dest)

    inserted = 0
    with open(dest, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 4: continue
            code_full = parts[0]  # z.B. DE.01
            if not code_full.startswith('DE.'): continue
            admin1_code = code_full.split('.')[1]
            if admin1_code not in BUNDESLAND_MAP: continue
            iso_id, kuerzel, name_de = BUNDESLAND_MAP[admin1_code]
            geonames_id = parts[3]
            # Koordinaten aus allCountries später — für jetzt NULL
            con.execute("""INSERT OR REPLACE INTO bundesland
                (id, staat_id, kuerzel, geonames_code, lat, lon)
                VALUES (?,?,?,?,NULL,NULL)""",
                (iso_id, 'DE', kuerzel, geonames_id))
            con.execute("""INSERT OR REPLACE INTO translations
                (pool, objekt_id, key, lang, value) VALUES (?,?,?,?,?)""",
                ('bundesland', iso_id, 'name', 'de', name_de))
            inserted += 1
    con.commit()
    print(f"  bundesland: {inserted} Einträge")

# ─── Kreis (admin2) für DE ────────────────────────────────────
def load_kreis(con):
    """
    Laedt Landkreise aus Destatis GV100 (amtliches Gemeindeverzeichnis).
    Satzart 40 = Kreis / kreisfreie Stadt.
    Fallback: GeoNames admin2 (Regierungsbezirke).
    """
    # GV100 — manuell herunterladen von:
    # https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/
    #         Administrativ/Archiv/GV100ADQ/GV100AD3110.html
    # → "Herunterladen (zip)" → als GV100.zip in geonames_data/ speichern
    dest = DATA_DIR / "GV100.zip"
    if not dest.exists():
        # Automatischer Download versuchen
        gv100_urls = [
            "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GV100ADQ/GV100AD3110.zip",
            "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GV100ADQ/GV100AD3109.zip",
            "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GV100ADQ/GV100AD3106.zip",
            "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GV100ADQ/GV100AD3103.zip",
            "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GV100/31122023_GV100.zip",
            "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GV100/31122022_GV100.zip",
        ]
        downloaded = False
        for url in gv100_urls:
            fname = url.split('/')[-1]
            print(f"  Versuche: {fname} ...", end=" ", flush=True)
            try:
                opener = urllib.request.build_opener(
                    urllib.request.HTTPSHandler(context=_SSL_NO_VERIFY))
                with opener.open(url, timeout=15) as r, open(dest, 'wb') as f:
                    f.write(r.read())
                print("fertig")
                downloaded = True
                break
            except Exception as e:
                print(f"fehlgeschlagen")
        if not downloaded:
            print(f"  HINWEIS: GV100.zip nicht herunterladbar.")
            print(f"  → Bitte manuell herunterladen von:")
            print(f"    https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/")
            print(f"    Gemeindeverzeichnis/Administrativ/Archiv/GV100ADQ/GV100AD3110.html")
            print(f"  → Als '{dest}' speichern, dann Script neu starten.")
            print(f"  Fallback: GeoNames admin2 (nur ~19 Eintraege)")
    else:
        print(f"  Vorhanden: {dest.name}")

    # AGS-Bundeslandschluessel (2-stellig) → ISO 3166-2
    AGS_BL = {
        "01": "DE-SH", "02": "DE-HH", "03": "DE-NI", "04": "DE-HB",
        "05": "DE-NW", "06": "DE-HE", "07": "DE-RP", "08": "DE-BW",
        "09": "DE-BY", "10": "DE-SL", "11": "DE-BE", "12": "DE-BB",
        "13": "DE-MV", "14": "DE-SN", "15": "DE-ST", "16": "DE-TH",
    }

    inserted = 0
    try:
        with zipfile.ZipFile(dest) as zf:
            fname = next(
                (n for n in zf.namelist() if n.endswith('.txt') and 'GV100' in n),
                next((n for n in zf.namelist() if n.endswith('.txt')), None)
            )
            if not fname:
                raise Exception("Keine .txt Datei im ZIP gefunden")
            print(f"    GV100: lese {fname}")
            debug_count = 0
            with zf.open(fname) as f:
                for line in io.TextIOWrapper(f, encoding="utf-8", errors="replace"):
                    if len(line) < 30: continue
                    satzart = line[0]        # 1 Zeichen: 1=BL, 4=Kreis, 5=GV, 6=Gem.
                    if satzart != '4': continue  # nur Kreise (Satzart 4)

                    ags_bl   = line[7:9]          # BL-Schlüssel 2-stellig
                    ags_full = line[10:15].strip() # AGS 5-stellig
                    name_raw = line[22:72].strip() if len(line) > 72 else line[22:].strip()

                    # Debug: erste 4 Einträge zeigen
                    if debug_count < 4:
                        print(f"      Satzart={satzart!r} BL={ags_bl!r} AGS={ags_full!r} Name={name_raw!r}")
                        debug_count += 1

                    if ags_bl not in AGS_BL: continue
                    if len(ags_full) < 5: continue

                    bl_id = AGS_BL[ags_bl]

                    # Typ und bereinigten Namen bestimmen
                    nl = name_raw.lower()
                    if "kreisfrei" in nl or "stadtkreis" in nl:
                        typ = "kreisfreie Stadt"
                        name_clean = name_raw
                    elif "landkreis" in nl:
                        typ = "Landkreis"
                        name_clean = name_raw.replace("Landkreis ", "").strip()
                    else:
                        typ = "Kreis"
                        name_clean = name_raw

                    con.execute(
                        "INSERT OR REPLACE INTO kreis"
                        " (id, bundesland_id, staat_id, typ, einwohner, flaeche_km2, lat, lon)"
                        " VALUES (?,?,?,?,NULL,NULL,NULL,NULL)",
                        (ags_full, bl_id, "DE", typ)
                    )
                    con.execute(
                        "INSERT OR REPLACE INTO translations"
                        " (pool, objekt_id, key, lang, value) VALUES (?,?,?,?,?)",
                        ("kreis", ags_full, "name", "de", name_clean)
                    )
                    inserted += 1

        con.commit()
        print(f"  kreis (Destatis GV100): {inserted} Eintraege")

        # Zweiter Durchlauf: gv100_gemeinde ist nicht mehr nötig — VG250 CSV übernimmt das
        # Tabelle trotzdem anlegen für Kompatibilität
        con.execute("CREATE TABLE IF NOT EXISTS gv100_gemeinde (name TEXT, kreis_id TEXT)")
        con.commit()

    except Exception as e:
        import traceback
        print(f"  FEHLER GV100: {e}")
        traceback.print_exc()
        print("  Fallback: GeoNames admin2...")
        _load_kreis_geonames_fallback(con)


def _load_kreis_geonames_fallback(con):
    """Fallback: GeoNames admin2 (~19 Regierungsbezirke)"""
    url  = "https://download.geonames.org/export/dump/admin2Codes.txt"
    dest = DATA_DIR / "admin2Codes.txt"
    download(url, dest)
    bl_map = {a1: iso_id for a1, (iso_id, _, _) in BUNDESLAND_MAP.items()}
    inserted = 0
    with open(dest, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 4: continue
            code_full = parts[0]
            if not code_full.startswith("DE."): continue
            segs = code_full.split(".")
            if len(segs) < 3: continue
            a1 = segs[1]
            if a1 not in bl_map: continue
            kreis_id = "DE." + a1 + "." + segs[2]
            con.execute(
                "INSERT OR REPLACE INTO kreis (id, bundesland_id, staat_id, lat, lon)"
                " VALUES (?,?,?,NULL,NULL)",
                (kreis_id, bl_map[a1], "DE")
            )
            con.execute(
                "INSERT OR REPLACE INTO translations (pool, objekt_id, key, lang, value)"
                " VALUES (?,?,?,?,?)",
                ("kreis", kreis_id, "name", "de", parts[1])
            )
            inserted += 1
    con.commit()
    print(f"  kreis (GeoNames Fallback): {inserted} Eintraege")


# ─── Stadt (allCountries) für DE ─────────────────────────────
# Feature-Codes die wir behalten (Städte/Gemeinden)
CITY_FEATURES = {
    'PPL','PPLA','PPLA2','PPLA3','PPLA4','PPLC','PPLG','PPLS','PPLX'
}

def build_ags_map_from_csv():
    """
    Laedt AGS8->Kreis-AGS5 Mapping aus BKG VG250-CSV (ags_gemeinde_kreis.csv).
    Erzeugt durch build_ags_mapping.py aus DE_VG250.gpkg.
    """
    csv_path = DATA_DIR / "ags_gemeinde_kreis.csv"
    if not csv_path.exists():
        print(f"    HINWEIS: {csv_path} nicht gefunden — Fallback auf GV100-Namen")
        return _build_gv100_name_map(), {}

    ags8_map = {}   # AGS8 (8-stellig) -> kreis_ags5
    name_map = {}   # normierter Name -> kreis_ags5
    import csv as csv_mod
    count = 0
    with open(csv_path, encoding='utf-8', newline='') as f:
        reader = csv_mod.DictReader(f)
        for row in reader:
            ags8 = str(row.get('ags8','')).strip().zfill(8)
            ags5 = str(row.get('ags5','')).strip().zfill(5)
            gen  = str(row.get('gen','')).strip().lower()
            if not ags8 or not ags5 or not gen: continue
            ags8_map[ags8] = ags5
            if gen not in name_map:
                name_map[gen] = ags5
            count += 1
    print(f"    VG250-Mapping: {count} Gemeinden (AGS8+Name->Kreis)")
    return name_map, ags8_map


def _build_gv100_name_map():
    """Fallback: GV100 Satzart 6 Name->AGS5"""
    dest = DATA_DIR / "GV100.zip"
    if not dest.exists():
        return {}
    ags_map = {}
    try:
        with zipfile.ZipFile(dest) as zf:
            fname = next(
                (n for n in zf.namelist() if n.endswith('.txt') and 'GV100' in n),
                next((n for n in zf.namelist() if n.endswith('.txt')), None)
            )
            if not fname:
                return {}
            with zf.open(fname) as f:
                for line in io.TextIOWrapper(f, encoding='utf-8', errors='replace'):
                    if len(line) < 25 or line[0] != '6': continue
                    ags5 = line[10:15].strip()
                    name_raw = line[22:72].strip()
                    if not ags5 or len(ags5) < 5: continue
                    name_norm = name_raw.split(',')[0].strip().lower()
                    if name_norm not in ags_map:
                        ags_map[name_norm] = ags5
        print(f"    GV100-Namensmap (Fallback): {len(ags_map)} Eintraege")
    except Exception as e:
        print(f"    GV100-Namensmap fehlgeschlagen: {e}")
    return ags_map


def build_gv100_ags_map():
    """Kompatibilitaets-Wrapper"""
    name_map, _ = build_ags_map_from_csv()
    return name_map


def load_stadt(con):
    url  = "https://download.geonames.org/export/dump/DE.zip"
    dest = DATA_DIR / "DE.zip"
    download(url, dest)

    # Mapping für admin1 → bundesland_id (GeoNames-Nummerierung)
    bl_map = {}
    for a1, (iso_id, _, _) in BUNDESLAND_MAP.items():
        bl_map[a1] = iso_id

    # VG250-Mapping für kreis_id-Zuweisung (BKG, AGS8+Name-basiert)
    print("  Lade VG250-Mapping für Kreis-Verknüpfung...")
    vg250_name_map, vg250_ags8_map = build_ags_map_from_csv()

    # DE.txt aus ZIP lesen
    print("  Entpacke DE.zip und lese Städte...", flush=True)
    inserted = 0
    skipped = 0
    with zipfile.ZipFile(dest) as zf:
        with zf.open('DE.txt') as f:
            for line in io.TextIOWrapper(f, encoding='utf-8'):
                parts = line.strip().split('\t')
                if len(parts) < 15: continue
                feature_class = parts[6]
                feature_code  = parts[7]
                if feature_class != 'P': continue  # nur populated places
                if feature_code not in CITY_FEATURES: continue
                geonames_id  = parts[0]
                name         = parts[1]
                lat          = float(parts[4]) if parts[4] else None
                lon          = float(parts[5]) if parts[5] else None
                admin1       = parts[10]  # Bundesland-Code (01-16)
                admin2       = parts[11]  # Kreis-Code
                einwohner    = int(parts[14]) if parts[14] else None
                hoehe        = int(parts[16]) if parts[16] else None
                bl_id = bl_map.get(admin1)
                # kreis_id über VG250-Mapping (Name-basiert, VG250 hat deutschen Namen)
                kreis_id = None
                name_norm = name.split(',')[0].strip().lower()
                if name_norm in vg250_name_map:
                    kreis_id = vg250_name_map[name_norm]
                else:
                    # Fallback: ASCII-Name
                    ascii_name = parts[2].split(',')[0].strip().lower() if len(parts) > 2 else ''
                    if ascii_name and ascii_name in vg250_name_map:
                        kreis_id = vg250_name_map[ascii_name]

                con.execute("""INSERT OR REPLACE INTO stadt
                    (id, staat_id, bundesland_id, kreis_id, lat, lon,
                     einwohner, hoehe_m, feature_code)
                    VALUES (?,?,?,?,?,?,?,?,?)""",
                    (geonames_id, 'DE', bl_id, kreis_id,
                     lat, lon, einwohner, hoehe, feature_code))
                con.execute("""INSERT OR REPLACE INTO translations
                    (pool, objekt_id, key, lang, value) VALUES (?,?,?,?,?)""",
                    ('stadt', geonames_id, 'name', 'de', name))
                inserted += 1
                if inserted % 5000 == 0:
                    print(f"    {inserted} Städte...", flush=True)
                    con.commit()

    con.commit()
    print(f"  stadt: {inserted} Einträge (DE)")

# --- Deutsche Alternativnamen aus alternateNamesV2.zip ----------
def load_alternatenamen_de(con):
    url  = "https://download.geonames.org/export/dump/alternateNamesV2.zip"
    dest = DATA_DIR / "alternateNamesV2.zip"
    download(url, dest)

    # Alle deutschen Stadt-IDs laden
    stadt_ids = set(
        row[0] for row in con.execute("SELECT id FROM stadt WHERE staat_id='DE'")
    )
    print(f"  {len(stadt_ids)} Stadt-IDs geladen")

    updated = 0
    print("  Lese alternateNamesV2.zip...", flush=True)
    with zipfile.ZipFile(dest) as zf:
        alle_dateien = zf.namelist()
        print(f"    Dateien im ZIP: {alle_dateien[:5]}")
        # Explizit alternateNamesV2.txt wählen, nicht die Sprachcodes-Datei
        fname = next((n for n in alle_dateien if 'alternateNames' in n and n.endswith('.txt')), None)
        if not fname:
            fname = next((n for n in alle_dateien if n.endswith('.txt')), alle_dateien[0])
        print(f"    Lese: {fname}")
        # Sprach-Codes die deutsch bedeuten
        DE_LANGS = {'de', 'deu', 'ger'}
        debug_zeilen = 0
        found_de = 0
        with zf.open(fname) as f:
            for line in io.TextIOWrapper(f, encoding='utf-8'):
                parts = line.strip().split("\t")
                if len(parts) < 4: continue
                lang        = parts[2]
                geonames_id = parts[1]
                alt_name    = parts[3]
                is_historic = parts[7] if len(parts) > 7 else ""

                # Debug: erste 3 Zeilen ausgeben
                if debug_zeilen < 3:
                    print(f"    Beispiel: lang={lang!r} id={geonames_id} name={alt_name!r}")
                    debug_zeilen += 1

                if lang in DE_LANGS:
                    found_de += 1

                if lang not in DE_LANGS: continue
                if geonames_id not in stadt_ids: continue
                if is_historic == "1": continue

                con.execute(
                    "INSERT OR REPLACE INTO translations"
                    " (pool, objekt_id, key, lang, value) VALUES (?,?,?,?,?)",
                    ("stadt", geonames_id, "name", "de", alt_name))
                updated += 1
                if updated % 10000 == 0:
                    print(f"    {updated} Namen aktualisiert...", flush=True)
                    con.commit()
        print(f"    Gefundene DE-Zeilen gesamt: {found_de}")

    con.commit()
    print(f"  alternateNames DE: {updated} Eintraege aktualisiert")

    # Kreis-ID Nachbesserung: Städte ohne kreis_id via deutschen Namen nachschlagen
    name_map, ags8_map = build_ags_map_from_csv()
    if ags8_map or name_map:
        fixed = 0
        rows = con.execute(
            "SELECT s.id FROM stadt s WHERE s.kreis_id IS NULL AND s.staat_id='DE'"
        ).fetchall()

        for (sid,) in rows:
            kreis_id = None
            t = con.execute(
                "SELECT value FROM translations WHERE pool='stadt' AND objekt_id=? AND lang='de'",
                (sid,)).fetchone()
            if t:
                name_norm = t[0].split(',')[0].strip().lower()
                if name_norm in name_map:
                    kreis_id = name_map[name_norm]
                else:
                    treffer = [(k, v) for k, v in name_map.items()
                               if k.startswith(name_norm + ' ')
                               and not k[len(name_norm):].startswith(' (')
                               and len(name_norm) > 5]
                    if len(treffer) == 1:
                        kreis_id = treffer[0][1]
            if kreis_id:
                con.execute("UPDATE stadt SET kreis_id=? WHERE id=?", (kreis_id, sid))
                fixed += 1

        con.commit()
    # Manuelle Fixes fuer bekannte Duplikate (zwei Städte gleichen Namens, eine ohne kreis_id)
    manual_fixes = [
        ("Limburg an der Lahn", "06533"),  # GeoNames hat auch "Limburg" → VG250 matcht die kürzere Variante
        ("Muelheim an der Ruhr", "05117"), # GeoNames ohne Umlaut, VG250 hat "Mülheim an der Ruhr"
        ("Oldenburg (Oldenburg)", "03403"), # GeoNames mit Klammer, VG250 hat "Oldenburg"
    ]
    for mname, mkrz in manual_fixes:
        rows_changed = con.execute(
            "UPDATE stadt SET kreis_id=? WHERE kreis_id IS NULL AND staat_id='DE' AND id IN ("
            "  SELECT s.id FROM stadt s "
            "  JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name' "
            "  WHERE t.value=?)", (mkrz, mname)).rowcount
        if rows_changed:
            fixed += rows_changed
            print(f"    Manueller Fix: {mname} → {mkrz}")

        print(f"  kreis_id Nachbesserung (VG250): {fixed} Städte verknüpft")


# AP4: Schablonen-Tabelle befuellen (lang=de, Pareto)
def load_schablonen_de(con):
    rows = [
        # fragetyp, lang, attribut_id, template, attribut_label, antwort_prefix
        ('attributabfrage', 'de', 'bundesland_id',
         'In welchem {attribut_label} liegt {objekt_name}?', 'Bundesland', ''),
        ('attributabfrage', 'de', 'staat_id',
         'In welchem {attribut_label} liegt {objekt_name}?', 'Land', ''),
        ('schaetzung_bereich', 'de', 'hoehe_m',
         'In welchem {attribut_label} liegt {objekt_name}?', 'Höhenbereich', ''),
        ('vergleich_max', 'de', 'einwohner',
         'Welche dieser {attribut_label} hat die meisten Einwohner?', 'Staedte', ''),
        ('kfz_abfrage', 'de', 'kfz_id',
         'Welches {attribut_label} hat {objekt_name}?', 'KFZ-Kennzeichen', ''),
        ('kfz_umkehr', 'de', 'kfz_id',
         'Zu welcher Stadt gehört das Kennzeichen {wert}?', 'Kennzeichen', ''),
        ('schaetzung_wert', 'de', 'einwohner',
         'Wie viele {attribut_label} hat {objekt_name} ungefaehr?', 'Einwohner', 'ca. '),
    ]
    for row in rows:
        con.execute(
            "INSERT OR REPLACE INTO schablonen"
            " (fragetyp, lang, attribut_id, template, attribut_label, antwort_prefix)"
            " VALUES (?,?,?,?,?,?)", row)
    con.commit()
    print(f"  schablonen: {len(rows)} Eintraege (lang=de)")


# AP3: KFZ-Kennzeichen laden (AGS5 → Kennzeichen)
# Quelle: KBA + Destatis, Stand 09/2025 — eingebettet, kein Download nötig
AGS5_KFZ = {
    # Schleswig-Holstein (01)
    "01001":"FL",  "01002":"KI",  "01003":"HL",  "01004":"NMS",
    "01051":"HEI", "01053":"RZ",  "01054":"NF",  "01055":"OH",
    "01056":"PLÖ", "01057":"RD",  "01058":"SL",  "01059":"SE",
    "01060":"OD",  "01061":"IZ",  "01062":"PI",
    # Hamburg (02)
    "02000":"HH",
    # Niedersachsen (03)
    "03101":"BS",  "03102":"SZ",  "03103":"WOB",
    "03151":"GF",  "03153":"HE",  "03154":"NOM", "03155":"OHA",
    "03157":"WF",  "03158":"HM",  "03159":"GÖ",
    "03241":"H",
    "03251":"DH",  "03252":"HM",  "03254":"HOL", "03255":"MI",
    "03256":"MI",  "03257":"NI",  "03258":"HK",
    "03351":"CE",  "03352":"CUX", "03353":"WL",  "03354":"DAN",
    "03355":"LG",  "03356":"OHZ", "03357":"ROW", "03358":"HK",
    "03359":"STD", "03360":"UE",
    "03361":"CE",  "03362":"CUX", "03363":"HI",  "03364":"LG",
    "03365":"LER", "03366":"OL",  "03367":"OS",  "03368":"AUR",
    "03369":"STD",
    "03401":"DEL", "03402":"EMD", "03403":"OL",  "03404":"OS",  "03405":"WHV",
    "03451":"FRI", "03452":"ROW", "03453":"VEC", "03454":"LER",
    "03455":"NOH", "03456":"EL",  "03457":"WTM", "03458":"DAN",
    "03459":"UE",  "03460":"WST", "03461":"OHZ", "03462":"VER", "03463":"BRA",
    # Bremen (04)
    "04011":"HB",  "04012":"HB",
    # Nordrhein-Westfalen (05)
    "05111":"D",   "05112":"DU",  "05113":"E",   "05114":"KR",
    "05116":"MG",  "05117":"MH",  "05119":"OB",  "05120":"RS",
    "05122":"SG",  "05124":"W",
    "05154":"ME",  "05158":"ME",  "05162":"NE",  "05166":"VIE", "05170":"WES",
    "05314":"BN",  "05315":"K",   "05316":"LEV",
    "05334":"AC",  "05354":"EU",  "05358":"BM",  "05362":"GL",
    "05366":"GM",  "05370":"SU",  "05374":"KLE", "05378":"GL",  "05382":"SU",
    "05512":"BO",  "05513":"DO",  "05515":"GE",  "05516":"HA",
    "05517":"HAM", "05520":"HER",
    "05554":"BOR", "05558":"COE", "05562":"RE",  "05566":"ST",
    "05570":"UN",  "05574":"WAF",
    "05711":"BI",
    "05754":"GT",  "05758":"HF",  "05762":"HX",  "05766":"LIP",
    "05770":"MI",  "05774":"PB",  "05778":"SI",
    "05911":"BO",  "05913":"DO",  "05914":"HA",  "05915":"HAM", "05916":"HER",
    "05954":"EN",  "05958":"HSK", "05962":"MK",  "05966":"OE",
    "05970":"SI",  "05974":"SO",  "05978":"UN",
    # Hessen (06)
    "06411":"DA",  "06412":"F",   "06413":"OF",  "06414":"WI",   # RB Darmstadt SK
    "06431":"HP",  "06432":"DA",  "06433":"GG",  "06434":"HG",   # Bergstraße,DA-Dieburg,Groß-Gerau,Hochtaunus
    "06435":"MKK", "06436":"MTK", "06437":"ERB", "06438":"OF",   # MKK,Main-Taunus,Odenwaldkr,Offenbach LK
    "06439":"RÜD", "06440":"FB",                                  # Rheingau-Taunus,Wetterau
    "06531":"GI",  "06532":"LDK", "06533":"LM",  "06534":"MR",   # Gießen SK,Lahn-Dill,Limburg,Marburg
    "06535":"VB",                                                  # Vogelsberg
    "06611":"KS",                                                  # Kassel SK
    "06631":"FD",  "06632":"HEF", "06633":"KS",  "06634":"HR",   # Fulda,Hersfeld-R,Kassel LK,Schwalm-Eder
    "06635":"KB",  "06636":"ESW",                                  # Waldeck-Frankenberg,Werra-Meißner

    # Rheinland-Pfalz (07)
    "07111":"KO",
    "07131":"AK",  "07132":"AW",  "07133":"BIT", "07134":"MYK",
    "07135":"NR",  "07137":"SIM", "07138":"WW",  "07140":"MYK",
    "07141":"TR",  "07143":"BKS", "07144":"COC", "07145":"TR",
    "07211":"LU",
    "07231":"BKS", "07232":"BIT", "07233":"DAU", "07235":"TR",
    "07311":"FT",  "07312":"KL",
    "07313":"GER", "07314":"KH",  "07315":"BIR", "07316":"KL",
    "07317":"KIB", "07318":"KUS", "07319":"LD",  "07320":"ZW",
    "07331":"DÜW", "07332":"NW",  "07333":"HOM", "07334":"MZG",
    "07335":"NK",  "07336":"SLS", "07337":"WND", "07338":"SB",
    "07339":"RP",  "07340":"SÜW", "07341":"PS",
    # Baden-Württemberg (08)
    "08111":"S",
    "08115":"BB",  "08116":"ES",  "08117":"GP",  "08118":"LB",  "08119":"WN",
    "08121":"HN",  "08125":"HD",  "08126":"KA",  "08127":"BR",  "08128":"CW",  # 08121=Heilbronn SK
    "08135":"HDH", "08136":"AA",
    "08211":"BAD", "08212":"KA",
    "08215":"FR",  "08216":"OG",  "08217":"RA",
    "08221":"HD",  "08222":"SHA", "08223":"KÜN", "08224":"TBB", "08225":"ÖHR",  # 08221=Heidelberg SK
    "08226":"MOS",
    "08231":"KA",  "08232":"KN",  "08235":"LÖ",  "08236":"WT",  "08237":"FDS",
    "08311":"FR",  "08315":"FR",  "08316":"EM",  "08317":"OG",   # RB Freiburg
    "08325":"RW",  "08326":"VS",  "08327":"TUT", "08335":"KN",  "08336":"LÖ",
    "08337":"WT",
    "08415":"RT",  "08416":"TÜ",  "08417":"BL",   # RB Tübingen
    "08421":"UL",  "08425":"GZ",  "08426":"BCH", "08427":"MOS",
    "08435":"FN",  "08436":"RV",  "08437":"SIG",
    # Bayern (09)
    "09161":"M",   "09162":"M",   "09163":"EBE",
    "09171":"IN",  "09172":"EI",  "09173":"ND",  "09174":"PAF",
    "09175":"AIC", "09176":"DAH", "09177":"FFB", "09178":"LL",
    "09179":"STA", "09180":"TÖL", "09181":"MB",  "09182":"RO",
    "09183":"AÖ",  "09184":"MÜ",  "09185":"BGD", "09186":"TS",
    "09187":"GAP", "09188":"WM",  "09189":"TÖL", "09190":"WM",
    "09261":"A",   "09262":"AIC", "09263":"DLG", "09264":"GZ",
    "09265":"NU",  "09266":"OA",  "09267":"OAL", "09268":"MN",
    "09271":"KE",  "09272":"MM",  "09273":"LI",  "09274":"FÜS",
    "09275":"PA",  "09276":"REG", "09277":"PAN", "09278":"BOG", "09279":"DGF",
    "09361":"AN",  "09362":"ERH", "09363":"WEN", "09364":"AS",
    "09371":"ER",  "09372":"FÜ",  "09373":"N",   "09374":"SC",  "09375":"LAU",
    "09376":"SAD", "09377":"TIR",
    "09461":"BA",  "09462":"BA",  "09463":"CO",  "09464":"FO",
    "09471":"BT",  "09472":"HO",  "09473":"KC",  "09474":"KU",
    "09475":"LIF", "09476":"WUN", "09477":"TIR", "09478":"NEW", "09479":"SAD",
    "09561":"R",   "09562":"CHA", "09563":"KEH", "09564":"REG", "09565":"NM",
    "09571":"LA",  "09572":"DEG", "09573":"DGF", "09574":"PA",
    "09575":"PAN", "09576":"SR",  "09577":"BOG", "09578":"FRG",
    "09661":"AM",  "09662":"WEN", "09663":"NEW",
    "09671":"SW",  "09672":"MSP", "09673":"KT",  "09674":"HAS",
    "09675":"AB",  "09676":"MIL", "09677":"KG",  "09678":"NES", "09679":"WÜ",
    "09761":"WÜ",  "09762":"KT",  "09763":"WÜ",  "09764":"MIL",
    "09771":"A",   "09772":"A",   "09773":"DLG", "09774":"GZ",
    "09775":"NU",  "09776":"LI",  "09777":"OAL", "09778":"MN",
    "09779":"NÖ",  "09780":"OA",
    # Saarland (10)
    "10041":"SB",  "10042":"MZG", "10043":"NK",  "10044":"SLS",
    "10045":"SB",  "10046":"WND",
    # Berlin (11)
    "11000":"B",
    # Brandenburg (12)
    "12051":"CB",  "12052":"FF",  "12053":"P",
    "12054":"BAR", "12060":"EE",  "12061":"HVL", "12062":"MOL",
    "12063":"OPR", "12064":"PM",  "12065":"PR",  "12066":"TF",
    "12067":"UM",  "12068":"LDS", "12069":"LOS", "12070":"OSL",
    "12071":"SPN", "12072":"BSK", "12073":"UM",
    # Mecklenburg-Vorpommern (13)
    "13003":"HGW", "13004":"NB",  "13006":"SN",
    "13071":"MSE", "13072":"MSE", "13073":"LRO", "13074":"VR",
    "13075":"NWM", "13076":"VG",  "13077":"LUP",
    # Sachsen (14)
    "14511":"C",
    "14521":"ERZ", "14522":"BZ",  "14523":"MEI", "14524":"GR",
    "14525":"DW",  "14526":"Z",
    "14612":"DD",
    "14625":"MEI", "14626":"PIR", "14627":"BZ",  "14628":"GR",
    "14713":"L",   "14729":"DZ",  "14730":"L",
    # Sachsen-Anhalt (15)
    "15001":"DE",  "15002":"HAL", "15003":"MD",
    "15081":"ABI", "15082":"BLK", "15083":"BÖ",  "15084":"HZ",
    "15085":"JL",  "15086":"MSH", "15087":"SAW", "15088":"SK",
    "15089":"SDL", "15090":"WB",  "15091":"SLK",
    # Thüringen (16)
    "16051":"EF",  "16052":"G",   "16053":"J",   "16054":"SHL", "16055":"WE",
    "16056":"EIC", "16057":"GTH", "16058":"GRZ", "16059":"HBN", "16060":"IK",
    "16061":"KYF", "16062":"SON", "16063":"SÖM", "16064":"SM",  "16065":"EA",
    "16066":"AP",  "16067":"RU",  "16068":"SHK", "16069":"SOK", "16070":"WAK",
    "16071":"NDH", "16072":"UH",
    "16073":"RU",  "16074":"SHK", "16075":"SOK", "16076":"GRZ", "16077":"ABG",
}

def load_kfz_kennzeichen(con):
    """
    Befuellt kfz_kennzeichen-Tabelle aus AGS5_KFZ-Dict.
    Verknuepft mit kreis-Tabelle via AGS5-Schluessel.
    Kein Download noetig — Daten sind eingebettet (KBA Stand 09/2025).
    """
    # Bekannte Kreis-IDs aus DB
    kreis_ids = set(r[0] for r in con.execute("SELECT id FROM kreis"))

    inserted = 0
    kein_kreis = 0

    for ags5, kfz in AGS5_KFZ.items():
        if ags5 not in kreis_ids:
            kein_kreis += 1
            continue
        # Alle AGS5→KFZ Einträge speichern (ein Kennzeichen kann mehrere Kreise haben)
        con.execute(
            "INSERT OR REPLACE INTO kfz_kennzeichen (id, kreis_id, staat_id, aktiv)"
            " VALUES (?,?,?,1)",
            (kfz, ags5, "DE")
        )
        inserted += 1
        # translations: Kennzeichen-Name = das Kennzeichen selbst
        con.execute(
            "INSERT OR REPLACE INTO translations (pool, objekt_id, key, lang, value)"
            " VALUES (?,?,?,?,?)",
            ("kfz", kfz, "name", "de", kfz)
        )

    con.commit()
    if kein_kreis:
        print(f"    Hinweis: {kein_kreis} AGS5-Eintraege ohne Kreis-Match (GV100 noetig)")

    # Sonderfaelle: Kennzeichen die nicht 1:1 auf einen AGS5-Eintrag passen
    sonderfaelle = [
        ("RÜ", "06433", "DE"),  # Rüsselsheim am Main, zusaetzlich zu GG fuer Gross-Gerau
    ]
    for kfz, ags5, staat in sonderfaelle:
        con.execute("INSERT OR IGNORE INTO kfz_kennzeichen (id, kreis_id, staat_id, aktiv) VALUES (?,?,?,1)",
                    (kfz, ags5, staat))
        con.execute("INSERT OR REPLACE INTO translations (pool, objekt_id, key, lang, value) VALUES (?,?,?,?,?)",
                    ("kfz", kfz, "name", "de", kfz))
    con.commit()
    print(f"  kfz_kennzeichen: {inserted} Eintraege")


# AP2: PLZ-Tabelle befuellen aus zuordnung_plz_ort.csv
def load_plz(con):
    """
    Laedt PLZ aus suche-postleitzahl.org CSV.
    Verknuepft PLZ mit Stadt via Namens-Match.
    Quelle: downloads.suche-postleitzahl.org/v2/public/zuordnung_plz_ort.csv
    """
    import csv as csv_mod
    csv_path = DATA_DIR / "zuordnung_plz_ort.csv"
    if not csv_path.exists():
        print(f"  HINWEIS: {csv_path} nicht gefunden — PLZ-Tabelle leer")
        return

    inserted = 0
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv_mod.DictReader(f)
        for row in reader:
            plz    = str(row.get("plz", "")).strip().zfill(5)
            osm_id = str(row.get("osm_id", "")).strip()
            if not plz or len(plz) != 5: continue
            con.execute(
                "INSERT OR REPLACE INTO plz (id, staat_id, osm_id) VALUES (?,?,?)",
                (plz, "DE", osm_id)
            )
            # Translation: PLZ-Name = PLZ selbst
            con.execute(
                "INSERT OR REPLACE INTO translations (pool, objekt_id, key, lang, value)"
                " VALUES (?,?,?,?,?)",
                ("plz", plz, "name", "de", plz)
            )
            inserted += 1

    con.commit()
    print(f"  plz: {inserted} Eintraege ({inserted} PLZ→Stadt-Zuordnungen)")

    # Jetzt PLZ→Stadt verknuepfen via Namens-Match
    # plz_stadt Mapping: plz_id → stadt_id (ueber Ortsnamen)
    con.execute("""CREATE TABLE IF NOT EXISTS plz_stadt (
        plz_id   TEXT REFERENCES plz(id),
        stadt_id TEXT REFERENCES stadt(id),
        PRIMARY KEY (plz_id, stadt_id)
    )""")

    linked = 0
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv_mod.DictReader(f)
        for row in reader:
            plz    = str(row.get("plz", "")).strip().zfill(5)
            ort    = str(row.get("ort", "")).strip()
            if not plz or not ort: continue
            # Stadt per deutschem Namen suchen
            r = con.execute(
                "SELECT s.id FROM stadt s "
                "JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name' "
                "WHERE t.value=? AND s.staat_id='DE' "
                "ORDER BY s.einwohner DESC NULLS LAST LIMIT 1",
                (ort,)).fetchone()
            if r:
                con.execute(
                    "INSERT OR IGNORE INTO plz_stadt (plz_id, stadt_id) VALUES (?,?)",
                    (plz, r[0]))
                linked += 1

    con.commit()
    print(f"  plz_stadt: {linked} Verknuepfungen (PLZ↔Stadt)")

# ─── Validierung ─────────────────────────────────────────────
def validate(con):
    print("\n=== Validierung ===")
    checks = [
        ("staat", "SELECT COUNT(*) FROM staat",
         lambda n: n >= 9, f"Mindestens 9 Staaten erwartet"),
        ("bundesland", "SELECT COUNT(*) FROM bundesland WHERE staat_id='DE'",
         lambda n: n == 16, "Genau 16 Bundesländer erwartet"),
        ("kreis", "SELECT COUNT(*) FROM kreis WHERE staat_id='DE'",
         lambda n: n > 300, "Mehr als 300 Landkreise (Destatis GV100)"),
        ("stadt DE", "SELECT COUNT(*) FROM stadt WHERE staat_id='DE'",
         lambda n: n > 5000, "Mehr als 5.000 Städte erwartet"),
        ("translations", "SELECT COUNT(*) FROM translations",
         lambda n: n > 1000, "Mehr als 1.000 Translations erwartet"),
        ("münchen", "SELECT COUNT(*) FROM stadt s JOIN translations t ON t.objekt_id=s.id WHERE t.value='München' AND t.lang='de'",
         lambda n: n >= 1, "München muss vorhanden sein"),
        ("plz", "SELECT COUNT(*) FROM plz WHERE staat_id='DE'",
         lambda n: n > 8000, "Mehr als 8.000 PLZ erwartet"),
        ("kfz", "SELECT COUNT(*) FROM kfz_kennzeichen WHERE staat_id='DE'",
         lambda n: n > 300, "Mehr als 300 KFZ-Kreis-Verknuepfungen erwartet"),
        ("schablonen", "SELECT COUNT(*) FROM schablonen WHERE lang='de'",
         lambda n: n >= 3, "Mindestens 3 deutsche Schablonen erwartet"),
        ("berlin bl", "SELECT bundesland_id FROM stadt s JOIN translations t ON t.objekt_id=s.id WHERE t.value='Berlin' AND t.lang='de' AND s.feature_code='PPLC'",
         lambda v: v == 'DE-BE', "Berlin muss in DE-BE liegen"),
    ]
    passed = failed = 0
    for name, sql, check, msg in checks:
        try:
            row = con.execute(sql).fetchone()
            val = row[0] if row else None
            ok = check(val)
            status = "✓" if ok else "✗"
            print(f"  {status} {name}: {val}  — {msg}")
            if ok: passed += 1
            else: failed += 1
        except Exception as e:
            print(f"  ✗ {name}: FEHLER — {e}")
            failed += 1
    print(f"\n  {passed}/{passed+failed} Checks bestanden")
    return failed == 0

# ─── Main ────────────────────────────────────────────────────
def main():
    print("AP1 — GeoNames Basispools (Pareto)")
    print("=" * 40)

    if Path(DB_PATH).exists():
        print(f"Bestehende DB gefunden: {DB_PATH}")
        ans = input("Neu aufbauen? [j/N] ").strip().lower()
        if ans != 'j':
            print("Abgebrochen.")
            con = sqlite3.connect(DB_PATH)
            validate(con)
            return

    print(f"\nBaue {DB_PATH} auf...")
    Path(DB_PATH).unlink(missing_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA journal_mode=WAL")

    print("\n1. Schema erstellen")
    create_schema(con)

    print("\n2. Staat laden")
    load_staat(con)

    print("\n3. Bundesland laden")
    load_bundesland(con)

    print("\n4. Kreis laden")
    load_kreis(con)

    print("\n5. Stadt laden (dauert ~1-2 Min)")
    load_stadt(con)

    print("\n5b. Deutsche Alternativnamen laden (Muenchen statt Munich etc.)")
    load_alternatenamen_de(con)

    print("\n5c. AP2: PLZ laden")
    load_plz(con)

    print("\n6a. AP3: KFZ-Kennzeichen laden")
    load_kfz_kennzeichen(con)

    print("\n6b. AP4: Schablonen-Tabelle befuellen")
    load_schablonen_de(con)

    print("\n7. Validierung")
    ok = validate(con)

    con.close()
    size_mb = Path(DB_PATH).stat().st_size / 1024 / 1024
    print(f"\nFertig: {DB_PATH} ({size_mb:.1f} MB)")
    if ok:
        print("✓ Alle Checks bestanden — AP1 abgeschlossen")
    else:
        print("✗ Einige Checks fehlgeschlagen — Logs prüfen")

if __name__ == '__main__':
    main()
