# QuizAway → MixMi!/7a — Transfer-Basiskonzept

**Datei:** `quizaway-7a-container-transfer-basiskonzept-2026-06-21.md`
**Pfad:** LernApp `docs/konzepte/`
**Status:** ⚠️ **ABGELÖST durch v1.1** (`quizaway-7a-container-transfer-konzept-v1.1-2026-06-21.md`, freigegeben/archivreif). Dieses v0.1-Spaziergang-Denkpapier bleibt nur als Provenienz. Wesentliche Revision: v0.1 vermutete QuizAway-Klasse-O als Chain-Konsumenten (`compareCheck`) — v1.1 verwirft das: QuizAway ist 1-von-4-MC, **kein** Chain-Konsument; echter Chain-Kandidat = Sortierspiel-Player.
**Datum:** 2026-06-21

**Bindender Rahmen / Vorlesetexte:**
- Card-Chain-(Mechanik-)Kern Strategie-Synthese **v1.3** (Xalento `docs/konzepte/card-chain-engine-strategie-synthese-v1.3-2026-06-19.md`) — definiert „Karte ist Karte", die vier Plug-Points, und benennt den **QuizAway-Refactor explizit als 2. realen Konsumenten**, der die Engine-Extraktion auslöst.
- ADR-A12 (klassik-quiz-fokus) — Engine erst extrahieren, wenn ein 2. Fall sie einfordert.
- QuizAway-Konzept v1.3 (LernApp `docs/konzepte/quizaway_konzept-9.md`).

> **Zweck dieses Papiers:** kurz den Spielablauf QuizAway festhalten — und dann durchdenken, *wie viel* von QuizAway sich tatsächlich in der 7a-Container-Mechanik abbilden lässt. Die zentrale Frage (§4) ist nicht „passt es", sondern „**welche Teile** sind echte Card-Chains und welche nur dieselbe Karten-/Runden-Infrastruktur ohne Kette".

---

## 1. Spielablauf QuizAway (Kurzfassung)

Standortbasiertes Geo-Quiz, „GeoGuessr trifft Quizduell". Fragen zu deutschen Städten.

**Rundenstruktur:**
- 5 Runden pro Spiel, 3 Fragen pro Runde.
- Vor jeder Runde: **Kategoriewahl aus 3 zufällig angebotenen Kategorien** (im Duell abwechselnd, wie Quizduell).
- Frage = 1 Stadt + 4 Antwortoptionen (A–D), Multiple-Choice.

**Takt / Timer (Zwangsweiterschaltung):**
- Kategoriewahl 28 s → Auto-Weiter auf Zufallskategorie.
- Frage 14 s → Timeout = 0 Punkte.
- Feedback 14 s → Auto-Weiter. Rundenabschluss 14 s → Auto-Weiter.

**Punkte:** richtig in 0–3 s = 120 P, danach −7 P/s bis 0 bei 14 s. Falsch / Timeout = 0.

**Modi:** Sofa (zufällige DE-Tour), Virtuelle Route (Start→Ziel, Städte entlang der Strecke), Live (GPS-Radius 5–50 km), **Duell** (echtes P2P/WebRTC, beide bekommen dieselben Fragen, asynchron).

**Drumherum:** 3 Schwierigkeitsgrade (Pool-Größe), Liga-System (Duolingo-Stil, wöchentlich, Top5 auf/Letzte5 ab), P2P-Sync per Event-Ledger + Bloom-Filter.

**Fragetypen (wichtig für §4):** der Katalog ist heterogen —
- **Vergleich zweier Städte:** „Welche ist größer — Mainz oder Wiesbaden?", Höhe, Dichte, Gründungsjahr.
- **Sortier-/Reihenfolge-Fragen:** „Welche Stadt kommt nach Kassel, wenn du von Hamburg nach München fährst?" (Routenprojektion), „nächste Nachbarstadt".
- **Schätzen / Schwelle:** „Hat Hamburg mehr oder weniger als 2.500 Brücken?", „über 200.000 EW?".
- **Reine Faktenzuordnung:** „Für welche Stadt steht ‚KO'?", „In welchem Bundesland liegt Fulda?".

---

## 2. Die 7a-Container-Mechanik (Kurzfassung)

Aus der Strategie-Synthese, repo-verifiziert:

