"""Gemeinde-Achsen Iteration 1: Eingabedateien für den Karten-Prompt v0.5 bauen.

Je Zielort eine Datei data/gemeinde-achsen/iter1/eingabe-v0.5/<slug>.txt mit den Blöcken, die der
Prompt nennt: ZIELORT, GRUNDDATEN, PLAN, LETZTER_PIN, FAHRT, FAKTEN, SPENDER.
Ein Kartenlauf liest nur prompt-karten-v0.5.txt und diese eine Datei.

Aufruf:  python -X utf8 scripts/data-build/gemeinde_achsen_karten_eingabe.py
"""
import io
import json
import os
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'iter1')
AUS = os.path.join(ITER, 'eingabe-v0.5')

# Zahlen, bei denen verschiedene Werte der Quellen nebeneinander gezeigt werden
MEHRWERTIG = ('hoehe_m', 'flaeche_km2', 'ersterwaehnung')
# Eigenschaften, bei denen nur die führende Quelle gezeigt wird (Altbestand weicht wegen Stand oder Fehlern ab)
NUR_FUEHREND = ('einwohner', 'kfz', 'landkreis', 'bundesland', 'plz')
# Spender für Familie B: drei kleine Extraktionen aus verschiedenen Landschaften, je Ort zwei davon
SPENDER = ['s4-dornstetten', 's10-tengen', 's2-renchen']
# Karte 2 als Leiter statt Spannen
LEITER = ('05-st-peter', '07-kirchzarten')


def de(zahl):
    if isinstance(zahl, float):
        return ('%.2f' % zahl).rstrip('0').rstrip('.').replace('.', ',')
    if isinstance(zahl, int) and abs(zahl) >= 10000:
        return '{:,}'.format(zahl).replace(',', '.')
    return str(zahl)


def zeile(key, liste):
    erster = liste[0]
    w = erster['wert']
    vermerke = []
    if erster.get('hinweis', '').startswith('gilt für die Gemeinde'):
        vermerke.append('GILT FÜR DIE GEMEINDE ' + erster['hinweis'].split('Gemeinde ')[1].split(',')[0].upper())
    if 'Aktualität nicht geprüft' in erster.get('hinweis', ''):
        vermerke.append('AKTUALITÄT NICHT GEPRÜFT')
    if key == 'wahl_btw25':
        text = 'Bundestagswahl 2025, Zweitstimmen: %s; Wahlbeteiligung %s %%' % (
            ', '.join('%s %s %%' % (p, de(a)) for p, a in w['anteile_prozent'].items()), de(w['wahlbeteiligung_prozent']))
    elif key == 'buergermeister':
        text = w['name'] + (' (%s)' % w['partei'] if w.get('partei') else '')
    elif key in ('naechste_grossstadt', 'km_landeshauptstadt'):
        text = '%s, %d km Luftlinie' % (w['name'], w['km'])
    elif key in MEHRWERTIG:
        werte = []
        for e in liste:
            if e['wert'] not in werte:
                werte.append(e['wert'])
        text = ' | '.join(de(x) for x in werte)
        if len(werte) > 1 and (max(werte) - min(werte)) > 0.05 * max(abs(max(werte)), 1):
            vermerke.append('MEHRERE WERTE')
        quellen = []
        for e in liste:
            if e['quelle'] not in quellen:
                quellen.append(e['quelle'])
        return '  %s: %s%s  [%s]' % (key, text, ''.join(' — ' + v for v in vermerke), '; '.join(quellen))
    elif isinstance(w, list):
        text = ', '.join(str(x) for x in w)
    else:
        text = de(w)
    stand = ', Stand %s' % erster['stand'].replace('-00-00', '') if erster.get('stand') else ''
    return '  %s: %s%s  [%s%s]' % (key, text, ''.join(' — ' + v for v in vermerke), erster['quelle'], stand)


def grunddaten_text(ort, nur=None):
    aus = []
    for key, liste in ort['eigenschaften'].items():
        if nur and key not in nur:
            continue
        if key == 'kueste' and liste[0]['wert'] != 'ja':
            continue
        aus.append(zeile(key, liste))
    return '\n'.join(aus)


def plan(i, slug, ortsteil):
    a = lambda k: ((i * 3 + k * 5) % 4) + 1
    b = lambda k: ((i + k) % 3) + 1
    zahl = ('C-LEITER, letzte Stufe mit "höher": %d' % (a(2) % 3 + 1)) if slug in LEITER else 'C, wahre Spanne an Stelle %d' % a(2)
    politik = 'Klassiker Politik (Wahlergebnis%s), A oder C, wahre Option an Stelle %d' % (
        '; die Angabe gilt für die ganze Stadt' if ortsteil else '', a(4))
    return '\n'.join([
        '  Karte 1: Geschichte, A, wahre Option an Stelle %d' % a(1),
        '  Karte 2: Klassiker Zahl (Größe, Höhe, Alter oder Entfernung), %s' % zahl,
        '  Karte 3: Geschichte, B, Lüge an Stelle %d' % b(3),
        '  Karte 4: %s' % politik,
        '  Karte 5: Geschichte, A, wahre Option an Stelle %d' % a(5),
        '  Karte 6: Klassiker Zugehörigkeit oder Lage (Kennzeichen, Landkreis, Bahnhof, Großstadt), A, wahre Option an Stelle %d' % a(6),
        '  Karte 7: Geschichte, A oder B nach deiner Wahl, wahre Option an Stelle %d (bei B: Lüge an Stelle %d)' % (a(7), b(7)),
    ])


def lies(pfad):
    with io.open(pfad, encoding='utf-8') as f:
        return f.read().strip()


def main():
    with io.open(os.path.join(ITER, 'grunddaten.json'), encoding='utf-8') as f:
        orte = json.load(f)['orte']
    ziel = [o for o in orte if o['rolle'] == 'ziel']
    name = {o['slug']: o['name'] for o in orte}
    os.makedirs(AUS, exist_ok=True)
    for i, o in enumerate(ziel):
        teile = ['ZIELORT: %s (%s)' % (o['name'], o['einheit']), '',
                 'GRUNDDATEN:', grunddaten_text(o), '',
                 'PLAN:', plan(i, o['slug'], o['einheit'].startswith('Ortsteil')), '']
        if i > 0:
            v = ziel[i - 1]
            teile += ['LETZTER_PIN: %s (%s)' % (v['name'], v['einheit']),
                      grunddaten_text(v, nur=('einwohner', 'flaeche_km2', 'hoehe_m', 'landkreis', 'kfz', 'ersterwaehnung',
                                              'wahl_btw25', 'naechste_grossstadt', 'bahnhof')), '']
        else:
            teile += ['LETZTER_PIN: keiner (erster Ort der Fahrt)', '']
        teile += ['FAHRT: ' + ', '.join(z['name'] for z in ziel), '',
                  'FAKTEN (Zielort %s):' % o['name'], lies(os.path.join(ITER, 'extraktion', o['slug'] + '.txt')), '']
        for s in (SPENDER[i % 3], SPENDER[(i + 1) % 3]):
            teile += ['SPENDER: %s (nicht Teil der Fahrt)' % name[s], lies(os.path.join(ITER, 'extraktion', s + '.txt')), '']
        text = '\n'.join(teile)
        with io.open(os.path.join(AUS, o['slug'] + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text + '\n')
        print('%-16s %7d Zeichen' % (o['slug'], len(text)))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
