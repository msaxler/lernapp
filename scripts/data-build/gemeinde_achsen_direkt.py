"""Gemeinde-Achsen: Modellstufen als direkter, isolierter Aufruf (Kosten-Pareto H2; Spielkonzept v0.3.1 §8 Nr. 9).

Je Ort ein `claude -p` ohne Werkzeuge, in einem leeren Arbeitsordner außerhalb des Repos (kein Projektgedächtnis),
mit Tokenzählung aus der JSON-Ausgabe. Stufen:
  extraktion  Prompt <raum>/prompt-stufe1-v0.6.txt, Eingabe quellen-amtlich/<slug>.txt; bei dünner amtlicher Quelle
              (unter WIKI_AB Zeichen) kommt der Wikipedia-Text als eigener Abschnitt dazu. Ausgabe extraktion/<slug>.txt
  karten      Prompt <raum>/prompt-karten-v0.8.txt, Eingabe eingabe-v0.8/<slug>.txt. Ausgabe karten-v0.8/<slug>.md
  pruefung    Prompt <raum>/prompt-pruefung-v0.1.txt (Prüfstufe 1: Abgleich mit dem Quelltext, ohne Netz), Eingabe
              Karten + Quelltexte. Ausgabe pruefung-v0.1/<slug>.md
  stufe2      Prompt <raum>/prompt-stufe2-v0.1.txt (Prüfstufe 2: Netzsuche, nur WebSearch und WebFetch erlaubt), Eingabe
              nur die Karten, die Stufe 1 mit URTEIL stufe2 weitergereicht hat, samt dem, was offen ist. Orte ohne solche
              Karten laufen nicht. Ausgabe stufe2-v0.1/<slug>.md
  gegenprobe  Prompt <raum>/prompt-gegenprobe-v0.1.txt: volle Netzprüfung der Karten, die gegenprobe-auswahl.json für
              den Ort nennt (Stichprobe aus den in Stufe 1 bestätigten). Ausgabe gegenprobe-v0.1/<slug>.md
Aufwand je Aufruf: <raum>/aufwand/<stufe>[-<tag>]-<slug>.json (Modell, Token, Kosten, Dauer).
--tag X hängt X an die Ordner der Karten und Prüfungen (karten-v0.8-X, pruefung-v0.1-X): derselbe Ablauf mit
einem anderen Modell, ohne die erste Fassung zu überschreiben.

Aufruf:  GA_RAUM=bahn python -X utf8 scripts/data-build/gemeinde_achsen_direkt.py <stufe> [--model haiku] [--parallel 4] [slugs]
"""
import concurrent.futures
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAUM = os.path.join(WURZEL, 'data', 'gemeinde-achsen', os.environ.get('GA_RAUM', 'iter1'))
WIKI_AB = 12000
VERBOTEN = 'Bash,Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Agent,Task,NotebookEdit,TodoWrite'
STUFEN = {
    'extraktion': ('prompt-stufe1-v0.6.txt', 'extraktion', '.txt'),
    # GA_PROMPT_KARTEN / GA_PROMPT_PRUEFUNG wählen eine spätere Prompt-Fassung (v0.8.1, v0.2: Zahlenregel nach der
    # Gegenprobe, Mike 2026-10-03); die Ausgabeordner bleiben, die Fassung steht im Aufwand-Protokoll
    'karten': (os.environ.get('GA_PROMPT_KARTEN', 'prompt-karten-v0.8.txt'), 'karten-v0.8', '.md'),
    'pruefung': (os.environ.get('GA_PROMPT_PRUEFUNG', 'prompt-pruefung-v0.1.txt'), 'pruefung-v0.1', '.md'),
    'stufe2': ('prompt-stufe2-v0.1.txt', 'stufe2-v0.1', '.md'),
    'gegenprobe': ('prompt-gegenprobe-v0.1.txt', 'gegenprobe-v0.1', '.md'),
}
TAG = ''   # main() setzt '-<tag>'


