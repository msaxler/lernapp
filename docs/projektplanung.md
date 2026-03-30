# Projektplanung — QuizAway & Xalento

*Version 3.0 · März 2026 · DOK-2 v18*
*AP1–AP13 abgeschlossen · LA-1 + LA-2 abgeschlossen · vollständig mit DOK-3 v9 abgeglichen*

---

## 1. Übersicht QuizAway-Arbeitspakete (AP1–AP13)

Alle QuizAway-APs sind **abgeschlossen**. QuizAway v5 ist der fertige Prototyp.

| AP | Name | Status |
|----|------|--------|
| AP1 | GeoNames Basispools | ✅ abgeschlossen |
| AP2 | Geometrie-Pipelines (PLZ) | ✅ abgeschlossen |
| AP3 | DE-spezifische Pools (KFZ) | ✅ abgeschlossen |
| AP4 | Translations & Schablonen | ✅ abgeschlossen |
| AP5 | Event-Ledger-Modul | ✅ abgeschlossen |
| AP6 | WebRTC PoC | ✅ abgeschlossen |
| AP7 | Nostr Relay PoC | ✅ abgeschlossen |
| AP8 | Ledger-Merge P2P | ✅ abgeschlossen |
| AP9 | Fragengerator PoC | ✅ abgeschlossen |
| AP10 | SQLite Build-Pipeline | ✅ abgeschlossen |
| AP11 | PWA Shell | ✅ abgeschlossen |
| AP12 | QuizAway spielbar | ✅ abgeschlossen |
| AP13 | Duel-Modus | ✅ abgeschlossen |

Details zu AP1–AP13 siehe DOK-2 v17 (`docs/quellen/dok2_projektplanung_v17.docx`).

---

## 2. Xalento-Arbeitspakete (LA-1–LA-17)

