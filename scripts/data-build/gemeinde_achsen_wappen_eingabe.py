"""Gemeinde-Achsen: Eingabedateien für den Wappen-Lauf (prompt-karten-v0.7.txt + prompt-karten-wappen-v0.1.txt).

Je Zielort mit belegter Wappenbegründung (wappen.json, "begruendung": true) eine Datei
data/gemeinde-achsen/<raum>/eingabe-w0.1/<slug>.txt mit ZIELORT (LAGE, ARTIKEL), GRUNDDATEN (nur was der
Steckbrief braucht), PLAN (eine Pflichtkarte, höchstens eine Zusatzkarte), FAHRT und FAKTEN DER WAPPEN-QUELLE
(fakten/<slug>+w.txt, von gemeinde_achsen_fakten.py aus extraktion/<slug>+w.txt).

Aufruf:  python -X utf8 scripts/data-fetch/gemeinde_achsen_wappen.py
         (Extraktion der +w-Quellen als Agent)
         python -X utf8 scripts/data-build/gemeinde_achsen_fakten.py
         python -X utf8 scripts/data-build/gemeinde_achsen_wappen_eingabe.py [slugs]     (GA_RAUM=<raum>)
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemeinde_achsen_karten_eingabe import ITER, grunddaten_text, lies  # noqa: E402

AUS = os.path.join(ITER, 'eingabe-w0.1')
STECKBRIEF = ('einwohner', 'landkreis', 'naechste_grossstadt', 'hoehe_m')


def lage_text(o):
    # wie gemeinde_achsen_karten_eingabe.main(): ein Stadtteil liegt in seiner Stadt, nicht „nördlich von“ ihr
    lage = o['eigenschaften']['lage'][0]['wert']
    if o['einheit'].startswith('Ortsteil'):
        km_text, _, rest = lage.partition(' von ')
        stadt = o['einheit'].split(' von ', 1)[1]
        if rest.split(' (')[0] == stadt:
            return 'Stadtteil von %s, %s der Stadtmitte (Luftlinie)' % (stadt, km_text)
        return 'Stadtteil von %s; %s von %s (Luftlinie)' % (stadt, km_text, rest.split(' (')[0])
    return lage


def main():
    nur = sys.argv[1:]
    with io.open(os.path.join(ITER, 'grunddaten.json'), encoding='utf-8') as f:
        orte = json.load(f)['orte']
    with io.open(os.path.join(ITER, 'wappen.json'), encoding='utf-8') as f:
        wappen = {w['slug']: w for w in json.load(f)}
    ziel = [o for o in orte if o['rolle'] == 'ziel']
    os.makedirs(AUS, exist_ok=True)
    for i, o in enumerate(ziel):
        w = wappen.get(o['slug'])
        if (nur and o['slug'] not in nur) or not w or not w['begruendung']:
            continue
        fakten = os.path.join(ITER, 'fakten', w['datei'])
        if not os.path.exists(fakten):
            sys.exit('fehlt: %s (Extraktion und gemeinde_achsen_fakten.py zuerst)' % fakten)
        stelle = ((i * 3 + 2) % 4) + 1
        teile = ['ZIELORT: %s (%s)' % (o['name'], o['einheit']),
                 'LAGE: ' + lage_text(o),
                 # benannte Fundstellen aus den Abschnittsköpfen der Quelle, damit die Quellenzeile nichts erfinden muss
                 # (w0.1 bekam nur URLs; Horben trug darauf einen erfundenen Titel)
                 'ARTIKEL: WAPPEN-QUELLE, Fundstellen: ' + ' · '.join(re.findall(
                     r'^== Aus (.+?) ==$', lies(os.path.join(ITER, 'quellen', w['datei'])), flags=re.M)), '',
                 'GRUNDDATEN:', grunddaten_text(o, nur=STECKBRIEF), '',
                 'PLAN:',
                 '  Karte 1: Geschichte (Wappen), A, wahre Option an Stelle %d' % stelle,
                 '  Zusatzkarte 2 (nur wenn FAKTEN zu einer anderen Figur eine eigene belegte Herkunft nennen): '
                 'Geschichte (Wappen), A oder B, Lösung an anderer Stelle als bei Karte 1', '',
                 'FAHRT: ' + ', '.join(z['name'] for z in ziel), '',
                 'FAKTEN DER WAPPEN-QUELLE (%s):' % o['name'], lies(fakten), '']
        text = '\n'.join(teile)
        with io.open(os.path.join(AUS, o['slug'] + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text + '\n')
        print('%-18s %6d Zeichen' % (o['slug'], len(text)))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
