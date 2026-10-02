"""Gemeinde-Achsen: Ausreißer-Karten aus der Bundestagswahl 2025 (Lauf a0.1; Spielkonzept v0.2.8 §8 Nr. 7).

Mike, 2026-10-03: Die Ausreißer-Karte bleibt („wegen ihrer Relevanz“), Form A zuerst; hat ein Ort einen Ausreißer,
steht die Karte in seinem Vorrat. Schwellen (von Mike bestätigt):
  (a) Wahlkreis: andere stärkste Partei (Zweitstimmen) als das Land, und höchstens drei Wahlkreise des Landes
      haben dieselbe stärkste Partei. Die Karte steht im Vorrat jedes Orts des Wahlkreises auf der Fahrt.
  (b) Ort gegen Kreis: ein Parteianteil weicht um mindestens acht Prozentpunkte vom Kreis ab; gefragt wird, bei welcher
      Partei die Abweichung am größten ist, deshalb muss sie mindestens 1,5 Punkte vor der nächsten liegen.
Nur Gesamtergebnisse, Urne und Brief (Mike, 2026-10-03): Zählt die Verbandsgemeinde die Briefwahl, trägt der Ort keine
Karte nach (b). Ein Stadtteil nimmt sein Ergebnis aus den Grunddaten (Stadtbezirk bzw. Stimmbezirke); „nur ungefähr“
trägt keine Karte.

Die Karten schreibt dieses Skript selbst aus den Zahlen (Klassiker, kein Kartenlauf); geprüft werden sie unabhängig
von check/gemeinde_achsen_ausreisser_pruefen.py. Ausgabe: <raum>/karten-a0.1/<slug>.md (nur Orte mit Karte) und
<raum>/ausreisser.json.

Aufruf:  python -X utf8 scripts/data-build/gemeinde_achsen_ausreisser.py      (GA_RAUM=<raum>)
"""
import csv
import io
import json
import os
import re
import sys
import zipfile

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
WBZ = os.path.join(WURZEL, 'data', 'raw', 'btw25_wbz.zip')
AUS = os.path.join(ITER, 'karten-a0.1')
QUELLE = 'Quelle: Die Bundeswahlleiterin, Wahlbezirksstatistik Bundestagswahl 2025 (Stand 23.02.2025)'
SCHWELLE_B, ABSTAND_B, HOECHSTENS_A = 8.0, 1.5, 3
HAUPT = ['CDU', 'AfD', 'SPD', 'GRÜNE', 'Die Linke']
# Nominativ, Dativ, Plural (für das Verb)
NAME = {'CDU': ('die CDU', 'der CDU', False), 'AfD': ('die AfD', 'der AfD', False), 'SPD': ('die SPD', 'der SPD', False),
        'GRÜNE': ('die Grünen', 'den Grünen', True), 'Die Linke': ('die Linke', 'der Linken', False),
        'FDP': ('die FDP', 'der FDP', False), 'BSW': ('das BSW', 'dem BSW', False)}


def gross(s):
    return s[0].upper() + s[1:]


def de(x):
    return ('%.1f' % x).replace('.', ',')


