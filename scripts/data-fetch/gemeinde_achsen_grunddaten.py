"""Gemeinde-Achsen Iteration 1: Grunddaten (Schicht 0) je Ort erweitern.

Liest data/gemeinde-achsen/iter1/schicht0.json (Ortsliste, Wikidata-Kennung) und schreibt
data/gemeinde-achsen/iter1/grunddaten.json: je Ort ein Satz optionaler Eigenschaften, jede mit Wert,
Quelle und Stand. Fehlt eine Angabe, fehlt die Eigenschaft; nichts wird geraten.

Quellen:
  - Wikidata: Einwohner, Höhe, Fläche, Koordinaten, Zugehörigkeit, Kfz-Kennzeichen (P395), PLZ, Vorwahl,
    Gemeindeschlüssel, Ersterwähnung (P1249), Partnerstädte, Bahnhöfe (SPARQL).
  - Wikipedia-Infobox: Höhe, Landkreis, Bürgermeister, Eingemeindung (Stadtteile).
  - Extraktion Schicht 1 (dewiki): Jahr der Ersterwähnung aus dem Ortsblock.
  - Bundeswahlleiterin, Wahlbezirksstatistik Bundestagswahl 2025: Zweitstimmen je Gemeinde (amtlich).
  - Altbestand der Originalvariante (data/geo.sqlite, staedte.json, bahnhof.json, geschichte.json,
    kfz_kennzeichen.csv): als zweite Quelle, wo der Ort dort vorkommt. Abweichungen werden vermerkt.
  - berechnet: Einwohnerdichte, Luftlinie zur nächsten Großstadt und zur Landeshauptstadt.

Aufruf:  python -X utf8 scripts/data-fetch/gemeinde_achsen_grunddaten.py
Entscheid dazu: docs/konzepte/gemeinde-achsen-entscheidungen-2026-10-01.md, E10 und E11.
"""
import csv
import datetime
import io
import json
import math
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(WURZEL, 'data')
AUS = os.path.join(DATA, 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
UA = {'User-Agent': 'LernApp-GemeindeAchsen/0.1 (https://github.com/msaxler/lernapp)'}
WBZ_URL = 'https://www.bundeswahlleiterin.de/dam/jcr/e79a7bd3-0607-4e87-9752-8e601e299e00/btw25_wbz.zip'
WBZ_ZIP = os.path.join(DATA, 'raw', 'btw25_wbz.zip')
HEUTE = datetime.date.today().isoformat()
# Einstellungen des Raums (Ortsliste, Stadtbezirke); der Raum Freiburg (iter1) hat keine Datei
RAUM = {}
if os.path.exists(os.path.join(AUS, 'orte.json')):
    with io.open(os.path.join(AUS, 'orte.json'), encoding='utf-8') as _f:
        RAUM = json.load(_f)

# Katalog der Grunddaten. Herkunft: Fragekategorie der Originalvariante (data/fragen.json) oder 'neu'.
# einwertig / vollstaendig: Angaben, die der Negativnachweis braucht (Entscheid E5).
# (Schlüssel, Bezeichnung, Herkunft, einwertig, Quelle vollständig, zeitabhängig)
KATALOG = [
    ('bundesland', 'Bundesland', 'geo', True, True, False),
    ('landkreis', 'Landkreis oder Stadtkreis', 'geo', True, True, False),
    ('einwohner', 'Einwohner', 'ew', True, True, True),
    ('flaeche_km2', 'Fläche in km²', 'ew', True, True, False),
    ('dichte_ew_km2', 'Einwohner je km²', 'ew', True, True, True),
    # nicht einwertig: Kreise geben Altkennzeichen aus (Breisgau-Hochschwarzwald seit 2023 auch MÜL, NEU);
    # Wikidata P395 nennt nur das Hauptkennzeichen (Faktencheck 2026-10-02, F4)
    ('kfz', 'Kfz-Kennzeichen', 'kfz', False, False, False),
    ('hoehe_m', 'Höhe in m', 'hoehe', True, False, False),
    ('naechste_grossstadt', 'Nächste Großstadt, Luftlinie', 'dist', True, True, False),
    ('km_landeshauptstadt', 'Luftlinie zur Landeshauptstadt in km', 'dist', True, True, False),
    ('lage', 'Lage zur nächsten Großstadt (für den Steckbrief)', 'dist', True, True, False),
    ('ersterwaehnung', 'Jahr der ersten Erwähnung', 'gesch', True, False, False),
    ('eingemeindung', 'Eingemeindung (Stadtteile)', 'gesch', True, False, False),
    ('bahnhof', 'Bahnhöfe und Haltepunkte', 'bahn', False, False, False),
    ('plz', 'Postleitzahl', 'Altbestand geo.sqlite, bisher ohne Frage', False, True, False),
    ('vorwahl', 'Telefonvorwahl', 'neu', False, True, False),
    ('gewaesser', 'Flüsse', 'Altbestand staedte.json, bisher ohne Frage', False, False, False),
    ('kueste', 'Küstenort', 'Altbestand geo.sqlite, bisher ohne Frage', True, True, False),
    ('wahl_btw25', 'Bundestagswahl 2025, Zweitstimmen', 'neu (Politik)', True, True, True),
    ('buergermeister', 'Bürgermeister', 'neu (Politik)', True, False, True),
    ('partnerstaedte', 'Partnerstädte', 'neu', False, False, False),
]
ISO_LAND = {'DE-BW': 'Baden-Württemberg', 'DE-BY': 'Bayern', 'DE-HE': 'Hessen', 'DE-RP': 'Rheinland-Pfalz', 'DE-SL': 'Saarland',
            'DE-NW': 'Nordrhein-Westfalen', 'DE-NI': 'Niedersachsen', 'DE-SH': 'Schleswig-Holstein',
            'DE-MV': 'Mecklenburg-Vorpommern', 'DE-BB': 'Brandenburg', 'DE-SN': 'Sachsen', 'DE-ST': 'Sachsen-Anhalt',
            'DE-TH': 'Thüringen'}
LANDESHAUPTSTADT = {'Baden-Württemberg': 'Stuttgart', 'Bayern': 'München', 'Hessen': 'Wiesbaden',
                    'Rheinland-Pfalz': 'Mainz', 'Saarland': 'Saarbrücken', 'Nordrhein-Westfalen': 'Düsseldorf',
                    'Niedersachsen': 'Hannover', 'Schleswig-Holstein': 'Kiel', 'Mecklenburg-Vorpommern': 'Schwerin',
                    'Brandenburg': 'Potsdam', 'Sachsen': 'Dresden', 'Sachsen-Anhalt': 'Magdeburg', 'Thüringen': 'Erfurt'}


def hole(url):
    """GET mit Wartezeit bei HTTP 429 (Wikimedia drosselt dichte Anfragen) und bei Serverfehlern
    (der Abfragedienst von Wikidata antwortet zeitweise mit 502 bis 504; Befund Raum Neuwied, 2026-10-02)."""
    for versuch in range(6):
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 502, 503, 504) or versuch == 5:
                raise
            warte = int(e.headers.get('Retry-After') or 0) or 10 * (versuch + 1)
            print('  429, warte %d s' % warte)
            time.sleep(warte)


