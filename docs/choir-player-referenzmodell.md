# Choir Player — Korrigiertes Referenzmodell
## Deterministisches Playback: Cursor · Scroll · Highlight · Mehrstimmigkeit

> **Version:** 1.0 (korrigiert)  
> **Basis:** Ursprünglicher Vorschlag, mit Behebung aller identifizierten kritischen Bugs  
> **Prinzip:** Keine Heuristiken — alles deterministisch aus MusicXML, Verovio und Tone.js abgeleitet

---

## 0) Gesamtarchitektur

```
MusicXML
  └─ Parser
       ├─ NoteEvents (Ties aufgelöst, Tuplets skaliert, docOrder gesetzt)
       └─ TempoMap (stückweise, exakt)
            └─ Verovio Rendering
                 ├─ xml:id → SVG-IDs (1:1, verlustfrei)
                 └─ TimeMap (t in ms → x lokal)  ← Verovio liefert Millisekunden!
                      └─ Konvertierung ms → Beats via beatToSeconds⁻¹
                           └─ GlobalMap (tBeat → x monoton, systemübergreifend)
                                └─ Runtime
                                     ├─ Tone.js Lookahead-Scheduler (Audio + Highlight)
                                     ├─ RenderLoop (Cursor + Scroll, rAF)
                                     └─ Highlight Engine (event-getrieben via Tone.Draw)
```

**Nicht verhandelbare Synchronisationsprinzipien:**
- **Eine Zeitquelle** → `Tone.Transport`
- **Cursor** = Funktion von `tBeat`
- **Scroll** = Funktion von Cursor-X
- **Highlight** = event-getrieben (nicht polling)

---

## 1) Datenmodelle

### 1.1 NoteEvent (kanonisch)

```typescript
interface NoteEvent {
  id: string;           // z. B. "ev_42"
  startBeat: number;    // in Vierteln ab Stückanfang
  endBeat: number;      // exklusiv
  startSec: number;     // vorberechnete Sekunden (nach Parsing)
  endSec: number;       // vorberechnete Sekunden
  voice: number;        // Stimmennummer aus MusicXML (1-basiert)
  staff: number;        // Systemzeile (1 = oben)
  docOrder: number;     // laufender Index beim XML-Parsen
  notes: string[];      // Pitches, z. B. ["C4","E4","G4"]
  elementIds: string[]; // Verovio-SVG-IDs (inkl. Tie-Gruppen)
}
```

**Invarianten:**
- Jede klingende Einheit = genau **ein** Event
- Ties sind bereits aufgelöst (Tie-Gruppe → ein Event mit mehreren `elementIds`)
- `elementIds[0]` = Startnote = stabiler visueller Referenzpunkt

---

### 1.2 TempoMap

```typescript
interface TempoSegment {
  beat: number;  // Startbeat dieses Tempos
  bpm: number;   // Viertel pro Minute
}

// Beispiel:
const tempoMap: TempoSegment[] = [
  { beat: 0,  bpm: 120 },
  { beat: 32, bpm: 90  },
];
```

---

### 1.3 TimeMap (aus Verovio)

```typescript
interface TimeMapPoint {
  t: number;  // Zeit in Millisekunden (Verovio-Ausgabe!)
  x: number;  // X-Position in SVG-Einheiten (lokal pro System)
}
```

> ⚠️ **Kritisch:** Verovio's `renderToTimemap()` liefert `t` in **Millisekunden**, nicht in Beats.  
> Die Konvertierung zu Beats erfolgt über `secondsToBeat(t / 1000)` (siehe Abschnitt 4).

---

### 1.4 GlobalMap (monoton, beatbasiert)

```typescript
interface GlobalMapPoint {
  t: number;  // in Beats (nach Konvertierung)
  x: number;  // X-Position global (monoton steigend, systemübergreifend)
}
```

---

## 2) MusicXML-Parsing

### 2.1 Parser-Zustand

```javascript
const state = {
  divisions: 480,   // ticks pro Viertel (aus <divisions>)
  tempoMap: [],     // wird beim Parsen befüllt
  voicePositions: {}, // Beat-Position pro Stimme
  docOrder: 0,      // laufender Zähler
};
```

### 2.2 Notendauer in Beats

```javascript
function durationBeats(xmlDuration, divisions) {
  return xmlDuration / divisions;
}
```

