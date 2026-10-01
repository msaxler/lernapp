# QuizAway — Spielkonzept Reise-Modus v0.2

**Story-Satz:**
*Ein Ort wird zum nächsten Spielort. Das Spiel wirft eine Behauptung auf, die man sich zurechtlegen kann. Man legt sich fest. Der Ort erzählt, was wirklich ist, nimmt die eigene Theorie mit und knüpft an den Ort davor an. Der Reiseführer ist das Fundament; wie man sich festlegt, ist pro Sitzplatz anders, und dort sitzt der Witz.*

---

## Status-Block

| | |
|---|---|
| **Version** | v0.2 (nach Review-Runde 3, fünf Reviews R3-A bis R3-E) |
| **Datum** | 2026-10-01 |
| **Status** | Konzept, bereit für Papier-Feldtest. Keine Implementierungsfreigabe; die kommt nach Feldtest-Protokollen (§11). |
| **Scope** | Spielmechanik des Reise-Modus: Auto-Gruppe, Bahn-Gruppe, Bahn-Solo, mit drei Streckenquellen. Der frühere „Sofa"-Modus ist keine eigene Situation, sondern gewürfelte Strecke plus Display-Modus. Fern-Duell nicht Gegenstand. Inhalte und Technik gesetzt; §8 nennt Schnittstellen, §9 Berührungspunkte. |
| **Provenance** | v0.1 → Runde 3 (fünf Reviews) → Rulings in Anhang A → v0.2. Synthese nach stärkstem Argument. |
| **Entschieden (Mike)** | Ein Gerät. Beifahrer liest, TTS optional später. Kein Solo im Auto. |
| **Offen** | Nichts mehr auf Konzeptebene. Alles Weitere entscheidet der Feldtest (§10). |

**TL;DR gegenüber v0.1:** Der Kern wird präziser gefasst (Frage-/Reveal-Zyklus identisch, Modi ändern nur Bedienung, Festlegung, Sozialschicht). Drei Widersprüche sind aufgelöst: Fahrtbilanz statt Score, kein „Weiter" nur innerhalb der Frage, Radar ist keine Ausnahme mehr, sondern Familie A mit Nachbarorten und verbal stellbar (Auto bekommt Geo-Fragen zurück). Neu: Push im Auto, Pull in der Bahn. Neu: Auto-Festlegung mit Mehrheit und Gespalten-Fall im Reveal. Solo bekommt eine vierte Quelle, den Anschluss (Reveals verknüpfen Orte, Karte antwortet), und ein Teilen-Artefakt am Ende. Leiter wird Ablaufmodifikator mit eigenem Kipp. Content-Regeln für Distraktoren und Lüge sind als Schnittstelle benannt. K1 und K3 messen jetzt Ursachen, nicht Abbruch.

---

## 1. Der Core-Loop

Fünf Schritte, in jeder Situation gleich. Modi dürfen nur Bedienung, Festlegung (Schritt 3) und soziale Zusatzschichten verändern.

**1. Auslöser.** Ein Ort wird zum nächsten Spielort. Je nach Streckenquelle (§1a) geschieht das durch Position, Zeittakt oder einen Weiterschaltimpuls. Im Auto drängt sich die Frage auf (Push); in der Bahn wartet sie (Pull, §3).

**2. Behauptung aufwerfen.** Eine kurze Frage oder Aussage über den Ort mit drei oder vier Optionen. **Qualitätsregel:** Jede Option muss als eigenständige plausible Theorie formulierbar sein („Der Name kommt vom Bach" statt „wegen eines Flusses"). Frage in einem Atemzug, Optionen kurz, keine nackten Zahlen.

**3. Theorie bilden und festlegen.** Die Spielenden legen sich fest. *Wie*, bestimmt der Modus (§3). Begründen ist Standardangebot, nie Pflicht.

