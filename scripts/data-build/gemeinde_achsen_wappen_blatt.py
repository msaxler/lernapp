"""Gemeinde-Achsen: Abnahmeblatt der Wappen-Karten (Lauf w0.1) beider Räume.

Liest <raum>/karten-w0.1/*.md und <raum>/faktencheck/urteile.json (Lauf w0.1) und schreibt
docs/konzepte/quizaway-wappen-karten-<datum>.md: je Karte Vorderseite, Rückseite, Urteil des Faktenchecks.
Vor dem Neuaufbau prüfen, ob Mike schon Kreuze gesetzt hat (dann nicht überschreiben).

Aufruf:  python -X utf8 scripts/data-build/gemeinde_achsen_wappen_blatt.py
"""
import datetime
import glob
import io
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GA = os.path.join(WURZEL, 'data', 'gemeinde-achsen')
RAEUME = [('iter1', 'Freiburg'), ('neuwied', 'Neuwied')]
FELDER = 'SORTE|FAMILIE|FAKT-ID|GEWÄHLTER FAKT|BEKANNTHEIT|VORDERSEITE|RÜCKSEITE|WÖRTER RÜCKSEITE|NEGATIVNACHWEISE|PRÜFHINWEIS|## '


def feld(text, name):
    m = re.search(r'^%s:?[ \t]*(.*?)(?=^(?:%s))' % (name, FELDER), text + '\n## ENDE', flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def main():
    heute = datetime.date.today().isoformat()
    ziel = os.path.join(WURZEL, 'docs', 'konzepte', 'quizaway-wappen-karten-%s.md' % heute)
    if os.path.exists(ziel) and '[x]' in io.open(ziel, encoding='utf-8').read().lower():
        sys.exit('Blatt trägt schon Kreuze: ' + ziel)
    aus = ['# QuizAway Reise-Modus – Wappen-Karten (Lauf w0.1), %s' % heute, '',
           'Fragenfamilie Wappen nach Mikes Entscheid vom 2. Oktober 2026: Warum-Frage (woher stammt eine Figur, wofür steht '
           'sie); ohne belegte Begründung keine Karte. Quelle je Ort: Wappenabschnitt und Wappentabelle des Ortsartikels, '
           'Eintrag der Wikipedia-Wappenliste, wo nötig Nachrecherche (LEO-BW, Gemeinde, Stadt Neuwied). Kette: '
           '`gemeinde_achsen_wappen.py` → Extraktion → `gemeinde_achsen_fakten.py` → `gemeinde_achsen_wappen_eingabe.py` → '
           'Kartenlauf (Prompt v0.7 mit Zusatz `prompt-karten-wappen-v0.1.txt`) → Prüfskript `--lauf w0.1` → Faktencheck '
           '(`faktencheck/auftrag-w0.1.txt`), Befunde eingearbeitet.', '',
           'Ohne Wappen-Karte: Zähringen (nur Blasonierung belegt), Günterstal (kein Ortswappen, nur das des Klosters), '
           'Rengsdorf (für die Ortsgemeinde nichts belegt). UNSICHER heißt unten: Die Aussage trägt allein die amtliche Quelle '
           '(LEO-BW = Landesarchiv, Gemeinde, Stadt); ich werte das als belegt.', '',
           '**Fragen an Mike** (Kreuz setzen):', '',
           '- [ ] Passt die Kartenform (Figur in Alltagsworten, vier Theorien, Herkunft auf der Rückseite)? Wenn nein: was stört?',
           '- [ ] Gundelfingen Karte 1 und Denzlingen Karte 1 fragen beide nach dem badischen Schrägbalken. Beide behalten? '
           '(Vorschlag: nur Gundelfingen; Denzlingen hat die Pflugschar.)',
           '- [ ] Kommen die Wappen-Karten in den Vorrat (je Ort ein bis zwei Karten zusätzlich)?', '',
           'Einzelne Karten streichen: Kreuz in die Zeile „streichen“ der Karte.', '']
    for raum, name in RAEUME:
        urteile = {}
        pfad = os.path.join(GA, raum, 'faktencheck', 'urteile.json')
        for u in json.load(io.open(pfad, encoding='utf-8')):
            if u['lauf'] == 'w0.1':
                urteile[(u['ort'], u['karte'])] = u
        aus += ['## Raum %s' % name, '']
        for datei in sorted(glob.glob(os.path.join(GA, raum, 'karten-w0.1', '[0-9]*.md'))):
            slug = os.path.basename(datei)[:-3]
            text = io.open(datei, encoding='utf-8').read()
            for nr, karte in re.findall(r'^## Karte (\d+)\n(.*?)(?=^## )', text, flags=re.S | re.M):
                u = urteile.get((slug, int(nr)), {})
                vorn = feld(karte, 'VORDERSEITE').split('\n')
                rueck = feld(karte, 'RÜCKSEITE')
                aus += ['### %s, Karte %s' % (vorn[0].strip(), nr), '']
                aus += ['> ' + z.strip() for z in vorn[1:] if z.strip()]
                aus += ['', rueck.replace('\n', '  \n'), '',
                        '*Faktencheck: %s%s*' % (u.get('urteil', 'ungeprüft'),
                                                 (' – ' + u['befund'][:220]) if u.get('urteil') not in (None, 'OK') else ''),
                        '', '- [ ] streichen', '']
    with io.open(ziel, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(aus))
    print('geschrieben:', ziel, sum(1 for z in aus if z.startswith('### ')), 'Karten')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
