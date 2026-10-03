"""Gemeinde-Achsen: Quelltexte aus vertrauenswürdigen Quellen holen (Spielkonzept v0.3.1 §8 Nr. 9).

Je Ort, ohne Modellaufruf:
  - eigene Webseite der Gemeinde (Wikidata P856, oder in orte.json unter "webseite" gesetzt): Startseite und
    Sitemap nach Seiten zu Geschichte, Porträt, Sehenswürdigkeiten, Zahlen durchsuchen, höchstens MAX_SEITEN
    Seiten derselben Domain lesen, Menü- und Fußzeilen-Reste entfernen (Zeilen, die auf vielen Seiten gleich sind);
  - Landesportal, soweit per Adresse erreichbar: regionalgeschichte.net (Rheinland-Pfalz, Saarland; Muster
    /<region>/<ort>.html, in orte.json unter "portal" gesetzt). LEO-BW und LAGIS Hessen liefern ihre Ortsseiten
    nur über eine Suchoberfläche mit Skript bzw. antworteten in der Probe nicht (504); sie fehlen in dieser Fassung.

Ausgabe: data/gemeinde-achsen/<raum>/quellen-amtlich/<slug>.txt – Abschnitte "=== QUELLE: <url> | <art> ===",
dazu quellen-amtlich/index.json (je Ort: Seiten, Zeichen, Art). Wikipedia bleibt in quellen/ als Wegweiser.

Aufruf:  GA_RAUM=bahn python -X utf8 scripts/data-fetch/gemeinde_achsen_quellen_amtlich.py [slugs]
"""
import collections
import html
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAUM = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
AUS = os.path.join(RAUM, 'quellen-amtlich')
UA = {'User-Agent': 'Mozilla/5.0 (LernApp-GemeindeAchsen/0.1; https://github.com/msaxler/lernapp)'}
MAX_SEITEN = 14
MAX_ZEICHEN_SEITE = 12000
# Wörter in Linktext oder Adresse, die auf ortskundliche Seiten zeigen; Gewicht für die Reihenfolge
STICH = [(r'geschicht|chronik|histor', 5), (r'stadtportr|ortsportr|portr[aä]it|stadtinfo|ortsinfo|wir-ueber|ueber-uns', 4),
         (r'zahlen|daten-und-fakten|daten-fakten', 3), (r'sehensw|denkm[aä]l|kirche|burg|schloss|museum|wappen|persoenlich|beruehmt', 2),
         (r'ortsteil|stadtteil', 1)]
WEG = (r'veranstalt|termin|kalender|aktuell|news|presse|stellen|ausschreib|formular|login|suche|kontakt|impressum|datenschutz|'
       r'ordnung|vertrag|satzung|gebuehr|gebühr|miet|austritt|dienstleistung|gottesdienst|\.jpe?g|\.png|\.docx?|mailto:|tel:')
# PDFs nur, wenn sie ausdrücklich ortskundlich sind (Stadtrundgang, Chronik)
PDF_JA = r'geschicht|chronik|histor|rundgang|portr'


def holen_roh(url, n=1500000, versuche=2):
    for v in range(versuche):
        try:
            r = urllib.request.urlopen(urllib.request.Request(adresse(url), headers=UA), timeout=40)
            return r.geturl(), r.read(n), (r.headers.get('Content-Type') or '').lower()
        except Exception as e:
            fehler = e
            time.sleep(1.5)
    raise fehler


def holen(url, n=1500000, versuche=2):
    u, roh, _ = holen_roh(url, n, versuche)
    return u, roh.decode('utf-8', 'replace')


def _zeilen(h):
    h = re.sub(r'(?i)<br\s*/?>|</p>|</h\d>|</li>|</tr>|</div>', '\n', h)
    t = html.unescape(re.sub('<[^>]+>', ' ', h))
    zeilen = [re.sub(r'[ \t ]+', ' ', z).strip() for z in t.split('\n')]
    return [z for z in zeilen if len(z) > 2]


