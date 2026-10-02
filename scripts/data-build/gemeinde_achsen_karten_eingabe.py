"""Gemeinde-Achsen Iteration 1: Eingabedateien für den Karten-Prompt v0.6 bauen.

Je Zielort eine Datei data/gemeinde-achsen/iter1/eingabe-v0.6/<slug>.txt mit den Blöcken, die der
Prompt nennt: ZIELORT (mit LAGE und ARTIKEL), GRUNDDATEN, PLAN, LETZTER_PIN, FAHRT, FAKTEN,
FAKTEN AUS ZWEITER QUELLE (bei dünnem Ortsartikel), SPENDER.
Ein Kartenlauf liest nur prompt-karten-v0.6.txt und diese eine Datei.

Neu gegenüber v0.5 (Bericht zum zweiten Volllauf W3, W8; Faktencheck F4; Entscheide Mike 2026-10-02):
  - Der PLAN gibt die Eigenschaft jedes Klassikers vor und wechselt sie von Ort zu Ort.
  - Die Höhe trägt nur eine Karte, wenn die Quellen höchstens fünf Prozent auseinanderliegen.
  - Zweite Quelle bei dünnem Artikel; ein Spender statt zwei.
  - BERICHTIGUNGEN: die Gründe aus faktencheck/korrekturen.json je Ort (erst nach der Probe an drei Orten
    eingeführt; die Probe-Eingaben von Zähringen, St. Peter und Horben liefen ohne diesen Block).
Die Eingaben des zweiten Volllaufs liegen unverändert in eingabe-v0.5/ (Stand des Skripts: Commit 09b317f).

Aufruf:  python -X utf8 scripts/data-build/gemeinde_achsen_karten_eingabe.py
"""
import io
import json
import os
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'iter1')
AUS = os.path.join(ITER, 'eingabe-v0.6')

# Zahlen, bei denen verschiedene Werte der Quellen nebeneinander gezeigt werden
MEHRWERTIG = ('hoehe_m', 'flaeche_km2', 'ersterwaehnung')
# ein kleiner Spender je Ort für Weg (b), abwechselnd aus drei Landschaften
SPENDER = ['s4-dornstetten', 's10-tengen', 's2-renchen']
# Karte 2 als Leiter statt Spannen
LEITER = ('05-st-peter', '07-kirchzarten')
# Rotation der Klassiker: (Eigenschaft, Familie, Beschreibung für den PLAN)
ZAHL = [('einwohner', 'Einwohnerzahl'), ('ersterwaehnung', 'Jahr der ersten Erwähnung'), ('flaeche_km2', 'Fläche der Gemarkung'),
        ('hoehe_m', 'Höhe des Orts'), ('dichte_ew_km2', 'Einwohner je Quadratkilometer')]
POLITIK = [('A', 'zweitstärkste Partei'), ('C', 'Wahlbeteiligung in Prozent'), ('C', 'Anteil der stärksten Partei in Prozent')]
LAGE = [('landkreis', 'A', 'Landkreis'), ('kfz', 'A', 'Kennzeichen'), ('partnerstaedte', 'A', 'Partnerstadt'),
        ('eingemeindung', 'C', 'Jahr der Eingemeindung'), ('km_landeshauptstadt', 'C', 'Luftlinie zur Landeshauptstadt'),
        ('flaeche_km2', 'C', 'Fläche der Gemarkung'), ('dichte_ew_km2', 'C', 'Einwohner je Quadratkilometer')]


def de(zahl):
    if isinstance(zahl, float):
        return ('%.2f' % zahl).rstrip('0').rstrip('.').replace('.', ',')
    if isinstance(zahl, int) and abs(zahl) >= 10000:
        return '{:,}'.format(zahl).replace(',', '.')
    return str(zahl)


def verschiedene(liste):
    werte = []
    for e in liste:
        if e['wert'] not in werte:
            werte.append(e['wert'])
    return werte


