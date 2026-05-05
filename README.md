# LernApp / QuizAway

**Stand:** April 2026 · QuizAway v5 produktiv auf https://lernapp-wfd5.onrender.com

QuizAway ist eine PWA zum Geo-Quiz mit Sofa-Modus, Virtuelle Route, Live- und Duell-Modus. Backend ist ein einfacher Python-Rendezvous-Server (Stdlib-only), Frontend ist Single-File-HTML mit `sql.js` + GeoNames-Datenbank.

## Setup für lokale Entwicklung

### Voraussetzungen
- **Python 3.11** (geprüft mit Render Python-Runtime)
- Internet-Zugang beim ersten Start (lädt `geo.sqlite` aus GitHub-Release)

### Schnellstart

```bash
git clone https://github.com/msaxler/lernapp.git
cd lernapp

# Python-Abhängigkeiten installieren (aktuell nur Stdlib, requirements.txt ist leer)
pip install -r requirements.txt

# Server starten — lädt geo.sqlite automatisch aus dem GitHub-Release v1.0-data
python scripts/sync/rendezvous.py --port 8080
```

Im Browser http://localhost:8080 öffnen.

## Deployment auf Render

`render.yaml` definiert zwei Services:

| Service | Start-Command |
|---|---|
| `quizaway` | `python scripts/sync/rendezvous.py --port $PORT` |
| `duellmaschine` | `cd scripts/sync && python duellmaschine.py` |

**Auto-Deploy:** Push auf `main` → Render baut + restartet beide Services. `geo.sqlite` wird beim Start vom Bootstrap-Block in `rendezvous.py` automatisch von GitHub-Release `v1.0-data` heruntergeladen falls nicht vorhanden (persistent disk oder Container-FS).

## Datenbank-Architektur — `data/geo.sqlite`

**Größe:** ~18 MB · **Inhalt:** ~77.000 deutsche Städte mit Geo-Koordinaten, KFZ-Kennzeichen, Bundesland-Zuordnung etc.

**Bewusst NICHT im Repo** — wird per GitHub-Release verteilt:
- Release-Tag: `v1.0-data`
- URL: https://github.com/msaxler/lernapp/releases/download/v1.0-data/geo.sqlite
- Hardcoded in `scripts/sync/rendezvous.py:11` (`GEO_URL`)

### Datenbank neu bauen

```bash
cd data/
python ../scripts/data-build/ap1_build_pools.py
```

Das Skript:
1. Lädt GeoNames-Quelldaten (`allCountries.zip`, `admin1Codes`, `admin2Codes`) ins `geonames_data/` Verzeichnis (falls nicht vorhanden)
2. Lädt zusätzliche Quellen (Destatis-Städte-Liste, KFZ-Kennzeichen)
3. Baut `geo.sqlite` mit Tabellen `staat`, `bundesland`, `kreis`, `stadt`

**Hinweis:** Behörden-Websites haben oft Self-Signed-Certs — der Download-Code in `ap1_build_pools.py` umgeht das via SSL-Override.

### Neuen Release hochladen (nach DB-Update)

```bash
# DB lokal bauen
python scripts/data-build/ap1_build_pools.py

# Asset im bestehenden Release ersetzen
gh release upload v1.0-data data/geo.sqlite --clobber

# Render-Container restarten — beim Start lädt rendezvous.py die neue DB
# (löschen vorher manuell, weil Bootstrap-Check `if not exists` skipt)
```

**Manuelle Patches (rendezvous.py):** der `geo_patch()`-Block in `rendezvous.py` enthält bekannte Daten-Korrekturen (z.B. Simmern/Hunsrück Kreis-ID-Fehler) die nach dem Download angewendet werden. Bei einem DB-Rebuild diesen Block prüfen ob die Patches noch nötig sind.

## Verzeichnisstruktur

```
LernApp/
├── apps/
│   └── quizaway/
│       ├── quizaway_v5.html      ← App (PWA, sql.js + geo.sqlite)
│       ├── sw.js                 ← Service Worker
│       ├── manifest.json
│       └── icon-*.png
├── scripts/
│   ├── sync/
│   │   ├── rendezvous.py         ← Server (Signaling + Lobby + sqlite-Bootstrap)
│   │   └── duellmaschine.py      ← Duell-Modus-Server
│   ├── data-build/
│   │   ├── ap1_build_pools.py    ← geo.sqlite Tabellen-Schema + Initial-Build
│   │   └── build_ags_mapping.py  ← KFZ-Kennzeichen AGS5-Mapping
│   ├── data-fetch/               ← Single-Quellen-Importer (Wikidata, Destatis, GeoNames)
│   ├── data-patch/               ← Einmalige Daten-Korrekturen
│   └── check/                    ← Validierungs-Skripte
├── data/
│   └── geo.sqlite                ← (NICHT im Repo — siehe oben)
├── docs/
│   ├── ARCHITECTURE.md           ← Detaillierte Architektur-Diskussion
│   ├── produktvision.md
│   ├── projektplanung.md
│   └── konzepte/                 ← Konzept-Dokumente
├── geonames_data/                ← Rohdaten-Cache (partiell ignored)
├── render.yaml                   ← Render-Deploy-Konfig
├── requirements.txt              ← Python-Abhängigkeiten (aktuell leer, nur Stdlib)
└── RECOVERY.md                   ← Recovery-Audit (Stand 2026-05-05)
```

## Bekannte Punkte

- **Python-Version:** Code referenziert `py -3.11` in einigen `scripts/data-fetch/`- und `scripts/data-patch/`-Skripten. `.python-version`-Datei fehlt (TODO).
- **`geonames_data/`:** Mix aus committed (DE.zip, GV100.zip, admin1CodesASCII.txt) und ignored Files. Inkonsistenz noch nicht aufgelöst — siehe RECOVERY.md.
- **`data/raw/`** und **`backup/`** sind ignored (lokale Arbeit).

## Status-Verweis

Recovery-Audit: [`RECOVERY.md`](RECOVERY.md) (Stand 2026-05-05)
Detail-Architektur: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
Projektplanung: [`docs/projektplanung.md`](docs/projektplanung.md)