### 2.3 Tuplets (exakt, deterministisch)

MusicXML-Quelle:
```xml
<time-modification>
  <actual-notes>3</actual-notes>
  <normal-notes>2</normal-notes>
</time-modification>
```

```javascript
function applyTuplet(durationBeats, tuplet) {
  // Tripole: 3 Noten auf 2 Schläge → Faktor 2/3
  return durationBeats * (tuplet.normal / tuplet.actual);
}
```

→ vollständig deterministisch, kein Sonderfall im Runtime-Code.

### 2.4 Mehrstimmigkeit (parallele Zeitachsen)

```javascript
// Zeitfortschritt pro Stimme separat verwalten
const voicePositions = {};

function advanceVoice(voice, durationBeats) {
  voicePositions[voice] = (voicePositions[voice] ?? 0) + durationBeats;
}

function getVoiceBeat(voice) {
  return voicePositions[voice] ?? 0;
}
```

---

## 3) Beat ↔ Sekunden (KORRIGIERT)

### 3.1 Beat → Sekunden

```javascript
// BUG-FIX: Grenzfall beat === next.beat muss ins NÄCHSTE Segment
// Original verwendete <= was zur falschen Segmentzuweisung führte
function beatToSeconds(beat) {
  let seconds = 0;

  for (let i = 0; i < tempoMap.length; i++) {
    const cur  = tempoMap[i];
    const next = tempoMap[i + 1];

    if (!next || beat < next.beat) {
      // beat liegt in diesem Segment
      seconds += (beat - cur.beat) * (60 / cur.bpm);
      return seconds;
    }

    // Segment vollständig aufaddieren
    seconds += (next.beat - cur.beat) * (60 / cur.bpm);
  }

  return seconds; // sollte nicht erreichbar sein bei korrekter tempoMap
}
```

**Was korrigiert wurde:**  
Das Original prüfte `beat <= endBeat` — bei `beat === next.beat` landete die Note
fälschlicherweise im aktuellen Segment statt im nächsten. Korrekt ist `beat < next.beat`.

### 3.2 Sekunden → Beat (für RenderLoop)

```javascript
function secondsToBeat(sec) {
  let time = 0;

  for (let i = 0; i < tempoMap.length; i++) {
    const cur = tempoMap[i];
    const next = tempoMap[i + 1];

    const segDuration = next
      ? (next.beat - cur.beat) * (60 / cur.bpm)
      : Infinity;

    if (sec < time + segDuration) {
      return cur.beat + (sec - time) * (cur.bpm / 60);
    }

    time += segDuration;
  }

  // Fallback: hinter dem letzten Segment extrapolieren
  const last = tempoMap[tempoMap.length - 1];
  return last.beat + (sec - time) * (last.bpm / 60);
}
```

### 3.3 Events vorberechnen (nach Parsing, einmalig)

```javascript
for (const ev of events) {
  ev.startSec = beatToSeconds(ev.startBeat);
  ev.endSec   = beatToSeconds(ev.endBeat);
}
```

---

## 4) Verovio-Integration

### 4.1 xml:id vergeben (vor dem Rendering)

```javascript
let counter = 0;

function assignIds(xmlDoc) {
  xmlDoc.querySelectorAll("note").forEach(note => {
    if (!note.hasAttribute("xml:id")) {
      note.setAttribute("xml:id", "n_" + String(counter++).padStart(6, "0"));
    }
  });
}
// → danach nur noch mit diesem modifizierten XML arbeiten
```

### 4.2 Verovio-Optionen (IDs müssen erhalten bleiben)

```javascript
vrvToolkit.setOptions({
  svgHtml5: true,
  // KEINE Option, die xml:id-Attribute entfernt oder transformiert
});
const svg = vrvToolkit.renderToSVG(1);
```

### 4.3 TimeMap abrufen und in Beats konvertieren (KRITISCH KORRIGIERT)

```javascript
// Verovio liefert t in Millisekunden — NICHT in Beats!
const rawTimeMap = vrvToolkit.renderToTimemap(); 
// rawTimeMap: Array<{ t: number /*ms*/, x: number }>

const timeMapInBeats = rawTimeMap.map(p => ({
  t: secondsToBeat(p.t / 1000),  // ms → sec → beats
  x: p.x
}));
```

