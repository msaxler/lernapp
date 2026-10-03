"""Gemeinde-Achsen, Raum bahn: geprüfte Fassung der Karten bauen (Prüfstufen nach Spielkonzept v0.3.1 §8 Nr. 9).

Je Karte aus karten-v0.8/<slug>.md das Endurteil:
  Prüfstufe 1 (pruefung-v0.1) → bei "stufe2" das Urteil von Prüfstufe 2 (stufe2-v0.1) → bei einer Karte der
  Gegenprobe (gegenprobe-v0.1) deren Urteil, wenn es strenger ist → Handberichtigungen (korrekturen-hand.json).
Berichtigungen der Modellstufen (Feld BERICHTIGT mit VORDERSEITE: oder RÜCKSEITE:) werden eingesetzt; fehlt der
berichtigten Rückseite die Quellenzeile, bleibt die alte stehen. Schreibt
  karten-geprueft/v0.8/<slug>.md   je Karte die Zeile "FAKTENCHECK: <Status> – <Grund>" unter der Überschrift
  vorrat-liste.json                alle Karten außer den gesperrten
  kuratierung.json                 leer, solange Mike nicht kuratiert hat (wird nicht überschrieben)
Die Rohausgaben bleiben unverändert.

Aufruf:  GA_RAUM=bahn python -X utf8 scripts/data-build/gemeinde_achsen_bahn_geprueft.py
"""
import io
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAUM = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'bahn'))
LAUF = 'v0.8'
STRENGE = {'bestätigt': 0, 'unsicher': 1, 'korrigiert': 2, 'gesperrt': 3}


def lies(p):
    with io.open(p, encoding='utf-8') as f:
        return f.read()


def abschnitte(text, muster=r'^## Karte (\d+)\s*$'):
    teile = re.split(muster, text, flags=re.M)
    return dict((int(teile[i]), teile[i + 1]) for i in range(1, len(teile) - 1, 2))


def feld(text, name):
    m = re.search(r'^%s:[ \t]*(.*?)(?=^[A-ZÄÖÜ][A-ZÄÖÜ0-9 -]*:|\Z)' % name, text, flags=re.S | re.M)
    return m.group(1).strip() if m else ''


def urteil(text):
    m = re.search(r'^URTEIL:\s*([a-zäöü0-9]+)', text or '', flags=re.M | re.I)
    return m.group(1).lower() if m else None


def einsetzen(karte, berichtigt):
    """Ersetzt VORDERSEITE/RÜCKSEITE der Karte durch die berichtigte Fassung."""
    if not berichtigt or berichtigt.strip() in ('–', '-'):
        return karte, False
    # die letzte Karte einer Prüfdatei: Trennlinie und ÜBERSICHT gehören nicht zur Berichtigung
    berichtigt = re.split(r'^(?:---\s*$|## )', berichtigt, flags=re.M)[0]
    geaendert = False
    for name in ('VORDERSEITE', 'RÜCKSEITE'):
        m = re.search(r'^%s:[ \t]*(.*?)(?=^(?:VORDERSEITE|RÜCKSEITE):|\Z)' % name, berichtigt, flags=re.S | re.M)
        # "RÜCKSEITE: –" heißt: diese Seite bleibt, wie sie ist
        if not m or m.group(1).strip() in ('', '–', '-'):
            continue
        neu = m.group(1).strip()
        alt = feld(karte, name)
        if name == 'RÜCKSEITE' and 'Quelle:' not in neu and 'Quelle:' in alt:
            neu += '\n' + alt[alt.index('Quelle:'):]
        k = re.search(r'^%s:[ \t]*\n?(.*?)(?=^[A-ZÄÖÜ][A-ZÄÖÜ0-9 -]*:|\Z)' % name, karte, flags=re.S | re.M)
        if k:
            karte = karte[:k.start(1)] + neu + '\n' + karte[k.end(1):]
            geaendert = True
    return karte, geaendert


