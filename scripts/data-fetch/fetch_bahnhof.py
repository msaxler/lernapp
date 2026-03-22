"""
Quiz Away — DB OpenData: Bahnhofskategorien
============================================
Holt Bahnhofskategorien (1–7) für alle Städte in staedte.json
vom DB OpenData Portal (data.deutschebahn.com).

DB-Kategorien:
  1 — Großstadtbahnhöfe / Knotenbahnhöfe (Frankfurt Hbf, Berlin Hbf)
  2 — Fernverkehrsbahnhöfe (Kassel-Wilhelmshöhe, Mannheim Hbf)
  3 — Mittelzentren mit Fernverkehr (Fulda, Montabaur)
  4 — Regionalbahnhöfe mit hohem Aufkommen
  5 — Normalbahnhöfe
  6 — Kleine Bahnhöfe
  7 — Kleinste Haltepunkte

Aufruf:
  python fetch_bahnhof.py
  python fetch_bahnhof.py --staedte staedte.json --out bahnhof.json

Benötigt Internetverbindung (einmalig).
"""

import json, time, argparse, urllib.request, urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument("--staedte", default="staedte.json")
parser.add_argument("--out",     default="bahnhof.json")
args = parser.parse_args()

with open(args.staedte, encoding="utf-8") as f:
    staedte = json.load(f)

# DB StaDa API (Stationsdaten)
# Dokumentation: https://data.deutschebahn.com/dataset/data-stationsdaten
STADA_URL = "https://apis.deutschebahn.com/db-api-marketplace/apis/station-data/v2/stations"

# Fallback: DB OpenData CSV (kein API-Key nötig)
# https://data.deutschebahn.com/dataset/data-stationsdaten
CSV_URL = "https://download-data.deutschebahn.com/static/datasets/stationsdaten/DBSuS-Uebersicht_Bahnhoefe-Stand2023-03.csv"

def hole_via_csv():
    """Lädt das vollständige Bahnhofsverzeichnis als CSV (kein API-Key nötig)."""
    print("Lade DB Bahnhofsverzeichnis (CSV)...")
    import ssl
    # SSL-Kontext: DB-Downloadserver hat Zertifikatsproblem mit Hostname-Mismatch
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        CSV_URL,
        headers={"User-Agent": "QuizAwayBot/1.0 (educational project)"}
    )
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        raw = resp.read().decode("latin-1")
    
    zeilen = raw.strip().split("\n")
    header = zeilen[0].split(";")
    print(f"  Spalten: {header[:8]}")
    
    # Bahnhöfe parsen
    bahnhoefe = []
    for zeile in zeilen[1:]:
        felder = zeile.split(";")
        if len(felder) < 5:
            continue
        bahnhoefe.append(felder)
    
    print(f"  {len(bahnhoefe)} Bahnhöfe geladen")
    return header, bahnhoefe

def suche_bahnhof(stadtname, header, bahnhoefe):
    """
    Sucht den wichtigsten Bahnhof einer Stadt im DB-Verzeichnis.
    Gibt Kategorie und Bahnhofsname zurück.
    """
    # Spaltenindizes ermitteln
    try:
        idx_name = header.index("Bahnhof") if "Bahnhof" in header else 1
        idx_kat  = header.index("Kat") if "Kat" in header else 3
    except ValueError:
        # Fallback: typische Spaltenposition
        idx_name, idx_kat = 1, 3

    treffer = []
    stadtname_lower = stadtname.lower()
    
    for felder in bahnhoefe:
        if len(felder) <= max(idx_name, idx_kat):
            continue
        name = felder[idx_name].strip().lower()
        # Matching: Stadtname im Bahnhofsnamen
        if stadtname_lower in name or name.startswith(stadtname_lower[:6].lower()):
            try:
                kat = int(felder[idx_kat].strip())
                treffer.append((kat, felder[idx_name].strip()))
            except (ValueError, IndexError):
                pass
    
    if not treffer:
        return None, None
    
    # Bester Treffer: niedrigste Kategorie (= größter Bahnhof)
    treffer.sort(key=lambda x: x[0])
    return treffer[0]

# ── Hauptprogramm ──────────────────────────────────────────────────────────
print(f"Suche Bahnhofsdaten für {len(staedte)} Städte...\n")

try:
    header, bahnhoefe = hole_via_csv()
except Exception as e:
    print(f"❌ CSV-Download fehlgeschlagen: {e}")
    print("   Bitte manuell herunterladen von:")
    print("   https://data.deutschebahn.com/dataset/data-stationsdaten")
    exit(1)

ergebnisse = {}
nicht_gefunden = []

for i, stadt in enumerate(staedte):
    name = stadt["name"]
    kat, bahnhof_name = suche_bahnhof(name, header, bahnhoefe)
    
    if kat:
        ergebnisse[name] = {
            "kategorie": kat,
            "bahnhof_name": bahnhof_name,
            "fernverkehr": kat <= 2,
            "ice_halt": kat <= 3,
        }
        status = f"Kat {kat} — {bahnhof_name}"
    else:
        ergebnisse[name] = {"kategorie": None}
        nicht_gefunden.append(name)
        status = "nicht gefunden"
    
    print(f"  [{i+1:2d}/{len(staedte)}] {name:25s} {status}")

# ── Speichern ──────────────────────────────────────────────────────────────
with open(args.out, "w", encoding="utf-8") as f:
    json.dump(ergebnisse, f, ensure_ascii=False, indent=2)

# ── Statistik ──────────────────────────────────────────────────────────────
mit_kat = sum(1 for d in ergebnisse.values() if d.get("kategorie"))
kat_counts = {}
for d in ergebnisse.values():
    k = d.get("kategorie")
    if k:
        kat_counts[k] = kat_counts.get(k, 0) + 1

print(f"\n✅  {args.out} gespeichert")
print(f"   Gefunden:      {mit_kat}/{len(staedte)}")
print(f"   Nicht gefunden: {len(nicht_gefunden)}")
if nicht_gefunden:
    print(f"   → {', '.join(nicht_gefunden)}")
print()
for k in sorted(kat_counts):
    label = ["","Knotenbahnhof","Fernverkehr","Fernverkehr (klein)","Regional","Normal","Klein","Kleinst"][k]
    print(f"   Kat {k} ({label:20s}): {kat_counts[k]} Städte")
print("\nNächster Schritt: python generate_questions.py")
