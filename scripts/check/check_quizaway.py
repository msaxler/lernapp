# -*- coding: utf-8 -*-
"""
check_quizaway.py — Smoke-Test für quizaway_v4.html
Prüft ob alle wesentlichen Strukturen, Funktionen und IDs noch vorhanden sind.
Aufruf: python check_quizaway.py
"""
import re, sys

FILE = 'quizaway_v4.html'
ok = 0
fail = 0

def check(label, condition, detail=''):
    global ok, fail
    if condition:
        print(f"  ✓  {label}")
        ok += 1
    else:
        print(f"  ✗  {label}" + (f"  [{detail}]" if detail else ''))
        fail += 1

html = open(FILE, encoding='utf-8').read()
print(f"=== QuizAway Smoke-Test ({FILE}) ===\n")

# ─── Screens ──────────────────────────────────────────────────────────────
print("Screens:")
for s in ['screen-start','screen-schwierigkeit','screen-kategorie','screen-frage',
          'screen-feedback','screen-runde','screen-ende',
          'screen-route','screen-duell-start','screen-duell-kat',
          'screen-duell-warteraum','screen-duell-ergebnis',
          'screen-liga','screen-profil','screen-rangliste']:
    check(s, f'id="{s}"' in html)

# ─── Kern-Funktionen ──────────────────────────────────────────────────────
print("\nKern-Funktionen:")
for fn in ['ladeDB','zeigeFrage','zeigeFeedback','naechsteFrage','naechsteRunde',
           'antwortGewaehlt','zeitAbgelaufen','starteAutoWeiter','stopAutoWeiter',
           'zeigeSchwierigkeit','schwierWaehle','schwierWeiter',
           'zeigeKategoriewahl','katGewaehlt',
           'zeigeDuellKat','zeigeDuellKat','duellKatGewaehlt','duellScreenInit','duellStart',
           'zeigeDuellErgebnis','generiereGegner',
           'lobbyOeffnen','lobbyListe','lobbyAngebotErstellen','lobbyBeitreten',
           'duelStarteRunde','duelKatBestaetigen','duelRundeAbgeschlossen',
           'duelZeigeVergleich','duelNaechsteRunde','duelZeigeEndergebnis',
           'generiereGeoFragen','generiereHoeheFragen','generiereEwFragen',
           'generiereKfzFragen','generiererPlzFragen',
           'showScreen','spielerNameLaden','spielerNameAendern',
           'p2pHost','p2pJoin']:
    check(fn, f'function {fn}(' in html or f'function {fn} (' in html)

# ─── Wichtige IDs ─────────────────────────────────────────────────────────
print("\nWichtige Element-IDs:")
for eid in ['db-status','gegner-preview','kat-cards','duell-kat-cards',
            'naechste-runde-btn','duell-runden-label','duell-runden-reveal',
            'dsb-me','dsb-opp','lobby-liste','lobby-create-section','lobby-warte-section',
            'p2p-log','p2p-status','schwier-auto-hinweis','kat-auto-hinweis',
            'kat-sub-label','duell-guest-warte','drr-me-punkte','drr-opp-punkte']:
    check(eid, f'id="{eid}"' in html or f"getElementById('{eid}')" in html)

# ─── Spieler-Name-Anzeige ─────────────────────────────────────────────────
print("\nSpielername:")
check('class spieler-name-anzeige vorhanden', 'spieler-name-anzeige' in html)
check('spielerNameLaden() Aufruf', 'spielerNameLaden()' in html)
check('localStorage quizaway_spielername', 'quizaway_spielername' in html)

# ─── KFZ / PLZ Kategorien ─────────────────────────────────────────────────
print("\nKategorien:")
for kat in ["id: 'geo'", "id: 'hoehe'", "id: 'ew'", "id: 'kfz'", "id: 'plz'"]:
    check(kat, kat in html)
check("bahn locked:true", "id: 'bahn'" in html and "locked: true" in html)

# ─── Duell State & Protokoll ──────────────────────────────────────────────
print("\nDuell P2P:")
check('duel State definiert', 'let duel = {' in html)
check('TURN-Server OpenRelay', 'openrelay.metered.ca' in html)
check('RENDEZVOUS dynamisch', 'location.hostname' in html and 'RENDEZVOUS' in html)
check('duelSetupDC', 'function duelSetupDC(' in html)
check('duelHandleMsg', 'function duelHandleMsg(' in html)
check('Ping-Timer', 'pingTimer' in html)
check('abbruchTimer', 'abbruchTimer' in html)

# ─── Rendezvous / Lobby Endpunkte ─────────────────────────────────────────
print("\nLobby-Endpunkte (HTML):")
for ep in ['/lobby/create', '/lobby/join/', '/lobby/status/', '/lobby/cancel/', '/lobby/offer/']:
    check(ep, ep in html)

# ─── Lobby URL-Konsistenz ─────────────────────────────────────────────────
print("\nLobby URL-Konsistenz:")
check("Guest holt Offer über /lobby/offer/ (nicht /offer/)",
      "rendezvousFetch('/lobby/offer/'" in html or "RENDEZVOUS + '/lobby/offer/'" in html)