def uneins(key, liste):
    """Zahl mit Quellwerten, die mehr als fünf Prozent auseinanderliegen."""
    werte = verschiedene(liste)
    return key in MEHRWERTIG and len(werte) > 1 and (max(werte) - min(werte)) > 0.05 * max(abs(max(werte)), 1)


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
    elif key == 'kfz':
        text = '%s (Hauptkennzeichen; Kreise geben daneben oft frühere Kennzeichen aus)' % w
    elif key in MEHRWERTIG:
        if uneins(key, liste):
            vermerke.append('MEHRERE WERTE')
        quellen = []
        for e in liste:
            if e['quelle'] not in quellen:
                quellen.append(e['quelle'])
        return '  %s: %s%s  [%s]' % (key, ' | '.join(de(x) for x in verschiedene(liste)), ''.join(' — ' + v for v in vermerke), '; '.join(quellen))
    elif isinstance(w, list):
        text = ', '.join(str(x) for x in w)
    else:
        text = de(w)
    stand = ', Stand %s' % erster['stand'].replace('-00-00', '') if erster.get('stand') else ''
    return '  %s: %s%s  [%s%s]' % (key, text, ''.join(' — ' + v for v in vermerke), erster['quelle'], stand)


def grunddaten_text(ort, nur=None):
    aus = []
    for key, liste in ort['eigenschaften'].items():
        if (nur and key not in nur) or key == 'lage' or (key == 'kueste' and liste[0]['wert'] != 'ja'):
            continue
        aus.append(zeile(key, liste))
    return '\n'.join(aus)


def zulaessig(ort, key):
    e = ort['eigenschaften']
    return key in e and not uneins(key, e[key])


def waehle(ort, rotation, i, gesperrt=()):
    """Erste zulässige Eigenschaft der Rotation ab Stelle i, dazu die nächste als Ersatz."""
    kand = [rotation[(i + k) % len(rotation)] for k in range(len(rotation))]
    kand = [r for r in kand if zulaessig(ort, r[0]) and r[0] not in gesperrt]
    return kand[0], (kand[1] if len(kand) > 1 else None)


def plan(i, ort):
    slug = ort['slug']
    a = lambda k: ((i * 3 + k * 5) % 4) + 1
    b = lambda k: ((i + k) % 3) + 1
    zahl, zahl_ersatz = waehle(ort, ZAHL, i)
    pol_fam, pol = POLITIK[i % len(POLITIK)]
    # Landkreis und Kennzeichen eines Stadtteils sind die der Stadt und schon durch den Steckbrief verraten
    stadt = ('landkreis', 'kfz') if ort['einheit'].startswith('Ortsteil') else ()
    lage, lage_ersatz = waehle(ort, LAGE, i, gesperrt=(zahl[0], zahl_ersatz[0] if zahl_ersatz else '') + stadt)
    ersatz = lambda e: ' (Ersatz: %s)' % e[-1] if e else ''
    zahl_form = ('C-LEITER, letzte Stufe mit "höher": %d' % (a(2) % 3 + 1)) if slug in LEITER else 'C, wahre Spanne an Stelle %d' % a(2)
    return '\n'.join([
        '  Karte 1: Geschichte, A, wahre Option an Stelle %d' % a(1),
        '  Karte 2: Klassiker, EIGENSCHAFT %s: %s%s, %s' % (zahl[0], zahl[1], ersatz(zahl_ersatz), zahl_form),
        '  Karte 3: Geschichte, B, Lüge an Stelle %d' % b(3),
        '  Karte 4: Klassiker Politik, EIGENSCHAFT wahl_btw25: %s, %s, wahre Option an Stelle %d' % (pol, pol_fam, a(4)),
        '  Karte 5: Geschichte, A, wahre Option an Stelle %d' % a(5),
        '  Karte 6: Klassiker, EIGENSCHAFT %s: %s%s, %s, wahre Option an Stelle %d' % (lage[0], lage[2], ersatz(lage_ersatz), lage[1], a(6)),
        '  Karte 7: Geschichte, A oder B, oder C mit einer überraschenden Zahl aus FAKTEN (Regel 6); '
        'wahre Option an Stelle %d (bei B: Lüge an Stelle %d)' % (a(7), b(7)),
    ])


def lies(pfad):
    with io.open(pfad, encoding='utf-8') as f:
        return f.read().strip()


