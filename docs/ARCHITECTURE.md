# QuizAway v5 — Entwicklungsumgebung & Architektur

*Stand: März 2026 · QuizAway v5 abgeschlossen · Xalento LA-1/LA-2 abgeschlossen*

---

## Verzeichnisstruktur

```
D:\claude-code\LernApp\
├── apps\
│   └── quizaway\
│       ├── quizaway_v5.html      ← App (Single-File PWA, sql.js + geo.sqlite)
│       ├── sw.js                 ← Service Worker (Cache-Name quizaway-v5.1)
│       ├── manifest.json         ← PWA Manifest (start_url → quizaway_v5.html)
│       ├── icon-192.png          ← PWA Icon
│       ├── icon-512.png          ← PWA Icon
│       └── duel_sim.html         ← Duell-Simulator (Relay/ACK-Tests)
├── scripts\
│   ├── sync\
│   │   └── rendezvous.py         ← Server (Signaling + Warteraum + Relay-Fallback)
│   ├── data-build\
│   │   ├── ap1_build_pools.py    ← Geo-Pools in geo.sqlite schreiben
│   │   └── build_ags_mapping.py  ← KFZ-Kennzeichen AGS5-Mapping
│   ├── data-fetch\
│   │   ├── fetch_staedte.py      ← Städtedaten aus GeoNames / Destatis
│   │   ├── fetch_kfz.py          ← KFZ-Kennzeichen (AGS5-basiert)
│   │   └── fetch_wikidata.py     ← Wikidata-Felder
│   ├── data-patch\               ← Einmalige Korrekturen an Rohdaten
│   ├── data-explore\             ← Diagnose- und Analyseskripte
│   └── check\
│       ├── check_quiz.py         ← Validierung QuizAway v5 (49 Checks)
│       └── pruefen.py            ← KFZ-Datenqualitätsprüfung
├── data\
│   └── geo.sqlite                ← Geodatenbank (17,7 MB, 77.052 Städte)
│                                    Nicht im Repo — beim Serverstart automatisch
│                                    von GitHub Releases geladen
├── docs\                         ← Gesamte Dokumentation (Markdown)
│   ├── ARCHITECTURE.md           ← diese Datei
│   ├── produktvision.md          ← DOK-3 v9 (Produktvision QuizAway & Xalento)
│   ├── projektplanung.md         ← DOK-2 v17 (Arbeitspakete AP1–AP13 + LA-1–LA-12)
│   ├── quizaway_handbuch.html    ← Benutzerhandbuch v2 (HTML)
│   └── konzepte\
│       ├── duell_verbindung_learnings.md  ← P2P/Relay-Erkenntnisse
│       ├── quizaway_konzept-9.md          ← aktuelles Konzeptdokument
│       └── pwa_lernapp.md
├── requirements.txt              ← Python-Abhängigkeiten (stdlib only)
└── Procfile                      ← Render-Startbefehl
```

> `geo.sqlite` und `data/raw/` sind in `.gitignore` — sie werden lokal erzeugt
> bzw. beim Serverstart automatisch von GitHub Releases heruntergeladen.

---

## Lokaler Server starten

```cmd
cd D:\claude-code\LernApp
python scripts\sync\rendezvous.py --port 80
```

Zugriff lokal:
- PC:          `http://localhost/apps/quizaway/quizaway_v5.html`
- Smartphone:  `http://<lokale-IP>/apps/quizaway/quizaway_v5.html` (ipconfig → IPv4)

Port 80 ohne Admin-Rechte:
```cmd
netsh http add urlacl url=http://+:80/ user=Administrator
```

Alternativ Port 8080 (keine Admin-Rechte nötig):
```cmd
python scripts\sync\rendezvous.py --port 8080
```

---

## Deployment

**GitHub:**
- Repo: https://github.com/msaxler/lernapp
- Branch: main

**Render:**
- Dashboard: https://dashboard.render.com/web/srv-d6usqgvgi27c73ektdc0
- URL: https://lernapp-wfd5.onrender.com
- Free Tier: schläft nach 15 min Inaktivität — erster Request ~30 s

Deploy-Workflow:
```
Datei ändern → git add <datei> → git commit -m "..." → git push
→ Render deployed automatisch (ca. 1–2 min)
```

Deploy-relevante Dateien:
```
apps/quizaway/quizaway_v5.html
apps/quizaway/sw.js
apps/quizaway/manifest.json
apps/quizaway/icon-192.png
apps/quizaway/icon-512.png
scripts/sync/rendezvous.py
Procfile
requirements.txt
```

`geo.sqlite` ist **nicht** im Repo — wird beim ersten Serverstart von
`https://github.com/msaxler/lernapp/releases/download/v1.0-data/geo.sqlite`
heruntergeladen.

**Service Worker Cache-Busting:** Bei App-Änderungen `CACHE_NAME` in `sw.js`
hochzählen (aktuell `quizaway-v5.1`), damit Mobilgeräte den alten SW-Cache
verwerfen und frische Dateien laden.

---

## Rendezvous-Server Architektur

`scripts/sync/rendezvous.py` — ein Python-Prozess, vier Aufgabenbereiche:

### Statische Dateien
Liefert alle Dateien unter `apps/` und `data/` direkt aus.

### Warteraum-Endpunkte (CAS-Modell)

