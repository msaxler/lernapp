#!/usr/bin/env python3
"""
extract_gtfs_strecken.py
========================
Liest ICE/IC/EC-Strecken aus einer GTFS-ZIP-Datei (z.B. latest.zip von gtfs.de)
und aktualisiert den ice_strecken-Block in bahnhof.json.

Quelle: https://gtfs.de  (DELFI e.V., kostenlos, offiziell)
Download: latest.zip -> direkt in LernApp-Ordner legen

Aufruf:
  python extract_gtfs_strecken.py                        # sucht latest.zip im selben Ordner
  python extract_gtfs_strecken.py --gtfs meine.zip       # andere ZIP-Datei
  python extract_gtfs_strecken.py --dry-run              # nur anzeigen, nicht speichern

Ergebnis: bahnhof.json wird aktualisiert (ice_strecken-Block).
"""

import csv, json, os, sys, argparse, zipfile, io
from collections import defaultdict

STAEDTE_F = os.path.join(os.path.dirname(__file__), "staedte.json")
BAHNHOF_F = os.path.join(os.path.dirname(__file__), "bahnhof.json")
GTFS_F    = os.path.join(os.path.dirname(__file__), "latest.zip")

# Welche Zuggattungen kommen in den Pool?
GATTUNGEN = {'ICE', 'IC', 'EC', 'ECE', 'RJ'}  # RJ = Railjet (Österreich, fährt nach Deutschland)

def lade_gtfs_datei(zf, name):
    """Liest eine CSV-Datei aus der ZIP."""
    with zf.open(name) as f:
        return list(csv.DictReader(io.TextIOWrapper(f, encoding='utf-8-sig')))

def normalisiere_stadtname(stop_name, stadtnames):
    """
    Prüft ob ein Haltepunkt zu einer unserer Städte gehört.
    Gibt Stadtname zurück oder None.
    """
    for stadt in stadtnames:
        # "Berlin Hbf", "Berlin Hauptbahnhof", "Berlin Hbf (tief)"
        if stop_name == stadt:
            return stadt
        if stop_name.startswith(stadt + ' ') or stop_name.startswith(stadt + ','):
            teil = stop_name[len(stadt):].strip().lstrip(',').strip()
            if any(kw in teil for kw in ('Hbf', 'Hauptbahnhof', 'Hbf.', 'Pbf')):
                return stadt
            # Manche Städte haben nur "Stadtname Fernbf" o.ä.
            if teil == '' or teil.startswith('('):
                return stadt
    return None