def kd(name):
    """Ordner einer Fassung: karten-v0.8, pruefung-v0.1, stufe2-v0.1 mit Tag."""
    return name + TAG
# Prüfstufe 2 darf ins Netz, sonst nichts
VERBOTEN_STUFE2 = 'Bash,Read,Write,Edit,Glob,Grep,Agent,Task,NotebookEdit,TodoWrite'


def abschnitte(text):
    """'## Karte N'-Abschnitte einer Datei als {N: Text}."""
    teile = re.split(r'^## Karte (\d+)\s*$', text, flags=re.M)
    return dict((int(teile[i]), teile[i + 1].strip()) for i in range(1, len(teile) - 1, 2))


def offen_stufe2(slug):
    pr = abschnitte(lies(os.path.join(RAUM, kd('pruefung-v0.1'), slug + '.md')))
    return sorted(n for n, t in pr.items() if re.search(r'^URTEIL:\s*stufe2', t, flags=re.M | re.I))


def lies(p):
    with io.open(p, encoding='utf-8') as f:
        return f.read()


def eingabe(stufe, slug, name, titel):
    if stufe == 'extraktion':
        t = lies(os.path.join(RAUM, 'quellen-amtlich', slug + '.txt'))
        wiki = os.path.join(RAUM, 'quellen', slug + '.txt')
        if len(t) < WIKI_AB and os.path.exists(wiki):
            t += '\n\n=== QUELLE: https://de.wikipedia.org/wiki/%s | Wikipedia ===\n%s' % (titel.replace(' ', '_'), lies(wiki))
        return t
    if stufe == 'karten':
        return lies(os.path.join(RAUM, 'eingabe-v0.8', slug + '.txt'))
    if stufe == 'stufe2':
        karten = abschnitte(lies(os.path.join(RAUM, kd('karten-v0.8'), slug + '.md')))
        pr = abschnitte(lies(os.path.join(RAUM, kd('pruefung-v0.1'), slug + '.md')))
        return '\n\n'.join('## Karte %d\n%s\n\nOFFEN NACH STUFE 1:\n%s' % (n, karten.get(n, ''), pr[n]) for n in offen_stufe2(slug))
    if stufe == 'gegenprobe':
        karten = abschnitte(lies(os.path.join(RAUM, kd('karten-v0.8'), slug + '.md')))
        return '\n\n'.join('## Karte %s %d\n%s' % (name, n, karten[n]) for n in auswahl(slug))
    if stufe == 'pruefung':
        return ('=== KARTEN ===\n' + lies(os.path.join(RAUM, kd('karten-v0.8'), slug + '.md')) +
                '\n\n=== FAKTEN, AUS DENEN DIE KARTEN GEBAUT SIND ===\n' + lies(os.path.join(RAUM, 'eingabe-v0.8', slug + '.txt')) +
                '\n\n=== QUELLTEXTE ===\n' + lies(os.path.join(RAUM, 'quellen-amtlich', slug + '.txt')))


def auswahl(slug):
    pfad = os.path.join(RAUM, 'gegenprobe-auswahl.json')
    return json.loads(lies(pfad)).get(slug, []) if os.path.exists(pfad) else []


def umgebung():
    env = dict(os.environ)
    for k in list(env):
        if (k.startswith('CLAUDE_CODE_') and k != 'CLAUDE_CODE_GIT_BASH_PATH') or k in (
                'ANTHROPIC_BASE_URL', 'CLAUDECODE', 'CLAUDE_AGENT_SDK_VERSION'):
            del env[k]
    env['CLAUDE_CODE_GIT_BASH_PATH'] = r'D:\Programme\Git\bin\bash.exe'
    return env


