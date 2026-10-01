# QuizAway — PC-Prüfung UI-Konzept Reise-Modus v0.1

**Datum:** 2026-10-01 · **Geprüft:** `quizaway-ui-konzept-reise-modus-v0.1-2026-10-01.md` (GEOSYNC 021, Synthese der UI-Runde vom Spaziergang) und die HTML-Skizze „QuizAway Reise-Modus Screens" (Eingang U0) · **Gegen:** Spielkonzept v0.2.4, Kartensatz Fassung 2, Transfer-Konzept v1.1 · **Nicht geprüft:** die Eingänge U1–U9 selbst; sie liegen hier nicht vor.

**Urteil:** Die Synthese ist in ihrer Hauptlinie richtig: Das Spielkonzept entscheidet, nicht die Mehrheit, und alle Ablehnungen in §3 sind vom Spielkonzept gedeckt. Sechs Punkte halten der Prüfung nicht stand oder sind unbestimmt (U1–U6); sie betreffen den nächsten Test, die Textlängen, die Festlegung im Auto, die Fahrtkarte im Auto, die Leiter und die zwei Taps in der Bahn. Von Mikes drei offenen Punkten ist einer klar (Ziffern), einer nicht per Ruling entscheidbar (Dunkel), einer eine bewusste Abweichung vom Spielkonzept (zwei Taps).

---

## A. Was stimmt

- **Methode:** „Stärkstes Argument, nicht Mehrheit", Spielkonzept als Instanz. Die zwölf Mehrheits-Vorschläge, die abgelehnt sind (Auto-Advance, Weiter-Knopf, Urteil zuerst, Lacher, Avatare, Countdown, Bewertungs-Emojis und weitere), widersprechen dem Spielkonzept tatsächlich.
- **Der Fund „uneinig":** Der dritte Festlegungsfall fehlt in allen Fremd-Entwürfen und ist in v0.1 drin.
- **Pin-Zustände ohne Theorie-Urteil:** Die Skizze unterschied noch „daneben mit Theorie" und „daneben ohne". Die App kann das nicht wissen; v0.1 hat es richtig entfernt.
- **Entfernung statt Countdown, Farbe plus Form plus Legende, keine Lacher in der Bilanz, Wer-glaubt-wem als eine Textzeile:** alle im Sinn des Spielkonzepts.

---

## B. Befunde

### U1. Papier-Screens gehören nicht in den zweiten Solo-Test (§6, Status-Block)

v0.1 will die Karten für den zweiten Solo-Test „im Smartphone-Ausschnitt" drucken, mit neuer Reveal-Reihenfolge. Der zweite Solo-Test soll aber eine Frage beantworten: Entsteht bei den Karten 3 und 10 eine Theorie, wenn die Lüge nicht mehr wiedererkannt werden kann? Dafür bleiben acht Karten bewusst unverändert. Ändert sich zugleich Format, Schriftgröße und Reihenfolge der Rückseite, ist kein Unterschied mehr zuzuordnen. Die Papier-Screens sind ein eigener Test (dritte Person oder Bahn-Gruppe).

### U2. „Im Auto scrollt kein Screen" gilt nur mit einer Längenregel, die es noch nicht gibt (§1 Nr. 2, R-UI-18)

Gemessen im Browser mit den Schriften und Maßen aus R-UI-18 (Fraunces, Nunito Sans, Zeilenabstand 1,4, Kacheln ≥ 72 px, Rand 16 px, eine Leiste 56 px) und den Texten des Kartensatzes. Höhe des Inhalts in px bei 360 px Breite:

| Frage-Screen | Frage 24 / Option 20 px | Frage 28 / Option 22 px |
|---|---|---|
| Karte 3 (drei Aussagen) | 494 | 522 |
| Karte 1 Umkirch | 557 | 591 |
| Karte 4 Zähringen (Optionen mit 7–8 Wörtern) | 578 | 677 |
| Karte 4, Frage auf 24 Wörter verlängert (Regelgrenze) | 746 | 912 |

| Reveal-Screen (Zitat, Geschichte, Urteil, Quelle, Anschluss, Leiste) | 16 px | 18 px | 20 px | 22 px |
|---|---|---|---|---|
| Karte 1 (45 Wörter) | 425 | 452 | 508 | 571 |
| Karte 4 (67 Wörter) | 497 | 612 | 686 | 767 |
| Karte 5 (45 + Anschluss 30) | 582 | 678 | 755 | 872 |
| Karte 3 (82 Wörter) | 593 | 668 | 748 | 901 |
| Karte 10 (106 Wörter) | 707 | 848 | 946 | 1117 |

Zur Einordnung: Ein Telefon mit 360 × 800 px hat nach Abzug der Systemleisten etwa 730–750 px, ein kleines mit 360 × 640 etwa 600 (Schätzung, nicht gemessen). Bei 390 px Breite sind die Werte 20–60 px kleiner.

