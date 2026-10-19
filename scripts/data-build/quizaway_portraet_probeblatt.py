"""Ortsporträt: lesbares Probekarten-Blatt aus karten-v0.8-portraet/<slug>.md für Mike und Tochter (Abnahme nach Geschmack).
Je Karte: Rang, Facette, Charakteristikum, Vorderseite, Rückseite; am Ende der Steckbrief. Ohne Prüffelder.
Aufruf: python -X utf8 scripts/data-build/quizaway_portraet_probeblatt.py 432-breitnau 433-kirchzarten > docs/konzepte/<datei>.md
"""
import io, os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORDNER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'bahn', 'karten-v0.8-portraet')
FELDER = 'FACETTE|SORTE|FAMILIE|FAKT-ID|GEWÄHLTER FAKT|CHARAKTERISTIKUM|BEKANNTHEIT|RANG|VORDERSEITE|RÜCKSEITE|WÖRTER RÜCKSEITE|NEGATIVNACHWEISE|PRÜFHINWEIS|PRÜFSTUFE|ERFUNDEN'


def feld(text, name):
    m = re.search(r'^%s:[ \t]*(.*?)(?=^(?:%s):|\Z)' % (name, FELDER), text + '\n', flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print('# QuizAway Ortsporträt – Probekarten (Prompt v0.9, %s)\n' % ', '.join(sys.argv[1:]))
    print('Abnahme nach Geschmack: Löst die Karte beim Vorbeifahren ein „Echt?!“ aus, und weiß man danach etwas über den Ort? '
          'Noch ohne Faktencheck (Prüfstufen 1 und 2 folgen). Rang = Vorschlag des Modells, 1 = beste Karte zuerst.\n')
    for slug in sys.argv[1:]:
        with io.open(os.path.join(ORDNER, slug + '.md'), encoding='utf-8') as f:
            t = f.read()
        teile = re.split(r'^## Karte (\d+)\s*$', t, flags=re.M)
        karten = [(int(teile[i]), teile[i + 1]) for i in range(1, len(teile) - 1, 2)]
        rest = teile[-1]
        karten.sort(key=lambda k: int((re.match(r'(\d+)', feld(k[1], 'RANG')) or re.match(r'(\d+)', '99')).group(1)))
        print('\n## %s\n' % slug)
        for n, k in karten:
            vorn = feld(k, 'VORDERSEITE').split('\n')
            rueck = feld(k, 'RÜCKSEITE').split('\n')
            print('### Rang %s · Karte %d · %s · %s' % (feld(k, 'RANG').split(' – ')[0], n, feld(k, 'FACETTE'), feld(k, 'CHARAKTERISTIKUM')))
            print('*%s*\n' % vorn[1] if len(vorn) > 1 else '')
            print('**%s**\n' % (vorn[2] if len(vorn) > 2 else ''))
            for o in vorn[3:]:
                print('- ' + o)
            print('\n> ' + ' '.join(z for z in rueck if not z.startswith('Quelle:')).replace('Du hattest [Option] getippt. ', ''))
            print('>\n> *%s*\n' % ' '.join(z for z in rueck if z.startswith('Quelle:')))
        m = re.search(r'^## STECKBRIEF\s*\n(.*?)(?=^## |\Z)', rest, flags=re.S | re.M)
        if m:
            print('### Steckbrief\n')
            for z in m.group(1).strip().split('\n'):
                print('- ' + z.strip())
            print()


if __name__ == '__main__':
    main()
