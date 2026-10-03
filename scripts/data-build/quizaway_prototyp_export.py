"""QuizAway Reise-Modus: Vorrat beider Räume für den Fahrt-Prototyp exportieren (apps/quizaway-reise/daten.js).

Liest je Raum vorrat-liste.json (welche Karten im Vorrat sind), die geprüften Fassungen (karten-geprueft/<lauf>/<ort>.md),
die Orts-Anschlüsse des jüngsten Kartenlaufs, Grunddaten (Name, Koordinaten) und kuratierung.json (Reihe des Kartensatzes
für den Tisch = erste Karte je Ort). Schreibt eine JavaScript-Datei (window.QA_DATEN = {...}), damit die Seite auch ohne
Server läuft. Karten, deren Lösung sich nicht lesen lässt, bleiben draußen und werden gemeldet.

Aufruf:  python -X utf8 scripts/data-build/quizaway_prototyp_export.py
"""
import io
import json
import math
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GA = os.path.join(WURZEL, 'data', 'gemeinde-achsen')
ZIEL = os.path.join(WURZEL, 'apps', 'quizaway-reise', 'daten.js')
# Raum: Ordner, Anzeigename, Lauf mit den Orts-Anschlüssen, Lauf der Tisch-Reihe
RAEUME = [('iter1', 'Freiburg und Umland', 'v0.6', 'v0.5'), ('neuwied', 'Rhein und Wied', 'v0.7', 'v0.7'),
          ('bahn', 'Bahn Freiburg–Neuwied (rechte Rheinseite)', 'v0.8', 'v0.8')]
KOPF = {'v0.4': 'Vorschlag'}


def lies(pfad):
    with io.open(pfad, encoding='utf-8') as f:
        return f.read()


def abschnitte(text, kopf):
    teile = re.split(r'^##\s*%s\s*(\d+)\s*$' % kopf, text, flags=re.M)
    return {int(teile[i]): re.split(r'^##\s*(?:ORTS-ANSCHLUSS|NICHT VERWENDET|UNGEREGELT)', teile[i + 1], flags=re.M)[0]
            for i in range(1, len(teile), 2)}


def feld(text, name):
    m = re.search(r'^%s:[ \t]*(.*?)(?=^[A-ZÄÖÜ][A-ZÄÖÜ -]+:|\Z)' % name, text, flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def karte_lesen(text):
    vorn = [z.strip() for z in feld(text, 'VORDERSEITE').split('\n') if z.strip()]
    rueck_ganz = feld(text, 'RÜCKSEITE')
    rueck, _, quelle = rueck_ganz.partition('\nQuelle:')
    if not quelle:
        m = re.search(r'^(.*?)\s*Quelle:\s*(.*)$', rueck_ganz, flags=re.S)
        rueck, quelle = (m.group(1), m.group(2)) if m else (rueck_ganz, '')
    rueck = ' '.join(rueck.split())
    familie = feld(text, 'FAMILIE').split()[0].upper() if feld(text, 'FAMILIE') else '?'
    optionen = [re.sub(r'^\d[.):]?\s+', '', z) for z in vorn[2:] if re.match(r'^\d[.):]?\s', z)]
    frage = ' '.join(z for z in vorn[2:] if not re.match(r'^\d[.):]?\s', z))
    # Leiter: "Höher bis Stufe N" ist die Formel; Kartenläufe schreiben je nach Frage auch "Größer/Mehr/Älter bis Stufe N"
    m = re.search(r'(Richtig war|Die Lüge war|(?:Höher|Größer|Mehr|Älter) bis Stufe)\s*(\d)', rueck)
    if not m:
        return None
    art = 'leiter' if m.group(1).endswith('bis Stufe') else {'Richtig war': 'richtig', 'Die Lüge war': 'luege'}[m.group(1)]
    if 'LEITER' in familie:
        art = 'leiter'
    return {'familie': 'Leiter' if art == 'leiter' else familie, 'sorte': (feld(text, 'SORTE').split() or ['Geschichte'])[0],
            'ort': vorn[0], 'steckbrief': vorn[1] if len(vorn) > 1 else '', 'frage': frage, 'optionen': optionen,
            'art': art, 'loesung': int(m.group(2)), 'rueckseite': rueck,
            'quelle': ' '.join(quelle.split()).replace('Quelle: ', ''),
            'faktencheck': (feld(text, 'FAKTENCHECK').split(' – ')[0] or 'ungeprüft').strip()}


def km(a, b):
    p1, p2 = math.radians(a['lat']), math.radians(b['lat'])
    d = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b['lon'] - a['lon']) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(d))


