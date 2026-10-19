"""Quellenprobe Ortsporträt (Mike 2026-10-19: Qualität zuerst, Region Freiburg): Was gibt OpenStreetMap für einen Ort her?
Overpass: benannte Objekte mit Charakter (Bad, Museum, Burg, Aussicht, Theater, Klinik, Hochschule, Brauerei, Fluss,
Gipfel, Wanderweg-Relation, Naturpark …) innerhalb der Gemeindegrenze (admin_level 8, Name = Ort), sonst im Umkreis.
Aufruf: python -X utf8 scripts/data-explore/osm_ortsportraet_probe.py "Kirchzarten" "Staufen im Breisgau"
Schreibt data/gemeinde-achsen/probe-ortsportraet/osm-<name>.json und druckt eine Übersicht je Kategorie.
"""
import io, json, os, re, sys, time, urllib.parse, urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUS = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'probe-ortsportraet')
URL = 'https://overpass-api.de/api/interpreter'
UA = {'User-Agent': 'quizaway-ortsportraet-probe/0.1 (msaxler@gmail.com)'}

KATEGORIEN = [
    ('Bad / Freizeit', '["leisure"~"^(swimming_pool|water_park|swimming_area|sports_centre|golf_course|ice_rink|miniature_golf)$"]'),
    ('Museum / Sehenswert', '["tourism"~"^(museum|attraction|viewpoint|theme_park|zoo|artwork|gallery)$"]'),
    ('Burg / Denkmal', '["historic"~"^(castle|ruins|monument|memorial|fort|manor|city_gate|tower|mine|archaeological_site)$"]'),
    ('Kultur / Bildung', '["amenity"~"^(theatre|cinema|university|college|library|arts_centre|planetarium)$"]'),
    ('Klinik / Reha', '["amenity"~"^(hospital|clinic)$"]'),
    ('Brauerei / Winzer', '["craft"~"^(brewery|winery|distillery)$"]'),
    ('Industrie / Betrieb', '["man_made"~"^(works|mine|windmill|watermill|tower|lighthouse|chimney)$"]'),
    ('Kirche / Kloster', '["amenity"="place_of_worship"]["building"~"^(church|cathedral|chapel|monastery)$"]'),
    ('Gipfel / Natur', '["natural"~"^(peak|cave_entrance|waterfall|spring|hot_spring)$"]'),
    ('Schutzgebiet', '["boundary"~"^(national_park|protected_area)$"]'),
    ('Bahnhof', '["railway"~"^(station|halt)$"]'),
    ('Sport (Stadion/Halle)', '["leisure"~"^(stadium|sports_hall|track)$"]'),
]


def abfrage(q, versuche=3):
    for i in range(versuche):
        try:
            req = urllib.request.Request(URL, data=urllib.parse.urlencode({'data': q}).encode(), headers=UA)
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except Exception as e:
            print('  Overpass-Fehler', e, '- warte')
            time.sleep(20 * (i + 1))
    return {'elements': []}


def probe(name):
    # Gemeindegrenze: Relation admin_level 8 mit diesem Namen; die Objekte darin (area)
    q = '[out:json][timeout:120];\narea["boundary"="administrative"]["admin_level"="8"]["name"="%s"]->.g;\n(' % name
    for _, f in KATEGORIEN:
        for t in ('node', 'way', 'relation'):
            q += '\n  %s%s["name"](area.g);' % (t, f)
    # Flüsse und Wanderwege, die das Gebiet berühren
    q += '\n  way["waterway"~"^(river|stream)$"]["name"](area.g);\n  relation["route"="hiking"]["name"](area.g);'
    q += '\n);\nout tags center;'
    d = abfrage(q)
    aus = {}
    gesehen = set()
    for e in d.get('elements', []):
        t = e.get('tags', {})
        n = t.get('name')
        if not n or n in gesehen:
            continue
        kat = 'Fluss / Bach' if t.get('waterway') else 'Wanderweg' if t.get('route') == 'hiking' else None
        if not kat:
            for k, f in KATEGORIEN:
                schl = re.findall(r'\["(\w+)"', f)[0]
                if schl in t and re.search(re.findall(r'~"(.+?)"', f)[0] if '~' in f else '^' + re.findall(r'="(.+?)"', f)[0] + '$', t[schl]):
                    kat = k
                    break
        if not kat:
            continue
        gesehen.add(n)
        kurz = {k: v for k, v in t.items() if k in ('name', 'wikipedia', 'wikidata', 'website', 'description', 'start_date',
                                                   'opening_hours', 'ele', 'sport', 'operator', 'brand', 'historic', 'tourism',
                                                   'leisure', 'amenity', 'craft', 'natural', 'waterway', 'route', 'distance', 'railway')}
        aus.setdefault(kat, []).append(kurz)
    return aus


if __name__ == '__main__':
    os.makedirs(AUS, exist_ok=True)
    for name in sys.argv[1:]:
        print('==', name)
        aus = probe(name)
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')).strip('-')
        with io.open(os.path.join(AUS, 'osm-%s.json' % slug), 'w', encoding='utf-8', newline='\n') as f:
            json.dump(aus, f, ensure_ascii=False, indent=1)
        for kat, liste in aus.items():
            print('  %-22s %2d  %s' % (kat, len(liste), ', '.join(x['name'] for x in liste[:8]) + (' …' if len(liste) > 8 else '')))
        print('  gesamt', sum(len(v) for v in aus.values()), 'benannte Objekte')
        time.sleep(5)
