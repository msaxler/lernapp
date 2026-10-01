# QuizAway — UI-Konzept Reise-Modus v0.1

Synthese der UI-Review-Runde 1 (Smartphone-Oberfläche, Best Practice). Gilt für das Spielkonzept Reise-Modus v0.2.3 (GEOSYNC 020). Das Spielkonzept ist die Instanz; wo ein UI-Vorschlag ihm widerspricht, verliert der Vorschlag, auch wenn er mehrheitlich kam.

## Status-Block

| | |
|---|---|
| **Repo / Pfad** | lernapp / docs-konzepte |
| **Version** | v0.1 (2026-10-01) |
| **Status** | Entwurf, Rulings zur Freigabe durch Mike. Drei Punkte ausdrücklich offen (§7). |
| **Grundlage** | Spielkonzept Reise-Modus v0.2.3 (freigegeben), Feldtest-Protokoll Solo Freiburg (GEOSYNC 019) |
| **Eingänge** | U0 eigene HTML-Skizze „QuizAway Reise-Modus Screens"; U1–U7 sieben Text-Konzepte der Review-Partner (zwei Anhänge waren Duplikate des R4-A-Reviews, nicht UI-relevant); U8 Screen-Collage (13 Screens + Design-Prinzipien); U9 gerendertes Einzelbild „Niederbieber · Ort 4 von 12 · Push · Beifahrer liest" |
| **Methode** | Stärkstes Argument, nicht Mehrheit. Jedes Ruling nennt den Konflikt, die Entscheidung, den Grund und, wo nötig, das Kipp-Kriterium. |
| **Nächster Schritt** | Freigabe → HTML-Skizze auf v0.1 ziehen → Papier-Screens für den zweiten Solo-Test und den Bahn-Gruppen-Tisch |

---

## 1. Was alle Eingänge gemeinsam tragen (ohne Ruling)

Diese Punkte kamen aus mindestens fünf Quellen gleichlautend und widersprechen dem Spielkonzept nicht. Sie gelten.

1. **Kein Login, kein Onboarding, kein Hamburger-Menü.** Die App öffnet auf dem Startschirm, eine Entscheidung (Modus), danach nie wieder gefragt. Einstellungen (Audio, Theme) hinter einem Zahnrad nur auf dem Startschirm.
2. **Ein Screen, ein Gedanke.** Frage und Reveal sind getrennte, bildschirmfüllende Zustände. Im Auto scrollt kein Screen. In der Bahn scrollt nur die Fahrtkarte.
3. **Die ganze Fläche ist der Button.** Optionen sind Kacheln, keine Radiobuttons, keine Checkboxen.
4. **Kein Timer, kein Score, keine Punktewolke, keine Streak.** Fortschritt nur als dezente Zeile „Ort 4 von 12".
5. **Bedienelemente im unteren Drittel** (Daumenzone; im Auto liegt das Gerät in der Halterung oder auf dem Schoß, das obere Drittel ist Anzeige).
6. **Animationen ≤ 200 ms, nichts blinkt, nichts pulsiert im Auto** (K9). Einzige Bewegung: Reveal gleitet von unten hoch.
7. **Haptik:** kurzer Impuls bei Antwort-Tap und beim Erscheinen des Reveals. Ersetzt den Spielstein.
8. **Teilen = Bild über System-Share.** Kein eigener Export-Dialog.
9. **Kein „Nochmal spielen" am Fahrtende.** „Schließen" führt zum Start.
10. **Quelle sichtbar, aber klein**, unter jedem Reveal.

---

## 2. Rulings — Angenommen