def main():
    daten, fehler = {'stand': '', 'raeume': []}, []
    for ordner, anzeige, lauf_anschluss, lauf_reihe in RAEUME:
        iter_ = os.path.join(GA, ordner)
        grund = {o['slug']: o for o in json.loads(lies(os.path.join(iter_, 'grunddaten.json')))['orte'] if o['rolle'] == 'ziel'}
        vorrat = json.loads(lies(os.path.join(iter_, 'vorrat-liste.json')))
        kur = json.loads(lies(os.path.join(iter_, 'kuratierung.json')))
        reihe = kur.get('kartensatz', {}).get('reihe', {})
        pfad_b = os.path.join(iter_, 'anschluss-berichtigt.json')
        berichtigt = json.loads(lies(pfad_b)) if os.path.exists(pfad_b) else {}
        orte, vorher = [], None
        # Reihenfolge der Fahrt: orte.json, wo es sie gibt (Raum bahn: Nummern 01–10 Messorte, 11–29 Ausbau), sonst Slug
        pfad_o = os.path.join(iter_, 'orte.json')
        reihe_orte = [o[0] for o in json.loads(lies(pfad_o))['orte'] if o[0] in grund] if os.path.exists(pfad_o) else sorted(grund)
        # nur Orte mit Karten im Vorrat (im Raum bahn laufen die Ausbau-Orte noch)
        reihe_orte = [s for s in reihe_orte if any(x['ort'] == s for x in vorrat)]
        for slug in reihe_orte:
            g = grund[slug]
            karten = []
            for v in [x for x in vorrat if x['ort'] == slug]:
                pfad = os.path.join(iter_, 'karten-geprueft', v['lauf'], slug + '.md')
                k = karte_lesen(abschnitte(lies(pfad), KOPF.get(v['lauf'], 'Karte'))[v['karte']])
                if not k:
                    fehler.append('%s %s %s %d: Lösung nicht lesbar' % (ordner, slug, v['lauf'], v['karte']))
                    continue
                k['id'] = '%s/%s/%d' % (slug, v['lauf'], v['karte'])
                k['tisch'] = (v['lauf'] == lauf_reihe and reihe.get(slug) == v['karte'])
                karten.append(k)
            anschluss = []
            pfad = os.path.join(iter_, 'karten-geprueft', lauf_anschluss, slug + '.md')
            if os.path.exists(pfad):
                m = re.search(r'^## ORTS-ANSCHLUSS\s*\n(.*?)(?=^## |\Z)', lies(pfad), flags=re.S | re.M)
                if m:
                    anschluss = [z.strip(' -') for z in m.group(1).strip().split('\n') if z.strip() and not z.lower().startswith('keiner')]
            # Der Anschluss des Kartenlaufs gilt nur für den Vorgänger, den seine Eingabe als LETZTER_PIN hatte; ist auf
            # der Fahrt ein anderer Ort davor (Raum bahn nach dem Ausbau), entfällt er
            pfad_e = os.path.join(iter_, 'eingabe-' + lauf_anschluss, slug + '.txt')
            if anschluss and vorher and os.path.exists(pfad_e):
                m = re.search(r'^LETZTER_PIN:\s*(.*?)\s*\(', lies(pfad_e), flags=re.M)
                if m and m.group(1) != grund[vorher]['name']:
                    anschluss = []
            # berichtigte Fassung (Alltagssprache, beide Orte beim Namen; Mike 2026-10-03) geht vor; mit "von" nur für
            # genau diesen Vorgänger
            b = berichtigt.get(slug)
            if isinstance(b, dict):
                anschluss = b['zeilen'] if b.get('von') == vorher else []
            elif b:
                anschluss = b
            # der Prüfvermerk „(Namensteil)“ ist für den Faktencheck, nicht für den Bildschirm
            anschluss = [re.sub(r'\s*\(Namensteil\)\s*$', '', z) for z in anschluss]
            ort = {'slug': slug, 'name': g['name'], 'lat': g['lat'], 'lon': g['lon'], 'karten': karten,
                   'anschluss_von': vorher, 'anschluss': anschluss}
            if vorher:
                ort['km_vom_vorigen'] = round(km(grund[vorher], g), 1)
            orte.append(ort)
            vorher = slug
        daten['raeume'].append({'id': ordner, 'name': anzeige, 'orte': orte})
        print('%-8s %2d Orte, %3d Karten, Tisch-Reihe %d' % (ordner, len(orte), sum(len(o['karten']) for o in orte),
                                                            sum(1 for o in orte for k in o['karten'] if k['tisch'])))
    os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
    with io.open(ZIEL, 'w', encoding='utf-8', newline='\n') as f:
        f.write('// Erzeugt von scripts/data-build/quizaway_prototyp_export.py – nicht von Hand ändern.\n')
        f.write('window.QA_DATEN = ' + json.dumps(daten, ensure_ascii=False, indent=0) + ';\n')
    print('geschrieben:', ZIEL, os.path.getsize(ZIEL), 'Bytes')
    for f in fehler:
        print('  -', f)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
