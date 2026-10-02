"""Gemeinde-Achsen Iteration 1: jede Karte an ihren Fakt binden.

Liest aus den geprüften Fassungen (karten-geprueft/v0.4, v0.5, v0.6) je Karte das Feld GEWÄHLTER FAKT
und sucht dazu die Kennung des Fakts (fakten/index.json, siehe gemeinde_achsen_fakten.py):
  - Klassiker:   <slug>/G.<eigenschaft>, beim Wahlergebnis mit der gefragten Größe (G.wahl_btw25.zweite …)
  - Geschichten: der Fakt des Orts, dessen Bezeichnung, Eigenschaften und Werte das Feld am besten treffen;
                 trägt eine Karte die Zeile "FAKT-ID:", gilt diese (Prompt ab v0.7).
Einträge in karten-fakt-von-hand.json gehen der Suche vor (falsche oder unsichere Treffer, mit Grund).
Zwei Karten tragen denselben Fakt, wenn ihr "schluessel" gleich ist: bei breiten Fakten (ort, stadtteil,
gemeinde und Grunddaten) Kennung samt Eigenschaft, sonst die Kennung; fakten-gleich.json führt Kennungen
zusammen, die dieselbe Sache meinen (ein Ding, zweimal extrahiert).
Schreibt karten-fakt.json.

Aufruf:  python -X utf8 scripts/data-build/gemeinde_achsen_karten_fakt.py [--zeigen]
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemeinde_achsen_fakten import ROH, fakten  # noqa: E402

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
LAEUFE = [('v0.4', 'Vorschlag'), ('v0.5', 'Karte'), ('v0.6', 'Karte'), ('a0.1', 'Karte')]  # a0.1: Ausreißer (2026-10-03)
# ein weiterer Raum (GA_RAUM=neuwied) nennt seine Läufe in <raum>/orte.json (dort jüngster zuerst)
if os.path.exists(os.path.join(ITER, 'orte.json')):
    with io.open(os.path.join(ITER, 'orte.json'), encoding='utf-8') as _f:
        LAEUFE = [(l[0], l[1]) for l in reversed(json.load(_f)['laeufe'])]
FELDER = 'FAKTENCHECK|SORTE|FAMILIE|FAKT-ID|GEWÄHLTER FAKT|BEKANNTHEIT|VORDERSEITE|RÜCKSEITE|WÖRTER RÜCKSEITE|ANSCHLUSS|NEGATIVNACHWEISE|PRÜFHINWEIS|## '
# Fakten, die viele verschiedene Sachen tragen: hier entscheidet erst die Eigenschaft über "derselbe Fakt"
BREIT = ('ort', 'stadtteil', 'gemeinde', 'dorf', 'stadt')
# ab hier nennt das Feld die Belege der wahren Aussagen einer Lügen-Karte, nicht mehr den gewählten Fakt
BELEGE = r'Belege? der wahren|Wahre Aussagen?\b|\(wahre Aussagen?|gestützt durch|Stütz'
WAHL = [('zweitstärkste', 'zweite'), ('stärksten partei', 'erste'), ('wahlbeteiligung', 'beteiligung')]


def lies(name):
    with io.open(os.path.join(ITER, name), encoding='utf-8') as f:
        return f.read()


def lies_json(name, leer):
    return json.loads(lies(name)) if os.path.exists(os.path.join(ITER, name)) else leer


def feld(v, name):
    m = re.search(r'^%s:?[ \t]*(.*?)(?=^(?:%s))' % (name, FELDER), v + '\n## ENDE', flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def karten(lauf, kopf, ort):
    # ein Lauf muss nicht jeden Ort haben (Ausreißer-Karten nur, wo es einen Ausreißer gibt)
    if not os.path.exists(os.path.join(ITER, 'karten-geprueft', lauf, ort + '.md')):
        return {}
    teile = re.split(r'^##\s*%s\s*(\d+)\s*$' % kopf, lies(os.path.join('karten-geprueft', lauf, ort + '.md')), flags=re.M)
    return dict((int(teile[i]), re.split(r'^##\s*(?:ORTS-ANSCHLUSS|NICHT VERWENDET|UNGEREGELT)', teile[i + 1], flags=re.M)[0])
                for i in range(1, len(teile), 2))


def glatt(text):
    return re.sub(r'[„“”"‚‘’\'()\[\]]', '', text.lower()).replace('_', ' ')


def treffer(kopf_text, ganz, fakt):
    """Punktzahl, wie gut ein Fakt das Feld GEWÄHLTER FAKT trifft, und die zuerst genannte Eigenschaft."""
    punkte = 0.0
    bez = glatt(fakt['bezeichnung'])
    if len(bez) >= 4 and bez in kopf_text:
        punkte += 3 + min(len(bez), 40) / 20.0 + (2 if kopf_text.find(bez) < 60 else 0)
    if glatt(fakt['entitaet']) in kopf_text[:50]:
        punkte += 1
    stellen = sorted((ganz.find(glatt(k)), k) for k in fakt['eigenschaften'] if len(k) >= 5 and glatt(k) in ganz)
    punkte += min(len(stellen), 4)
    punkte += min(sum(1 for w in fakt['werte'] if len(w) >= 6 and glatt(w) in ganz), 4)
    return punkte, (stellen[0][1] if stellen else '')


def binde(ort, text, fakten, werte):
    """(Kennung, Eigenschaft, Punkte, Abstand zum Zweiten) für ein Feld GEWÄHLTER FAKT."""
    if text.startswith('GRUNDDATEN'):
        m = re.match(r'GRUNDDATEN[ ,:]+([a-z0-9_]+)', text)
        if not m:
            sys.exit('Grunddaten ohne Eigenschaft: %s | %s' % (ort, text[:80]))
        groesse = next((kurz for wort, kurz in WAHL if wort in text.lower()), 'ergebnis') if m.group(1) == 'wahl_btw25' else ''
        return '%s/G.%s' % (ort, m.group(1)), groesse, 9.0, 9.0
    kopf_text = glatt(re.split(BELEGE, text)[0])
    rang = []
    for kennung, f in fakten.items():
        if kennung.split('/')[0].split('+')[0] != ort:
            continue
        p, eig = treffer(kopf_text, kopf_text, dict(f, werte=werte.get(kennung, [])))
        rang.append((p, kennung, eig))
    rang.sort(key=lambda r: (-r[0], r[1]))
    return rang[0][1], rang[0][2], rang[0][0], rang[0][0] - rang[1][0]


def schluessel(kennung, eigenschaft, index, gleich, geteilt=()):
    """geteilt: Fakten, die mehr als eine Sache tragen (karten-fakt-von-hand.json); dort zählt die Eigenschaft mit."""
    if kennung in gleich:
        return gleich[kennung]
    breit = '/G.' in kennung or kennung in geteilt or index.get(kennung, {}).get('entitaet', '').lower() in BREIT
    voll = '%s.%s' % (kennung, eigenschaft) if breit and eigenschaft else kennung
    return gleich.get(voll, voll)


def main():
    index = lies_json(os.path.join('fakten', 'index.json'), {})
    # gesucht wird in den Werten der Rohextraktion: die Karten zitieren, was ihr Lauf gelesen hat,
    # und die Bindung darf sich nicht verschieben, wenn eine Berichtigung dazukommt
    werte = {}
    for datei in sorted(set(k.split('/')[0] for k in index)):
        for kennung, block in fakten(os.path.join(ROH, datei + '.txt')):
            werte[kennung] = [m.group(1).strip().strip('"') for m in re.finditer(r'^  [^:\n]+:[ \t]*(.*)$', block, flags=re.M)]
    von_hand = lies_json('karten-fakt-von-hand.json', {})
    geteilt = set(h['fakt'] for k, h in von_hand.items() if k != '_doc' and h.get('schluessel'))
    gleich = {}
    for gruppe in lies_json('fakten-gleich.json', {'gruppen': []})['gruppen']:
        for k in gruppe['kennungen'][1:]:
            gleich[k] = gruppe['kennungen'][0]
    orte = sorted(set(k.split('/')[0].split('+')[0] for k in index))
    aus, unsicher = [], []
    for ort in orte:
        for lauf, kopf in LAEUFE:
            for nr, v in sorted(karten(lauf, kopf, ort).items()):
                text = ' '.join(feld(v, 'GEWÄHLTER FAKT').split())
                hand = von_hand.get('%s|%s|%d' % (ort, lauf, nr))
                eigene = feld(v, 'FAKT-ID').split()
                eigener = ''
                if hand:
                    kennung, eig, wie = hand['fakt'], hand.get('eigenschaft', ''), 'von Hand: ' + hand['grund']
                    eigener = hand.get('schluessel', '')
                elif eigene and eigene[0].startswith('GRUNDDATEN'):
                    kennung, eig, _, _ = binde(ort, 'GRUNDDATEN %s %s' % (eigene[0].partition('.')[2], text), index, werte)
                    wie = 'Kartenlauf'
                elif eigene:
                    kennung, _, eig = eigene[0].partition('.')
                    wie = 'Kartenlauf'
                else:
                    kennung, eig, punkte, abstand = binde(ort, text, index, werte)
                    wie = 'Suche'
                    if punkte < 5 or abstand < 1:
                        wie = 'Suche, unsicher'
                        unsicher.append((ort, lauf, nr, kennung, punkte, abstand, text[:110]))
                if '/G.' not in kennung and kennung not in index:
                    sys.exit('unbekannte Kennung %s bei %s %s %d' % (kennung, ort, lauf, nr))
                aus.append({'ort': ort, 'lauf': lauf, 'karte': nr, 'fakt': kennung, 'eigenschaft': eig,
                            'schluessel': eigener or schluessel(kennung, eig, index, gleich, geteilt), 'feld': text[:160],
                            'bezeichnung': index.get(kennung, {}).get('bezeichnung', 'Grunddaten'), 'wie': wie})
    with io.open(os.path.join(ITER, 'karten-fakt.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(aus, f, ensure_ascii=False, indent=0)
    zahl = {}
    for a in aus:
        zahl[a['wie'].split(':')[0]] = zahl.get(a['wie'].split(':')[0], 0) + 1
    print('Karten: %d · %s' % (len(aus), ' · '.join('%s %d' % kv for kv in sorted(zahl.items()))))
    for u in unsicher:
        print('  unsicher: %s %s %d → %s (%.1f Punkte, Abstand %.1f) | %s' % u)
    if '--zeigen' in sys.argv:
        for a in aus:
            print('%s %s %2d → %-30s %-28s | %s' % (a['ort'][:6], a['lauf'], a['karte'], a['schluessel'], a['bezeichnung'][:28], a['feld'][:75]))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