def main():
    parser = argparse.ArgumentParser(description='GTFS-Strecken nach bahnhof.json extrahieren')
    parser.add_argument('--gtfs',    default=GTFS_F, help='Pfad zur GTFS-ZIP')
    parser.add_argument('--dry-run', action='store_true', help='Nicht speichern')
    parser.add_argument('--staedte', default=STAEDTE_F)
    parser.add_argument('--bahnhof', default=BAHNHOF_F)
    args = parser.parse_args()

    if not os.path.exists(args.gtfs):
        print(f"❌  GTFS-Datei nicht gefunden: {args.gtfs}")
        print(f"    Bitte latest.zip von https://gtfs.de herunterladen")
        print(f"    und in den LernApp-Ordner legen.")
        sys.exit(1)

    print(f"📂  Lese GTFS: {args.gtfs}")

    with open(args.staedte, encoding='utf-8') as f:
        staedte = json.load(f)
    stadtnames = [s['name'] for s in staedte]

    if os.path.exists(args.bahnhof):
        with open(args.bahnhof, encoding='utf-8') as f:
            bahnhof = json.load(f)
    else:
        bahnhof = {"bahnhof_kategorien": {}, "ice_strecken": {}, "kontraintuitive_fakten": []}

    with zipfile.ZipFile(args.gtfs) as zf:
        print("    routes.txt ...")
        routes    = lade_gtfs_datei(zf, 'routes.txt')
        print("    trips.txt ...")
        trips     = lade_gtfs_datei(zf, 'trips.txt')
        print("    stops.txt ...")
        stops_raw = lade_gtfs_datei(zf, 'stops.txt')
        print("    stop_times.txt ...")
        stop_times = lade_gtfs_datei(zf, 'stop_times.txt')

    # Stop-ID → Name
    stop_map = {s['stop_id']: s['stop_name'] for s in stops_raw}

    # Route-ID → Gattung + Linienname
    route_info = {}
    for r in routes:
        kurz = r['route_short_name'].strip()
        gattung = kurz.split()[0] if kurz else ''
        if gattung in GATTUNGEN:
            route_info[r['route_id']] = {
                'linie': kurz,
                'gattung': gattung
            }

    # Trip-ID → Route-ID (nur erster Trip pro Route reicht)
    trip_route = {}
    route_trip = {}  # route_id → erster trip_id
    for t in trips:
        rid = t['route_id']
        tid = t['trip_id']
        trip_route[tid] = rid
        if rid not in route_trip:
            route_trip[rid] = tid

    # Stop-Times gruppiert nach Trip
    trip_stops = defaultdict(list)
    for st in stop_times:
        tid = st['trip_id']
        if trip_route.get(tid) in route_info:  # nur relevante Trips
            trip_stops[tid].append((
                int(st['stop_sequence']),
                st['stop_id'],
                st.get('departure_time', '')
            ))

    print(f"\n🔍  Verarbeite {len(route_info)} ICE/IC/EC-Linien ...\n")

    neue_strecken = {}

    for rid, info in sorted(route_info.items(), key=lambda x: x[1]['linie']):
        tid = route_trip.get(rid)
        if not tid or tid not in trip_stops:
            continue

        halte = sorted(trip_stops[tid], key=lambda x: x[0])
        alle_namen = [stop_map.get(h[1], '') for h in halte]
        alle_zeiten = [h[2] for h in halte]

        # Quiz-Halte: unsere Städte auf dieser Strecke
        quiz_halte = []
        quiz_zeiten = []
        for i, name in enumerate(alle_namen):
            stadt = normalisiere_stadtname(name, stadtnames)
            if stadt and stadt not in quiz_halte:
                quiz_halte.append(stadt)
                quiz_zeiten.append(alle_zeiten[i])

        if len(quiz_halte) < 2:
            continue

        # Schlüssel: "Hamburg–München" o.ä.
        key = f"{quiz_halte[0]}–{quiz_halte[-1]}"

        # Duplikat: nur behalten wenn mehr Quiz-Halte
        if key in neue_strecken:
            if len(quiz_halte) <= len(neue_strecken[key]['halte_quiz']):
                continue

        neue_strecken[key] = {
            'halte':       alle_namen,
            'halte_quiz':  quiz_halte,
            'halte_zeiten': quiz_zeiten,
            'zuggattung':  info['gattung'],
            'linie':       info['linie'],
            'beschreibung': f"{info['linie']}: {quiz_halte[0]} → {quiz_halte[-1]}"
        }

        print(f"  {info['linie']:12s}  {' → '.join(quiz_halte)}")

    print(f"\n📊  Ergebnis: {len(neue_strecken)} Strecken\n")

    if args.dry_run:
        print("⚠️   --dry-run: bahnhof.json wird NICHT aktualisiert.")
        return

    # Bestehende Strecken behalten, neue ergänzen/überschreiben
    alt = bahnhof.get('ice_strecken', {})
    alt.update(neue_strecken)
    bahnhof['ice_strecken'] = alt

    with open(args.bahnhof, 'w', encoding='utf-8') as f:
        json.dump(bahnhof, f, ensure_ascii=False, indent=2)

    print(f"✅  bahnhof.json aktualisiert — {len(alt)} Strecken gesamt")
    print(f"   ({len(neue_strecken)} aus GTFS, {len(alt)-len(neue_strecken)} handgepflegt behalten)\n")
    print("Nächste Schritte:")
    print("  python generate_questions.py")
    print("  python inject_questions.py")

if __name__ == '__main__':
    main()
