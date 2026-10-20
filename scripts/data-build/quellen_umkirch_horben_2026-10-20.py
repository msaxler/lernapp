"""Quellen für Umkirch (437) und Horben (435) von Hand in orte.json (Ortsporträt, 2026-10-20): beide Gemeinde-Webseiten haben
Skript-Menüs, die der Krabbler nicht sieht (Umkirch 0 Seiten, Horben 2). Seiten per Suche gefunden; dazu LEO-BW (Gemeinde +
Altgemeinde) als Landesportal. Aufruf: python -X utf8 scripts/data-build/quellen_umkirch_horben_2026-10-20.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
Q = {
    '437-umkirch': {
        'webseite': 'https://www.umkirch.de/',
        'seiten': ['https://www.umkirch.de/Leben-in-Umkirch/Historisches', 'https://www.umkirch.de/Leben-in-Umkirch/Das-ist-Umkirch',
                   'https://www.umkirch.de/Leben-in-Umkirch/Kultur-Freizeit/Heimatmuseum', 'https://www.umkirch.de/Leben-in-Umkirch/Freizeit',
                   'https://www.umkirch.de/Wirtschaft',
                   'https://rundgang.umkirch.de/rundwege/gemeinde-umkirch/pois/schloss-bueningen',
                   'https://rundgang.umkirch.de/pois-en/die-schlossmuehle-umkircher-museum', 'https://rundgang.umkirch.de/pois-en/das-roemische-an-umkirch'],
        'portal': ['https://www.leo-bw.de/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/9416/Umkirch',
                   'https://www.leo-bw.de/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/9413/Umkirch'],
    },
    '435-horben': {
        'webseite': 'https://www.horben.de/',
        'seiten': ['https://gemeinde.horben.de/eip/pages/historie-fakten-ueber-horben.php', 'https://www.horben.de/eip/pages/schauinslandbahn.php',
                   'https://www.horben.de/eip/pages/wandern.php', 'https://gemeinde.horben.de/'],
        'portal': ['https://www.leo-bw.de/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/8504/Horben',
                   'https://www.leo-bw.de/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/8502/Horben'],
    },
}
with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
o['quellen_amtlich'].update(Q)
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('eingetragen:', list(Q))
