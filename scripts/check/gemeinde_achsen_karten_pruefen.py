"""Gemeinde-Achsen Iteration 1: generierte Kartenvorschläge mechanisch prüfen.

Liest data/gemeinde-achsen/iter1/karten/*.md (Ausgabe des Karten-Prompts) und prüft je Vorschlag:
Wörter der Rückseite (<= 70), Wörter je Option (<= 8), Wörter der Frage (<= 25), Stelle der Lösung,
Anschluss vorhanden, Wege der Negativnachweise (a/b/c).
Schreibt data/gemeinde-achsen/iter1/karten-pruefung.json und druckt eine Tabelle.

Aufruf:  python scripts/check/gemeinde_achsen_karten_pruefen.py
"""
import glob
import io
import json
import os
import re

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KARTEN = os.path.join(WURZEL, 'data', 'gemeinde-achsen', 'iter1', 'karten')


def feld(text, name, bis):
    m = re.search(r'^%s:?\s*(.*?)(?=^(?:%s)\b)' % (name, bis), text, flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def pruefe(vorschlag):
    felder = 'FAMILIE|GEWÄHLTER FAKT|BEKANNTHEIT|VORDERSEITE|RÜCKSEITE|WÖRTER RÜCKSEITE|ANSCHLUSS|NEGATIVNACHWEISE|## '
    v = vorschlag + '\n## ENDE'
    fakt = feld(v, 'GEWÄHLTER FAKT', felder)
    vorn = feld(v, 'VORDERSEITE', felder)
    rueck = feld(v, 'RÜCKSEITE', felder)
    ansch = feld(v, 'ANSCHLUSS', felder)
    neg = feld(v, 'NEGATIVNACHWEISE', felder)
    bek = feld(v, 'BEKANNTHEIT', felder)
    rueck_text = re.split(r'^\s*Quelle:', rueck, flags=re.M)[0]
    optionen = re.findall(r'^\s*(\d)[.)]\s+(.+)$', vorn, flags=re.M)
    zeilen = [z for z in vorn.split('\n') if z.strip() and not re.match(r'^\s*\d[.)]\s', z)]
    frage = zeilen[-1] if zeilen else ''
    m = re.search(r'(?:Richtig war|Die Lüge war|Richtig:?)\s*(\d)', rueck_text)
    return {
        'fakt': ' '.join(fakt.split())[:140],
        'bekanntheit': (bek.split() or ['?'])[0].strip('–-:').lower(),
        'woerter_rueckseite': len(rueck_text.split()),
        'woerter_frage': len(frage.split()),
        'optionen': len(optionen),
        'max_woerter_option': max([len(o.split()) for _, o in optionen] or [0]),
        'loesung_stelle': int(m.group(1)) if m else None,
        'anschluss': not ansch.lower().startswith('keiner'),
        'wege': ''.join(sorted(set(re.findall(r'Weg \(([abc])\)', neg)))),
    }


def main():
    alle = []
    print('%-16s %2s %4s %5s %4s %3s %6s %5s  %s' % ('Ort', 'Nr', 'Rück', 'Frage', 'Opt', 'St.', 'Anschl', 'Wege', 'Fakt'))
    for pfad in sorted(glob.glob(os.path.join(KARTEN, '*.md'))):
        slug = os.path.splitext(os.path.basename(pfad))[0]
        with io.open(pfad, encoding='utf-8') as f:
            text = f.read()
        teile = re.split(r'^##\s*Vorschlag\s*(\d)\s*$', text, flags=re.M)
        for i in range(1, len(teile), 2):
            rest = re.split(r'^##\s*(?:NICHT VERWENDET|UNGEREGELT)', teile[i + 1], flags=re.M)[0]
            p = pruefe(rest)
            p.update({'ort': slug, 'vorschlag': int(teile[i])})
            alle.append(p)
            print('%-16s %2d %4d %5d %4d %3s %6s %5s  %s' % (
                slug, p['vorschlag'], p['woerter_rueckseite'], p['woerter_frage'], p['max_woerter_option'],
                p['loesung_stelle'], 'ja' if p['anschluss'] else '-', p['wege'], p['fakt'][:70]))
    with io.open(os.path.join(os.path.dirname(KARTEN), 'karten-pruefung.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(alle, f, ensure_ascii=False, indent=1)
    zu_lang = [a for a in alle if a['woerter_rueckseite'] > 70]
    print('Vorschläge: %d · Rückseite über 70 Wörter: %d · Option über 8 Wörter: %d · mit Anschluss: %d' % (
        len(alle), len(zu_lang), sum(1 for a in alle if a['max_woerter_option'] > 8), sum(1 for a in alle if a['anschluss'])))


if __name__ == '__main__':
    main()