**R-UI-1 — Modus-Wahl: drei Karten, nicht zwei.**
Konflikt: U2, U4, U5 bieten nur „Ich fahre / Wir sitzen alle"; U0, U7 bieten drei Modi. Entscheidung: **drei Karten**, weil Bahn-Solo einen eigenen Takt hat (Ortsliste als Vorschau, Drei Dinge am Ende, kein Multi-Select) und sich nicht aus „Wir sitzen alle" ableiten lässt, ohne später eine Spieleranzahl abzufragen. Die **Formulierung bleibt offen** (Spielkonzept §3: Entscheidung nach dem Feldtest; nicht „wir" für eine Einzelperson, nicht an die Streckenquelle gekoppelt). Arbeitsfassung: „Jemand fährt" / „Wir sitzen zusammen" / „Ich bin allein unterwegs".

**R-UI-2 — Streckenquelle: drei Karten in einem Sheet, dann fertig.**
Aus U2, U5 übernommen: „Echte Fahrt (GPS)" / „Geplante Route" / „Gewürfelt". Geplante Route = genau ein Screen „Von … / Nach …" mit Tausch-Icon, keine Wizard-Seiten. Gewürfelt = Raum-Chips (Umkreis 50 km, Landkreis, Bundesland, Deutschland) und ein großer Würfel-Button. Gewürfelte Strecke auf der Fahrtkarte **gestrichelt**, damit „virtuell" ohne Text erkennbar ist. Reihenfolge: erst Strecke, dann Modus (so U5); Begründung: die Streckenwahl hat Eingaben, die Moduswahl ist ein Tap. Das Schwere zuerst, das Leichte als Abschluss.

**R-UI-3 — Auto: Vollbild, nicht Bottom Sheet über Karte.**
Konflikt: U2, U5 legen Frage und Reveal als Bottom Sheet über eine abgedunkelte Karte; U3, U4, U6 fordern Vollbild. Entscheidung: **Vollbild im Auto**. Grund: Spielkonzept §3.1 schließt „Karte als Darstellung" im Auto aus; eine Karte hinter dem Sheet wäre genau das, nur kleiner. Dazu U4: Der Screen ist im Auto der Spickzettel des Beifahrers, jede Fläche, die nicht Frage oder Option ist, kostet Lesbarkeit. **Bahn (Gruppe und Solo): Sheet oder Split-View über der schematischen Fahrtkarte** ist richtig, weil Radar die Karte braucht und die Fahrtkarte dort das Zuhause ist („Die Karte ist das Zuhause, die Frage ist ein Gast, der Reveal ist der Grund, warum man bleibt", U2).

**R-UI-4 — Auto: Dark Theme als Voreinstellung. Bahn: Systemeinstellung.**
U1, U2, U5, U6 fordern Dunkel im Auto (Blendfreiheit nachts, Android-Auto-Praxis); U0 war hell. Entscheidung: **Auto dunkel (mattes Anthrazit, kein reines Schwarz), Bahn folgt dem System.** Ortsschild-Gelb bleibt Akzent, es trägt auf dunklem Grund besser als auf hellem. Kipp: Wenn im Feldtest am Tag die Spiegelung auf dunklem Grund stört, wird im Auto ein Hell/Dunkel-Schalter im Zahnrad angeboten, nie ein Auto-Wechsel nach Uhrzeit (der wäre Überraschung im falschen Moment).

