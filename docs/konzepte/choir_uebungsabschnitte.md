# Choir Trainer — Übungsabschnitte (Konzept v1)

*Stand: April 2026 · Status: Konzept, noch nicht implementiert*

**Arbeitspakete:** LA-18 · LA-18b · LA-19 · LA-19b · LA-20 · LA-21
→ Details: `docs/projektplanung.md`

| Paket | Inhalt | Aufwand |
|---|---|---|
| LA-18 | Toggle-Panel + Dexie-Schema (V1) | ~2 Tage |
| LA-18b | Drag + Snap-Points (V2) | ~2 Tage |
| LA-19 | Taktnummer-Eingabe + taktgenaue Blöcke (V1) | ~2–3 Tage |
| LA-19b | Long-Press + note-präzise Streifen (V2) | ~3 Tage |
| LA-20 | Section-Loop + Playback | ~2–3 Tage |
| LA-21 | FSRS-Integration + Fortschrittsmodal | ~3–4 Tage |

---

## 1. Zweck

Nutzer können ein Stück in bis zu 7 benannte Übungsabschnitte aufteilen. Jeder Abschnitt wird
separat mit FSRS bewertet. Der Gesamtfortschritt ergibt sich aus der Union-Coverage aller
Abschnitte gewichtet nach FSRS-Ø. Das schafft einen messbaren Übeanreiz: man sieht, wie weit
man mit dem Stück wirklich ist.

---

## 2. Datenmodell (Dexie)

```typescript
interface PracticeSection {
  id:          string          // UUID
  pieceId:     string          // Content-ID
  voiceId:     string          // partId der Übestimme
  userId:      string          // lokaler Nutzer
  name:        string          // "Abschnitt 1", "Abschnitt 2", ...
  color:       string          // Xalento-Palette, automatisch vergeben
  startTstamp: number          // timemap-Timestamp (ms) Startnote
  endTstamp:   number          // timemap-Timestamp (ms) Endnote (inkl. Dauer)
  startNoteId: string          // Verovio Note-ID Startnote
  endNoteId:   string          // Verovio Note-ID Endnote
  fsrs:        FSRSCard        // FSRS-Zustand
  practicedAt: number | null   // letzter Übezeitpunkt (Unix ms)
  practicedCount: number       // Anzahl abgeschlossener Loops
}

interface PieceSectionMeta {
  pieceId:   string
  voiceId:   string
  userId:    string
  loopPause: number            // Pause zw. Loops in Sekunden (Default: 2, Range: 0–5)
}
```

**Defaultabschnitt:** Das gesamte Stück gilt als implizit vorausgewählter Abschnitt (kein
Dexie-Eintrag nötig). Sobald ein echter Abschnitt definiert wird, ist dieser aktiv.

**Überlappungen:** erlaubt. Zwei Abschnitte dürfen dieselben Takte enthalten.

**Max. 7 Abschnitte** pro Stimme pro Stück. Bei Erreichen des Limits muss vor dem Anlegen
eines neuen Abschnitts ein vorhandener gelöscht werden.

---

## 3. Modi

### 3.1 Navigations-Modus

Standard-Modus. Score scrollt manuell (Pointer Events). Kein Playback.

Aktionen:
- Scrollen (Pan)
- Abschnitt antippen (im Score: Farbstreifen; im Sheet: Liste)
- Abschnitt definieren (Long-Press → Edit-Modus)
- Playback starten (Play-Button → wechselt zu Playback-Modus)
- Freier Playback-Start (beliebige Note lang antippen → spielt ab dort bis Stückende)

### 3.2 Playback-Modus

Score scrollt automatisch. Kein manuelles Scrollen.

Aktionen:
- Pause (bleibt an aktueller Position)
- Stop (zurück zu Navigations-Modus, Score bleibt an letzter Position)
- Loop aktiv/inaktiv togglen

### 3.3 Edit-Modus (Abschnitt definieren)

