#!/usr/bin/env python3
"""
fetch_ice_strecken.py
=====================
Lädt ICE / IC / EC Strecken von der DB REST API (v6.db.transport.rest)
und ergänzt/aktualisiert den ice_strecken-Block in bahnhof.json.

Voraussetzung:
  pip install requests

Aufruf:
  python fetch_ice_strecken.py
  python fetch_ice_strecken.py --dry-run     # nur anzeigen, nicht speichern
  python fetch_ice_strecken.py --max 30      # max. 30 Verbindungen pro Strecke

Ergebnis: bahnhof.json wird aktualisiert (ice_strecken-Block).
"""

import json, time, argparse, sys, os, re
from datetime import datetime, timedelta
from collections import defaultdict

try:
    import requests
except ImportError:
    print("❌  'requests' fehlt — bitte installieren:")
    print("    pip install requests")
    sys.exit(1)

# ── Konfiguration ──────────────────────────────────────────────────────────
API_BASE   = "https://v6.db.transport.rest"  # Fallback: v5.db.transport.rest oder dbf.finalreboot.net

API_KANDIDATEN = [
    "https://v6.db.transport.rest",
    "https://v5.db.transport.rest",
    "https://dbf.finalreboot.net",
]

def finde_api_base():
    """Probiert API-Endpunkte durch und nimmt den ersten erreichbaren."""
    import requests as _req
    for basis in API_KANDIDATEN:
        try:
            r = _req.get(f"{basis}/stops/search",
                         params={"query": "Berlin Hbf", "results": 1},
                         timeout=8)
            if r.status_code == 200 and r.json():
                print(f"✅  API erreichbar: {basis}")
                return basis
        except Exception:
            print(f"   ⚠️  {basis} — nicht erreichbar")
    return None
STAEDTE_F  = os.path.join(os.path.dirname(__file__), "staedte.json")
BAHNHOF_F  = os.path.join(os.path.dirname(__file__), "bahnhof.json")
ZUGGATTUNGEN = {"nationalExpress", "national"}  # ICE=nationalExpress, IC/EC=national
PAUSE_SEK  = 0.8   # Pause zwischen API-Calls (Rate-Limit vermeiden)

# Städtepaare: Start → Ziel (repräsentative Fernverkehrsverbindungen)
# Abdeckt alle Himmelsrichtungen und möglichst viele der 51 Städte
VERBINDUNGEN = [
    # Nord–Süd
    ("Hamburg",         "München"),
    ("Hamburg",         "Stuttgart"),
    ("Hamburg",         "Frankfurt am Main"),
    ("Kiel",            "München"),
    ("Flensburg",       "München"),
    ("Bremen",          "München"),
    ("Rostock",         "München"),
    # West–Ost
    ("Köln",            "Berlin"),
    ("Köln",            "Dresden"),
    ("Düsseldorf",      "Berlin"),
    ("Dortmund",        "Berlin"),
    ("Aachen",          "Berlin"),
    # Diagonal
    ("Hamburg",         "Wien"),
    ("Berlin",          "München"),
    ("Berlin",          "Frankfurt am Main"),
    ("Berlin",          "Stuttgart"),
    ("Berlin",          "Köln"),
    ("Hamburg",         "Zürich"),
    ("Köln",            "München"),
    ("Frankfurt am Main","Berlin"),
    ("Frankfurt am Main","Hamburg"),
    ("Frankfurt am Main","Dresden"),
    ("Frankfurt am Main","Stuttgart"),
    ("Nürnberg",        "Hamburg"),
    ("München",         "Köln"),
    ("München",         "Hamburg"),
    ("Stuttgart",       "Berlin"),
    ("Stuttgart",       "Hamburg"),
    # Regionale Verbindungen (IC/EC)
    ("Rostock",         "Stuttgart"),
    ("Stralsund",       "München"),
    ("Kiel",            "Frankfurt am Main"),
    ("Bremen",          "Stuttgart"),
    ("Hannover",        "Stuttgart"),
    ("Hannover",        "München"),
    ("Leipzig",         "Köln"),
    ("Dresden",         "Frankfurt am Main"),
    ("Dresden",         "Köln"),
    ("Erfurt",          "Frankfurt am Main"),
    ("Kassel",          "München"),
    ("Würzburg",        "Hamburg"),
    ("Augsburg",        "Hamburg"),
    ("Freiburg im Breisgau", "Hamburg"),
    ("Karlsruhe",       "Hamburg"),
    ("Mannheim",        "Hamburg"),
    ("Saarbrücken",     "Berlin"),
    ("Trier",           "Frankfurt am Main"),
    ("Wiesbaden",       "Hamburg"),
    ("Mainz",           "Hamburg"),
    ("Regensburg",      "Hamburg"),
    ("Passau",          "Hamburg"),
]


