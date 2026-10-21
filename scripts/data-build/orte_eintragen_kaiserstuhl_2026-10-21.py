"""Mike 2026-10-21: „du kannst noch den Rest Kaiserstuhl rechnen“. Neu im Raum bahn: Sasbach, Wyhl, Forchheim (Gemeinden am
Nordrand) und die Ortsteile mit eigenem Wikipedia-Artikel: Vogtsburgs Winzerdörfer Oberrotweil, Achkarren, Burkheim,
Bischoffingen, Bickensohl, Oberbergen, Schelingen; Leiselheim (Sasbach); Nieder- und Oberrimsingen (Breisach, Tuniberg).
Ohne eigenen Artikel (bleiben im Gemeinde-Porträt): Jechtingen → Sasbach; Königschaffhausen, Kiechlinsbergen, Amoltern →
Endingen. Bahlingen, Riegel, Endingen (401–403) werden nur neu gerechnet. Nicht Kaiserstuhl, nicht dabei: Teningen-/Emmendingen-
Ortsteile, Sexau, Malterdingen, Weisweil. Einheit der Ortsteile = Wikidata-Label der Gemeinde (grunddaten sucht das Label).
Aufruf: python -X utf8 scripts/data-build/orte_eintragen_kaiserstuhl_2026-10-21.py
"""
import json, os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PFAD = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'orte.json')
V, SA, B = 'Ortsteil von Vogtsburg im Kaiserstuhl', 'Ortsteil von Sasbach am Kaiserstuhl', 'Ortsteil von Breisach am Rhein'
T = 'https://tourismus.breisach.de'
# slug, Name, Wikipedia-Titel, Einheit, Anker (eingefügt danach, in dieser Reihenfolge)
NEU = [('472-oberrotweil', 'Oberrotweil', 'Oberrotweil', V, '467-vogtsburg'),
       ('473-achkarren', 'Achkarren', 'Achkarren', V, '472-oberrotweil'),
       ('474-burkheim', 'Burkheim', 'Burkheim am Kaiserstuhl', V, '473-achkarren'),
       ('475-bischoffingen', 'Bischoffingen', 'Bischoffingen', V, '474-burkheim'),
       ('476-bickensohl', 'Bickensohl', 'Bickensohl', V, '475-bischoffingen'),
       ('477-oberbergen', 'Oberbergen', 'Oberbergen (Vogtsburg im Kaiserstuhl)', V, '476-bickensohl'),
       ('478-schelingen', 'Schelingen', 'Schelingen', V, '477-oberbergen'),
       ('469-sasbach', 'Sasbach', 'Sasbach am Kaiserstuhl', 'Gemeinde', '478-schelingen'),
       ('479-leiselheim', 'Leiselheim', 'Leiselheim', SA, '469-sasbach'),
       ('470-wyhl', 'Wyhl', 'Wyhl am Kaiserstuhl', 'Gemeinde', '479-leiselheim'),
       ('471-forchheim-kaiserstuhl', 'Forchheim', 'Forchheim (Kaiserstuhl)', 'Gemeinde', '470-wyhl'),
       ('480-niederrimsingen', 'Niederrimsingen', 'Niederrimsingen', B, '466-guendlingen'),
       ('481-oberrimsingen', 'Oberrimsingen', 'Oberrimsingen', B, '480-niederrimsingen')]
Q = {s: {'webseite': 'https://www.vogtsburg.de/', 'seiten': [], 'portal': []}
     for s in ('472-oberrotweil', '473-achkarren', '474-burkheim', '475-bischoffingen', '476-bickensohl', '477-oberbergen', '478-schelingen')}
Q['479-leiselheim'] = {'webseite': 'https://www.sasbach.de/', 'seiten': [], 'portal': []}
Q['470-wyhl'] = {'webseite': 'https://www.wyhl.de/', 'seiten': ['https://www.wyhl.de/seite/492997/geschichte.html'], 'portal': []}
Q['480-niederrimsingen'] = {'webseite': T + '/ort/breisach-niederrimsingen-66b4fa7ade',
                            'seiten': [T + '/ort/breisach-niederrimsingen-66b4fa7ade', T + '/vielfalt/breisacher-stadtteile',
                                       'https://stadt.breisach.de/de/kultur_und_freizeit/hallen/attila-halle_niederrimsingen',
                                       T + '/tour/niederrimsingen-gottenheim-burgunderpfad-8e372fe062'], 'portal': []}
Q['481-oberrimsingen'] = {'webseite': T + '/ort/breisach-oberrimsingen-mit-grezhausen-6bd33b3f0c',
                          'seiten': [T + '/ort/breisach-oberrimsingen-mit-grezhausen-6bd33b3f0c', T + '/vielfalt/breisacher-stadtteile',
                                     T + '/attraktion/schloss-rimsingen-41e8f532bb', 'https://stadt.breisach.de/de/kultur/sehenswuerdigkeiten/schloss_rimsingen',
                                     'https://stadt.breisach.de/de/kultur_und_freizeit/hallen/tuniberghalle_oberrimsingen'], 'portal': []}
with open(PFAD, encoding='utf-8') as f:
    o = json.load(f)
orte = o['orte']
vorhanden = {e[0] for e in orte}
for slug, name, titel, einheit, anker in NEU:
    if slug in vorhanden:
        print('schon da:', slug); continue
    i = next(i for i, e in enumerate(orte) if e[0] == anker)
    orte.insert(i + 1, [slug, 'ziel', name, titel, einheit])
    o['laender'][slug] = 'BW'
o['quellen_amtlich'].update(Q)
o['_doc'] += ' Rest Kaiserstuhl (Mike 2026-10-21): Sasbach, Wyhl, Forchheim, Vogtsburgs 7 Winzerdörfer, Leiselheim, Nieder-/Oberrimsingen (469–481); Jechtingen und Endingens Ortsteile ohne Artikel bleiben in der Gemeinde.'
with open(PFAD, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(o, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Orte:', len(orte), '|', [e[0] for e in orte if e[0][:3] in ('467', '469', '470', '471', '472', '478', '479', '466', '480', '481')])
