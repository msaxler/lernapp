#!/usr/bin/env python3
"""
check_quiz.py — Prüft quizaway_v5.html auf Konsistenz.
Aufruf: py check_quiz.py  (aus LernApp/ oder scripts/check/)
"""
import re, sys, json
from pathlib import Path

# Datei finden egal von wo aufgerufen
ROOT = Path(__file__).resolve().parent.parent.parent
HTML_PATH = ROOT / "apps" / "quizaway" / "quizaway_v5.html"
SW_PATH   = ROOT / "apps" / "quizaway" / "sw.js"
RV_PATH   = ROOT / "scripts" / "sync"  / "rendezvous.py"

# ============================================================
# Checks für quizaway_v5.html
# ============================================================
HTML_CHECKS = [

    # ── Grundstruktur ──
    ("Fragen aus SQL-Datenbank (sql.js)",
        'sql-wasm.js', True,
        "sql.js fehlt → Fragen können nicht aus Datenbank geladen werden"),

    ("5 Runden",
        "runde === 5", True,
        "Runden-Check fehlt für runde===5"),

    ("KEINE 7-Runden-Logik",
        "runde === 7", False,
        "Alter 7-Runden-Check noch vorhanden → auf 5 ändern"),

    # ── Timer ──
    ("Frage-Timer 14s",
        "timerSek = 14", True,
        "Frage-Timer ist nicht 14s"),

    ("Punkteformel 120 Punkte max",
        "vergangen - 3) * 7", True,
        "Punkteformel stimmt nicht → 120 - (vergangen-3)*7"),

    ("Feedback Auto-Weiter 14s",
        "starteAutoWeiter(14 * DEBUG_TIMER_FAKTOR, () => naechsteFrage()", True,
        "Feedback-Screen hat keinen 14s Auto-Weiter"),

    ("Rundenabschluss Auto-Weiter 14s",
        "starteAutoWeiter(14 * DEBUG_TIMER_FAKTOR, () => naechsteRunde()", True,
        "Rundenabschluss hat keinen 14s Auto-Weiter"),

    ("Warteraum-Timer 120s (JS)",
        "120 * (DEBUG_TIMER_FAKTOR", True,
        "Warteraum-Timer ist nicht 120s → sekEl = 120"),

    ("Warteraum-Timer 120s (HTML-Span)",
        ">120<", True,
        "Warteraum-Anzeige zeigt nicht 120"),

    # ── Auto-Weiter Infrastruktur ──
    ("stopAutoWeiter vorhanden",
        "function stopAutoWeiter()", True,
        "stopAutoWeiter() Funktion fehlt"),

    ("starteAutoWeiter vorhanden",
        "function starteAutoWeiter(", True,
        "starteAutoWeiter() Funktion fehlt"),

    # ── Kategorien ──
    ("3 Kategorien zur Auswahl (slice)",
        "slice(0, 3)", True,
        "Kategoriewahl zeigt nicht 3 Karten"),

    ("Kategorie dist vorhanden",
        "'dist'", True,
        "Kategorie 'dist' (Distanz & Lage) fehlt"),

    # ── Layout / CSS ──
    ("route-map-svg-wrap vorhanden",
        "route-map-svg-wrap", True,
        "route-map-svg-wrap Wrapper fehlt"),

    ("Screens overflow-y:scroll (iOS-Fix)",
        "overflow-y: scroll", True,
        ".screen hat kein overflow-y:scroll → iOS Safari kann nicht scrollen"),

    ("-webkit-overflow-scrolling touch",
        "-webkit-overflow-scrolling: touch", True,
        "Momentum-Scrolling für iOS fehlt"),

    ("#phone overflow:visible auf Mobile",
        "overflow: visible", True,
        "#phone hat kein overflow:visible in Mobile-Query → iOS Touch-Events blockiert"),

    ("min-height:100dvh",
        "min-height: 100dvh", True,
        "body hat kein min-height:100dvh → Dynamic-Viewport fehlt"),

    # ── Live-Modus ──
    ("zeigeLiveModus vorhanden",
        "function zeigeLiveModus()", True,
        "zeigeLiveModus() fehlt"),

    ("Live-Modus: liveSetGPS aktualisiert Karte (kein Auto-Start)",
        "liveUpdateKarte(lat, lon)", True,
        "liveSetGPS() aktualisiert Karte nicht — ruft stattdessen direkt liveStartQuiz() auf → Karte wird übersprungen"),

    ("Leaflet-Karte vorhanden",
        "L.map('live-map'", True,
        "Leaflet-Karte im Live-Modus fehlt"),

    # ── Duell / Relay ──
    ("duelNewPC vorhanden",
        "function duelNewPC()", True,
        "duelNewPC() Hilfsfunktion fehlt"),

    ("ICE_SERVERS definiert",
        "const ICE_SERVERS", True,
        "ICE_SERVERS Konstante fehlt"),

    ("Mindestens 2 STUN-Server",
        "stun:stun1.l.google.com", True,
        "Nur 1 STUN-Server konfiguriert"),

    ("TURN-Server konfiguriert",
        "turn:", True,
        "Kein TURN-Server konfiguriert"),

    ("activateRelayMode vorhanden",
        "async function activateRelayMode()", True,
        "activateRelayMode() Funktion fehlt"),

    ("relayPollLoop vorhanden",
        "async function relayPollLoop()", True,
        "relayPollLoop() Funktion fehlt"),

    ("Relay-Felder im duel-Objekt",
        "relayMode:", True,
        "relayMode fehlt im duel-Objekt"),

    ("relayId im duel-Objekt",
        "relayId:", True,
        "relayId fehlt im duel-Objekt"),

    ("duelAbgebrochen stoppt Relay",
        "duel.relayMode = false", True,
        "duelAbgebrochen() setzt relayMode nicht zurück → Poll-Loop läuft weiter"),

    ("dc.onclose: Relay-Guard",
        "if (duel.relayMode) return", True,
        "dc.onclose hat keinen Relay-Guard"),

    ("dc.onclose: Relay-Fallback bei aktivem Spiel",
        "DataChannel getrennt — versuche Relay-Fallback", True,
        "dc.onclose ruft activateRelayMode() nicht auf wenn Spiel aktiv"),

    ("ACK-basiertes Reliable Messaging",
        "function duelSendReliable(", True,
        "duelSendReliable() fehlt"),

    ("Duplikat-Schutz seenSeqs",
        "seenSeqs", True,
        "seenSeqs (Duplikat-Schutz) fehlt"),

    ("Ping-Timeout löst Relay aus",
        "activateRelayMode(); // sofort Relay", True,
        "Ping-Timeout aktiviert Relay nicht → Verbindungsverlust nach 30s"),

    ("Warteraum WARTERAUM_TTL",
        "WARTERAUM_TTL", False,  # steht in rendezvous.py, nicht im HTML
        ""),  # kein HTML-Check nötig

    # ── Service Worker ──
    ("SW registriert",
        "serviceWorker.register", True,
        "Service Worker wird nicht registriert"),

    # ── favicon ──
    ("Favicon-Link vorhanden",
        'rel="icon"', True,
        'favicon.ico 502 verhindern: <link rel="icon"> fehlt'),
]

