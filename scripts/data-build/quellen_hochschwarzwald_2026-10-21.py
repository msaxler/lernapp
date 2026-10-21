"""2026-10-21: St. Peter, Feldberg, Lenzkirch, Eisenbach bekamen im Lauf Hochschwarzwald 0 Gemeinde-Seiten. Ursache: die
Wikidata-Adressen sind Landing-Pages des Hochschwarzwald-Tourismus-Verbunds (5–6 KB, nur Logo-Links); die eigentlichen
Gemeindeseiten liegen dahinter (st-peter.eu, feldberg.org/start, lenzkirch.de/index.php, eisenbach.de/pb/…). hochschwarzwald.de
selbst sperrt (403). Seiten von Hand per curl-Linksuche; danach Nachlauf der vier Orte.
Aufruf: python -X utf8 scripts/data-build/quellen_hochschwarzwald_2026-10-21.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
P, F, L, E = 'http://www.st-peter.eu', 'https://feldberg.org', 'https://www.lenzkirch.de', 'https://www.eisenbach.de/pb/'
Q = {
    '483-sankt-peter': {'webseite': P + '/unser-dorf.html',
                        'seiten': [P + '/unser-dorf/geschichte.html', P + '/unser-dorf/kultur/ortschronik.html',
                                   P + '/unser-dorf/ehemaliges-benediktiner-kloster.html', P + '/unser-dorf/historischer-dorfrundgang.html',
                                   P + '/unser-dorf/kultur/brauchtum-in-st-peter.html', P + '/unser-dorf/kultur/filmdorf-st-peter.html',
                                   P + '/unser-dorf/kultur/st-peter-zentrum-der-musik-im-hochschwarzwald.html', P + '/bioenergiedorf.html',
                                   P + '/aktivitaeten/hallenbad-st-peter.html', P + '/sehenswuerdigkeiten.html', P + '/unser-dorf/kultur-soziales-und-bildung/kirchen.html'],
                        'portal': []},
    '485-feldberg': {'webseite': F + '/start',
                     'seiten': [F + '/leben-in', F + '/leben-in/feldbergturm', F + '/leben-in/feldbergbahn', F + '/leben-in/feldberghalle',
                                F + '/leben-in/kunst+in+feldberg', F + '/leben-in/kunst+in+feldberg/kunst+am+bach', F + '/leben-in/grillplaetze',
                                F + '/leben-in/infrastruktur/erneuerbare+energien', F + '/leben-in/infrastruktur/oeffentlicher+nahverkehr',
                                F + '/leben-in/kirche+_+glaube', F + '/leben-in/vereine', F + '/service-bieten/grusswort'],
                     'portal': []},
    '487-lenzkirch': {'webseite': L + '/index.php',
                      'seiten': [L + '/unsere-gemeinde/ueber-lenzkirch/geschichte', L + '/unsere-gemeinde/ueber-lenzkirch/daten-fakten',
                                 L + '/unsere-gemeinde/ueber-lenzkirch/staedtepartnerschaft', L + '/leben-in-lenzkirch/sport-/-freizeit/schwimmbaeder',
                                 L + '/leben-in-lenzkirch/sport-/-freizeit/wintersport', L + '/leben-in-lenzkirch/sport-/-freizeit/sportstaetten',
                                 L + '/leben-in-lenzkirch/sport-/-freizeit/unsere-vereine', L + '/leben-in-lenzkirch/veranstaltungen-/-maerkte/wochenmarkt-lenzkirch-und-ortsteile',
                                 L + '/unsere-gemeinde/raumvermietung/kursaal-lenzkirch', L + '/unsere-gemeinde/raumvermietung/haus-des-gastes-saig'],
                      'portal': []},
    '488-eisenbach': {'webseite': E + '374918.html',
                      'seiten': [E + '374918.html', E + '3896891.html', E + '3896915.html', E + '3897299.html', E + '3897323.html',
                                 E + '3897251.html', E + '3897275.html', E + '3897155.html', E + '3897179.html', E + '3965547.html',
                                 E + '3897059.html', E + '3897071.html'],
                      'portal': []},
}
with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
o['quellen_amtlich'].update(Q)
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Quellen gesetzt:', list(Q))