def lauf(stufe, slug, name, titel, modell):
    prompt_datei, ordner, endung = STUFEN[stufe]
    if stufe in ('karten', 'pruefung', 'stufe2'):
        ordner = kd(ordner)
    anleitung = lies(os.path.join(RAUM, prompt_datei)).replace('{ORTSNAME}', name)
    text = ('Du bekommst eine Anleitung und eine Eingabe. Arbeite genau nach der Anleitung. Gib nur die Ausgabe im '
            'verlangten Format zurück, ohne Vorrede.\n\n=== ANLEITUNG ===\n' + anleitung + '\n\n=== EINGABE ===\n' +
            eingabe(stufe, slug, name, titel))
    if stufe == 'stufe2' and not offen_stufe2(slug):
        return slug, {'fehler': 'keine Karte an Stufe 2 – kein Lauf'}
    if stufe == 'gegenprobe' and not auswahl(slug):
        return slug, {'fehler': 'keine Karte in der Stichprobe – kein Lauf'}
    arbeit = tempfile.mkdtemp(prefix='qa-direkt-')
    t0 = time.time()
    netz = stufe in ('stufe2', 'gegenprobe')
    verboten = VERBOTEN_STUFE2 if netz else VERBOTEN
    werkzeug = ['--allowedTools', 'WebSearch,WebFetch'] if netz else []
    p = subprocess.run(['claude.cmd', '-p', '--model', modell, '--output-format', 'json', '--disallowedTools', verboten] + werkzeug,
                       input=text.encode('utf-8'), capture_output=True, cwd=arbeit, env=umgebung(), timeout=3600)
    dauer = time.time() - t0
    try:
        d = json.loads(p.stdout.decode('utf-8', 'replace'))
    except ValueError:
        return slug, {'fehler': (p.stderr or p.stdout).decode('utf-8', 'replace')[:500]}
    os.makedirs(os.path.join(RAUM, ordner), exist_ok=True)
    with io.open(os.path.join(RAUM, ordner, slug + endung), 'w', encoding='utf-8', newline='\n') as f:
        f.write(d.get('result', '') + '\n')
    u = d.get('usage', {})
    a = {'stufe': stufe + TAG, 'ort': slug, 'prompt': prompt_datei, 'modell_wunsch': modell, 'modelle': list((d.get('modelUsage') or {}).keys()),
         'eingabe_zeichen': len(text), 'token_ein': u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) +
         u.get('cache_read_input_tokens', 0), 'token_aus': u.get('output_tokens', 0), 'usage': u,
         'kosten_usd': d.get('total_cost_usd'), 'sekunden': round(dauer), 'fehler': d.get('is_error'),
         'zeit': time.strftime('%Y-%m-%dT%H:%M:%S')}
    os.makedirs(os.path.join(RAUM, 'aufwand'), exist_ok=True)
    with io.open(os.path.join(RAUM, 'aufwand', '%s%s-%s.json' % (stufe, TAG, slug)), 'w', encoding='utf-8') as f:
        json.dump(a, f, ensure_ascii=False, indent=1)
    return slug, a


def main():
    global TAG
    args = sys.argv[1:]
    stufe = args.pop(0)
    modell, parallel = 'haiku', 4
    if '--model' in args:
        i = args.index('--model'); modell = args[i + 1]; del args[i:i + 2]
    if '--parallel' in args:
        i = args.index('--parallel'); parallel = int(args[i + 1]); del args[i:i + 2]
    if '--tag' in args:
        i = args.index('--tag'); TAG = '-' + args[i + 1]; del args[i:i + 2]
    conf = json.loads(lies(os.path.join(RAUM, 'orte.json')))
    orte = [(s, n, t) for s, r, n, t, _ in conf['orte'] if r == 'ziel' and (not args or s in args)]
    with concurrent.futures.ThreadPoolExecutor(parallel) as ex:
        for slug, a in ex.map(lambda o: lauf(stufe, o[0], o[1], o[2], modell), orte):
            if 'token_ein' in a:
                print('%-20s %-10s ein %6d  aus %6d  %5.2f USD  %4d s  %s' % (slug, stufe, a['token_ein'], a['token_aus'],
                      a['kosten_usd'] or 0, a['sekunden'], ','.join(a['modelle'])), flush=True)
            else:
                print('%-20s FEHLER %s' % (slug, a['fehler']), flush=True)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
