# STATUS — LernApp

**Stand:** 2026-10-01 (QuizAway-Abschnitt; übrige Abschnitte Stand 2026-05-09)
**Status:** Konzeptphase / vor LA-3-Implementation
**Repo:** github.com/msaxler/lernapp (privat)

---

## QuizAway Reise-Modus (wieder aufgenommen 2026-10-01)

**Ein Repo für alle Geräte, der PC führt (Mike, 2026-10-01).** Maßgeblich ist der Stand in diesem Repo (GitHub `msaxler/lernapp`, gespiegelt nach Drive `xcop/lernapp/`). Was am Handy entsteht, kommt als GEOSYNC-Datei an den PC und wird hier eingearbeitet. Versionsnummern der Konzepte vergibt der PC; am Handy bitte auf der hier genannten Fassung aufsetzen und keine eigene Folgeversion anlegen.

Alle Dokumente unter `docs/konzepte/`. Keine Implementierungsfreigabe; die kommt nach Feldtest Stufe 2.

- **Spielkonzept v0.2.5** `quizaway-spielkonzept-reise-modus-v0.2.5-2026-10-01.md` (maßgeblich; v0.2, v0.2.3 und v0.2.4 liegen daneben, Anhang A steht in v0.2). **Achtung für Mobile-Claude:** v0.2.4 und v0.2.5 sind am PC entstanden. Nicht auf v0.2.3 weiterarbeiten und keine eigene „v0.2.4" anlegen; nächste Fassung ist v0.2.6. Neu in v0.2.5: Ziffern 1–4 mit „zwo", Auflösung ≤ 70 Wörter einschließlich Anschluss, Leiter als „höher / hier steige ich aus", zwei Handlungen in der Bahn als Hypothese.
- **Feldtest Stufe 1, Solo:** erste Person gelaufen (Kartensatz, Protokoll). 6 von 10 Karten mit begründeter Theorie; K1 und K3a nicht erhoben.
- **PC-Prüfung** `quizaway-spielkonzept-v0.2.3-pruefung-pc-2026-10-01.md` (B1–B10), Entscheide Mike „alle gemäß Vorschlägen" → v0.2.4 Anhang D.
- **Nächster Schritt Mike:** zweite Solo-Person mit **Kartensatz Fassung 2** `quizaway-feldtest-solo-kartensatz-freiburg-v2-2026-10-01.md` (Lügen der Karten 3 und 10 ersetzt, Kürzel W). Rohbogen der ersten Person: „Gundelfingen" fiel bei Karte 3 und 10 nicht; das Wiedererkennen bleibt eine unbelegte Vermutung (v0.2.5 §8 Nr. 2).
- **Stufe 2 (generierte Karten):** `quizaway-stufe2-vorbereitung-2026-10-01.md` — Ortsliste (10 Ziel- plus 10 Spenderorte), Karten-Prompt v0.3, Probe an Umkirch (gleicher Fakt wie die handgeschriebene Karte, sobald der Extraktions-Prompt nach Gründen und Herkunft fragt). Volllauf nicht gestartet.
- **Gemeinde-Achsen:** v0.5 plus E1–E3 (28.06.) plus **E4–E8** `gemeinde-achsen-entscheidungen-2026-10-01.md`.
- **Oberfläche und Design:** maßgeblich ist **UI-Konzept v0.2** `quizaway-ui-konzept-reise-modus-v0.2-2026-10-01.md` (v0.1 vom Spaziergang plus PC-Prüfung `quizaway-ui-konzept-v0.1-pruefung-pc-2026-10-01.md`, U1–U12, plus sechs Entscheide Mikes). **Screens v0.2 zum Durchtippen** (Originalgröße, Hell/Dunkel umschaltbar): `docs/konzepte/skizzen/quizaway-reise-modus-screens-v0.2.html`, veröffentlicht unter https://claude.ai/artifact/1MFUd2u45eyLXhGwTGD4n2. Die ältere Skizze „QuizAway Reise-Modus Screens" (Stand vor v0.1) ist überholt. Papier-Screens nicht im zweiten Solo-Test. Nachtrag in v0.2: Spaltung zählt nicht als Treffer; Schrift im Auto fest, in der Bahn mitwachsend; Solo wählt und bestätigt mit „Festlegen"; eigenes Aussehen (Ortsschild-Gelb, hell und dunkel) auf dem Farbsystem von MixMi (R-UI-19). Offen nur noch: Hell/Dunkel im Auto ansehen, Papier-Test der Screens, Nachfrage. Nachfrage an die Reviewpartner (zehn Fragen, ein Paste) liegt bereit: `quizaway-oberflaeche-review-briefing-runde5-2026-10-01.md`.
- **Später:** PC-Session gegen Transfer-Konzept v1.1; dessen Kipp-Kriterium §2 ist durch den Reise-Modus ausgelöst (v0.2.5 §9).

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
