#!/usr/bin/env python3
"""
check_quiz.py — Prüft quizaway_v3.html und generate_questions.py auf Konsistenz.
Aufruf: py -3.11 check_quiz.py
"""
import re, sys, json
from pathlib import Path

HTML = Path("quizaway_v3.html")
GQ   = Path("generate_questions.py")

# ============================================================
# Checks für quizaway_v3.html
# ============================================================
HTML_CHECKS = [
    ("Frage-Timer 14s (JS)",
        "timerSek = 14", True,
        "Frage-Timer ist nicht 14s → state.timerSek = 14"),

    ("KEIN Frage-Timer 20s",
        "timerSek = 20", False,
        "Frage-Timer steht noch auf 20s → auf 14 ändern"),

    ("Feedback Auto-Weiter 14s",
        "starteAutoWeiter(14, () => naechsteFrage", True,
        "Feedback-Screen hat keinen 14s Auto-Weiter zu naechsteFrage()"),

    ("Rundenabschluss Auto-Weiter 14s",
        "starteAutoWeiter(14, () => naechsteRunde", True,
        "Rundenabschluss hat keinen 14s Auto-Weiter zu naechsteRunde()"),

    ("Kategoriewahl Auto-Weiter 14s",
        "starteAutoWeiter(14", True,
        "Kategoriewahl hat keinen 14s Auto-Weiter"),

    ("KEIN Rundenabschluss 10s",
        "starteAutoWeiter(10", False,
        "Rundenabschluss hat noch 10s statt 7s"),

    ("Kat-Timer Runde 1 = 14s, sonst 7s",
        "runde === 1 ? 28 : 14", True,
        "Kat-Timer ist nicht rundenabhängig → const katTimerSek = state.runde === 1 ? 28 : 14"),

    ("5 Runden (nicht 7)",
        "runde === 5", True,
        "Runden-Check fehlt für runde===5 → sollte 5 Runden sein"),

    ("KEINE 7-Runden-Logik",
        "runde === 7", False,
        "Runden-Check steht noch auf runde===7 → auf 5 ändern"),

    ("stopAutoWeiter vorhanden",
        "function stopAutoWeiter()", True,
        "stopAutoWeiter() Funktion fehlt"),

    ("starteAutoWeiter vorhanden",
        "function starteAutoWeiter(", True,
        "starteAutoWeiter() Funktion fehlt"),

    ("stopAutoWeiter in naechsteFrage",
        "naechsteFrage() {\n  stopAutoWeiter", True,
        "naechsteFrage() ruft stopAutoWeiter() nicht auf"),

    ("stopAutoWeiter in naechsteRunde",
        "naechsteRunde() {\n  stopAutoWeiter", True,
        "naechsteRunde() ruft stopAutoWeiter() nicht auf"),

    ("Kategorien slice(0,3)",
        "slice(0, 3)", True,
        "Kategoriewahl zeigt nicht 3 Karten (slice fehlt)"),

    ("Punkteformel 120 Punkte max",
        "vergangen - 3) * 7", True,
        "Punkteformel nicht aktuell → vergangen <= 3 ? 120 : Math.max(0, 120 - (vergangen - 3) * 7)"),

    ("vergangen auf 7s-Basis",
        "vergangen = 14 - state.timerSek", True,
        "vergangen-Berechnung noch auf alter Basis → 14 - state.timerSek"),

    # ── CSS / Layout ──
    ("route-map-svg-wrap vorhanden",
        "route-map-svg-wrap", True,
        "route-map-svg-wrap Wrapper fehlt → Karte läuft aus dem Bereich"),

    ("route-screen overflow:hidden",
        "overflow:hidden; box-sizing:border-box", True,
        "route-screen hat kein overflow:hidden → Inhalt läuft aus dem Screen"),

    ("route-map-wrap flex:1 min-height:0",
        "flex:1; min-height:0", True,
        "route-map-wrap hat kein flex:1 min-height:0 → Karte ignoriert Flex-Begrenzung"),

    ("Duell Kat-Timer rundenabhängig",
        "duellState.runde === 1 ? 28 : 14", True,
        "Duell Kat-Timer ist nicht rundenabhängig → duellState.runde === 1 ? 28 : 14"),

    ("Routen-Fallback kategorietreu",
        "f.kat === state.gewaehlteKat.id && !bereits.has", True,
        "Routen-Fallback filtert nicht nach Kategorie → falsche Kategorien möglich"),

    # ── Modus/Schwierigkeit-Anzeige ──
    ("frage-modus-badge vorhanden",
        "frage-modus-badge", True,
        "frage-modus-badge fehlt → Modus/Schwierigkeit nicht im Spielscreen sichtbar"),

    ("frage-modus-badge wird gesetzt",
        "frage-modus-badge').textContent", True,
        "frage-modus-badge wird in zeigeFrage() nicht gesetzt"),

    ("Modus-Label sofa/route/duell",
        "modus === 'sofa'  ? 'Sofa'", True,
        "Modus-Label für sofa/route/duell fehlt in zeigeFrage()"),
]