- **Frage:** Typische Karten passen. An der Grenze der Redaktionsregel (25 Wörter Frage, 8 Wörter je Option) passt der Screen bei 24/20 px gerade noch und bei 28/22 px nicht mehr.
- **Reveal:** v0.1 nennt für den Reveal im Auto keine Schriftgröße. Bei 20 px (Vorlesegröße) passt er bis etwa 65–70 Wörter einschließlich Anschluss. Vier der zehn handgeschriebenen Karten liegen darüber (3, 5, 6, 10), eine genau an der Grenze (9).
- **Die Regel dahinter fehlt im Spielkonzept:** Es begrenzt Frage und Optionen, aber nicht die Auflösung. Die Geschichten im Kartensatz haben 31–106 Wörter, die Anschlüsse bis 39. 106 Wörter sind vorgelesen rund 45 Sekunden; die ganze Auto-Runde soll 60 dauern. Die „50 bis 90 Wörter" im Karten-Prompt und im Runde-5-Briefing habe ich selbst gesetzt; sie stehen in keinem freigegebenen Dokument.
- **Systemschrift:** R-UI-18 will, dass Frage und Optionen mit der Systemschriftgröße wachsen; die Skizze sagt das Gegenteil („Schriftgröße folgt dem Modus, nicht der Systemeinstellung"). Mit vergrößerter Systemschrift ist „kein Scrollen" nicht zu halten. Eines von beiden muss weichen.

Vorschlag: Auflösung im Auto höchstens 70 Wörter einschließlich Anschluss, Schrift 20 px, Frage-Screen auf 24/20 px festlegen. Das hält den Screen auf üblichen Telefonen ohne Scrollen und die Vorlesezeit unter 30 Sekunden.

### U3. Die Festlegung im Auto ist in R-UI-7 nicht widerspruchsfrei

- „Bei Einstimmigkeit genügt der Kachel-Tap, die Leiste bestätigt; bei Spaltung ist sie Pflicht." Löst der erste Kachel-Tap schon auf, kann nie eine zweite Kachel gewählt werden. Bestätigt die Leiste, kostet auch die einstimmige Antwort zwei Taps. Ehrlich gezählt: einstimmig zwei Taps, gespalten drei, uneinig einer. Das ist vertretbar und schützt vor Fehltipps (der Kachel-Tap ist bis zur Leiste korrigierbar), sollte aber so dastehen. Das Spielkonzept sagt „so schnell wie die Einzelwahl"; das stimmt dann, weil beide Wege die Leiste brauchen.
- **Beschriftung „3 · 2 · 1 → Auflösen":** Das „3-2-1" ruft der Beifahrer, bevor getippt wird. Auf der Leiste, die nach dem Tippen kommt, steht es an der falschen Stelle.
- **„Gleich" und „Jetzt":** „Jetzt" (nächsten Ort sofort auslösen) hat nur auf dem Leerlauf-Screen einen Sinn, „Gleich" (Frage zurückstellen) nur auf dem Frage-Screen. Das Inventar führt auf S4 beide und R-UI-7 legt beide neben die Leiste.
- **„Gleich" neben „Auflösen":** Ein Fehltipp wirft die Frage zurück, nachdem alle gerufen haben. Einfache Abhilfe: „Gleich" verschwindet, sobald eine Kachel gewählt ist.

### U4. R-UI-3 liest §3.1 zu weit: Die Fahrtkarte gilt auch im Auto

v0.1 begründet Vollbild im Auto damit, dass §3.1 die „Karte als Darstellung" ausschließt, und folgert: „Die Fahrtkarte ist im Auto erst am Ende sichtbar." §3.1 meint dort die Radar-Karte. Die Fahrtkarte steht in §4 unter „alle Modi", und der Nachschlag über den Pin (§1 Schritt 5) setzt sie voraus. Folgen in v0.1:

- R-UI-9 sagt „Nachschlag bleibt über den Pin möglich"; im Auto gibt es während der Fahrt keinen Pin.
- S6 hat für alle Modi die Leiste „Zur Fahrtkarte"; im Auto gibt es dieses Ziel nicht.
- Naheliegend ist: Vollbild für Frage und Reveal bleibt, der Leerlauf-Screen S4 ist die Fahrtkarte (Linie, Pins, nächster Ort).

Im Inventar fehlen außerdem: der Tap „Fahrt abschließen" (§4), der Wechsel auf geplante Route bei GPS-Verlust (§1a), „Fahrt fortsetzen" auf dem Start, das Pin-Detail, die Leiter in Bahn und Solo (S5L gibt es nur fürs Auto) und die Frage, ob Solo nach dem Kachel-Tap ein „Festlegen" braucht (die Skizze hat es, v0.1 schweigt).

### U5. Die Leiter in R-UI-13 bringt eine Mechanik mit, die das Spiel nicht hat

„Mehr / Weniger" plus „Stopp-Leiste mit der Bank (Sicher: 3.000)" ist das Muster eines Spiels mit Einsatz: Man stoppt, um Gewonnenes zu sichern. Im Reise-Modus gibt es nichts zu sichern. Ohne Einsatz sind „Weniger" und „Stopp" dieselbe Aussage. Die einzige getestete Leiter (Karte 5: „Höher als 400, 600, 800, 1.000 m? Wo steigst du aus?") zeigte alle Stufen auf einmal und erzeugte eine begründete Theorie. v0.1 lehnt genau diese Darstellung ab, mit der Begründung „Spannung der Stopp-Entscheidung".

Die Unschärfe liegt im Spielkonzept selbst („Mehr/Weniger-Sequenz mit Abbruch"). Vor dem Screen braucht es dort einen Satz, was eine Stufe ist. Vorschlag nach der Karte, die funktioniert hat: je Stufe „höher" oder „hier steige ich aus"; der Ausstieg ist die Antwort.

### U6. Zwei Taps in der Bahn weichen vom Spielkonzept ab (R-UI-10)

§1 Schritt 5 sagt: zwischen zwei Orten „ein Tap, großes Ziel". R-UI-10 braucht zwei Handlungen (Reveal schließen, dann Frage starten). v0.1 legt das als offen vor, nennt die Abweichung aber nicht. Als Hypothese mit Kipp KU5 ist es vertretbar; dann gehört der Satz im Spielkonzept angepasst. Daneben widersprechen sich Grundsatz 2 („getrennte, bildschirmfüllende Zustände") und R-UI-3 („Bahn: Sheet oder Split-View über der Fahrtkarte").

### U7. Ziffern statt Buchstaben (R-UI-5): ja, mit einer Einschränkung

- Der Kartensatz nutzt schon Ziffern („Richtig war 2"); der erste Feldtest lief damit. Nur die Beispiele im Spielkonzept sagen noch „C!".
- Die Begründung „eins, zwei, drei, vier sind es immer" stimmt so nicht: „zwei" und „drei" sind im Deutschen das bekannte Verwechslungspaar, deshalb sagt man am Funk „zwo". Buchstaben sind trotzdem schlechter (B, C, D reimen sich alle drei).
- Folge: Ziffern, und der Beifahrer liest „zwo". KU6 sollte gezielt auf zwei/drei achten.

### U8. Dunkel im Auto (R-UI-4) ist per Argument nicht zu entscheiden

- Für die Nacht trägt die Begründung (Blendung der fahrenden Person).
- Für den Tag spricht die Forschung zur Lesbarkeit eher für dunkle Schrift auf hellem Grund, besonders bei kleiner Schrift (Piepenbrock, Mayr und Buchner; der Vorteil wird mit der helleren Fläche und der engeren Pupille erklärt). Lange Fahrten sind überwiegend Tagfahrten.
- v0.1 schließt den Wechsel „nach Uhrzeit" aus, weil er überrascht. Ein Wechsel nur beim Start einer Fahrt, nach der Systemeinstellung, überrascht nicht; die Skizze hatte genau das.
- Technische Folge, die v0.1 nicht nennt: Eine Web-App bekommt die Position nur, solange sie im Vordergrund läuft und der Bildschirm an ist. Im Auto leuchtet der Leerlauf-Screen also die ganze Fahrt. Nachts muss gerade dieser Screen sehr dunkel sein.
- Das lässt sich in fünf Minuten ansehen: Skizze auf dem Telefon öffnen (sie folgt der Systemeinstellung), im stehenden Auto mittags und abends beide Fassungen vergleichen.

### U9. Was ist ein Treffer, wenn die Gruppe gespalten war? (R-UI-14, R-UI-15)

Die Pins kennen „Treffer, daneben, gespalten, uneinig", die Bilanz „Orte, Treffer, Spaltungen". Offen ist, ob eine Spaltung, bei der eine Hälfte richtig lag, als Treffer zählt. Das Spielkonzept sagt dazu nichts. Einfachste Zählung: Treffer ist nur einstimmig richtig; Spaltung und uneinig sind eigene Zustände.

### U10. Designsystem (R-UI-18): Maße ohne Herkunft, drei Sachpunkte

- **Herkunft:** Kein Maß trägt, woher es kommt. Die 48 px entsprechen den üblichen Plattform-Richtlinien. Für die 72 px gibt es eine nahe Referenz: Googles Richtlinie für Apps im Auto verlangt 76 × 76 dp, allerdings für die fahrende Person; für Beifahrer gibt es meines Wissens keine Vorgabe.
- **Haptik:** „Ersetzt den Spielstein" setzt Vibration voraus. Die Vibrations-Schnittstelle des Browsers fehlt auf iPhone und iPad als Standard; es gibt Umwege, deren Verlässlichkeit ich nicht geprüft habe. Vor dem Festschreiben auf dem iPad ausprobieren.
- **Kontrast:** nachgerechnet. Gelb `#f6c700` auf Anthrazit 10,3 : 1 und Schwarz auf Gelb 10,7 : 1 sind gut. Gelb auf hellem Grund hat 1,5 : 1 und geht nur als Fläche mit schwarzer Schrift. Das Spine-Blau `#2b4b6f` hat auf Anthrazit 1,8 : 1; folgt die Bahn dem System, braucht das dunkle Thema ein anderes Blau (die Skizze hat dafür `#8fb4dc`).
- **Schrift:** Fraunces für Ortsname und Frage ist eine Geschmacksentscheidung mit einer Vermutung zur Lesbarkeit beim Vorlesen, kein Beleg.
- **Familie:** v0.1 nennt weder das Farbsystem von MixMi (acht umschaltbare Designs) noch das Aussehen von QuizAway v5 (dunkel, Bernstein, Bebas Neue). Ein eigenes Aussehen für den Reise-Modus ist vertretbar, sollte aber Mikes Entscheidung sein und nicht nebenbei entstehen.

### U11. Kleineres

- Grundsatz 1 spricht von „einer Entscheidung (Modus)"; mit R-UI-2 sind es zwei (Strecke, dann Modus). „Danach nie wieder gefragt" kann nur „in dieser Fahrt" heißen.
- S9 Bingo als „eigener Tab" widerspricht „keine Tabs" aus der Skizze.
- R-UI-16 verweist auf §8 Nr. 4b (Kann-Klasse). „Nur wenn Material da ist" gilt für beide Anschluss-Klassen (§1 Schritt 4d); 4b ist nur der Erzählanschluss.
- Grundsatz 6 verweist auf „K9"; in v0.2.4 heißt das „Fahrer-Ausschluss".
- Grundlage ist „v0.2.3 (freigegeben)". Freigegeben war v0.2.2; am PC gibt es inzwischen v0.2.4. Die für Ziffern angekündigte „redaktionelle Anpassung in v0.2.4" wäre also v0.2.5.
- Beim Hochziehen der Skizze auf v0.1 zusätzlich zu entfernen: der Link „Noch eine Frage zu Umkirch?" (ein Angebot, das §6 ausschließt), die Randleiste „Gundelfingen kommt in 6 km" (eine Vorschau, kein Anschluss), das große grüne Urteil.

### U12. Was die Runde nicht behandelt hat

Übelkeit beim Lesen im Auto; Lesbarkeit von mehreren Tischseiten (MixMi dreht dafür ein Fenster um 180°); Format und Inhalt des Teilen-Bilds; Maße mit Herkunftsangabe. Das waren Fragen aus dem Runde-5-Briefing vom PC, das die Runde nicht kannte. Als Ganzes ist das Briefing überholt; als kurze Nachfrage mit diesen vier Punkten bleibt es brauchbar.

---

## C. Zu Mikes drei offenen Punkten (§7) und drei weiteren

1. **Ziffern (R-UI-5):** Ja. Beifahrer liest „zwo" (U7).
2. **Dunkel im Auto (R-UI-4):** Nicht per Ruling. Start nach Systemeinstellung, kein Wechsel während der Fahrt, und vorher im Auto ansehen (U8).
3. **Zwei Taps in der Bahn (R-UI-10):** Als Hypothese mit KU5 annehmen und die Abweichung von §1 Schritt 5 im Spielkonzept vermerken (U6).
4. **Papier-Screens:** nicht im zweiten Solo-Test (U1).
5. **Auflösung im Auto:** höchstens 70 Wörter einschließlich Anschluss als Redaktionsregel ins Spielkonzept (U2).
6. **Leiter:** „höher / hier steige ich aus", kein Stopp mit Bank (U5).

**Entschieden (Mike, 2026-10-01): alle sechs „OK".** Umsetzung: Spielkonzept v0.2.5 (Anhang E), UI-Konzept v0.2, Karten-Prompt v0.3 (70 Wörter), Nachfrage an die Reviewpartner mit zehn Fragen.

**Zum Ablauf:** Am Handy und am PC wird am selben Konzept gearbeitet. Das Handy kennt v0.2.4, Kartensatz Fassung 2 und die Stufe-2-Vorbereitung erst nach einem Commit im LernApp-Repo (der den Drive-Sync auslöst). Bis dahin entstehen dort Dokumente auf dem Stand v0.2.3.

*Ende Prüfbericht.*