Wird aus Navigations-Modus geöffnet (Long-Press auf beliebige Note oder "+ Neuer Abschnitt"
im Sheet).

Schritte:
1. Long-Press auf Startnote → Note wird grün markiert, Status zeigt "Startpunkt gesetzt"
2. Zu Endnote navigieren (scrollen)
3. Endnote antippen → Abschnitt wird gespeichert, Edit-Modus endet
4. Abbrechen: Escape / erneuter Long-Press irgendwo / Abbrechen-Button

---

## 4. FSRS & Gesamtfortschritt

### 4.1 Automatisches Rating (Option A — Alltag)

Kein Rating-Dialog, kein Unterbrechen des Übeflusses. Das System leitet das FSRS-Rating
automatisch aus der Anzahl vollständig abgeschlossener Loops pro Session ab:

| Abgeschlossene Loops | Automatisches Rating |
|---|---|
| < 2 | Again |
| 2 – 5 | Hard |
| 6 – 9 | Good |
| ≥ 10 | Easy |

"Vollständig" = Playback hat `endTstamp` des Abschnitts erreicht ohne vorherigen Stop.
Ein vorzeitig gestoppter Loop zählt nicht.

### 4.2 Manuelles Override (Option B — FSRS-Screen)

Separater Screen (erreichbar über Hauptnavigation), der alle Abschnitte aller Stücke
mit FSRS-Status auflistet. Der Nutzer kann dort für jeden Abschnitt das automatisch
ermittelte Rating nachträglich überschreiben (Again / Hard / Good / Easy).

Dieser Screen dient gleichzeitig als Wiederholungsplaner: welche Abschnitte sind heute
fällig, welche wurden zuletzt geübt.

### 4.3 Gesamtfortschritt des Stücks

```
Coverage   = Länge aller Abschnitte (Union, keine Doppelzählung) / Gesamtlänge Stück
FSRS-Ø    = gewichteter Durchschnitt aller Abschnitts-FSRS-Scores (Gewicht = Abschnittslänge)
Gesamt    = Coverage × FSRS-Ø  → 0–100 %
```

Beispiel: 60 % des Stücks abgedeckt, FSRS-Ø = 80 % → Gesamtfortschritt = 48 %.
Anreiz: Lücken schließen + FSRS-Score halten.

---

## 5. Screen-Design

### 5.1 Normaler Betrieb — Score maximiert

```
┌─────────────────────────────────┐
│                                 │
│   ╔═══════════════════════════╗ │
│   ║  [Farbstreifen Abschn.1]  ║ │
│   ║  𝄞  ♩  ♩  ♪  ♩  ♩  ♩    ║ │
│   ║       ♩  ♩  ♩  ♩  ♩      ║ │
│   ╚═══════════════════════════╝ │
│                                 │
│   ╔═══════════════════════════╗ │
│   ║  [Farbstreifen Abschn.2]  ║ │
│   ║  𝄞  ♩  ♩  ♩  ♩  ♩  ♩    ║ │
│   ║       ♩  ♩  ♪  ♩  ♩      ║ │
│   ╚═══════════════════════════╝ │
│                                 │
├─────────────────────────────────┤  ← Persistent Bar (~60px)
│ 🟣 Abschnitt 2  🔊━━●━━━  ⏸  ↑│
└─────────────────────────────────┘
```

- **Farbstreifen**: 4px dünne Linie in Abschnittsfarbe direkt über den betreffenden Noten
- **Persistent Bar**: Abschnitts-Dot + Name · Übestimme-Lautstärke (Slider) · Play/Pause · Sheet-Handle ↑

---

### 5.2 Bottom Sheet — Snap 1 (~35%, Player-Controls)

