"""
Quiz Away — Wikidata-Abfrage: Stadtgeschichte
==============================================
Holt Gründungsjahre und erste urkundliche Erwähnungen
für alle Städte in staedte.json via Wikidata SPARQL.

Aufruf:
  python fetch_wikidata.py
  python fetch_wikidata.py --staedte staedte.json --out geschichte.json

Benötigt Internetverbindung (einmalig).
Ergebnis wird lokal in geschichte.json gespeichert.
"""

import json, time, argparse
import urllib.request, urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument("--staedte", default="staedte.json")
parser.add_argument("--out",     default="geschichte.json")
args = parser.parse_args()

with open(args.staedte, encoding="utf-8") as f:
    staedte = json.load(f)

SPARQL_URL = "https://query.wikidata.org/sparql"
HEADERS = {
    "User-Agent": "QuizAwayBot/1.0 (educational project)",
    "Accept": "application/sparql-results+json"
}

def sparql_query(query):
    """Führt eine SPARQL-Abfrage gegen Wikidata aus."""
    params = urllib.parse.urlencode({"query": query, "format": "json"})
    url = f"{SPARQL_URL}?{params}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def hole_stadtdaten(stadtname):
    """
    Sucht eine deutsche Stadt in Wikidata und holt:
    - Gründungsjahr (P571)
    - Erste urkundliche Erwähnung (P1249 oder P571 als Fallback)
    - Wikidata-ID
    """
    query = f"""
    SELECT ?item ?gruendung ?erwaehnung WHERE {{
      ?item wdt:P31/wdt:P279* wd:Q515 .        # ist eine Stadt
      ?item wdt:P17 wd:Q183 .                   # in Deutschland
      ?item rdfs:label "{stadtname}"@de .        # deutscher Name
      OPTIONAL {{ ?item wdt:P571 ?gruendung. }}  # Gründungsdatum
      OPTIONAL {{ ?item wdt:P1249 ?erwaehnung. }} # erste Erwähnung
    }}
    LIMIT 3
    """
    try:
        result = sparql_query(query)
        bindings = result["results"]["bindings"]
        if not bindings:
            return None

        row = bindings[0]
        wikidata_id = row["item"]["value"].split("/")[-1]

        gruendung = None
        if "gruendung" in row:
            val = row["gruendung"]["value"]
            # Format: +1200-01-01T00:00:00Z → 1200
            if val.startswith("+"):
                val = val[1:]
            try:
                gruendung = int(val[:4])
                if gruendung < 0:
                    gruendung = None  # v.Chr. überspringen
            except ValueError:
                pass

        erwaehnung = None
        if "erwaehnung" in row:
            val = row["erwaehnung"]["value"]
            if val.startswith("+"):
                val = val[1:]
            try:
                erwaehnung = int(val[:4])
                if erwaehnung < 0:
                    erwaehnung = None
            except ValueError:
                pass

        # Fallback: Gründung als Erwähnung nutzen
        jahr = erwaehnung or gruendung

        return {
            "wikidata_id": wikidata_id,
            "gruendung": gruendung,
            "erste_erwaehnung": erwaehnung,
            "jahr": jahr  # bestes verfügbares Jahr
        }

    except Exception as e:
        return {"fehler": str(e)}

# ── Alle Städte abfragen ───────────────────────────────────────────────────
print(f"Frage {len(staedte)} Städte bei Wikidata ab...\n")

ergebnisse = {}
fehler = []

for i, stadt in enumerate(staedte):
    name = stadt["name"]
    print(f"  [{i+1:2d}/{len(staedte)}] {name} ...", end=" ", flush=True)

    daten = hole_stadtdaten(name)

    if daten is None:
        print("nicht gefunden")
        fehler.append(name)
        ergebnisse[name] = {"jahr": None}
    elif "fehler" in daten:
        print(f"Fehler: {daten['fehler']}")
        fehler.append(name)
        ergebnisse[name] = {"jahr": None}
    else:
        jahr = daten.get("jahr")
        print(f"✅  Jahr: {jahr}" if jahr else "⚠️  kein Jahr")
        ergebnisse[name] = daten

    # Wikidata-Ratenlimit respektieren
    time.sleep(0.5)

# ── Speichern ──────────────────────────────────────────────────────────────
with open(args.out, "w", encoding="utf-8") as f:
    json.dump(ergebnisse, f, ensure_ascii=False, indent=2)

# ── Zusammenfassung ────────────────────────────────────────────────────────
mit_jahr   = sum(1 for d in ergebnisse.values() if d.get("jahr"))
ohne_jahr  = len(ergebnisse) - mit_jahr

print(f"\n✅  {args.out} gespeichert")
print(f"   Mit Jahr:  {mit_jahr}")
print(f"   Ohne Jahr: {ohne_jahr}")
if fehler:
    print(f"\n⚠️  Nicht gefunden: {', '.join(fehler)}")
print("\nNächster Schritt: python generate_questions.py")
