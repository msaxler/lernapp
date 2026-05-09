# CLAUDE.md — LernApp Projektregeln

## Projekt-Charakter

LernApp ist die generische Medien-Lern-App mit FSRS — Konzeptphase, vor LA-3-Implementation. Drei Stützpfeiler: **Daten · Didaktik · Player**. Player-agnostische Architektur: ein Lerninhalt, mehrere Player.

Verbindliche Architektur-Referenzen:
- `docs/produktvision.md` Sektion C.4 (Knotenmodell / Lernraumtopologie)
- `docs/pwa_lernapp.md` (Drei-Stützpfeiler-Konzept)
- `docs/choir-player-referenzmodell.md` (Player-Agnostik)
- `docs/projektplanung.md` (LA-Reihenfolge mit Blockern)

## Coding Guidelines

Übernommen aus Xalento (verbindlich ab Tag 1):
- System-Verhaltensmodell V8 (Xalento-Repo `docs/architektur/SYSTEM_VERHALTENSMODELL.md`) — 10 Verhaltensregeln, 6 Domänen
- Defensive Programmierung v2.1
- Anti-Rucksack v1.1
- Regel 10 (Falsifikationstest vor Fix): bei jedem Bug-Fix vor Eingriff sechs Bedingungen erfüllen — Reproduktion, minimaler Testfall, kausal-ausreichende Hypothese, unabhängiger Falsifikationstest, failing test vor Änderung, minimaler Eingriff.

## STATUS.md-Pflege (Mobile-Claude-Kontrakt, 9. Mai 2026)

`STATUS.md` im Repo-Root ist die Quelle für Mobile-Claude beim Spaziergang ("wie ist der Stand"). Sync-Tool spiegelt sie als Singleton nach `xcop/lernapp/STATUS.md`.

**Pflicht zur Aktualisierung bei:**
- LA-Status-Änderung (LA-X startet / blockiert / wird abgeschlossen)
- Neuer ADR oder Architektur-Entscheidung
- Migrations-Phase ändert sich (z.B. Wissenstransfer Schritt 1 startet)
- Pending-Liste hat sich substanziell geändert

**Pre-commit-Hook warnt** wenn STATUS.md älter als 14 Tage UND aktueller Commit hat strukturelle Änderungen.

## Drive-Sync

LernApp wird über Sync-Tool nach `xcop/lernapp/` gespiegelt. Pre-commit-Hook installiert via:
```
node D:/claude-code/tools/drive-sync/install-hook.js D:/claude-code/LernApp
```

Whitelist in `.sync-drive.json`. Bei jedem Doku-Commit auf main: Hook ruft sync.js, geänderte `.md`-Files landen mit Timestamp in Drive (außer STATUS.md = Singleton).

## Aktuelle Blocker

- **LA-3 (Quiz-Player) blockiert durch:** (1) Wissenstransfer Choir-Trainer-Stack → QuizAway, (2) Lernarchitektur-ADR
- Verfahrensrichtlinie Migration QuizAway: ENTWURF (siehe STATUS.md)
- Player-Schnittstelle Zwei-Modi-Modell: ENTWURF (vor LA-3 als ADR-PLAYER-07-modi formalisieren)

## Repo-Struktur

- `apps/` — Apps (in Konzeptphase, Code folgt mit LA-3)
- `docs/` — Architektur, Konzepte, ADRs
  - `docs/produktvision.md` — Hauptdokument mit Knotenmodell
  - `docs/projektplanung.md` — LA-Reihenfolge
  - `docs/adr/` — Architektur-Entscheidungs-Records
  - `docs/konzepte/` — Detail-Konzepte
- `python/` — Tooling-Skripte
- `data/` — Daten-Setups (Geonames etc.)

## Pending: Nächste Schritte

Siehe STATUS.md für tagesaktuellen Stand. Strategisch:
1. Verfahrensrichtlinie Migration QuizAway finalisieren
2. Wissenstransfer Choir-Trainer-Stack → QuizAway-Domänen-Layout dokumentieren
3. Lernarchitektur-ADR + Player-Modi-ADR formalisieren
4. LA-3 starten
