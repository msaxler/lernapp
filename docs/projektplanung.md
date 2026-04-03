# Projektplanung — QuizAway & Xalento

*Version 3.3 · April 2026 · DOK-2 v21*
*AP1–AP13 abgeschlossen · LA-1–LA-7 (Teil 1) abgeschlossen · vollständig mit DOK-3 v9 abgeglichen*

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

## 2. Xalento-Arbeitspakete (LA-1–LA-23)

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
- **Willkommen-zurück-Nachricht:** Kehrt ein Nutzer nach > 7 Tagen zurück, zeigt Xalento aktiv: *„Du hast 2 Wochen pausiert — kein Problem. FSRS hat deine Karten nicht vergessen, nur neu geplant. Heute sind X Karten fällig."* Kein Schuldgefühl, keine verlorene Arbeit.
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
A (Zuhören/Media-Player), B (Singen/Performance-Player), C (Bewertung/Intonation).
LA-6–LA-8 bauen alle drei Phasen auf gemeinsamer Architektur.*

#### Architektur-Leitprinzipien (gültig für LA-6–LA-8)

Erkenntnisse aus Analyse bewährter Open-Source-Projekte (mei-friend) und
konzeptioneller Auseinandersetzung mit dem Synchronisationsproblem:

**1. Zeit als gemeinsame Referenz — nicht Pixel-Breite**
Score-Scroll und Karaoke-Scroll teilen dieselbe Zeitbasis. Breiten-Matching
zwischen SVG-Takten und Karaoke-Slots ist fragil. Stattdessen:
```
translateX = containerWidth/2 − currentTime × pxPerSec
pxPerSec   = svgTotalWidth / totalDurationSec   (einmalig berechnet)
```
Score und Karaoke können unterschiedliche `pxPerSec`-Werte haben —
wichtig für Mobile: Karaoke lesbar groß, Score kompakter.

**2. Karaoke: aktive Silbe immer zentriert**
Kein fester Slot-Breiten-Match. Stattdessen:
```
delta = containerCenter − (activeEl.getBoundingClientRect().center)
lyricsWrapper.style.transform = translateX(delta + "px")
```
Aktives Wort bleibt stabil in der Mitte, Rest scrollt relativ. Optimal für
Mobile (großer Font, kein Mitlesen im Vorbeifahren).

**3. Note-Highlighting via Timemap (mei-friend Pattern)**
`renderToTimemap()` → `{ tstamp, on[], off[] }` — alle Timestamps in ms
bei Score-Tempo. Skalierung bei Tempo-Änderung: `delayMs = tstamp × (bpmRef/bpm)`.
CSS: `.note-active use, .note-active path { fill: #D97706 !important }`.

**4. SATB-Layout: volle Höhe, horizontaler Scroll**
Verovio rendert alle Stimmen in ein einziges hohes SVG (Systeme untereinander).
Score-Container: `overflow: hidden`, horizontaler Scroll. Kein vertikales Scrollen —
alle Stimmen sind immer gleichzeitig sichtbar.

**5. Stimm-Auswahl: Dimming der Nicht-Übungsstimme**
```css
g.staff { opacity: 0.25 }          /* alle dimmen */
g.staff-N { opacity: 1.0 }         /* Übungsstimme N hervorheben */
```
Verovio-SVG enthält `g.staff-1`, `g.staff-2` etc. — direkt ansprechbar.

**6. Phase-aware Intonation (für Performance-Player Phase C)**
Tonphasen haben unterschiedliche Toleranzen — wie ein Chorleiter bewertet:
```
Attack  (erste 20% der Notendauer): ±40 Cent  — Einsatz darf unscharf sein
Stable  (20–80 %):                  ±15 Cent  — Halteton wird gemessen
Release (letzte 20 %):              ±50 Cent  — Ende egal
```
Score pro Syllable: `max(0, 1 − abs(cents) / tolerance)` (linear).

**7. Vibrato-Analyse**
Vibrato ist kein Fehler — muss herausgefiltert oder separat bewertet werden:
- Stabilität: Pitch-Buffer über ~200 ms, stdDev < 5 Hz → stabil, sonst Vibrato
- Rate: Zero-Crossing-Count / Dauer / 2 → Hz (Ziel: 4–7 Hz)
- Breite: max − min in Cent (Ziel: 20–50 ¢)

**8. Phrasen-Bewertung**
Einzelsilben-Score ist musikalisch unvollständig. Phrasen-Score:
```
phraseScore = Σ(syllableScore × noteDuration) / Σ(noteDuration)
```
Phrasengrenzen: Pause > 500 ms oder MEI/MusicXML `<phrase>`-Markierung.

**9. Pitch-Erkennung: Autocorrelation korrekt**
Standard-Algorithmus sucht **minimale** Differenz (größte Ähnlichkeit):
```typescript
let best = Infinity
for (let lag = 8; lag < 1000; lag++) {
  const corr = sum |buffer[i] − buffer[i+lag]|
  if (corr < best) { best = corr; bestLag = lag }
}
freq = sampleRate / bestLag
```
(Nicht Maximum — das wäre invertiert und liefert falsches Ergebnis.)

#### LA-6 — Chorübung Phase A: Media-Player ✅ abgeschlossen

**Voraussetzungen** LA-3
**Output** Media-Player-Komponente (60/40-Layout) — MusicXML-Rendering via Verovio SVG,
Ton-Synthese via Tone.js PolySynth, Tempo-Kontrolle 50–150 %, Liedtext-Panel mit
Takt-Synchronisation, FSRS-Bewertung nach dem Abspielen
**Architektur (endgültig nach Umbau von OSMD + Web Audio API):**
- `useVerovio(musicXml)` → SVG lazy (Verovio WASM ~7.5 MB, eigener Auto-Chunk)
- `useMediaPlayer(notes, bpmRef)` → Tone.js `PolySynth` + `Transport.schedule()`
- `parseMusicXml(xml)` liefert `ParsedNote[]` — MusicXML-Parser unverändert korrekt
- OSMD vollständig entfernt
- Code-Splitting: `vendor-tone` (235 kB) + auto-chunk `verovio-module` (7.5 MB lazy)
**Deck** SingOn-Chor Bass 2 — alle 5 Sequenzen spielbar, FSRS-Integration
**Testkriterium** 5 Chorübungen abspielen · Tempo-Slider funktioniert ·
Verovio SVG korrekt gerendert · 77 Tests grün

#### LA-7 — Cursor-Sync + Layout-Refinements + Lyrics

**Voraussetzungen** LA-6
**Status** Teil 1 abgeschlossen ✅

