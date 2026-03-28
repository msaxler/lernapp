# QuizAway — Entwicklungsumgebung & Architektur

## Verzeichnisstruktur

```
D:\claude-code\LernApp\
├── apps\
│   └── quizaway\
│       ├── quizaway_v4.html      ← App (Single-File PWA, ~10.800 Fragen eingebettet)
│       ├── sw.js                 ← Service Worker (PWA, Cache-Name quizaway-v4)
│       ├── manifest.json         ← PWA Manifest
│       ├── icon-192.png          ← PWA Icon
│       └── icon-512.png          ← PWA Icon
├── scripts\
│   ├── sync\
│   │   ├── rendezvous.py         ← Server (Signaling + Warteraum + statische Dateien)
│   │   ├── duellmaschine.html    ← Standalone Duell-Testclient (kein echtes Quiz)
│   │   ├── duellmaschine.py      ← Standalone Rendezvous-Server für Duell-Tests
│   │   └── README_duellmaschine.md
│   ├── data-build\
│   │   ├── ap1_build_pools.py    ← Geo-Pools in geo.sqlite schreiben
│   │   ├── generate_questions.py ← Fragen aus Städtedaten erzeugen
│   │   └── inject_questions.py   ← Fragen in quizaway_v4.html einbetten
│   ├── data-fetch\
│   │   ├── fetch_staedte.py      ← Städtedaten aus GeoNames / Destatis
│   │   ├── fetch_kfz.py          ← KFZ-Kennzeichen (AGS5-basiert)
│   │   ├── fetch_bahnhof.py      ← DB-Bahnhofskategorien
│   │   └── fetch_wikidata.py     ← Wikidata-Felder (Geschichte, Ersterwähnung)
│   ├── data-patch\               ← Einmalige Korrekturen an Rohdaten
│   ├── data-explore\             ← Diagnose- und Analyseskripte
│   └── check\
│       └── check_quizaway.py     ← Validierung (137 Checks)
├── data\
│   └── geo.sqlite                ← Geodatenbank (17,7 MB, 77.052 Städte)
│                                    Nicht im Repo — wird beim Serverstart
│                                    automatisch von GitHub Releases geladen
├── docs\
│   ├── ARCHITECTURE.md           ← diese Datei
│   ├── CREDENTIALS.md
│   ├── pwa_lernapp.md
│   └── konzepte\
│       ├── quizaway_konzept-7.md
│       ├── quizaway_konzept-8.md
│       └── quizaway_konzept-9.md ← aktuelles Konzeptdokument
├── docu\
│   ├── quizaway_handbuch.html    ← Benutzerhandbuch (HTML)
│   ├── quizaway_handbuch.docx    ← Benutzerhandbuch (Word)
│   └── dok*.docx / pwa_*.docx   ← Übergeordnete Lernapp-Konzepte
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
- PC:          `http://localhost/apps/quizaway/quizaway_v4.html`
- Smartphone:  `http://<lokale-IP>/apps/quizaway/quizaway_v4.html` (ipconfig → IPv4)

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
- Auth: Google Account (msaxler@gmail.com)
- Branch: main

**Render:**
- Dashboard: https://dashboard.render.com/web/srv-d6usqgvgi27c73ektdc0
- Service: lernapp
- URL: https://lernapp-wfd5.onrender.com
- Auth: msaxler@gmail.com (via GitHub)
- Free Tier: schläft nach 15 min Inaktivität — erster Request ~30 s

Deploy-Workflow:
```
Datei ändern
→ git add <datei>
→ git commit -m "..."
→ git push
→ Render deployed automatisch (ca. 1–2 min)
```

