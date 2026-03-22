"""
fetch_flaeche.py — Holt Fläche (km²) für alle Städte in staedte.json
======================================================================
Quelle: Wikidata SPARQL (P2046 = Fläche)
Schreibt die Fläche direkt in staedte.json zurück.

Aufruf:
  python fetch_flaeche.py
  python fetch_flaeche.py --dry-run    (nur anzeigen, nicht speichern)

Benötigt Internetverbindung (einmalig, ~5 Minuten für 210 Städte).
"""

import json, time, argparse, urllib.request, urllib.parse, os, shutil

parser = argparse.ArgumentParser()
parser.add_argument('--staedte', default='staedte.json')
parser.add_argument('--dry-run', action='store_true')
args = parser.parse_args()

SPARQL_URL = 'https://query.wikidata.org/sparql'
HEADERS = {
    'User-Agent': 'QuizAwayBot/1.0 (fetch_flaeche educational project)',
    'Accept': 'application/sparql-results+json'
}

with open(args.staedte, encoding='utf-8') as f:
    staedte = json.load(f)

fehlend = [s for s in staedte if not s.get('flaeche')]
print(f'Städte ohne Fläche: {len(fehlend)}/{len(staedte)}')
print(f'Frage Wikidata ab...\n')

def hole_flaeche(stadtname):
    query = f"""
SELECT ?flaeche WHERE {{
  ?item wdt:P31/wdt:P279* wd:Q515 .
  ?item wdt:P17 wd:Q183 .
  ?item rdfs:label "{stadtname}"@de .
  ?item wdt:P2046 ?flaeche .
}}
LIMIT 1
"""
    params = urllib.parse.urlencode({'query': query, 'format': 'json'})
    req = urllib.request.Request(f'{SPARQL_URL}?{params}', headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode('utf-8'))
        bindings = data['results']['bindings']
        if bindings:
            return round(float(bindings[0]['flaeche']['value']), 1)
        return None
    except Exception as e:
        return f'ERR:{e}'

# Index für schnellen Zugriff
stadt_map = {s['name']: s for s in staedte}
gefunden = fehler = 0

for i, s in enumerate(fehlend):
    name = s['name']
    print(f'  [{i+1:3d}/{len(fehlend)}] {name:<35}', end=' ', flush=True)
    result = hole_flaeche(name)
    if isinstance(result, float) and result > 0:
        stadt_map[name]['flaeche'] = result
        print(f'✅  {result} km²')
        gefunden += 1
    elif isinstance(result, str) and result.startswith('ERR'):
        print(f'⚠️  {result}')
        fehler += 1
    else:
        print('— nicht gefunden')
        fehler += 1
    time.sleep(0.6)

print(f'\n📊  Ergebnis: {gefunden} Flächen gefunden, {fehler} nicht gefunden')

# Stichprobe
noch_leer = [s['name'] for s in staedte if not s.get('flaeche')]
if noch_leer:
    print(f'⚠️  Noch ohne Fläche ({len(noch_leer)}): {", ".join(noch_leer[:10])}')

if args.dry_run:
    print('\n⚠️  --dry-run: staedte.json nicht aktualisiert.')
else:
    backup = args.staedte.replace('.json', '_backup_flaeche.json')
    shutil.copy2(args.staedte, backup)
    print(f'💾  Backup: {backup}')
    with open(args.staedte, 'w', encoding='utf-8') as f:
        json.dump(staedte, f, ensure_ascii=False, indent=2)
    print(f'✅  {args.staedte} aktualisiert')
    print('\nNächste Schritte:\n  python generate_questions.py\n  python inject_questions.py')