def main():
    nur = sys.argv[1:]  # optional: nur diese Slugs bauen
    with io.open(os.path.join(ITER, 'grunddaten.json'), encoding='utf-8') as f:
        orte = json.load(f)['orte']
    with io.open(os.path.join(ITER, 'schicht0.json'), encoding='utf-8') as f:
        artikel = {o['slug']: o['dewiki'] for o in json.load(f)}
    zweit = []
    if os.path.exists(os.path.join(ITER, 'zweitquellen.json')):
        with io.open(os.path.join(ITER, 'zweitquellen.json'), encoding='utf-8') as f:
            zweit = json.load(f)
    # Befunde des Faktenchecks fließen als Berichtigungen zurück, damit ein neuer Lauf bekannte Fehler nicht wiederholt
    berichtigt = {}
    pfad = os.path.join(ITER, 'faktencheck', 'korrekturen.json')
    if os.path.exists(pfad):
        with io.open(pfad, encoding='utf-8') as f:
            for k in json.load(f):
                # Gründe, die nur auf eine andere Karte verweisen ("Wie v0.5 Karte 7 …"), sagen dem Kartenlauf nichts
                if k['grund'] != 'Steckbrief berichtigt.' and not k['grund'].startswith('Wie v0.') \
                        and k['grund'] not in berichtigt.setdefault(k['ort'], []):
                    berichtigt[k['ort']].append(k['grund'])
    ziel = [o for o in orte if o['rolle'] == 'ziel']
    name = {o['slug']: o['name'] for o in orte}
    os.makedirs(AUS, exist_ok=True)
    for i, o in enumerate(ziel):
        if nur and o['slug'] not in nur:
            continue
        lage = o['eigenschaften']['lage'][0]['wert']
        if o['einheit'].startswith('Ortsteil'):
            # ein Stadtteil liegt nicht "nördlich von" seiner Stadt, sondern in ihr (Faktencheck v0.6, Zähringen)
            km_text, _, rest = lage.partition(' von ')
            lage = 'Stadtteil von %s, %s der Stadtmitte (Luftlinie)' % (rest.split(' (')[0], km_text)
        teile = ['ZIELORT: %s (%s)' % (o['name'], o['einheit']),
                 'LAGE: ' + lage,
                 'ARTIKEL: ' + artikel[o['slug']], '',
                 'GRUNDDATEN:', grunddaten_text(o), '',
                 'PLAN:', plan(i, o), '']
        if i > 0:
            v = ziel[i - 1]
            teile += ['LETZTER_PIN: %s (%s)' % (v['name'], v['einheit']),
                      grunddaten_text(v, nur=('einwohner', 'flaeche_km2', 'hoehe_m', 'landkreis', 'kfz', 'ersterwaehnung',
                                              'wahl_btw25', 'naechste_grossstadt', 'bahnhof')), '']
        else:
            teile += ['LETZTER_PIN: keiner (erster Ort der Fahrt)', '']
        teile += ['FAHRT: ' + ', '.join(z['name'] for z in ziel), '',
                  'FAKTEN (Zielort %s):' % o['name'], lies(os.path.join(ITER, 'extraktion', o['slug'] + '.txt')), '']
        for z in zweit:
            pfad = os.path.join(ITER, 'extraktion', z['datei'])
            if z['slug'] == o['slug'] and os.path.exists(pfad):
                teile += ['FAKTEN AUS ZWEITER QUELLE (Wikipedia, Artikel „%s“):' % z['titel'], lies(pfad), '']
        if berichtigt.get(o['slug']):
            teile += ['BERICHTIGUNGEN (aus dem Faktencheck früherer Läufe; gehen FAKTEN vor):'] + [
                '  - ' + b for b in berichtigt[o['slug']]] + ['']
        s = SPENDER[i % 3]
        teile += ['SPENDER: %s (nicht Teil der Fahrt)' % name[s], lies(os.path.join(ITER, 'extraktion', s + '.txt')), '']
        text = '\n'.join(teile)
        with io.open(os.path.join(AUS, o['slug'] + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text + '\n')
        print('%-16s %7d Zeichen' % (o['slug'], len(text)))
        print(plan(i, o))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
