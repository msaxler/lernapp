"""2026-10-20: Ihringen, Breisach und Gündlingen bekamen im Lauf Nordwest 0 Gemeinde-Seiten – die Startseiten (komm.one bzw.
Breisacher Portal) tragen ihre Menüs per Skript, der Krabbler findet keine Links. Seiten von Hand gesucht (curl + Link-Suche):
Ihringen unter /unser-ihringen (Gemeindeporträt, Dorfchronik, Ortsteile, Heimatmuseum, Salomonisches Urteil, Daten und Fakten,
Liliental, Kaiserstuhlbad, Weintage); Breisach über stadt.breisach.de + tourismus.breisach.de (Stadtgeschichte, Stadtteile,
Sehenswürdigkeiten); Gündlingen über die Tourismus-Ortsseite + Hallen/Spielplatz der Stadt. Danach Nachlauf nur dieser drei Orte.
Aufruf: python -X utf8 scripts/data-build/quellen_ihringen_breisach_2026-10-20.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
I = 'https://www.ihringen.de'
S, T = 'https://stadt.breisach.de', 'https://tourismus.breisach.de'
Q = {
    '69-ihringen': {'webseite': I + '/unser-ihringen',
                    'seiten': [I + '/unser-ihringen/gemeindeportrait', I + '/unser-ihringen/gemeindeportrait/dorfchronik',
                               I + '/unser-ihringen/gemeindeportrait/ortsteile', I + '/unser-ihringen/gemeindeportrait/heimatmuseum',
                               I + '/unser-ihringen/gemeindeportrait/salomonisches+urteil', I + '/unser-ihringen/daten+und+fakten',
                               I + '/kultur-und-freizeit/liliental', I + '/leben-in-ihringen/oeffentliche+einrichtungen/kaiserstuhlbad',
                               I + '/kultur-und-freizeit/veranstaltungen/ihringer+weintage', I + '/kultur-und-freizeit/sport+_+aktiv/wandern'],
                    'portal': []},
    '70-breisach': {'webseite': S + '/',
                    'seiten': [T + '/vielfalt/stadtgeschichte', T + '/vielfalt/breisacher-stadtteile', S + '/de/kultur/sehenswuerdigkeiten',
                               S + '/de/kultur/sehenswuerdigkeiten/st-stephansmuenster', S + '/de/kultur/sehenswuerdigkeiten/museum_im_rheintor',
                               S + '/de/kultur/sehenswuerdigkeiten/radbrunnen_turm', S + '/de/kultur/sehenswuerdigkeiten/das_blaue_haus'],
                    'portal': []},
    '466-guendlingen': {'webseite': T + '/ort/breisach-guendlingen-82f9a565b5',
                        'seiten': [T + '/ort/breisach-guendlingen-82f9a565b5', T + '/vielfalt/breisacher-stadtteile',
                                   S + '/de/kultur_und_freizeit/hallen/gemeindesaal_guendlingen', S + '/de/kultur/hallen/malteserhalle_guendlingen',
                                   S + '/de/bildung_gesellschaft_und_soziales/spielplaetze/guendlingen',
                                   T + '/attraktion/tante-m-dorfladen-guendlingen-90d948ae91'],
                        'portal': []},
}
with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
o['quellen_amtlich'].update(Q)
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Quellen gesetzt:', list(Q))