def laden():
    z = zipfile.ZipFile(WBZ)
    zeilen = list(csv.reader(io.StringIO(z.read('btw25_wbz_ergebnisse.csv').decode('utf-8-sig')), delimiter=';'))
    kopf = zeilen[4]
    ix = {k: i for i, k in enumerate(kopf)}
    zw = [(k[:-len(' - Zweitstimmen')], i) for i, k in enumerate(kopf) if k.endswith(' - Zweitstimmen') and not k.startswith(('Ungültige', 'Gültige'))]
    er = [(k[:-len(' - Erststimmen')], i) for i, k in enumerate(kopf) if k.endswith(' - Erststimmen') and not k.startswith(('Ungültige', 'Gültige'))]
    zahl = lambda x: int(x) if x.strip().isdigit() else 0
    summe, erst, wk_von, land_von, fremd = {}, {}, {}, {}, set()
    for r in zeilen[5:]:
        if len(r) < len(kopf) or not r[ix['Land']].isdigit():
            continue
        land = r[ix['Land']]
        kreis = land + r[ix['Regierungsbezirk']] + r[ix['Kreis']]
        ags = kreis + r[ix['Gemeinde']]
        wk = r[ix['Wahlkreis']]
        wk_von.setdefault(ags, wk)
        land_von[wk] = land
        if r[ix['Kennziffer Briefwahlzugehörigkeit']].strip() not in ('', '00'):
            fremd.add(ags)
        for s in ('L' + land, 'K' + kreis, 'G' + ags, 'W' + wk):
            d = summe.setdefault(s, {})
            for p, i in zw:
                d[p] = d.get(p, 0) + zahl(r[i])
        e = erst.setdefault(wk, {})
        for p, i in er:
            e[p] = e.get(p, 0) + zahl(r[i])
    namen = {}
    for l in z.read('btw25_wbz_leitband.csv').decode('utf-8-sig').split('\n'):
        p = l.split(';')
        if len(p) > 8 and p[0] in ('10', '30', '40'):
            schl = {'10': 'L' + p[2], '30': 'W' + p[1], '40': 'K' + p[2] + p[3] + p[4]}[p[0]]
            namen[schl] = re.sub(r' \(Wkr\. [^)]*\)$', '', p[8]).strip()
    return summe, erst, wk_von, land_von, fremd, namen


def anteile(d):
    g = sum(d.values())
    return {p: 100.0 * v / g for p, v in d.items()} if g else {}


def erster(d):
    return max(d, key=d.get)


def im_kreis(name):
    if name.endswith(', Stadtkreis'):
        return 'in der Stadt ' + name[:-len(', Stadtkreis')]
    if name.endswith(', Stadt') or name.endswith(', kreisfreie Stadt'):
        return 'in der Stadt ' + name.split(',')[0]
    return 'im Landkreis ' + name


def steckbrief(o):
    e = o['eigenschaften']
    ew = int(round(e['einwohner'][0]['wert'], -2))
    lage = e['lage'][0]['wert'].split(' (')[0]
    if o['einheit'].startswith('Ortsteil'):
        stadt = o['einheit'].split(' von ', 1)[1]
        km, _, rest = lage.partition(' von ')
        ort_lage = '%s der Stadtmitte' % km if rest == stadt else '%s von %s' % (km, rest)
        return 'Stadtteil von %s mit rund %s Einwohnern, %s.' % (stadt, '{:,}'.format(ew).replace(',', '.'), ort_lage)
    art = 'Stadt' if o['einheit'] == 'Stadt' else 'Gemeinde'
    return '%s mit rund %s Einwohnern, %s.' % (art, '{:,}'.format(ew).replace(',', '.'), lage)


def stelle(i, k):
    return ((i * 3 + k * 5) % 4) + 1


def karte(nr, fakt_id, gewaehlt, vorn, optionen, wahr, rueck, nachweise, hinweis):
    opts = list(optionen)
    zeilen = ['## Karte %d' % nr, 'SORTE: Klassiker', 'FAMILIE: A', 'FAKT-ID: GRUNDDATEN.%s' % fakt_id,
              'GEWÄHLTER FAKT: GRUNDDATEN %s: %s' % (fakt_id, gewaehlt),
              'BEKANNTHEIT: niedrig. Wahlergebnisse einzelner Orte und Wahlkreise kennt kaum jemand.',
              'VORDERSEITE:'] + vorn + ['%d. %s' % (j + 1, gross(NAME[p][0])) for j, p in enumerate(opts)]
    rueck = rueck + ' Richtig war %d.' % (opts.index(wahr) + 1)
    zeilen += ['RÜCKSEITE:', rueck, QUELLE, 'WÖRTER RÜCKSEITE: %d' % len(rueck.split()), 'NEGATIVNACHWEISE:']
    zeilen += ['%d: Weg (a). %s' % (opts.index(p) + 1, t) for p, t in nachweise]
    zeilen += ['PRÜFHINWEIS: %s' % hinweis, '']
    return '\n'.join(zeilen)


def setze(wahr, andere, pos):
    opts = [p for p in andere if p != wahr][:3]
    opts.insert(pos - 1, wahr)
    return opts


