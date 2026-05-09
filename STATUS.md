# STATUS — LernApp

**Stand:** 2026-05-09 mittag
**Status:** Konzeptphase / vor LA-3-Implementation
**Repo:** github.com/msaxler/lernapp (privat)

---

## Architektur-Fundament (verbindlich)

- **Drei Stützpfeiler:** Daten · Didaktik · Player (siehe `docs/pwa_lernapp.md`)
- **Player-agnostische Architektur:** ein Lerninhalt, mehrere Player als auswechselbare Sicht (siehe `docs/choir-player-referenzmodell.md`)
- **Fünfstufige Hierarchie:** Schulfach → Werk → Programm → Lerneinheit → Übungsabschnitt
- **FSRS-Karte = Übungsabschnitt** (kleinste sinnvolle Wiederholungs-Einheit)
- **Knotenmodell:** Lernraumtopologie aus Knoten + 3 Verbindungstypen (Autor / Attribut / Pfad) — siehe `docs/produktvision.md` Sektion C.4 „Die Lernraumtopologie"

## Aktiv

- LA-1 ✅ — Projektgerüst
- LA-2 ✅ — FSRS-Engine + Dexie Store

## Pending

| LA | Beschreibung | Blocker |
|---|---|---|
| **LA-3** | Quiz-Player | **(1) Wissenstransfer Choir-Trainer-Stack → QuizAway-Domänen-Layout (2) Lernarchitektur-ADR fehlt** |
| LA-4 | Export/Import | LA-3 |
| LA-5 | Chorübung-Inhalte | LA-3 |

## Migration QuizAway → Xalento-Zielarchitektur (Spaziergang 8.5.)

**Verfahrensrichtlinie (ENTWURF, finalisierung pending):**
1. QuizAway als erste Anwendung der Xalento-Zielarchitektur
2. Architektur abgeleitet aus Choir Trainer + Xalento (operativ) + V8 (architektonisch)
3. **Vorbedingung:** dokumentierter Wissenstransfer Choir Trainer → QuizAway
4. Architektur-Detailfragen erst nach Wissenstransfer
5. **Schutzraum Choir Trainer:** in Stabilisierung (LA-21+22), keine rückwirkenden Änderungen während Migration
6. QuizAway v5 als funktionaler Vergleichspunkt — Migration abgeschlossen wenn alle 4 Modi (Sofa/Route/Live/Duell) gleichwertig

**Reihenfolge:** Schritt 0 (Verfahrensrichtlinie finalisieren) → Schritt 1 (Wissenstransfer) → Schritt 2 (Architektur-ADRs) → Schritt 3 (LA-3 starten)

## Player-Schnittstelle Zwei-Modi-Modell (Spaziergang 8.5., ENTWURF)

- **Freier Modus:** Player autonom, kein FSRS-Feedback
- **Auftragsgebundener Modus:** Übung innerhalb von Didaktik-Auftrag, EvaluationEvent zurück, FSRS-Update

→ als ADR-PLAYER-07-modi vor LA-3 zu formalisieren

## Wichtige Dokumente

| Bereich | Pfad |
|---|---|
| Produktvision (mit Knotenmodell) | `docs/produktvision.md` Sektion C.4 |
| PWA-Lernapp-Konzept | `docs/pwa_lernapp.md` |
| Player-agnostische Architektur | `docs/choir-player-referenzmodell.md` |
| Projektplanung (LA-Reihenfolge) | `docs/projektplanung.md` |
| QuizAway Konzept v9 | `docs/konzepte/quizaway_konzept-9.md` |
| ADR-001 Copilot-Architektur-Pattern | `docs/adr/ADR-001-Copilot-Architektur-Pattern.md` |

## Drive-Sync

- Sub-Ordner: `xcop/lernapp/`
- 16 Doku-Files synct via post-commit-Hook
