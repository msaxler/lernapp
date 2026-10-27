"""Vertiefung Freiburg (Mike 2026-10-27): Grenzen der Freiburger Stadtteile als GeoJSON über Nominatim (Overpass fiel am
27.10. aus). Stadtteile der Kernstadt sind in OSM admin_level 10, eingemeindete Ortschaften 9, Stadtbezirke 11.
Je Ort die Relation, deren Name dem Ortsnamen gleicht und deren Stufe 9 oder 10 ist; Dietenbach hat keine (Neubaugebiet).
Schreibt data/gemeinde-achsen/freiburg-vertiefung/grenzen/<slug>.geojson
Aufruf:  python -X utf8 scripts/data-fetch/freiburg_stadtteil_grenzen.py
"""
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAUM = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn')
AUS = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'freiburg-vertiefung', 'grenzen')
UA = {'User-Agent': 'QuizAway-Recherche (msaxler@gmail.com)'}
NOM = 'https://nominatim.openstreetmap.org/'


def holen(pfad):
    time.sleep(1.2)
    with urllib.request.urlopen(urllib.request.Request(NOM + pfad, headers=UA), timeout=60) as r:
        return json.loads(r.read().decode('utf-8'))


def stadtteile():
    with io.open(os.path.join(RAUM, 'orte.json'), encoding='utf-8') as f:
        return [(o[0], o[2]) for o in json.load(f)['orte'] if o[4] == 'Ortsteil von Freiburg im Breisgau']


def main():
    os.makedirs(AUS, exist_ok=True)
    for slug, name in stadtteile():
        ziel = os.path.join(AUS, slug + '.geojson')
        if os.path.exists(ziel):
            continue
        treffer = holen('search?' + urllib.parse.urlencode({'q': name + ', Freiburg im Breisgau', 'format': 'jsonv2',
                                                             'extratags': 1, 'limit': 10}))
        rel = [t for t in treffer if t.get('osm_type') == 'relation' and t.get('type') == 'administrative' and t['name'] == name
               and (t.get('extratags') or {}).get('admin_level') in ('9', '10')]
        if not rel:
            print('%-24s keine Grenze' % slug, flush=True)
            continue
        r = rel[0]
        g = holen('lookup?' + urllib.parse.urlencode({'osm_ids': 'R%d' % r['osm_id'], 'format': 'geojson', 'polygon_geojson': 1}))
        with io.open(ziel, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(g, f, ensure_ascii=False)
        print('%-24s R%d admin %s' % (slug, r['osm_id'], r['extratags']['admin_level']), flush=True)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
