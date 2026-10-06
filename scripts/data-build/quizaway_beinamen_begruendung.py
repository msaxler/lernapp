"""QuizAway Grundversorgung: kurze Begründung je amtlichem Beinamen (Mike 2026-10-07: „kurze Begründung für die 153
Beinamen => OK“).

Je Aufruf zehn Orte, Opus 5.5 mit Websuche (nur WebSearch und WebFetch erlaubt), in einem leeren Arbeitsordner.
Ausgabe je Ort: ein Satz (höchstens 25 Wörter), warum der Ort den Beinamen trägt, eine Quellenadresse und ob der Grund
belegt ist. Unbelegte Begründungen nimmt der Prototyp nicht (Karte bleibt dann ohne Begründung).
Schreibt data/grundversorgung/beinamen-begruendung.json: {ags: {"beiname", "satz", "quelle", "belegt"}} und je Aufruf
den Aufwand nach data/grundversorgung/aufwand-beinamen/.

Aufruf:  python -X utf8 scripts/data-build/quizaway_beinamen_begruendung.py [--parallel 4]
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
GRUND = os.path.join(WURZEL, 'apps', 'quizaway-reise', 'grund-de.js')
ZIEL = os.path.join(WURZEL, 'data', 'grundversorgung', 'beinamen-begruendung.json')
AUFWAND = os.path.join(WURZEL, 'data', 'grundversorgung', 'aufwand-beinamen')
MODELL = 'claude-opus-5-5'
VERBOTEN = 'Bash,Read,Write,Edit,Glob,Grep,Agent,Task,NotebookEdit,TodoWrite'
PROMPT = """Du schreibst Rückseiten für ein Reise-Quiz. Zu jedem Ort unten steht sein amtlicher Beiname (Zusatzbezeichnung im
Verzeichnis der Verwaltungsgebiete). Schreibe je Ort EINEN Satz auf Deutsch, höchstens 25 Wörter, der sagt, warum der Ort
diesen Beinamen trägt – so, dass man beim Vorlesen „ach so!“ denkt. Prüfe den Grund per Websuche (Gemeinde-Webseite,
Landesportal, seriöse Presse; Wikipedia nur als Wegweiser). Regeln:
- nur belegte Tatsachen; keine Ausschmückung, keine Superlative ohne Beleg
- möglichst ohne Zahlen; eine Jahreszahl nur, wenn sie den Grund trägt
- nicht den Beinamen wörtlich wiederholen, sondern den Grund nennen (Personen, Werke, Ereignisse, Bauwerke)
- findest du keinen belastbaren Beleg: belegt = false und satz = ""
Antworte NUR mit einem JSON-Array, ein Objekt je Ort in derselben Reihenfolge:
[{"ags": "...", "satz": "...", "quelle": "https://...", "belegt": true}]

ORTE:
"""


def umgebung():
    env = dict(os.environ)
    for k in list(env):
        if (k.startswith('CLAUDE_CODE_') and k != 'CLAUDE_CODE_GIT_BASH_PATH') or k in (
                'ANTHROPIC_BASE_URL', 'CLAUDECODE', 'CLAUDE_AGENT_SDK_VERSION'):
            del env[k]
    env['CLAUDE_CODE_GIT_BASH_PATH'] = r'D:\Programme\Git\bin\bash.exe'
    return env


def orte():
    with io.open(GRUND, encoding='utf-8') as f:
        text = f.read()
    g = json.loads(text[text.index('{'):text.rstrip().rindex(';')])
    return [(a[0], a[1], g['laender'][a[0][:2]], a[10]) for a in g['g'] if len(a) > 10 and a[10]]


def lauf(nr, gruppe):
    try:
        return lauf_einmal(nr, gruppe)
    except Exception as e:   # ein kaputter Aufruf darf den Lauf nicht abbrechen; der Ort bleibt offen
        print('Gruppe %2d: Fehler %s' % (nr, str(e)[:100]), flush=True)
        return nr, [], 0


def lauf_einmal(nr, gruppe):
    eingabe = PROMPT + '\n'.join('- ags %s: %s (%s), Beiname „%s“' % x for x in gruppe)
    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        p = subprocess.run(['claude.cmd', '-p', '--model', MODELL, '--output-format', 'json', '--disallowedTools', VERBOTEN,
                            '--allowedTools', 'WebSearch,WebFetch'],
                           input=eingabe, capture_output=True, text=True, encoding='utf-8', cwd=tmp, env=umgebung(), timeout=1800)
    d = json.loads(p.stdout)
    os.makedirs(AUFWAND, exist_ok=True)
    with io.open(os.path.join(AUFWAND, 'gruppe-%02d.json' % nr), 'w', encoding='utf-8') as f:
        json.dump({'modelle': list((d.get('modelUsage') or {}).keys()), 'kosten_usd': d.get('total_cost_usd'),
                   'sekunden': round(time.time() - t0), 'fehler': d.get('is_error')}, f, ensure_ascii=False)
    # erstes vollständiges JSON-Array der Antwort (dahinter kann noch Text stehen, 2026-10-07)
    r = d.get('result', '')
    try:
        antw = json.JSONDecoder().raw_decode(r[r.index('['):])[0]
    except ValueError:
        antw = []
    return nr, antw, d.get('total_cost_usd') or 0


def main():
    par = int(sys.argv[sys.argv.index('--parallel') + 1]) if '--parallel' in sys.argv else 4
    alle = orte()
    vorher = {}
    if os.path.exists(ZIEL):
        with io.open(ZIEL, encoding='utf-8') as f:
            vorher = json.load(f)
    offen = [x for x in alle if x[0] not in vorher]
    gruppen = [offen[i:i + 10] for i in range(0, len(offen), 10)]
    print('%d Orte mit Beinamen, %d offen, %d Aufrufe' % (len(alle), len(offen), len(gruppen)), flush=True)
    beiname = {x[0]: x[3] for x in alle}
    summe = 0
    with concurrent.futures.ThreadPoolExecutor(par) as ex:
        # jede Gruppe speichern, sobald sie fertig ist (mit ex.map riss am 2026-10-07 ein Fehler in Gruppe 3 die fertigen
        # Gruppen 4-9 mit)
        for fut in concurrent.futures.as_completed([ex.submit(lauf, nr, g) for nr, g in enumerate(gruppen)]):
            nr, antw, usd = fut.result()
            summe += usd
            for e in antw:
                if e.get('ags') in beiname:
                    vorher[e['ags']] = {'beiname': beiname[e['ags']], 'satz': e.get('satz', ''), 'quelle': e.get('quelle', ''),
                                        'belegt': bool(e.get('belegt'))}
            with io.open(ZIEL, 'w', encoding='utf-8', newline='\n') as f:
                json.dump(vorher, f, ensure_ascii=False, indent=1)
            print('Gruppe %2d: %d Antworten, %.2f USD' % (nr, len(antw), usd), flush=True)
    print('belegt: %d von %d; Kosten %.2f USD' % (sum(1 for v in vorher.values() if v['belegt']), len(vorher), summe))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
