"""2026-10-26: Essener Stadtteile haben keine eigene Webseite, aber je eine Seite auf essen.de
(dasistessen/stadtteile/<ordner>/<name>_startseite.de.jsp) mit Unterseiten Geschichte, Kultur/Freizeit, Statistik.
Das Skript liest jede Startseite, nimmt die Unterseiten im selben Ordner und setzt sie als feste Liste mit "nur_seiten",
damit keine stadtweiten Menü-Seiten dazukommen. Überruhr hat zwei Seiten (Hinsel, Holthausen).
Aufruf: python -X utf8 scripts/data-build/quellen_essen_stadtteile_2026-10-26.py
"""
import json, os, re, time, urllib.parse, urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
B = 'https://www.essen.de/dasistessen/stadtteile/'
UA = {'User-Agent': 'Mozilla/5.0 (LernApp-GemeindeAchsen/0.1; https://github.com/msaxler/lernapp)'}
START = {'360-heisingen': ['heisingen_2/heisingen_startseite.de.jsp'],
         '418-kupferdreh': ['kupferdreh_2/kupferdreh_startseite.de.jsp'],
         '419-ueberruhr': ['ueberruhr_hinsel_/ueberruhr_hinsel_startseite.de.jsp',
                           'ueberruhr_holthausen/ueberruhr_holthausen_startseite.de.jsp'],
         '420-bergerhausen': ['bergerhausen_/bergerhausen_startseite.de.jsp'],
         '421-rellinghausen': ['rellinghausen_1/rellinghausen_startseite.de.jsp'],
         '422-stadtwald-essen': ['stadwald/stadtwald_startseite.de.jsp'],
         '423-fischlaken': ['fischlaken_1/fischlaken_startseite.de.jsp'],
         '424-werden': ['werden_2/werden_startseite.de.jsp'],
         '425-burgaltendorf': ['burgaltendorf_2/burgaltendorf_startseite.de.jsp'],
         '426-steele': ['steele_2/steele_startseite.de.jsp'],
         '427-byfang': ['byfang/byfang_startseite.de.jsp'],
         '428-ruettenscheid': ['ruettenscheid_1/ruettenscheid_startseite.de.jsp'],
         '429-bredeney': ['bredeney_1/bredeney_startseite.de.jsp'],
         '430-huttrop': ['huttrop_2/huttrop_startseite.de.jsp'],
         '431-kettwig': ['kettwig/kettwig_startseite.de.jsp'],
         '490-schuir': ['schuir_1/schuir_startseite.de.jsp'],
         '491-heidhausen': ['heidhausen_1/heidhausen_startseite.de.jsp'],
         '492-haarzopf': ['haarzopf/haarzopf_startseite.de.jsp'],
         '493-margarethenhoehe': ['margarethenhoehe/margarethenhoehe_startseite.de.jsp'],
         '494-suedostviertel': ['suedostviertel_1/suedostviertel_startseite.de.jsp'],
         '495-freisenbruch': ['freisenbruch_2/fischlaken_startseite.de.jsp']}  # Dateiname so auf essen.de

with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
for slug, starts in START.items():
    seiten = []
    for s in starts:
        url = B + s
        h = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode('utf-8', 'replace')
        ordner = url.rsplit('/', 1)[0] + '/'
        seiten.append(url)
        for href in re.findall(r'href="([^"#?]+)"', h):
            u = urllib.parse.urljoin(url, href)
            if u.startswith(ordner) and u not in seiten and re.search(r'\.de\.(html|jsp)$', u):
                seiten.append(u)
        time.sleep(0.5)
    o['quellen_amtlich'][slug] = {'webseite': seiten[0], 'seiten': seiten, 'portal': [], 'nur_seiten': True}
    print('%-22s %2d Seiten: %s' % (slug, len(seiten), ' '.join(u.rsplit('/', 1)[1] for u in seiten[1:])))
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