**Teil 1 — Note-Cursor-Sync ✅ abgeschlossen**
- `useVerovio` liefert `timemap: TimemapEvent[]` aus `renderToTimemap()`
- `useMediaPlayer` scheduliert alle `on`/`off`-Timeouts vor Playback-Start
- CSS `.note-active use, .note-active path { fill: #D97706 !important }`
- Scaling korrekt: `delayMs = tstamp × (bpmRef / bpm)` bei Tempo-Änderung
- Pattern übernommen von mei-friend (MIT): `classList.add/remove` + Child-Propagation

**Teil 2 — Score-Scroll: Zeit als gemeinsame Referenz**
Aktuell: Takt-Mittelpunkte aus DOM, `translateX = containerWidth/2 − measureCenter[idx]`
→ Ziel: zeit-basiert, robuster bei variablen Taktbreiten:
```typescript
const pxPerSec    = svgTotalWidth / totalDurationSec
const currentTime = offsetSec  // aus Tone.Transport oder setTimeout-Tracking
setTranslateX(containerWidth / 2 − currentTime * pxPerSec)
```
Vorteil: Tempo-Änderungen wirken automatisch korrekt (kein Neuberechnen der Positionen).

**Teil 3 — Karaoke-Panel: aktive Silbe zentrieren**
Aktuell: feste Slot-Breiten + gleicher translateX wie Score
→ Ziel: Mobile-optimiertes Pattern:
```typescript
const rect  = activeEl.getBoundingClientRect()
const delta = containerCenter − (rect.left + rect.width / 2)
setKaraokeTranslate(delta)
```
Aktive Silbe bleibt stabil in der Mitte, Rest scrollt relativ. Score und Karaoke
teilen Zeitbasis aber können unterschiedliche `pxPerSec`-Werte haben.

**Teil 4 — Lyrics in MusicXML einbetten**
`<lyric>` in `<note>`-Elemente von `singon-bass2.ts` eintragen:
```xml
<lyric number="1">
  <syllabic>single</syllabic>   <!-- begin | middle | end | single -->
  <text>Und</text>
</lyric>
```
Verovio rendert Lyrics automatisch unter Noten im SVG.
`MediaContent.lyrics[]` bleibt erhalten — dient weiterhin dem Karaoke-Panel.

**Technologie** Verovio Timemap, Tone.js Transport, CSS transitions
**Testkriterium** Aktive Note leuchtet orange · Karaoke-Silbe zentriert ·
Score scrollt zeit-basiert · Lyrics im SVG sichtbar

---

#### LA-8 — Performance-Player Phase B + C + Chorübung Deck

**Voraussetzungen** LA-7

**Teil 1 — Performance-Player Phase B: Singen**

*Ablauf:* App spielt N Takte als Anlauf → Aufnahme startet automatisch →
Sänger singt → Selbsteinschätzung → FSRS-Bewertung

- N-Takt-Anlauf konfigurierbar (Standard: 1 Takt)
- `MediaRecorder API` für Aufnahme, `getUserMedia` mit Fallback-Hinweis für iOS
- Looping schwieriger Stellen: Taktbereich wählbar, automatische Wiederholung
- Stimm-Auswahl für SATB:
  - Dropdown: Sopran / Alt / Tenor / Bass
  - Verovio SVG: `g.staff` via CSS opacity gedimmt, Übungsstimme hervorgehoben
  - Karaoke-Panel zeigt nur Text der gewählten Stimme
- Selbsteinschätzung: *Nochmal / Unsicher / Gut / Sicher* → FSRS-Rating
- `Tone.Part` als saubere Ablösung der `Transport.schedule()`-Einzelaufrufe

**Technologie** MediaRecorder API, getUserMedia (iOS Safari: requiresUserGesture),
Tone.Part, CSS opacity für Stimm-Dimming
**Testkriterium** Anlauf spielt korrekte Takte · Aufnahme startet/stoppt ·
Stimm-Dimming sichtbar · Selbsteinschätzung speichert FSRS · iOS Safari getestet

---

**Teil 2 — Performance-Player Phase C: Intonation**

*Pitch-Analyse im Browser via Web Audio API — kein Server, kein Upload*

**Pitch-Erkennung**
- Autocorrelation auf Float32-Buffer (korrekt: minimale Differenz → bestLag)
- `freq = sampleRate / bestLag`
- Stabilitäts-Filter: Pitch-Buffer über ~200 ms, `stdDev < 5 Hz` → stabiler Ton,
  sonst Vibrato → nicht in Score einberechnen

**Phase-aware Intonation**
```
Attack  (erste 20 % der Notendauer): ±40 ¢ Toleranz
Stable  (20–80 %):                   ±15 ¢ Toleranz  ← streng
Release (letzte 20 %):               ±50 ¢ Toleranz
```
Score: `max(0, 1 − |cents| / tolerance)` → 0.0–1.0 pro Frame

**Vibrato-Analyse** (separater Kanal, kein Fehler)
- Rate: Zero-Crossing-Count / Dauer / 2 → Hz (Ziel: 4–7 Hz)
- Breite: `max(cents) − min(cents)` (Ziel: 20–50 ¢)
- Feedback: „Vibrato zu breit (80 ¢)" / „Vibrato zu langsam (3 Hz)"

**Phrasen-Bewertung**
```
phraseScore = Σ(syllableScore × noteDuration) / Σ(noteDuration)
```
Phrasengrenzen: Pause > 500 ms. Gewichtung macht lange Noten wichtiger als kurze.

**Zielton aus MusicXML**
`parseMusicXml()` liefert bereits `ParsedNote.pitch` (z. B. `"G3"`).
MIDI-Frequenz: `440 × 2^((midi − 69) / 12)`.

**UI — Intonations-Feedback**
- Cents-Anzeige: `|diff| < 10 ¢` → grün · `< 25 ¢` → gelb · `> 25 ¢` → rot
- Phrase-Score nach jeder Phrase: „85 % — gut"
- Vibrato-Feedback als einmalige Meldung nach Phrase
- Kein Punkte-Druck — Information, nicht Bewertung (Gamification-Prinzip)

**Technologie** Web Audio API (AnalyserNode, Float32Array), Autocorrelation,
React state für Echtzeit-Feedback
**Testkriterium** Kammerton A4 wird als 440 Hz erkannt (±5 Hz) ·
Bewusst falscher Ton > 50 ¢ wird rot markiert · Vibrato A4±30 ¢@6 Hz erkannt ·
Phrasen-Score nach Silben korrekt gewichtet · iOS Safari getestet

---