# ============================================================
# Checks für sw.js
# ============================================================
SW_CHECKS = [
    ("Cache-Name v5",
        "quizaway-v5", True,
        "sw.js Cache-Name ist nicht v5 → alter Cache bleibt aktiv"),

    ("App-Shell: quizaway_v5.html",
        "quizaway_v5.html", True,
        "sw.js cached noch quizaway_v4.html statt v5"),

    ("API-Ausschluss /warteraum/",
        "pathname.startsWith('/warteraum/')", True,
        "/warteraum/ wird gecacht → Spielerliste veraltet"),

    ("API-Ausschluss /relay/",
        "pathname.startsWith('/relay/')", True,
        "/relay/ wird gecacht → Relay-Nachrichten gehen verloren"),

    ("API-Ausschluss /lobby/",
        "pathname.startsWith('/lobby/')", True,
        "/lobby/ wird gecacht → Duell-Signaling bricht"),

    ("API-Ausschluss /offer/ und /answer/",
        "pathname.startsWith('/offer/')", True,
        "/offer/ wird gecacht → WebRTC-Signaling bricht"),
]

# ============================================================
# Checks für rendezvous.py
# ============================================================
RV_CHECKS = [
    ("WARTERAUM_TTL = 150",
        "WARTERAUM_TTL = 150", True,
        "WARTERAUM_TTL ist nicht 150 → Spieler verschwinden zu früh/spät"),

    ("Relay-Store vorhanden",
        "relay_msgs", True,
        "relay_msgs fehlt → Server-Relay nicht implementiert"),

    ("POST /relay/.../init Handler",
        "relay/') and p.endswith('/init')", True,
        "POST /relay/{id}/init Handler fehlt"),

    ("POST /relay/.../send Handler",
        "relay/') and p.endswith('/send')", True,
        "POST /relay/{id}/send Handler fehlt"),

    ("GET /relay/ Short-Poll Handler",
        "p.startswith('/relay/') and p.count('/') == 2", True,
        "GET /relay/{id} Handler fehlt"),

    ("CORS-Header vorhanden",
        "Access-Control-Allow-Origin", True,
        "CORS fehlt → Browser blockiert API-Anfragen"),
]

# ============================================================
# Runner
# ============================================================
def run_checks(label, path, checks):
    print(f"\n── {label} ({('vorhanden' if path.exists() else '❌ FEHLT')}) ──")
    if not path.exists():
        print(f"  ❌  {path} nicht gefunden!")
        return 0, len(checks), [f"{path} fehlt"]
    content = path.read_text(encoding='utf-8')
    ok = 0
    fehler = []
    for eintrag in checks:
        if len(eintrag) == 4:
            beschreibung, suchstring, muss_vorhanden, meldung = eintrag
        else:
            continue
        if not beschreibung or not meldung and not muss_vorhanden:
            continue  # Platzhalter überspringen
        gefunden = suchstring in content
        korrekt = (gefunden == muss_vorhanden)
        status = '✅' if korrekt else '❌'
        note = '' if korrekt else f"  [{'vorhanden — sollte fehlen' if gefunden else 'fehlt'}]"
        print(f"  {status}  {beschreibung}{note}")
        if korrekt:
            ok += 1
        elif meldung:
            fehler.append(meldung)
    return ok, len([e for e in checks if e[3]]), fehler

def main():
    print("check_quiz.py — Konsistenzprüfung QuizAway v5")
    print("=" * 55)

    alle_fehler = []
    alle_ok = 0
    alle_total = 0

    ok, total, fehler = run_checks("quizaway_v5.html", HTML_PATH, HTML_CHECKS)
    alle_ok += ok; alle_fehler += fehler; alle_total += total

    ok, total, fehler = run_checks("sw.js", SW_PATH, SW_CHECKS)
    alle_ok += ok; alle_fehler += fehler; alle_total += total

    ok, total, fehler = run_checks("rendezvous.py", RV_PATH, RV_CHECKS)
    alle_ok += ok; alle_fehler += fehler; alle_total += total

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