Xalento ist die generalisierte Lernplattform auf Basis der QuizAway-Erkenntnisse.
Stack: React 18 · TypeScript 5 · Vite 5 · Dexie.js (IndexedDB) · FSRS-5
Verzeichnis: `D:\claude-code\Xalento\`

### Leitprinzipien Gamification (DOK-3 v9, Abschnitt C.6)

Vor jedem LA gilt als Designregel:

| ✅ Erwünscht | ❌ Verboten |
|---|---|
| FSRS-Scheduling-Transparenz sichtbar machen | Badges für Klickzahlen |
| Dauerhaftes Wissen zeigen ("seit 3 Wochen sicher") | Globale Ranglisten |
| Optionale Hinweise ("8 Karten fällig") | Pflicht-Streaks |
| Wettbewerb am Lerninhalt gebunden | Leben/Herzen-System |
| Belohnung unmittelbar nach Aufgabe | Punkte für Schnelligkeit |

*Forschungsbasis: Bai et al. (2020), Ninaus (2025) — Gamification wirkt nur wenn
Spielelemente direkt zur Lernaufgabe passen.*

---

### Phase 0 — Fundament

#### LA-1 — Projektgerüst ✅ abgeschlossen

**Output** Vite/React/TypeScript Monorepo, ESLint, Prettier, Vitest, alle Packages
**Testkriterium** `npm run dev` startet · `npm test` grün · `npm run build` sauber

#### LA-2 — FSRS-Engine ✅ abgeschlossen

**Output** FSRS-5 Engine (`engine/fsrs.ts`), Dexie Store (`store/db.ts`),
`useFSRS` Hook, Learn-Screen mit 4 Bewertungs-Buttons, 5 Beispielkarten (Biologie Zelle)
**Enthält** `scheduleCard`, `formatNextReview`, `isDue`, `getDueProgress`, `isOverdue`
**Testkriterium** 34/34 Tests grün

---

### Phase 1 — Kern-Player + Gamification-Basis

#### LA-3 — Quiz-Player

**Voraussetzungen** LA-2
**Output** Vollständiger Quiz-Player — Frage aufdecken, 4 Optionen mit Highlight,
Erklärung, FSRS-Bewertung 1–4, Feedback-Label ("✓ Wieder in 4 Tagen")
**Gamification-Regel** Keine Punkte für Schnelligkeit · Keine Leben/Herzen ·
Bewertungsbuttons zeigen Konsequenz, nicht Wertung
**Technologie** React, TypeScript, `useFSRS` Hook
**Testkriterium** 3 Karten durchspielen · FSRS-Werte korrekt gespeichert ·
Feedback-Label erscheint nach jeder Bewertung

#### LA-4 — Fortschritts-Screen (Gamification Ebene 1 + 2)

**Voraussetzungen** LA-3
**Output** Deck-Dashboard und Session-Abschluss-Screen — sichtbare
Scheduling-Transparenz als primäre Motivation
**Enthält:**
- Deck-Übersicht: *Heute fällig: 8 · Neu: 3 · Gelernt gesamt: 47*
- Session-Abschluss: *Richtig: 9/12 · Morgen: 3 Karten · In 3 Tagen: 5 Karten*
- Pro-Karte-Ansicht: *"Zellkern: seit 3 Wochen sicher — wieder in 12 Tagen"*
- Lernkette (Ebene 2): *"Diese Karte kennst du seit 3 Wochen zuverlässig"* statt Streak-Zähler
- Optionaler Hinweis: *"Du hast heute noch 5 Karten fällig"* — Information, kein Druck
**Gamification-Regel** Kein Pflicht-Streak · Kein Aussetzer-Bestrafung ·
Fokus auf dauerhaftes Wissen, nicht tägliche Disziplin
**Testkriterium** Deck-Dashboard zeigt korrekte Zahlen aus Dexie ·
Session-Screen erscheint nach letzter Karte

#### LA-5 — Offline-Export / Import

**Voraussetzungen** LA-2
**Output** JSON-Export und -Import aller Karten + FSRS-Lernfortschritt
**Technologie** Dexie.js, JSON, File System Access API (Chrome) / Download-Link (Fallback)
**Testkriterium** Export → gültiges JSON · Import → Karten + Fortschritt wiederhergestellt ·
Merge-Logik: neuerer FSRS-Stand gewinnt bei Konflikt

---

### Phase 2 — Chorübung (erster Anwendungsfall)

*Chorübung gliedert sich nach DOK-3 C.8 in drei Phasen:
A (Zuhören/Media-Player), B (Singen/Performance-Player), C (Bewertung).
LA-6 und LA-7 bauen die beiden benötigten Player-Typen.*

#### LA-6 — Chorübung Phase A: Media-Player

**Voraussetzungen** LA-3
**Output** Media-Player-Komponente (60/40-Layout) — MusicXML-Rendering via OSMD,
MP3-Wiedergabe, Tempo-Kontrolle 50–150 %, Score und Text laufen mit
**Technologie** OSMD 1.9.6, Tone.js, WaveSurfer.js
**Deck** SingOn-Chor Bass 2 — erste 5 Sequenzen spielbar
**Testkriterium** 5 Chorübungen abspielen · Tempo-Slider funktioniert ·
MusicXML korrekt gerendert auf iOS und Android

#### LA-7 — Chorübung Phase B+C: Performance-Player

**Voraussetzungen** LA-6
**Output** Performance-Player — Mikrofon-Aufnahme, Selbsteinschätzung (Phase B),
Pitch-Analyse optional (Phase C)
**Phase B (sofort)** App spielt letzten N Takte als Anlauf, dann Aufnahme starten ·
Bewertung per Selbsteinschätzung: *Nochmal / Fast / Gut / Perfekt*
**Phase C (später)** Mikrofon-Analyse: Pitch-Messung via Web Audio API
**Technologie** Web Audio API, Tone.js, MediaRecorder API
**Testkriterium** Aufnahme startet nach Anlauf · Selbsteinschätzung speichert FSRS-Wert ·
funktioniert auf iOS Safari (getUserMedia)

#### LA-8 — Chorübung Deck (vollständig)

**Voraussetzungen** LA-6 + LA-7
**Output** Vollständiges Deck SingOn-Chor Bass 2 — alle Stücke in Phase A und B spielbar ·
FSRS plant Wiederholungen pro Sequenz
**Testkriterium** Komplettes Stück durchspielen · FSRS scheduliert korrekt ·
Export/Import des Deck-Fortschritts funktioniert

---

### Phase 3 — Player-Ausbau (für Biologie Sek1)

*Die folgenden Player decken die Wissenstypen Strukturwissen und Prozesswissen ab —
die Vorbereitung für das Biologie-Deck. Alle teilen dieselbe FSRS-Infrastruktur.*

#### LA-9 — Beschriftungs-Player

**Voraussetzungen** LA-3
**Output** SVG-Bild mit nummerierten Pfeilen — Lernender tippt Bezeichnungen ein ·
häufigster Aufgabentyp in Biologie-Schulbüchern
**Technologie** React, SVG-Overlay, Wikimedia Commons Bilder
**Testkriterium** Zellbild mit 5 Organellen korrekt beschriftet ·
Tipp-Toleranz (Groß/Kleinschreibung, Leerzeichen) · FSRS-Integration

#### LA-10 — Zuordnungs-Player

**Voraussetzungen** LA-3
**Output** Drag-and-Drop Zuordnung — zwei Spalten verbinden ·
fühlt sich an wie Sammelkartenspiel
**Technologie** React DnD, Touch-Events (Pointer Events API)
**Testkriterium** 5 Tier-Lebensraum-Paare korrekt zuordnen auf Touch-Screen ·
FSRS-Integration

#### LA-11 — Lückentext- und Sortier-Player

**Voraussetzungen** LA-3
**Output** Lückentext (Dropdown + Freitext) + Sortieraufgabe für Abläufe
**Technologie** React, TypeScript
**Testkriterium** Fotosynthese-Lückentext spielbar · Nahrungskette sortierbar ·
FSRS-Integration

---

### Phase 4 — Biologie Sek1

#### LA-12 — Wikidata-Pipeline

**Voraussetzungen** LA-3
**Output** Automatisierte Abfrage Wikidata → JSON-Decks (Arten, Anatomie, Ökosysteme),
Bilder von Wikimedia Commons
**Technologie** Python, Wikidata SPARQL API, Wikimedia Commons
**Testkriterium** 500 Biologie-Karten automatisch generiert · Bilder verknüpft ·
Lehrplan Klasse 5–6 als Kurationsraster angewendet

#### LA-13 — Biologie Sek1 Deck

**Voraussetzungen** LA-9 + LA-10 + LA-11 + LA-12
**Output** Vollständig kuratiertes Deck Biologie Klasse 5–6 — alle Player-Typen genutzt ·
Lehrplan-konform
**Testkriterium** Kapitel Zellaufbau komplett durcharbeitbar ·
FSRS plant Wiederholungen · Export/Import funktioniert

---

### Phase 5 — Gamification erweitert

#### LA-14 — Duell-Modus Lern-App (Gamification Ebene 3)

**Voraussetzungen** LA-3 + LA-4
**Output** Zwei Lernende treten gegeneinander an — technisch aus QuizAway übernommen,
thematisch an den Lerninhalt des aktuellen Decks gebunden (nicht Geo-Quiz sondern
Biologie/Chemie/Geschichte)
**Enthält:**
- Warteraum-Matchmaking (CAS-Modell aus QuizAway)
- 5 Runden, Wahlrecht wechselt nach Rundenergebnis
- Ergebnis zeigt Punkte **und** welche Karten beide beherrschen (Lernfokus)
- Optional: Runde 5 als Joker-Runde mit Spezialregel
**Gamification-Regel** Wettbewerb ist sinnvoll weil er direkt am Lerninhalt hängt —
kein inhaltsleerer Wettbewerb
**Technologie** WebRTC DataChannel + Relay-Fallback aus QuizAway portiert
**Technische Auflagen aus `docs/konzepte/duell_verbindung_learnings.md`:**
- Signaling: **WebSocket** statt HTTP-Polling (kein Sleep-Problem, weniger Roundtrips)
- TURN: **eigener coturn-Server oder bezahlter Dienst** — OpenRelay ist unzuverlässig
- Relay-Fallback: beibehalten — bewährt; als WebSocket effizienter als Short-Poll
- ACK-Protokoll + Duplikat-Schutz (`seenSeqs`): beibehalten, in eigene Klasse auslagern
- SW-Cache: alle dynamischen Endpunkte (`/warteraum/`, `/lobby/`, `/relay/`) **von Anfang an** ausschließen
- Rendezvous: **Always-On** — kein Render Free Tier (30s Aufwachzeit ist inakzeptabel)
- Rundenwechsel: Wahlrecht-Logik deterministisch · Auto-Advance-Timer (5s) beibehalten
**Testkriterium** Verbindung Mobilnetz ↔ WLAN funktioniert · Relay-Fallback aktiviert sich
automatisch · Duplikate werden erkannt · kein Spielabbruch beim Netzwechsel

#### LA-15 — Klassen-Dashboard (Gamification Ebene 4)

**Voraussetzungen** LA-4
**Output** Lehrer-Ansicht — zeigt Wissensstand der Klasse, nicht Punktestand
**Ansicht:**
- *Schüler A: 8/10 Karten sicher · Schüler B: 4/10 Karten sicher*
- *Heute fällig (Klasse): Ø 6 Karten*
- *Letzte Aktivität pro Schüler — ohne Druck*
**Gamification-Regel** Kein Punkteranking · Kein öffentlicher Vergleich ·
Fokus auf Beherrschung, nicht Wettbewerb
**Technologie** Read-only Dashboard, kein eigenes Backend (Shared IndexedDB Export)

---

### Phase 6 — Go-to-Market

#### LA-16 — Launch / Social Contract

**Voraussetzungen** LA-8 (Chorübung vollständig)
**Output** App öffentlich erreichbar — kostenlos · Teilen-Funktion ·
Social Contract: *"Wer es nützlich findet, gibt es weiter"*
**Technologie** Render/Vercel, PWA
**Testkriterium** 10 externe Nutzer aktiv · Share-Link funktioniert

#### LA-17 — Zahlung

**Voraussetzungen** LA-16 + ~10.000 aktive Nutzer
**Output** Bezahlschranke — Wero, PayPal, Lightning/Nostr-Zap (NIP-57)
**Strategie** Basisversion kostenlos bleibt · Zahlung für erweiterte Features ·
kein App-Store-Zwang solange möglich (30 % Provision vermeiden)
**Testkriterium** Zahlung funktioniert auf iOS und Android

---

## 3. Offen / Zurückgestellt

Diese Features sind in DOK-3 beschrieben aber bewusst noch keinem LA zugeordnet
(Pareto — erst wenn Kernfunktion stabil):

| Feature | DOK-3 Referenz | Zurückgestellt bis |
|---------|----------------|-------------------|
| Kryptographische Identität (secp256k1, kein Account) | C.10 | Nach LA-5 bewerten |
| Nostr-Sync / Geräte-Sync | A.1, D.1 | Nach LA-16 |
| Explorer-Komponente (Eigenbau, Einhandbedienung) | C.4, C.5 | Phase 3 |
| Liga-System (öffentlich, entschieden) | B.3, Offene Punkte | Nach LA-14 |
| Performance-Player Mikrofon-Analyse Phase C | C.8 | Nach LA-7 |
| Analyse-Player (Essay, Argumentation) | C.11 | Phase 3+ |
| Persistenz-Backend (Nextcloud vs. kDrive) | Offene Punkte | Vor LA-16 entscheiden |
| QuizAway → Xalento Migration (4-Schritt-Pfad) | B.6, D.3 | Parallel zu LA-13 |

---

## 4. Abhängigkeiten Xalento

```
LA-1 → LA-2 → LA-3 → LA-4
                  ↓       ↓
                 LA-5    LA-14
                  ↓
              LA-6 → LA-7 → LA-8 → LA-16 → LA-17
                  ↓
              LA-9 ↘
              LA-10 → LA-13 → LA-14
              LA-11 ↗
                  ↓
              LA-12 ↗
                  ↓
              LA-15 (nach LA-4)