**Teil 3 — Chorübung Deck vollständig**
- SingOn-Chor Bass 2: alle Stücke in Phase A, B, C spielbar
- MusicXML aller Sequenzen mit `<lyric>`-Elementen
- FSRS scheduliert pro Sequenz und Phase unabhängig
- Export/Import des Deck-Fortschritts funktioniert

**Testkriterium** Komplettes Stück durcharbeitbar in allen drei Phasen ·
FSRS-Scheduling korrekt · Export/Import funktioniert

---

### Phase 3 — Player-Ausbau (für Informatik Sek I)

*Die folgenden Player decken die Wissenstypen Strukturwissen und Prozesswissen ab —
die Vorbereitung für das Informatik-Deck. Alle teilen dieselbe FSRS-Infrastruktur.*

#### LA-9 — Beschriftungs-Player

**Voraussetzungen** LA-3
**Output** SVG-Bild mit nummerierten Pfeilen — Lernender tippt Bezeichnungen ein ·
typischer Aufgabentyp für Hardware-Diagramme, Netzwerktopologien, UML
**Technologie** React, SVG-Overlay
**Testkriterium** Computerhardware-Diagramm mit 5 Komponenten korrekt beschriftet ·
Tipp-Toleranz (Groß/Kleinschreibung, Leerzeichen) · FSRS-Integration

#### LA-10 — Zuordnungs-Player

**Voraussetzungen** LA-3
**Output** Drag-and-Drop Zuordnung — zwei Spalten verbinden ·
fühlt sich an wie Sammelkartenspiel
**Technologie** React DnD, Touch-Events (Pointer Events API)
**Testkriterium** 5 Datentyp-Beispiel-Paare korrekt zuordnen auf Touch-Screen ·
FSRS-Integration

#### LA-11 — Lückentext-, Sortier- und Fehler-finden-Player

**Voraussetzungen** LA-3
**Output** Drei interaktive Aufgabenformate für Informatik Sek I:
- **Lückentext** (Dropdown + Freitext): Pseudocode oder Algorithmus-Beschreibung mit Lücken
- **Sortieraufgabe**: Schritte eines Ablaufs in die richtige Reihenfolge bringen
- **Fehler finden**: Fehlerhafter Pseudocode / fehlerhafter Algorithmus — Nutzer markiert die Zeile mit dem Fehler
  und wählt die Korrektur aus. Entspricht dem informatikdidaktischen Konzept "Debugging als Lernform":
  Fehler erkennen ist kognitiv anspruchsvoller als Lücken füllen (Bloom Stufe 4 Analysieren)
**Technologie** React, TypeScript
**Testkriterium** Algorithmus-Lückentext (z.B. Bubblesort) spielbar · Sortierschritte sortierbar ·
Fehler-finden-Aufgabe: fehlerhafter Pseudocode korrekt identifiziert · FSRS-Integration

---

### Phase 4 — Informatik Sek I

#### LA-12 — Informatik-Inhaltspipeline

**Voraussetzungen** LA-3
**Output** Kuratierte JSON-Decks aus Lehrplan RLP + OER-Quellen,
strukturiert nach Modul-Raster Klasse 5–8 (5 Module, RLP-orientiert)
**Technologie** Python, ggf. APIs von Code.org / CS Unplugged
**Quellen:**
- Lehrplan RLP Gymnasium Informatik Sek I (Kompetenzen + Inhalte pro Jahrgang)
- OER-Plattformen: CS Unplugged (Algorithmen/Codierung), Open Roberta (Programmierung), Code.org
- Python/JavaScript-Ökosystem: Tutorials, Übungsaufgaben, Beispiele
**Modul-Kurationsraster (Klasse 5–8, RLP-orientiert):**
- **Modul 1** (Kl. 5/6): Algorithmen & Problemlösen — Ablaufdiagramme, Struktogramme, Sortierverfahren
- **Modul 2** (Kl. 5/6): Daten & Codierung — Binärsystem, ASCII, Datenkompression, Verschlüsselung
- **Modul 3** (Kl. 6/7): Erste Programmierung — Variablen, Schleifen, Bedingungen (Scratch/Blockly → Python)
- **Modul 4** (Kl. 7/8): Informatiksysteme — Hardware, Betriebssystem, Netzwerke, Internet-Protokolle
- **Modul 5** (Kl. 8): Informatik & Gesellschaft — KI-Grundlagen, Datenschutz, Algorithmen-Fairness
Startmodul (Pareto): Modul 1 "Algorithmen verstehen" — sofort demonstrierbar im Sortier-Player (LA-11)
**Hinweis** Weniger fertige Aufgabendatenbanken als in Mathe — dafür mehr Freiheit
bei didaktischer Aufbereitung. Engpass ist Kuration, nicht Material.
**Testkriterium** ≥40 Karten pro Modul · Modul 1 vollständig kuratiert · alle Player-Typen abgedeckt

#### LA-13 — Informatik Sek I Deck

**Voraussetzungen** LA-9 + LA-10 + LA-11 + LA-12
**Output** Vollständig kuratiertes Deck Informatik Klasse 7–8 — alle Player-Typen genutzt ·
Lehrplan-konform RLP
**Startmodul (Pareto):** "Algorithmen verstehen" — Sortierverfahren, Pseudocode, Struktogramme
**Testkriterium** Modul Algorithmen komplett durcharbeitbar ·
FSRS plant Wiederholungen · Export/Import funktioniert

---

### Phase 5 — Gamification erweitert

#### LA-14 — Duell-Modus Lern-App (Gamification Ebene 3)