**Was korrigiert wurde:**  
Das Original-Modell ließ diese Konvertierung unerwähnt / implizit. Ohne sie ist
die GlobalMap in der falschen Zeiteinheit und Cursor + Scheduler laufen auseinander.

### 4.4 Mapping validieren

```javascript
function validateMapping(events) {
  for (const ev of events) {
    for (const id of ev.elementIds) {
      if (!document.getElementById(id)) {
        throw new Error(`SVG-Element fehlt für ID: ${id}`);
      }
    }
  }
}
```

---

## 5) GlobalMap aufbauen (systemübergreifend, monoton)

### 5.1 Systeme segmentieren

```javascript
function segment(timeMap) {
  const systems = [];
  let current = [timeMap[0]];

  for (let i = 1; i < timeMap.length; i++) {
    if (timeMap[i].x < timeMap[i - 1].x) {
      // X-Rücksprung = neues System
      systems.push(current);
      current = [];
    }
    current.push(timeMap[i]);
  }
  systems.push(current);
  return systems;
}
```

### 5.2 GlobalMap bauen

```javascript
function buildGlobalMap(systems) {
  let offset = 0;
  const globalMap = [];

  for (const sys of systems) {
    const base = sys[0].x;

    for (const p of sys) {
      globalMap.push({
        t: p.t,
        x: p.x - base + offset
      });
    }

    offset += sys[sys.length - 1].x - base;
  }

  return globalMap; // monoton steigendes x für alle t
}
```

---

## 6) Interpolation (kontinuierliche X-Position)

```javascript
// BUG-FIX: Edge-Case am Stücksende — map[i+1] könnte undefined sein
function getX(map, t) {
  if (map.length === 0) return 0;

  // Vor dem ersten Punkt
  if (t <= map[0].t) return map[0].x;

  // Nach dem letzten Punkt → extrapolieren oder letzten Wert halten
  if (t >= map[map.length - 1].t) return map[map.length - 1].x;

  // Interpolieren
  let i = 0;
  while (i < map.length - 1 && map[i + 1].t <= t) i++;

  const p1 = map[i];
  const p2 = map[i + 1];
  const r  = (t - p1.t) / (p2.t - p1.t);

  return p1.x + r * (p2.x - p1.x);
}
```

**Was korrigiert wurde:**  
Das Original griff auf `map[i+1]` zu ohne zu prüfen ob `i+1` existiert → NaN am Stücksende.

---

## 7) LeaderEvent (deterministisch)

### 7.1 Aktive Events zum Zeitpunkt t

```javascript
function getActiveEvents(t) {
  return events.filter(ev => ev.startBeat <= t && t < ev.endBeat);
}
```

### 7.2 Führendes Event (totale Ordnung, keine Heuristik)

Priorität: **(1) früheste Startzeit → (2) niedrigste Voice → (3) oberstes Staff → (4) XML-Reihenfolge**

```javascript
function getLeaderEvent(active) {
  if (active.length === 0) return null;

  return active.reduce((best, cur) => {
    if (!best) return cur;

    if (cur.startBeat < best.startBeat) return cur;
    if (cur.startBeat > best.startBeat) return best;

    if (cur.voice < best.voice) return cur;
    if (cur.voice > best.voice) return best;

    if (cur.staff < best.staff) return cur;
    if (cur.staff > best.staff) return best;

    return cur.docOrder < best.docOrder ? cur : best;
  }, null);
}
```

---

## 8) Lookahead-Scheduler (Tone.js)

### 8.1 Parameter

```javascript
const LOOKAHEAD = 0.1;   // Sekunden vorausplanen
const INTERVAL  = 0.025; // Scheduler-Interval in Sekunden
let schedulerIndex = 0;
```

### 8.2 Scheduler

```javascript
function scheduler() {
  const now     = Tone.now();
  const horizon = now + LOOKAHEAD;

  while (schedulerIndex < events.length) {
    const ev = events[schedulerIndex];

    if (ev.startSec >= horizon) break;

    scheduleEvent(ev);
    schedulerIndex++;
  }
}

setInterval(scheduler, INTERVAL * 1000);
```

### 8.3 Event schedulen (KRITISCH KORRIGIERT)

