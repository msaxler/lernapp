"""Gemeinde-Achsen Iteration 1: Fakten mit fester Kennung und mit den Berichtigungen des Faktenchecks.

Die Rohextraktion (extraktion/<datei>.txt) bleibt unverändert. Dieses Skript schreibt je Datei eine
berichtigte Fassung nach fakten/<datei>.txt:
  - Jeder Fakt (Block ENTITÄT … ---) bekommt die Zeile "ID: <datei>/<lfd. Nr.>", z. B. 09-horben/031.
    Die Nummer ist die Stelle des Blocks in der Rohextraktion und bleibt damit fest.
  - Die Berichtigungen aus faktencheck/berichtigungen.json werden am Fakt selbst angebracht:
      "wert"      Eigenschaft bekommt einen neuen Wert ("alt" muss im bisherigen Wert stehen)
      "streichen" Eigenschaft entfällt
      "hinweis"   Zeile "BERICHTIGT: …" im Fakt (Vorbehalt, strittiger Wert, Beleg nur Wikipedia)
      "sperre"    Zeile "NICHT VERWENDEN: …" (der Fakt trägt keine Karte)
    Trifft eine Berichtigung ihre Stelle nicht, bricht das Skript ab.
  - fakten/index.json: je Kennung Entität, Bezeichnung, Eigenschaften, Zahl der Berichtigungen.
Berichtigungen an Grunddaten tragen die Kennung <slug>/G.<eigenschaft>; sie stehen nicht in fakten/,
das Eingabe-Skript hängt sie an die Zeile der Grunddaten.

Aufruf:  python -X utf8 scripts/data-build/gemeinde_achsen_fakten.py
"""
import glob
import io
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
ROH = os.path.join(ITER, 'extraktion')
AUS = os.path.join(ITER, 'fakten')
BERICHTIGUNGEN = os.path.join(ITER, 'faktencheck', 'berichtigungen.json')
# Die Extraktion schreibt den Namen des Fakts nicht immer unter BEZEICHNUNG
NAMENSFELDER = ('BEZEICHNUNG', 'DESIGNNUNG')


def lies(pfad):
    with io.open(pfad, encoding='utf-8') as f:
        return f.read()


def bloecke(text):
    return [b.strip('\n') for b in re.split(r'^---\s*$', text, flags=re.M) if b.strip()]


def kopf(block, name):
    m = re.search(r'^%s:[ \t]*(.*)$' % name, block, flags=re.M)
    return m.group(1).strip() if m else ''


def bezeichnung(block):
    for feld in NAMENSFELDER:
        if kopf(block, feld):
            return kopf(block, feld)
    m = re.search(r'^  (?:name|bezeichnung|titel):[ \t]*(.*)$', block, flags=re.M)
    # ohne Namen steht die Art des Fakts für ihn (ortsgeschichte, bürgerentscheid, keltisches_oppidum)
    return m.group(1).strip() if m else kopf(block, 'ENTITÄT').replace('_', ' ')


def eigenschaften(block):
    return dict((m.group(1), m.group(2).strip()) for m in re.finditer(r'^  ([^:\n]+):[ \t]*(.*)$', block, flags=re.M))


def fakten(datei):
    """Liste (Kennung, Block) einer Rohdatei."""
    stamm = os.path.basename(datei)[:-4]
    return [('%s/%03d' % (stamm, i + 1), b) for i, b in enumerate(bloecke(lies(datei)))]


def berichtige(kennung, block, eintraege):
    for e in eintraege:
        art = e['art']
        if art in ('wert', 'streichen'):
            muster = r'^  %s:[ \t]*(.*)$' % re.escape(e['eigenschaft'])
            m = re.search(muster, block, flags=re.M)
            if not m:
                sys.exit('Berichtigung trifft nicht: %s hat keine Eigenschaft %s' % (kennung, e['eigenschaft']))
            if e.get('alt') and e['alt'] not in m.group(1):
                sys.exit('Berichtigung trifft nicht: %s %s enthält nicht „%s“ (steht: %s)' % (
                    kennung, e['eigenschaft'], e['alt'], m.group(1)))
            neu = '' if art == 'streichen' else '  %s: %s' % (e['eigenschaft'], e['neu'])
            block = block[:m.start()] + neu + block[m.end() + (1 if art == 'streichen' else 0):]
        zeile = {'wert': 'BERICHTIGT', 'streichen': 'BERICHTIGT', 'hinweis': 'BERICHTIGT', 'sperre': 'NICHT VERWENDEN'}[art]
        block = block.rstrip('\n') + '\n%s: %s' % (zeile, e['grund'])
    return block


def main():
    datei = json.loads(lies(BERICHTIGUNGEN)) if os.path.exists(BERICHTIGUNGEN) else {'berichtigungen': [], 'nur_karte': []}
    eintraege = datei['berichtigungen']
    # Jeder Befund des Faktenchecks muss an einem Fakt hängen oder als reiner Kartenfehler geführt sein
    erfasst = set(tuple(h) for e in eintraege for h in e['herkunft']) | set((n['ort'], n['lauf'], n['karte']) for n in datei['nur_karte'])
    korrekturen = os.path.join(ITER, 'faktencheck', 'korrekturen.json')  # fehlt, solange ein Raum keinen Faktencheck hat
    offen = [k for k in (json.loads(lies(korrekturen)) if os.path.exists(korrekturen) else [])
             if (k['ort'], k['lauf'], k['karte']) not in erfasst]
    je_fakt = {}
    for e in eintraege:
        je_fakt.setdefault(e['fakt'], []).append(e)
    os.makedirs(AUS, exist_ok=True)
    index, getroffen = {}, set()
    for datei in sorted(glob.glob(os.path.join(ROH, '[0-9]*.txt'))):
        aus = []
        for kennung, block in fakten(datei):
            index[kennung] = {'entitaet': kopf(block, 'ENTITÄT'), 'bezeichnung': bezeichnung(block),
                              'eigenschaften': sorted(eigenschaften(block)), 'berichtigungen': len(je_fakt.get(kennung, []))}
            if kennung in je_fakt:
                block = berichtige(kennung, block, je_fakt[kennung])
                getroffen.add(kennung)
            aus.append('ID: %s\n%s' % (kennung, block))
        with io.open(os.path.join(AUS, os.path.basename(datei)), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n---\n'.join(aus) + '\n')
        print('%-22s %3d Fakten, %d berichtigt' % (os.path.basename(datei), len(aus),
                                                   sum(1 for k, _ in fakten(datei) if k in je_fakt)))
    grund = [e['fakt'] for e in eintraege if '/G.' in e['fakt']]
    fehlend = sorted(set(je_fakt) - getroffen - set(grund))
    if fehlend:
        sys.exit('Berichtigung ohne Fakt: ' + ', '.join(fehlend))
    with io.open(os.path.join(AUS, 'index.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(index, f, ensure_ascii=False, indent=0)
    print('zusammen: %d Fakten · %d Berichtigungen an %d Fakten · %d an Grunddaten · Befunde des Faktenchecks ohne Fakt: %d' % (
        len(index), len(eintraege) - len(grund), len(getroffen), len(grund), len(offen)))
    for k in offen:
        print('  offen: %s %s %d – %s' % (k['ort'], k['lauf'], k['karte'], k['grund'][:100]))
    return 1 if offen else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