def text_aus(h):
    h = re.sub(r'(?is)<(script|style|noscript|svg|nav|header|footer|form|aside)[^>]*>.*?</\1>', ' ', h)
    # <main>/<article> nur, wenn dort wirklich der Text steht (in Braubach trägt <article> nur die Überschrift)
    m = re.search(r'(?is)<main[^>]*>(.*)</main>', h) or re.search(r'(?is)<article[^>]*>(.*)</article>', h)
    if m:
        z = _zeilen(m.group(1))
        if sum(len(x) for x in z) >= 500:
            return z
    b = re.search(r'(?is)<body[^>]*>(.*)</body>', h)
    return _zeilen(b.group(1) if b else h)


def pdf_text(daten):
    """Text eines PDF der Gemeinde (Stadtrundgang, Chronik); ohne pypdf bleibt das PDF draußen."""
    try:
        import pypdf
        r = pypdf.PdfReader(io.BytesIO(daten))
        t = '\n'.join((p.extract_text() or '') for p in r.pages[:30])
        return [re.sub(r'\s+', ' ', z).strip() for z in t.split('\n') if len(z.strip()) > 2]
    except Exception:
        return []


def adresse(u):
    """Umlaute in Adressen (sankt-goarshausen.de/sehenswürdigkeiten/) für urllib verpacken."""
    p = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(urllib.parse.unquote(p.path)), p.query, ''))


def domain(u):
    d = urllib.parse.urlparse(u).netloc.lower()
    return d[4:] if d.startswith('www.') else d


def gleiche_seite(u, start):
    """Dieselbe Gemeinde-Domain; Unterdomains derselben Gemeinde (kaub.welterbe-mittelrheintal.de) zählen mit."""
    return domain(u) == domain(start)


def kandidaten(start_url, start_html):
    links = []
    for href, txt in re.findall(r'(?is)<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', start_html):
        t = html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', txt))).strip()
        links.append((urllib.parse.urljoin(start_url, href), t))
    # Sitemap (für Seiten, deren Menü erst ein Skript baut, etwa Kenzingen)
    try:
        _, sm = holen(urllib.parse.urljoin(start_url, '/sitemap.xml'), 3000000, 1)
        for loc in re.findall(r'<loc>([^<]+)</loc>', sm):
            links.append((html.unescape(loc.strip()), ''))
    except Exception:
        pass
    wertung = {}
    for u, t in links:
        u = urllib.parse.unquote(u.split('#')[0])
        s = (t + ' ' + u).lower()
        if not gleiche_seite(u, start_url) or re.search(WEG, s) or u.rstrip('/') == start_url.rstrip('/'):
            continue
        if '.pdf' in s and not re.search(PDF_JA, s):
            continue
        w = sum(g for muster, g in STICH if re.search(muster, s))
        if w and len(u) < 220:
            # tiefe Unterseiten (Veranstaltungen mit ID, Einzelmeldungen) abwerten
            w -= 2 * bool(re.search(r'id_\d+|/\d{4}/\d{2}/', u))
            wertung[u] = max(wertung.get(u, 0), w)
    return [u for u, w in sorted(wertung.items(), key=lambda x: (-x[1], len(x[0]))) if w > 0]


