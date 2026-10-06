"""Gemeinde-Achsen: Anschlüsse in alle Richtungen aus den Grunddaten rechnen (Mike 2026-10-07).

Bisher hatte jeder Ort genau einen Anschluss, den an seinen Vorgänger in orte.json. Im Umkreis eines Orts (Freiburg,
Neuwied) kommt man aber aus verschiedenen Richtungen an. Dieses Skript rechnet für jedes Ortspaar mit höchstens
RADIUS_KM Luftlinie je Richtung bis zu zwei Zeilen, ohne Modell, nach den Regeln der Handzeilen (Mike 2026-10-03):
Alltagssprache, beide Orte beim Namen, gesagt wird, was verglichen wird. Reihenfolge der Kandidaten:
Landesgrenze · Kreisgrenze · stärkste Partei verschieden · Einwohner · Höhe · Fläche · Platz zwei verschieden.
Wahl nur als Gesamtergebnis der Bundestagswahl 2025 (grunddaten.json). Zahlen werden gerundet und in Worten
verglichen („gut dreieinhalbmal“), nie genauer, als die Daten tragen.

Handzeilen in anschluss-berichtigt.json (geprüft) haben für ihr Ortspaar Vorrang; der Export führt beides zusammen.
Schreibt <raum>/anschluesse-umkreis.json: {ort: {von: [zeilen]}}.

Aufruf:  GA_RAUM=bahn python -X utf8 scripts/data-build/gemeinde_achsen_anschluesse.py [--zeigen <slug>]
"""
import io
import json
import math
import os
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAUM = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'bahn'))
RADIUS_KM = 20
ZAHLWORT = {2: 'doppelt', 3: 'dreimal', 4: 'viermal', 5: 'fünfmal', 6: 'sechsmal', 7: 'siebenmal', 8: 'achtmal',
            9: 'neunmal', 10: 'zehnmal', 11: 'elfmal', 12: 'zwölfmal', 13: 'dreizehnmal', 14: 'vierzehnmal',
            15: 'fünfzehnmal', 16: 'sechzehnmal', 17: 'siebzehnmal', 18: 'achtzehnmal', 19: 'neunzehnmal',
            20: 'zwanzigmal'}
HALB = {1.5: 'anderthalbmal', 2.5: 'zweieinhalbmal', 3.5: 'dreieinhalbmal', 4.5: 'viereinhalbmal'}
PARTEI = {'CDU': ('die CDU', False), 'SPD': ('die SPD', False), 'AfD': ('die AfD', False), 'GRÜNE': ('die Grünen', True),
          'FDP': ('die FDP', False), 'Die Linke': ('die Linke', False), 'BSW': ('das BSW', False), 'CSU': ('die CSU', False),
          'FREIE WÄHLER': ('die Freien Wähler', True)}


def w(o, k):
    v = o['eigenschaften'].get(k)
    if isinstance(v, list):
        v = v[0] if v else None
    return v.get('wert') if isinstance(v, dict) else v


def km(a, b):
    p1, p2 = math.radians(a['lat']), math.radians(b['lat'])
    d = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b['lon'] - a['lon']) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(d))


def mal(r):
    """Verhältnis r >= 1.4 in Worten: 'gut dreieinhalbmal', 'fast doppelt', 'rund 25-mal'."""
    if r >= 20:
        n = int(round(r / 5.0) * 5)
        return ('rund %d-mal' % n) if n > 20 else 'rund zwanzigmal'
    stufen = [s / 2.0 for s in range(3, 10)] + list(range(5, 21))   # 1,5 … 4,5 in halben, dann ganze Schritte
    s = min(stufen, key=lambda x: abs(x - r))
    wort = HALB.get(s) or ZAHLWORT[int(s)]
    if abs(r - s) / s <= 0.03:
        return wort
    return ('fast ' if r < s else 'gut ') + wort


def rund(n):
    if n >= 100000:
        return '{:,}'.format(int(round(n, -4))).replace(',', '.')
    if n >= 10000:
        return '{:,}'.format(int(round(n, -3))).replace(',', '.')
    return '{:,}'.format(int(round(n, -2))).replace(',', '.')


def kreis(o):
    k = w(o, 'landkreis')
    if not k:
        return None
    return 'zum ' + k if k.lower().endswith('kreis') else 'zum Landkreis ' + k