def main():
    summe, erst, wk_von, land_von, fremd, namen = laden()
    with io.open(os.path.join(ITER, 'grunddaten.json'), encoding='utf-8') as f:
        orte = [o for o in json.load(f)['orte'] if o['rolle'] == 'ziel']
    os.makedirs(AUS, exist_ok=True)
    uebersicht = []
    for i, o in enumerate(orte):
        ags = o['gemeindeschluessel'][:8]
        kreis, land, wk = ags[:5], ags[:2], wk_von[ags]
        karten, eintrag = [], {'slug': o['slug'], 'ort': o['name'], 'wahlkreis': wk, 'karten': []}
        # (a) Wahlkreis gegen Land
        w, l = anteile(summe['W' + wk]), anteile(summe['L' + land])
        p = erster(w)
        gleich = sorted(x for x in land_von if land_von[x] == land and erster(summe['W' + x]) == p)
        if p != erster(l) and len(gleich) <= HOECHSTENS_A:
            weitere = [x for x in gleich if x != wk]
            zweite = sorted(w, key=w.get, reverse=True)[1]
            bund = sum(1 for x in land_von if erster(summe['W' + x]) == p)
            ep = erster(erst[wk])
            nie = [q for q in HAUPT if q not in (p, erster(l)) and not any(erster(summe['W' + x]) == q for x in land_von if land_von[x] == land)]
            if len(nie) >= 3:
                pos = stelle(i, 1)
                opts = setze(p, nie, pos)
                wname, lname = namen['W' + wk], namen['L' + land]
                nur = {0: 'die sonst in %s in keinem Wahlkreis vorn lag' % lname,
                       1: 'die das in %s nur in einem weiteren Wahlkreis schaffte' % lname}.get(
                    len(weitere), 'die das in %s nur in %d weiteren Wahlkreisen schaffte' % (lname, len(weitere)))
                frage = 'Bundestagswahl 2025: Im Wahlkreis %s lag bei den Zweitstimmen eine Partei vorn, %s. Welche?' % (wname, nur)
                vorn = [o['name'], steckbrief(o)[:-1] + '; gehört zum Wahlkreis %s.' % wname, frage]
                plural = NAME[p][2]
                sonst = ('Sonst %s %s im Land nur in %s vorn, bundesweit in %d von 299 Wahlkreisen.' % (
                    'lagen' if plural else 'lag', 'sie', ' und '.join(namen['W' + x] for x in weitere), bund)) if weitere else (
                    'Im Land %s %s sonst nirgends vorn, bundesweit in %d von 299 Wahlkreisen.' % ('lagen' if plural else 'lag', 'sie', bund))
                alle = [x for x in land_von if land_von[x] == land]
                sieger = erster(l)
                land_satz = 'Im Land lag in %d von %d Wahlkreisen %s vorn.' % (
                    sum(1 for x in alle if erster(summe['W' + x]) == sieger), len(alle), NAME[sieger][0])
                rueck = ('Du hattest [Option] getippt. %s Hier %s %s vorn, mit %s Prozent vor %s mit %s. %s Bei den Erststimmen %s dort %s vorn.' % (
                    land_satz, 'lagen' if plural else 'lag', NAME[p][0], de(w[p]), NAME[zweite][1], de(w[zweite]), sonst,
                    'lagen' if NAME[ep][2] else 'lag', NAME[ep][0]))
                nachweise = [(q, 'In %s lag %s in keinem der %d Wahlkreise bei den Zweitstimmen vorn.' % (lname, NAME[q][0],
                              sum(1 for x in land_von if land_von[x] == land))) for q in opts if q != p]
                gewaehlt = 'Wahlkreis %s (%s), Zweitstimmen: %s vorn mit %s %% (Land: %s vorn); Wahlkreise des Landes mit %s vorn: %s; bundesweit %d' % (
                    wk, wname, p, de(w[p]), erster(l), p, ', '.join(gleich), bund)
                karten.append(('ausreisser_wahlkreis', gewaehlt, vorn, opts, p, rueck, nachweise,
                               'Wahlkreis-Ausreißer; die Karte steht im Vorrat jedes Orts des Wahlkreises, gespielt höchstens einmal je Fahrt.'))
                eintrag['karten'].append({'art': 'a', 'wahlkreis': wname, 'partei': p, 'prozent': round(w[p], 1), 'gleich_im_land': gleich})
        # (b) Ort gegen Kreis, nur mit Gesamtergebnis
        wahl = o['eigenschaften']['wahl_btw25'][0]
        hinweis = wahl.get('hinweis', '')
        if o['einheit'].startswith('Ortsteil'):
            ort = {q: v for q, v in wahl['wert']['anteile_prozent'].items()} if 'nur ungefähr' not in hinweis else {}
        elif ags in fremd:
            ort = {}
            eintrag['ohne_b'] = 'Briefwahl bei der Verbandsgemeinde, kein Gesamtergebnis der Gemeinde'
        else:
            ort = anteile(summe['G' + ags])
        k = anteile(summe['K' + kreis])
        abw = sorted(((ort[q] - k[q], q) for q in HAUPT if q in ort and q in k), key=lambda t: -abs(t[0]))
        if abw and abs(abw[0][0]) >= SCHWELLE_B and abs(abw[0][0]) - abs(abw[1][0]) >= ABSTAND_B:
            d, p = abw[0]
            pos = stelle(i, 2)
            opts = setze(p, [q for _, q in abw], pos)
            kname = im_kreis(namen['K' + kreis])
            frage = 'Bundestagswahl 2025: Bei welcher Partei wich %s am stärksten vom Ergebnis %s ab?' % (o['name'], kname)
            vorn = [o['name'], steckbrief(o), frage]
            n2, q2 = abw[1]
            rueck = ('Du hattest [Option] getippt. %s gab %s %s Prozent der Zweitstimmen, %s waren es %s: %s Punkte %s. '
                     'Die nächstgrößte Abweichung hatte %s mit %s Punkten.' % (
                         o['name'], NAME[p][1], de(ort[p]), kname, de(k[p]), de(abs(d)), 'mehr' if d > 0 else 'weniger',
                         NAME[q2][0], de(abs(n2))))
            nachweise = [(q, 'Abweichung %s: %s Punkte, kleiner als %s.' % (q, de(abs(dd)), de(abs(d)))) for dd, q in abw if q in opts and q != p]
            gewaehlt = '%s %s %s %% gegen %s %% %s (Abweichung %s Punkte; nächstgrößte %s %s)' % (
                o['name'], p, de(ort[p]), de(k[p]), kname, de(d), q2, de(n2))
            karten.append(('ausreisser_kreis', gewaehlt, vorn, opts, p, rueck, nachweise,
                           'Ort gegen Kreis; Ergebnis des Orts: %s.' % (hinweis or 'Summe der Gemeinde')))
            eintrag['karten'].append({'art': 'b', 'partei': p, 'ort': round(ort[p], 1), 'kreis': round(k[p], 1), 'abweichung': round(d, 1)})
        pfad = os.path.join(AUS, o['slug'] + '.md')
        if karten:
            text = ''.join(karte(n + 1, *c[:2], c[2], c[3], c[4], c[5], c[6], c[7]) for n, c in enumerate(karten))
            text += '## ORTS-ANSCHLUSS\nkeiner (Skript-Lauf)\n## NICHT VERWENDET\nkeiner\n## UNGEREGELT\nkeiner\n'
            with io.open(pfad, 'w', encoding='utf-8', newline='\n') as f:
                f.write(text)
        elif os.path.exists(pfad):
            os.remove(pfad)
        uebersicht.append(eintrag)
        print('%-18s %s%s' % (o['slug'], '; '.join('%s %s' % (c['art'], c['partei']) for c in eintrag['karten']) or '-',
                              ('  (' + eintrag['ohne_b'] + ')') if 'ohne_b' in eintrag else ''))
    with io.open(os.path.join(ITER, 'ausreisser.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'_doc': 'Ausreißer je Zielort, Bundestagswahl 2025 (gemeinde_achsen_ausreisser.py, Lauf a0.1)', 'orte': uebersicht},
                  f, ensure_ascii=False, indent=1)
    print('Karten:', sum(len(e['karten']) for e in uebersicht))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
