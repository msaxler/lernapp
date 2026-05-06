# Projekt: LernApp / Xalento
## Stand: 2026-05-06

> Projektion aus Primärquellen (ADR-001, Produktvision DOK-3 v11, ARCHITECTURE.md).
> Bei Widerspruch gilt die Primärquelle.
> QuizAway ist ein Player-Typ innerhalb der Plattform — nicht das Zentrum.

## 0. Aktiver Fokus
Geändert: 2026-05-06
Bestätigt: 2026-05-06
Seit 2026-05-06: Lernarchitektur-ADR (Drei-Schichten / Player-agnostisch) ist der fehlende strukturelle Schritt vor LA-3 (Quiz-Player Neubau). Copilot-Pilot läuft parallel — 14-Tage-Validierung ab heute.

## 1. Aktueller Zustand
- QuizAway v5: stabil, deployed auf Render — 10.800 Laufzeit-Fragen, echtes P2P-Duell, GPS-Live-Modus
- Xalento-Stack: LA-1 (Projektgerüst) + LA-2 (FSRS-Engine + Dexie) abgeschlossen
- LA-3 (Quiz-Player Neubau): offen — wartet auf Lernarchitektur-ADR
- Choir-Trainer: produktiv (Xalento-Stack, MusicXML-Player)
- Lernarchitektur-ADR (Drei-Schichten): konzeptionell in Vision, aber nicht finalisiert — echte Blockade

## 2. Letzte Entscheidungen
- 2026-05-06: Copilot-Architektur-Pattern eingeführt, LernApp als Pilot-Projekt (ADR-001 Rev 3)
- 2026-04: QuizAway Neubau als Neubau auf Xalento-Stack entschieden — nach LA-8 (ARCHITECTURE.md)
- 2026-04: Player-Typ-Konzept definiert: Quiz-Player ✓, Beschriftungs-, Zuordnungs-, Lückentext-, Sortierspiel-Player konzipiert (DOK-3 v11 C.9)

## 3. Offene Punkte
- Lernarchitektur-ADR fehlt — Player-Schnittstelle (Plattform ↔ Player-Typ) nicht ausgespect.
- LA-3 Quiz-Player Neubau: blockiert bis Lernarchitektur-ADR steht
- AP13 Duell-Modus Neuimplementierung (v5 noch mit Relay-Fallback, Ziel: Always-On WS + eigener TURN)
- Drei IR-Refactoring-Phasen: Phase 3 (Audio-Engine-Reconciliation) noch offen — kein Blocker für QuizAway

## 4. Nächste Schritte
- Lernarchitektur-ADR finalisieren (Drei-Schichten: Lernraumtopologie / Player-Typ / Implementierung)
- Dann: LA-3 Quiz-Player starten (Neubau auf React + TS + Vite + Dexie, analog Choir-Trainer)
- Parallel: Copilot-Pilot 14 Tage — min. 3 mobile Abfragen/Tag, max. 1 STATUS.md-Update/Session

## 5. Relevante Artefakte
- ADR-001 Copilot-Architektur-Pattern → docs/adr/ADR-001-Copilot-Architektur-Pattern.md
- Produktvision DOK-3 v11 → docs/produktvision.md
- Architektur → docs/ARCHITECTURE.md
- QuizAway v5 (deployed) → apps/quizaway/quizaway_v5.html

---

## Fehlerprotokoll (Pilot-Phase)

*Jede schlechte Copilot-Antwort wird hier eingetragen — Symptom und Ursache getrennt.*

| Datum | Abfrage (kurz) | Symptom | Ursache |
|---|---|---|---|
| — | — | — | — |