**R-UI-5 — Optionen beschriftet mit Ziffern 1–4, nicht A–D.** *(offen, §7)*
Konflikt: U0 nutzt Ziffern; U1, U5, U6, U7, U8, U9 nutzen Buchstaben, und auch das Spielkonzept selbst schreibt im Beispiel „C!". Entscheidung nach stärkstem Argument: **Ziffern.** Grund: Im Auto ist die Festlegung ein Zuruf ohne Blick aufs Display (§3.1). „B" und „D" sind bei Fahrgeräusch kaum zu unterscheiden, „C" und „E" ebenfalls; „eins, zwei, drei, vier" sind es immer. Zweiter Grund: Radar nummeriert die Nachbarorte ohnehin (U4: „Zeigen ersetzt Tippen"); ein Beschriftungssystem für alle Familien ist weniger zu lernen als zwei. Folge: Die Beispiele im Spielkonzept („A gegen B", „C!") sind als Ziffern zu lesen; redaktionelle Anpassung in v0.2.4.

**R-UI-6 — Multi-Select: zwei Kacheln antippen, dann „Auflösen". Kein Doppel-Tap.**
Konflikt: U1 schlägt Doppel-Tap für die zweite Option vor; U0, U4, U5 tippen zwei Kacheln und bestätigen. Entscheidung: **zwei Taps + Auflösen.** Grund: U5s eigene Regel „ein Tap = eine Aktion, kein Long-Press, kein Swipe für Kernaktionen". Ein Doppel-Tap ist eine versteckte Geste, die der Beifahrer unter Zeitdruck nicht findet. Die gewählten Kacheln zeigen einen Haken; die Spaltung ist erstklassig sichtbar, kein Fehlerzustand (U4). **Ergänzung aus U0, von keinem anderen Eingang gesehen:** Der Fall „zersplittert" braucht einen **eigenen Button „uneinig"** neben „Auflösen" (Spielkonzept §3.1). Er fehlt in sämtlichen Fremd-Mockups; ohne ihn ist der dritte Festlegungsfall nicht bedienbar.

**R-UI-7 — Festlegung im Auto: „3 · 2 · 1 → Auflösen" als eine Leiste.**
Der Beifahrer tippt die gerufene Mehrheit, dann die Leiste. Bei Einstimmigkeit genügt der Kachel-Tap, die Leiste bestätigt; bei Spaltung ist sie Pflicht. Leiste im unteren Rand, durchgehend (U4-Muster „Stopp-Leiste"). „Gleich" (Frage verschieben) und „Jetzt" (Force-Push bei GPS-Hänger, U3, U6) liegen ebenfalls unten, als kleine Textflächen links und rechts der Leiste, **nicht oben rechts** (U6), wegen Grundsatz 5.

**R-UI-8 — Reveal-Reihenfolge: Theorie, Geschichte, Urteil zuletzt, Quelle. Keine Vor-Markierung der richtigen Option.**
Konflikt: U1, U7, U8 setzen das Urteil nach oben („Richtig!", „Knapp daneben"); U0, U3, U4, U5, U6 setzen es ans Ende. U5 zeigt oben außerdem die richtige Kachel still markiert. Entscheidung: **Urteil zuletzt, als kleiner Chip; die richtige Option wird nirgends vorab hervorgehoben.** Grund: Reveal-Vertrag (§8 Nr. 5). Eine blau umrandete Kachel über dem Text verrät das Urteil, bevor jemand den ersten Satz gelesen hat; dann ist die Geschichte Nachtrag statt Belohnung. Oben steht nur die eigene Festlegung als Zitat: „Eure Theorie: 3 — vom Kloster." Bei Spaltung: beide; bei zersplittert: „Ihr wart euch komplett uneinig."

**R-UI-9 — Kein Weiter, kein Auto-Advance. Reveal bleibt stehen.**
Konflikt: U2 und U5 schlagen „Nächster Ort" als Primary mit **Auto-Advance nach 5 s** vor; U7 und U8 haben „Weiter"-Buttons im Reveal. U3, U4, U6 und U0 lehnen ab. Entscheidung: **Abgelehnt, in allen Modi.** Grund: Spielkonzept §1 („kein Weiter") und §3.1: Der Reveal bleibt stehen, bis das Gespräch verklungen ist; im Auto bringt der nächste Ort den nächsten Screen, sonst nichts. Ein Auto-Advance nach 5 s würde den Nachhall abschneiden, genau den Teil des Loops, den der Solo-Test als tragend gezeigt hat. **Schließen des Reveals:** Wisch nach unten oder Tap auf die untere Leiste „Zur Fahrtkarte". Kein „Tap irgendwo" (U3, U6), weil ein Fehltipp beim Herumzeigen den Reveal wegwischt. Nachschlag bleibt über den Pin möglich.

**R-UI-10 — Bahn: Fahrtkarte ist der Ruhezustand, „Nächster Ort: X — Frage starten" ihre größte Fläche.**
Aus U4 (Weiterschalt-Tap als größte Fläche der Pull-Ansicht, nicht als Menüpunkt) und U0 (Spine). Der Pull-Trigger ist eine Fläche über die ganze Breite am unteren Rand der Fahrtkarte, in der Bahn-Gruppe und Solo identisch. Nach dem Reveal landet man auf der Fahrtkarte, sieht den neuen Pin erscheinen (das ist der Nachhall) und tippt die nächste Frage. Das sind zwei Taps pro Runde. **Kipp:** Wenn Testpersonen die Fahrtkarte zwischen Reveal und nächster Frage als Umweg empfinden, bekommt der Reveal in der Bahn (nicht im Auto) eine zweite Leiste „Nächster Ort: X" und überspringt die Karte; dann wird der neue Pin beim nächsten Öffnen der Karte gezeigt.

**R-UI-11 — Bahn-Optionen: vertikale Liste, nicht 2×2. Ausnahme Radar.**
Konflikt: U5 Mockup 10 setzt in der Bahn 2×2-Kacheln mit Ein-Wort-Optionen („Fluss", „Bauer"). Entscheidung: **vertikale Liste in allen Familien**, weil Optionen vollständige Theorien oder Aussagen sind (Formgleichheit, §8 Nr. 3) und in 2×2 auf ein Wort gekürzt werden müssten, das die Pointe verrät oder zerstört. **Ausnahme Radar:** Dort sind die Optionen die Ziffern der Nachbarorte; vier Buttons nebeneinander unter der schematischen Karte (U6) sind richtig.

**R-UI-12 — Wer-glaubt-wem: eine Textzeile, keine Avatare, keine Namen, keine Balken.**
U2, U5, U8 zeichnen Spieler-Chips, Avatare, Prozentbalken und einen eigenen Screen „Wer liegt richtig?". Entscheidung: **abgelehnt.** Spielkonzept §3.2: Einschätzungen werden in v1 nicht aufgezeichnet, die Schicht ist rein mündlich. Namen eingeben verletzt Grundsatz 1 (Null Reibung); Balken verletzen §3.3 („keine Statistik als Belohnung"). Die UI zeigt in der Bahn-Gruppe, wenn die Schicht aktiv ist, **eine Zeile über den Optionen:** „Erst jede:r laut: welche Nummer? Dann: wer liegt richtig?" Mehr nicht.

**R-UI-13 — Leiter-Screen (U4 übernommen).**
Nur die aktuelle Stufe („Mehr als 5.000 Einwohner?"), zwei halbdisplaygroße Flächen **Mehr / Weniger**, darunter die durchgehende **Stopp-Leiste** mit der Bank („Sicher: 3.000"). Keine Übersicht aller Stufen (U8 zeigt drei Stufen gleichzeitig; das macht aus der Leiter eine Tabelle und nimmt der Stopp-Entscheidung die Spannung).

**R-UI-14 — Fahrtkarte: Farbe plus Form plus Legende, keine Bewertungs-Emojis.**
Spielkonzept §4 erlaubt „Farbe oder Emoji". U3, U6 schlagen 🤦‍♂️ für „völlig falsch" und 🎉 für Treffer vor. Entscheidung: **Farbe + Form mit Legende** (U4): Treffer, daneben, gespalten (halb/halb), uneinig. Grund: 🤦‍♂️ ist eine Bewertung und damit Rucksack (§6); die Legende statt reiner Farbcodierung ist Barrierefreiheit. Der „Ort der Fahrt" bekommt als einziger Pin eine Krone oder einen Stern, von der Gruppe gesetzt, nicht vom System.

**R-UI-15 — Fahrtbilanz: Orte · Treffer · Spaltungen. Keine Lacher.**
U3, U5, U6, U7, U8 schreiben „3 Lacher" in die Bilanz. **Abgelehnt**, Spielkonzept §4: Lacher ist kein Datenpunkt. Ersatz ist der Ort der Fahrt (Gruppe) bzw. Drei Dinge (Solo). Solo zeigt keine Spaltungen (gibt es dort nicht).

**R-UI-16 — Anschluss als eigene, optionale Sektion im Reveal.**
U5 Mockup 12 und U0 stimmen überein: Der Anschluss steht unter einer Trennlinie, mit eigener kleiner Überschrift, **nur wenn Material da ist, sonst fehlt die Sektion ganz** (keine leere Zeile, kein „kein Anschluss"). Entspricht §8 Nr. 4b (Kann-Klasse). „Auf Karte zeigen" (U5) und Linien zwischen verknüpften Pins (U3) sind **Kann** für Solo, nicht v1.

**R-UI-17 — Push-Vorankündigung als Entfernung, nicht als Countdown.**
U8 zeigt „Frage kommt in 18 Sek." und „Du hast 20 Sekunden Zeit". **Countdown abgelehnt** (Grundsatz 4, Timer ist Kahoot-Reflex). Im Auto darf der Fahrt-Leerlauf-Screen „Nächster Ort: Bendorf · 3,2 km" zeigen (U5); das ist Orientierung, kein Druck. Sekundenangaben nirgends.

**R-UI-18 — Designsystem (aus U4, U5, U6 zusammengeführt).**
- Tap-Targets: ≥ 48 × 48 px überall; **Auto-Optionen ≥ 72 px hoch**, Bahn-Optionen ≥ 56 px; 8 px Abstand zwischen Kacheln (Fehltipps bei Erschütterung).
- Typografie Auto: Ortsname 20 px, Frage 24–28 px, Optionen 20–22 px, Zeilenabstand 1,4. Bahn: Frage 22 px, Optionen 17 px, Body 15 px, Quelle 13 px. Dynamic Type: Frage und Optionen skalieren mit.
- Schriften: Fraunces (Ortsname, Frage: der Reiseführer spricht), Nunito Sans (alles andere). Serifenlos für Optionen, weil Lesegeschwindigkeit dort zählt.
- Farben: Auto Anthrazit `#1b1f24` mit heller Schrift; Ortsschild-Gelb `#f6c700` nur für aktive Zustände (gewählte Kachel, Auflösen-Leiste, Pin des aktuellen Orts); Spine-Blau `#2b4b6f` in der Bahn. Kein Giftgrün, kein Signalrot im Reveal.
- Kontrast ≥ 4,5 : 1. Screenreader-Reihenfolge: Ortsname → Frage → Optionen → Festlegung → Reveal.
- Abstände: Screen-Padding 16 px, Card-Padding 16 px, Grabber 36 × 4 px.
- Vollständige Vorlesbarkeit jedes Screens (U4, Vorbereitung auf TTS: wenn TTS kommt, ändert sich am Auto-Frage-Screen nur die Pausen-Markierung, am Layout nichts).

---

## 3. Rulings — Abgelehnt (Kurzliste mit Grund)

| Vorschlag | Quelle | Grund |
|---|---|---|
| Auto-Advance nach 5 s | U2, U5 | §1 kein Weiter; schneidet den Nachhall ab (R-UI-9) |
| „Weiter" / „Weiter zur Station" im Reveal | U7, U8 | dito |
| Urteil zuerst, „Richtig!" grün oben | U1, U7, U8 | Reveal-Vertrag §8 Nr. 5 (R-UI-8) |
| Richtige Kachel im Reveal still vormarkiert | U5 | verrät das Urteil vor der Geschichte (R-UI-8) |
| Doppel-Tap für zweite Option | U1 | versteckte Geste; „ein Tap = eine Aktion" (R-UI-6) |
| Bottom Sheet über Karte im Auto | U2, U5 | §3.1 keine Karte im Auto (R-UI-3) |
| 2×2-Kacheln in der Bahn | U5 | Optionen sind Sätze, nicht Wörter (R-UI-11) |
| Avatare, Namen, Prozentbalken, eigener Wer-liegt-richtig-Screen | U2, U5, U8 | §3.2 nicht aufgezeichnet; Null Reibung (R-UI-12) |
| „3 Lacher" in der Bilanz | U3, U5, U6, U7, U8 | §4 kein Datenpunkt (R-UI-15) |
| Bewertungs-Emojis auf Pins | U3, U6 | Rucksack §6 (R-UI-14) |
| Countdown „Frage kommt in 18 Sek.", „20 Sekunden Zeit" | U8 | Timer (R-UI-17) |
| „Später"-Icon zum Überspringen im Auto | U2 | „Gleich"-Tap deckt den Fall; ein Skip ohne Reveal erzeugt Rucksack |
| Force-Push oben rechts | U6 | Bedienelemente unten (Grundsatz 5) |
| Tap irgendwo schließt den Reveal | U3, U6 | Fehltipp beim Herumzeigen (R-UI-9) |
| Leiter mit allen Stufen sichtbar | U8 | nimmt der Stopp-Entscheidung die Spannung (R-UI-13) |
| „Neustart"-Button am Ende | U7, U8 | Grundsatz 9 |
| Antwortkacheln „halbe Breite, Drittel Höhe" | U6 | vier Optionen plus Frage passen dann nicht auf einen Screen |
| Fortschrittsbalken (dünne Linie oben) | U2, U5 | eine Textzeile „Ort 4 von 12" reicht; ein Balken ist ein Zähler, der sich füllt |
| Hell-Theme-Pflicht im Auto | U0 (eigene Skizze) | R-UI-4 |

---

## 4. Screen-Inventar v0.1 (konsolidiert)

| # | Screen | Modi | Kerninhalt | Bedienung (unten) |
|---|---|---|---|---|
| S1 | Start | alle | Wortmarke, stille Streckenvorschau | „Fahrt starten" (56 px, voll breit), Zahnrad oben rechts |
| S2 | Streckenquelle | alle | Sheet mit 3 Karten: GPS / Geplant / Gewürfelt | ein Tap |
| S2a | Geplante Route | alle | Von / Nach, Tausch, Vorschau „14 Orte · 189 km" | „Route starten" |
| S2b | Gewürfelt | alle | Raum-Chips, Würfel-Button ⌀ 140 px | Würfeln, Neu mischen |
| S3 | Modus | alle | 3 Karten (R-UI-1) | ein Tap, danach nie wieder |
| S4 | Auto: Leerlauf | Auto | dunkel, „Nächster Ort: X · 3,2 km", „Ort 4 von 12" | „Gleich" / „Jetzt" |
| S5 | Auto: Frage | Auto | Ortsname, Frage, 4 Kacheln 1–4 ≥ 72 px, Multi-Select-Haken | „uneinig" · „3·2·1 → Auflösen" · „Gleich" |
| S5L | Auto: Leiter | Auto | Stufe, Mehr / Weniger | Stopp-Leiste mit Bank |
| S6 | Reveal | alle | Eure Theorie (Zitat) → Geschichte → Urteil-Chip → Quelle → [Anschluss] | Wisch ↓ oder „Zur Fahrtkarte" |
| S7 | Bahn: Fahrtkarte | Bahn-G, Solo | Spine mit Pins (Farbe + Form + Legende), „Ort 4 von 12" | „Nächster Ort: X — Frage starten" (größte Fläche) |
| S8 | Bahn: Frage | Bahn-G, Solo | Sheet über S7, Frage, Liste 1–4 ≥ 56 px; Gruppe: Wer-glaubt-wem-Zeile optional | „Auflösen" (Gruppe mit Multi-Select) |
| S8R | Bahn: Radar | Bahn-G, Solo | schematische Karte mit Nachbarorten 1–4 oben | 4 Ziffern-Buttons nebeneinander |
| S9 | Bahn: Bingo | Bahn-G, Solo | eigener Tab neben S7, nur auf ortsarmen Strecken | Felder tippen |
| S10 | Fahrtende | alle | Karte mit allen Pins, Bilanz (R-UI-15), Ort der Fahrt (Gruppe) / Drei Dinge (Solo), Große Fahrtfrage optional | „Teilen" · „Schließen" gleich groß |

Im Auto gibt es außer S4, S5, S5L, S6 und S10 nichts. Die Fahrtkarte ist im Auto erst am Ende sichtbar (§3.1).

---

## 5. Kipp-Kriterien für die UI (Feldtest-Fragen)

- **KU1 Beifahrer-Blick:** Braucht der Beifahrer mehr als einen Blick, um nach dem Zuruf zu tippen? Dann sind Kacheln oder Schrift zu klein, nicht die Mechanik falsch.
- **KU2 Fehltipp:** Mehr als ein Fehltipp pro zehn Orte im fahrenden Auto → Kachelhöhe und Abstand hoch, Auflösen-Leiste weiter weg von den Kacheln.
- **KU3 Zähler als Druck:** Wird „Ort 4 von 12" als Zeitdruck genannt? Dann entfällt die Zeile im Auto; in der Bahn bleibt sie, weil der Spine sie ohnehin zeigt.
- **KU4 Spiegelung:** Dunkles Display bei Tag unlesbar → Hell/Dunkel-Schalter im Zahnrad (R-UI-4).
- **KU5 Umweg Fahrtkarte:** Zwei Taps zwischen Reveal und nächster Frage werden als Umweg genannt → R-UI-10 Kipp.
- **KU6 Ziffern-Zuruf:** Rufen Testpersonen trotz Ziffern-Beschriftung Buchstaben oder Inhalt („das Kloster!")? Dann ist die Beschriftung Nebensache und der Beifahrer tippt nach Inhalt; Ziffern bleiben trotzdem, schaden nicht.

---

## 6. Was die UI-Runde über den Papier-Feldtest sagt

Zwei Eingänge (U4, U5) weisen darauf hin, und das Protokoll aus GEOSYNC 019 bestätigt es: Die Papierkarten des Solo-Tests waren bereits der Auto-Frage-Screen (ein Blatt, Frage vorne, Reveal hinten). Für den zweiten Solo-Test und den Bahn-Gruppen-Tisch werden die Karten im Smartphone-Ausschnitt gedruckt (S5 vorne, S6 hinten, Urteil-Chip unten, Quelle klein). Damit wird mit der Mechanik auch die Reveal-Reihenfolge (R-UI-8) getestet, ohne dass eine Zeile Code existiert.

---

## 7. Offen für Mike

1. **R-UI-5 Ziffern statt Buchstaben.** Ändert die Beispiele im Spielkonzept (redaktionell, v0.2.4). Stärkstes Argument ist der Zuruf im Auto; wenn du Buchstaben aus anderen Gründen willst (Gewohnheit aus QuizAway v5, Transfer-Konzept), sag es, dann Buchstaben überall und Radar bleibt die einzige Ziffern-Stelle.
2. **R-UI-4 Dunkel im Auto.** Die eigene Skizze war hell; die Reviews haben mich umgestimmt. Freigabe oder Einspruch.
3. **R-UI-10 zwei Taps in der Bahn.** Ich halte den Umweg über die Fahrtkarte für den Nachhall-Moment, aber das ist Hypothese; Kipp KU5 ist dafür da.

Nach Freigabe: HTML-Skizze auf v0.1 ziehen (dunkler Auto-Screen, Leiter-Screen, „uneinig"-Button, Radar-Buttons, Legende), danach die Papier-Screens für Test 2.