**Voraussetzungen** LA-3 + LA-4
**Output** Zwei Lernende treten gegeneinander an — technisch aus QuizAway übernommen,
thematisch an den Lerninhalt des aktuellen Decks gebunden (nicht Geo-Quiz sondern
Informatik/Mathematik/Geschichte)
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
- **Inhalts-Heatmap:** Welche Karten sitzen in der Klasse am schlechtesten? Ranking der 5 schwächsten Karten mit Beherrschungsquote (z. B. *„Zellkern: nur 3 von 18 Schülern sicher"*). Kein Schüler-Ranking, keine öffentlichen Vergleiche. — *Aufwand gering: FSRS-Daten liegen bereits in Dexie, nur neue Aggregations-Abfrage.*
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

#### LA-18 — Choir Trainer: Übungsabschnitte — Bottom Sheet & Infrastruktur (V1) ✅

**Status** Abgeschlossen
**Voraussetzungen** LA-8 abgeschlossen
**Aufwand** ~2 Tage · Risiko: NIEDRIG
**Output** Fundament für LA-19–LA-21

- Dexie-Schema: neue Tabellen `practiceSections`, `pieceSectionMeta`
- Toggle-Panel (kein Drag) — Button öffnet/schließt Panel vollständig
- Ein Panel (keine Snap-Points): Controls oben, Abschnittsliste unten, scrollbar
- Persistent Bar: Play/Pause · Abschnitts-Dot · Toggle-Button · Übestimme-Lautstärke
- Bestehende Player-Controls (Tempo, Metronom, Lautstärke, Navigation) ins Panel migrieren

**Testkriterium** Panel öffnet/schließt stabil auf iOS + Android · Dexie-Tabellen angelegt

---

#### LA-18b — Choir Trainer: Bottom Sheet Drag & Snap-Points (V2)

**Voraussetzungen** LA-18 + LA-21 (Grundfunktion stabil im Einsatz)
**Aufwand** ~2 Tage · Risiko: MITTEL
**Output** Komfortverbesserung: echtes Drag-Gesture-System mit 2 Snap-Points

- Snap 1 (~35%): Controls · Snap 2 (~70%): Controls + Abschnittsliste
- Touch-Drag zum Öffnen/Schließen (Pointer Events API)

**Testkriterium** Drag + Snap funktioniert auf iOS + Android ohne Ghost-Touches

---

#### LA-19 — Choir Trainer: Abschnittsdefinition & Score-Visualisierung (V1) ✅

**Status** Abgeschlossen
**Voraussetzungen** LA-18
**Aufwand** ~2–3 Tage · Risiko: NIEDRIG
**Output** Nutzer können Abschnitte definieren und im Score sehen

- Abschnittsdefinition per Taktnummer-Eingabe: "Von Takt [ ] bis Takt [ ]"
- Score-Visualisierung: taktgenaue Farbblöcke (ganze Takte eingefärbt, kein note-präzises Overlay)
- Abschnittsliste im Panel: Farb-Dot · Name (automatisch) · Taktbereich · Löschen
- Max. 7 Abschnitte pro Stimme pro Stück
- Farben: Xalento-Palette rotierend (7 Farben, s. Konzept)
- "+ Neuer Abschnitt" Button · Löschen per Long-Press in der Liste

**Testkriterium** Abschnitt anlegen, sehen, löschen funktioniert · Taktblöcke korrekt eingefärbt

---

#### LA-19b — Choir Trainer: Note-präzise Abschnittsdefinition (V2)

**Voraussetzungen** LA-19 + LA-21 (Grundfunktion stabil im Einsatz)
**Aufwand** ~3 Tage · Risiko: HOCH
**Output** Komfortverbesserung: Abschnitt per Long-Press direkt im Score definieren

- Edit-Modus: Long-Press Startnote (grün markiert) → scrollen → Endnote antippen → speichern
- Note-präzise Farbstreifen (4px) statt taktgenaue Blöcke
- Abbruch: erneuter Long-Press / Abbrechen-Button

**Testkriterium** Note-präzise Grenzen werden korrekt auf scrollendem SVG dargestellt

---

#### LA-20 — Choir Trainer: Section-Loop & Playback

**Voraussetzungen** LA-19
**Aufwand** ~2–3 Tage · Risiko: NIEDRIG
**Output** Loop und Playback kennen Sektionsgrenzen

- `useMediaPlayer`: aktive Sektionsgrenzen (`startTstamp` / `endTstamp`) respektieren
- Loop mit einstellbarer Pause zwischen Wiederholungen (Default 2 s, Range 0–5 s)
- Freier Playback-Start: Tap auf beliebige Note → spielt ab dort bis Stückende (kein Loop)
- Nach Pause: Score bleibt an Playback-Position, Play setzt dort fort

**Testkriterium** Loop läuft stabil durch mehrere Wiederholungen · Pause korrekt · Stop hält Position

---

#### LA-21 — Choir Trainer: FSRS-Integration & Fortschrittsmodal

**Voraussetzungen** LA-20
**Aufwand** ~3–4 Tage · Risiko: NIEDRIG
**Output** Messbarer Lernfortschritt pro Abschnitt und Stück

- Automatisches FSRS-Rating nach Session (Loop-Zähler → Heuristik):
  `< 2 → Again · 2–5 → Hard · 6–9 → Good · ≥ 10 → Easy`
- FSRS-Modal (📊-Button im Panel): alle Abschnitte mit FSRS-Status + manueller Override
- Gesamtfortschritt: `Coverage × FSRS-Ø` (Union-Coverage gewichtet nach Abschnittslänge)
- FSRS-Engine aus LA-2 wird wiederverwendet

**Testkriterium** Automatisches Rating wird nach Session korrekt gespeichert ·
Override im Modal funktioniert · Gesamtfortschritt stimmt rechnerisch

---

#### LA-22 — Professionelle Projektstruktur

**Voraussetzungen** LA-21 (Choir Trainer vollständig abgeschlossen)
**Aufwand** ~5–7 Tage · Risiko: NIEDRIG
**Warum jetzt** Vor LA-16 (Launch) muss das Projekt professionell aufgestellt sein —
Testabdeckung, CI/CD, Backup und Dokumentation sind Launch-Voraussetzungen.

**Verzeichnisstruktur**
- Monorepo-Konventionen konsolidieren (`apps/`, `packages/`, `tools/`, `docs/`)
- Trennung von `src/`, `tests/`, `fixtures/`, `mocks/` in allen Paketen
- Aufräumen: lose Dateien im Root entfernen (Setup-Skripte, alte .html-Dateien etc.)

**Build & CI/CD**
- `Makefile` ausbauen: `make ci` als vollständiger Pipeline-Lauf
- GitHub Actions: automatisch test + build + Netlify-Deploy bei Push auf `main`
- Versionierung: semver + `CHANGELOG.md`

**Tests & Testsuite**
- Teststruktur: Unit (FSRS-Engine, musicxml-Parser) · Integration (Dexie-Operationen) · E2E (Playwright)
- Testfälle für alle kritischen Pfade dokumentieren
- Coverage-Report (Ziel: >80% für Engine-Code)
- `make test` läuft vollständige Suite inkl. Coverage

**Backup**
- Dexie-Export/Import vollständig (lokale Nutzerdaten sichern)
- Git-Branching-Strategie: `main` (stabil) · `develop` (aktiv) · `feature/*`
- Backup-Dokumentation für Nutzer (PWA-Daten sind lokal — was passiert bei Gerätewechsel?)

**Dokumentation**
- ADR-Verzeichnis ausbauen (bereits begonnen in `docs/konzepte/`)
- JSDoc → TypeDoc für öffentliche APIs
- `CONTRIBUTING.md` — Onboarding für neue Entwickler
- `CLAUDE.md` aktuell halten (KI-Kontext)

**Testkriterium** `make ci` läuft grün (lint + typecheck + tests + build) ·
GitHub Actions deployt automatisch · Coverage-Report erzeugt ·
Neuer Entwickler kann Projekt in <30 min aufsetzen

---

#### LA-23 — Blockly-Programmierumgebung (Informatik Sek I)

**Voraussetzungen** LA-22 (Projektstruktur stabil) + LA-11 (Sortier/Lückentext-Player)
**Aufwand** ~7–10 Tage · Risiko: MITTEL (externe Bibliothek, Mobile-Kompatibilität prüfen)
**Warum** Blockly ist der technologische Differenziator für Informatik Sek I: visuelles
Programmieren direkt im Browser, kein Install, sofortiges Feedback. Kein Quizlet, kein
Anki, kein anderes Lerntool bietet das. Zielgruppe Klasse 5–7 (Modul 3 der Pipeline).

**Output** Neues Package `packages/blockly-player` — ein eigenständiger React-Player-Typ:
- Blockly-Workspace embedded (Google Blockly via npm)
- Aufgabentypen:
  - **Puzzle-Modus**: Vorgefertigte Blöcke in richtige Reihenfolge legen (wie Sortier-Player)
  - **Ergänzungs-Modus**: Lückenhaftes Programm vervollständigen (Parameter, Werte eintragen)
  - **Freier Modus**: Kleines Programm selbst bauen, Output wird geprüft
- Mobile-first: Touch-Drag für Blöcke, Pinch-Zoom für Workspace
- FSRS-Integration: Bewertung nach Puzzle-/Ergänzungsaufgabe automatisch

**Abgrenzung** Kein vollwertiger Code-Editor — Blockly bleibt visuell und spielerisch.
Python/Text-Programmierung ist LA-∞ (nach Launch). Blockly ist der Einstieg.

**Technologie** Google Blockly (Apache-2.0), React, TypeScript; ggf. Skulpt für Python-Preview
**Testkriterium** Modul-3-Aufgabe "Schleife bauen" im Puzzle-Modus auf Smartphone lösbar ·
FSRS-Bewertung korrekt gespeichert · Build-Größe <500 KB Zuwachs

---

#### LA-24a — Redakteur-Tool: MusicXML-Cleaner, Preview & Signing

**Voraussetzungen** LA-22 (Projektstruktur stabil)
**Aufwand** ~5–7 Tage · Risiko: NIEDRIG
**Warum** Stücke sind aktuell hardcoded im Build. Vor jeder Erweiterung der Bibliothek braucht der Redakteur ein Werkzeug das MusicXML prüft, bereinigt, hörbar und sichtbar macht — und erst dann signiert. Dieser Schritt ist unabhängig von der Netzwerk-Infrastruktur und sofort nutzbar.

**Vertrauensmodell (Trust Chain)**

Der Root-Redakteur (zunächst: Entwickler) hält ein secp256k1-Keypair — kompatibel mit Nostr. Er kann weitere Peers als Redakteure zulassen, indem er deren Public Key signiert. Zulassung und Entzug werden als signierte Ereignisse publiziert. Clients prüfen bei jedem Stück: *Ist die Signatur von einem aktuell gültigen Redakteur?* — sonst wird das Stück ignoriert.

```
Root-Redakteur (secp256k1 Keypair)
  ├── signiert Stücke              → gültig für alle Clients
  ├── signiert Redakteur-B pubkey  → B wird zugelassen
  └── signiert Revocation B        → B abgelehnt ab sofort
```

**Vier Stufen des Redakteur-Flows**

*Stufe 1 — Einlesen & Validieren*
- Pflichtfelder vorhanden? (Noten, Parts, Tempo, Taktart, Liedtext)
- Verovio rendert fehlerfrei?
- Mindest-Notenanzahl (kein leeres oder fragmentiertes Stück)
- Ergebnis: `OK` / `Warnung (weiter möglich)` / `ABGELEHNT` mit Begründung

*Stufe 2 — Bereinigen (nur wenn nicht abgelehnt)*

| Element | Behandlung |
|---|---|
| Noten, Pausen, Takte, Taktart, Tonart | ✅ behalten |
| Tempo-Markierungen, Probenzeichen | ✅ behalten |
| Liedtext (Silben unter Noten) | ✅ behalten |
| Dynamik (p, f, cresc.) | ⚙️ konfigurierbar |
| Fingersätze, Bogentexte, Editorkommentare | ❌ entfernen |
| Copyright-Texte im Score, Verlagshinweise | ❌ entfernen |
| MIDI-Spielanweisungen | ❌ entfernen |
| Seitenumbrüche, Layout-Hints | ❌ entfernen (Verovio regelt das) |

Tool gibt Bereinigungsbericht aus: was wurde entfernt, was blieb, Vorher/Nachher-Größe.

*Stufe 3 — Preview (visuell + auditiv)*
- Bereinigtes Stück wird direkt im Choir Trainer geladen (Redakteur-Modus: lokale Datei statt Bibliothek)
- Redakteur hört und sieht exakt was der Nutzer später bekommt
- Alle Stimmen einzeln abspielbar, Score-Scroll prüfbar
- Entscheidung: Freigeben oder Ablehnen (mit Begründung im Log)

*Stufe 4 — Signieren & Paketieren*
- Metadaten anlegen: Titel, Stimmen, Komponist, Lizenz, Sprache
- Signatur mit privatem Redakteurs-Key (secp256k1)
- Output: `{ musicxml, meta, redakteur_pubkey, timestamp, signature }`
- Paket bereit für LA-24b (Gossip-Verteilung)

**Implementierung**
- Node.js CLI: `xalento-editor clean input.xml [--output paket.json]`
- Choir Trainer: URL-Parameter `?local=paket.json` aktiviert Redakteur-Modus (lädt lokale Datei)
- Keypair-Verwaltung: `xalento-editor keygen`, `xalento-editor trust peer.pubkey`, `xalento-editor revoke peer.pubkey`
- Alle signierten Redakteur-Zulassungen und Revocations werden lokal als append-only Log gehalten

**Testkriterium**
- Valides SingOn-Stück durchläuft alle 4 Stufen fehlerfrei
- Defektes MusicXML wird mit Begründung abgelehnt
- Bereinigtes Stück klingt und sieht im Choir Trainer korrekt aus
- Signiertes Paket wird von einem zweiten Gerät als gültig erkannt

---

#### LA-24b — Gossip-Verteilung: P2P-Bibliothek & Redakteurs-Netz

**Voraussetzungen** LA-24a (Redakteur-Tool + Paket-Format stabil) · LA-16 (erste echte Nutzer vorhanden)
**Aufwand** ~7–10 Tage · Risiko: HOCH (P2P-Protokoll, Nostr-Integration, Offline-Sync)
**Warum** Sobald mehrere Nutzer oder Redakteure existieren, muss die Stück-Verteilung ohne zentralen Server funktionieren. Jedes Gerät ist Container und Verteiler zugleich.

**Konzept** (Vollbeschreibung → Produktvision C.12)

*Zwei Speicherbereiche pro Gerät:*

**Bibliotheks-Container (persönlich, nutzerverwaltet)**
Der Nutzer wählt aktiv welche Stücke er üben will. Diese liegen vollständig lokal in Dexie — offline spielbar, FSRS-integriert, Abschnitte definierbar. Größe wächst dynamisch mit der Auswahl.

**Gossip-Container (Netzwerk-Beitrag, systemverwaltet)**
Ein vom Nutzer konfigurierter Speicherblock mit fester Mindestgröße (Standard: 50 MB, wählbar: 20 / 50 / 100 / 200 MB). Der Inhalt wird vollautomatisch vom System bestimmt — der Nutzer entscheidet nur über die Größe.

Das System befüllt den Gossip-Container nach zwei Signalen:
- **Nachfrage**: Welche Stücke werden im Netz am häufigsten angefragt und sind am wenigsten verbreitet?
- **Region**: Welche Stücke werden bevorzugt in der eigenen geografischen Umgebung nachgefragt? (grob-granular: Land / Sprachraum — kein Präzisionsstandort)

Eviction: Wenn der Container voll ist, fliegen seltenst-angefragte Stücke raus. Keine erzwungene Überlappung mit der persönlichen Bibliothek — das System platziert was netzwerkweit gerade nützlicher ist.

Ein Stück im Gossip-Container aber nicht in der persönlichen Bibliothek kann der Nutzer nicht direkt spielen — er kann es aber mit einem Klick in die Bibliothek übernehmen.

*Weitere Konzepte:*
- **Gossip-Verbreitung**: Stück-Pakete (aus LA-24a) verbreiten sich P2P über Nostr-Relay oder direkt. Ein Gerät das ein Paket hat, gibt es weiter — kein zentraler Inhaltsserver nötig.
- **Signatur-Prüfung client-seitig**: Jedes empfangene Paket wird gegen die bekannte Redakteurs-Trust-Chain geprüft. Ungültige oder revozierte Signaturen werden stillschweigend ignoriert.
- **Bibliotheks-Screen**: Drei Bereiche — *Meine Bibliothek* (aktiv geübt) · *Verfügbar lokal* (im Gossip-Container, ein Klick zum Übernehmen) · *Verfügbar im Netz* (bekannt aber nicht lokal, Download nötig). Jeder Eintrag zeigt Titel, Stimmen, Lizenz, Signatur-Status.
- **Redakteurs-Netz**: Zulassung und Entzug von Redakteuren propagieren über denselben Gossip-Kanal wie Stücke.
- **Nachfragesignale**: Anonym aggregiert — kein Personenbezug, keine Geräte-ID. Nur Häufigkeit pro Stück pro Region fließt ins Netz.
- **Standort-Einwilligung (opt-in)**: Regionale Platzierung setzt einen bekannten Knoten-Standort voraus. Beim ersten Start des Gossip-Containers erscheint eine Standortabfrage (Browser Geolocation API). Gespeichert wird nur Land + Bundesland/Region — keine Koordinaten, keine Weitergabe. Ablehnung ist jederzeit möglich; der Container arbeitet dann ohne regionale Optimierung weiter (Fallback: globale Nachfrage).

**Abgrenzung**
Kein allgemeines CMS. Kein Upload durch Endnutzer — ausschließlich durch zugelassene Redakteure mit gültigem Keypair. Die initiale Zulassung neuer Redakteure ist ein Out-of-Band-Prozess (Key-Austausch persönlich oder via vertrauenswürdigem Kanal).

**Testkriterium**
- Neues Stück von Redakteur signiert → erscheint auf zweitem Gerät ohne App-Update
- Stück mit ungültiger oder revozierter Signatur wird abgelehnt
- Offline-Nutzung nach einmaligem Empfang funktioniert vollständig
- Gossip-Container wird automatisch befüllt und bei Kapazitätsüberschreitung korrekt evicted
- Bibliotheks-Screen zeigt alle drei Bereiche korrekt an
- Redakteurs-Entzug propagiert und revozierte Stücke werden nicht mehr angezeigt

---

#### LA-25 — Bibliotheks-Ordnungssystem: Recherche & Konzept

**Voraussetzungen** LA-24a (Paket-Format + Metadaten definiert)
**Aufwand** Recherche ~2–3 Tage · Konzept ~1–2 Tage · Risiko: NIEDRIG
**Warum** Bevor das Bibliotheks-UI implementiert wird, muss das Ordnungssystem konzeptionell geklärt sein. Es soll weder zu simpel (nur Ordner) noch zu komplex (beliebige Ontologie) werden — sondern genau das abbilden was Chorsänger und Chorleiter tatsächlich brauchen.

**Ordnungskonzept (geklärt)**

Das Grundprinzip ist bekannt und erprobt — identisch mit dem Bildviewer-Projekt (erstes gemeinsames Projekt): **n:m-Attributsystem**. Kein Hierarchie-Problem, kein Widerspruch.

```
Stück  ←——→  Attribut  (beliebig viele, beliebige Kombination)

"In manus tuas"  →  [Byrd] [16. Jh.] [Weihnachtskonzert 2025] [Latein] [Bass]
"O magnum"       →  [Pärt] [Modern]  [Weihnachtskonzert 2025] [Latein] [Sopran]

Filter [Weihnachtskonzert 2025]      → beide Stücke
Filter [Byrd] + [Bass]               → nur "In manus tuas"
Filter [Latein] + [Modern]           → nur "O magnum"
```

Ein Stück kann in beliebig vielen Konzerten, Epochen, Sammlungen erscheinen — ohne Widerspruch, ohne Hierarchie-Problem. Die "Struktur" ergibt sich aus der Attribut-Kombination. Das Muster ist einfach, erweiterbar und bereits implementiert.

*Attribut-Dimensionen (Defaultsatz — wird durch Recherche verfeinert)*
```
Konzert / Anlass:  "Weihnachtskonzert 2025" · "Jahreshauptversammlung"
Chor / Ensemble:   "SingOn" · "Kammerchor XY"
Komponist:         "Byrd" · "Bach" · "Pärt"
Epoche:            "Renaissance" · "Barock" · "Romantik" · "Modern"
Sprache:           "Latein" · "Deutsch" · "Englisch"
Schwierigkeit:     "Einsteiger" · "Fortgeschritten" · "Konzertreif"
Stimme:            aus MusicXML automatisch übernommen
Eigene Tags:       frei definierbar, lokal privat
```

**Attribut-Quellen und Kontrolle**
- Redakteur schlägt Metadaten vor (im signierten Paket aus LA-24a)
- Nutzer kann jeden Vorschlag **übernehmen oder ablehnen** — für sich persönlich
- Eigene Tags sind immer lokal und privat
- Standardfelder aus MusicXML (Titel, Komponist, Opus) werden automatisch übernommen

**Recherche-Auftrag: Wie lösen Top-Apps die Bibliotheksfrage?**

Zu untersuchende Apps:
| App | Plattform | Schwerpunkt |
|---|---|---|
| forScore | iOS | Professionelle Notenverwaltung, sehr verbreitet |
| Mobile Sheets | Android | Breite Nutzerbasis, viele Metadaten-Felder |
| Piascore | iOS | Einsteigerfreundlich, einfache Kategorisierung |
| Newzik | iOS/Web | Kollaborativ, Ensemble-orientiert |
| MusicReader | Multi | Langzeit-etabliert, komplexe Bibliothek |
| Choral Public Domain Library (CPDL) | Web | Chorspezifisch, Metadaten-Standard |
| IMSLP | Web | Klassik-Archiv, Kategorisierungstiefe |

Forschungsfragen (fokussiert — Grundprinzip n:m ist geklärt):
1. **Attribut-Dimensionen**: Welche Kategorien/Dimensionen sind in der Branche Standard? Was fehlt im eigenen Defaultsatz?
2. **Metadaten-Felder**: Welche Felder sind Pflicht, welche optional? Gibt es Branchenstandards (z.B. Dublin Core, MusicXML-eigene Felder)?
3. **MusicXML-Integration**: Werden eingebettete Metadaten (work-title, composer, rights, language) automatisch übernommen?
4. **Nutzer-eigene Attribute**: Können Nutzer eigene Tags anlegen? Wie werden Redakteurs-Attribute von Nutzer-Tags unterschieden?
5. **Ensemble-/Gruppenkontext**: Kann ein Chorleiter eine Stückliste für eine Gruppe definieren, die Mitglieder dann übernehmen?

**FSRS-Status auf Gruppenebene (Kernanforderung)**

Jedes Attribut / jede Gruppe erbt automatisch einen FSRS-Status aus den ihr zugeordneten Stücken. Keine zusätzlichen Daten nötig — die FSRS-Werte existieren bereits pro Stück und werden on-the-fly aggregiert.

Zwei Kennzahlen pro Gruppe:
- **Coverage**: Wieviele Stücke wurden überhaupt schon geübt? → `geübt / gesamt`
- **Mastery**: Wie gut sind die geübten im Schnitt? → gewichteter FSRS-Stability-Durchschnitt

```
Konzert "Weihnachten 2026" — 15 Stücke
  ├── Coverage:  6 / 15  (40 % begonnen)
  ├── Mastery:   Ø Stability der 6 geübten → "Gut"
  └── Anzeige:   "6 Stücke konzertreif · 9 noch nicht begonnen"

Sammlung "Bach-Choräle" — 900 Stücke
  ├── Coverage:  400 / 900  (44 % begonnen)
  ├── Mastery:   Ø Stability der 400 geübten
  └── Anzeige:   Fortschrittsbalken + Stability-Farbe

Komponist "Byrd" — 12 Stücke
  ├── Coverage:  12 / 12  (100 % begonnen)
  └── Mastery:   Ø = 8.4 → "Sehr gut"
```

Dieselbe Formel wie `calcProgress()` im `SectionProgressModal` (LA-21) — dort für Abschnitte eines Stücks, hier skaliert auf Bibliotheks-Ebene. Kein neues Konzept, nur eine neue Aggregations-Ebene.

Phasen (Hören / Singen) werden getrennt ausgewiesen — ein Stück kann für Phase A "Gut" und für Phase B "Neu" sein. Die Gruppe zeigt beide Werte.

**Output des Arbeitspakets**
- Kurze Analyse der 5–7 untersuchten Apps (je 1 Seite)
- Vergleichstabelle: Attribut-Dimensionen · Suche · MusicXML-Nutzung · Nutzer-Attribute · FSRS-Äquivalent (falls vorhanden)
- Empfehlung: Defaultsatz der Attribut-Dimensionen für den Choir Trainer
- Entwurf des Metadaten-Schemas für LA-24a (welche Felder im signierten Paket)
- Spezifikation der FSRS-Gruppen-Aggregation (Coverage + Mastery pro Attribut)

**Testkriterium**
- Jedes SingOn-Stück kann in das empfohlene Schema eingeordnet werden
- Konzert "Weihnachten 2026" mit 15 Stücken zeigt korrekten Coverage- und Mastery-Wert
- Schema ist erweiterbar ohne Breaking Change
- Redakteur-Metadaten und Nutzer-eigene Tags sind klar getrennt
- Phase A und Phase B werden getrennt ausgewiesen

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
| QuizAway-Timer: nur Duell-Modus — Sofa/Route/Live ohne Zeitdruck | B.3 | Vor nächstem QA-Release |
| QuizAway Kategorie: Historische Persönlichkeiten (Geburts-/Wirkungsorte) | B.4 | Datenpipeline klären |
| QuizAway Kategorie: Fun Facts (skurriles Ortswissen) | B.4 | Datenpipeline klären |
| Performance-Player Mikrofon-Analyse Phase C | C.8 | Nach LA-7 |
| Analyse-Player (Essay, Argumentation) | C.11 | Phase 3+ |
| Persistenz-Backend (Nextcloud vs. kDrive) | Offene Punkte | Vor LA-16 entscheiden |
| QuizAway → Xalento Neubau (Local-First, Xalento-Stack) | B.6 | Nach LA-8 (Choir Trainer stabil) |

---

## 4. Abhängigkeiten Xalento

```
LA-1 → LA-2 → LA-3 → LA-4
                  ↓       ↓
                 LA-5    LA-14
                  ↓
              LA-6 → LA-7 → LA-8 → LA-18 → LA-19 → LA-20 → LA-21 → LA-22 → LA-23 → LA-16 → LA-17
                                                                                  ↓
                                                                                LA-24
                                      ↓               ↓
                                    LA-18b           LA-19b
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
| LA-9+10 alt → LA-12+13: Informatik Sek I | Umbenannt + Fach gewechselt (Bio → Informatik) |
| LA-11 alt → LA-16: Launch | Umbenannt |
| LA-12 alt → LA-17: Zahlung | Umbenannt |
| LA-14 neu: Duell-Modus Lern-App | DOK-3 C.6 Ebene 3 — fehlte komplett |
| LA-15 neu: Klassen-Dashboard | DOK-3 C.6 Ebene 4 — fehlte komplett |
| LA-1 + LA-2: Status → abgeschlossen | Fertiggestellt März 2026 |
| LA-18–LA-21 neu: Choir Trainer Übungsabschnitte | Konzept April 2026 — Pareto-V1 + V2-Pakete |
| LA-22 neu: Professionelle Projektstruktur | April 2026 — vor Launch, nach Choir Trainer |
| LA-23 neu: Blockly-Programmierumgebung | April 2026 — Informatik-Differenziator, nach LA-22 |
| LA-24a neu: Redakteur-Tool (Cleaner, Preview, Signing) | nach LA-22 — sofort nutzbar für SingOn-Stücke, kein Netzwerk nötig |
| LA-24b neu: Gossip-Verteilung (P2P-Bibliothek) | nach LA-24a + LA-16 (erste Nutzer) — Nostr-Relay, Trust-Chain, Bibliotheks-Screen |
| LA-11 erweitert: + Fehler-finden-Player | April 2026 — Debugging als Lernform (Bloom 4) |
| LA-12 erweitert: Modul 1–5 Kurationsraster | April 2026 — RLP-orientiert, Klasse 5–8 |
| Offene-Punkte-Tabelle | DOK-3 Offene Punkte strukturiert |
| LA-4: Willkommen-zurück-Nachricht | ADR April 2026 — Pausen kommunizieren statt bestrafen |
| LA-15: Inhalts-Heatmap | ADR April 2026 — Inhalt statt Aktivität im Dashboard |

---

## 6. Strategische Entscheidungen (April 2026)

*Quelle: ADR_LernBattle_Analyse.md · April 2026*

### StimmBild — Pause bis externe Unterstützung gesichert

StimmBild bleibt auf dem aktuellen Stand. Gründe:

- Zeitdruck Berlin-Wahl September 2026 zu hoch für Solo-Entwicklung
- Auflagen für politische Apps (Neutralität, Quellentransparenz, rechtliche Absicherung) ohne externe Unterstützung nicht erfüllbar
- Halbfertiger Launch wäre schlimmer als kein Launch

StimmBild ist nicht aufgegeben — nur entkoppelt vom Berliner Wahltermin. Wiederaufnahme sinnvoll wenn: Uni-Kooperation steht, externe Redakteure verfügbar, mehr Entwicklungskapazität.

### QuizAway — Neubau auf Xalento-Stack statt schrittweise Migration

*Architekturentscheidung April 2026*

Der ursprünglich geplante 4-Schritt-Migrationspfad (DOK-3 B.6 alt) wird ersetzt. Der Choir Trainer hat bewiesen, dass React + TypeScript + Vite + Dexie.js + PWA eine vollständig stabile, offline-fähige App ohne Serverabhängigkeiten im Betrieb ergibt. QuizAway wird auf demselben Stack neu gebaut — als weiterer Player-Typ auf der gemeinsamen Xalento-Architektur.

**Konsequenz für die Stabilität:**

| Modus | Heute | Nach Neubau |
|---|---|---|
| Sofa / Route / Live | Serverabhängig (Render) | 100 % lokal, offline-fähig |
| Duell | Render + OpenRelay + HTTP-Polling | Always-On WebSocket + eigener coturn |
| Stabilitätsprofil | Mehrere Single Points of Failure | Choir-Trainer-Niveau |

**Wann:** Nach LA-8 (Choir Trainer vollständig stabil und abgenommen) — dann ist der Stack erprobt und QuizAway kann als LA-X (noch nicht nummeriert) eingeplant werden.

### Fachentscheidung: Informatik statt Biologie

*Entscheidung April 2026*

Das erste Schulfach-Deck wird Informatik (nicht Biologie). Gründe:

- **Kompetenz**: Inhaltskuration erfordert Urteilsvermögen — in Informatik vorhanden, in Biologie nicht
- **Technischer Vorteil**: Informatik erlaubt später einzigartige Player-Typen: Code live ausführen,
  Algorithmen animieren, Debugging als Lernform — das kann kein anderes Fach so
- **Lehrplan**: RLP Informatik Sek I klar in 4 Bereiche gegliedert (Algorithmen & Programmierung,
  Daten & Codierung, Informatiksysteme, Informatik Mensch & Gesellschaft) — ideal für Lernpfade
- **Material**: Ausreichend vorhanden. Lehrplan + OER (CS Unplugged, Open Roberta, Code.org) +
  Python/JS-Ökosystem. Engpass ist Kuration, nicht Materialmangel.

**Startmodul (Pareto):** "Algorithmen verstehen" — Sortierschritte visualisieren + Sortier-Player
(LA-11). Sofort demonstrierbar, visuell überzeugend, Lehrplan-konform.

**Hinweis:** Weniger klassische Einzelaufgaben als in Mathe/Bio — mehr Projekte und Problemlösen.
Didaktische Aufbereitung liegt stärker beim Entwickler. Das ist Chance und Aufwand zugleich.

### Neue Prioritätsreihenfolge

1. Xalento Fundament (LA-1–LA-3) — läuft
2. Chorübung (LA-6–LA-8 + LA-18–LA-21) — erster echter Anwendungsfall
3. InforLearn RLP (LA-9–LA-13 + LA-15) — erste öffentliche Priorität, erster Schulmarkt-Auftritt
4. Kooperation Universität Koblenz (Informatik-Didaktik + Institut für Pädagogik) — nach LA-15, mit laufender App und echten Nutzungsdaten
5. StimmBild — Wiederaufnahme mit akademischer Rückendeckung, ohne Wahltermin-Druck

### Uni Koblenz — Kooperationsidee (mittelfristig)

Zieltermin: nach Fertigstellung LA-13 + LA-15, voraussichtlich 2027.

Was bis dahin vorzubereiten ist:
- Laufende InforLearn-App mit echten Schülerinhalten, lehrplankonform RLP Informatik Klasse 7–8
- Klassen-Dashboard (LA-15) mit Inhalts-Heatmap — das ist der Differenziator gegenüber Quizlet & Co.
- FSRS-Nutzungsdaten aus SingOn-Chor als erster Beleg für Lernwirksamkeit

Ansprechpartner: Fachbereich Informatik (Professur Informatik und ihre Didaktik) + Institut für Pädagogik (Prof. Dr. Pätzold, Prof. Dr. Hoffmann).
