# Recovery-Audit: LernApp / QuizAway

**Stand:** 2026-05-05
**Repo:** https://github.com/msaxler/lernapp
**Letzter Push:** 2026-04-04 (Commit "C.17 Navigations-Hierarchie")
**Branch:** main, up to date

## Status: ⚠️ Lücken (mehrere kritische Datenartefakte fehlen)

QuizAway läuft in Production auf `lernapp-wfd5.onrender.com` über Render.com. Die wichtige Daten-Datenbank `geo.sqlite` (18 MB, 2100 Städte) ist NICHT im Repo, wird aber zur Laufzeit benötigt. Ein Build-Skript zur Re-Generierung existiert, ist aber nicht klar dokumentiert.

## Audit-Funde (Kategorie D – kritisch fehlend)

| Datei/Pfad | Größe | Empfehlung |
|---|---|---|
| `data/geo.sqlite` | 18 MB | per Build-Skript oder GitHub Release verteilen — **dokumentieren wo / wie**. Aktuell weder im Repo noch in Releases (zu prüfen) |
| `admin_struktur.txt` | 677 KB | klären: Daten-Quelle oder Output? Falls Output → ignorieren; falls Quelle → per LFS oder Build-Skript |
| `quizaway_v4.html` (root, untracked) | 256 KB | duplikat zu `apps/quizaway/quizaway_v4.html`? Klären/löschen |
| `geonames_data/` (382 MB total) | partiell ignoriert + partiell committed | inkonsistent — `.gitignore` listet `DE.zip`, `GV100.zip` als ignoriert, aber `git ls-files` zeigt sie als committed. **Klärung notwendig.** |

## Unpushed Commits

_keine_

## Untracked (Stand 2026-05-05)

```
.claude/                              (Claude-Code-Config, lokal halten)
admin_struktur.txt                    (677 KB — siehe Funde oben)
docs/choir-player-referenzmodell.md   (Konzept-Doku, sollte committed werden)
docs/konzepte/informatik_lehrplan.md  (Konzept-Doku, sollte committed werden)
quizaway_v4.html                      (256 KB — Duplikat?)
```

## Modifizierte (uncommitted)

- `docs/konzepte/choir_uebungsabschnitte.md` — sollte committed oder verworfen
- `stimmbild_proto_v2.html` — Status klären

## Checkliste-Ergebnis

### Build & Setup
- ✅ `requirements.txt` vorhanden (aber leer — "nur Python-Standard-Bibliothek")
- ❌ `README.md` FEHLT komplett
- ❌ `.python-version` fehlt — aber Code referenziert `py -3.11` (in scripts/data-fetch/, scripts/data-patch/)
- ✅ `render.yaml` für Deploy
- ⚠️ Build-Skripte für `geo.sqlite`: existieren (`scripts/data-fetch/fetch_staedte.py`, `backup/ap1_build_pools.py`), aber keine zentrale Anleitung

### Dokumentation & Architektur
- ✅ ADRs in `docs/` partiell vorhanden
- ⚠️ Konzept-Dokumente: einige untracked (informatik_lehrplan.md, choir-player-referenzmodell.md)
- ❌ Diagramme: nicht gefunden

### Assets & Daten
- ❌ `data/geo.sqlite` (18 MB) — NICHT im Repo, NICHT in `.gitignore` ausgeschlossen-erklärt. Wird bei Production-Deploy via fetch geladen (`apps/quizaway/quizaway_v4.html`: `await fetch('/data/geo.sqlite')`)
- ⚠️ `geonames_data/`: Mix aus committed (`DE.zip`, `GV100.zip`, `admin1CodesASCII.txt`) und ignored Files
- ✅ `data/raw/` per `.gitignore` ausgeschlossen
- ❌ Test-Fixtures: kein dediziertes test-Verzeichnis mit Fixtures gefunden

### CI/CD & Deployment
- ❌ Keine `.github/workflows/`
- ✅ `render.yaml` vorhanden (Render-Deploy-Konfig committed)
- ❌ `.env.example` fehlt — keine ENV-Var-Schema-Dokumentation
- ⚠️ Wie kommt `data/geo.sqlite` in den Render-Container? Build-Skript oder Pre-Built-Bundle? **OFFEN.**

### Externe Abhängigkeiten
- ⚠️ Geonames-Daten: Quelle dokumentiert? (vermutlich download.geonames.org, sollte in README dokumentiert werden)
- ⚠️ Politische Grenzen-Daten: `vg250.zip` Quelle dokumentieren

## Empfohlene Nachträge ins Repo

1. **`README.md` schreiben** (1-2 h) — Setup-Anweisungen, Python-Version, Datenbank-Build-Schritte
2. **`.python-version` anlegen** (1 min) — `3.11` (aus Scripts ableitbar)
3. **`scripts/build_geo_sqlite.py` als Single-Entry-Point** (~1 h Aufwand) — fetcht alle Quelldaten + baut `data/geo.sqlite` reproduzierbar
4. **GitHub-Release mit `geo.sqlite` als Asset** (~10 min) — wenn der Build zu langsam für Render-Container ist
5. **`.env.example`** für künftige ENV-Vars
6. **`.gitignore` audit** — `geonames_data/*.zip` Inkonsistenz auflösen (entweder ALLES ignorieren oder ALLES committen)
7. **Untracked Konzept-Docs committen** (informatik_lehrplan.md, choir-player-referenzmodell.md)
8. **Frage klären: `quizaway_v4.html` im Root vs in `apps/quizaway/`** — Duplikat oder unterschiedliche Versionen?

## Bewusst NICHT im Repo (dokumentiert)

- `__pycache__/`, `*.pyc`
- `backup/` (Lokale Backups)
- `*.env`, `CREDENTIALS.md`
- `data/raw/`, `archive/`

## Offene Fragen

1. **Wie wird `geo.sqlite` auf Render.com bereitgestellt?** Build-Step in `render.yaml` fehlt, kein Pre-fetch-Skript erkennbar. Möglicherweise in der lokalen Pre-Deploy-Schleife gebaut + manuell per `git push --force` ins Render-Volume?
2. **`admin_struktur.txt` (677 KB):** Quelle oder Output?
3. **`stimmbild_proto_v2.html` Status** — soll das Repo-relevant sein?
4. **Sind die `geonames_data/*.zip`-Files trotz `.gitignore` versehentlich committed?** (mit `git check-ignore` zu verifizieren)