# ============================================================
# Checks für generate_questions.py
# ============================================================
GQ_CHECKS = [
    ("KFZ_KREISSTADT Tabelle vorhanden",
        "KFZ_KREISSTADT", True,
        "KFZ_KREISSTADT fehlt → patch_generate_kfz.py ausführen"),

    ("KFZ Erklärung nutzt _kfz_erkl()",
        "_kfz_erkl(kfz, name", True,
        "KFZ-Erklärung (Richtung 1) nutzt nicht _kfz_erkl() → patch_generate_kfz.py"),

    ("KFZ Erklärung nutzt _kfz_erkl2()",
        "_kfz_erkl2(kfz, name", True,
        "KFZ-Erklärung (Richtung 2) nutzt nicht _kfz_erkl2() → patch_generate_kfz.py"),

    ("SU → Siegburg in Tabelle",
        '"SU": "Siegburg"', True,
        'SU→Siegburg fehlt in KFZ_KREISSTADT'),


]

# ============================================================
# Fragen-JSON Checks
# ============================================================
def check_fragen():
    fragen_path = Path("fragen.json")
    results = []
    if not fragen_path.exists():
        results.append((False, "fragen.json vorhanden", "fragen.json fehlt → generate_questions.py ausführen"))
        return results
    try:
        fragen = json.loads(fragen_path.read_text(encoding='utf-8'))
    except Exception as e:
        results.append((False, "fragen.json lesbar", str(e)))
        return results

    results.append((True, f"fragen.json vorhanden ({len(fragen)} Fragen)", ""))

    kfz_fragen = [f for f in fragen if f['kat'] == 'kfz']
    # Prüfe ob noch alte Erklärungen drin sind
    alte_erkl = [f for f in kfz_fragen
                 if 'Zulassungsbereich' not in f.get('erkl','')
                 and f.get('erkl','').count(' ist das Kennzeichen für ') > 0]
    # Nur als Problem wenn viele betroffen (>30% der KFZ-Fragen ohne Zulassungsbereich-Hinweis)
    # — manche Städte sind selbst der Namenspatron, die haben keine Zulassungsbereich-Erwähnung
    ok = len(alte_erkl) < len(kfz_fragen) * 0.7
    results.append((ok,
        f"KFZ-Erklärungen enthalten Zulassungsbereich ({len(kfz_fragen)-len(alte_erkl)}/{len(kfz_fragen)} Fragen)",
        "Viele KFZ-Fragen ohne Zulassungsbereich-Hinweis → generate_questions.py neu ausführen"))

    # Kategorien-Verteilung
    from collections import Counter
    kat_count = Counter(f['kat'] for f in fragen)
    for kat, count in sorted(kat_count.items()):
        results.append((count >= 20,
            f"Kategorie '{kat}': {count} Fragen",
            f"Zu wenig Fragen für '{kat}' → generate_questions.py prüfen"))

    return results

# ============================================================
# Runner
# ============================================================
def run_checks(label, path, checks):
    print(f"\n── {label} ({'vorhanden' if path.exists() else 'FEHLT'}) ──")
    if not path.exists():
        print(f"  ❌  {path} nicht gefunden!")
        return 0, [f"{path} fehlt"]
    content = path.read_text(encoding='utf-8')
    ok = 0
    fehler = []
    for beschreibung, suchstring, muss_vorhanden, meldung in checks:
        gefunden = suchstring in content
        korrekt = (gefunden == muss_vorhanden)
        status = '✅' if korrekt else '❌'
        note = '' if korrekt else f"  [{'vorhanden — sollte fehlen' if gefunden else 'fehlt'}]"
        print(f"  {status}  {beschreibung}{note}")
        if korrekt:
            ok += 1
        else:
            fehler.append(meldung)
    return ok, fehler

def main():
    print("check_quiz.py — Konsistenzprüfung Quiz Away")
    print("=" * 55)

    alle_fehler = []
    alle_ok = 0
    alle_total = 0

    # HTML
    ok, fehler = run_checks("quizaway_v3.html", HTML, HTML_CHECKS)
    alle_ok += ok; alle_fehler += fehler; alle_total += len(HTML_CHECKS)

    # generate_questions.py
    ok, fehler = run_checks("generate_questions.py", GQ, GQ_CHECKS)
    alle_ok += ok; alle_fehler += fehler; alle_total += len(GQ_CHECKS)

    # fetch_staedte.py
    fs = Path("fetch_staedte.py")
    print(f"\n── fetch_staedte.py ──")
    if fs.exists():
        fs_c = fs.read_text(encoding='utf-8')
        ars_ok = "'ars':" in fs_c and "d['ars']" in fs_c
        print(f"  {'✅' if ars_ok else '❌'}  ars-Feld wird in staedte.json gespeichert")
        if not ars_ok:
            alle_fehler.append("fetch_staedte.py speichert 'ars' nicht → patch_fetch_staedte.py ausführen")
        else:
            alle_ok += 1
        alle_total += 1
    else:
        print(f"  ⚠️   fetch_staedte.py nicht gefunden (übersprungen)")

    # fragen.json
    print(f"\n── fragen.json ──")
    for korrekt, beschreibung, meldung in check_fragen():
        print(f"  {'✅' if korrekt else '❌'}  {beschreibung}")
        if not korrekt:
            alle_fehler.append(meldung)
        else:
            alle_ok += 1
        alle_total += 1

    # Zusammenfassung
    print(f"\n{'=' * 55}")
    print(f"  {alle_ok}/{alle_total} Checks bestanden")

    if alle_fehler:
        print(f"\n⚠️  {len(alle_fehler)} Problem(e):\n")
        for f in alle_fehler:
            print(f"  → {f}")
        print()
        sys.exit(1)
    else:
        print("\n✅  Alles OK!\n")
        sys.exit(0)

if __name__ == '__main__':
    main()