**4. Story-Reveal.** (a) Die Festlegung wird aufgegriffen, auch eine gespaltene. (b) Die Geschichte des Orts wird erzählt und webt die Theorie ein. (c) Das Urteil wird nach der Erklärung eindeutig, sofern die Dramaturgie davon profitiert; es wird nicht künstlich nachgeschoben, wenn die Geschichte es schon gesagt hat. (d) Wo möglich, knüpft der Reveal an einen vorherigen Ort der Fahrt an (§3.3, Anschluss). Quelle sichtbar.

**5. Nachhall.** Der Ort wandert auf die Fahrtkarte. Kein „Weiter" innerhalb der Frage-/Reveal-Sequenz. Zwischen Orten gibt es je nach Streckenquelle einen Weiterschaltimpuls (ein Tap, großes Ziel, kein Menü). Nachschlag zum selben Ort nur durch explizites Tippen, nie automatisch, nie angeboten.

**Was der Loop nicht hat:** Zeitdruck als Spannungsquelle, Punktestand pro Frage, Rangliste, Leben, Streaks, Statistiken als Belohnung.

### 1a. Streckenquelle

| Quelle | Wie | Takt | Wofür |
|---|---|---|---|
| **Echte Fahrt** | GPS, nächster Ort mit Material auf oder nahe der Position | Bewegung | Auto, Bahn |
| **Geplante Route** | Streckenliste (Google-Maps-Route, Bahnverbindung), Orte entlang der Linie | Tap oder Zeittakt | Bahn ohne GPS, Vorbereitung, Nachspielen |
| **Gewürfelte Strecke** | x Orte aus einem definierten Raum, zu einer virtuellen Strecke verbunden | Tap oder Zeittakt | Sofa, Wartezimmer, Üben, Feldtest |

**Regeln:**
- Die Quelle liefert nur Orte **mit Material**. Lieber 10 Orte mit Fragen als 15 mit Lücken. Ein Ort ohne Material wird still übersprungen, nie als leere Frage ausgeliefert.
- Die Quelle ist orthogonal zum Modus. Gewürfelte Strecke im Bahn-Gruppen-Modus am Küchentisch ist zulässig.
- Keine Ortsschilderkennung, keine Kamera. GPS ist eine Quelle von dreien.
- Fahrtkarte und Bingo funktionieren für alle Quellen gleich.
- Kipp: Feldtest zählt still übersprungene Kilometer; ab einer Schwelle stimmt die Material-Heuristik nicht.

---

## 2. Die drei Fragefamilien und ein Ablaufmodifikator

Alle Familien sind „ein Klick, drei oder vier Strings".

| Familie | Form | Datenquelle | Einsatz |
|---|---|---|---|
| **A — Behauptung** | Frage, vier Theorien als Optionen | Schicht 2 für die wahre Option; Distraktoren mit Negativnachweis (§8) | Standard |
| **B — Lüge** | Drei Aussagen, eine gelogen | ≥ 2 belastbare Schicht-2-Fakten; Lüge mit Negativnachweis (§8) | Nur wo Daten reichen, sonst A. Aussagen ≤ 8 Wörter. Im Auto mit Kipp (§3.1). |
| **C — Größenordnung** | Zahlenfrage ohne Zahlen: Epochen, Spannen | Schicht 1 numerisch | Höchstens jede dritte Frage, nie zwei hintereinander |

