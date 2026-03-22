"""
Quiz Away — Fragen in HTML einbauen
====================================
Liest fragen.json und ersetzt den FRAGEN-Block in quizaway_v2.html.

Aufruf:
  python inject_questions.py
  python inject_questions.py --fragen fragen.json --html quizaway_v2.html --out quizaway_v2.html
"""

import json, re, argparse, shutil
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--fragen", default="fragen.json")
parser.add_argument("--html",   default="quizaway_v2.html")
parser.add_argument("--out",    default="quizaway_v2.html")
args = parser.parse_args()

# ── Fragen laden ───────────────────────────────────────────────────────────
with open(args.fragen, encoding="utf-8") as f:
    fragen = json.load(f)

print(f"📂  {len(fragen)} Fragen geladen aus {args.fragen}")

# ── HTML laden ─────────────────────────────────────────────────────────────
with open(args.html, encoding="utf-8") as f:
    html = f.read()

# ── Backup anlegen ─────────────────────────────────────────────────────────
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = args.html.replace(".html", f"_backup_{ts}.html")
shutil.copy(args.html, backup)
print(f"💾  Backup gespeichert: {backup}")

# ── FRAGEN-Block suchen ────────────────────────────────────────────────────
# Sucht: const FRAGEN = [ ... ];   (mehrzeilig)
pattern = re.compile(r'const FRAGEN\s*=\s*\[.*?\];', re.DOTALL)
match = pattern.search(html)

if not match:
    print("❌  FRAGEN-Block nicht gefunden! Abbruch.")
    exit(1)

print(f"🔍  FRAGEN-Block gefunden: Zeile {html[:match.start()].count(chr(10))+1} bis {html[:match.end()].count(chr(10))+1}")

# ── Neuen FRAGEN-Block zusammenbauen ──────────────────────────────────────
def js_str(s):
    """String für JavaScript escapen"""
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")

zeilen = ["const FRAGEN = ["]
for fq in fragen:
    falsch_js = ", ".join(f"'{js_str(x)}'" for x in fq["falsch"])
    zeile = (
        f"  {{ "
        f"id:'{fq['id']}', "
        f"kat:'{fq['kat']}', "
        f"sw:'{fq.get('sw','S')}', "
        f"stadt:'{js_str(fq['stadt'])}', "
        f"bl:'{js_str(fq['bl'])}', "
        f"frage:'{js_str(fq['frage'])}', "
        f"richtig:'{js_str(fq['richtig'])}', "
        f"falsch:[{falsch_js}], "
        f"erkl:'{js_str(fq['erkl'])}' "
        f"}},"
    )
    zeilen.append(zeile)

zeilen.append("];")
neuer_block = "\n".join(zeilen)

# ── Ersetzen ───────────────────────────────────────────────────────────────
html_neu = html[:match.start()] + neuer_block + html[match.end():]

# ── Google Fonts entfernen & Offline-Fallback sicherstellen ────────────────
import re as _re
html_neu = _re.sub(r"\s*@import url\('https://fonts\.googleapis[^']*'\);\n?", '', html_neu)
html_neu = html_neu.replace("font-family: 'DM Sans', sans-serif;",
                             "font-family: 'DM Sans', system-ui, -apple-system, sans-serif;")
html_neu = html_neu.replace("font-family: 'Bebas Neue', sans-serif;",
                             "font-family: 'Bebas Neue', system-ui, -apple-system, sans-serif;")

# ── Speichern ──────────────────────────────────────────────────────────────
with open(args.out, "w", encoding="utf-8") as f:
    f.write(html_neu)

# ── Statistik ──────────────────────────────────────────────────────────────
kat_count = {}
for fq in fragen:
    kat_count[fq["kat"]] = kat_count.get(fq["kat"], 0) + 1

print(f"\n✅  {args.out} aktualisiert — {len(fragen)} Fragen eingebaut")
print()
for kat, count in sorted(kat_count.items()):
    print(f"   {kat:6s}  {count:4d} Fragen")

print(f"\n🌐  Im Browser neu laden — fertig!")

import subprocess
subprocess.run(['py', '-3.11', 'check_quiz.py'])