def zeilen(a, b):
    """Kandidaten für den Anschluss von a (vorher gespielt) nach b, beste zuerst."""
    na, nb = a['name'], b['name']
    out = []
    la, lb = w(a, 'bundesland'), w(b, 'bundesland')
    if la and lb and la != lb:
        out.append('Landesgrenze: %s liegt in %s, %s in %s.' % (na, la, nb, lb))
    else:
        ka, kb = kreis(a), kreis(b)
        if ka and kb and ka != kb:
            out.append('Kreisgrenze: %s gehört %s, %s %s.' % (na, ka, nb, kb))
        elif (ka and not kb and b['einheit'] == 'Stadt') or (kb and not ka and a['einheit'] == 'Stadt'):
            if ka:
                out.append('Kreisgrenze: %s gehört %s, %s ist kreisfrei.' % (na, ka, nb))
            else:
                out.append('Kreisgrenze: %s ist kreisfrei, %s gehört %s.' % (na, nb, kb))
    wa, wb = w(a, 'wahl_btw25') or {}, w(b, 'wahl_btw25') or {}
    pa = sorted(wa.get('anteile_prozent', {}).items(), key=lambda x: -x[1])
    pb = sorted(wb.get('anteile_prozent', {}).items(), key=lambda x: -x[1])
    if pa and pb and pa[0][0] != pb[0][0] and pa[0][0] in PARTEI and pb[0][0] in PARTEI:
        (ta, pla), (tb, plb) = PARTEI[pa[0][0]], PARTEI[pb[0][0]]
        out.append('Bundestagswahl 2025: In %s %s %s vorn, in %s %s.' % (na, 'lagen' if pla else 'lag', ta, nb, tb))
    ea, eb = w(a, 'einwohner'), w(b, 'einwohner')
    if ea and eb:
        g, k, ng, nk = (ea, eb, na, nb) if ea >= eb else (eb, ea, nb, na)
        r = g / float(k)
        if r < 1.1:
            out.append('%s und %s sind fast gleich groß: rund %s und %s Einwohner.' % (na, nb, rund(ea), rund(eb)))
        elif r < 1.4:
            out.append('%s hat rund %s Einwohner mehr als %s.' % (ng, rund(g - k), nk))
        else:
            out.append('%s hat %s so viele Einwohner wie %s.' % (ng, mal(r), nk))
    ha, hb = w(a, 'hoehe_m'), w(b, 'hoehe_m')
    if ha and hb and abs(ha - hb) >= 150:
        hoch, tief = (nb, na) if hb > ha else (na, nb)
        out.append('%s liegt rund %d Meter höher als %s.' % (hoch, int(round(abs(ha - hb), -1)), tief))
    fa, fb = w(a, 'flaeche_km2'), w(b, 'flaeche_km2')
    if fa and fb and ea and eb:
        g, k, ng, nk, eg, ek = (fa, fb, na, nb, ea, eb) if fa >= fb else (fb, fa, nb, na, eb, ea)
        if g / k >= 2 and eg < ek:
            out.append('%s hat %s so viel Fläche wie %s, aber weniger Einwohner.' % (ng, mal(g / k), nk))
    if pa and pb and pa[0][0] == pb[0][0] and len(pa) > 1 and len(pb) > 1 and pa[1][0] != pb[1][0] \
            and pa[1][0] in PARTEI and pb[1][0] in PARTEI:
        out.append('Bundestagswahl 2025: Auf Platz zwei kam in %s %s, in %s %s.' % (na, PARTEI[pa[1][0]][0], nb, PARTEI[pb[1][0]][0]))
    return out[:2]


def main():
    with io.open(os.path.join(RAUM, 'grunddaten.json'), encoding='utf-8') as f:
        orte = [o for o in json.load(f)['orte'] if o.get('lat') and o.get('lon')]
    aus, paare = {}, 0
    for b in orte:
        for a in orte:
            if a is b or km(a, b) > RADIUS_KM:
                continue
            z = zeilen(a, b)
            if z:
                aus.setdefault(b['slug'], {})[a['slug']] = z
                paare += 1
    with io.open(os.path.join(RAUM, 'anschluesse-umkreis.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'_doc': 'Gerechnet von scripts/data-build/gemeinde_achsen_anschluesse.py (Radius %d km); '
                           'Handzeilen in anschluss-berichtigt.json haben für ihr Paar Vorrang.' % RADIUS_KM,
                   'anschluesse': aus}, f, ensure_ascii=False, indent=1)
    print('%d Ortspaare (gerichtet) an %d Orten' % (paare, len(aus)))
    if '--zeigen' in sys.argv:
        s = sys.argv[sys.argv.index('--zeigen') + 1]
        for von, z in aus.get(s, {}).items():
            print('  von %-22s %s' % (von, ' | '.join(z)))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
