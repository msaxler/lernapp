"""Vertiefung Freiburg (Mike 2026-10-27): Orte von visit.freiburg.de (Tourismus der Stadt, FWTM) holen.

Liest die POI-Sitemap (rund 900 Seiten: Sehenswürdigkeiten, Kultur, Natur, aber auch Läden, Lokale, Toiletten), holt jede
Seite einmal (vorhandene bleiben), zieht aus dem JSON-LD Name, Typ, Adresse, Koordinaten, Kurzbeschreibung und aus dem
Seitentext die Kategoriezeile und den Fließtext. Schreibt
  data/gemeinde-achsen/freiburg-vertiefung/visit/roh/<name>.html   Rohseiten
  data/gemeinde-achsen/freiburg-vertiefung/visit/pois.json          je POI ein Eintrag
Aufruf:  python -X utf8 scripts/data-fetch/freiburg_visit_pois.py
"""
import html
import io
import json
import os
import re
import sys
import time
import urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUS = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'freiburg-vertiefung', 'visit')
SITEMAP = 'https://visit.freiburg.de/sitemap.xml'
UA = {'User-Agent': 'Mozilla/5.0 (QuizAway-Recherche)'}


def holen(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read().decode('utf-8', 'replace')


def text(roh):
    """Fließtext des Hauptteils ohne Skripte, Navigation und Fuß."""
    t = re.sub(r'(?s)<(script|style|nav|header|footer)\b.*?</\1>', ' ', roh)
    m = re.search(r'(?s)<main\b.*?</main>', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', m.group(0) if m else t))
    return re.sub(r'\s+', ' ', t).strip()


def lesen(roh, url):
    ld = {}
    for m in re.findall(r'(?s)<script type="application/ld\+json">(.*?)</script>', roh):
        try:
            d = json.loads(m)
        except ValueError:
            continue
        if isinstance(d, dict) and d.get('geo'):
            ld = d
            break
    adr, geo = ld.get('address') or {}, ld.get('geo') or {}
    t = text(roh)
    # Kopfzeile vor dem Namen: Bildnachweis, Zugang, Kategorien („FWTM-Joos Jederzeit frei zugänglich Kultur Holbeinpferd …“)
    name = ld.get('name', '')
    kopf = t[:t.find(name)] if name and name in t[:400] else ''
    return {'url': url, 'name': name, 'typ': ld.get('@type'), 'kopf': kopf.strip(),
            'strasse': adr.get('streetAddress', '').strip(), 'plz': adr.get('postalCode', ''),
            'lat': geo.get('latitude'), 'lon': geo.get('longitude'), 'kurz': ld.get('description', ''),
            'text': t}


def main():
    os.makedirs(os.path.join(AUS, 'roh'), exist_ok=True)
    index = holen(SITEMAP)
    teil = [html.unescape(u) for u in re.findall(r'<loc>([^<]*sitemap=pois[^<]*)</loc>', index)]
    urls = []
    for t in teil:
        urls += [html.unescape(u) for u in re.findall(r'<loc>([^<]*)</loc>', holen(t))]
    print(len(urls), 'POI-Seiten', flush=True)
    pois = []
    for i, url in enumerate(urls):
        datei = os.path.join(AUS, 'roh', re.sub(r'[^a-z0-9-]', '_', url.rstrip('/').rsplit('/', 1)[-1].lower())[:120] + '.html')
        if not os.path.exists(datei):
            try:
                roh = holen(url)
            except Exception as e:
                print('FEHLER', url, e, flush=True)
                continue
            with io.open(datei, 'w', encoding='utf-8') as f:
                f.write(roh)
            time.sleep(0.7)
        with io.open(datei, encoding='utf-8') as f:
            pois.append(lesen(f.read(), url))
        if i % 100 == 0:
            print(i, url, flush=True)
    with io.open(os.path.join(AUS, 'pois.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(pois, f, ensure_ascii=False, indent=1)
    print('Fertig:', len(pois), 'POIs,', sum(1 for p in pois if p['lat']), 'mit Koordinaten', flush=True)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
