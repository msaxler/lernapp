"""Gemeinde-Achsen Iteration 1: Extraktionen auszählen.

Liest data/gemeinde-achsen/iter1/extraktion/*.txt (Ausgabe des Stufe-1-Prompts) und zählt je Ort:
Blöcke, Entitätstypen, Warum-Eigenschaften, Superlative, Blöcke außer `ort`.
Schreibt data/gemeinde-achsen/iter1/zaehlung.json und druckt eine Tabelle.

Aufruf:  python scripts/data-explore/gemeinde_achsen_zaehlen.py
"""
import glob
import io
import json
import os
import re

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITER = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))

# Eigenschaftsnamen, die eine Herkunft, Deutung, Ursache oder einen Anlass tragen
# "grund" nur als eigenes Wortglied (grund, grund_erhalt, zerstoerung_grund), nicht in grundbesitz
WARUM = re.compile(r'(namensherkunft|herkunft|benannt|(^|_)grund(_|$)|anlass|ursache|deutung|(^|_)wegen(_|$)|(^|_)zweck(_|$))', re.I)
# Superlative nur am Eigenschaftsnamen messen (superlativ, einzig…, aeltest…), nicht am Wert
SUPER = re.compile(r'(superlativ|einzig|aeltest|ältest|groesst|größt|hoechst|höchst)', re.I)


def bloecke(text):
    teile = re.split(r'^\s*-{3,}\s*$', text, flags=re.M)
    aus = []
    for t in teile:
        m = re.search(r'^\s*ENTIT[ÄA]T:\s*(.+)$', t, flags=re.M)
        if not m:
            continue
        typ = m.group(1).strip().lower()
        eig = re.findall(r'^\s{2,}([\wäöüÄÖÜß\-]+):\s*(.+)$', t, flags=re.M)
        aus.append((typ, eig))
    return aus


def main():
    with io.open(os.path.join(ITER, 'schicht0.json'), encoding='utf-8') as f:
        s0 = {e['slug']: e for e in json.load(f)}
    zeilen, alle_typen = [], {}
    for pfad in sorted(glob.glob(os.path.join(ITER, 'extraktion', '*.txt'))):
        slug = os.path.splitext(os.path.basename(pfad))[0]
        with io.open(pfad, encoding='utf-8') as f:
            bl = bloecke(f.read())
        typen = sorted({t for t, _ in bl})
        for t in typen:
            alle_typen.setdefault(t, set()).add(slug)
        warum = [(t, k) for t, eig in bl for k, _ in eig if WARUM.search(k)]
        superl = [(t, k) for t, eig in bl for k, v in eig if SUPER.search(k)]
        ohne_ort = [t for t, _ in bl if t != 'ort']
        zeilen.append({
            'slug': slug, 'rolle': s0.get(slug, {}).get('rolle', '?'), 'name': s0.get(slug, {}).get('name', slug),
            'woerter_quelle': s0.get(slug, {}).get('woerter'), 'bloecke': len(bl), 'typen': len(typen),
            'warum': len(warum), 'superlative': len(superl), 'bloecke_ohne_ort': len(ohne_ort),
            'warum_eigenschaften': sorted({k for _, k in warum}),
        })
    with io.open(os.path.join(ITER, 'zaehlung.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'orte': zeilen, 'typen_gesamt': len(alle_typen),
                   'typen_in_mind_3_orten': sorted(t for t, s in alle_typen.items() if len(s) >= 3)},
                  f, ensure_ascii=False, indent=1)
    print('%-16s %-7s %7s %6s %5s %5s %5s' % ('Ort', 'Rolle', 'Wörter', 'Blöcke', 'Typen', 'Warum', 'Super'))
    for z in zeilen:
        print('%-16s %-7s %7s %6d %5d %5d %5d' % (z['slug'], z['rolle'], z['woerter_quelle'], z['bloecke'],
                                                 z['typen'], z['warum'], z['superlative']))
    print('Entitätstypen gesamt: %d, davon in mindestens drei Orten: %d' % (
        len(alle_typen), sum(1 for s in alle_typen.values() if len(s) >= 3)))


if __name__ == '__main__':
    main()