- **Container** = stabiles Topologie-Element in einer **verketteten Liste** (`leftNeighborId`). Container ist die *Truth*, alle Projektionen (`placedWerke`) sind *Views*.
- **Card** = austauschbarer Inhalt eines Containers. „Karte ist Karte" — Bedeutung entsteht aus Kontext + Payload, nicht aus dem Typ.
- **Riddle** = die aktuell zu platzierende Karte.
- **`chronoCheck`** = injizierte Pure Function: „liegt das Jahr der Riddle-Karte zwischen den Karten der Nachbar-Container?" → entscheidet Korrektheit.
- **Schwelle** = N korrekt platzierte Karten = Spielende.
- **Deck** zieht die nächste Riddle; **Meta-Reihe** trägt ToDo/Aktion, Stand, Aufräumen (nichts Spielmechanisches mehr unter der Timeline).
- Vier Plug-Point-Hypothesen: `correctnessCheck`, `advanceTeamStrategy`, `winChecker`, `thresholdRule`.

**Kernaussage:** Das, was MixMi spielmechanisch *ist*, lässt sich auf einen Satz reduzieren — *eine austauschbare Karte korrekt in eine geordnete Kette einsortieren, geprüft durch eine austauschbare Vergleichsfunktion, bis die Schwelle erreicht ist.*

---

## 3. Direkte Abbildung — was 1:1 passt