def km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(a))


def wert(w, quelle, stand=None, hinweis=None):
    e = {'wert': w, 'quelle': quelle}
    if stand:
        e['stand'] = stand
    if hinweis:
        e['hinweis'] = hinweis
    return e


# ── Wikidata ────────────────────────────────────────────────────────────────

def wd_claims(qids):
    d = hole('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'wbgetentities', 'format': 'json', 'ids': '|'.join(qids), 'props': 'claims|labels', 'languages': 'de'}))
    return d['entities']


def gueltige(claims, prop):
    """Alle nicht verworfenen Aussagen ohne Enddatum: Liste (Wert, Zeitpunkt, bevorzugt)."""
    aus = []
    for c in claims.get(prop, []):
        snak = c.get('mainsnak', {})
        if snak.get('snaktype') != 'value' or c.get('rank') == 'deprecated' or 'P582' in c.get('qualifiers', {}):
            continue
        zeit = ''
        for q in c.get('qualifiers', {}).get('P585', []):
            if q.get('snaktype') == 'value':
                zeit = q['datavalue']['value']['time'][1:11]
        aus.append((snak['datavalue']['value'], zeit, c.get('rank') == 'preferred'))
    return aus


def neuester(claims, prop):
    kand = sorted(gueltige(claims, prop), key=lambda k: (k[2], k[1]))
    return (kand[-1][0], kand[-1][1]) if kand else (None, None)


def wd_bahnhoefe(qids):
    # in Gruppen zu acht: 29 Orte auf einmal (Raum bahn, 2026-10-03) brachten den Abfragedienst an die Zeitgrenze (500)
    aus = {}
    for i in range(0, len(qids), 8):
        q = ('SELECT ?ort ?sLabel ?tLabel WHERE { VALUES ?ort { %s } ?s wdt:P131 ?ort ; wdt:P31 ?t . '
             '?t wdt:P279* wd:Q12819564 . SERVICE wikibase:label { bd:serviceParam wikibase:language "de". } }'
             % ' '.join('wd:' + x for x in qids[i:i + 8]))
        d = hole('https://query.wikidata.org/sparql?' + urllib.parse.urlencode({'query': q, 'format': 'json'}))
        for b in d['results']['bindings']:
            if re.search(r'Bahnhof|Haltepunkt', b['tLabel']['value']):
                aus.setdefault(b['ort']['value'].rsplit('/', 1)[1], set()).add(b['sLabel']['value'])
    return aus


# ── Wikipedia-Infobox ───────────────────────────────────────────────────────

def infobox(titel):
    d = hole('https://de.wikipedia.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'parse', 'format': 'json', 'page': titel, 'prop': 'wikitext', 'section': 0, 'redirects': 1}))
    m = re.search(r'\{\{Infobox[^\n]*\n(.*?)\n\}\}', d['parse']['wikitext']['*'], flags=re.S)
    felder = {}
    for zeile in (m.group(1) if m else '').split('\n'):
        t = re.match(r'\s*\|\s*([^=]+?)\s*=\s*(.*)$', zeile)
        if t and t.group(2).strip():
            roh = re.sub(r'<[^>]+>', ' ', t.group(2))
            roh = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', roh)
            felder[t.group(1).strip().upper()] = ' '.join(roh.split())
    return felder


# ── Extraktion Schicht 1: Ersterwähnung aus dem Ortsblock ───────────────────

def ersterwaehnung_extraktion(slug, name):
    pfad = os.path.join(AUS, 'extraktion', slug + '.txt')
    if not os.path.exists(pfad):
        return []
    with io.open(pfad, encoding='utf-8') as f:
        bloecke = f.read().split('\n---')
    jahre = []
    for b in bloecke:
        kopf = re.search(r'ENTITÄT:\s*(\S+)\s*\nBEZEICHNUNG:\s*([^\n]+)', b)
        if not kopf or kopf.group(1).lower() not in ('ort', 'gemeinde', 'stadt', 'ortsteil', 'stadtteil'):
            continue
        if name.lower() not in kopf.group(2).lower():
            continue
        for k, v in re.findall(r'^\s+(erste?[a-zäöü_]*erw[aä]e?hnung[a-zäöü_]*):\s*"?(\d{3,4})\b', b, flags=re.M | re.I):
            if int(v) not in jahre:
                jahre.append(int(v))
    return jahre


# ── Bundestagswahl 2025, Wahlbezirksstatistik ───────────────────────────────

def wahl_laden():
    if not os.path.exists(WBZ_ZIP):
        os.makedirs(os.path.dirname(WBZ_ZIP), exist_ok=True)
        req = urllib.request.Request(WBZ_URL, headers=UA)
        with urllib.request.urlopen(req, timeout=120) as r, open(WBZ_ZIP, 'wb') as f:
            f.write(r.read())
    with zipfile.ZipFile(WBZ_ZIP) as z:
        text = z.read('btw25_wbz_ergebnisse.csv').decode('utf-8-sig')
    zeilen = list(csv.reader(io.StringIO(text), delimiter=';'))
    kopf = zeilen[4]
    ix = {k: i for i, k in enumerate(kopf)}
    parteien = [(k[:-len(' - Zweitstimmen')], i) for i, k in enumerate(kopf)
                if k.endswith(' - Zweitstimmen') and not k.startswith(('Ungültige', 'Gültige'))]
    # Namen der Verbandsgemeinden (Leitband, Satzart 50)
    with zipfile.ZipFile(WBZ_ZIP) as z:
        leit = z.read('btw25_wbz_leitband.csv').decode('utf-8-sig')
    vg_name = {}
    for l in leit.split('\n'):
        p = l.split(';')
        if len(p) > 8 and p[0] == '50':
            vg_name[p[2] + p[3] + p[4] + p[5]] = p[8]
    summe = {}
    zahl = lambda x: int(x) if x.strip().isdigit() else 0
    for r in zeilen[5:]:
        if len(r) < len(kopf) or not r[ix['Land']].isdigit():
            continue
        kreis = r[ix['Land']] + r[ix['Regierungsbezirk']] + r[ix['Kreis']]
        ags = kreis + r[ix['Gemeinde']]
        vg = 'VG' + kreis + r[ix['Verbandsgemeinde']]
        # je Zeile drei Summen: die Gemeinde, ihre Verbandsgemeinde, der einzelne Wahlbezirk (ags#nummer)
        for schluessel, name in ((ags, r[ix['Gemeindename']]), (vg, vg_name.get(vg[2:], '')),
                                 ('%s#%s' % (ags, r[ix['Wahlbezirk']].strip()), r[ix['Gemeindename']])):
            s = summe.setdefault(schluessel, {'name': name, 'berechtigt': 0, 'waehlende': 0, 'gueltig': 0, 'p': {},
                                              'scheine': 0, 'brief': 0})
            s['berechtigt'] += zahl(r[ix['Wahlberechtigte (A)']])
            s['scheine'] += zahl(r[ix['Wahlberechtigte mit Sperrvermerk (A2)']])
            if r[ix['Bezirksart']].strip() == '5':
                s['brief'] += zahl(r[ix['Wählende (B)']])
            s['waehlende'] += zahl(r[ix['Wählende (B)']])
            s['gueltig'] += zahl(r[ix['Gültige - Zweitstimmen']])
            for p, i in parteien:
                s['p'][p] = s['p'].get(p, 0) + zahl(r[i])
        # Rheinland-Pfalz: Kleine Gemeinden zählen ihre Briefwahl nicht selbst aus, sondern die Verbandsgemeinde
        # für alle zusammen. Dann fehlt der Gemeinde-Summe die Briefwahl (Befund Raum Neuwied, 2026-10-02).
        if r[ix['Kennziffer Briefwahlzugehörigkeit']].strip() not in ('', '00'):
            summe[ags]['briefwahl_bei'] = vg
    return summe


def wahl_bezirke(summe, ags, praefix):
    """Summe der Wahlbezirke einer Gemeinde, deren Nummer zu einem Stadtteil gehört.

    Urnenbezirke sind vierstellig (1201), Briefwahlbezirke dreistellig (121); beide beginnen mit der
    Kennzahl des Stadtteils (Stimmbezirkseinteilung der Stadt)."""
    aus = {'name': '', 'berechtigt': 0, 'waehlende': 0, 'gueltig': 0, 'p': {}, 'scheine': 0, 'brief': 0}
    n = 0
    for k, s in summe.items():
        if k.startswith(ags + '#') and len(k.split('#')[1]) in (3, 4) and k.split('#')[1].startswith(praefix):
            n += 1
            for f in ('berechtigt', 'waehlende', 'gueltig', 'scheine', 'brief'):
                aus[f] += s[f]
            for p, v in s['p'].items():
                aus['p'][p] = aus['p'].get(p, 0) + v
    return aus if n else None


# Stadtteil-Ergebnisse veröffentlichen die Städte selbst (Entscheid Mike 2026-10-02). Freiburg: Open Data des
# Wahlportals (komm.ONE votemanager), Ebene Stadtbezirke, Briefwahl eingerechnet.
STADTBEZIRKE = {'08311000': 'https://wahlergebnisse.komm.one/lb/produktion/wahltermin-20250223/08311000/daten/opendata/'}
KURZNAME = {'Christlich Demokratische Union Deutschlands': 'CDU', 'Sozialdemokratische Partei Deutschlands': 'SPD',
            'BÜNDNIS 90/DIE GRÜNEN': 'GRÜNE', 'Freie Demokratische Partei': 'FDP', 'Alternative für Deutschland': 'AfD',
            'Die Linke': 'Die Linke', 'FREIE WÄHLER': 'FREIE WÄHLER', 'Volt Deutschland': 'Volt',
            'Bündnis Sahra Wagenknecht - Vernunft und Gerechtigkeit': 'BSW'}


def wahl_stadtbezirk(ags, name):
    """Zweitstimmen eines Stadtbezirks aus dem Open-Data-Angebot der Stadt; None, wenn es keins gibt."""
    if ags not in STADTBEZIRKE:
        return None
    roh = os.path.join(DATA, 'raw')
    dateien = {'open_data.json': os.path.join(roh, 'btw25_%s_open_data.json' % ags)}
    if not os.path.exists(dateien['open_data.json']):
        os.makedirs(roh, exist_ok=True)
        with urllib.request.urlopen(urllib.request.Request(STADTBEZIRKE[ags] + 'open_data.json', headers=UA), timeout=60) as r, \
                open(dateien['open_data.json'], 'wb') as f:
            f.write(r.read())
    with io.open(dateien['open_data.json'], encoding='utf-8') as f:
        od = json.load(f)
    csv_name = next(c['url'] for c in od['csvs'] if c['ebene'] == 'Stadtbezirke')
    pfad = os.path.join(roh, 'btw25_%s_stadtbezirke.csv' % ags)
    if not os.path.exists(pfad):
        with urllib.request.urlopen(urllib.request.Request(STADTBEZIRKE[ags] + csv_name, headers=UA), timeout=60) as r, open(pfad, 'wb') as f:
            f.write(r.read())
    partei = {}
    for p in od['dateifelder'][0]['parteien']:
        m = re.search(r'F(\d+)', p['feld'])
        if m:
            partei['F' + m.group(1)] = KURZNAME.get(p['wert'], p['wert'])
    with io.open(pfad, encoding='utf-8-sig') as f:
        for z in csv.DictReader(f, delimiter=';'):
            if z['gebiet-name'] == name:
                zahl = lambda x: int(x) if (x or '').strip().isdigit() else 0
                return {'name': name, 'berechtigt': zahl(z['A']), 'waehlende': zahl(z['B']), 'gueltig': zahl(z['F']),
                        'p': {partei[k]: zahl(v) for k, v in z.items() if k in partei}}
    return None


def wahl_eintrag(s, bezug=None, quelle=None):
    alle = sorted(s['p'].items(), key=lambda kv: -kv[1])
    # alle Parteien ab fünf Prozent, mindestens die vier stärksten
    rang = [kv for i, kv in enumerate(alle) if i < 4 or 100.0 * kv[1] / s['gueltig'] >= 5.0]
    w = {'staerkste_partei': rang[0][0],
         'anteile_prozent': {p: round(100.0 * n / s['gueltig'], 1) for p, n in rang},
         'wahlbeteiligung_prozent': round(100.0 * s['waehlende'] / s['berechtigt'], 1) if s['berechtigt'] else None,
         'gueltige_zweitstimmen': s['gueltig']}
    return wert(w, quelle or 'Bundeswahlleiterin, Wahlbezirksstatistik Bundestagswahl 2025 (amtlich)', '2025-02-23',
                bezug or 'Summe aller Urnen- und Briefwahlbezirke der Gemeinde')


# ── Altbestand der Originalvariante ─────────────────────────────────────────

class Altbestand:
    def __init__(self):
        lies = lambda n: json.load(io.open(os.path.join(DATA, n), encoding='utf-8'))
        self.staedte = lies('staedte.json')
        self.geschichte = lies('geschichte.json')
        self.bahnhof = lies('bahnhof.json')['bahnhof_kategorien']
        with io.open(os.path.join(DATA, 'kfz_kennzeichen.csv'), encoding='utf-8') as f:
            self.kfz_csv = {r['stadt']: r['kfz'] for r in csv.DictReader(f)}
        pfad = os.path.join(DATA, 'geo.sqlite')
        self.db = sqlite3.connect(pfad) if os.path.exists(pfad) else None

    def stadt_json(self, namen):
        for s in self.staedte:
            if s['name'] in namen:
                return s
        return None

    def geo(self, namen, lat, lon):
        """Zeilen aus geo.sqlite mit passendem Namen im Umkreis von 3 km."""
        if not self.db:
            return []
        frage = ("select s.id, t.value, s.kreis_id, s.einwohner, s.hoehe_m, s.ist_kuestenstadt, s.lat, s.lon "
                 "from stadt s join translations t on t.pool='stadt' and t.objekt_id=s.id and t.key='name' "
                 "where t.value in (%s)" % ','.join('?' * len(namen)))
        return [r for r in self.db.execute(frage, list(namen)) if km(lat, lon, r[6], r[7]) <= 3.0]

    def plz(self, stadt_ids):
        if not self.db or not stadt_ids:
            return []
        frage = 'select distinct plz_id from plz_stadt where stadt_id in (%s) order by 1' % ','.join('?' * len(stadt_ids))
        return [r[0] for r in self.db.execute(frage, stadt_ids)]

    def kfz_kreis(self, kreis_id):
        if not self.db or not kreis_id:
            return []
        return [r[0] for r in self.db.execute('select id from kfz_kennzeichen where kreis_id=? and aktiv=1', (kreis_id,))]


# ── Zusammenbau ─────────────────────────────────────────────────────────────

def main():
    with io.open(os.path.join(AUS, 'schicht0.json'), encoding='utf-8') as f:
        orte = json.load(f)
    alt = Altbestand()
    wahl = wahl_laden()
    ent = wd_claims([o['wikidata'] for o in orte])
    bahn = wd_bahnhoefe([o['wikidata'] for o in orte])
    grossstaedte = [s for s in alt.staedte if s['einwohner'] >= 100000]
    aus, maengel = [], []

    for o in orte:
        c = ent[o['wikidata']]['claims']
        e = {}
        ist_ortsteil = o['einheit'].startswith('Ortsteil')
        box = infobox(o['dewiki'])
        time.sleep(1)
        # Bei Stadtteilen kommen Zugehörigkeit, Kennzeichen und Wahl von der Gemeinde (Entscheid E7).
        traeger_qid, traeger_c, bezug = o['wikidata'], c, None
        stadt, stadt_box = None, {}
        if ist_ortsteil:
            # die Stadt steht in der Einheit ("Ortsteil von Neuwied") und unter P131 des Stadtteils
            stadt = o['einheit'].split(' von ', 1)[1]
            kand = wd_claims([v['id'] for v, _, _ in gueltige(c, 'P131')])
            traeger_qid = next(q for q, t in kand.items() if t['labels'].get('de', {}).get('value') == stadt)
            traeger = kand[traeger_qid]
            traeger_c = traeger['claims']
            bezug = 'gilt für die Gemeinde %s, nicht für den Stadtteil allein' % traeger['labels']['de']['value']
            stadt_box = infobox(stadt)
            time.sleep(1)

        # Zugehörigkeit
        einheiten = [v['id'] for v, _, _ in gueltige(traeger_c, 'P131')]
        labels = wd_claims(einheiten) if einheiten else {}
        kreis = [labels[q]['labels']['de']['value'] for q in einheiten
                 if re.match(r'(Land|Stadt)kreis', labels[q]['labels'].get('de', {}).get('value', ''))]
        if ist_ortsteil and not kreis:
            kreis = ['Stadtkreis ' + stadt]  # kreisfreie Stadt: P131 nennt keinen Kreis
        # Die Infobox führt: Wikidata nennt unter P131 auch aufgelöste Kreise ohne Enddatum.
        if box.get('LANDKREIS'):
            e['landkreis'] = [wert(box['LANDKREIS'], 'dewiki Infobox')]
            passend = [k for k in kreis if box['LANDKREIS'] in k]
            if passend:
                e['landkreis'].append(wert(passend[0], 'Wikidata P131'))
            for k in kreis:
                if box['LANDKREIS'] not in k:
                    maengel.append('%s: Wikidata P131 nennt „%s“ ohne Enddatum, Infobox „%s“' % (o['name'], k, box['LANDKREIS']))
        elif kreis:
            e['landkreis'] = [wert(kreis[0], 'Wikidata P131', hinweis=bezug)]
        land = box.get('BUNDESLAND') or stadt_box.get('BUNDESLAND')
        land = ISO_LAND.get(land, land)  # die Infobox der Ortsteile nennt das Land als Kürzel (DE-RP)
        if not land:
            sys.exit('%s: kein Bundesland in der Infobox' % o['name'])
        e['bundesland'] = [wert(land, 'dewiki Infobox' if box.get('BUNDESLAND') else 'über die Gemeinde', hinweis=None if box.get('BUNDESLAND') else bezug)]

        # Einwohner, Fläche, Dichte
        w, z = neuester(c, 'P1082')
        if w:
            e['einwohner'] = [wert(int(float(w['amount'])), 'Wikidata P1082', z)]
        elif re.match(r'\d[\d.]*$', box.get('EINWOHNER', '')):
            # Stadtteile ohne Einwohnerzahl in Wikidata (Raum Neuwied): Infobox des Stadtteil-Artikels
            e['einwohner'] = [wert(int(box['EINWOHNER'].replace('.', '')), 'dewiki Infobox', box.get('EINWOHNER-STAND-DATUM') or box.get('EINWOHNER-STAND'))]
        w, _ = neuester(c, 'P2046')
        if w:
            e['flaeche_km2'] = [wert(float(w['amount']), 'Wikidata P2046')]
        elif box.get('FLÄCHE'):
            e['flaeche_km2'] = [wert(float(box['FLÄCHE'].replace(',', '.')), 'dewiki Infobox')]
        if 'einwohner' in e and 'flaeche_km2' in e:
            e['dichte_ew_km2'] = [wert(int(round(e['einwohner'][0]['wert'] / e['flaeche_km2'][0]['wert'])), 'berechnet aus Einwohner und Fläche')]

        # Kfz-Kennzeichen
        w, _ = neuester(traeger_c, 'P395')
        if w:
            e['kfz'] = [wert(w, 'Wikidata P395', hinweis=bezug)]

        # Höhe: alle Werte, die die Quellen nennen
        hoehen = []
        for v, _, _ in gueltige(c, 'P2044'):
            hoehen.append(wert(int(round(float(v['amount']))), 'Wikidata P2044'))
        if re.match(r'\d+', box.get('HÖHE', '')):
            hoehen.append(wert(int(re.match(r'\d+', box['HÖHE']).group(0)), 'dewiki Infobox'))
        if hoehen:
            e['hoehe_m'] = hoehen

        # Entfernungen
        lat, lon = o['lat'], o['lon']
        naechste = min(grossstaedte, key=lambda s: km(lat, lon, s['lat'], s['lon']))
        e['naechste_grossstadt'] = [wert({'name': naechste['name'], 'km': int(round(km(lat, lon, naechste['lat'], naechste['lon'])))},
                                         'berechnet aus Koordinaten (Wikidata, staedte.json), Großstadt ab 100.000 Einwohnern')]
        # Lage für den Steckbrief: Entfernung und Himmelsrichtung von der nächsten Großstadt aus
        winkel = math.degrees(math.atan2((lon - naechste['lon']) * math.cos(math.radians(lat)), lat - naechste['lat'])) % 360
        richtung = ['nördlich', 'nordöstlich', 'östlich', 'südöstlich', 'südlich', 'südwestlich', 'westlich', 'nordwestlich'][int((winkel + 22.5) // 45) % 8]
        e['lage'] = [wert('%d km %s von %s (Luftlinie, Ortsmitte zu Stadtmitte)' % (
            e['naechste_grossstadt'][0]['wert']['km'], richtung, naechste['name']), 'berechnet aus Koordinaten')]
        haupt = alt.stadt_json([LANDESHAUPTSTADT.get(land, '')])
        if haupt:
            e['km_landeshauptstadt'] = [wert({'name': haupt['name'], 'km': int(round(km(lat, lon, haupt['lat'], haupt['lon'])))},
                                             'berechnet aus Koordinaten (Wikidata, staedte.json)')]

        # Geschichte
        w, _ = neuester(c, 'P1249')
        erw = [wert(int(w['time'][1:5]), 'Wikidata P1249')] if w else []
        for j in ersterwaehnung_extraktion(o['slug'], o['name']):
            erw.append(wert(j, 'dewiki, Extraktion Schicht 1 (Ortsblock)'))
        if erw:
            e['ersterwaehnung'] = erw
        if box.get('EINGEMEINDUNG') or box.get('EINGEMEINDUNGSDATUM'):
            e['eingemeindung'] = [wert(box.get('EINGEMEINDUNG') or box['EINGEMEINDUNGSDATUM'], 'dewiki Infobox')]

        # Bahn
        if bahn.get(o['wikidata']):
            e['bahnhof'] = [wert(sorted(bahn[o['wikidata']]), 'Wikidata (Bahnhöfe mit P131 = Ort)', hinweis='Liste nicht gesichert vollständig')]

        # Post und Telefon
        plz = sorted(set(v for v, _, _ in gueltige(c, 'P281')))
        if plz:
            e['plz'] = [wert(plz, 'Wikidata P281')]
        vorwahl = sorted(set(v for v, _, _ in gueltige(c, 'P473')))
        if vorwahl:
            e['vorwahl'] = [wert(vorwahl, 'Wikidata P473')]

        # Politik
        ags_w, _ = neuester(traeger_c, 'P439')
        ags = ags_w if isinstance(ags_w, str) else None
        bezirk = wahl_stadtbezirk(ags, o['name']) if ist_ortsteil and ags else None
        praefix = RAUM.get('stadtbezirke', {}).get(ags, {}) if ist_ortsteil and ags else {}
        if bezirk:
            e['wahl_btw25'] = [wahl_eintrag(bezirk, 'Ergebnis des Stadtbezirks, Briefwahl eingerechnet',
                                            'Stadt Freiburg im Breisgau, Wahlergebnis nach Stadtbezirken (Open Data des Wahlportals, amtlich)')]
        elif o['name'] in praefix.get('bezirke', {}) and wahl_bezirke(wahl, ags, praefix['bezirke'][o['name']]):
            # Stadt ohne eigenes Open-Data-Angebot: Stimmbezirke des Stadtteils aus der Bundesstatistik summieren
            teil = wahl_bezirke(wahl, ags, praefix['bezirke'][o['name']])
            bezug_teil = 'Summe der Urnen- und Briefwahlbezirke des Stadtteils'
            if teil['brief'] > teil['scheine']:
                # mehr Briefwähler als im Stadtteil Wahlscheine ausgegeben: der Briefwahlbezirk zählt Fremde mit
                bezug_teil += ('; nur ungefähr: der Briefwahlbezirk zählt %d Stimmen bei %d im Stadtteil ausgegebenen '
                               'Wahlscheinen' % (teil['brief'], teil['scheine']))
                maengel.append('%s: Briefwahlbezirk mit %d Stimmen bei %d Wahlscheinen; Stadtteilergebnis nur ungefähr'
                               % (o['name'], teil['brief'], teil['scheine']))
            e['wahl_btw25'] = [wahl_eintrag(teil, bezug_teil, praefix['quelle'])]
        elif ags and ags in wahl and wahl[ags].get('briefwahl_bei'):
            # Die Briefwahl wird für die Verbandsgemeinde gemeinsam ausgezählt: Ein vollständiges Ergebnis gibt es
            # nur für die Verbandsgemeinde; die Gemeinde-Summe wären allein die Urnenstimmen.
            vg = wahl[wahl[ags]['briefwahl_bei']]
            e['wahl_btw25'] = [wahl_eintrag(vg, 'gilt für die Verbandsgemeinde %s, nicht für die %s allein; die Briefwahl wird '
                                            'dort für alle Gemeinden gemeinsam ausgezählt' % (vg['name'], o['einheit']))]
            maengel.append('%s: Briefwahl nur auf Ebene der Verbandsgemeinde %s; Wahlergebnis gilt für die Verbandsgemeinde' % (o['name'], vg['name']))
        elif ags and ags in wahl:
            e['wahl_btw25'] = [wahl_eintrag(wahl[ags], bezug)]
        elif not ist_ortsteil:
            maengel.append('%s: kein Wahlergebnis zum Gemeindeschlüssel %s' % (o['name'], ags))
        bm = box.get('BÜRGERMEISTER')
        if bm:
            partei = box.get('PARTEI')
            m = re.match(r'(.+?)\s*\((.+)\)\s*$', bm)
            if m:
                bm, partei = m.group(1), m.group(2)
            e['buergermeister'] = [wert({'name': bm, 'partei': partei} if partei else {'name': bm}, 'dewiki Infobox', o.get('abruf'),
                                        'zeitabhängig; Aktualität nicht geprüft')]
        partner = [v['id'] for v, _, _ in gueltige(c, 'P190')]
        if partner:
            pl = wd_claims(partner)
            e['partnerstaedte'] = [wert([pl[q]['labels'].get('de', {}).get('value', q) for q in partner], 'Wikidata P190')]

        # Altbestand der Originalvariante als zweite Quelle
        namen = {o['name'], re.sub(r'\s*\(.*\)', '', o['dewiki']), o['name'].replace('St. ', 'Sankt ')}
        sj = alt.stadt_json(namen)
        if sj and km(lat, lon, sj['lat'], sj['lon']) > 5:
            maengel.append('%s: staedte.json führt den Namen mit Koordinaten %.0f km entfernt' % (o['name'], km(lat, lon, sj['lat'], sj['lon'])))
            sj = None
        if sj:
            e.setdefault('einwohner', []).append(wert(sj['einwohner'], 'Altbestand staedte.json'))
            e.setdefault('flaeche_km2', []).append(wert(sj['flaeche'], 'Altbestand staedte.json'))
            e.setdefault('hoehe_m', []).append(wert(sj['hoehe'], 'Altbestand staedte.json'))
            if sj.get('fluesse'):
                e['gewaesser'] = [wert(sj['fluesse'], 'Altbestand staedte.json')]
            e.setdefault('kfz', []).append(wert(sj['kfz'], 'Altbestand staedte.json'))
        geo = alt.geo(namen, lat, lon)
        for r in geo:
            if r[3]:
                e.setdefault('einwohner', []).append(wert(r[3], 'Altbestand geo.sqlite (GeoNames %s)' % r[0]))
            if r[4] is not None:
                e.setdefault('hoehe_m', []).append(wert(r[4], 'Altbestand geo.sqlite (GeoNames %s)' % r[0]))
        if geo:
            e['kueste'] = [wert('ja' if any(r[5] for r in geo) else 'nein', 'Altbestand geo.sqlite')]
            alt_plz = alt.plz([r[0] for r in geo])
            if alt_plz:
                e.setdefault('plz', []).append(wert(alt_plz, 'Altbestand geo.sqlite'))
            kreise = set(r[2] for r in geo if r[2])
            for k in kreise:
                kz = alt.kfz_kreis(k)
                if kz:
                    e.setdefault('kfz', []).append(wert(kz[0] if len(kz) == 1 else kz, 'Altbestand geo.sqlite (Kreis %s)' % k))
                else:
                    maengel.append('%s: geo.sqlite hat für Kreis %s kein Kennzeichen' % (o['name'], k))
        for n in namen:
            if n in alt.kfz_csv:
                e.setdefault('kfz', []).append(wert(alt.kfz_csv[n], 'Altbestand kfz_kennzeichen.csv'))
            if n in alt.geschichte:
                g = alt.geschichte[n]
                if g.get('erste_erwaehnung'):
                    e.setdefault('ersterwaehnung', []).append(wert(g['erste_erwaehnung'], 'Altbestand geschichte.json'))
            if n in alt.bahnhof:
                e.setdefault('bahnhof', []).append(wert(alt.bahnhof[n], 'Altbestand bahnhof.json'))

        # Abweichungen zwischen den Quellen vermerken (erste Quelle gilt als führend)
        for key, liste in e.items():
            if len(liste) < 2:
                continue
            erster = liste[0]['wert']
            for w2 in liste[1:]:
                if isinstance(erster, (int, float)) and isinstance(w2['wert'], (int, float)):
                    grenze = 0.15 if key == 'einwohner' else 0.05
                    if abs(w2['wert'] - erster) > grenze * max(abs(erster), 1):
                        w2['abweichend'] = True
                elif isinstance(erster, str) and isinstance(w2['wert'], str) and erster not in w2['wert'] and w2['wert'] not in erster:
                    w2['abweichend'] = True
                if w2.get('abweichend'):
                    maengel.append('%s: %s %s (%s) gegen %s (%s)' % (o['name'], key, erster, liste[0]['quelle'], w2['wert'], w2['quelle']))

        aus.append({'slug': o['slug'], 'rolle': o['rolle'], 'name': o['name'], 'einheit': o['einheit'],
                    'wikidata': o['wikidata'], 'lat': lat, 'lon': lon, 'gemeindeschluessel': ags,
                    'eigenschaften': e})
        print('%-16s %2d Eigenschaften: %s' % (o['slug'], len(e), ' '.join(sorted(e))))

    ziel = os.path.join(AUS, 'grunddaten.json')
    with io.open(ziel, 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'erzeugt': HEUTE,
                   'katalog': [dict(zip(('schluessel', 'bezeichnung', 'herkunft', 'einwertig', 'quelle_vollstaendig', 'zeitabhaengig'), k)) for k in KATALOG],
                   'nicht_uebernommen': ['naechstes_nachbarland: Die Grenzpunkt-Tabelle der Originalvariante ist zu grob '
                                         '(der Punkt „Breisach“ liegt bei 7,01° statt 7,58° Ost); braucht Grenzgeometrie.',
                                         'ice_strecken, bahnhof_kategorie: im Altbestand nur für 51 große Städte.'],
                   'maengel': maengel, 'orte': aus}, f, ensure_ascii=False, indent=1)
    print('\nAbdeckung (von %d Orten):' % len(aus))
    for k in KATALOG:
        n = sum(1 for a in aus if k[0] in a['eigenschaften'])
        nz = sum(1 for a in aus if k[0] in a['eigenschaften'] and a['rolle'] == 'ziel')
        print('  %-22s %2d, davon Zielorte %2d von 10' % (k[0], n, nz))
    print('\nAbweichungen und Lücken: %d' % len(maengel))
    for m in maengel:
        print('  -', m)
    print('geschrieben:', ziel)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
