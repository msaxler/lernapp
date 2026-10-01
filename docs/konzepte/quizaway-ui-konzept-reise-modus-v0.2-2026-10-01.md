# QuizAway — UI-Konzept Reise-Modus v0.2

Synthese der UI-Review-Runde 1 (Smartphone-Oberfläche, Best Practice), nachgeführt nach der PC-Prüfung. Gilt für das Spielkonzept Reise-Modus **v0.2.5**. Das Spielkonzept ist die Instanz; wo ein UI-Vorschlag ihm widerspricht, verliert der Vorschlag, auch wenn er mehrheitlich kam.

## Status-Block

| | |
|---|---|
| **Repo / Pfad** | lernapp / docs/konzepte |
| **Version** | v0.2 (2026-10-01). v0.1 (GEOSYNC 021) plus PC-Prüfung `quizaway-ui-konzept-v0.1-pruefung-pc-2026-10-01.md` (U1–U12) plus sechs Entscheide Mikes („OK" zu Abschnitt C). |
| **Status** | Entwurf. Die drei offenen Punkte aus v0.1 §7 und die vier aus der ersten Fassung von v0.2 §7 sind entschieden (Nachtrag am selben Tag: R-UI-14, 15, 18, 19, S8). Offen ist nur noch, was Ansehen, Nachfrage und Test klären (§7). Keine Implementierungsfreigabe. |
| **Grundlage** | Spielkonzept Reise-Modus v0.2.5, Kartensatz Freiburg Fassung 2, Feldtest-Protokoll Solo Freiburg |
| **Eingänge** | U0 eigene HTML-Skizze „QuizAway Reise-Modus Screens"; U1–U7 sieben Text-Konzepte der Review-Partner; U8 Screen-Collage; U9 gerendertes Einzelbild. Die Eingänge liegen nur am Handy vor; die PC-Prüfung hat die Synthese geprüft, nicht die Eingänge. |
| **Methode** | Stärkstes Argument, nicht Mehrheit. Jedes Ruling nennt den Konflikt, die Entscheidung, den Grund und, wo nötig, das Kipp-Kriterium. |
| **Geändert gegenüber v0.1** | Grundsätze 1, 2, 6, 7; R-UI-3, 4, 5, 7, 9, 10, 13, 14, 15, 16, 18; neu R-UI-19; Inventar §4; §6; §7. Unverändert: R-UI-1, 2, 6, 8, 11, 12, 17 und die Ablehnungen in §3. |
| **Screens** | `skizzen/quizaway-reise-modus-screens-v0.2.html`, zum Durchtippen in Originalgröße, Hell/Dunkel umschaltbar; veröffentlicht unter https://claude.ai/artifact/1MFUd2u45eyLXhGwTGD4n2. Sieben Screens: Auto-Leerlauf, Auto-Frage, Leiter, Auflösung, Solo-Fahrtkarte, Solo-Radar, Fahrtende. Geprüft bei 360 × 740 px: Kein Auto-Screen scrollt. Befund dabei: Mit der Ziffer vor dem Text laufen Optionen mit acht Wörtern bei 20 px auf drei Zeilen; der Frage-Screen hatte nur 19 px Luft. |
| **Nächster Schritt** | Hell und Dunkel im Auto ansehen → Papier-Screens als eigener Test (nicht im zweiten Solo-Test) |

---

## 1. Was alle Eingänge gemeinsam tragen (ohne Ruling)

1. **Kein Login, kein Onboarding, kein Hamburger-Menü.** Die App öffnet auf dem Startschirm. Je Fahrt zwei Entscheidungen (Strecke, dann Situation), danach wird in dieser Fahrt nichts mehr gefragt. Einstellungen hinter einem Zahnrad nur auf dem Startschirm.
2. **Ein Screen, ein Gedanke.** Frage und Auflösung sind getrennte Zustände. Im Auto füllen sie den Bildschirm, und kein Screen scrollt; das gilt mit den Maßen und Textlängen aus R-UI-18. In der Bahn liegen sie als Blatt über der Fahrtkarte (R-UI-3), und nur die Fahrtkarte scrollt.
3. **Die ganze Fläche ist der Button.** Optionen sind Kacheln, keine Radiobuttons, keine Checkboxen.
4. **Kein Timer, kein Score, keine Punktewolke, keine Streak.** Fortschritt nur als dezente Zeile „Ort 4 von 12".
5. **Bedienelemente im unteren Drittel.**
6. **Animationen ≤ 200 ms, nichts blinkt, nichts pulsiert im Auto** (Fahrer-Ausschluss, Spielkonzept §3.1). Einzige Bewegung: Die Auflösung gleitet von unten hoch.
7. **Haptik, wo das Gerät sie hergibt:** kurzer Impuls bei Antwort-Tap und beim Erscheinen der Auflösung. Auf iPhone und iPad stellt der Browser die Vibration nicht als Standard bereit; kein Ablauf darf von ihr abhängen.
8. **Teilen = Bild über System-Share.** Kein eigener Export-Dialog.
9. **Kein „Nochmal spielen" am Fahrtende.** „Schließen" führt zum Start.
10. **Quelle sichtbar, aber klein**, unter jeder Auflösung.

---

## 2. Rulings

**R-UI-1 — Situation wählen: drei Karten, nicht zwei.** *(unverändert)*
Drei Karten, weil Bahn-Solo einen eigenen Takt hat (Ortsliste als Vorschau, Drei Dinge am Ende, keine Mehrfachauswahl). Die Formulierung bleibt offen (Spielkonzept §3). Arbeitsfassung: „Jemand fährt" / „Wir sitzen zusammen" / „Ich bin allein unterwegs".

**R-UI-2 — Streckenquelle: drei Karten in einem Blatt, dann fertig.** *(unverändert)*
„Echte Fahrt (GPS)" / „Geplante Route" / „Gewürfelt". Geplante Route ist genau ein Screen „Von … / Nach …". Gewürfelt: Raum-Chips und ein großer Würfel-Button. Gewürfelte Strecke auf der Fahrtkarte gestrichelt. Reihenfolge: erst Strecke, dann Situation.

**R-UI-3 — Auto: Frage und Auflösung im Vollbild; die Fahrtkarte ist der Leerlauf.** *(berichtigt)*
Vollbild für Frage und Auflösung im Auto bleibt: Der Screen ist der Spickzettel des Beifahrers, jede Fläche, die nicht Frage oder Option ist, kostet Lesbarkeit. Die Begründung aus v0.1 („§3.1 schließt die Karte im Auto aus") traf aber nur die Radar-Karte. Die Fahrtkarte gilt in allen Modi (Spielkonzept §4), und der Nachschlag über den Pin (§1 Schritt 5) setzt sie voraus. **Der Leerlauf-Screen im Auto ist deshalb die schematische Fahrtkarte** (Linie, Pins, nächster Ort mit Entfernung). Bahn (Gruppe und Solo): Frage und Auflösung als Blatt über der Fahrtkarte.

**R-UI-4 — Hell oder Dunkel: beim Start der Fahrt nach Systemeinstellung, kein Wechsel während der Fahrt.** *(entschieden, Mike)*
v0.1 wollte das Auto immer dunkel. Für die Nacht trägt das (Blendung der fahrenden Person). Für den Tag spricht die Lesbarkeitsforschung eher für dunkle Schrift auf hellem Grund, besonders bei kleiner Schrift, und lange Fahrten sind überwiegend Tagfahrten. Entscheidung: Die App übernimmt beim Start der Fahrt die Systemeinstellung und wechselt während der Fahrt nicht; ein Schalter im Zahnrad. **Vor einer weiteren Festlegung wird es angesehen:** Skizze auf dem Telefon, im stehenden Auto, mittags und abends, beide Fassungen. Zwei Bedingungen gelten unabhängig vom Ergebnis: Beide Fassungen sind gleichwertig gestaltet, und der Leerlauf-Screen ist in der dunklen Fassung sehr dunkel, denn er leuchtet die ganze Fahrt (eine Web-App bekommt die Position nur im Vordergrund bei eingeschaltetem Bildschirm).

**R-UI-5 — Optionen mit Ziffern 1–4; im Auto „zwo".** *(entschieden, Mike)*
Ziffern statt Buchstaben; der Kartensatz nutzt sie schon. B, C und D reimen sich und sind im Fahrgeräusch nicht zu trennen. Auch Ziffern sind nicht von selbst eindeutig: „zwei" und „drei" sind das bekannte Verwechslungspaar, deshalb liest und ruft man „zwo". Radar nummeriert die Nachbarorte ohnehin; es gibt damit ein Beschriftungssystem für alle Familien.

**R-UI-6 — Mehrfachauswahl: zwei Kacheln antippen, dann „Auflösen". Kein Doppel-Tap.** *(unverändert)*
Gewählte Kacheln zeigen einen Haken; die Spaltung ist erstklassig sichtbar, kein Fehlerzustand. Der Fall „zersplittert" hat einen eigenen Button „uneinig" (Spielkonzept §3.1); er fehlt in sämtlichen Fremd-Entwürfen.

**R-UI-7 — Festlegung im Auto: Kachel, dann „Auflösen".** *(neu gefasst)*
v0.1 schrieb, bei Einstimmigkeit genüge der Kachel-Tap. Das schließt die Mehrfachauswahl aus: Löst der erste Tap schon auf, kann keine zweite Kachel gewählt werden. Es gilt:
- **Jede Festlegung endet mit der Leiste „Auflösen".** Einstimmig oder Mehrheit: eine Kachel, dann die Leiste (zwei Taps). Patt: zwei Kacheln, dann die Leiste (drei Taps). Zersplittert: „uneinig" (ein Tap, löst sofort auf).
- Der Kachel-Tap ist bis zur Leiste korrigierbar. Das ist der Schutz gegen Fehltipps bei Erschütterung.
- **Die Leiste heißt „Auflösen".** Das „3-2-1" ruft der Beifahrer vor dem Zuruf; es steht als Hinweiszeile über den Kacheln, nicht auf der Leiste.
- **Untere Reihe des Frage-Screens, zwei Zustände:** Solange keine Kachel gewählt ist: „Gleich" und „uneinig". Sobald eine Kachel gewählt ist: nur „Auflösen". So liegt „Gleich" nie neben „Auflösen", und ein Fehltipp kann die Frage nicht zurückwerfen, nachdem alle gerufen haben.
- **„Jetzt"** (nächsten Ort sofort auslösen) steht nur auf dem Leerlauf-Screen, unten.

**R-UI-8 — Reihenfolge der Auflösung: Theorie, Geschichte, Urteil zuletzt, Quelle. Keine Vor-Markierung der richtigen Option.** *(unverändert)*
Oben steht nur die eigene Festlegung als Zitat, mit dem Wortlaut der Option: „Eure Theorie: 3 — Hier wurde eine Kirche komplett umgebaut." Bei Patt beide; bei zersplittert: „Ihr wart euch komplett uneinig." Das Urteil steht am Ende als kleiner Chip.

**R-UI-9 — Kein Weiter, kein Auto-Advance. Die Auflösung bleibt stehen.** *(ergänzt)*
Abgelehnt in allen Modi (Spielkonzept §1). Schließen: Wisch nach unten oder die untere Leiste. **Im Auto** führt die Leiste zum Leerlauf (Fahrtkarte); kommt vorher der nächste Ort, ersetzt seine Frage die Auflösung. **In der Bahn** führt sie zur Fahrtkarte. Kein „Tap irgendwo". Nachschlag über den Pin, in allen Modi.

**R-UI-10 — Bahn: Fahrtkarte ist der Ruhezustand; zwei Handlungen zwischen Auflösung und nächster Frage.** *(entschieden als Hypothese, Mike)*
„Nächster Ort: X — Frage starten" ist die größte Fläche der Fahrtkarte. Nach der Auflösung landet man auf der Fahrtkarte, sieht den neuen Pin erscheinen und startet die nächste Frage. Das sind zwei Handlungen, wo das Spielkonzept bisher „ein Tap" sagte; die Abweichung ist dort vermerkt (v0.2.5 §1 Schritt 5). **Kipp KU5:** Wird die Fahrtkarte als Umweg genannt, bekommt die Auflösung in der Bahn eine Leiste „Nächster Ort: X" und überspringt die Karte.

**R-UI-11 — Bahn-Optionen: senkrechte Liste, nicht 2×2. Ausnahme Radar.** *(unverändert)*
Optionen sind ganze Sätze. Radar: vier Ziffern-Buttons nebeneinander unter der schematischen Karte.

**R-UI-12 — Wer-glaubt-wem: eine Textzeile, keine Avatare, keine Namen, keine Balken.** *(unverändert)*
Eine Zeile über den Optionen: „Erst jede:r laut: welche Nummer? Dann: wer liegt richtig?"

**R-UI-13 — Leiter: „höher" oder „hier steige ich aus".** *(entschieden, Mike)*
v0.1 übernahm „Mehr / Weniger" mit einer Stopp-Leiste samt Bank („Sicher: 3.000"). Das ist das Muster eines Spiels mit Einsatz; der Reise-Modus hat keinen. Es gilt die Form der Karte, die im ersten Test funktioniert hat: Je Stufe zwei Flächen, **„höher"** und **„hier steige ich aus"**; der Ausstieg ist die Antwort, danach kommt die Auflösung. Keine Bank, keine Stopp-Leiste. Die Stufen dürfen alle zugleich sichtbar sein; die aktuelle ist hervorgehoben. Die Leiter gibt es in allen Situationen (im Auto nur ab drei Personen).

**R-UI-14 — Fahrtkarte: Farbe plus Form plus Legende, keine Bewertungs-Emojis.** *(Zählung entschieden, Mike)*
Vier Zustände, die die App aus dem Getippten kennt: **Treffer** (eine Option getippt, richtig), **daneben** (eine Option getippt, falsch), **gespalten** (zwei Optionen getippt; halb/halb, gleich ob eine davon richtig war), **uneinig**. Der „Ort der Fahrt" bekommt als einziger Pin ein Zeichen, von der Gruppe gesetzt.

**R-UI-15 — Fahrtbilanz: Orte · Treffer · Spaltungen. Keine Lacher.** *(Zählung entschieden, Mike)*
Eine Spaltung zählt nicht als Treffer, auch wenn eine Hälfte richtig lag. „Uneinig" ist weder Treffer noch Spaltung. Solo zeigt keine Spaltungen.

**R-UI-16 — Anschluss als eigene, optionale Sektion in der Auflösung.** *(Verweis berichtigt)*
Unter einer Trennlinie, mit kleiner Überschrift, nur wenn es einen gibt; sonst fehlt die Sektion ganz. Das gilt für beide Anschluss-Klassen (Spielkonzept §1 Schritt 4d: höchstens einer, kein Fallback). Der Anschluss zählt in die 70 Wörter der Auflösung. „Auf Karte zeigen" und Linien zwischen Pins sind Kann für Solo, nicht v1.

**R-UI-17 — Vorankündigung als Entfernung, nicht als Countdown.** *(unverändert)*
„Nächster Ort: Bendorf · 3,2 km" auf dem Leerlauf-Screen. Sekundenangaben nirgends.

**R-UI-18 — Designsystem: Arbeitswerte mit Herkunft.**
- **Textlängen:** Frage ≤ 25 Wörter, Option ≤ 8, Auflösung ≤ 70 einschließlich Anschluss (Spielkonzept v0.2.5).
- **Schrift im Auto (gemessen):** Ortsname 20 px, Frage 24 px, Optionen 20 px, Auflösung 20 px, Zeilenabstand 1,4. Mit diesen Werten und den Texten des Kartensatzes ist der Frage-Screen bei 360 px Breite 494–578 px hoch und die Auflösung bei 67 Wörtern 686 px; ein Telefon mit 360 × 800 px zeigt etwa 730–750. Bei Frage 28 / Option 22 px passt eine Frage an der Wortgrenze nicht mehr (912 px). Messung: PC-Prüfung U2.
- **Schrift in der Bahn (aus den Eingängen, ohne Messung):** Frage 22 px, Optionen 17 px, Fließtext 15 px, Quelle 13 px.
- **Trefferflächen:** ≥ 48 × 48 px überall (übliche Plattform-Richtlinie). Auto-Optionen ≥ 72 px hoch, 8 px Abstand. Nächste Referenz: Googles Richtlinie für Apps im Auto verlangt 76 × 76 dp für die fahrende Person; für Beifahrer ist mir keine Vorgabe bekannt.
- **Systemschrift (entschieden, Mike):** Im Auto bleibt die Schrift fest auf den gemessenen Werten; sie sind schon Vorlesegröße, und nur so hält „kein Scrollen". In Bahn-Gruppe und Solo wächst sie mit der Systemeinstellung; dort darf das Blatt scrollen.
- **Schriften:** Fraunces für Ortsname und Frage, Nunito Sans für alles andere. Eine Geschmacksentscheidung mit einer Vermutung zur Lesbarkeit, kein Beleg.
- **Farben:** Ortsschild-Gelb `#f6c700` nur als Fläche mit schwarzer Schrift (10,7 : 1) oder als Akzent auf Anthrazit `#1b1f24` (10,3 : 1); auf hellem Grund hat es 1,5 : 1 und trägt keine Schrift. Spine-Blau `#2b4b6f` nur auf hellem Grund (8,7 : 1); auf Anthrazit hat es 1,8 : 1, die dunkle Fassung nimmt `#8fb4dc`. Kein Giftgrün, kein Signalrot in der Auflösung.
- **Kontrast** ≥ 4,5 : 1 für Text. Vorlesereihenfolge: Ortsname → Frage → Optionen → Festlegung → Auflösung.
- **Abstände:** Rand 16 px, Kachel-Innenabstand 16 px.

**R-UI-19 — Aussehen: eigenes Bild für den Reise-Modus, auf dem Farbsystem von MixMi gebaut.** *(Mike: „nach deinem Vorschlag"; der Vorschlag steht hier erstmals ausgeschrieben)*
- **Eigenes Bild:** Ortsschild-Gelb mit schwarzer Schrift als einziges Markenzeichen, ruhige Flächen, genau zwei Fassungen (hell, dunkel). Die Designs von MixMi (Verlauf in Logo-Farben, Milchglas-Karten, langsame Atem-Animation) passen hier nicht: Im Auto soll nichts pulsieren, und beim Vorlesen zählt ruhiger Grund mehr als Schmuck.
- **Gleiche Technik:** Farben und Maße liegen wie bei MixMi als benannte Variablen in einer Themen-Klasse (dort `--iter7a-*` mit `themeStore`). Der Reise-Modus ist damit ein weiteres Thema im selben System und kein drittes daneben; das Bild lässt sich später ändern, ohne Bildschirme anzufassen.
- **Keine Design-Auswahl in der ersten Fassung.** Acht umschaltbare Designs wie in MixMi sind hier Rucksack; es gibt nur Hell und Dunkel (R-UI-4).
- **Nähe zu QuizAway v5:** v5 ist dunkel mit Bernstein `#f0a500`. Das Ortsschild-Gelb `#f6c700` auf Anthrazit liegt dicht daneben; die dunkle Fassung wirkt wie eine Fortsetzung, nicht wie ein Bruch.
- **Schriften bleiben Arbeitsannahme** (Fraunces, Nunito Sans), bis der Papier-Test der Screens gelaufen ist.

---

## 3. Abgelehnt (Kurzliste mit Grund)

| Vorschlag | Quelle | Grund |
|---|---|---|
| Auto-Advance nach 5 s | U2, U5 | Spielkonzept §1 kein Weiter; schneidet den Nachhall ab (R-UI-9) |
| „Weiter" / „Weiter zur Station" in der Auflösung | U7, U8 | dito |
| Urteil zuerst, „Richtig!" grün oben | U1, U7, U8 | Reveal-Vertrag §8 Nr. 5 (R-UI-8) |
| Richtige Kachel in der Auflösung still vormarkiert | U5 | verrät das Urteil vor der Geschichte (R-UI-8) |
| Doppel-Tap für zweite Option | U1 | versteckte Geste (R-UI-6) |
| Blatt über Karte im Auto für Frage und Auflösung | U2, U5 | Lesbarkeit beim Vorlesen (R-UI-3) |
| 2×2-Kacheln in der Bahn | U5 | Optionen sind Sätze, nicht Wörter (R-UI-11) |
| Avatare, Namen, Prozentbalken, eigener Wer-liegt-richtig-Screen | U2, U5, U8 | §3.2 nicht aufgezeichnet (R-UI-12) |
| „3 Lacher" in der Bilanz | U3, U5, U6, U7, U8 | §4 kein Datenpunkt (R-UI-15) |
| Bewertungs-Emojis auf Pins | U3, U6 | Rucksack §6 (R-UI-14) |
| Countdown „Frage kommt in 18 Sek.", „20 Sekunden Zeit" | U8 | Timer (R-UI-17) |
| „Später"-Icon zum Überspringen im Auto | U2 | „Gleich" deckt den Fall |
| „Jetzt" oben rechts | U6 | Bedienelemente unten (Grundsatz 5) |
| Tap irgendwo schließt die Auflösung | U3, U6 | Fehltipp beim Herumzeigen (R-UI-9) |
| Leiter mit „Mehr / Weniger" und Stopp-Leiste samt Bank | U4, in v0.1 angenommen | Muster eines Spiels mit Einsatz; der Reise-Modus hat keinen (R-UI-13) |
| „Bei Einstimmigkeit genügt der Kachel-Tap" | v0.1 | schließt die Mehrfachauswahl aus (R-UI-7) |
| Auto immer dunkel | v0.1 | für Tagfahrten nicht belegt; Start nach Systemeinstellung (R-UI-4) |
| „Neustart"-Button am Ende | U7, U8 | Grundsatz 9 |
| Antwortkacheln „halbe Breite, Drittel Höhe" | U6 | vier Optionen plus Frage passen dann nicht auf einen Screen |
| Fortschrittsbalken | U2, U5 | eine Textzeile „Ort 4 von 12" reicht |
| Link „Noch eine Frage zu …?" in der Auflösung | U0 | angebotener Nachschlag, Spielkonzept §6 |

---

## 4. Screen-Inventar v0.2

| # | Screen | Situation | Kerninhalt | Bedienung (unten) |
|---|---|---|---|---|
| S1 | Start | alle | Wortmarke; bei offener Fahrt „Fahrt fortsetzen" | „Fahrt starten" (56 px, volle Breite), Zahnrad oben rechts |
| S2 | Streckenquelle | alle | Blatt mit 3 Karten: GPS / Geplant / Gewürfelt | ein Tap |
| S2a | Geplante Route | alle | Von / Nach, Tausch, Vorschau „14 Orte · 189 km" | „Route starten" |
| S2b | Gewürfelt | alle | Raum-Chips, Würfel-Button | Würfeln, neu mischen |
| S3 | Situation | alle | 3 Karten (R-UI-1) | ein Tap |
| S4 | Auto: Leerlauf = Fahrtkarte | Auto | Linie mit Pins, „Nächster Ort: X · 3,2 km", „Ort 4 von 12"; bei GPS-Verlust Zeile „Kein GPS — auf Route wechseln" | „Jetzt" · „Fahrt abschließen" (klein) |
| S5 | Auto: Frage | Auto | Ortsname mit Steckbrief-Zeile, Frage, Hinweis „3-2-1", 2–4 Kacheln 1–4 ≥ 72 px | ohne Auswahl: „Gleich" · „uneinig"; mit Auswahl: „Auflösen" |
| SL | Leiter | alle | Stufen, aktuelle hervorgehoben | „höher" · „hier steige ich aus" |
| S6 | Auflösung | alle | Eure Theorie (Zitat) → Geschichte → Urteil-Chip → Quelle → [Anschluss]; im Auto 20 px, ohne Scrollen | Wisch ↓ oder Leiste (Auto: zum Leerlauf; Bahn: „Zur Fahrtkarte") |
| S7 | Bahn: Fahrtkarte | Bahn-Gruppe, Solo | Linie mit Pins (Farbe + Form + Legende), „Ort 4 von 12"; Solo mit den Namen der kommenden Orte; Bingo als Streifen, nur auf ortsarmen Strecken | „Nächster Ort: X — Frage starten" (größte Fläche) · „Fahrt abschließen" (klein) |
| S7d | Pin-Detail | alle | Ortsname, Steckbrief-Satz, die gespielte Auflösung; Nachschlag | schließen |
| S8 | Bahn: Frage | Bahn-Gruppe, Solo | Blatt über S7, Frage, Liste 1–4 ≥ 56 px; Gruppe: Wer-glaubt-wem-Zeile optional | Gruppe: „Auflösen" (mit Mehrfachauswahl); Solo: „Festlegen" (Wahl bis dahin änderbar) |
| S8R | Bahn: Radar | Bahn-Gruppe, Solo | schematische Karte mit Nachbarorten 1–4 | 4 Ziffern-Buttons nebeneinander |
| S10 | Fahrtende | alle | Karte mit allen Pins, Bilanz (R-UI-15), Ort der Fahrt (Gruppe) / Drei Dinge (Solo), Große Fahrtfrage optional | „Teilen" · „Schließen" gleich groß |

Im Auto gibt es S4, S5, SL, S6, S7d und S10.

---

## 5. Kipp-Kriterien für die UI (Feldtest-Fragen)

- **KU1 Beifahrer-Blick:** Braucht der Beifahrer mehr als einen Blick, um nach dem Zuruf zu tippen? Dann sind Kacheln oder Schrift zu klein, nicht die Mechanik falsch.
- **KU2 Fehltipp:** Mehr als ein Fehltipp pro zehn Orte im fahrenden Auto → Kachelhöhe und Abstand hoch.
- **KU3 Zähler als Druck:** Wird „Ort 4 von 12" als Zeitdruck genannt? Dann entfällt die Zeile im Auto.
- **KU4 Hell und Dunkel:** Welche Fassung ist mittags im Auto besser lesbar, welche stört abends die fahrende Person? Ergebnis des Ansehens entscheidet über die Voreinstellung (R-UI-4).
- **KU5 Umweg Fahrtkarte:** Zwei Handlungen zwischen Auflösung und nächster Frage werden als Umweg genannt → R-UI-10 Kipp.
- **KU6 Ziffern-Zuruf:** Werden „zwei" und „drei" verwechselt, obwohl „zwo" gelesen wird? Rufen Testpersonen den Inhalt statt der Ziffer („das Kloster!")? Dann tippt der Beifahrer nach Inhalt; Ziffern bleiben.
- **KU7 Scrollen im Auto:** Muss der Beifahrer beim Vorlesen der Auflösung scrollen? Dann stimmt Wortgrenze oder Schriftgröße nicht.

---

## 6. Papier-Screens: ein eigener Test

Die Papierkarten des Solo-Tests waren bereits nahe am Auto-Frage-Screen (ein Blatt, Frage vorne, Auflösung hinten). Karten im Telefon-Ausschnitt (S5 vorne, S6 hinten, Urteil-Chip unten, Quelle klein) prüfen die Reihenfolge der Auflösung ohne eine Zeile Code. **Sie kommen aber nicht in den zweiten Solo-Test** (Entscheid Mike): Der vergleicht die Karten 3 und 10 mit der ersten Person und verträgt keine zweite Änderung. Die Papier-Screens laufen mit einer weiteren Person oder am Bahn-Gruppen-Tisch. Dafür müssen die Auflösungen auf 70 Wörter gekürzt sein; vier Karten des Satzes liegen darüber.

---

## 7. Offen

**Entschieden seit v0.1 (Mike, 2026-10-01):** Ziffern mit „zwo" (R-UI-5); Hell/Dunkel nach Systemeinstellung beim Start, vorher im Auto ansehen (R-UI-4); zwei Handlungen in der Bahn als Hypothese (R-UI-10); Papier-Screens getrennt (§6); Auflösung ≤ 70 Wörter (R-UI-18); Leiter als „höher / hier steige ich aus" (R-UI-13).

**Entschieden im Nachtrag (Mike, 2026-10-01):** Spaltung zählt nicht als Treffer (R-UI-14, R-UI-15); Schrift im Auto fest, in der Bahn mitwachsend (R-UI-18); Solo wählt und bestätigt mit „Festlegen", weil man sonst nicht weiß, wann es weitergeht, und noch einmal überlegen und korrigieren kann (S8); Aussehen nach R-UI-19.

Damit endet in jeder Situation die Festlegung mit einer Leiste: im Auto und in der Bahn-Gruppe „Auflösen", im Solo „Festlegen". Der Kachel-Tap allein löst nirgends auf.

**Noch offen, und wodurch es sich klärt:**
1. **Hell oder Dunkel als Voreinstellung im Auto:** durch Ansehen im stehenden Auto, mittags und abends (R-UI-4, KU4).
2. **Vier Themen, die die Runde nicht behandelt hat** (Übelkeit beim Lesen im Auto, Lesbarkeit von mehreren Tischseiten, Format des Teilen-Bilds, Maße mit Herkunft): durch die Nachfrage `quizaway-oberflaeche-review-briefing-runde5-2026-10-01.md`.
3. **Schriften und Reihenfolge der Auflösung:** durch den Papier-Test der Screens (§6).
4. **Formulierung der drei Situationen auf dem Startschirm** (R-UI-1): nach dem Feldtest, wie im Spielkonzept §3 vorgesehen.

*Ende UI-Konzept v0.2.*
