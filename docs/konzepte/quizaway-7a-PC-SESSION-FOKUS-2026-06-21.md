# QuizAway→7a — PC-Session-Fokus: Hypothesen gegen Doku & Code gespiegelt

**Datei:** `quizaway-7a-PC-SESSION-FOKUS-2026-06-21.md`
**Pfad:** LernApp `docs/konzepte/`
**Bezug:** Transfer-Konzept **v1.1** (`quizaway-7a-container-transfer-konzept-v1.1-2026-06-21.md`, freigegeben).
**Zweck:** Mike-Auftrag — die vier strittigen Punkte **gezielt gegen Doku und Code spiegeln**, statt das Papier neu zu bewerten. Unten: Befund pro Punkt mit `Datei:Zeile`-Beleg + offener Rest.
**Datum:** 2026-06-21 · **KEIN Code-Auftrag** — nur Realitätscheck.

> **Gesamt-Ergebnis vorab:** Alle vier Punkte geprüft. Der **Kernbefund von v1.1 hält** (QuizAway = Infrastruktur-, nicht Chain-Konsument). Zwei Stützpfeiler der Sparthese sind aber **dünner als das Papier suggeriert** — und zwar genau dort, wo v1.1 selbst hedged: die **Projektion ist Phase-4-reservierter Typ, kein konsumierter Code** (Punkt 2), und **`@xalento/p2p-tele` existiert nicht** (Punkt 4). Beides bestätigt die Hedges, entwertet aber „klarer Reuse-Kandidat" zu „klarer *Bau*-Kandidat".

---

## Punkt 1 — Kernbefund-Konsistenz (Card-Chain / Synthese v1.3 / ADR-A12)

**Frage:** Verdrahten Card-Chain-Synthese v1.3 / ADR-A12 QuizAway *bereits* als Chain-Trigger? Passt der reale Stand zu „vorläufig nicht ausgelöst"?

**Befund: ✅ konsistent — v1.1 *schärft* v1.3, widerspricht ihr nicht.**

- **ADR-A12** (`klassik-quiz-fokus/docs/architektur/adr/ADR-A12-engine-extrahieren-statt-entwerfen.md`, `status: accepted`): Trigger = „**zweiter konkreter Fall (zweites Spiel ODER zweiter Area-Typ)**". Nennt QuizAway **nirgends** als den Chain-Konsumenten. Validiert sei „nur eine Area-Familie (Sequenz via `leftNeighborId`)". → ADR-A12 ist generisch, nicht an QuizAway gebunden.
- **Synthese v1.3** (`Xalento/docs/konzepte/card-chain-engine-strategie-synthese-v1.3-2026-06-19.md`): §5 nennt den QuizAway-Refactor als *Kandidaten*-Trigger, **§5 Open-Item** lässt aber „MC Variante A (Meta-Karten) vs. B (Timeline-Karten)" ausdrücklich offen „erst beim QuizAway-Refactor". v1.3 hatte also schon vorgesehen, dass QuizAway MC statt Chain sein *könnte*. v1.1 **beantwortet** dieses Open-Item (MC, kein Chain).
- **ROADMAP** (`klassik-quiz-fokus/ROADMAP.md`): **keine** Zeile, die QuizAway als Card-Chain/`compareCheck`-Extraktion verdrahtet (grep `card-chain|compareCheck|order-line|Tag 12` → leer). Einzige Tele-Zeile = „Tele-Tranche 1: Rendezvous + WebRTC" (Transport, s. Punkt 4). Die in Synthese v1.3 §6 als *unerledigt* notierte Aktion „Roadmap-Eintrag Tag 12+: QuizAway als 2. Konsument" wurde offenbar **nie angelegt** — gut so.

**→ Realität deckt sich mit „vorläufig nicht ausgelöst". Nichts in Code/ADR/Roadmap prä-verdrahtet QuizAway als Chain-Trigger.**

