# QuizAway → MixMi!/7a — Transfer-Konzept v1.1 (Archiv-finale Fassung)

**Datei:** `quizaway-7a-container-transfer-konzept-v1.1-2026-06-21.md`
**Pfad:** `LernApp docs/konzepte/`
**Status:** **Freigegeben / archivreif** (alle Reviewer: Freigabereife bestätigt). KEIN Auftrag, kein Commit-Trigger.
**Datum:** 2026-06-21

---

## Provenienz & TLDR

v1.0 + **finale Review-Runde** (einhellige Freigabe). Zwei letzte Nachschärfungen (Doc 13), beide übernommen:

1. **Projektion entschärft (Claim-Disziplin):** „klarer **Wiederverwendungs-Kandidat**" statt „potenziell sehr großer Hebel" — gezeigt ist **UI-Flexibilität**, *nicht* ein Aufwands-Rang. Ob Projektion auch einer der größten Aufwandshebel ist, zeigt die Implementierung (§4).
2. **NvN-Scoring entschieden (von „offen" zu Default):** `TeamScore = Sum(PlayerScores)` — fester Default; Mittelwert/Median **nur**, falls je asymmetrische Teamgrößen unterstützt werden sollen (§12).

**Kernbefund (durabel, von allen Reviews als stärkste Aussage bestätigt):**
> **QuizAway nutzt die gemeinsame Infrastruktur, ist aber *kein* zweiter Konsument der Card-Chain-Topologie. ADR-A12 bleibt unangetastet** — der Chain-Extraktions-Trigger ist durch QuizAway vorläufig nicht ausgelöst (echter Kandidat: Sortierspiel-Player).

**Sparthese (stützend, hedged):** Projektions-Reuse + Meta-Steuerung + generische Tele (gekapselter Coordinator) ⇒ vermutlich erheblich gesparte Programmierarbeit — Rangfolge der Hebel an der 7a-Implementierung zu verifizieren.

---

## 1. Spielablauf QuizAway (Kurzfassung)

Im Kern total einfach: **eine von vier Antworten wählen** entscheidet über die Punkte — **richtig/falsch** plus **Zeitabzug** für die lokal gemessene Antwortdauer. Die Timeline hält **nur die bisherigen Fragen und Antworten** fest; daraus **jederzeit ein Zwischenstand**, am Ende der Endstand.

5 Runden/Spiel, 3 Fragen/Runde. Frage = 1 Fragekarte + **4 Antwortkarten (A–D), genau eine korrekt**. **Ein Klick** = Antwort, kein Bestätigen, Zeit beim Klick. Pro-Frage-Fenster 14 s (Timeout=0). Modi: Sofa, Virtuelle Route, Live, **Duell (1v1, → NvN)**.

---

## 2. Das Spielprinzip: genau eine von vier — und seine Scope-Grenze

> **Fragekarte + 4 Antwortkarten. Genau eine ist korrekt. Ein Klick.**

In der konzipierten QuizAway nutzt **jede** Frage dieses Schema; alle „Fragetypen" (Zahl, Fakt, Vergleich, Reihenfolge) sind reiner **Inhalt** und laufen durch `chosenIndex === correctIndex`.

**Bewusste Scope-Grenze:** Andere Antwort-Modalitäten — *Zahl eingeben*, *Koordinate setzen*, *Permutation erzeugen* — sind **andere Player-Typen**, nicht Varianten in QuizAways `evaluate`. Die Plattform-Generalisierung lebt in der **Infrastruktur** und in **Geschwister-Player-Typen** (Sortierspiel-Player), nicht in einem generischen Antwort-Modell, das man QuizAway aufzwingt.
> **Kipp-Kriterium:** realer Konsument mit QuizAway-Flow + anderer Antwortform → dann Schema revisiten, nicht spekulativ vorher.

---

## 3. Zustandsmodell — Zwei Reihen als *optionale* Hypothese

QuizAways aktiver Zustand ist schlicht:

```
{ currentQuestion, history: AnsweredEntry[], metaState }
```

**Das ist die belastbare Basis — ohne jedes Reihen-Konzept.** Die Analogie zu MixMis Zwei-Reihen-Architektur (Durchführungs-Reihe + Steuerungs-Reihe) ist **eine optionale Reuse-Hypothese**, **nicht** Voraussetzung der Sparthese:

- **MixMi:** Durchführungs-Reihe = aktiver Zustand über die sortierte Kette; Steuerungs-Reihe = Meta-Reihe.
- **QuizAway:** „Durchführungs-Reihe" wäre nur ein Append-Log mit `currentQuestion` am Kopf; ob QuizAway diese Abstraktion **überhaupt braucht**, entscheidet erst die Implementierung — `{ currentQuestion, history[], metaState }` genügt fachlich.

> **Kopf-Prinzip (fachliche Klammer):** Liegt eine „Durchführungs-Reihe" vor, ist ihr Kopf immer das **aktuell zu beantwortende** Element — analog zu MixMis Kopf-Container, wo das **Riddle** die zu platzierende Karte ist. Mit `evaluate` friert der Zustand ein, der Eintrag wird zum unveränderlichen `AnsweredEntry` und rückt in den Verlauf; die nächste Frage kommt an den Kopf. *Fokus/Interaktivität* an der Kopf-Projektion, Verlauf schreibgeschützt.

> **Belastbarer Reuse = Projektion (§4) + Meta-Steuerung + generische Tele (§7).** Der Zwei-Reihen-Reuse ist Zugabe, kein Fundament.

> **Kipp-Kriterium (kein Chain):** Kette nur, wenn der Spieler eine Ordnung **selbst baut** (wächst, bewertet). In QuizAway nie → Append-Log, kein `leftNeighborId`.

---

## 4. Container / Payload / Projektion — klarer Wiederverwendungs-Kandidat

Das 7a-Modell trennt **Container** (logische Truth) / **Payload** (Frage, Optionen) / **Projektion** (View an Ort/Geometrie/Größe). Weil die Projektion entkoppelt ist, wird **dieselbe Payload** ohne Zusatzlogik zu **Liste / Grid / Streifen** und passt sich **Mobil/Desktop** an (A34 → 2×2; Desktop → Streifen).

**Ehrliche Einordnung (Review, finalisiert):** Gezeigt ist hier **hohe UI-Flexibilität**. **Nicht** gezeigt ist, dass Projektion *erheblich Entwicklungsaufwand spart* — der reale Aufwand einer Quiz-App kann ebenso in **Fragenkatalog, MatchCoordinator, Persistenz, Multiplayer, Authoring-Tools** liegen. Daher die belastbare Position:
> Projektion ist ein **klarer Wiederverwendungs-Kandidat**. **Ob** sie zugleich **einer der größten Aufwandshebel** ist, muss die Implementierung zeigen.

---

## 5. Zug-Modell: parallele Zugfähigkeit, lokale Zeit, Start-Sync nur im Duell

- **Turn-Rotation entfällt** (globaler Phasen-Tick). Skalierung 1v1→NvN trivial.
- **Parallele Zugfähigkeit:** Alle Spieler erhalten dieselbe Frage/dasselbe Paket und antworten **im eigenen Zeitfenster** (logische Gleichzeitigkeit, nicht physikalische Simultanität). Auslieferung darf (locker) minimal versetzt sein; nur das **Duell** strebt nahezu gleichzeitiges Aufdecken an.
- **Zeitmessung rein lokal:** lokal aufdecken → lokal Timer → lokal messen.
  > **Präzise:** Lokale Messung löst Fairness **innerhalb** eines Aufdeckfensters — sie ersetzt **keine Startsynchronisation**. Flow-Modi: egal (Aggregat am Ende). Duell: Start nah beieinander → nahezu gleichzeitige Auslieferung (§7.4).
- **Duell-Entscheidung (Variante A, einhellig):** verglichen wird die lokal gemessene **Zeitdifferenz Aufdecken→Klick**, nicht die Wall-Clock; kein Uhrenabgleich.

---

## 6. Datenmodell — eine Frageform, Scoring im Deck

```typescript
interface Question {
  questionId: string; prompt: string;
  options: [string, string, string, string];  // IMMER 4
  correctIndex: 0 | 1 | 2 | 3;                 // GENAU eine richtig
  scoreParams: ScoreParams;                    // pro Frage/Deck — NICHT global
  meta?: { city: string; lat: number; lon: number };
}
interface PlayerAnswer { chosenIndex: 0 | 1 | 2 | 3; elapsedMs: number; } // LOKAL
interface AnsweredEntry { entryId:string; questionId:string; answer:PlayerAnswer; resolution:{correct:boolean;score:number}; }

interface ScoreParams { budget:number; ratePerSec:number; graceSec:number; }
function timeScore(ms:number,p:ScoreParams){ const t=Math.max(0,ms/1000-p.graceSec); return Math.max(0,Math.round(p.budget-p.ratePerSec*t)); }
function evaluate(q:Question,a:PlayerAnswer){ const correct=a.chosenIndex===q.correctIndex; return {correct,score:correct?timeScore(a.elapsedMs,q.scoreParams):0}; }
```

`ScoreParams` liegen **im Deck/in der Frage** (schwere Fragen/Bonus = höheres `budget` über dieselbe `evaluate`).

---

## 7. Mehrspieler — generische Tele + gekapselter Match-Coordinator

### 7.1 Schichtung

| Schicht | Verantwortung | Wiederverwendbarkeit |
|---|---|---|
| **`@xalento/p2p-tele`** | **reiner Transport**: Peers, Byte-/Nachrichten-Transport. Kennt **kein** Packet/Round/Reveal/Barrier. | generisch, app-übergreifend (auch MixMi-Sessions, Sortierspiel-Player) |
| **QuizAwayMatchCoordinator** | Reveal, Pakete, **zeitbeschränkte Barriere**, Timeout, Aggregation, Duell-Konfig | QuizAway-spezifisch |

> **Ehrliche Einordnung:** Der Coordinator ist **nicht „dünn"** — hier konzentriert sich der **eigentliche Mehrspieler-Aufwand**. Der Gewinn ist nicht seine Größe, sondern seine **Kapselung**: sauber getrennt von Transport (Tele) und Spielmechanik (`evaluate`), damit **austauschbar**. Domänenwissen liegt **nicht** in Tele.

### 7.2 Zweck & Paketierung (locker)

Sync = **Flow-Koordination**, nicht Fairness: alle Teams *einigermaßen* beim gleichen Fragenstand. **Paket = Runde** (default 1 Paket = 3 Fragen → 5 Sync-Runden/Spiel). Pro Modus konfigurierbar (im Coordinator: 3 für Sofa/Route, 1 für Duell). `PacketResult` trägt die lokalen Antworten/Zeiten.

### 7.3 Zeitbeschränkte Barriere — präzise Semantik

Maßgeblich ist **nur** das **Pro-Frage-Fenster** W (z. B. 14 s), **lokal**, ab dem lokalen Aufdecken **jeder einzelnen Frage**:

- Jede Frage löst bei `min(Antwortzeit, W)` auf; bei W ohne Antwort → **Timeout = 0**, weiter zur nächsten Frage im Paket.
- Ein Paket terminiert pro Team **immer von selbst** in ≤ `n × W` — eine „nie beantwortete" Frage **kann nicht hängen** (läuft nach eigenen 14 s ab).
- **Barriere:** nächstes Paket, sobald **alle** `PacketResult`s vorliegen **oder** nach `n × W + Netz-Toleranz G`; ein bis dahin nicht meldendes Team bekommt fehlende Antworten als **falsch**.

→ Kein „2+3+14 vs. 14+14+14"-Problem: jede Frage ist **einzeln gedeckelt**; `n × W` ist die *Obergrenze* der Paketdauer, **keine gemeinsame Paket-Uhr**. Niemand wartet unbegrenzt.

### 7.4 Duell (eng) — Variante A

Einziger Modus mit enger Sync: **Paketgröße = 1**, **Reveal-Verzögerung minimiert**, damit die lokal gemessene Zeit für beide annähernd unter denselben Bedingungen startet. Verglichen werden die **`elapsedMs`** — Zeitmessung bleibt lokal.
> **Kipp-Kriterium:** echter Echtzeit-Wettlauf (Server-Uhr) ⇒ grundsätzlich andere Sync-Architektur → **eigener ADR**, nicht hier.

> **Sparthese (präzisiert):** … weil die **generische Tele** als reiner Transport **app-übergreifend** bleibt (recycelbar für MixMi-Sessions / Sortierspiel-Player) und die **gesamte fachliche Match-Logik in einem gekapselten, austauschbaren Coordinator** steckt — bei lokaler Zeit ohne Timing-Coupling.

---

## 8. Direkte Abbildung — Reuse aus MixMi/7a (gewichtet & gehedged)

| QuizAway-Element | 7a-Pendant | Passung |
|---|---|---|
| Projektion/Layout (Mobil↔Desktop) | Container/Payload/Projektion | ✅ **klarer Reuse-Kandidat** (UI-Flex gezeigt; Aufwands-Rang offen) |
| Meta-Steuerung (Stand, Kategorie, Zähler) | Steuerungs-Reihe | ✅ belastbar |
| Mehrspieler-Transport | **Tele (generisch)** | ✅ app-übergreifend |
| Mehrspieler-Match-Logik | **MatchCoordinator** | ◐ gekapselt, **nicht dünn** |
| Zustandsmodell `{currentQuestion, history[], metaState}` | (zwei Reihen) | ◐ **optionale Hypothese** |
| MC-Frage (1 von 4) | Kopf / `currentQuestion` | ✅ append statt Kette |
| Zeitmessung | rein lokal (Start-Sync nur Duell) | ✅ kein Uhrenabgleich |
| `chronoCheck`/`leftNeighborId`/`advanceTeamStrategy` | — | ➖ **nicht** konsumiert |

---

## 9. Kernbefund: Infrastruktur-Konsument, kein Chain-Konsument

Von allen Reviewern als der **eigentliche, gut abgesicherte** Befund bestätigt (stärkster Satz des Papiers):

- QuizAway konsumiert die Chain-Topologie **nicht** (jede Frage 1-von-4; Reihenfolge nur Inhalt; Mehrspieler über Tele, nicht über geteilte Kette).
- `compareCheck<TAxis>` wäre **verfrüht**. → **kein hinreichender zweiter Chain-Konsument**.

> **„Chain-Extraktions-Trigger durch QuizAway vorläufig nicht ausgelöst." ADR-A12 bleibt unangetastet.** Echter zweiter Chain-Fall = **Sortierspiel-Player** (Ordnung *erzeugen*).

---

## 10. Einpassung ins Lernkonzept

Belastbare gemeinsame Substanz: **Projektion** (Reuse-Kandidat) + **Meta-Steuerung** + **generische Tele**. Optional: Zwei-Reihen-Muster. App-spezifisch: **MatchCoordinator**. MixMi: Kette (Ordnung erzeugen). QuizAway: Append-Log (1-von-4). Sortierspiel-Player: echte Chain.

---

## 11. Anti-Rucksack v1.1 (inkl. dokumentierter Ablehnungen)

- ❌ keine `leftNeighborId`-Kette / kein `chronoCheck` / kein `compareCheck<TAxis>` für QuizAway
- ❌ kein `advanceTeamStrategy` als Turn-Rotation
- ❌ kein generisches `evaluate` in QuizAway *(Kipp: realer Konsument mit QuizAway-Flow + anderer Antwortform)*
- ❌ kein Echtzeit-Wettlauf im Duell *(Kipp: eigener ADR)*
- ❌ keine reine Soft-Barrier *(ersetzt durch zeitbeschränkte Barriere)*
- ❌ keine Domänenlogik in Tele (Packet/Reveal/Barrier im Coordinator)
- ❌ kein `ScoreParams` im globalen Kern (gehört ins Deck/Meta)
- ❌ keine voreilige „Durchführungs-Reihe"-Abstraktion in QuizAway (erst wenn API sie rechtfertigt)
- ❌ keine Behauptung einer Hebel-**Rangfolge** vor der Implementierung
- ❌ kein gerätespezifischer Layout-Code (Projektion)
- ✅ `{currentQuestion, history[], metaState}` + `Question`(Payload) + Projektionen + `evaluate`/`timeScore` (ScoreParams im Deck) + **Tele (generisch) + MatchCoordinator (gekapselt) + zeitbeschränkte Barriere**

---

## 12. Umsetzungs-Entscheidungen

1. **NvN-Team-Score — entschieden:** `TeamScore = Sum(PlayerScores)` als **Default** (einfach, konsistent; lokale Pro-Spieler-Messung bleibt sauber; im Coordinator per `reduce()`). **Mittelwert/Median nur**, falls **ausdrücklich** asymmetrische Teamgrößen unterstützt werden sollen — andernfalls keine theoretische Alternative offenhalten.
2. **Default-Paketgröße pro Modus** im Coordinator-Konfigurator (3 Sofa/Route, 1 Duell) + Netz-Toleranz `G`.
3. **Benennung** „Durchführungs-Reihe/Container" → evtl. `HistoryEntry`/Snapshot (mit der API-Validierung entscheiden).
4. **API-Validierung des Zwei-Reihen-Reuse** an der 7a-Implementierung (1. Konsument), bevor QuizAway andockt — ob gemeinsamer **Code** oder nur gemeinsames **Muster**.

*Im Review abschließend geklärt:* Duell-Zeitmechanik (A), Barriere-Semantik (Pro-Frage-Fenster), Tele-Schichtung, Sync-Zweck, Parallelitäts-Begriff, ScoreParams-Ort, Projektions-Einordnung, NvN-Default.

---

## 13. These v1.1 (freigegeben)

> **Der durable Befund:** QuizAway nutzt die gemeinsame **Infrastruktur** (Projektion, Meta-Steuerung, generische Tele), ist aber **kein zweiter Konsument der Card-Chain-Topologie** — weshalb **ADR-A12 unangetastet** bleibt und der Chain-Extraktions-Trigger der Strategie-Synthese v1.3 **vorläufig nicht ausgelöst** ist (echter Kandidat: Sortierspiel-Player). QuizAways Spielprinzip ist **eine von vier, ein Klick, lokal gemessene Zeit** (ScoreParams im Deck), bewusst auf 1-von-4 begrenzt; andere Antwort-Modalitäten sind **andere Player-Typen**. Der aktive Zustand ist schlicht `{ currentQuestion, history[], metaState }`; die **Zwei-Reihen-Analogie** zu MixMi ist eine **optionale Reuse-Hypothese**, kein Fundament. Das **Container/Payload/Projektion-Modell** liefert viewport-adaptive Layouts und ist ein **klarer Wiederverwendungs-Kandidat**, dessen Rang als Aufwandshebel die Implementierung zeigen muss. Mehrspieler ist **orthogonal und zweischichtig**: **generische Tele** (app-übergreifend recycelbar) + **gekapselter, austauschbarer QuizAwayMatchCoordinator** (Pakete, Reveal, **zeitbeschränkte Barriere** — Pro-Frage-Fenster lokal, offene Antworten bei Zeitschranke = falsch, niemand wartet unbegrenzt). Sync koordiniert nur den **Flow** (locker, Paket = Runde) — **außer im Duell** (Paket=1, nahezu simultaner Reveal, Vergleich lokaler `elapsedMs`, kein Uhrenabgleich; Echtzeit-Wettlauf = künftiger ADR). NvN-Team-Score ist **`Sum(PlayerScores)`** (Default). Daraus **Mikes Sparthese**: Projektions-Reuse + Meta-Steuerung + orthogonale, zweischichtige Tele ⇒ vermutlich erheblich gesparte Programmierarbeit — Rangfolge der Hebel an der 7a-Implementierung zu verifizieren.