Deploy-relevante Dateien:
```
apps/quizaway/quizaway_v4.html
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
heruntergeladen und dann lokal gecacht (`data/geo.sqlite`).

---

## Rendezvous-Server Architektur

`scripts/sync/rendezvous.py` — ein Python-Prozess, vier Aufgabenbereiche:

### Statische Dateien
Der Server liefert alle Dateien unter `apps/` und `data/` direkt aus.
Zugriff über Pfad, z. B. `GET /apps/quizaway/quizaway_v4.html`.

### Warteraum-Endpunkte

| Endpunkt | Methode | Funktion |
|---|---|---|
| `/warteraum/betreten` | POST | Spieler registrieren, ID vergeben |
| `/warteraum/verlassen` | POST | Spieler austragen |
| `/warteraum/liste` | GET | Aktive Spieler auflisten (nur < 30 s gesehen) |
| `/warteraum/heartbeat` | POST | Spieler als aktiv markieren (alle 10 s) |

**Heartbeat-Filter:** `/warteraum/liste` gibt nur Spieler zurück, deren
`zuletzt_gesehen`-Timestamp weniger als 30 Sekunden alt ist. Aktive Clients
senden alle 10 s einen Heartbeat. Spieler, die die App schließen oder deren
Request fehlschlägt, verschwinden spätestens nach 30 s aus der Liste.

**sessionStorage-Retry:** `warteraumAustragen()` speichert die eigene ID in
`sessionStorage`. Beim nächsten Warteraum-Aufruf (`warteraumInit()`) wird ein
vergessenes Austragen nachgeholt. Sichert gegen Render-Cold-Start-Ausfälle.

### WebRTC-Signaling-Endpunkte

| Endpunkt | Methode | Funktion |
|---|---|---|
| `/lobby/offer` | POST | SDP Offer vom HOST ablegen |
| `/lobby/answer` | POST | SDP Answer vom GUEST ablegen |
| `/lobby/ice` | POST | ICE-Kandidaten austauschen |
| `/lobby/poll` | GET | Auf Gegner-Nachricht warten (Long-Poll) |

### Hilfendpunkte

| Endpunkt | Methode | Funktion |
|---|---|---|
| `/ping` | GET | Health-Check (UptimeRobot) |

### Startup: Geo-Patch

Beim Serverstart führt `geo_patch()` idempotente Korrekturen an `geo.sqlite`
aus — bekannte Datenfehler, die im Rohdatensatz vorhanden sind:

| Korrektur | Beschreibung |
|---|---|
| Simmern/Hunsrück `kreis_id` 07143 → 07140 | War fälschlich im Westerwaldkreis (KFZ: WW) statt im Rhein-Hunsrück-Kreis (KFZ: SIM) |

Neue Datenfehler werden hier idempotent ergänzt.

---

## App-Architektur (quizaway_v4.html)

Vanilla JS Single-File PWA. Alle Fragen (~10.800), Kategoriedaten und
App-Logik sind in einer einzigen HTML-Datei gebündelt. Die Geodatenbank
(`geo.sqlite`) wird per sql.js (WebAssembly) im Browser geladen.

### P2P Duell-Modus

| Komponente | Technologie |
|---|---|
| Verbindungsaufbau | WebRTC DataChannel |
| Signaling | rendezvous.py (Offer/Answer/ICE via HTTP) |
| NAT-Traversal | STUN: Google + TURN: OpenRelay |
| Nachrichtenübertragung | `duelSendReliable()` mit ACK-basiertem Retry |
| Spiellogik | vollständig P2P — kein Server nach Verbindungsaufbau |

**Rollenverteilung:** HOST = wählt Runden 1 und 3, GUEST = wählt Runden 2 und 4.
Runde 5: Spieler mit mehr Punkten wählt (Tiebreaker: kürzere Gesamtspielzeit,
danach deterministischer Hash beider Spielernamen).

### GPS im Warteraum

Beim Betreten des Warteraums startet `gpsStart()` automatisch:
- Versuch 1+2: `enableHighAccuracy: true` (GPS-Chip, genau, langsamer)
- Versuch 3: `enableHighAccuracy: false` (IP/WLAN-Ortung, schnell, grob)

Für KFZ-Fragen ist Kreis-Genauigkeit ausreichend — IP-Ortung reicht dafür.
GPS-Daten werden in der `hello`-Nachricht an den Gegner übertragen und
bestimmen den regionalen Fragenpool beider Spieler.

---

## Technologie-Stack

| Schicht | Technologie |
|---|---|
| App | Vanilla JS, Single HTML File |
| Geodatenbank | SQLite via sql.js (WebAssembly) 1.10.2 |
| P2P | WebRTC DataChannel |
| Server | Python 3 stdlib (kein Framework, keine Dependencies) |
| PWA | Service Worker, Cache-First, Cache-Name `quizaway-v4` |
| Deployment | Render (Free Tier), GitHub Releases (geo.sqlite) |

---

## Build-Pipeline (Fragen neu generieren)

```
scripts/data-fetch/fetch_staedte.py     →  staedte.json       (2.051 Städte)
scripts/data-fetch/fetch_kfz.py         →  kfz in staedte.json
scripts/data-build/ap1_build_pools.py   →  geo.sqlite Pools
scripts/data-build/generate_questions.py→  fragen.json        (~10.800 Fragen)
scripts/data-build/inject_questions.py  →  quizaway_v4.html   (Fragen eingebettet)
scripts/check/check_quizaway.py         →  Validierung (137 Checks)
```

---

## Nächste Phase: Lernapp (Xalento)

QuizAway ist ein abgeschlossener Prototyp. Das Spiel wird später neu gebaut
als Teil der universellen Lernplattform (Xalento), mit:

- React 18 + TypeScript 5 + Vite 5
- FSRS Spaced Repetition Engine
- WebDAV Sync (Nextcloud)
- Generative Fragenerzeugung zur Laufzeit (kein eingebettetes Fragen-JSON)
- Ligasystem (P2P Event-Ledger + Bloom-Filter-Gossip)
- Erweiterung auf DACH / Europa

Technische Grundlage: `docu/dok3_produktvision_v7.docx`, `docu/dok2_projektplanung_v16.docx`