| Endpunkt | Methode | Funktion |
|---|---|---|
| `/warteraum/betreten` | POST | Spieler registrieren (Zustand FREE) |
| `/warteraum/verlassen` | POST | Spieler austragen |
| `/warteraum/liste` | GET | Aktive Spieler (nur < 30 s gesehen) |
| `/warteraum/heartbeat` | POST | Spieler als aktiv markieren (alle 10 s) |

Warteraum-Timeout: 120 Sekunden — danach startet das Spiel gegen den virtuellen Gegner.

### WebRTC-Signaling-Endpunkte

| Endpunkt | Methode | Funktion |
|---|---|---|
| `/lobby/offer` | POST | SDP Offer vom HOST ablegen |
| `/lobby/answer` | POST | SDP Answer vom GUEST ablegen |
| `/lobby/ice` | POST | ICE-Kandidaten austauschen |
| `/lobby/poll` | GET | Auf Gegner-Nachricht warten |

### Relay-Fallback-Endpunkte

| Endpunkt | Methode | Funktion |
|---|---|---|
| `/relay/{id}/init` | POST | Relay-Session anlegen |
| `/relay/{id}/send` | POST | Nachricht in Queue stellen |
| `/relay/{id}?fuer=X` | GET | Nachricht abholen (Short-Poll, 3 s) |

Der Relay-Fallback wird automatisch aktiviert wenn WebRTC scheitert — der Nutzer
merkt nichts davon. Siehe `docs/konzepte/duell_verbindung_learnings.md`.

### Hilfendpunkte

| Endpunkt | Methode | Funktion |
|---|---|---|
| `/ping` | GET | Health-Check (UptimeRobot) |

### Startup: Geo-Patch

`geo_patch()` führt idempotente Korrekturen an `geo.sqlite` aus:

| Korrektur | Beschreibung |
|---|---|
| Simmern/Hunsrück `kreis_id` 07143 → 07140 | War fälschlich im Westerwaldkreis |

---

## App-Architektur (quizaway_v5.html)

Vanilla JS Single-File PWA. Die Geodatenbank (`geo.sqlite`, 17,7 MB) wird
per sql.js (WebAssembly) im Browser geladen — ~10.800 Fragen generiert zur Laufzeit.

### Spielmodi

| Modus | Beschreibung |
|---|---|
| Sofa-Modus | Alleine spielen, 5 Runden, 3 Fragen pro Runde |
| Live-Modus | GPS-basiert, Fragen aus dem Radius um den eigenen Standort |
| Duel-Modus | P2P gegen echten Gegner via WebRTC + Relay-Fallback |

### P2P Duell-Modus

| Komponente | Technologie |
|---|---|
| Verbindungsaufbau | WebRTC DataChannel (PIN-System) |
| Signaling | rendezvous.py (Offer/Answer/ICE via HTTP) |
| NAT-Traversal | STUN: Google + TURN: OpenRelay |
| Relay-Fallback | HTTP Short-Poll wenn WebRTC scheitert (automatisch) |
| Nachrichtenübertragung | `duelSendReliable()` mit ACK-basiertem Retry |
| Duplikat-Schutz | `seenSeqs` Set — verhindert doppelte Spiellogik |
| Spiellogik | vollständig P2P — kein Server nach Verbindungsaufbau |

**Relay-Aktivierung:** Automatisch bei ICE-Fehler, 3 fehlgeschlagenen Pings
oder nach 12-Sekunden-Timeout. Details: `docs/konzepte/duell_verbindung_learnings.md`.

**Rollenverteilung:** HOST wählt Runden 1, 3 · GUEST wählt Runden 2, 4 ·
Runde 5: Spieler mit mehr Punkten wählt (Tiebreaker: Gesamtspielzeit → Hash).

### GPS im Warteraum & Live-Modus

Warteraum: `gpsStart()` startet automatisch für regionale KFZ-Fragen.
Live-Modus: `liveGPSStart()` → Karte mit Radius → Stadtauswahl durch Nutzer → Quiz.

---

## Technologie-Stack

| Schicht | Technologie |
|---|---|
| App | Vanilla JS, Single HTML File |
| Geodatenbank | SQLite via sql.js (WebAssembly) 1.10.2 |
| P2P | WebRTC DataChannel |
| Relay-Fallback | HTTP Short-Poll via rendezvous.py |
| Server | Python 3 stdlib (kein Framework, keine Dependencies) |
| PWA | Service Worker, Cache-First, Cache-Name `quizaway-v5.1` |
| Deployment | Render (Free Tier), GitHub Releases (geo.sqlite) |

---

## Validierung

```cmd
python -X utf8 scripts\check\check_quiz.py   # 49/49 Checks
```

---

## Nächste Phase: Xalento (Lern-App)

QuizAway ist ein abgeschlossener Prototyp. Die nächste Phase ist Xalento —
eine generalisierte Lernplattform in `D:\claude-code\Xalento\`:

| Arbeitspaket | Status |
|---|---|
| LA-1 Projektgerüst (Vite/React/TS) | ✅ abgeschlossen |
| LA-2 FSRS-Engine + Dexie Store | ✅ abgeschlossen |
| LA-3 Quiz-Player | offen |
| LA-4 Export/Import | offen |
| LA-5 Chorübung-Inhalte | offen |

Technische Grundlage: `docs/projektplanung.md` (DOK-2 v17), `docs/produktvision.md` (DOK-3 v9)
