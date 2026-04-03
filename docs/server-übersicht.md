# Server-Übersicht — QuizAway & Xalento

*Zuletzt aktualisiert: April 2026 · Netlify → Cloudflare Pages migriert (2026-04-03)*

---

## Inhaltsverzeichnis

1. [Übersicht aller Dienste](#1-übersicht-aller-dienste)
2. [GitHub](#2-github)
3. [Cloudflare Pages — Xalento](#3-cloudflare-pages--xalento)
4. [Render — QuizAway/LernApp](#4-render--quizawaylernapp)
5. [Lokale Entwicklungsserver](#5-lokale-entwicklungsserver)
6. [Zusammenspiel der Dienste](#6-zusammenspiel-der-dienste)
7. [Wichtige Befehle Schnellreferenz](#7-wichtige-befehle-schnellreferenz)
8. [Credentials](#8-credentials)

---

## 1. Übersicht aller Dienste

| Dienst | Produkt | Typ | URL |
|--------|---------|-----|-----|
| GitHub | beide | Quellcode-Hosting, CI-Trigger | github.com/msaxler |
| Cloudflare Pages | Xalento | Statisches Hosting + PWA | xalento.pages.dev |
| Render (quizaway) | QuizAway | Python-Backend: WebRTC-Signaling + Geo-Daten | \<service\>.onrender.com |
| Render (duellmaschine) | QuizAway | Python-Backend: Duell-Matchmaking | \<service\>.onrender.com |
| Vite Dev-Server | Xalento | Lokaler Dev-Server mit HMR | https://LAN-IP:5173 |
| Python Dev-Server | QuizAway | Lokaler Test-Server | http://localhost:8080 |

---

## 1b. Adressen-Schnellreferenz

> PC-LAN-IP aktuell: **192.168.178.48** (kann sich nach Router-Neustart ändern — dann `ipconfig` ausführen)

### Xalento

| Zweck | Adresse | Gerät |
|-------|---------|-------|
| Lokale Entwicklung (PC) | https://localhost:5173 | nur PC |
| Lokale Entwicklung (Smartphone im WLAN) | https://192.168.178.48:5173 | Smartphone im Heimnetz |
| Produktion / Unterwegs | https://xalento.pages.dev | alle Geräte, kein WLAN nötig |

⚠️ Beim ersten Aufruf von `https://192.168.178.48:5173` zeigt der Browser eine Sicherheitswarnung (selbstsigniertes Zertifikat) → „Erweitert" → „Trotzdem fortfahren" (einmalig pro Gerät/Browser).

### QuizAway / LernApp

| Zweck | Adresse | Gerät |
|-------|---------|-------|
| Rendezvous-Server lokal (PC) | http://localhost:8080 | nur PC |
| Rendezvous-Server lokal (Smartphone im WLAN) | http://192.168.178.48:8080 | Smartphone im Heimnetz |
| Duellmaschine lokal (PC) | http://localhost:8081 | nur PC |
| Duellmaschine lokal (Smartphone im WLAN) | http://192.168.178.48:8081 | Smartphone im Heimnetz |
| Rendezvous-Server Produktion | https://\_\_\_\_\_.onrender.com | alle Geräte |
| Duellmaschine Produktion | https://\_\_\_\_\_.onrender.com | alle Geräte |

### LAN-IP aktualisieren
Falls sich die IP geändert hat (nach Router-Neustart):
```bash
ipconfig | grep IPv4
# neue IP oben in dieser Tabelle eintragen
```

---

## 2. GitHub

### Was GitHub leistet
- Versionskontrolle (git) für beide Projekte
- Hostet Quellcode und Release-Assets (z.B. `geo.sqlite`)
- **Trigger-Mechanismus:** Ein `git push` löst automatisch den Build auf Netlify (Xalento) bzw. ein Re-Deploy auf Render (QuizAway) aus
- Release-Asset `geo.sqlite` wird beim Serverstart von Render heruntergeladen falls nicht vorhanden

### Repos

| Repo | Lokal | Remote |
|------|-------|--------|
| Xalento | `D:\claude-code\Xalento` | github.com/msaxler/xalento |
| LernApp/QuizAway | `D:\claude-code\LernApp` | github.com/msaxler/lernapp |

### Wichtigste Befehle

```bash
# Änderungen committen und deployen (löst Netlify/Render aus)
git add <dateien>
git commit -m "beschreibung"
git push origin main

# Status prüfen
git status
git log --oneline -5

# Lokalen Stand mit Remote abgleichen
git pull origin main
```

### Release-Assets verwalten (geo.sqlite)
```bash
# Neues Release auf GitHub erstellen → Assets hochladen:
# github.com/msaxler/lernapp → Releases → Draft new release
# Asset: data/geo.sqlite (wird von Render beim Start heruntergeladen)
```

### Login
- **URL:** github.com
- **Benutzername:** msaxler
- **Passwort/Token:** → siehe Abschnitt 8

---

## 3. Cloudflare Pages — Xalento

> ⚠️ Netlify wurde am 2026-04-03 abgelöst (22 Deploys = 330 Credits, Limit überschritten).
> Alte URL `vermillion-creponne-33ae65.netlify.app` ist nicht mehr erreichbar.

### Was Cloudflare Pages leistet
- Hostet den **statischen Build** (`apps/lern-app/dist/`) als öffentliche Web-App
- Liefert echtes **HTTPS-Zertifikat** → Mikrofon (`navigator.mediaDevices`) funktioniert ohne Warnung
- **SPA-Routing** nativ unterstützt: nicht gefundene Pfade liefern automatisch `index.html`
- Hostet den **Service Worker** → App ist offline nutzbar (PWA)
- Ermöglicht **Homescreen-Installation** auf Android/iOS
- **Unlimitierte Deploys** auf dem kostenlosen Plan

### Verzeichnisse

| Ort | Inhalt |
|-----|--------|
| Lokal: `D:\claude-code\xalento\` | Quellcode-Root (Monorepo) |
| Lokal: `apps/lern-app/src/` | React-Anwendungscode |
| Lokal: `apps/lern-app/public/` | Statische Assets (Icons etc.) |
| Lokal: `apps/lern-app/dist/` | Build-Output (wird von Cloudflare ausgeliefert) |

### Build-Einstellungen (Cloudflare Dashboard)

| Feld | Wert |
|------|------|
| Build command | `npm run build --workspace=apps/lern-app` |
| Build output directory | `apps/lern-app/dist` |
| Root directory | *(leer)* |
| Environment variable | `VITE_NO_HTTPS=1` |

### Deploy-Mechanismus
```
git push origin main
       ↓
GitHub-Webhook → Cloudflare Pages
       ↓
Cloudflare: npm install + npm run build
       ↓  (ca. 60–90 Sekunden)
       ↓
dist/ live unter xalento.pages.dev
```

### Wichtigste Aktionen im Cloudflare-Dashboard
- **dash.cloudflare.com** → Workers & Pages → xalento → Deployments → Build-Status + Logs
- **Rollback:** Deployments → älteres Deployment anklicken → "Rollback to this deployment"
- **Umgebungsvariablen:** Settings → Environment variables

### Login
- **URL:** dash.cloudflare.com
- **E-Mail:** msaxler@gmail.com (Google Sign-In)
- **Projekt:** xalento

---

## 4. Render — QuizAway/LernApp

Render betreibt zwei Python-Backend-Server. Beide haben **keine externen
Python-Abhängigkeiten** — nur die Python-Standard-Bibliothek.

---

### 4a. Service „quizaway" — Rendezvous-Server

#### Was dieser Server leistet
- **Auslieferung der Web-App:** Liefert `quizaway_v4.html` und zugehörige Assets als HTTP-Responses
- **WebRTC-Signaling:** Vermittelt SDP-Offer/Answer und ICE-Kandidaten zwischen zwei Browsern, die sich verbinden wollen (Peer-to-Peer). Die Verbindung läuft danach direkt Browser↔Browser — der Server ist nur beim Verbindungsaufbau beteiligt
- **Duell-Lobby:** Warteraum-Logik — Spieler melden sich an, Server führt sie zusammen
- **Geo-Daten:** Beim Start wird `geo.sqlite` geprüft und ggf. von GitHub Releases heruntergeladen. Die SQLite-Datenbank enthält alle Geo-Fragen (Städte, Kreise etc.)
- **Geo-Patches:** Bekannte Datenfehler in `geo.sqlite` werden beim Start automatisch korrigiert

#### Verzeichnisse auf Render

| Pfad auf Render | Inhalt |
|-----------------|--------|
| `/opt/render/project/src/` | Ausgecheckter Git-Repo-Inhalt |
| `/opt/render/project/src/scripts/sync/rendezvous.py` | Startskript |
| `/data/` | **Persistenter Disk** (1 GB) — hier liegt `geo.sqlite` dauerhaft |
| `/data/geo.sqlite` | Geo-Datenbank (~einige MB), wird beim ersten Start heruntergeladen |

#### Konfiguration in `render.yaml`
```yaml
services:
  - type: web
    name: quizaway
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python scripts/sync/rendezvous.py --port $PORT
    envVars:
      - key: PORT
        value: 10000
    disk:
      name: quizaway-data
      mountPath: /data
      sizeGB: 1
```

#### Lokal starten
```bash
cd D:\claude-code\LernApp\scripts\sync
python rendezvous.py
# → PC:          http://localhost:8080
# → Smartphone:  http://192.168.178.48:8080
```

---

### 4b. Service „duellmaschine" — Duell-Matchmaking

#### Was dieser Server leistet
- **Duell-Modus PoC:** Spieler betreten einen Warteraum, der Server führt je zwei Spieler zu einem Duell zusammen (Matchmaking)
- **WebRTC-Signaling:** Wie beim Rendezvous-Server — vermittelt Verbindungsaufbau zwischen den Duell-Teilnehmern
- **CAS (Compare-and-Swap):** Atomare Zustandsänderungen bei gleichzeitigen Zugriffen mehrerer Spieler
- **Keepalive via UptimeRobot:** Render deaktiviert kostenlose Dienste nach 15 Minuten Inaktivität. UptimeRobot pingt alle 5 Minuten `/ping` → Server bleibt aktiv

#### Konfiguration

```yaml
# render.yaml (in apps/duellmaschine/ oder eigenem Repo)
startCommand: bash -c "cd scripts/sync && python duellmaschine.py"
```

#### UptimeRobot-Einstellung
```
Monitor Type:  HTTP(s)
URL:           https://<service-name>.onrender.com/ping
Interval:      5 Minuten
```

#### Lokal starten
```bash
cd D:\claude-code\LernApp\scripts\sync
python duellmaschine.py
# → PC:          http://localhost:8081
# → Smartphone:  http://192.168.178.48:8081
# Testen: 4 Browser-Tabs öffnen, Spielernamen vergeben
```

### Render-Dashboard — wichtigste Aktionen
- **dashboard.render.com** → Service auswählen
- **Logs:** "Logs"-Tab → Echtzeit-Ausgabe des Python-Servers
- **Manueller Neustart:** "Manual Deploy" → "Deploy latest commit"
- **Disk-Inhalt prüfen:** Shell-Tab → `ls /data/`
- **Umgebungsvariablen:** Environment → Add Environment Variable

### Login Render
- **URL:** dashboard.render.com
- **Benutzername/E-Mail:** → siehe Abschnitt 8
- **Passwort:** → siehe Abschnitt 8

---

## 5. Lokale Entwicklungsserver

### 5a. Vite Dev-Server — Xalento

> ⚠️ **Voraussetzung:** Bevor `https://localhost:5173` (z. B. `/chor`) im Browser geöffnet werden kann, muss der Dev-Server in einem CMD-Fenster laufen (siehe Befehl unten). Ohne laufenden Server ist die Adresse nicht erreichbar.

```bash
cd D:\claude-code\Xalento
npm run dev
# → PC:          https://localhost:5173
# → Smartphone:  https://192.168.178.48:5173
```

**Was er leistet:**
- Hot Module Replacement (HMR) — Änderungen im Browser sofort ohne Reload
- Selbstsigniertes HTTPS-Zertifikat (`@vitejs/plugin-basic-ssl`) → `navigator.mediaDevices` (Mikrofon) im LAN verfügbar
- Erster Aufruf im Browser: Sicherheitswarnung → "Erweitert" → "Trotzdem besuchen" (einmalig)

**Wann benutzen:** Beim Entwickeln am PC — schneller Feedback-Loop ohne Push/Deploy

**Nicht nötig für:** Smartphone-Tests → dafür Netlify verwenden

### 5b. Python Dev-Server — QuizAway

```bash
cd D:\claude-code\LernApp\scripts\sync
python rendezvous.py
# → http://localhost:8080
```

**Was er leistet:** Identisch mit dem Render-Server, aber lokal — zum Testen ohne Deployment

---

## 6. Zusammenspiel der Dienste

### Xalento — Datenfluss

```
Entwickler (PC)
    │
    ├─ npm run dev ──────────────────→ Browser (PC/Smartphone im LAN)
    │                                  Hot-Reload, HTTPS via basicSsl
    │
    └─ git push origin main
               │
               ▼
          GitHub (msaxler/xalento)
               │  Webhook
               ▼
          Cloudflare Pages Build
          (npm run build, ~60s)
               │
               ▼
     xalento.pages.dev
     ├─ React-App (alle Daten lokal in IndexedDB)
     ├─ Service Worker (Offline-Cache)
     └─ PWA (Homescreen-Install, kein WLAN nötig)
```

**Wichtig:** Xalento hat kein Backend. Alle Nutzerdaten (FSRS-Fortschritt, Decks) liegen im Browser (Dexie/IndexedDB). Netlify liefert nur statische Dateien.

### QuizAway — Datenfluss

```
Entwickler (PC)
    │
    └─ git push origin main
               │
               ▼
          GitHub (msaxler/lernapp)
               │  Auto-Deploy
               ▼
          Render (quizaway + duellmaschine)
               │
               ▼
     Spieler A (Browser) ←──WebRTC──→ Spieler B (Browser)
               │                              │
               └───── Signaling über ─────────┘
                    Render-Server (nur beim
                    Verbindungsaufbau nötig,
                    danach P2P direkt)
```

**geo.sqlite-Bootstrapping:**
```
Render startet rendezvous.py
    │
    ├─ /data/geo.sqlite vorhanden? ──ja──→ Patches anwenden → Server ready
    │
    └─ nein → Download von:
              github.com/msaxler/lernapp/releases/download/v1.0-data/geo.sqlite
                       │
                       ▼
              Gespeichert auf /data/ (persistenter Disk)
                       │
                       ▼
              Patches anwenden → Server ready
```

---

## 7. Wichtige Befehle Schnellreferenz

### Git (beide Projekte)
```bash
git status                          # Was ist geändert?
git add <datei>                     # Datei stagen
git add -p                          # Änderungen interaktiv stagen
git commit -m "beschreibung"        # Commit
git push origin main                # Push → Auto-Deploy
git log --oneline -10               # Letzte Commits
git diff                            # Was hat sich geändert?
```

### Xalento (D:\claude-code\Xalento)
```bash
npm run dev                         # Dev-Server starten
npm run build                       # Produktions-Build lokal testen
npm test                            # Vitest-Tests
node scripts/gen-icons.js           # PWA-Icons neu generieren
```

### LernApp (D:\claude-code\LernApp)
```bash
python scripts/sync/rendezvous.py   # Rendezvous-Server lokal starten
python scripts/sync/duellmaschine.py # Duellmaschine lokal starten
```

### Cloudflare Pages
```bash
# Deploy läuft automatisch via git push — kein CLI nötig
# Dashboard: dash.cloudflare.com → Workers & Pages → xalento
```

---

## 8. Credentials

> ⚠️ Diesen Abschnitt nur lokal verwenden — nie committen oder teilen.

### GitHub
| Feld | Wert |
|------|------|
| URL | github.com |
| Benutzername | msaxler |
| E-Mail | |
| Passwort | |
| Personal Access Token | |

### Cloudflare Pages
| Feld | Wert |
|------|------|
| URL | dash.cloudflare.com |
| E-Mail | msaxler@gmail.com |
| Login | Google Sign-In |
| Projekt | xalento |
| Live-URL | https://xalento.pages.dev |

### Render
| Feld | Wert |
|------|------|
| URL | dashboard.render.com |
| E-Mail | |
| Passwort | |

### UptimeRobot (Keepalive für Render)
| Feld | Wert |
|------|------|
| URL | uptimerobot.com |
| E-Mail | |
| Passwort | |
| Monitor-URL duellmaschine | https://\_\_\_\_\_.onrender.com/ping |
| Monitor-URL quizaway | https://\_\_\_\_\_.onrender.com/ping |