def ort_holen(slug, cfg):
    teile, protokoll = [], {'slug': slug, 'seiten': []}
    start = cfg.get('webseite')
    if start:
        try:
            su, sh = holen(start)
            protokoll['start'] = su
            urls = kandidaten(su, sh)
            gelesen = []
            for u in urls:
                if len(gelesen) >= MAX_SEITEN:
                    break
                try:
                    gu, roh, typ = holen_roh(u, 8000000)
                except Exception as e:
                    protokoll['seiten'].append({'url': u, 'fehler': str(e)[:80]})
                    continue
                zeilen = pdf_text(roh) if ('pdf' in typ or roh[:5] == b'%PDF-') else text_aus(roh.decode('utf-8', 'replace'))
                if sum(len(z) for z in zeilen) < 300:
                    continue
                gelesen.append((urllib.parse.unquote(gu), zeilen))
                time.sleep(0.5)
            # Menü- und Fußzeilenreste: Zeilen, die auf mindestens der Hälfte der Seiten vorkommen
            zaehler = collections.Counter(z for _, zs in gelesen for z in set(zs))
            grenze = max(3, len(gelesen) // 2)
            schon = set()
            for gu, zs in gelesen:
                rein = [z for z in zs if zaehler[z] < grenze]
                txt = '\n'.join(rein)[:MAX_ZEICHEN_SEITE]
                # dieselbe Seite unter zweiter Adresse (?seite=1, Rundgang-Stationen mit gleichem Text) nur einmal;
                # verglichen wird erst nach dem Entfernen der Menüreste, sonst sehen alle Seiten gleich aus
                if len(txt) < 300 or txt[:600] in schon:
                    continue
                schon.add(txt[:600])
                teile.append('=== QUELLE: %s | Gemeinde-Webseite ===\n%s' % (gu, txt))
                protokoll['seiten'].append({'url': gu, 'art': 'Gemeinde-Webseite', 'zeichen': len(txt)})
        except Exception as e:
            protokoll['fehler_webseite'] = str(e)[:120]
    for pu in cfg.get('portal', []):
        try:
            gu, gh = holen(pu)
            txt = '\n'.join(text_aus(gh))[:MAX_ZEICHEN_SEITE * 2]
            if len(txt) >= 300:
                teile.append('=== QUELLE: %s | Landesportal ===\n%s' % (gu, txt))
                protokoll['seiten'].append({'url': gu, 'art': 'Landesportal', 'zeichen': len(txt)})
        except Exception as e:
            protokoll['seiten'].append({'url': pu, 'fehler': str(e)[:80]})
    return teile, protokoll


def webseite_aus_wikidata(titel):
    q = ('https://www.wikidata.org/w/api.php?action=wbgetentities&sites=dewiki&format=json&props=claims&titles='
         + urllib.parse.quote(titel))
    _, s = holen(q)
    for e in json.loads(s)['entities'].values():
        web = [x['mainsnak']['datavalue']['value'] for x in e.get('claims', {}).get('P856', []) if 'datavalue' in x['mainsnak']]
        # amtliche Adresse der Stadt vor Tourismus-Adressen
        web.sort(key=lambda w: (0 if re.search(r'stadt-|gemeinde-|vg-', w) else 1))
        return web[0] if web else None


def main():
    with io.open(os.path.join(RAUM, 'orte.json'), encoding='utf-8') as f:
        conf = json.load(f)
    wahl = set(sys.argv[1:])
    os.makedirs(AUS, exist_ok=True)
    idx_pfad = os.path.join(AUS, 'index.json')
    index = json.load(io.open(idx_pfad, encoding='utf-8')) if os.path.exists(idx_pfad) else {}
    quellen_cfg = conf.get('quellen_amtlich', {})
    for slug, rolle, name, titel, _ in conf['orte']:
        if rolle != 'ziel' or (wahl and slug not in wahl):
            continue
        cfg = dict(quellen_cfg.get(slug, {}))
        if not cfg.get('webseite'):
            cfg['webseite'] = webseite_aus_wikidata(titel)
        t0 = time.time()
        teile, prot = ort_holen(slug, cfg)
        prot['sekunden'] = round(time.time() - t0)
        prot['zeichen'] = sum(len(t) for t in teile)
        index[slug] = prot
        with io.open(os.path.join(AUS, slug + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('ORT: %s\n\n' % name + '\n\n'.join(teile) + '\n')
        n_gem = sum(1 for s in prot['seiten'] if s.get('art') == 'Gemeinde-Webseite')
        n_por = sum(1 for s in prot['seiten'] if s.get('art') == 'Landesportal')
        print('%-20s %2d Gemeinde-Seiten, %d Portal, %6d Zeichen, %3d s %s' % (slug, n_gem, n_por, prot['zeichen'], prot['sekunden'],
              prot.get('fehler_webseite', '')))
    with io.open(idx_pfad, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