```
┌─────────────────────────────────┐
│                                 │
│   ╔═══════════════════════════╗ │
│   ║  𝄞  ♩  ♩  ♪  ♩  ♩  ♩    ║ │  ← Score noch ~60% sichtbar
│   ╚═══════════════════════════╝ │
├─────────────────────────────────┤
│          ────────               │  ← Sheet-Handle
│                                 │
│  ← Abschnitt    ←← Stück        │  ← Navigation
│                                 │
│      ⏮  ⏸  ⏹                  │  ← Playback
│                                 │
│  Tempo:   ─────●──  100 %       │
│  Metronom:  [  AN  ]            │
│  Übestimme: ━━━━●━━━  75 %      │
│  Loop-Pause: ━━●━━━━  2 s       │
│                                 │
├─────────────────────────────────┤
│ 🟣 Abschnitt 2  🔊━━●━━━  ⏸  ↑│
└─────────────────────────────────┘
```

---

### 5.3 Bottom Sheet — Snap 2 (~70%, Section-Management)

```
┌─────────────────────────────────┐
│   ╔═══════════════════════════╗ │
│   ║  𝄞  ♩  ♩  ♩  ♩  ♩  ♩    ║ │  ← Score ~25% sichtbar
│   ╚═══════════════════════════╝ │
├─────────────────────────────────┤
│          ────────               │
│  ← Abschnitt  ←← Stück  ⏮ ⏸ ⏹│
│  Tempo: ──●──  Metronom: [AN]   │
├─────────────────────────────────┤
│  Gesamtfortschritt              │
│  ████████████░░░░░░░░  48 %     │
│  (60 % abgedeckt · FSRS-Ø 80 %)│
├─────────────────────────────────┤
│  🟣 Abschnitt 1   ████  T. 1–8 │  ← FSRS-Ampel + Taktbereich
│     zuletzt: gestern · 5×       │
│                                 │
│  🟠 Abschnitt 2 ★  ██░░  T. 9–16│  ← ★ = aktiv
│     zuletzt: heute · 2×         │
│                                 │
│  🟡 Abschnitt 3   ░░░░  T.17–24│  ← grau = noch nie geübt
│     noch nicht geübt            │
│                                 │
│  [+ Neuer Abschnitt]  [📊 FSRS] │
│                                 │
├─────────────────────────────────┤
│ 🟣 Abschnitt 2  🔊━━●━━━  ⏸  ↑│
└─────────────────────────────────┘
```

- **FSRS-Ampel**: grün (gut) · gelb (fällig) · rot (überfällig) · grau (neu)
- **Antippen eines Abschnitts**: Sheet schließt sich, Abschnitt wird aktiv
- **Long-Press auf Abschnitt**: Löschen / (kein Umbenennen — Namen sind automatisch)

---

### 5.4 Edit-Modus — Abschnitt definieren

```
┌─────────────────────────────────┐
│  ✂ ABSCHNITT DEFINIEREN    [✕] │  ← Status-Banner
│  Startpunkt antippen...         │
├─────────────────────────────────┤
│                                 │
│   ╔═══════════════════════════╗ │
│   ║  𝄞  ♩  ♩  ♪  ♩  ♩  ♩    ║ │
│   ║       ♩  ♩  ♩  ♩  ♩      ║ │
│   ╚═══════════════════════════╝ │
│                                 │
│   ╔═══════════════════════════╗ │
│   ║  𝄞  ♩  🟢  ♩  ♩  ♩  ♩   ║ │  ← Startnote grün markiert
│   ║       ♩  ♩  ♩  ♩  ♩      ║ │
│   ╚═══════════════════════════╝ │
│                                 │
│  Startpunkt gesetzt (T.9, Z.1)  │  ← Status nach Long-Press
│  Endpunkt antippen...           │
│                                 │
└─────────────────────────────────┘
```

Nach Antippen der Endnote:
```
│  ✓ Abschnitt 3 gespeichert (T.9–16) │
```
→ Edit-Modus endet, Score zeigt neuen Farbstreifen.

---

### 5.5 FSRS-Modal (aus Snap 2 via 📊-Button)

