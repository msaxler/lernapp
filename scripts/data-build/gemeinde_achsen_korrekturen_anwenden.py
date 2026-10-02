"""Gemeinde-Achsen Iteration 1: Ergebnis des Faktenchecks auf die Karten anwenden.

Die Rohausgaben der Kartenläufe (karten/ und karten-v0.5/) bleiben unverändert. Dieses Skript schreibt
geprüfte Fassungen nach karten-geprueft/v0.4/ und karten-geprueft/v0.5/:
  - je Karte eine Zeile "FAKTENCHECK: <Status> – <Grund>" direkt unter der Überschrift,
  - bei Status "korrigiert" die Ersetzungen aus faktencheck/korrekturen.json.
Status: bestätigt (Urteil OK), korrigiert, unsicher (Beleg nur Wikipedia), gesperrt (so nicht spielbar).
Außerdem zieht es die Korrekturen der v0.4-Karten im Kuratierblatt des ersten Laufs nach, ohne die
Kreuze dort anzutasten.

Aufruf:  python -X utf8 scripts/check/gemeinde_achsen_faktencheck_auswerten.py
         python -X utf8 scripts/data-build/gemeinde_achsen_korrekturen_anwenden.py
"""
import io
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
BLATT_V1 = os.path.join(WURZEL, 'docs', 'konzepte', 'quizaway-stufe2-kuratierblatt-2026-10-01.md')
LAEUFE = {'v0.6': ('karten-v0.6', 'Karte', 60), 'v0.5': ('karten-v0.5', 'Karte', 60), 'v0.4': ('karten', 'Vorschlag', 70)}
# ein weiterer Raum (GA_RAUM=neuwied) nennt seine Läufe in <raum>/orte.json; ein Kuratierblatt des ersten Laufs hat er nicht
if os.path.exists(os.path.join(ITER, 'orte.json')):
    with io.open(os.path.join(ITER, 'orte.json'), encoding='utf-8') as _f:
        LAEUFE = dict((l[0], (l[3], l[1], l[4])) for l in json.load(_f)['laeufe'])
    BLATT_V1 = None
FELDER = 'FAKTENCHECK|SORTE|FAMILIE|FAKT-ID|GEWÄHLTER FAKT|BEKANNTHEIT|VORDERSEITE|RÜCKSEITE|WÖRTER RÜCKSEITE|ANSCHLUSS|NEGATIVNACHWEISE|PRÜFHINWEIS|## '