```

Parallel startbar nach LA-2: LA-5, LA-6 (nach LA-3)
Parallel startbar nach LA-3: LA-9, LA-10, LA-11, LA-12

---

## 5. Vergleich alt (v17) → neu (v18)

| Änderung | Grund |
|----------|-------|
| LA-3 neu: Gamification-Designregeln explizit | DOK-3 C.6 — Anti-Pattern-Absicherung |
| LA-4 neu: Fortschritts-Screen | DOK-3 C.6 Ebene 1+2 — fehlte komplett |
| LA-5 → LA-6+7+8: Chorübung aufgeteilt | DOK-3 C.8 — 3-Phasen-Zyklus, Performance-Player eigenständig |
| LA-6+7+8 alt → LA-9+10+11: Player-Ausbau | Umbenannt, inhaltlich gleich |
| LA-9+10 alt → LA-12+13: Bio Sek1 | Umbenannt, inhaltlich gleich |
| LA-11 alt → LA-16: Launch | Umbenannt |
| LA-12 alt → LA-17: Zahlung | Umbenannt |
| LA-14 neu: Duell-Modus Lern-App | DOK-3 C.6 Ebene 3 — fehlte komplett |
| LA-15 neu: Klassen-Dashboard | DOK-3 C.6 Ebene 4 — fehlte komplett |
| LA-1 + LA-2: Status → abgeschlossen | Fertiggestellt März 2026 |
| Offene-Punkte-Tabelle | DOK-3 Offene Punkte strukturiert |
