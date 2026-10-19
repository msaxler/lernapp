"""Wahlbeteiligungs-Karten ohne deutlichen Abstand zum Landeswert aus dem Prototyp nehmen (Mike 2026-10-19).
Ohne Modell: trägt je Raum in kuratierung.json unter "raus" die Karten ein, die quizaway_prototyp_export.py dann
überspringt. Schwelle wie in gemeinde_achsen_karten_eingabe.py (WB_SCHWELLE). Mehrfach aufrufbar (ersetzt nur die
Einträge mit diesem Grund).
Aufruf: python -X utf8 scripts/data-patch/wahlbeteiligung_raus_2026-10-19.py [--probe]
"""
import io, json, os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GA = os.path.join(WURZEL, 'data', 'gemeinde-achsen')
GRUND = 'Wahlbeteiligung unauffällig gegen den Landeswert (Regel 2026-10-19)'
sys.path.insert(0, os.path.join(WURZEL, 'scripts', 'data-build'))
os.environ.setdefault('GA_RAUM', 'bahn')
from gemeinde_achsen_karten_eingabe import wahlbeteiligung_land, WB_SCHWELLE  # noqa: E402

probe = '--probe' in sys.argv
with io.open(os.path.join(WURZEL, 'apps', 'quizaway-reise', 'daten.js'), encoding='utf-8') as f:
    t = f.read()
daten = json.loads(re.search(r'=\s*(\{.*)', t, re.S).group(1).rstrip().rstrip(';'))
gesamt = 0
for raum in daten['raeume']:
    pfad_g = os.path.join(GA, raum['id'], 'grunddaten.json')
    with io.open(pfad_g, encoding='utf-8') as f:
        grund = {o['slug']: o for o in json.load(f)['orte']}
    pfad_k = os.path.join(GA, raum['id'], 'kuratierung.json')
    with io.open(pfad_k, encoding='utf-8') as f:
        kur = json.load(f)
    raus = {slug: [e for e in liste if e.get('grund') != GRUND] for slug, liste in kur.get('raus', {}).items()}
    n = 0
    for o in raum['orte']:
        for k in o['karten']:
            if 'Wahlbeteiligung' not in k['frage']:
                continue
            wl = wahlbeteiligung_land(grund[o['slug']])
            if wl and abs(wl[0] - wl[1]) >= WB_SCHWELLE:
                continue
            slug, lauf, nr = k['id'].split('/')
            raus.setdefault(slug, []).append({'lauf': lauf, 'karte': int(nr), 'grund': GRUND,
                                              'wert': wl[0] if wl else None, 'land': wl[1] if wl else None})
            n += 1
    raus = {s: l for s, l in raus.items() if l}
    kur['raus'] = raus
    kur['_doc_raus'] = ('Herausnahme ohne Modell: je Ort Liste {lauf, karte, grund}; quizaway_prototyp_export.py überspringt '
                        'diese Karten. Schwelle Wahlbeteiligung: %s Punkte gegen den Landeswert.' % WB_SCHWELLE)
    print('%-8s %3d Karten raus' % (raum['id'], n))
    gesamt += n
    if not probe:
        with io.open(pfad_k, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(kur, f, ensure_ascii=False, indent=1)
            f.write('\n')
print('gesamt', gesamt, '(Probe, nichts geschrieben)' if probe else 'geschrieben')
