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
# Ortsporträt (2026-10-19): GA_LAUF=v0.9 GA_TAG=-portraet liest karten-v0.8-portraet/, pruefung-v0.1-portraet/, stufe2-v0.1-portraet/
# und schreibt karten-geprueft/v0.9/; in vorrat-liste.json ersetzen die v0.9-Karten eines Orts dessen ältere Karten
# (Mike: Qualität zuerst), andere Orte bleiben unberührt.
LAUF = os.environ.get('GA_LAUF', 'v0.8')
TAG = os.environ.get('GA_TAG', '')
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


OPT = re.compile(r'^\d[.):]?\s')


def vorderseite_ordnen(neu, alt):
    """Bringt eine berichtigte Vorderseite in die Zeilenform der Karte (Ort / Steckbrief / Frage / 1.–4.).
    Die Prüfstufen schreiben sie teils in eine Zeile mit „ / “ und angehängtem „— RÜCKSEITE: …“ (Kloster Marienhaus 1),
    teils nur die neue Frage mit „(Optionen 1–4 bleiben gleich.)“ (Vörstetten 5); wörtlich eingesetzt, verlor die Karte
    Ort, Steckbrief und Antworten (86 leere Karten bis 2026-10-17)."""
    neu = re.split(r'\s*[—–-]?\s*RÜCKSEITE\b', neu, maxsplit=1)[0].strip()
    # „Frage neu: „…““ (Rüsselsheim 1, 8) und ein „…“ am Anfang (Buchenbach 9) sind nur Verpackung
    neu = re.sub(r'^[…/\s]+', '', re.sub(r'^Frage neu:\s*', '', neu)).strip()
    if neu.startswith('„') and '“' in neu:
        neu = neu[1:neu.rindex('“')] + neu[neu.rindex('“') + 1:]
    alt_z = [z.strip() for z in alt.split('\n') if z.strip()]
    zeilen = [z.strip() for z in neu.split('\n') if z.strip()]
    if len(zeilen) == 1 and ' / ' in zeilen[0]:
        teile = [t.strip() for t in zeilen[0].split(' / ')]
        zeilen = teile[:-1] + [t.strip() for t in re.split(r'\s+(?=\d[.)]\s)', teile[-1]) if t.strip()]
    if not any(OPT.match(z) for z in zeilen) and any(OPT.match(z) for z in alt_z):
        # nur die Frage ist neu: Ort, Steckbrief und Antworten bleiben aus der alten Karte
        frage = re.sub(r'\s*\((?:[^()]*?(?:bleib|unverändert|gleich)[^()]*)\)\s*', ' ', ' '.join(zeilen)).strip()
        # auch ohne Klammern: „… Frage? Optionen 1–4 unverändert.“ (Kloster Marienhaus 5, 2026-10-17)
        frage = re.sub(r'\s*(?:Die\s+)?(?:Optionen|Antworten)\s*\d?\s*[–-]?\s*\d?\s*(?:bleiben\s*)?(?:unverändert|gleich)\.?\s*$', '', frage)
        frage = re.sub(r'^[…/\s]+', '', frage.strip('„“"').strip()).strip()
        frage = re.sub(r'\s*\(\s*$', '', frage)   # abgeschnittene Klammer „(Optionen …“ (Müllheim 1)
        kopf = alt_z[:2]
        opts = [z for z in alt_z[2:] if OPT.match(z)]
        return '\n'.join(kopf + [frage] + opts)
    if alt_z and zeilen and zeilen[0] != alt_z[0] and len([z for z in zeilen if not OPT.match(z)]) == 1:
        # Frage und Antworten ohne Ort und Steckbrief
        zeilen = alt_z[:2] + zeilen
    return '\n'.join(zeilen)