| QuizAway-Element | 7a-Container-Pendant | Passung |
|---|---|---|
| Stadt-Frage als „Karte" | Card mit `TPayload` = Stadtdaten (lat/lon/EW/Höhe…) | ✅ direkt — „Karte ist Karte" |
| Runden/Fragen-Takt (5×3) | `thresholdRule` (Schwelle = X korrekte) + Runden als Meta-Phase | ✅ Schwelle ist generisch |
| Kategoriewahl (3 Karten) vor Runde | Meta-Reihe als Aktions-Center (genau die schon gebaute „ToDo/Aktion"-Rolle) | ✅ Wiederverwendung Meta-Reihe |
| Timer + Zwangsweiterschaltung | `advanceTeamStrategy` / Phasen-Auto-Advance | ✅ vorhanden in 7a (Auto-Advance) |
| Punkte/Stand | Stand-Karte in Meta-Reihe (`deriveStandDisplay`) | ✅ schon gebaut |
| Duell (2 Spieler) | Team-Shared-Timeline-Modell (Snake, `checkTeamWin`) | ✅ Modell existiert (T1–T5) |
| Schwierigkeitsgrad (Pool) | Deck-Filter / Cross-Game-Katalog (§3.2 Reshuffle) | ✅ Deck-Mechanik trägt das |
| Liga / P2P-Sync | außerhalb des Mechanik-Kerns (Event-Ledger) | ➖ orthogonal, nicht Container-Sache |

**Befund:** Das gesamte *Drumherum* von QuizAway (Karte, Runden, Schwelle, Meta-Reihe, Stand, Duell-Teams, Deck-Pool) fällt erstaunlich glatt auf bereits gebaute 7a-Bausteine. Der Transfer ist auf dieser Ebene fast geschenkt.

---

## 4. Der eigentliche Knackpunkt — ist QuizAway eine *Kette*?

Hier liegt die Denkarbeit für den Spaziergang. Die Strategie-Synthese sagt es schon (§2.3, Randnotiz): **bei Multiple-Choice wird die Container-*Position* trivial.** Eine MC-Frage „In welchem Bundesland liegt Fulda?" hat keinen linken Nachbarn, keine Ordnung — sie in eine `leftNeighborId`-Kette zu zwingen wäre ein Abstraktions-Leck.

Aber QuizAways Katalog ist **nicht homogen**. Er zerfällt sauber in zwei Klassen:

### Klasse O — echte Ordnungs-/Ketten-Fragen (Card-Chain passt natürlich)
Diese *sind* schon strukturell das, was MixMi macht — nur mit anderem Vergleichsoperator statt „Jahr":
- **Routenreihenfolge** „welche Stadt kommt nach Kassel" → Position auf einer Linie = `leftNeighborId`-Kette pur.
- **Geschichte / Gründungsjahr** „Trier oder Köln früher gegründet?" → **wortwörtlich `chronoCheck`**, nur andere Jahres-Quelle.
- **Einwohner / Höhe / Dichte / Fläche sortieren** → `compareCheck` auf einem Skalar. „Sortiere diese 4 Städte nach Einwohnerzahl" = MixMi-Mechanik mit Achse = EW statt Achse = Jahr.
- **Distanz / nächste Nachbarstadt** → Ordnung auf der Distanz-Achse.

→ Für Klasse O ist QuizAway **derselbe Kern**, mit `chronoCheck` generalisiert zu `compareCheck<TAxis>` (Achse: Jahr | EW | Höhe | Distanz | Routen-Projektion). Das ist exakt der „2. reale Konsument", der laut Strategie-Synthese zeigt, ob `correctnessCheck<T>` der richtige Schnitt ist.

### Klasse M — reine Multiple-Choice / Schwelle (Kette ist trivial/falsch)
- Bundesland, KFZ, Stadion, Spezialität, Persönlichkeit → reine Zuordnung, 4 Optionen.
- „über 200.000 EW?", „mehr als 2.500 Brücken?" → Schwellen-/Schätz-Check (`thresholdCheck` / `proximityCheck`), kein Nachbar.

→ Für Klasse M trägt der Container nur die *Karte* (Payload + Frage), aber **die Chain-Topologie ist leer**. Das ist der Fall (b) aus der Strategie-Synthese: `ChainMember<TCard, TPosition>` mit trivialer `TPosition` — oder konzeptionell: MC braucht eine **eigene Karten-Topologie** (Meta-Karte, nicht Timeline-Karte).

### Die Designscheide
Damit ist die offene Frage der Strategie-Synthese (Variante A „Meta-Karten" vs. B „Timeline-Karten") **durch QuizAway selbst beantwortbar — und zwar mit *beiden* Antworten gleichzeitig:**

> QuizAway ist nicht *ein* Konsument des Kerns, sondern **zwei**: Klasse O validiert die Card-Chain (compareCheck), Klasse M validiert die Meta-Karten-Variante (answerCheck/thresholdCheck **ohne** Chain). Genau das macht QuizAway zum idealen 2. Fall — es testet beide Hypothesen der Synthese in einer App.

---

## 5. Einpassung ins übergeordnete Lernkonzept

- QuizAway ist laut Produktvision **ein Player-Typ**, nicht das Zentrum. Der Mechanik-Kern wäre damit die gemeinsame Substanz von Quiz-Player (MixMi) **und** QuizAway **und** perspektivisch den anderen Player-Typen (Zuordnung, Lückentext, Sortierspiel).
- Das stützt die Reihenfolge des geplanten Refactorings: **erst MusicXML-Player / 7a sauber** (1. Konsument steht), **dann/parallel QuizAway** als 2. Konsument — und *erst dann*, mit zwei realen Fällen, die Engine-Extraktion (ADR-A12, „Tag 12+"-Roadmap-Eintrag aus der Synthese §6).
- „Sortierspiel-Player" aus der Produktvision (DOK-3 v11 C.9) und QuizAway-Klasse-O sind **derselbe Player** — das ist ein zusätzliches Argument, dass `compareCheck<TAxis>` die tragfähige Generalisierung ist, nicht nur eine QuizAway-Sonderlocke.

---

## 6. Fragen für den Spaziergang

1. **Ein Spiel oder zwei Modi?** Wird QuizAway *ein* Spiel mit zwei Frage-Klassen (O + M gemischt pro Runde), oder spaltet man sauber in „Sortier-Quiz" (Chain) und „Wissens-Quiz" (Meta)? Quizduell mischt — das wäre Klasse O+M gemischt, Container-Topologie mal gefüllt, mal trivial.
2. **`compareCheck<TAxis>`** — reicht ein generischer Vergleicher mit Achsen-Parameter (Jahr/EW/Höhe/Distanz), oder braucht Routenprojektion doch Sonderlogik (2D→1D-Projektion vor dem Vergleich)?
3. **Riddle bei MC:** Wenn die Karte keinen Platz in der Kette hat — ist „Festlegen" dann einfach „Antwort A–D wählen"? Lässt sich das v3-Festlegen-Verfahren (echter Container an P, verdeckt) auf MC übertragen, oder ist MC ein eigener Interaktions-Pfad?
4. **Was bleibt orthogonal:** Liga, P2P-Sync, GPS/Live-Modus sind klar *nicht* Container-Mechanik. Bleiben sie bewusst draußen (QuizAway-spezifischer Adapter über dem Kern)?
5. **Reihenfolge-Risiko:** Lohnt es, QuizAway-Klasse-O als *erstes* nach dem 7a-Stabilisieren anzugehen (billigster 2. Konsument, weil fast deckungsgleich) — und Klasse M erst danach?

---

## 7. Vorläufige These (zum Verwerfen unterwegs)

> QuizAway transferiert nicht „als Ganzes" auf die Container-Mechanik — sondern **zerfällt am Kern**: seine Sortier-/Vergleichsfragen *sind* MixMi mit anderer Achse (`compareCheck` statt `chronoCheck`) und liefern den sauberen 2. Konsumenten für die Engine-Extraktion; seine reinen Wissensfragen sind **Meta-Karten ohne Kette** und beweisen, dass der Kern eine chain-lose Variante braucht. Genau dieser Zerfall ist der Erkenntnisgewinn — er beantwortet die in der Strategie-Synthese v1.3 offen gelassene Typ-Realisierungs-Frage (a `Card<TPayload>` vs. b `ChainMember<TCard,TPosition>`) empirisch.
