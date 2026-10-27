"""2026-10-26: Quellen-Probe Autostrecke Neuwied–Heisingen (ohne Schreiben) ergab:
- Neuwieder Stadtteile (Niederbieber, Segendorf, Oberbieber, Altwied) bekämen über das Menü dieselben 20 stadtweiten
  neuwied.de-Seiten wie Neuwied selbst → nur die eigene Stadtteilseite ("nur_seiten").
- 0 Seiten: Rengsdorf (kurortrengsdorf.de ohne Links), Straßenhaus (orts.app, Skript), Willroth (geparkte Domain),
  Hümmerich (huemmerich-ww.de ist inzwischen eine GLÜCKSSPIEL-Seite – nie als Quelle!) → Ortsgemeinde-Seiten der
  Verbandsgemeinden Rengsdorf-Waldbreitbach bzw. Altenkirchen-Flammersfeld.
- Leverkusen: Startseite nur Bürgerservice-Links → Einstieg „Stadt erleben“. Langenfeld: Menü nur per Skript, bleibt
  ohne Gemeinde-Seiten (Wikipedia und OSM tragen).
Aufruf: python -X utf8 scripts/data-build/quellen_autostrecke_neuwied_essen_2026-10-26.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
NW = 'https://www.neuwied.de/stadtleben/standort/stadtteile/'
RW = 'https://www.rengsdorf-waldbreitbach.de/gemeinden-infrastruktur/gemeinden/'
AF = 'https://www.vg-altenkirchen-flammersfeld.de/gemeinde-politik/uebersicht-ortsgemeinden/'


def fest(*seiten):
    return {'webseite': seiten[0], 'seiten': list(seiten), 'portal': [], 'nur_seiten': True}


Q = {'404-niederbieber': fest(NW + 'niederbieber'),
     '405-segendorf': fest(NW + 'segendorf'),
     '408-oberbieber': fest(NW + 'oberbieber'),
     '497-altwied': fest(NW + 'altwied'),
     '498-rengsdorf': fest(RW + 'rengsdorf/', 'https://www.kurortrengsdorf.de/'),
     '500-strassenhaus': fest(RW + 'strassenhaus/'),
     '504-huemmerich': fest(RW + 'huemmerich/'),
     '502-willroth': fest(AF + 'willroth', 'https://www.vg-altenkirchen-flammersfeld.de/gemeinde-politik/chroniken-der-ortsgemeinden'),
     '193-leverkusen': {'webseite': 'https://www.leverkusen.de/stadt-erleben/', 'seiten': [], 'portal': []}}
with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
o['quellen_amtlich'].update(Q)
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Quellen gesetzt:', len(Q))