```
┌─────────────────────────────────┐
│  📊 Fortschritt             [✕] │
│  Byrd — Ave verum corpus        │
├─────────────────────────────────┤
│  Gesamtfortschritt              │
│  ████████████░░░░░░░░  48 %     │
│  60 % abgedeckt · FSRS-Ø 80 %  │
├─────────────────────────────────┤
│  🟣 Abschnitt 1   T. 1–8        │
│  FSRS: ████ Gut · 5× · gestern  │
│  [Again] [Hard] [Good] [Easy]   │
│                                 │
│  🟠 Abschnitt 2   T. 9–16       │
│  FSRS: ██░░ Fällig · 2× · heute │
│  [Again] [Hard] [Good] [Easy]   │
│                                 │
│  🟡 Abschnitt 3   T. 17–24      │
│  FSRS: ░░░░ Neu · noch nie      │
│  [Again] [Hard] [Good] [Easy]   │
└─────────────────────────────────┘
```

- Öffnet sich als Modal über dem aktuellen Screen
- Zeigt alle Abschnitte des aktuellen Stücks + Gesamtfortschritt
- Pro Abschnitt: FSRS-Balken, Bewertungstext, Loop-Zähler, letztes Übedatum
- Override-Buttons: Antippen überschreibt das automatisch ermittelte Rating sofort

---

## 6. Interaktionsflüsse

### Abschnitt üben (Kernflow, ≤ 3 Taps)

```
1. Score öffnen                     → Navigations-Modus
2. Bottom Sheet halb aufziehen      → Snap 1 oder Snap 2
3. Abschnitt antippen               → aktiv, Sheet schließt sich
4. Play antippen                    → Playback-Modus, Loop läuft
```

### Neuen Abschnitt definieren

```
1. Snap 2 aufziehen
2. "+ Neuer Abschnitt" antippen     → Edit-Modus öffnet sich
3. Zu Startnote scrollen
4. Long-Press auf Startnote         → grün markiert
5. Zu Endnote scrollen
6. Endnote antippen                 → gespeichert
```

### Freier Playback (kein Abschnittskontext)

```
Long-Press auf beliebige Note       → spielt ab dort bis Stückende
                                       kein Loop, keine Sektionsbindung
```

### Nach Pause fortsetzen

```
Pause antippen                      → Score bleibt an aktueller Position
Play antippen                       → spielt ab Pause-Position weiter
```

---

## 7. Farben (Xalento-Palette, rotierend)

| Abschnitt | Farbe      | Hex     |
|-----------|------------|---------|
| 1         | Lila       | #7C3AED |
| 2         | Orange     | #EA580C |
| 3         | Gelb-Grün  | #65A30D |
| 4         | Cyan       | #0891B2 |
| 5         | Pink       | #DB2777 |
| 6         | Bernstein  | #D97706 |
| 7         | Indigo     | #4338CA |

---

## 8. Technische Notizen

- **Grenzpunkte**: `startTstamp` / `endTstamp` aus `timemap[]` — unabhängig von Rendering
- **Farbstreifen im Score**: CSS-Overlay auf SVG-Ebene, positioniert via Note-ID → Bounding-Box
- **Loop-Steuerung**: `useMediaPlayer` kennt aktive Section-Boundaries, springt bei `endTstamp`
  zurück zu `startTstamp` nach `loopPause` Sekunden
- **FSRS-Bewertung**: automatisch nach Session-Ende (Loop-Zähler → Rating-Mapping), kein Dialog
- **Dexie-Tabellen**: `practiceSections`, `pieceSectionMeta`
- **Alte SingOn-Karten** (8-Takt-Cards): werden gelöscht, keine Migration

---

## 9. Offene Punkte (für Implementierung zu klären)

- Farbstreifen-Positionierung: SVG-Bounding-Box via `getBoundingClientRect` oder Verovio-API?
- Snap-Point-Bibliothek oder eigene Implementierung des Bottom Sheets?
