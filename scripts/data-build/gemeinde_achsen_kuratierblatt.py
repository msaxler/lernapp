"""Gemeinde-Achsen Iteration 1: Kuratierblatt aus den generierten Kartenvorschlägen bauen.

Liest data/gemeinde-achsen/iter1/karten/*.md und schreibt
docs/konzepte/quizaway-stufe2-kuratierblatt-2026-10-01.md: je Zielort die handgeschriebene Karte in einem Satz
und die bis zu drei Vorschläge mit Vorderseite, Rückseite, Wortzahl, Anschluss und Wegen der Negativnachweise.

Aufruf:  python scripts/data-build/gemeinde_achsen_kuratierblatt.py
"""
import glob
import io
import os
import re

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KARTEN = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'iter1', 'karten')
ZIEL = os.path.join(WURZEL, 'docs', 'konzepte', 'quizaway-stufe2-kuratierblatt-2026-10-01.md')

# Handgeschriebene Karte je Ort (Kartensatz Freiburg, Fassung 1) in einem Satz, und was Stufe 2 dazu ergab
HAND = {
    '01-umkirch': ('Umkirch', 'A', 'Namensherkunft: Kirche in den Wellen.',
                   'Vorschlag 1 nimmt denselben Fakt.'),
    '02-gundelfingen': ('Gundelfingen', 'C (Spannen)', 'Einwohnerzahl; größte Gemeinde im Landkreis ohne Stadtrecht.',
                        'Vorschlag 3 nimmt denselben Fakt.'),
    '03-denzlingen': ('Denzlingen', 'B', 'Wahr: sieben Zigarrenfabriken, Bahnhof seit 1845. Lüge: Straßenbahn (Fassung 2: bis 1810 württembergisch).',
                      'Vorschlag 1 baut die Lüge wie Fassung 2 über die Herrschaft und nutzt die Zigarrenfabriken als Wahrheit.'),
    '04-zaehringen': ('Zähringen', 'A', 'Die Herzöge benannten sich nach der Burg, nicht umgekehrt.',
                      'Nicht erreichbar: Der Fakt steht nicht im Artikel des Stadtteils (570 Wörter).'),
    '05-st-peter': ('St. Peter', 'C (Leiter)', 'Höhe des Orts, 716 m; Erzählanschluss an Zähringen (Hauskloster der Herzöge).',
                    'Andere Zahlen gewählt; der Erzählanschluss wurde verworfen, weil die Fakten das Herzogshaus nennen und nicht den Ort Zähringen.'),
    '06-glottertal': ('Glottertal', 'A (Radar)', 'Drehort der Schwarzwaldklinik.',
                      'Vom Bekanntheitsfilter gesperrt, wie gewollt. Radar ist aus extrahierten Fakten nicht erzeugbar; daher Familie A.'),
    '07-kirchzarten': ('Kirchzarten', 'B', 'Wahr: Tarodunum, Mountainbike-WM 1995. Lüge: liegt an der Rheintalbahn.',
                       'Vorschlag 2 baut dieselbe Lüge über die Bahnstrecke (Schwarzwaldbahn statt Höllentalbahn); Vorschlag 3 nutzt die WM 1995.'),
    '08-guenterstal': ('Günterstal', 'A (Radar)', 'Um ein Zisterzienserinnenkloster entstanden.',
                       'Kloster nicht gewählt. Vorschlag 2 nimmt die südlichste Straßenbahnhaltestelle, die bei der handgeschriebenen Karte in der Auflösung steht.'),
    '09-horben': ('Horben', 'C (Spannen)', 'Einwohnerzahl, 1.204.',
                  'Andere Zahlen gewählt. Die Ortshöhe wurde gemieden, weil Wikidata (495 m) und Artikel (607 m) sich widersprechen.'),
    '10-staufen': ('Staufen', 'B', 'Wahr: Fausts Tod 1539, Altstadt-Hebung nach der Bohrung 2007. Lüge: größte Gemeinde ohne Stadtrecht (Fassung 2: Landkreis Lörrach).',
                   'Faust und Hebungsrisse hat der Bekanntheitsfilter als „hoch" gesperrt; die Vorschläge sind leiser.'),
}


def feld(v, name):
    felder = 'FAMILIE|GEWÄHLTER FAKT|BEKANNTHEIT|VORDERSEITE|RÜCKSEITE|WÖRTER RÜCKSEITE|ANSCHLUSS|NEGATIVNACHWEISE|## '
    m = re.search(r'^%s:?\s*(.*?)(?=^(?:%s)\b)' % (name, felder), v + '\n## ENDE', flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def zitat(text):
    return '\n'.join('> ' + z if z.strip() else '>' for z in text.strip().split('\n'))


def main():
    aus = ['# QuizAway — Stufe 2, Kuratierblatt Raum Freiburg',
           '',
           '**Erzeugt am 2026-10-01** aus `data/gemeinde-achsen/iter1/karten/` mit `scripts/data-build/gemeinde_achsen_kuratierblatt.py`. '
           'Je Ort bis zu drei generierte Vorschläge in der Familie der handgeschriebenen Karte. '
           'Bericht dazu: `quizaway-stufe2-volllauf-2026-10-01.md`.',
           '',
           '**So geht es:** Je Ort eine Zeile ankreuzen. Wer eine Karte umformulieren will, schreibt es dazu. '
           'Die vollständigen Ausgaben mit allen Negativnachweisen stehen in den Kartendateien.',
           '']
    for pfad in sorted(glob.glob(os.path.join(KARTEN, '*.md'))):
        slug = os.path.splitext(os.path.basename(pfad))[0]
        name, fam, hand, befund = HAND[slug]
        with io.open(pfad, encoding='utf-8') as f:
            text = f.read()
        aus += ['---', '', '## %s · %s · Familie %s' % (slug[:2], name, fam), '',
                '**Handgeschrieben:** ' + hand, '', '**Stufe 2:** ' + befund, '']
        teile = re.split(r'^##\s*Vorschlag\s*(\d)\s*$', text, flags=re.M)
        nummern = []
        for i in range(1, len(teile), 2):
            v = re.split(r'^##\s*(?:NICHT VERWENDET|UNGEREGELT)', teile[i + 1], flags=re.M)[0]
            nr = teile[i]
            nummern.append(nr)
            rueck = feld(v, 'RÜCKSEITE')
            rueck_text = re.split(r'^\s*Quelle:', rueck, flags=re.M)[0].strip()
            ansch = feld(v, 'ANSCHLUSS')
            wege = ''.join(sorted(set(re.findall(r'Weg \(([abc])\)', feld(v, 'NEGATIVNACHWEISE')))))
            bek = (feld(v, 'BEKANNTHEIT').split() or ['?'])[0].strip('–-:.').lower()
            aus += ['### Vorschlag %s' % nr, '', zitat(feld(v, 'VORDERSEITE')), '', zitat(rueck_text), '',
                    '%d Wörter · Bekanntheit %s · Negativnachweis Weg %s · Anschluss: %s' % (
                        len(rueck_text.split()), bek, wege or '?', 'nein' if ansch.lower().startswith('keiner') else 'ja'),
                    '']
        aus += ['**Wahl:** ' + ' '.join('[ ] %s' % n for n in nummern) + ' [ ] keiner', '']
    aus += ['---', '', '*Ende Kuratierblatt.*', '']
    with io.open(ZIEL, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(aus))
    print('geschrieben:', ZIEL, len(aus), 'Zeilen')


if __name__ == '__main__':
    main()
