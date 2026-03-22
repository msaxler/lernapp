# QuizAway / Xalento — Entwicklungsumgebung & Architektur

## Verzeichnisstruktur

```
D:\claude-code\LernApp\          ← Hauptverzeichnis
├── quizaway_v4.html             ← App (komplette Single-File PWA)
├── rendezvous.py                ← Server (Signaling + Warteraum)
├── geo.sqlite                   ← Datenbank (17.7 MB, 77.052 Städte)
├── sw.js                        ← Service Worker (PWA, Cache quizaway-v4)
├── manifest.json                ← PWA Manifest
├── icon-192.png                 ← PWA Icon
├── ap1_build_pools.py           ← Datenpipeline Geo-Pools
├── check_quizaway.py            ← Validierung (137 Checks)
├── backup\                      ← Sicherungskopien
├── docu\                        ← Konzeptdokumente (DOK-1 bis DOK-3)
├── geonames_data\               ← Rohdaten GeoNames
└── __pycache__\
```

## Lokaler Server starten

```cmd
# Als Administrator (Port 80 benötigt erhöhte Rechte)
cd D:\claude-code\LernApp
python rendezvous.py --port 80

# Alternativ ohne Admin-Rechte
python rendezvous.py --port 8080
```

Zugriff lokal:
- PC:          http://localhost/quizaway_v4.html
- Smartphone:  http://<lokale-IP>/quizaway_v4.html  (ipconfig → IPv4)

Port 80 via netsh für Nicht-Admin:
```cmd
netsh http add urlacl url=http://+:80/ user=Administrator
```

## Deployment

**GitHub:**
- Repo: https://github.com/msaxler/lernapp
- Auth: Google Account (msaxler@gmail.com)
- Branch: main
- Deploy-Dateien: quizaway_v4.html, rendezvous.py, geo.sqlite, sw.js, manifest.json, icon-192.png

**Render:**
- Dashboard: https://dashboard.render.com/web/srv-d6usqgvgi27c73ektdc0
- Service: lernapp
- URL: https://lernapp-wfd5.onrender.com
- Auth: msaxler@gmail.com (via GitHub)
- Free Tier: schläft nach 15min Inaktivität — erster Request ~30s

Deploy-Workflow:
```
Datei ändern → nach D:\claude-code\LernApp\ kopieren
→ git add . → git commit -m "..." → git push
→ Render deployed automatisch
```

## Rendezvous-Server Architektur

Zwei Aufgaben in einem Python-Prozess:

| Endpunkt | Funktion |
|----------|----------|
| `/warteraum/*` | Matchmaking (CAS-Modell, FREE/CLAIMED/PAIRED/LEFT) |
| `/lobby/*` | WebRTC Signaling (Offer/Answer/ICE) |
| `GET /quizaway_v4.html` | Statische Auslieferung App |
| `GET /geo.sqlite` | Statische Auslieferung DB |

## Technologie-Stack (aktuell)

- **App:** Vanilla JS, Single HTML File, sql.js 1.10.2
- **DB:** geo.sqlite (SQLite via WebAssembly)
- **P2P:** WebRTC DataChannel, STUN (Google) + TURN (OpenRelay)
- **Server:** Python 3 stdlib only, keine Dependencies
- **PWA:** Service Worker, Cache-First, Cache-Name quizaway-v4

## Nächste Phase: Lernapp Xalento

Neues Projekt in `D:\claude-code\Xalento\` (noch anzulegen):

- React 18 + TypeScript 5 + Vite 5
- FSRS Spaced Repetition Engine
- WebDAV Sync (Nextcloud)
- Player-Typen: Quiz, Beschriftung, Zuordnung, Lückentext, Sortierung
- Startfach: Chorübung (SingOn, Bass 2)
- Ziel-Fach: Biologie Sekundarstufe 1

Arbeitspakete: LA-1 bis LA-12 → siehe DOK-2 v16 (docu\)
Architektur-Details → DOK-3 v8 (docu\)