def lade_staedte():
    with open(STAEDTE_F, encoding="utf-8") as f:
        staedte = json.load(f)
    # Name → Objekt
    return {s["name"]: s for s in staedte}


def lade_bahnhof():
    if os.path.exists(BAHNHOF_F):
        with open(BAHNHOF_F, encoding="utf-8") as f:
            return json.load(f)
    return {"bahnhof_kategorien": {}, "ice_strecken": {}, "kontraintuitive_fakten": []}


def normalisiere_name(name):
    """Vereinfacht Bahnhofs-Namen für den Vergleich mit staedte.json."""
    name = name.strip()
    # Klammern entfernen: "Frankfurt (Main) Hbf" → "Frankfurt am Main"
    name = re.sub(r"\s*\(Main\)", " am Main", name)
    name = re.sub(r"\s*Hbf$", "", name)
    name = re.sub(r"\s*Hauptbahnhof$", "", name)
    name = re.sub(r"\s*\(.*?\)", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def finde_station_id(stadtname, session):
    """Sucht die HAFAS-ID für einen Stadtnamen."""
    try:
        r = session.get(f"{API_BASE}/stops/search",
                        params={"query": stadtname + " Hbf", "results": 3},
                        timeout=10)
        r.raise_for_status()
        stops = r.json()
        for stop in stops:
            norm = normalisiere_name(stop.get("name", ""))
            if stadtname.lower() in norm.lower() or norm.lower() in stadtname.lower():
                return stop["id"], stop["name"]
        # Fallback: ersten nehmen
        if stops:
            return stops[0]["id"], stops[0]["name"]
    except Exception as e:
        print(f"    ⚠️  Suche fehlgeschlagen für '{stadtname}': {e}")
    return None, None


def hole_verbindungen(start_id, ziel_id, session, max_results=5):
    """Holt Verbindungen von Start nach Ziel (nur ICE/IC/EC)."""
    abfahrt = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    if abfahrt < datetime.now():
        abfahrt += timedelta(days=1)

    try:
        r = session.get(f"{API_BASE}/journeys",
                        params={
                            "from":    start_id,
                            "to":      ziel_id,
                            "results": max_results,
                            "departure": abfahrt.isoformat(),
                            "nationalExpress": "true",
                            "national": "true",
                            "regional": "false",
                            "suburban": "false",
                            "bus":      "false",
                            "ferry":    "false",
                            "subway":   "false",
                            "tram":     "false",
                            "taxi":     "false",
                            "transfers": 0,  # nur Direktverbindungen
                        },
                        timeout=15)
        r.raise_for_status()
        return r.json().get("journeys", [])
    except Exception as e:
        print(f"    ⚠️  Verbindungs-Abfrage fehlgeschlagen: {e}")
        return []


def extrahiere_halte(journey, stadtname_set):
    """
    Extrahiert Halte aus einer Journey die in staedte.json vorkommen.
    Gibt zurück: (zuggattung, zugnr, halte_alle, halte_quiz)
    halte_alle  = alle Halte des Zugs (Originalnamen)
    halte_quiz  = nur Halte die in staedte.json sind (normalisierte Namen)
    """
    legs = journey.get("legs", [])
    # Nur Direktverbindungen (1 Leg)
    if len(legs) != 1:
        return None

    leg = legs[0]
    produkt = leg.get("line", {})
    gattung = produkt.get("productName", "")
    zugnr   = produkt.get("name", "")

    # Nur ICE/IC/EC
    if produkt.get("product") not in ZUGGATTUNGEN:
        return None

    stopovers = leg.get("stopovers", [])
    if not stopovers:
        return None

    halte_alle  = []
    halte_quiz  = []

    for stop in stopovers:
        roh_name = stop.get("stop", {}).get("name", "")
        norm     = normalisiere_name(roh_name)

        halte_alle.append(roh_name)

        # In staedte.json vorhanden?
        for stadtname in stadtname_set:
            if (stadtname.lower() == norm.lower()
                    or stadtname.lower() in norm.lower()
                    or norm.lower() in stadtname.lower()):
                halte_quiz.append(stadtname)
                break

    return gattung, zugnr, halte_alle, halte_quiz


def strecken_key(halte_quiz):
    """Erzeugt einen eindeutigen Schlüssel für eine Strecke."""
    if not halte_quiz:
        return None
    return f"{halte_quiz[0]}–{halte_quiz[-1]}"


def main():
    parser = argparse.ArgumentParser(description="Lade ICE/IC/EC Strecken von DB REST API")
    parser.add_argument("--dry-run", action="store_true", help="Nicht speichern")
    parser.add_argument("--max",     type=int, default=5,  help="Max Verbindungen pro Strecke")
    parser.add_argument("--staedte", default=STAEDTE_F)
    parser.add_argument("--bahnhof", default=BAHNHOF_F)
    args = parser.parse_args()

    STAEDTE  = lade_staedte()
    BAHNHOF  = lade_bahnhof()
    stadtname_set = set(STAEDTE.keys())

    # API-Endpunkt automatisch ermitteln
    global API_BASE
    gefundene_basis = finde_api_base()
    if not gefundene_basis:
        print("\n❌  Kein API-Endpunkt erreichbar.")
        print("    Mögliche Ursachen:")
        print("    - Kein Internet / Firewall blockiert")
        print("    - Alle bekannten Endpunkte down")
        print("    Bitte später nochmal versuchen.")
        sys.exit(1)
    API_BASE = gefundene_basis

    session = requests.Session()
    session.headers.update({"User-Agent": "QuizAway/1.0 (Prototyp, nicht kommerziell)"})

    neue_strecken = {}   # key → {halte, halte_quiz, zuggattung, beschreibung}
    station_cache = {}   # stadtname → (id, api_name)

    print(f"\n🚂  Starte Strecken-Download ({len(VERBINDUNGEN)} Verbindungen)\n")

    for start_name, ziel_name in VERBINDUNGEN:
        print(f"  {start_name} → {ziel_name} ", end="", flush=True)

        # Station-IDs cachen
        for name in (start_name, ziel_name):
            if name not in station_cache:
                sid, sname = finde_station_id(name, session)
                station_cache[name] = (sid, sname)
                time.sleep(PAUSE_SEK)

        start_id, _ = station_cache[start_name]
        ziel_id,  _ = station_cache[ziel_name]

        if not start_id or not ziel_id:
            print("❌ Station nicht gefunden")
            continue

        journeys = hole_verbindungen(start_id, ziel_id, session, args.max)
        time.sleep(PAUSE_SEK)

        gefunden = 0
        for journey in journeys:
            result = extrahiere_halte(journey, stadtname_set)
            if not result:
                continue
            gattung, zugnr, halte_alle, halte_quiz = result

            if len(halte_quiz) < 3:
                continue  # zu wenige Quiz-relevante Halte

            key = strecken_key(halte_quiz)
            if not key:
                continue

            # Duplikat: nur aufnehmen wenn mehr halte_quiz als bisherige Version
            if key in neue_strecken:
                if len(halte_quiz) <= len(neue_strecken[key]["halte_quiz"]):
                    continue

            neue_strecken[key] = {
                "halte":       halte_alle,
                "halte_quiz":  halte_quiz,
                "zuggattung":  gattung,
                "zugnr":       zugnr,
                "beschreibung": f"{gattung} {start_name}–{ziel_name}",
            }
            gefunden += 1

        if gefunden:
            print(f"✅ {gefunden} Strecke(n)")
        else:
            print("⚠️  keine Direktverbindung")

    # ── Zusammenfassung ────────────────────────────────────────────────────
    print(f"\n📊  Ergebnis: {len(neue_strecken)} eindeutige Strecken\n")
    for key, s in sorted(neue_strecken.items()):
        print(f"  {s['zuggattung']:3s}  {key}")
        print(f"       Halte gesamt: {len(s['halte'])}  Quiz-Halte: {s['halte_quiz']}")

    if args.dry_run:
        print("\n⚠️  --dry-run: bahnhof.json wird NICHT aktualisiert.")
        return

    # ── Speichern ──────────────────────────────────────────────────────────
    # Bestehende handgepflegte Strecken behalten, neue ergänzen/überschreiben
    alt_strecken = BAHNHOF.get("ice_strecken", {})
    alt_strecken.update(neue_strecken)
    BAHNHOF["ice_strecken"] = alt_strecken

    with open(args.bahnhof, "w", encoding="utf-8") as f:
        json.dump(BAHNHOF, f, ensure_ascii=False, indent=2)

    print(f"\n✅  bahnhof.json aktualisiert — {len(alt_strecken)} Strecken gesamt")
    print(f"   (davon {len(neue_strecken)} neu/aktualisiert, "
          f"{len(alt_strecken) - len(neue_strecken)} handgepflegt behalten)\n")
    print("Nächster Schritt:")
    print("  python generate_questions.py")
    print("  python inject_questions.py")


if __name__ == "__main__":
    main()
