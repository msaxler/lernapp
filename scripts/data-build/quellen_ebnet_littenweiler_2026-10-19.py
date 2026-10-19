"""Quellen für die Freiburger Stadtteile Ebnet (387) und Littenweiler (388) in orte.json eintragen (Ortsporträt, 2026-10-19).
Stadtteile haben keine eigene Gemeinde-Webseite: Ebnet die Ortsverwaltung auf freiburg.de, Littenweiler den Bürgerverein
(nur http, Zertifikat passt nicht); dazu je die LEO-BW-Ortslexikon-Seite als Landesportal (Ortsgeschichte, 11–14 KB).
Aufruf: python -X utf8 scripts/data-build/quellen_ebnet_littenweiler_2026-10-19.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
Q = {
    '387-ebnet': {
        'webseite': 'https://www.freiburg.de/pb/206692.html',
        'seiten': ['https://www.freiburg.de/pb/206692.html', 'https://www.freiburg.de/pb/206696.html',
                   'https://www.freiburg.de/pb/206712.html', 'https://www.freiburg.de/pb/550854.html'],
        'portal': ['https://www.leo-bw.de/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/7710/Ebnet'],
    },
    '388-littenweiler': {
        'webseite': 'http://bv-littenweiler.de/joomla/',
        'seiten': ['http://bv-littenweiler.de/joomla/index.php?option=com_content&view=article&id=9&Itemid=5',
                   'http://bv-littenweiler.de/joomla/index.php?option=com_content&view=article&id=10&Itemid=3'],
        'portal': ['https://www.leo-bw.de/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/7723/Littenweiler'],
    },
}
with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
o['quellen_amtlich'].update(Q)
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('eingetragen:', list(Q))