**Radar** ist Familie A mit Nachbarorten als Optionen („Welcher dieser vier Orte hat ein Freibad?"). Verbal vollständig stellbar („südlich von euch X, nordöstlich Y…"), deshalb in allen Modi, auch im Auto. In Display-Modi kommt die schematische Karte mit nummerierten Punkten als Darstellung dazu (Centroide, keine Kacheln). **Ortsfokus-Regel:** Der Reveal einer Radar-Frage kehrt zum aktuellen Ort zurück („Dieser hat keins, der Nachbar schon, und zwar weil…"). Sonst wird der Reiseführer zum Nachbarschaftsquiz.

**Leiter** ist keine Familie, sondern ein **Ablaufmodifikator** über Familie C: eine Sequenz von Mehr/Weniger-Fragen mit Abbruch, mindestens drei Stufen, unter 60 Sekunden. Sie ist der fragilste Baustein im Kern, weil Ja/Nein wenig Theorie erlaubt (K3). Eigenes Kipp: Werden Leiter-Antworten im Feldtest je begründet? Wenn nicht, wird die Leiter gestrichen und C bleibt bei Spannen.

---

## 3. Die drei Präsentationsmodi

Ein Modus variiert genau drei Dinge: **Bedienung**, **Festlegung**, **Quelle des Moments**. Dazu kommt der **Takt**: Push oder Pull.

**Modus-Wahl beim Start der Fahrt:** eine Frage, zwei Antworten: „Fährt jemand?" (Auto-Modus) oder „Wir sitzen alle" (Bahn-Modus; Gruppe oder Solo ergibt sich aus der Spielerzahl). Ein Tap, dann nichts mehr.

### 3.1 Auto-Modus (Gruppe, Fahrer:in ohne Display) — Push

- **Takt:** Die Frage drängt sich auf, wenn der Ort kommt. Fenster 20–60 Sekunden, Gesamtrunde ≤ 60 Sekunden.
- **Bedienung:** Beifahrer liest vor (große Schrift, Frage und Optionen auf einem Screen, Reveal auf dem nächsten). Rollenwechsel pro Fahrtabschnitt ab drei Personen.
- **Festlegung:** Zuruf auf „3-2-1", alle gleichzeitig. **Regel:** Jede Festlegung muss ohne Blick aufs Display verbal eindeutig sein („C!", „Stopp!"). Beifahrer tippt die Mehrheit. **Bei Spaltung oder Patt tippt er beide Optionen**; der Reveal hat dafür einen zweiten Fall: „Ihr wart gespalten: A gegen B. Beide klingen plausibel, aber…" Keine „lauteste Theorie", keine Entscheidung durch den Beifahrer allein.
- **Quelle des Moments:** gleichzeitiges öffentliches Festlegen; die Spaltung ist der Moment, nicht ein Randfall. Feldtest zählt, wie oft gespalten wird.
- **Familie B im Auto:** zugelassen mit Formregel (≤ 8 Wörter, einmal wiederholen erlaubt). Kipp: Wird öfter wiederholt oder fragt jemand nach dem Reveal „was war nochmal zwei?", wird B im Auto auf zwei Aussagen (Entweder-Oder) gedrosselt oder pausiert.
- **Nicht verfügbar:** Wer-glaubt-wem, Bingo, Karte als Darstellung (Radar verbal ja).
- **Betriebsgrenze:** Bei zwei Personen ist der Beifahrer dauerhaft Vorleser, Moderator und Tipper. Das ist für lange Fahrten eine Grenze, nicht nur ein Kipp. TTS ist dafür die vorgesehene Entlastung (entschieden: optional, später).
- **K9:** Keine Bedienung, kein Blick der fahrenden Person. Ausschluss.

### 3.2 Bahn-Gruppen-Modus (Gerät in der Tischmitte) — Pull

- **Takt:** Die App zeigt still die Fahrtkarte mit dem nächsten Ort („Nächster Ort: X"). Die Gruppe startet die Frage, wenn sie bereit ist. Kein Ping. Fenster ≤ 90 Sekunden pro Runde als Richtwert.
- **Bedienung:** Alle lesen selbst, kein Vorleser, keine Host-Belastung.
- **Festlegung:** Zeigen oder kurzer Zuruf, ein Tap. **Wer-glaubt-wem** als Zusatzschicht ab drei Spielenden, nicht bei jeder Frage: Antworten werden gezeigt, die Einschätzung „wer liegt richtig" wird mündlich reihum gesagt, die nächste Person tippt. Kein Herumreichen pro Antwort. Kipp: Runde über zwei Minuten.
- **Quelle des Moments:** gemeinsamer Blick, Zeigen, Nacheinander-Diskutieren. Familie B spielt hier ihre Länge als Stärke aus.
- **Verfügbar:** alle Familien, Radar mit Karte, Wer-glaubt-wem, Bingo (§4) nur auf langen Strecken ohne Orte.

### 3.3 Bahn-Solo-Modus (eine Person, eigenes Tempo) — Pull

- **Takt:** Die Person scrollt die kommenden Orte der Strecke, startet die Frage selbst. Fenster frei.
- **Bedienung und Festlegung:** Tap. Leiter in Eigenregie gegen sich selbst.
- **Quelle des Moments (K5-Ersatz):** Solo hat keinen sozialen Moment, und das ist in Ordnung. K4 (Reveal trägt Geschichte) ist die tragende Säule; der Reveal muss solo pointierter sein als in der Gruppe, weil er die einzige Belohnung ist. Vier Ebenen, nicht gleichwertig:
  1. **Unmittelbar, jede Frage:** Die eigene Theorie als Gegenüber. Der Reveal kennt die gewählte Antwort und würdigt sie. **Formelhaftigkeits-Regel:** drei bis vier Einwebungs-Muster rotieren, die Theorie auch mal ernst nehmen („Deine Bach-Theorie war nicht falsch, der Bach heißt heute nur anders"), nie nur abfertigen.
  2. **Gewürz, nur Familie C:** Nähe statt richtig/falsch („nur 300 daneben").
  3. **Rahmen, über die Fahrt:** Sammeln. Die Karte wächst sichtbar. Allein ist das Fortschritt, kein Moment; es trägt nur zusammen mit 4.
  4. **Anschluss (neu):** Die Karte antwortet. Reveals verknüpfen den aktuellen Ort mit gespielten Pins („Der letzte Pin war doppelt so groß, 9 km weiter, und trotzdem hat der kleinere das Freibad"; „Ort A und Ort B teilten bis 1810 denselben Gerichtshof"). Das erzeugt die Serienneugier „mal sehen, was der nächste Ort erzählt". Content: Familie C und Vergleichsfakten über bereits gespielte Orte, also vorhanden, kein neuer Rucksack.
- **Teilen-Artefakt am Ende:** Die Fahrtkarte endet solo mit „Drei Dinge, die ich heute nicht wusste", teilbar als Bild. Das bedient K6 (Gesprächswert), nicht K5, und ist der einzige realistische Ersatz für den fehlenden Zuhörer.
- **Nicht solo:** Mehrheits-Balken, Prozentzahlen, jede Statistik als Belohnung. Das wäre die Retention-Mechanik, die ausgeschlossen ist.
- **Verfügbar:** alle Familien, Radar mit Karte, Bingo (eigene Karte).

### 3.4 Was ein Modus nicht darf

Einen eigenen Fragetyp einführen. Den Reveal verändern. Punkte pro Frage sichtbar machen. Eine Frage so bauen, dass sie nicht in allen drei Modi gestellt werden könnte. Der Frage-/Reveal-Zyklus ist in allen Modi identisch; Radar ist Darstellung, nicht Fragetyp.

---

## 4. Die zwei Rahmen

Rahmen sind Mechaniken, die den Core-Loop nicht verändern.

**Fahrtkarte (alle Modi).** Schematische Streckenkarte, ein Pin pro gespieltem Ort: Ortsname, ein Satz Steckbrief, Ergebnis als Farbe oder Emoji. Am Ende eine **Fahrtbilanz**: „Neuwied–Kassel: 14 Orte, 9 Treffer, 3 Lacher." **Präzisierung:** Treffer werden gezählt und am Ende benannt, nie pro Frage angezeigt, nie bewertet. Keine Darstellung, die „9 von 14" als gute oder schlechte Fahrt einordnet. Das ist Erinnerung, kein Score. Optional eine Große Fahrtfrage am Ziel über die gespielten Orte, als Leiter. Solo zusätzlich „Drei Dinge, die ich nicht wusste" (§3.3).

**Bingo (nur Bahn).** Gruppe: eine gemeinsame 3×3-Karte, alle rufen Kreuze. Solo: eigene Karte. Felder sind Achsen mit Schwellwert, **nur aus Schicht 0/1 automatisch prüfbar** (Einwohner, Kennzeichen, Fluss, Burg, Namensendung); was nicht prüfbar ist, ist kein Bingo-Feld. **Hierarchie:** Reise-Quiz ist Hauptspiel, Bingo ist Füller. Bingo unterbricht nie den Core-Loop und überspringt nie einen Ort mit Material. Einsatz nur auf langen Strecken ohne Orte, nicht als Dauerrahmen. Kipp: Zieht Aufmerksamkeit von der Frage.

---

## 5. Taktung (Hypothesen, ungetestet)

Richtwerte aus den Review-Runden, im Feldtest zu kalibrieren:

- Eine Frage pro Ort. Nachschlag nur durch explizites Tippen.
- Familie C höchstens jede dritte Frage, nie zwei hintereinander. Leiter höchstens jede fünfte.
- Wer-glaubt-wem (Bahn-Gruppe) höchstens jede vierte Frage.
- Radar mit Karte (Bahn) höchstens jede zweite Frage.
- Anschluss (Solo) nicht bei jeder Frage, sonst wird er Formel.
- Zeitbudget: Auto ≤ 60 s, Bahn-Gruppe ≤ 90 s, Solo frei.
- Mikro-Feedback erlaubt („Ort 4 von 12"), solange es nichts unterbricht.

---

## 6. Anti-Rucksack

Nicht in v1: Ortsschilderkennung, Kamera; TTS (optional später); Mehrheits-Balken und jede Prozentstatistik; p2p oder zweites Gerät; Fenster-Detektiv als Pflicht; Lokal-Rätsel; Team-Schätzung mit Rechnen; Kartenkacheln; Badges, Level, Achievements, Streaks; automatischer Nachschlag; „Noch eine?"-Button.

---

## 7. Kipp-Kriterien (präzisiert)

- **K1 — Kernversprechen:** Nach dem Reveal kann die spielende Person die eigene Theorie und die tatsächliche Geschichte in einem Satz wiedergeben und sagen, warum die Theorie plausibel oder falsch war. Kann sie das nicht, trägt der Reveal nicht. (Nicht mehr: „Satz wurde gelesen".)
- **K2 — Schnitt:** Eine Frage lässt sich nicht in allen drei Modi stellen, ohne den Fragetyp zu ändern → Kern/Schalen-Trennung falsch geschnitten.
- **K3a — Solo, Abbruch:** An natürlichen Pausen (Bahnhof, App-Wechsel) wird abgebrochen statt „noch ein Ort" gewählt. Ab zwei Abbrüchen vor dem geplanten Ende reicht der K5-Ersatz nicht.
- **K3b — Solo, Durchtippen:** Über mehrere aufeinanderfolgende Fragen wird keine Theorie mehr gebildet, der Reveal wird weggewischt (Lesedauer beim 10. Ort gegenüber dem 2.). Dann ist es Informationsabfrage, kein Spiel. K3b ist der wichtigere Fehler als K3a.
- **K4 — Host:** Beifahrer wirkt nach fünf Orten nur noch als Vorleser → Betriebsgrenze real, TTS vorziehen.
- **K5 — Streckenquelle:** Übersprungene Kilometer über Schwelle → Material-Heuristik falsch.
- **K6 — Leiter:** Leiter-Antworten werden nie begründet → Leiter streichen, C bleibt Spannen.

---

## 8. Schnittstelle zu den Inhalten (Gemeinde-Achsen)

Die Spielmechanik hängt an vier Content-Regeln, die ins Achsen-Regelwerk gehören, hier nur benannt:

1. **Negativnachweis für Distraktoren (Familie A):** Eine falsche Option muss falsch sein, nicht nur „nicht als richtig bekannt". Entweder eigener Negativnachweis oder kontrollierte Generierungsregel (gespiegelter Fakt eines Nachbarorts, der für den Zielort ausgeschlossen ist).
2. **Negativnachweis für die Lüge (Familie B):** Die falsche Aussage muss für den Zielort explizit widerlegt oder eindeutig einem anderen Ort zugeordnet sein. Sonst entsteht keine Lüge, sondern eine ungesicherte Aussage.
3. **Theorie-Formulierung:** Jede Option als eigenständige Theorie formulierbar (§1 Schritt 2). Das ist eine Anforderung an die Frage-Generierung, nicht an das UI.
4. **Reveal-Vertrag:** Der Reveal nimmt als Eingabe die gewählte Option **oder einen Optionssatz** (gespalten) und optional einen vorherigen Pin (Anschluss). Drei Template-Fälle: einstimmig richtig, einstimmig falsch, gespalten; dazu Rotation der Einwebungs-Muster.

Offene Content-Frage, kein Mechanikproblem: Wie viele der ~10.700 Orte haben ≥ 2 belastbare Fakten für Familie B? Die Quote entscheidet, ob B Regel oder Ausnahme ist.

---

## 9. Berührungspunkte mit dem Transfer-Konzept v1.1

- **Kern-Interface bleibt:** „ein Klick, vier Strings" ist die Touch-Schicht aller Modi. Zuruf ist Beifahrer-Tap nach Ruf.
- **Projektion bestätigt:** Radar ist dieselbe Frage mit anderer Darstellung, und zwar auch ohne Karte stellbar. Das ist der stärkste Beleg für die Projektions-These.
- **Leiter:** Ablaufmodifikator über C, kein Fragetyp. Modellieren als Sequenz über dem Kern.
- **Wer-glaubt-wem:** zweite Abgabe; einzige Erweiterung der Kern-Schnittstelle. Zusatzschicht, nicht Kern.
- **Reveal-Vertrag:** erweitert um Optionssatz (gespalten) und Anschluss-Pin. Kleine, aber echte Erweiterung gegenüber dem MixMi!-SteckbriefModal.
- **Streckenquelle:** eigener Baustein vor dem Kern, liefert „nächster Ort mit Material". Prüfen, ob v5-Route so geschnitten ist.
- **Push/Pull:** ein Flag beim Start, kein eigener Modus.
- **elapsedMs:** vorhanden, nie angezeigt. Fern-Duell unverändert.
- **Rahmen:** verändern den Core-Loop nicht; Fahrtkarte hält Zustand, Bingo nimmt Eingaben.

---

## 10. Feldtest

Drei Papier-Tests, alle ohne Code. Reihenfolge: Solo am Tisch zuerst (billigster, am wenigsten gesichert), dann Bahn-Gruppe am Tisch, dann Auto auf der Straße.

**Solo am Tisch:** gewürfelte Strecke, 10 Orte aus einem Raum, den die Testperson nicht kennt. Karten von Mike, Reveal auf der Rückseite, davon mindestens drei mit Anschluss an einen vorherigen Ort, zwei Radar verbal. Leere Streckenkarte zum Pinnen. Protokoll: K1 (Theorie und Geschichte in einem Satz wiedergeben, stichprobenartig abfragen), K3a (Pausen, Abbrüche), K3b (wird vor dem Umdrehen noch überlegt?), Lesedauer Ort 2 vs. Ort 10, abends „Drei Dinge".

**Bahn-Gruppe am Tisch:** gewürfelte Strecke, 8 Orte, zwei bis drei Personen. 3 Radar mit Punktekarte, 3 Lügen-Steckbriefe, 2 Wer-glaubt-wem mündlich. Eine 3×3-Bingokarte nur für eine künstliche „leere Strecke" von drei Orten ohne Frage. Protokoll: Zeigen, Diskussionsdauer, Bingo-Ablenkung, Nachschlag-Wunsch ohne Angebot.

**Auto auf der Straße:** echte Fahrt, 10 Orte, Beifahrer liest. 5 Behauptungen (davon 2 Radar verbal, 2 mit flachen Distraktoren als Kontrolle), 3 Lügen-Steckbriefe (≤ 8 Wörter), 2 Leitern. Protokoll: gleichzeitiges Rufen, **Spaltungen zählen**, Wiederholungen bei B, Lachmoment (wird das Ergebnis kommentiert?), Dauer pro Schritt, Beifahrer nach fünf Orten (Mitspieler oder Vorleser?), Leiter-Begründungen (K6), abends Weitererzählen.

**Übergreifende Frage, die alle drei Tests beantworten müssen:** Erzeugt „Ich habe eine Theorie" einen anderen Spielzustand als „Ich möchte die Information wissen"? Wenn ja, steht der Kern. Wenn nein, ist nicht an Bingo, Radar oder Audio zu optimieren, sondern am Verhältnis Theorie → Reveal.

---

## 11. Nächste Schritte

1. Mike-Freigabe von v0.2 als Feldtest-Grundlage.
2. Drei Papier-Tests nach §10, Protokolle als Markdown.
3. Protokolle → Spielkonzept v1.0 → Implementierungsfreigabe.
4. Content-Regeln aus §8 ins Achsen-Regelwerk übertragen (eigener Arbeitsschritt, parallel möglich).
5. Erst danach PC-Session: v1.0 gegen Transfer-Konzept v1.1 und Code (§9).

Keine weitere Review-Runde über die Mechanik. Fünf Reviewer sagen unabhängig: Der entscheidende Test ist jetzt nicht „Ist das Konzept logisch?", sondern der Feldtest.

---

**These:** Ein Reiseführer, der erst eine eigene Theorie verlangt und danach die Antwort erzählt. Der Reiseführer ist das Fundament und in jeder Situation gleich. Wie man sich festlegt, ist pro Sitzplatz anders, und dort liegt der Witz: im gleichzeitigen Rufen, im Zeigen, im Stopp gegen sich selbst. Das Fundament ist entschieden. Der Witz wird getestet.

*Ende Spielkonzept v0.2.*

---

## Anhang A — Rulings Runde 3

Fünf Reviews (R3-A bis R3-E). Angenommen, abgelehnt, mit Begründung. Reihenfolge nach Gewicht.

### Angenommen

| Finding | Von | Ruling |
|---|---|---|
| Score-Widerspruch Fahrtkarte | A, B, D | Fahrtbilanz statt Score; Treffer gezählt, nie pro Frage, nie bewertet (§4) |
| „Kein Weiter-Knopf" zu pauschal | A, B, D | Präzisiert: nicht innerhalb Frage/Reveal; zwischen Orten Weiterschaltimpuls je nach Quelle (§1) |
| Radar-Ausnahme kollidiert mit K2 | A, B, D | Ausnahme gestrichen. Radar ist Familie A mit Nachbarorten, verbal stellbar (D), Karte Darstellung. Auto bekommt Geo-Fragen (§2) |
| Radar bricht Ortsfokus | B | Ortsfokus-Regel: Reveal kehrt zum aktuellen Ort zurück (§2) |
| Auto-Festlegung unterspezifiziert, „lauteste Theorie" | A, B, D | Mehrheit; bei Spaltung beide Optionen, Reveal mit Gespalten-Fall (D). B's Patt-Regel „zuletzt gerufen" verworfen, weil sie die Spaltung versteckt statt sie zum Moment zu machen (§3.1) |
| Festlegung muss verbal eindeutig sein | A | Regel in §3.1 |
| Host-Belastung bei zwei Personen ist Betriebsgrenze | B | §3.1 |
| Push (Auto) vs. Pull (Bahn) | C | Angenommen als Takt-Eigenschaft der Modi, nicht als eigener Modus (§3). Stärkstes neues Argument der Runde. |
| Modus-Schalter beim Start | C | Eine Frage, ein Tap (§3). C's Kopplung an Audio-An/Aus nicht übernommen, weil Audio entschieden optional ist. |
| Solo: drei Quellen nicht gleichwertig | A, B, D | Vier Ebenen mit Gewichtung (§3.3) |
| Solo: vierte Quelle | A (Serienneugier), D (reaktive Karte), E (Detektiv-Faden) | Zusammengeführt als **Anschluss**: Reveals verknüpfen Orte. Drei Reviewer, drei Namen, eine Idee (§3.3) |
| Solo: Teilen-Impuls | B | „Drei Dinge, die ich nicht wusste" als Ende der Solo-Fahrtkarte (§3.3) |
| Solo: keine Statistik, K4 als Säule | C | Angenommen; Mehrheits-Balken solo gestrichen, nicht nur zurückgestellt (§3.3) |
| Formelhaftigkeit des Einwebens | D | Rotation von Mustern, Theorie ernst nehmen (§3.3, §8) |
| K1 zu schwach | A | Wiedergabe-Test statt Lese-Test (§7) |
| K3 misst Abbruch, nicht Ursache | A, D, E | K3a (Pausen-Abbrüche, ≥ 2) und K3b (Durchtippen, Lesedauer) (§7) |
| Leiter ist Ablauf, keine Familie | A, D | Ablaufmodifikator über C mit eigenem Kipp K6 (§2) |
| Lüge und Distraktoren brauchen Negativnachweis | A, B | Content-Schnittstelle §8 |
| Optionen als Theorien, operationalisiert | A | Qualitätsregel in §1 Schritt 2 |
| Urteil zuletzt nicht zu hart | A | Weichere Formulierung in §1 Schritt 4 |
| Bingo-Hierarchie, nur prüfbare Achsen | A, B | §4 |
| Leerläufe auf der Strecke | D | Material-Regel und Kipp K5 in §1a |
| Taktung als Hypothesen markieren | D | §5 |
| Nachschlag: nie automatisch, kein Angebot | A, D | §1 Schritt 5, §6 |
| Wer-glaubt-wem: Herumreichen ist Reibung | D | Einschätzung mündlich reihum, nächste Person tippt (§3.2) |
| „Rahmen sind nur Leser" ungenau | A | „verändern den Core-Loop nicht" (§4, §9) |
| These überkorrigiert („klein") | D | These umformuliert |
| Familie B im Auto zu schwer | E | Nicht ausgeschlossen (Runde 2: drei von vier wollten es im Auto), aber Kipp mit Drossel auf Entweder-Oder (§3.1) |
| Zeitbudgets pro Modus | B | §5 |

### Abgelehnt

| Finding | Von | Warum nicht |
|---|---|---|
| Radar als Rahmen statt Frage in der Bahn-Gruppe (Überforderung) | C | Vier von fünf Runde-2b-Reviewer sahen Radar als Frage tragfähig; C's Einwand (Karte lesen dauert) ist durch die verbale Stellbarkeit (D) und die Taktung (jede zweite Frage) beherrschbar. Kipp: Radar-Runden in der Bahn über 90 s. |
| C16 Mehrheits-Balken als Text-Statistik in der Bahn-Gruppe | C | Datenproblem unverändert (keine Antworten am Anfang); C selbst nennt Statistik solo Gamification, das Argument gilt auch in der Gruppe. Bleibt zurückgestellt. |
| Auto mit C17 Lokalradio als Standard | C | Von Mike entschieden: Beifahrer liest, TTS optional später. |
| Begründung als Pflicht im Auto („Standardangebot 5 s") | B | Runde 2 hat Pflicht verworfen; „Standardangebot" ist angenommen, Pflicht nicht. |
| Familie B im Auto ausschließen | E | Zu früh; Kipp statt Ausschluss. |

*Ende Anhang A.*
