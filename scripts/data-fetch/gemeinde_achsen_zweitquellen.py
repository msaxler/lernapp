"""Gemeinde-Achsen Iteration 1: zweite Quelle für Orte mit dünnem Artikel holen.

Entscheid Mike 2026-10-02: Liegt der Ortsartikel unter 1.000 Wörtern, werden die im Ortsartikel verlinkten
Artikel mitgelesen, die den Ortsnamen im Titel tragen (Burg, Kloster, Geschlecht). Für jeden solchen Artikel:
Klartext nach data/gemeinde-achsen/iter1/quellen/<slug>+<n>.txt; Übersicht in zweitquellen.json.
Die Extraktion (Schicht 1) läuft danach wie beim Ortsartikel mit prompt-stufe1-v0.5.1.txt.

Aufruf:  python -X utf8 scripts/data-fetch/gemeinde_achsen_zweitquellen.py
"""
import datetime
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemeinde_achsen_quellen import tabellentext  # noqa: E402

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
UA = {'User-Agent': 'LernApp-GemeindeAchsen/0.1 (https://github.com/msaxler/lernapp)'}
GRENZE_WOERTER = 1000
HOECHSTENS = 3  # verlinkte Artikel je Ort


def hole(parameter):
    url = 'https://de.wikipedia.org/w/api.php?' + urllib.parse.urlencode(dict(parameter, format='json'))
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.loads(r.read().decode('utf-8'))


def links(titel):
    aus, weiter = [], {}
    while True:
        d = hole(dict({'action': 'query', 'titles': titel, 'prop': 'links', 'plnamespace': 0, 'pllimit': 'max', 'redirects': 1}, **weiter))
        for seite in d['query']['pages'].values():
            aus += [l['title'] for l in seite.get('links', [])]
        if 'continue' not in d:
            return aus
        weiter = d['continue']


def artikel(titel):
    d = hole({'action': 'query', 'redirects': 1, 'titles': titel, 'prop': 'extracts|info|pageprops', 'explaintext': 1,
              'exsectionformat': 'wiki', 'inprop': 'url', 'ppprop': 'disambiguation'})
    return next(iter(d['query']['pages'].values()))


def main():
    with io.open(os.path.join(ITER, 'schicht0.json'), encoding='utf-8') as f:
        orte = json.load(f)
    heute = datetime.date.today().isoformat()
    uebersicht = []
    # Mit Slugs als Argument nur diese Orte (Ort nachziehen); die übrigen Einträge bleiben
    nur = sys.argv[1:]
    if nur and os.path.exists(os.path.join(ITER, 'zweitquellen.json')):
        with io.open(os.path.join(ITER, 'zweitquellen.json'), encoding='utf-8') as f:
            uebersicht = [z for z in json.load(f) if z['slug'] not in nur]
    for o in orte:
        if o['rolle'] != 'ziel' or o['woerter'] >= GRENZE_WOERTER or (nur and o['slug'] not in nur):
            continue
        stamm = o['name'][:max(5, len(o['name']) - 2)]  # „Zähring“ trifft Zähringer und Burg Zähringen
        kandidaten = [t for t in links(o['dewiki']) if stamm.lower() in t.lower() and t != o['dewiki']]
        print('%s (%d Wörter): Kandidaten %s' % (o['name'], o['woerter'], kandidaten))
        n = 0
        for titel in kandidaten:
            if n >= HOECHSTENS:
                break
            s = artikel(titel)
            text = s.get('extract', '')
            if 'disambiguation' in s.get('pageprops', {}) or len(text.split()) < 150:
                print('   übersprungen:', titel)
                continue
            n += 1
            datei = '%s+%d.txt' % (o['slug'], n)
            tab = tabellentext(s.get('title', titel))  # der Auszug lässt Tabellen weg (Bericht Neuwied N14)
            kopf = ('# Quelle: %s\n# Titel: %s\n# Abruf: %s\n# Lizenz: Wikipedia, CC BY-SA 4.0\n# Zweite Quelle zu: %s\n'
                    '# Tabellen: %d Wörter, am Ende angehängt\n\n'
                    % (s.get('fullurl', ''), s.get('title', titel), heute, o['dewiki'], len(tab.split())))
            with io.open(os.path.join(ITER, 'quellen', datei), 'w', encoding='utf-8', newline='\n') as f:
                f.write(kopf + text + ('\n\n\n== Aus Tabellen des Artikels ==\n\n' + tab if tab else '') + '\n')
            uebersicht.append({'slug': o['slug'], 'ort': o['name'], 'datei': datei, 'titel': s.get('title', titel),
                               'url': s.get('fullurl', ''), 'woerter': len(text.split()), 'abruf': heute})
            print('   %s: %s, %d Wörter' % (datei, s.get('title', titel), len(text.split())))
            time.sleep(1)
    with io.open(os.path.join(ITER, 'zweitquellen.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(uebersicht, f, ensure_ascii=False, indent=1)
    print('fertig:', len(uebersicht), 'Artikel')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