def einsetzen(karte, berichtigt):
    """Ersetzt VORDERSEITE/RÜCKSEITE der Karte durch die berichtigte Fassung."""
    if not berichtigt or berichtigt.strip() in ('–', '-'):
        return karte, False
    # die letzte Karte einer Prüfdatei: Trennlinie und ÜBERSICHT gehören nicht zur Berichtigung
    berichtigt = re.split(r'^(?:---\s*$|## )', berichtigt, flags=re.M)[0]
    # Rückseite in derselben Zeile wie die Vorderseite (Vörstetten 5, Kloster Marienhaus 1): als eigenes Feld lesen
    if not re.search(r'^RÜCKSEITE:', berichtigt, flags=re.M):
        berichtigt = re.sub(r'[ \t]*[—–-]?[ \t]*RÜCKSEITE:', '\nRÜCKSEITE:', berichtigt, count=1)
        berichtigt = re.sub(r'\s+/\s+Quelle:', '\nQuelle:', berichtigt)
    alte_optionen = [z.strip() for z in feld(karte, 'VORDERSEITE').split('\n') if OPT.match(z.strip())]
    rueck_neu = re.search(r'^RÜCKSEITE:[ \t]*(.*?)(?=^VORDERSEITE:|\Z)', berichtigt, flags=re.S | re.M)
    rueck_neu = rueck_neu.group(1).strip().lstrip('„') if rueck_neu else ''
    rueck_tauglich = rueck_neu.startswith('Du hattest') and re.search(r'Richtig war|Die Lüge war|bis Stufe', rueck_neu)
    geaendert = False
    for name in ('VORDERSEITE', 'RÜCKSEITE'):
        m = re.search(r'^%s:[ \t]*(.*?)(?=^(?:VORDERSEITE|RÜCKSEITE):|\Z)' % name, berichtigt, flags=re.S | re.M)
        # "RÜCKSEITE: –" heißt: diese Seite bleibt, wie sie ist
        if not m or m.group(1).strip() in ('', '–', '-'):
            continue
        neu = m.group(1).strip()
        alt = feld(karte, name)
        # Anführungszeichen um die berichtigte Rückseite („Du hattest … Richtig war 3.“) gehören nicht zum Text (Kestert, Mainz,
        # Rüsselsheim; sonst zeigte der Prototyp „Du hattest [Option] getippt.“ wörtlich)
        if name == 'RÜCKSEITE' and neu.startswith('„'):
            neu = re.sub(r'“(?=\s*(?:Quelle:|$))', '', neu[1:], count=1)
            neu = re.sub(r'\s+Quelle:', '\nQuelle:', neu, count=1)
        # Eine echte Rückseite beginnt mit „Du hattest“. Schreibt die Prüfstufe stattdessen eine Anweisung („unverändert …“,
        # „Der Text bleibt gleich, nur die Quellenzeile lautet …“; Augsburg 1, Olching 5, 2026-10-12), bleibt der alte Text
        # stehen; eine neue Quellenzeile wird übernommen
        if name == 'RÜCKSEITE' and not neu.startswith('Du hattest') and alt.startswith('Du hattest'):
            q = re.search(r'Quelle:[^\n]*', neu)
            text_alt = alt[:alt.index('Quelle:')].rstrip() if 'Quelle:' in alt else alt.rstrip()
            neu = text_alt + '\n' + (q.group(0) if q else (alt[alt.index('Quelle:'):] if 'Quelle:' in alt else ''))
        if name == 'RÜCKSEITE' and 'Quelle:' not in neu and 'Quelle:' in alt:
            neu += '\n' + alt[alt.index('Quelle:'):]
        if name == 'VORDERSEITE':
            neu = vorderseite_ordnen(neu, alt)
            # neue Antworten brauchen eine vollständige neue Rückseite (die Lösungsstelle kann sich verschoben haben);
            # fehlt sie (Stufe 2 brach ab: Kloster Marienhaus 1), ist die Berichtigung nicht einsetzbar
            if [z for z in neu.split('\n') if OPT.match(z)] != alte_optionen and not rueck_tauglich:
                return karte, False
            # Form prüfen: Ort, Steckbrief, eine Frage, Antworten 1, 2, 3 … ohne Lücke (nur einzelne Optionen berichtigt:
            # Weststadt 7, Mettmann 3, Hardert 3 → nicht einsetzbar)
            z = [x for x in neu.split('\n') if x.strip()]
            nummern = [int(x[0]) for x in z[2:] if OPT.match(x)]
            frage = [x for x in z[2:] if not OPT.match(x)]
            if len(z) < 5 or not frage or nummern != list(range(1, len(nummern) + 1)) or len(nummern) < 3 or '“ „' in neu:
                return karte, False
            # Anweisungsreste der Prüfstufe in der Frage („Optionen 1, 3 und 4 bleiben, Option 2 neu“, Bad Wörishofen 5):
            # nicht einsetzbar, die Karte bleibt in der Urfassung und läuft als „unsicher“
            if re.search(r'\bneu:|unverändert|(?:Optionen|Antworten)\s+bleiben|RÜCKSEITE|\bOption(?:en)?\s*\d|lautet:\s*„|^[…/]|\(\s*$',
                         ' '.join(frage)):
                return karte, False
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
    vorrat, summe, orte_lauf = [], {}, set()
    for slug, rolle, name, _, _ in conf['orte']:
        pfad = os.path.join(RAUM, 'karten-v0.8' + TAG, slug + '.md')
        if rolle != 'ziel' or not os.path.exists(pfad) or not os.path.exists(os.path.join(RAUM, 'pruefung-v0.1' + TAG, slug + '.md')):
            continue
        orte_lauf.add(slug)
        roh = lies(pfad)
        kopf, _, rest = roh.partition('## Karte ')
        # v0.9: STECKBRIEF steht vor ORTS-ANSCHLUSS; beides gehört in den Schluss, nicht in die letzte Karte
        schluss = re.search(r'^## (?:STECKBRIEF|ORTS-ANSCHLUSS).*', roh, flags=re.S | re.M)
        karten = abschnitte(re.split(r'^## (?:STECKBRIEF|ORTS-ANSCHLUSS)', roh, flags=re.M)[0])
        p1 = abschnitte(lies(os.path.join(RAUM, 'pruefung-v0.1' + TAG, slug + '.md')))
        p2 = abschnitte(lies(os.path.join(RAUM, 'stufe2-v0.1' + TAG, slug + '.md'))) if os.path.exists(os.path.join(RAUM, 'stufe2-v0.1' + TAG, slug + '.md')) else {}
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
    pfad_v = os.path.join(RAUM, 'vorrat-liste.json')
    if LAUF != 'v0.8' and os.path.exists(pfad_v):
        # Zusammenführen: Orte dieses Laufs ersetzen ihre älteren Karten, alle anderen Orte bleiben. Eine Vertiefung
        # (Lauf …-tief, Freiburg 2026-10-27) ersetzt nur ihre eigenen früheren Zusatzkarten; umgekehrt bleiben Zusatzkarten
        # stehen, wenn der Hauptlauf eines Orts neu geprüft wird.
        zusatz = '-tief' in LAUF   # auch weitere Runden (v0.9-tief2)
        alt = [v for v in json.loads(lies(pfad_v)) if v['ort'] not in orte_lauf
               or (v['lauf'] != LAUF if zusatz else '-tief' in v['lauf'])]
        vorrat = alt + vorrat
    with io.open(pfad_v, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(vorrat, f, ensure_ascii=False, indent=1)
    kur = os.path.join(RAUM, 'kuratierung.json')
    if not os.path.exists(kur):
        with io.open(kur, 'w', encoding='utf-8', newline='\n') as f:
            json.dump({'_doc': 'Kuratierung Raum bahn: noch keine (Mike hat nichts gestrichen).', 'kartensatz': {}}, f, ensure_ascii=False, indent=1)
    print('Urteile:', summe, '| im Vorrat:', len(vorrat), 'Karten an', len(set(v['ort'] for v in vorrat)), 'Orten')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