```javascript
function scheduleEvent(ev) {
  // BUG-FIX: Dauer muss als Differenz der Absolut-Sekunden berechnet werden,
  // NICHT als beatToSeconds(endBeat - startBeat), da das bei Tempoänderungen
  // den falschen Tempowert verwendet.
  const durationSec = ev.endSec - ev.startSec;  // korrekt: absolute Differenz

  synth.triggerAttackRelease(
    ev.notes,
    durationSec,
    ev.startSec   // absolute Zeit in Sekunden
  );

  Tone.Draw.schedule(() => {
    highlight(ev.elementIds);
  }, ev.startSec);
}
```

**Was korrigiert wurde:**  
Das Original berechnete `beatToSeconds(ev.endBeat - ev.startBeat)` — das ist die
Sekunden-Entsprechung der Beat-*Differenz*, gerechnet **ab Beat 0**, also mit dem
Tempo des ersten Segments. Bei Tempoänderungen innerhalb oder zwischen Noten
ergibt das eine falsche Länge. Korrekt ist `ev.endSec - ev.startSec`.

---

## 9) Cursor-Position

```javascript
function getCursorPosition(tBeat) {
  const x = getX(globalMap, tBeat);

  const active = getActiveEvents(tBeat);
  const leader = getLeaderEvent(active);

  if (!leader) return { x, y: 0 };

  const bbox = vrvToolkit.getElementBoundingBox(leader.elementIds[0]);

  return { x, y: bbox.y };
}
```

**Hinweis Y-Position:** `vrvToolkit.getElementBoundingBox()` liefert Koordinaten im
SVG-Koordinatensystem. Falls das SVG in einem scrollbaren Container liegt, muss `bbox.y`
ggf. um den Container-Offset korrigiert werden (abhängig von der Einbettung).

---

## 10) Sanftes Scrollen

### 10.1 Zielposition

```javascript
function scrollTarget(cursorX) {
  return cursorX - viewportWidth * 0.3; // Cursor bei 30% von links
}
```

### 10.2 Exponentielles Glätten (einfach)

```javascript
let scroll = 0;

function updateScroll(target) {
  const alpha = 0.08; // Glättungsfaktor (0 = kein Folgen, 1 = sofort)
  scroll += (target - scroll) * alpha;
  container.scrollLeft = scroll;
}
```

### 10.3 Physikalisches Federsystem (empfohlen bei langen Sprüngen)

```javascript
let scroll = 0;
let velocity = 0;

function updateScrollPhysics(target) {
  const k = 0.1; // Federkonstante
  const d = 0.8; // Dämpfung

  const force = (target - scroll) * k;
  velocity = velocity * d + force;
  scroll += velocity;

  container.scrollLeft = scroll;
}
```

---

## 11) RenderLoop (zentral)

```javascript
function renderLoop() {
  // Einzige Zeitquelle: Tone.Transport
  const tBeat = secondsToBeat(Tone.Transport.seconds);

  const pos = getCursorPosition(tBeat);

  cursor.style.transform = `translate(${pos.x}px, ${pos.y}px)`;

  updateScroll(scrollTarget(pos.x));

  requestAnimationFrame(renderLoop);
}
```

---

## 12) Highlighting (event-getrieben, tie-korrekt)

```javascript
function highlight(ids) {
  // Alle aktiven Highlights entfernen
  document.querySelectorAll(".active")
    .forEach(el => el.classList.remove("active"));

  // Neue IDs (inkl. aller Tie-Gruppen-Elemente) aktivieren
  ids.forEach(id => {
    document.getElementById(id)?.classList.add("active");
  });
}
```

---

## 13) Validierung & Stabilität

```javascript
// Prüft: Zu jedem TimeMap-Zeitpunkt existiert ein LeaderEvent
function validateMapping() {
  for (const p of globalMap) {
    const leader = getLeaderEvent(getActiveEvents(p.t));
    if (!leader) console.warn(`Kein Leader für t=${p.t} beats`);
  }
}

// Prüft: Events sind chronologisch sortiert
function validateEventsOrder() {
  for (let i = 1; i < events.length; i++) {
    if (events[i].startBeat < events[i - 1].startBeat) {
      throw new Error(`Zeitachse inkonsistent bei Event ${events[i].id}`);
    }
  }
}

// Prüft: Kein Leader-Widerspruch
function validateLeaderUniqueness(t) {
  const active = getActiveEvents(t);
  const leader = getLeaderEvent(active);
  if (!leader && active.length > 0) {
    throw new Error(`Kein Leader trotz ${active.length} aktiver Events bei t=${t}`);
  }
}
```