**Offen / PC-Aktion (klein):** Synthese v1.3 §5 trägt noch das *offene* MC-Open-Item, das v1.1 jetzt schließt. Erwägen: 1-Zeilen-Nachtrag/Querverweis in v1.3 („beantwortet durch Transfer-Konzept v1.1: QuizAway = MC/Infra, kein Chain") — sonst lebt eine offene Frage weiter, die faktisch entschieden ist.

---

## Punkt 2 — §12.4 Realitätscheck: Projektions-/Container-API = echter Code oder Muster?

**Frage:** Trägt die vorhandene 7a-Projektions-/Container-API den Reuse als **echten Code** — oder nur als **Muster**? (Davon hängt die Zwei-Reihen-Hypothese ab.)

**Befund: ⚠️ gespalten — Container-Kette = echter Code; *Projektion* = reservierter Typ + TODO, NICHT konsumiert.**

- **Container-Kette: echter Code.** `klassik-quiz-fokus/app/src/iter7a/types.ts:49-56` — `Container { leftNeighborId, card, ... }` als Pointer-Chain-Truth (ADR-A11). `Card` hat den generischen Payload-Hook `payload?: unknown` (`types.ts:36-47`). „Karte ist Karte" ist real verdrahtet. ContentSpec/ContentRenderer entkoppeln Interaktion deklarativ (`contentSpec.ts`). **Das trägt.**
- **Projektion: nur Muster.** Exakt die API, auf die v1.1 §4 (Liste/Grid/Streifen, Mobil↔Desktop) baut, ist **reserviert, aber leer**: `types.ts:39-46` —
  > „Reserviert für den Projektions-Layer; **Phase 2 rendert über CSS-Klassen, daher i. d. R. `[]`.** TODO (Phase 4 Wisch/Animation): hier befüllen, **sobald die Projektion Visualisierungen konsumiert**."
  Es gibt den Typ `Visualization{x,y,width,height,shape,…}` (`types.ts:23-34`), aber das Rendering läuft heute über CSS-Klassen, **nicht** über einen Projektions-Layer, der `visualizations` liest.

**→ Antwort auf §12.4: der Container-/Payload-Reuse ist *Code*; der **Projektions**-Reuse ist heute *Muster* (Phase-4-reservierter Typ + TODO). Die viewport-adaptiven Layouts aus v1.1 §4 haben **noch keinen** zu erbenden Code.** Die Zwei-Reihen-Hypothese steht damit auf dem Container-Teil (real), aber ihre UI-Verheißung (Projektion) ist unbau. v1.1s Hedge („Reuse-Kandidat, Aufwands-Rang offen") ist also **berechtigt** — schärfer formuliert: **Bau-Kandidat, nicht Erb-Kandidat.**

**Offen / PC-Aktion:** vor jedem QuizAway-Andocken zuerst klären, ob der 7a-1.-Konsument selbst den Projektions-Layer (Phase 4) baut. Erst dann ist „gemeinsamer Code" statt „gemeinsames Muster" überhaupt prüfbar (= v1.1 §12 Punkt 4 wörtlich).

---

## Punkt 3 — `ScoreParams` im Deck/Card gegen vorhandenes Schema

**Frage:** Passt v1.1s `ScoreParams` „im Deck/in der Frage" zum existierenden Deck-/Card-Schema?

**Befund: ⚠️ kein Zuhause in *keinem* der beiden Schemata — `ScoreParams` ist netto-neu.**

- **`@xalento/types`** (`Xalento/packages/types/src/index.ts:1-19`): `Card{ id, deckId, front, back, tags, createdAt, mediaUrl, mediaType }`, `Deck{ id, title, description, appContext, createdAt, cardCount }`. **Karteikarten-/FSRS-Modell** — kein `scoreParams`, kein `options`, kein `correctIndex`. (Deckt sich mit Synthese v1.3 §2.2 „Widerspruch": bestehendes `@xalento/types` = anderes Modell.)
- **7a** (`klassik-quiz-fokus/app/src/iter7a/types.ts`): `Card{ id, inhalt, visualizations, payload? }`; „Deck" = `DeckLine{ cards:(Card|null)[] }` (`:72`) + `DeckState{ round }` (`:77`). **Kein Punkte-Feld, kein Deck-Metadaten-Slot.** Scoring in 7a = `State.schwelle` (Anzahl korrekt, `:126`), nicht zeit-/punkte-basiert.

**→ v1.1s `Question{…scoreParams}` + „ScoreParams im Deck" mappt auf **keines** der Schemata. Sauberer Sitz nach „Karte ist Karte": `scoreParams` reitet im generischen `Card.payload` (7a hat den Hook bereits); Deck-Defaults brauchen ein **neues `DeckMeta`** — die 7a-`DeckLine`/`DeckState` haben dafür keinen Platz (`DeckState` kennt nur `round`).**

**Offen / PC-Aktion:** Entscheidung „scoreParams pro Frage (Payload) vs. Deck-Default (neues DeckMeta) vs. beides mit Override". v1.1 sagt „im Deck/Frage" — der Code zeigt: Frage-Ebene = `payload` (frei), Deck-Ebene = **muss erst geschaffen werden**. Anti-Rucksack: erst bei realem Bedarf.

---

## Punkt 4 — `@xalento/p2p-tele`: reiner Transport oder Domänenlogik drin?

**Frage:** Ist der aktuelle Stand wirklich reiner Transport — oder steckt schon Match-/Domänenlogik drin (dann Schicht-Trennung nachziehen)?

**Befund: ⚠️ Das Paket existiert nicht. Es gibt nichts „nachzuziehen" — die Schicht-Trennung ist Green-Field.**

- **Kein `@xalento/p2p-tele`.** `Xalento/packages/` = `{quiz, srs, sync, types, ui}`. `packages/sync/src` **leer**, `packages/quiz/src` **leer**, `apps/sync-core/src` **leer** (Scaffolds). → null Transport-Code auf Paket-Ebene.
- **Realer Transport existiert nur im Prototyp**, und dort **maximal vermischt**: `LernApp/apps/quizaway/quizaway_v5.html` enthält im **selben Single-File** 12 WebRTC-Treffer (`datachannel/RTCPeer/createOffer`) **neben** 292 Spiel-Logik-Treffern (`round/reveal/score/antwort`). Das ist das **Gegenteil** der v1.1-§7-Schichtung — Domänenlogik klebt am Transport.
- **ROADMAP** „Tele-Tranche 1": Rendezvous+WebRTC durch Adaptieren von `quizaway-rendezvous.py` + „Match-Code". (›Match-Code‹ hier = Lobby-/Matchmaking-Code, **nicht** Spielregeln — aber beim Bau sauber halten.)

**→ v1.1s saubere Tele(Transport)/Coordinator(Domäne)-Trennung (§7) ist ein **Neubau-Entwurf**, kein Refactor einer bestehenden Schicht. Es gibt kein `@xalento/p2p-tele`, dessen „Reinheit" verletzt sein könnte; der Prototyp ist das Mahnmal (alles in einer Datei). „Schicht-Trennung nachziehen" = **von Grund auf sauber bauen**, mit dem Prototyp als Negativbeispiel.**

**Offen / PC-Aktion:** Beim Anlegen von `@xalento/p2p-tele` (oder Befüllen von `packages/sync`) die v1.1-§7.1-Grenze als depcruise/ESLint-Schranke setzen (Tele kennt **kein** Packet/Round/Reveal/Barrier) — Regel-11-Police *vor* der ersten Tele-Tranche, sonst wiederholt sich die Prototyp-Vermischung.

> **⚠️ Nachtrag/Korrektur 2026-06-21 (Folge-Recherche, s. `quizaway-p2p-bestandsaufnahme-2026-06-21.md`):** Der obige „Green-Field/Mahnmal"-Schluss war **zu hart**. QuizAways P2P ist ein **voll funktionsfähiger, deployter Prototyp** (Rendezvous-Server `LernApp/scripts/sync/rendezvous.py` 625 Z. + Client-Stack `quizaway_v5.html`): WebRTC, STUN/TURN, **automatischer Server-Relay-Fallback**, ACK+Dedup, Heartbeat, Warteraum mit serverseitiger CAS-Paarung, Rundensync. Zusätzlich definieren die Xalento-Konzepte `p2p-tele-vereinheitlichung-modell-und-technik-v1.3` bereits die **Ziel-Schichtung (Plattform/Verben/Domäne) deckungsgleich zu v1.1 §7**. → „Schicht-Trennung nachziehen" = **vorhandene Prototyp-Logik gemäß vorhandenem Konzept extrahieren/portieren** (ideal: WebSocket statt HTTP-Poll), *nicht* von null erfinden. **Für die Sparthese gut:** der teuerste Brocken (robuster P2P-Transport inkl. Relay-Fallback) ist im Feld erprobt. Unverändert: das **Paket** existiert noch nicht (Extraktion bewusst aufgeschoben bis MixMi-Tele = 2. Konsument, ADR-A12-konform).

---

## Konsolidierte Kernaussage für Mike

1. **v1.1-Kernbefund hält** (QuizAway = Infra-, kein Chain-Konsument; ADR-A12 unangetastet; nichts prä-verdrahtet). ✅
2. **Beide harten Hedges von v1.1 sind durch den Code bestätigt** — und der Code sagt: *strenger* lesen. Projektion (§4) und Tele (§7) sind **noch nicht gebaut** (Projektion = Phase-4-Typ; `p2p-tele` = nicht existent). Damit ist die **Sparthese** vorerst „gespart, *sobald* gebaut", nicht „geerbt".
3. **`ScoreParams`** hat kein Schema-Zuhause → Payload (Frage) + neues `DeckMeta` (Deck), bewusst Anti-Rucksack.
4. **Reihenfolge-Konsequenz:** Der billige nächste Schritt ist **nicht** QuizAway-Andocken, sondern dass der **7a-1.-Konsument** Projektions-Layer + (optional) Tele-Paket *real* macht — erst dann wird aus „Muster" „Code", und erst dann ist v1.1 §12.4 echt prüfbar.