check("Host speichert Offer über /lobby/offer/",
      "'/lobby/offer/' + data.id" in html or "RENDEZVOUS + '/lobby/offer/' + aid" in html)
check("Answer über /answer/ (PIN-Store)",
      "RENDEZVOUS + '/answer/' + aid" in html)
check("Schwierigkeit-Label dynamisch (nicht hardcodiert 'Mittel')",
      'id="schwier-auto-label"' in html)
check("Server-Timeout-Hinweis nach 6s",
      'server-hint' in html and '6000' in html)
check("RENDEZVOUS dynamisch (localhost vs. Render)",
      "location.hostname" in html and "location.origin" in html)

# ─── Rendezvous.py Checks ─────────────────────────────────────────────────
import os
RV = 'rendezvous.py'
if os.path.exists(RV):
    rv = open(RV, encoding='utf-8').read()
    print("\nrendezvous.py:")
    check("GET /lobby/offer/ Endpunkt", "startswith('/lobby/offer/')" in rv and "GET" not in rv[rv.find("/lobby/offer/"):rv.find("/lobby/offer/")+5])
    # Einfachere Prüfung: Endpunkt existiert in do_GET
    do_get = rv[rv.find("def do_GET"):rv.find("def do_POST")] if "def do_GET" in rv else ""
    check("GET /lobby/offer/ in do_GET", "/lobby/offer/" in do_get)
    check("POST /lobby/offer/ in do_POST", "/lobby/offer/" in rv[rv.find("def do_POST"):])
    check("POST /lobby/join/ vorhanden", "/lobby/join/" in rv)
    check("POST /lobby/create vorhanden", "/lobby/create" in rv)
    check("Lobby TTL (LOBBY_TTL)", "LOBBY_TTL" in rv)
    check("lobby_cleanup()", "lobby_cleanup" in rv)
    check("PORT aus Umgebungsvariable", "os.environ.get('PORT'" in rv)
    check("ThreadedHTTPServer", "ThreadedHTTPServer" in rv)
else:
    print(f"\n  HINWEIS: {RV} nicht im aktuellen Verzeichnis — rendezvous.py-Checks übersprungen")

# ─── Warteraum ──────────────────────────────────────────────────────────────
print("\nWarteraum:")
check('screen-warteraum vorhanden', 'id="screen-warteraum"' in html)
check('zeigeWarteraum() vorhanden', 'function zeigeWarteraum(' in html)
check('warteraumInit() vorhanden', 'function warteraumInit(' in html)
check('warteraumVerlassen() vorhanden', 'function warteraumVerlassen(' in html)
check('warteraumWaehle() vorhanden', 'function warteraumWaehle(' in html)
check('warteraumHerausforderungAnnehmen() vorhanden', 'function warteraumHerausforderungAnnehmen(' in html)
check('warteraumAustragen() vorhanden', 'function warteraumAustragen(' in html)
check('warteraumFallbackVirtuell() vorhanden', 'function warteraumFallbackVirtuell(' in html)
check('warteraumEntscheideP2P() vorhanden', 'function warteraumEntscheideP2P(' in html)
check('kein _busy mehr', '_busy' not in html)
check('kein _sendeHerausforderung mehr', '_sendeHerausforderung' not in html)
check('Virtueller Gegner Kachel', 'wr-virtuell-card' in html)
check('Wunschgegner ausgegraut', 'Kommt bald' in html)
check('Spieler-Liste Element', 'wr-spieler-liste' in html)
check('14s AutoWeiter Warteraum', 'warteraum-auto-sek' in html)
check('Duell-Kachel auf Startscreen', 'zeigeWarteraum()' in html and 'mode-card-duell' in html)
check('Speed-Button vorhanden', 'debugSpeedToggle' in html)
check('DEBUG_TIMER_FAKTOR Bruch', '1/3' in html)
check('Footer: Duell-Link entfernt', "zeigeSchwierigkeit('duell')" not in html)

# ─── Service Worker / PWA ─────────────────────────────────────────────────
print("\nPWA:")
check('manifest.json', 'manifest.json' in html)
check('serviceWorker register', 'serviceWorker' in html)
check('sql-wasm.js', 'sql-wasm' in html)

# ─── Debug-Modus ──────────────────────────────────────────────────────────
print("\nDebug:")
check('DEBUG_TIMER_FAKTOR', 'DEBUG_TIMER_FAKTOR' in html)
check('debugTap()', 'function debugTap(' in html)
check('debug-panel', 'id="debug-panel"' in html)

# ─── Ergebnis ─────────────────────────────────────────────────────────────
print(f"\n{'='*45}")
print(f"  {ok} Checks bestanden · {fail} fehlgeschlagen")
if fail == 0:
    print("  ✓ Alles OK!")
else:
    print(f"  ✗ {fail} Probleme gefunden!")
    sys.exit(1)
