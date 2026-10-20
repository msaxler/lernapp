"""Gemeinde-Achsen Ortsporträt: Zeugenliste je Ort aus OpenStreetMap (Overpass), ohne Modell.
Quellenbefund 2026-10-19: OSM sagt verlässlich, WAS es im Gemeindegebiet gibt (Bad, Schanze, Klinik, Betrieb, Mühle,
Gipfel, Moor, Fernwanderweg), aber nicht warum es bemerkenswert ist – das liefern Gemeinde-Webseite und Wikipedia.
Je Ort: Relation admin_level 8 mit dem Namen aus orte.json (bei Ortsteilen: 9/10, sonst Umkreis 2 km um die Koordinate).
Schreibt <raum>/osm/<slug>.json (roh, nach Kategorie) und <raum>/osm/<slug>.txt (Block ZEUGEN für Extraktion und
Karteneingabe, gefiltert: Wanderwege nur mit Fernweg-/Themenweg-Namen, Bäche nur die zwei längsten Namen, Hallen und
Studios nur mit Eigennamen).
Aufruf:  GA_RAUM=bahn python -X utf8 scripts/data-fetch/gemeinde_achsen_osm.py <slugs>
"""
import io, json, os, re, sys, time, urllib.parse, urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAUM = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'bahn'))
AUS = os.path.join(RAUM, 'osm')
URL = 'https://overpass-api.de/api/interpreter'
UA = {'User-Agent': 'LernApp-GemeindeAchsen/0.1 (https://github.com/msaxler/lernapp)'}

# (Kategorie im Block, Overpass-Filter)
KATEGORIEN = [
    ('Bad', '["leisure"~"^(swimming_pool|water_park|swimming_area)$"]'),
    ('Freizeit', '["leisure"~"^(golf_course|ice_rink|miniature_golf|stadium|track|slipway|marina)$"]'),
    ('Freizeit', '["tourism"~"^(theme_park|zoo|attraction)$"]'),
    ('Museum', '["tourism"~"^(museum|gallery)$"]'),
    ('Aussicht', '["tourism"="viewpoint"]'),
    ('Burg/Denkmal', '["historic"~"^(castle|ruins|monument|memorial|fort|manor|city_gate|tower|mine|archaeological_site|wayside_shrine)$"]'),
    ('Kultur', '["amenity"~"^(theatre|cinema|arts_centre|planetarium)$"]'),
    ('Bildung', '["amenity"~"^(university|college)$"]'),
    ('Klinik', '["amenity"~"^(hospital|clinic)$"]'),
    ('Brauerei/Winzer', '["craft"~"^(brewery|winery|distillery)$"]'),
    ('Betrieb', '["man_made"~"^(works|mine|windmill|watermill|chimney|lighthouse)$"]'),
    ('Betrieb', '["landuse"="industrial"]'),
    ('Kirche/Kloster', '["amenity"="place_of_worship"]["building"~"^(church|cathedral|chapel|monastery)$"]'),
    ('Gipfel', '["natural"="peak"]'),
    ('Natur', '["natural"~"^(cave_entrance|waterfall|spring|hot_spring|gorge)$"]'),
    ('Schutzgebiet', '["boundary"~"^(national_park|protected_area)$"]'),
    ('Schutzgebiet', '["leisure"="nature_reserve"]'),
    ('Bahnhof', '["railway"~"^(station|halt)$"]'),
    ('Sportstätte', '["leisure"~"^(sports_hall|sports_centre)$"]'),
    ('Sportstätte', '["sport"~"^(ski_jumping|skiing|climbing|bobsleigh|toboggan)$"]'),
]
FERNWEG = re.compile(r'weg$|pfad$|steig$|route|Jakobus|Westweg|Ostweg|Mittelweg|Rundweg|E\d\b|Wiiwegli|Pfad\b', re.I)
RAUSCHEN = re.compile(r' - | – |→|Unterführung|Parkplatz|Haltestelle$', re.I)
STUDIO = re.compile(r'studio|gym|fitness|center|tc |tv |sv |fc ', re.I)


def abfrage(q, versuche=4):
    for i in range(versuche):
        try:
            req = urllib.request.Request(URL, data=urllib.parse.urlencode({'data': q}).encode(), headers=UA)
            with urllib.request.urlopen(req, timeout=240) as r:
                return json.load(r)
        except Exception as e:
            print('  Overpass:', e, '- warte')
            time.sleep(30 * (i + 1))
    return {'elements': []}


def gebiet(name, einheit, lat, lon):
    """Overpass-Gebietsfilter: die Verwaltungsgrenze, die den Ortsmittelpunkt enthält (Gemeinde admin_level 8, Ortsteil 9/10);
    nicht nach dem Namen – „Staufen“ traf eine andere Gemeinde als „Staufen im Breisgau“ (2026-10-20). Sonst Umkreis."""
    stufe = '^(9|10)$' if einheit.startswith('Ortsteil') else '^8$'
    radius = 2000 if einheit.startswith('Ortsteil') else 3000
    return ('is_in(%s,%s)->.a;\n(area.a["boundary"="administrative"]["admin_level"~"%s"];)->.g;' % (lat, lon, stufe), '(area.g)',
            '(around:%d,%s,%s)' % (radius, lat, lon))