def feld(text, name):
    m = re.search(r'^%s:?[ \t]*(.*?)(?=^(?:%s))' % (name, FELDER), text + '\n## ENDE', flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def lies(pfad):
    with io.open(pfad, encoding='utf-8') as f:
        return f.read()


def schreibe(pfad, text):
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    with io.open(pfad, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def grenzen(abschnitt, max_rueck):
    """Wortgrenzen einer Karte nach der Korrektur: Liste der Verstöße."""
    vorn = feld(abschnitt, 'VORDERSEITE')
    rueck = re.split(r'^\s*Quelle:', feld(abschnitt, 'RÜCKSEITE'), flags=re.M)[0].strip()
    optionen = re.findall(r'^\s*\d[.):]?\s+(.+)$', vorn, flags=re.M)
    zeilen = [z.strip() for z in vorn.split('\n') if z.strip() and not re.match(r'^\s*\d[.):]?\s', z) and not z.startswith('STELLE:')]
    frage = ' '.join(zeilen[2:]) if len(zeilen) > 2 else (zeilen[-1] if zeilen else '')
    aus = []
    if len(rueck.split()) > max_rueck:
        aus.append('Rückseite %d Wörter' % len(rueck.split()))
    if len(frage.split()) > 25:
        aus.append('Frage %d Wörter' % len(frage.split()))
    if max([len(o.split()) for o in optionen] or [0]) > 8:
        aus.append('Option über 8 Wörter')
    return aus, len(rueck.split())


def main():
    urteile = json.loads(lies(os.path.join(ITER, 'faktencheck', 'urteile.json')))
    korr = {(k['ort'], k['lauf'], k['karte']): k for k in json.loads(lies(os.path.join(ITER, 'faktencheck', 'korrekturen.json')))}
    status, fehler, woerter = {}, [], {}
    for u in urteile:
        schluessel = (u['ort'], u['lauf'], u['karte'])
        if u['urteil'] == 'OK':
            zweite = not u['zweite_quelle'].lower().startswith(('keine', 'netz nicht'))
            status[schluessel] = ('bestätigt', 'Artikel und zweite Quelle' if zweite else 'Artikel; keine zweite Quelle gefunden')
        elif schluessel in korr:
            status[schluessel] = (korr[schluessel]['status'], korr[schluessel]['grund'])
        else:
            fehler.append('ohne Korrektur-Eintrag: %s %s %d (%s)' % (u['ort'], u['lauf'], u['karte'], u['urteil']))
    for s in korr:
        if s not in status and s[2] != 'anschluss':
            fehler.append('Korrektur ohne Urteil: %s %s %s' % s)

    for lauf, (ordner, kopf, max_rueck) in LAEUFE.items():
        for ort in sorted(set(u['ort'] for u in urteile if u['lauf'] == lauf)):
            text = lies(os.path.join(ITER, ordner, ort + '.md'))
            teile = re.split(r'^(##\s*%s\s*\d+\s*)$' % kopf, text, flags=re.M)
            aus = [teile[0]]
            for i in range(1, len(teile), 2):
                nr = int(re.search(r'\d+', teile[i]).group(0))
                rest = teile[i + 1]
                # Der Schluss (Anschluss, nicht verwendet, ungeregelt) hängt an der letzten Karte; dort nicht ersetzen
                schnitt = re.search(r'^##\s*(?:ORTS-ANSCHLUSS|NICHT VERWENDET|UNGEREGELT)', rest, flags=re.M)
                karte, schluss = (rest[:schnitt.start()], rest[schnitt.start():]) if schnitt else (rest, '')
                s = (ort, lauf, nr)
                st, grund = status.get(s, ('ungeprüft', 'kein Urteil im Faktencheck'))
                for e in korr.get(s, {}).get('ersetzungen', []):
                    alt, neu = e[0], e[1]
                    # drittes Element "alle": der Satz steht in Rückseite und ANSCHLUSS-Feld zugleich
                    if karte.count(alt) != 1 and not (len(e) > 2 and karte.count(alt) > 1):
                        fehler.append('%s %s %d: Stelle %d-mal gefunden: %s' % (ort, lauf, nr, karte.count(alt), alt[:60]))
                        continue
                    karte = karte.replace(alt, neu)
                verstoesse, n = grenzen(karte, max_rueck)
                woerter[s] = n
                if st != 'gesperrt':
                    fehler += ['%s %s %d: %s' % (ort, lauf, nr, v) for v in verstoesse]
                karte = re.sub(r'^(WÖRTER RÜCKSEITE:).*$', lambda m: '%s %d' % (m.group(1), n), karte, count=1, flags=re.M) if korr.get(s, {}).get('ersetzungen') else karte
                # Ersetzungen im Orts-Anschluss: Eintrag mit "karte": "anschluss" (der Anschluss hängt am Ortspaar, nicht an einer Karte)
                if schluss:
                    for e in korr.get((ort, lauf, 'anschluss'), {}).get('ersetzungen', []):
                        if schluss.count(e[0]) != 1:
                            fehler.append('%s %s Anschluss: Stelle %d-mal gefunden: %s' % (ort, lauf, schluss.count(e[0]), e[0][:60]))
                            continue
                        schluss = schluss.replace(e[0], e[1])
                aus += [teile[i], '\nFAKTENCHECK: %s – %s' % (st, grund), karte, schluss]
            schreibe(os.path.join(ITER, 'karten-geprueft', lauf, ort + '.md'), ''.join(aus))

    # Kuratierblatt des ersten Laufs: Ersetzungen nachziehen, Faktencheck an die Kennzeile hängen
    blatt = lies(BLATT_V1) if BLATT_V1 else ''
    for (ort, lauf, nr), k in korr.items():
        if lauf != 'v0.4':
            continue
        for e in k['ersetzungen']:
            alt, neu = e[0], e[1]
            if blatt.count(alt) == 1:
                blatt = blatt.replace(alt, neu)
            elif blatt.count(neu) != 1:
                fehler.append('Kuratierblatt v1, %s Vorschlag %d: Stelle %d-mal gefunden: %s' % (ort, nr, blatt.count(alt), alt[:60]))
    zeilen, ort, nr = blatt.split('\n'), None, None
    slug = {u['ort'][:2]: u['ort'] for u in urteile}
    for i, z in enumerate(zeilen):
        m = re.match(r'^## (\d\d) · ', z)
        if m:
            ort = slug.get(m.group(1))
        m = re.match(r'^### Vorschlag (\d)', z)
        if m:
            nr = int(m.group(1))
        if re.match(r'^\d+ Wörter · Bekanntheit', z) and ort and nr:
            s = (ort, 'v0.4', nr)
            z = re.sub(r' · Faktencheck: .*$', '', z)
            z = re.sub(r'^\d+ Wörter', '%d Wörter' % woerter[s], z)
            zeilen[i] = '%s · Faktencheck: **%s**%s' % (z, status[s][0], '' if status[s][0] == 'bestätigt' else ' (%s)' % status[s][1])
    if BLATT_V1:
        schreibe(BLATT_V1, '\n'.join(zeilen))

    zahl = {}
    for st, _ in status.values():
        zahl[st] = zahl.get(st, 0) + 1
    print('Karten: %d · %s' % (len(status), ' · '.join('%s %d' % kv for kv in sorted(zahl.items()))))
    for lauf in LAEUFE:
        z = {}
        for (o, l, n), (st, _) in status.items():
            if l == lauf:
                z[st] = z.get(st, 0) + 1
        print('  %s: %s' % (lauf, ' · '.join('%s %d' % kv for kv in sorted(z.items()))))
    print('Fehler: %d' % len(fehler))
    for f in fehler:
        print('  -', f)
    schreibe(os.path.join(ITER, 'faktencheck', 'status.json'),
             json.dumps([{'ort': o, 'lauf': l, 'karte': n, 'status': st, 'grund': g, 'woerter_rueckseite': woerter.get((o, l, n))}
                         for (o, l, n), (st, g) in sorted(status.items())], ensure_ascii=False, indent=1))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