def main():
    conf = json.loads(lies(os.path.join(RAUM, 'orte.json')))
    hand = json.loads(lies(os.path.join(RAUM, 'korrekturen-hand.json'))) if os.path.exists(os.path.join(RAUM, 'korrekturen-hand.json')) else {}
    aus_ordner = os.path.join(RAUM, 'karten-geprueft', LAUF)
    os.makedirs(aus_ordner, exist_ok=True)
    vorrat, summe = [], {}
    for slug, rolle, name, _, _ in conf['orte']:
        pfad = os.path.join(RAUM, 'karten-v0.8', slug + '.md')
        if rolle != 'ziel' or not os.path.exists(pfad) or not os.path.exists(os.path.join(RAUM, 'pruefung-v0.1', slug + '.md')):
            continue
        roh = lies(pfad)
        kopf, _, rest = roh.partition('## Karte ')
        schluss = re.search(r'^## ORTS-ANSCHLUSS.*', roh, flags=re.S | re.M)
        karten = abschnitte(roh.split('## ORTS-ANSCHLUSS')[0])
        p1 = abschnitte(lies(os.path.join(RAUM, 'pruefung-v0.1', slug + '.md')))
        p2 = abschnitte(lies(os.path.join(RAUM, 'stufe2-v0.1', slug + '.md'))) if os.path.exists(os.path.join(RAUM, 'stufe2-v0.1', slug + '.md')) else {}
        gp = abschnitte(lies(os.path.join(RAUM, 'gegenprobe-v0.1', slug + '.md')), r'^## Karte .*? (\d+)\s*$') \
            if os.path.exists(os.path.join(RAUM, 'gegenprobe-v0.1', slug + '.md')) else {}
        teile = []
        for n in sorted(karten):
            k = karten[n]
            u1 = urteil(p1.get(n))
            quelle, status = p1.get(n, ''), u1 or 'ungeprüft'
            if u1 == 'stufe2':
                quelle, status = p2.get(n, ''), urteil(p2.get(n)) or 'unsicher'
            grund = feld(quelle, 'BEFUND') or 'keiner'
            if status == 'korrigiert':
                # BERICHTIGT reicht bis zum Ende des Abschnitts; darin stehen eigene Felder VORDERSEITE:/RÜCKSEITE:
                m = re.search(r'^BERICHTIGT:[ \t]*(.*)', quelle, flags=re.S | re.M)
                k, ok = einsetzen(k, m.group(1) if m else '')
                if not ok:
                    status, grund = 'unsicher', 'Berichtigung nicht einsetzbar: ' + grund
            if n in gp and STRENGE.get(urteil(gp[n]), 0) > STRENGE.get(status, 0):
                status, grund = urteil(gp[n]), 'Gegenprobe: ' + feld(gp[n], 'BEFUND')
            for h in hand.get(slug, []) if isinstance(hand.get(slug), list) else []:
                if h['karte'] == n and h['lauf'] == LAUF:
                    for alt, neu in h['ersetzungen']:
                        if alt not in k:
                            sys.exit('Handberichtigung trifft nicht: %s %d: %s' % (slug, n, alt))
                        k = k.replace(alt, neu)
                    status, grund = h['status'], h['grund']
            grund = ' '.join(grund.split())
            teile.append('## Karte %d\nFAKTENCHECK: %s – %s\n%s' % (n, status, grund, k.strip('\n')))
            summe[status] = summe.get(status, 0) + 1
            if status != 'gesperrt':
                vorrat.append({'ort': slug, 'lauf': LAUF, 'karte': n, 'sorte': (feld(k, 'SORTE').split() or ['?'])[0],
                               'familie': (feld(k, 'FAMILIE').split() or ['?'])[0], 'faktencheck': status})
        with io.open(os.path.join(aus_ordner, slug + '.md'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n\n'.join(teile) + '\n\n' + (schluss.group(0) if schluss else '') + '\n')
    with io.open(os.path.join(RAUM, 'vorrat-liste.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(vorrat, f, ensure_ascii=False, indent=1)
    kur = os.path.join(RAUM, 'kuratierung.json')
    if not os.path.exists(kur):
        with io.open(kur, 'w', encoding='utf-8', newline='\n') as f:
            json.dump({'_doc': 'Kuratierung Raum bahn: noch keine (Mike hat nichts gestrichen).', 'kartensatz': {}}, f, ensure_ascii=False, indent=1)
    print('Urteile:', summe, '| im Vorrat:', len(vorrat), 'Karten an', len(set(v['ort'] for v in vorrat)), 'Orten')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