def holen(name, einheit, lat, lon):
    a, innen, umkreis = gebiet(name, einheit, lat, lon)
    for filt in (innen, umkreis):
        q = '[out:json][timeout:180];\n%s\n(' % (a if filt == innen else '')
        for _, f in KATEGORIEN:
            for t in ('node', 'way', 'relation'):
                q += '\n  %s%s["name"]%s;' % (t, f, filt)
        q += '\n  way["waterway"~"^(river|stream)$"]["name"]%s;\n  relation["route"~"^(hiking|bicycle)$"]["name"]%s;\n);\nout tags center;' % (filt, filt)
        d = abfrage(q)
        if d.get('elements'):
            return d, 'Gemeindegrenze' if filt == innen else 'Umkreis'
    return {'elements': []}, 'nichts'


def sortieren(d):
    aus, gesehen = {}, set()
    for e in d.get('elements', []):
        t = e.get('tags', {})
        n = t.get('name')
        if not n or n in gesehen:
            continue
        kat = None
        if t.get('waterway'):
            kat = 'Gewässer'
        elif t.get('route') in ('hiking', 'bicycle'):
            kat = 'Wanderweg' if t['route'] == 'hiking' else 'Radweg'
        else:
            for k, f in KATEGORIEN:
                schl = re.findall(r'\["(\w+)"', f)[0]
                if schl not in t:
                    continue
                m = re.findall(r'~"(.+?)"', f)
                muster = m[0] if m else '^' + re.escape(re.findall(r'="(.+?)"', f)[0]) + '$'
                if re.search(muster, t[schl]):
                    kat = k
                    break
        if not kat:
            continue
        gesehen.add(n)
        zusatz = []
        if t.get('ele'):
            zusatz.append('%s m' % t['ele'].split('.')[0])
        if t.get('start_date'):
            zusatz.append('seit ' + t['start_date'][:4])
        if t.get('sport'):
            zusatz.append(t['sport'].replace('_', ' '))
        if t.get('distance'):
            zusatz.append('%s km' % t['distance'].replace('km', '').strip())
        aus.setdefault(kat, []).append({'name': n, 'zusatz': ', '.join(zusatz), 'wikipedia': t.get('wikipedia'), 'website': t.get('website'),
                                        'tags': {k: v for k, v in t.items() if k in ('leisure', 'tourism', 'historic', 'amenity', 'craft',
                                                                                       'man_made', 'natural', 'waterway', 'route', 'sport', 'railway', 'landuse')}})
    return aus


def block(aus, art):
    zeilen = ['ZEUGEN (OpenStreetMap, %s; belegt nur, dass es die Sache gibt):' % art]
    for kat, liste in aus.items():
        if kat == 'Wanderweg' or kat == 'Radweg':
            liste = [x for x in liste if FERNWEG.search(x['name']) and not RAUSCHEN.search(x['name'])][:6]
        elif kat == 'Gewässer':
            liste = [x for x in liste if x['tags'].get('waterway') == 'river'][:2] or liste[:2]
        elif kat == 'Sportstätte':
            liste = [x for x in liste if not STUDIO.search(x['name'])][:6]
        else:
            liste = liste[:8]
        for x in liste:
            zeilen.append('  %s: %s%s' % (kat, x['name'], ' (%s)' % x['zusatz'] if x['zusatz'] else ''))
    return '\n'.join(zeilen) + '\n'


def main():
    with io.open(os.path.join(RAUM, 'orte.json'), encoding='utf-8') as f:
        orte = {o[0]: o for o in json.load(f)['orte']}
    with io.open(os.path.join(RAUM, 'grunddaten.json'), encoding='utf-8') as f:
        grund = {o['slug']: o for o in json.load(f)['orte']}
    os.makedirs(AUS, exist_ok=True)
    for slug in sys.argv[1:]:
        o, g = orte[slug], grund[slug]
        d, art = holen(o[2], o[4], g['lat'], g['lon'])
        aus = sortieren(d)
        # Overpass-Ausfall (502 nach allen Versuchen, Littenweiler 2026-10-19): eine vorhandene Zeugenliste nicht mit „nichts“ überschreiben
        if not aus and os.path.exists(os.path.join(AUS, slug + '.txt')):
            print('%-24s Overpass ohne Antwort – vorhandene Zeugenliste bleibt' % slug)
            continue
        with io.open(os.path.join(AUS, slug + '.json'), 'w', encoding='utf-8', newline='\n') as f:
            json.dump({'ort': slug, 'gebiet': art, 'kategorien': aus}, f, ensure_ascii=False, indent=1)
        txt = block(aus, art)
        with io.open(os.path.join(AUS, slug + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(txt)
        print('%-24s %-14s %3d Objekte, %2d Zeugen im Block' % (slug, art, sum(len(v) for v in aus.values()), txt.count('\n') - 1))
        time.sleep(5)


if __name__ == '__main__':
    main()