---

## 14) Initialisierungs-Reihenfolge (vollständig)

```javascript
async function init(musicXmlString) {
  // 1. IDs vergeben (vor Rendering!)
  const xmlDoc = parseXML(musicXmlString);
  assignIds(xmlDoc);
  const xmlWithIds = serializeXML(xmlDoc);

  // 2. Events parsen (inkl. Ties auflösen, Tuplets skalieren)
  const { events, tempoMap } = parseMusicXML(xmlDoc);

  // 3. Sekunden vorberechnen
  for (const ev of events) {
    ev.startSec = beatToSeconds(ev.startBeat);
    ev.endSec   = beatToSeconds(ev.endBeat);
  }

  // 4. Verovio rendern
  vrvToolkit.loadData(xmlWithIds);
  const svg = vrvToolkit.renderToSVG(1);
  container.innerHTML = svg;

  // 5. TimeMap abrufen und von ms → Beats konvertieren
  const rawTimeMap = vrvToolkit.renderToTimemap();
  const timeMapBeats = rawTimeMap.map(p => ({
    t: secondsToBeat(p.t / 1000),  // ms → sec → beats
    x: p.x
  }));

  // 6. GlobalMap bauen
  const systems = segment(timeMapBeats);
  globalMap = buildGlobalMap(systems);

  // 7. Validieren
  validateMapping();
  validateEventsOrder();
  validateMapping(events);  // SVG-IDs prüfen

  // 8. Tone.js starten
  await Tone.start();
  Tone.Transport.start();
  setInterval(scheduler, INTERVAL * 1000);
  requestAnimationFrame(renderLoop);
}
```

---

## 15) Ergebnis-Eigenschaften

| Eigenschaft | Garantiert |
|---|---|
| Kontinuierlicher Cursor ohne Sprünge | ✅ (Interpolation in GlobalMap) |
| Korrekte Notenlängen bei Tempoänderungen | ✅ (Bug-Fix scheduleEvent) |
| Korrekte Segmentgrenzen in beatToSeconds | ✅ (Bug-Fix `<` statt `<=`) |
| Kein NaN am Stücksende | ✅ (Bug-Fix getX) |
| Korrekte TimeMap-Zeiteinheit | ✅ (ms → Beats Konvertierung) |
| Driftfreie Audio/Visual-Synchronität | ✅ (eine Zeitquelle: Tone.Transport) |
| Korrektes Highlighting inkl. Haltebögen | ✅ (Tie-Gruppen in elementIds) |
| Deterministischer Cursor bei Mehrstimmigkeit | ✅ (LeaderEvent-Ordnung) |
| Korrekte Systemumbrüche | ✅ (GlobalMap-Segmentierung) |

---

## 16) Behobene Bugs (Zusammenfassung)

| # | Bug | Original | Korrektur |
|---|---|---|---|
| 1 | `beatToSeconds`: falsche Segmentzuweisung an Grenzen | `beat <= endBeat` | `beat < next.beat` |
| 2 | `scheduleEvent`: falsche Notenlänge bei Tempoänderungen | `beatToSeconds(endBeat - startBeat)` | `ev.endSec - ev.startSec` |
| 3 | `getX`: NaN am Stücksende | kein Edge-Case | Guard für `t >= letzter Punkt` |
| 4 | TimeMap-Einheit unbehandelt | Verovio-ms implizit als Beats behandelt | explizit `p.t / 1000` → `secondsToBeat()` |

---

## 17) Erweiterbarkeit

Direkt anschließbar ohne Architekturänderung:

- **Rubato / Tempokurven:** TempoMap wird auf stückweise-lineare Interpolation erweitert
- **Looping:** `schedulerIndex` zurücksetzen + `Tone.Transport.seconds` offset verwalten
- **Scrubbing:** `Tone.Transport.seconds` direkt setzen, `schedulerIndex` neu suchen (Binary Search auf `startSec`)
- **Mehrere Seiten/Systeme:** GlobalMap bleibt unverändert, da Systemumbrüche bereits berücksichtigt

---

*Dieses Modell ist vollständig deterministisch, driftfrei und ohne Heuristiken.*  
*Alle vier kritischen Bugs des Originalvorschlags sind behoben.*
