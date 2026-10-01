# QuizAway — Spielkonzept Reise-Modus v0.2.5

**Story-Satz:**
*Ein Ort wird zum nächsten Spielort. Das Spiel wirft eine Behauptung auf, die man sich zurechtlegen kann. Man legt sich fest. Der Ort erzählt, was wirklich ist, nimmt die eigene Theorie mit und knüpft, wenn es sich lohnt, an einen Ort davor an. Der Reiseführer ist das Fundament; wie man sich festlegt, ist pro Sitzplatz anders, und dort sitzt der Witz.*

---

## Status-Block

| | |
|---|---|
| **Version** | v0.2.5 (v0.2.4 plus zehn Entscheide Mikes zur PC-Prüfung des UI-Konzepts, Anhang E; die letzten vier als Nachtrag am selben Tag). v0.2.4 war v0.2.3 plus PC-Prüfung gegen Kartensatz, Protokoll, Gemeinde-Achsen v0.5 und Transfer-Konzept v1.1 (Anhang D). **Achtung Zählung:** v0.2.4 und v0.2.5 sind am PC entstanden; eine am Handy geplante „v0.2.4" ist nicht diese. |
| **Datum** | 2026-10-01 |
| **Status** | v0.2.2 von Mike freigegeben als Feldtest-Grundlage (2026-10-01, 12:29). Erster Solo-Test gelaufen (15:17): Theoriebildung findet statt (6 von 10 T2, kein Ermüdungstrend); K1 und K3a sind noch nicht einzeln erhoben. v0.2.5 ist die Grundlage für die zweite Solo-Person (Kartensatz Fassung 2), für Stufe 2 und für das UI-Konzept v0.2. Keine Implementierungsfreigabe; die kommt nach Stufe 2 (§11). |
| **Scope** | Spielmechanik des Reise-Modus: Auto-Gruppe, Bahn-Gruppe, Bahn-Solo, drei Streckenquellen. „Sofa" ist gewürfelte Strecke plus Display-Modus. Fern-Duell nicht Gegenstand. |
| **Provenance** | v0.2 → Runde 4 (R4-A bis R4-D) → Rulings Anhang B → v0.2.1 → R4-E → Rulings Anhang C → v0.2.2 → Feldtest Solo Freiburg → v0.2.3 (§8 Nr. 2, Nr. 4b und Nr. 6, §11) → PC-Prüfung → Rulings Anhang D → v0.2.4 → UI-Runde (Handy) → UI-Konzept v0.1 → PC-Prüfung → Rulings Anhang E → v0.2.5. |
| **Entschieden (Mike)** | Ein Gerät. Beifahrer liest, TTS optional später. Kein Solo im Auto. |
| **Offen** | Nichts auf Konzeptebene. Alles Weitere entscheidet der Feldtest. |

**TL;DR gegenüber v0.2:** Keine neue Mechanik. Nur Schließungen: Der Anschluss ist Kernbaustein in allen Modi, hat zwei Klassen (Vergleich aus Achsen, Erzählung nur wo vorhanden), ist Beobachtung und nie neue Frage, bezieht sich auf den letzten gespielten Pin, und es gibt keinen Fallback. Familie B läuft im Auto als Zwei-Aussagen-Variante. Der Zwei-Personen-Betrieb im Auto ist ein eingeschränkter Modus, kein Kipp. Verbal-Radar nutzt Fahrtrichtung und Entfernung, keine Himmelsrichtungen. Fahrtende ist ein eigener Schritt. Wortzahlen sind verbindlich. Der Feldtest unterscheidet handgeschriebenen Content (Obergrenze, misst den Kern) von generiertem Content (misst die Pipeline) und klassifiziert Theorien in T0/T1/T2. Vier Formulierungsfehler sind korrigiert.

**Zusätzlich in v0.2.2 (aus R4-E):** Die Festlegung im Auto kennt jetzt drei Fälle statt zwei: einstimmig, gespalten, zersplittert. Ein „Jetzt"-Tap ist das Gegenstück zum „Gleich"-Tap, damit ein verspäteter GPS-Trigger den Moment nicht verpasst. Der Kontext-Spiegel ist als zulässige Generierungsregel für Distraktoren präzisiert. Think-Aloud ist die Methode für den Solo-Tisch. Am Fahrtende darf die Gruppe den „Ort der Fahrt" wählen, als Ersatz für die nicht zählbaren Lacher.

**Zusätzlich in v0.2.4 (aus der PC-Prüfung, Anhang D):** Keine neue Mechanik. Der Negativnachweis für gespiegelte Distraktoren gilt nur noch, wo er einer ist (einwertige Eigenschaft mit anderem Wert, oder vollständige Quelle). Der Spender eines gespiegelten Fakts darf kein Ort der Fahrt sein. Die Lügen-Hypothese aus v0.2.3 ist zurückgenommen und durch zwei prüfbare Vermutungen ersetzt. Die Theorie-Klassifikation bekommt das Kürzel W (gewusst oder wiedererkannt). Der Bekanntheitsfilter misst den Fakt, nicht den Ort. Radar bekommt eine Lösungsregel und eine eigene Längengrenze. §9 ist ausgeschrieben und in zwei Punkten berichtigt. Die Schicht-Begriffe folgen jetzt Gemeinde-Achsen v0.5; die Verweise auf eine ältere Kriterien-Zählung (K3, K4, K9) sind durch die Namen der Kriterien ersetzt.

**Zusätzlich in v0.2.5 (aus der Prüfung des UI-Konzepts, Anhang E):** Optionen tragen Ziffern 1–4, im Auto gerufen und vorgelesen mit „zwo". Die Auflösung hat jetzt eine Längenregel: höchstens 70 Wörter einschließlich Anschluss. Die Leiter ist bestimmt: je Stufe „höher" oder „hier steige ich aus"; es gibt kein Stopp, das etwas sichert. In der Bahn liegen zwischen Auflösung und nächster Frage zwei Handlungen statt einer, als Hypothese mit Kipp. Papier-Screens der Oberfläche werden getrennt vom zweiten Solo-Test geprüft.

---

## 1. Der Core-Loop

Fünf Schritte, in jeder Situation gleich.

**1. Auslöser.** Ein Ort wird zum nächsten Spielort: durch Position, Zeittakt oder Weiterschaltimpuls (§1a). Im Auto drängt sich die Frage auf (Push), in der Bahn wartet sie (Pull). Im Auto gibt es zwei Korrektur-Taps für den Beifahrer: **„Gleich"** stellt eine Push-Frage einmal hinten an (Kurve, Baustelle, laufende Diskussion), statt sie zu verwerfen; **„Jetzt"** löst den nächsten Ort mit Material sofort aus, wenn das Schild schon da ist und der GPS-Trigger hinterherhinkt (Tunnel, Brücke, Funkloch). Die App muss nicht wissen, wann das Schild kommt; sie muss bereit sein, wenn der Beifahrer es sagt.

**2. Behauptung aufwerfen.** Frage oder Aussage über den Ort mit zwei bis vier Optionen. **Qualitätsregel:** Jede Option muss als eigenständige plausible Theorie formulierbar sein („Der Name kommt vom Bach", nicht „wegen eines Flusses"). **Redaktionsregel, verbindlich:** Frage ≤ 25 Wörter, jede Option ≤ 8 Wörter, Gesamtvorlesezeit ≤ 20 Sekunden. **Auflösung ≤ 70 Wörter einschließlich Anschluss** (neu in v0.2.5): Entschieden ist das für das Auto, wo bei Vorlesegröße (20 px) mehr nicht ohne Scrollen auf den Bildschirm passt und mehr die Runde von 60 Sekunden sprengt; weil jede Karte in allen Modi spielbar sein muss (§3.4), ist es die Grenze für jede Karte. Der erste Kartensatz lag bei vier von zehn Karten darüber. **Beschriftung:** Optionen tragen Ziffern 1–4, keine Buchstaben; im Auto liest und ruft man „zwo", weil „zwei" und „drei" im Fahrgeräusch verwechselt werden. **Varianzregel:** nicht zweimal hintereinander dieselbe Fragefamilie, nicht zweimal hintereinander derselbe Fakten-Typ.

**3. Theorie bilden und festlegen.** Wie, bestimmt der Modus (§3). Begründen ist Standardangebot, nie Pflicht.

**4. Story-Reveal.** (a) Die Festlegung wird aufgegriffen: einstimmig, gespalten oder zersplittert (§3.1). (b) Die Geschichte des Orts wird erzählt und webt die Theorie ein. (c) Das Urteil wird nach der Erklärung eindeutig; es wird nicht nachgeschoben, wenn die Geschichte es schon gesagt hat. (d) **Anschluss (Kernbaustein, alle Modi):** höchstens ein Anschluss pro Reveal an den **letzten tatsächlich gespielten Pin**, nur wenn der Zusammenhang eigenständig interessant ist. Kein Fallback-Anschluss. Der Anschluss ist eine Beobachtung, nie eine neue Frage und nie eine neue Festlegung. Zwei Klassen, siehe §8. Quelle sichtbar.

**5. Nachhall.** Der Ort wandert auf die Fahrtkarte. Kein „Weiter" innerhalb der Frage-/Reveal-Sequenz. Zwischen Orten je nach Quelle ein Weiterschaltimpuls (ein Tap, großes Ziel). **In der Bahn sind es als Hypothese zwei Handlungen** (v0.2.5): Auflösung schließen, auf der Fahrtkarte erscheint der neue Pin, dann die nächste Frage starten. Der Umweg über die Fahrtkarte soll der Moment des Nachhalls sein. Kipp: Wird er als Umweg genannt, startet die nächste Frage direkt aus der Auflösung (UI-Konzept, KU5). Nachschlag zum selben Ort nur durch Tippen auf den Pin, nie automatisch, nie als Button angeboten.

**Was der Loop nicht hat:** Zeitdruck als Spannung, Punktestand pro Frage, Rangliste, Leben, Streaks, Statistiken als Belohnung.

### 1a. Streckenquelle

| Quelle | Wie | Takt | Wofür |
|---|---|---|---|
| **Echte Fahrt** | GPS, nächster Ort mit Material auf oder nahe der Position | Bewegung | Auto, Bahn |
| **Geplante Route** | Streckenliste (Google-Maps-Route, Bahnverbindung) | Tap oder Zeittakt | Bahn ohne GPS, Vorbereitung, Nachspielen |
| **Gewürfelte Strecke** | x Orte aus einem definierten Raum, zu einer Strecke verbunden | Tap oder Zeittakt | Sofa, Wartezimmer, Üben, Feldtest |

**Regeln:**
- Die Quelle liefert nur Orte **mit Material**. Ein Ort ohne Material wird still übersprungen, nie als leere Frage ausgeliefert. **Intern** werden zwei Größen geführt: relevante Orte passiert, Orte ausgespielt. Ob das Überspringen im UI sichtbar wird (dezente Marke „Ort passiert, kein Material"), entscheidet der Feldtest: Fragt jemand, warum die App stumm blieb, kommt die Marke.
- **„Aus der Nähe":** Auf ortsarmen Abschnitten (Autobahn, 80 km und drei Orte) darf die echte Fahrt Orte abseits der Linie hinzuziehen, als „aus der Nähe" markiert. Das ist eine Ergänzung der echten Fahrt, keine vierte Quelle.
- **Bahn-Definition:** „Ort an der Strecke" ist ein Ort mit Material innerhalb eines festen Korridors um die Linie (Richtwert 5 km). Sichtbarkeit aus dem Fenster ist nicht Bedingung.
- **GPS-Verlust:** manueller Wechsel auf geplante Route mit einem Tap. Die Fahrtkarte läuft weiter.
- Die Quelle ist orthogonal zum Modus. Keine Ortsschilderkennung, keine Kamera.
- Kipp (§7 K5): mehr als rund ein Drittel der passierten relevanten Orte bleibt wegen fehlenden Materials ungenutzt, oder Testpersonen nehmen längere Abschnitte als auffällig leer wahr, obwohl Orte da waren.

---

## 2. Die drei Fragefamilien und ein Ablaufmodifikator

Alle Familien sind im Grundfall „ein Klick, zwei bis vier Strings". Drei Abweichungen davon sind gewollt und in §9 als Erweiterungen der Schnittstelle geführt: die Leiter (Folge von Taps), die Mehrfachauswahl bei Spaltung (zwei Haken plus Bestätigen) und „uneinig" (ein Button ohne Option). Die Schicht-Angaben folgen Gemeinde-Achsen v0.5: Schicht 0 ist deterministisch ableitbar (Zahlen, Lage, Zugehörigkeit), Schicht 1 ist aus Text extrahiert (Geschichten, Namensherkunft).

| Familie | Form | Datenquelle | Einsatz |
|---|---|---|---|
| **A — Behauptung** | Frage, vier Theorien als Optionen | Schicht 1 für die wahre Option; Distraktoren mit Negativnachweis (§8) | Standard |
| **B — Lüge** | Bahn: drei Aussagen, eine gelogen. **Auto: zwei Aussagen, eine gelogen** („Eine der beiden stimmt nicht") | ≥ 2 belastbare Schicht-1-Fakten; Lüge mit Negativnachweis (§8) | Nur wo Daten reichen, sonst A. Aussagen ≤ 8 Wörter, gleich lang, gleich detailliert. |
| **C — Größenordnung** | Zahlenfrage ohne Zahlen: Epochen, Spannen | Schicht 0 numerisch | Höchstens jede dritte Frage, nie zwei hintereinander |

**Radar** ist Familie A mit Nachbarorten als Optionen. In Display-Modi mit schematischer Karte (nummerierte Punkte, Centroide). **Verbal (Auto):** relativ zur Fahrt, nie Himmelsrichtungen: „Auf eurer Strecke, 4 km vor euch: X. Weiter, 15 km: Y. Hinter der nächsten Abfahrt: Z. Welcher hat ein Freibad?" Richtung der Bewegung und Entfernung sind die Koordinaten, die Reisende haben. **Ortsfokus-Regel:** Der Reveal kehrt zum aktuellen Ort zurück. **Lösungsregel (neu):** Die richtige Option ist nicht immer der aktuelle Ort. Wer die Namen der kommenden Orte sieht (Solo-Vorschau, Fahrtkarte), gewinnt sonst jede Radar-Frage mit „der nächste Ort auf meiner Karte"; in den zwei Radar-Karten des ersten Tests war das so gebaut. Mal liegt die Lösung beim Nachbarn, und der Reveal erzählt, warum der aktuelle Ort es nicht hat. **Länge:** Radar verbal fällt nicht unter die Wortzahl-Regel aus §1 Schritt 2 (die Radar-Karte des ersten Tests hatte rund 60 Wörter). Startwert drei Orte wie im Beispiel oben; die Grenze misst der Auto-Test als Vorlesezeit.

**Leiter** ist ein **Ablaufmodifikator** über Familie C: eine Folge von mindestens drei Stufen („Höher als 400 m? Höher als 600 m? …"), unter 60 Sekunden, **höchstens jede zweite C-Frage**. **Form (v0.2.5):** Je Stufe gibt es genau zwei Antworten, „höher" oder „hier steige ich aus". Der Ausstieg ist die Antwort: Der Wert liegt nach Meinung der Spielenden zwischen der letzten bejahten und der abgelehnten Stufe. Es gibt kein „Stopp", das etwas sichert, und keine Bank; das Spiel hat keinen Einsatz. Die Stufen dürfen alle zugleich sichtbar sein (so die Karte des ersten Tests, die eine begründete Theorie hervorrief). Im Auto ruft man „höher" oder „raus". Fragilster Baustein, weil Ja/Nein wenig begründbares Raten erlaubt. Eigenes Kipp K6: Werden Leiter-Antworten je begründet? Wenn nicht, Leiter streichen, C bleibt Spannen. Im Zwei-Personen-Auto nicht verfügbar (§3.1).

---

## 3. Die drei Präsentationsmodi

Ein Modus definiert **Bedienung** und **Festlegung**. Daraus folgen sein **Takt** (Push oder Pull) und seine **Quelle des Moments**. Optionale **Zusatzschichten** sind je Modus ausdrücklich benannt. Der semantische Reveal (Antwort, Geschichte, Urteil) ist in allen Modi identisch; modusspezifische Ergänzungen dürfen ihn erweitern, nie verändern.

**Modus-Wahl beim Start:** Für den Feldtest schlicht „Auto / Bahn-Gruppe / Bahn-Solo". Die UI-Formulierung (neutral, nicht an die Streckenquelle gekoppelt, nicht „wir" für eine Einzelperson) ist eine Entscheidung nach dem Feldtest.

### 3.1 Auto-Modus (Gruppe, Fahrer:in ohne Display) — Push

- **Takt:** Push, Fenster 20–60 s, Gesamtrunde ≤ 60 s, „Gleich"- und „Jetzt"-Tap verfügbar (§1).
- **Bedienung:** Beifahrer liest vor. Rollenwechsel pro Fahrtabschnitt ab drei Personen.
- **Festlegung:** Zuruf auf „3-2-1", alle gleichzeitig. Jede Festlegung muss ohne Blick aufs Display verbal eindeutig sein („Zwo!", „Raus!"). Drei Fälle, die der Beifahrer ohne Nachdenken unterscheiden kann:
  - **Einstimmig** (alle dieselbe Option, oder bei zwei Personen beide gleich): ein Haken.
  - **Gespalten** (mindestens zwei Personen rufen dieselbe Option, aber nicht alle): Beifahrer tippt die Mehrheit; bei Patt setzt er zwei Haken und bestätigt mit einem Tap (Multi-Select, so schnell wie die Einzelwahl). Reveal-Fall „gespalten": „Ihr wart gespalten: 2 gegen 4. Beide klingen plausibel, aber…"
  - **Zersplittert** (alle rufen verschieden, möglich ab drei Personen): Beifahrer tippt **„uneinig"**, einen eigenen Button, keinen Haken. Reveal-Fall „zersplittert": „Ihr wart euch komplett uneinig. Die Wahrheit ist…", dann die Geschichte ohne Einweben einzelner Theorien. Keine Auswahl der „lustigsten" Theorie durch den Beifahrer; das wäre die „lauteste Theorie" durch die Hintertür.
  - Kein Tie-Breaker in keinem Fall. Die Spaltung ist der Moment.
- **Quelle des Moments:** gleichzeitiges öffentliches Festlegen; Spaltung und Zersplitterung sind der Moment. Feldtest zählt beide getrennt.
- **Familie B:** Zwei-Aussagen-Variante. Die Drei-Aussagen-Variante bleibt der Bahn.
- **Verfügbar:** A, B (zwei Aussagen), C, Leiter, Radar verbal. **Nicht:** Wer-glaubt-wem, Bingo, Karte als Darstellung.
- **Zwei-Personen-Betrieb (eine fährt, eine liest): eingeschränkter Modus.** Der Beifahrer ist Vorleser, Moderator und Tipper zugleich, der häufigste Fall (Paar, Elternteil und Kind). Deshalb: keine Leiter, Familie C nur als Spannen, Push bleibt, „Gleich"-Tap wird wichtiger. Lange Fahrten zu zweit sind die Grenze dieses Modus; TTS ist dafür die vorgesehene Entlastung (optional, später).
- **Fahrer-Ausschluss:** Keine Bedienung, kein Blick der fahrenden Person. Ohne Ausnahme.

### 3.2 Bahn-Gruppen-Modus (Gerät in der Tischmitte) — Pull

- **Takt:** Stille Fahrtkarte mit „Nächster Ort: X". Die Gruppe startet die Frage. Richtwert ≤ 90 s pro Runde.
- **Bedienung:** Alle lesen selbst.
- **Festlegung:** Zeigen oder kurzer Zuruf, ein Tap für die Frage-Antwort (Multi-Select bei Spaltung wie im Auto).
- **Zusatzschicht Wer-glaubt-wem** (ab drei Spielenden, nicht bei jeder Frage): Jede Person sagt ihre Antwort laut. Dann sagt jede Person laut, wer ihrer Meinung nach richtig liegt. Dann tippt eine Person die Frage-Antwort(en). Die Einschätzungen werden in v1 **nicht aufgezeichnet**; sie sind rein sozial, der Reveal löst sie mündlich auf. Kipp: Runde über zwei Minuten.
- **Quelle des Moments:** gemeinsamer Blick, Zeigen, Nacheinander-Diskutieren. Familie B (drei Aussagen) spielt hier ihre Stärke aus.
- **Verfügbar:** alle Familien, Radar mit Karte, Wer-glaubt-wem, Bingo nur auf ortsarmen Strecken (§4).

### 3.3 Bahn-Solo-Modus (eine Person, eigenes Tempo) — Pull

- **Takt:** Die Person sieht die **Namen** der kommenden Orte (keine Fakten, keine Fragen vorab) und startet die Frage selbst. Die Vorschau ist Absicht: Pull braucht sie, und die Überraschung liegt im Reveal, nicht im Ortsnamen.
- **Bedienung und Festlegung:** Tap auf eine Option wählt sie, „Festlegen" löst auf; bis dahin lässt sich die Wahl ändern (Mike, 2026-10-01: Man weiß sonst nicht, wann es weitergeht, und kann noch einmal überlegen). Leiter in Eigenregie.
- **Quelle des Moments (Solo-Moment):** Solo hat keinen sozialen Moment, und das ist in Ordnung. Der Reveal, der die Geschichte trägt, ist die tragende Säule; er muss solo pointierter sein, weil er die einzige Belohnung ist. Vier Ebenen, nicht gleichwertig:
  1. **Unmittelbar, jede Frage:** die eigene Theorie als Gegenüber. **Formelhaftigkeits-Regel:** drei bis vier Einwebungs-Muster rotieren, Theorie auch mal ernst nehmen.
  2. **Gewürz, nur Familie C:** Nähe statt richtig/falsch.
  3. **Rahmen:** Sammeln auf der Fahrtkarte. Allein Fortschritt, kein Moment.
  4. **Anschluss:** im Solo besonders wichtig, weil er die Serienneugier trägt („mal sehen, was der nächste Ort erzählt"). Regeln wie §1 Schritt 4 (d), Klassen wie §8.
- **Beim Abschluss der Fahrt:** „Drei Dinge, die ich heute nicht wusste", teilbar als Bild. Das bedient den Gesprächswert und ist der Ersatz für den fehlenden Zuhörer.
- **Nicht solo:** Mehrheits-Balken, Prozentzahlen, jede Statistik als Belohnung.
- **Verfügbar:** alle Familien, Radar mit Karte, Bingo nur auf ortsarmen Strecken (§4).

### 3.4 Was ein Modus nicht darf

Einen eigenen Fragetyp einführen. Den semantischen Reveal verändern (Ergänzungen ja, andere Antwort, Geschichte oder Urteil nein). Punkte pro Frage sichtbar machen. Eine Frage so bauen, dass sie nicht in allen drei Modi gestellt werden könnte; Radar ist Darstellung, Familie B zwei/drei Aussagen ist Dosierung derselben Frageform.

---

## 4. Die zwei Rahmen und das Fahrtende

Rahmen verändern den Core-Loop nicht.

**Fahrtkarte (alle Modi).** Schematische Streckenlinie, ein Pin pro gespieltem Ort: Ortsname, ein Satz Steckbrief, Ergebnis als Farbe oder Emoji. Nachschlag durch Tippen auf den Pin.

**Fahrtende (eigener Schritt).** Die Fahrt endet durch einen Tap „Fahrt abschließen" (oder Streckenende bei geplanter und gewürfelter Strecke). Dann: (1) **Fahrtbilanz**: „Neuwied–Kassel: 14 Orte, 9 Treffer, 4 Spaltungen." Alle Zahlen sind erfasste Ereignisse; „Lacher" ist kein Datenpunkt und steht nicht in der Bilanz. **Zählung (Mike, 2026-10-01):** Ein Treffer ist ein Ort, bei dem genau eine Option getippt wurde und diese richtig war (einstimmig oder Mehrheit; die App kann beides nicht unterscheiden). Eine Spaltung ist ein Ort mit zwei getippten Optionen (Patt); sie zählt nicht als Treffer, auch wenn eine Hälfte richtig lag. „Uneinig" ist ein eigener Zustand und weder Treffer noch Spaltung. (2) **Ort der Fahrt** (Gruppe, optional): Die Gruppe tippt einen Pin an, der den Moment der Fahrt markiert, egal ob Treffer oder Fehlschlag. Ein Tap, keine Begründung, kein Zwang; der Pin wird auf der Karte hervorgehoben. Das ist der Ersatz für die nicht zählbaren Lacher: Die Gruppe zählt ihn selbst. Solo entfällt. (3) Optional **Große Fahrtfrage** als Leiter über die gespielten Orte. (4) Solo: **„Drei Dinge, die ich nicht wusste."** (5) Bild-Export. Eine Fahrt, die nicht abgeschlossen wird, kann später fortgesetzt werden. **Ehrliche Benennung:** Die Bilanz zeigt eine Trefferzahl. Das ist kein Wettkampf-Score (nie pro Frage, keine Rangliste, keine Einordnung als gut oder schlecht), aber eine Zahl, die jemand sieht. Der Feldtest fragt, ob sie als Druck wirkt; wenn ja, fällt die Zahl, und die Bilanz besteht aus Orten, Pins und dem Ort der Fahrt.

**Bingo (nur Bahn, Gruppe und Solo).** Felder sind Achsen mit Schwellwert, nur aus Schicht 0 automatisch prüfbar. **Hierarchie:** Reise-Quiz ist Hauptspiel, Bingo ist Füller, in Gruppe und Solo gleichermaßen nur auf längeren ortsarmen Strecken aktiv. Bingo unterbricht nie den Core-Loop und überspringt nie einen Ort mit Material. Kipp: zieht Aufmerksamkeit von der Frage.

---

## 5. Taktung (Hypothesen, ungetestet)

- Eine Frage pro Ort. Nachschlag nur über den Pin.
- Familie C höchstens jede dritte Frage, nie zwei hintereinander. Leiter höchstens jede zweite C-Frage.
- Wer-glaubt-wem höchstens jede vierte Frage.
- Radar mit Karte (Bahn) höchstens jede zweite Frage.
- Anschluss nur bei eigenständig interessantem Zusammenhang; es gibt keine Quote nach oben, weil es keinen Fallback gibt.
- Varianz: nicht zweimal dieselbe Familie, nicht zweimal derselbe Fakten-Typ.
- Zeitbudget: Auto ≤ 60 s, Bahn-Gruppe ≤ 90 s, Solo frei.
- Mikro-Feedback erlaubt („Ort 4 von 12").

---

## 6. Anti-Rucksack

Nicht in v1: Ortsschilderkennung, Kamera; TTS (optional später); Mehrheits-Balken und jede Prozentstatistik; p2p oder zweites Gerät; Fenster-Detektiv als Pflicht; Lokal-Rätsel; Team-Schätzung mit Rechnen; Kartenkacheln; Badges, Level, Achievements, Streaks; automatischer Nachschlag; angebotener „Noch eine?"-Button; Fallback-Anschluss; Bingo im Auto; aufgezeichnete Wer-glaubt-wem-Einschätzungen.

---

## 7. Kipp-Kriterien

- **K1 — Kernversprechen (dreiteilig):** Nach dem Reveal kann die Person (1) ihre Theorie nennen, (2) den tatsächlichen Grund nennen, (3) sagen, warum ihre Theorie plausibel oder falsch war. Fehlt (3) regelmäßig, trägt der Kern nicht; (3) ist das Spiel. Keine Prozentschwelle bei kleinem Test, aber die drei Teile werden getrennt protokolliert.
- **K2 — Schnitt:** Eine Frage lässt sich nicht in allen drei Modi stellen, ohne den Fragetyp zu ändern.
- **K3a — Solo, Abbruch:** An natürlichen Pausen wird abgebrochen statt „noch ein Ort". Ab zwei Abbrüchen vor dem geplanten Ende. **Nur in der echten Bahn messbar**; am Tisch werden Pausen simuliert (drei Unterbrechungen mit Alltagsaufgabe) oder K3a entfällt dort.
- **K3b — Solo, Durchtippen:** **Primär:** Wird vor dem Reveal noch eine konkrete Theorie gebildet (T2, §10)? **Sekundär:** Lesedauer Ort 2 vs. Ort 10, nur als Indikator. Wenn nur noch durchgetippt wird, ist es Informationsabfrage, kein Spiel. Eine gewusste oder wiedererkannte Antwort (W, §10) ist kein Durchtippen; sie zählt gegen die Karte, nicht gegen den Kern.
- **K4 — Host:** Beifahrer wirkt nach fünf Orten nur noch als Vorleser.
- **K5 — Streckenquelle:** siehe §1a.
- **K6 — Leiter:** Leiter-Antworten werden nie begründet.
- **K7 — Anschluss (neu):** Anschlüsse werden als künstlich oder aufgesetzt empfunden, oder sie erzeugen Nachfragen, die eine zweite Frage erwarten.

---

## 8. Schnittstelle zu den Inhalten (Gemeinde-Achsen)

1. **Negativnachweis Distraktoren (A):** Eine falsche Option muss falsch sein; „nicht als richtig bekannt" reicht nicht. Eine Frage gilt nicht als korrekt, weil nur eine Option positiv belegt ist. Drei zulässige Wege:
   - **(a) Harter Negativnachweis:** Der Fakt ist für den Zielort explizit widerlegt.
   - **(b) Kontext-Spiegel** als kontrollierte Generierungsregel: Der Distraktor ist ein wahrer, belegter Fakt eines Orts **außerhalb der direkten Nachbarschaft** (Richtwert 50–100 km, gleiche Größenklasse). Er ist nur zulässig, wenn die Eigenschaft am Zielort **entweder mit einem anderen Wert belegt ist** (einwertige Eigenschaften: Namensherkunft, Herrschaft, Landkreis, Bahnstrecke) **oder aus einer vollständigen Quelle stammt und dort fehlt** (Schicht 0, zum Beispiel ein vollständig erfasstes Straßenbahnnetz). „Am Zielort nicht gesetzt" allein genügt nicht: In einer lückenhaft wachsenden Datenbank heißt das „unbekannt", nicht „falsch", und ein wahrer Distraktor bestraft die richtige Antwort. Der Abstand verhindert, dass der gespiegelte Fakt zufällig auch auf den Zielort zutrifft (Nachbarorte teilen Fluss, Landkreis, Dialektraum).
   - **(c) Erfundene Theorie gegen einen belegten einwertigen Fakt:** Ist die wahre Antwort einwertig und belegt (die Namensherkunft, der Grund einer Benennung), ist jede abweichende Theorie falsch und darf frei formuliert werden. So sind die Karten 1 und 4 des ersten Tests gebaut. Grenze: keine erfundene Theorie, die eine zweite, nur unbelegte Wahrheit sein könnte (Vorhandensein, Ereignisse).
   - **Spender-Regel (neu):** Der Spender eines gespiegelten Fakts darf **kein Ort dieser Fahrt** sein, weder schon gespielt noch angekündigt. Sonst wird die falsche Option wiedererkannt statt beurteilt (Befund aus dem ersten Test, Nr. 2). Die Abstandsregel deckt das auf kurzen Fahrten, auf langen nicht.
2. **Negativnachweis Lüge (B):** Die falsche Aussage muss für den Zielort widerlegt oder eindeutig einem anderen Ort zugeordnet sein. Zusätzlich **Formgleichheit:** Aussagen gleich lang, gleich detailliert, gleich spezifisch, damit die Lüge nicht an der Form erkennbar ist. Zur Formgleichheit gehört: Auffälligkeit darf nicht mit Wahrheit zusammenhängen (nicht immer die Lüge und nicht immer eine Wahrheit ist die spektakulärste Aussage), die Lüge darf der eigenen Vorderseite nicht widersprechen, und ihre Stelle wechselt von Karte zu Karte (im ersten Kartensatz stand sie dreimal an dritter Stelle). **Befund aus dem ersten Feldtest, berichtigt in v0.2.4:** v0.2.3 schloss aus dem Protokoll, die Lüge solle unspektakulärer klingen als die Wahrheiten. Der Kartensatz zeigt, dass sie das in allen drei B-Karten schon war; eine Theorie entstand trotzdem nur bei Karte 7. Die Karten 3 und 10 unterschieden sich anders: Ihre Lügen waren gespiegelte Fakten aus Gundelfingen, das als Karte 2 schon gespielt war, und bei Karte 10 kamen ein Widerspruch zur Vorderseite und eine fehlende Jahreszahl dazu. **Zwei Vermutungen, die die zweite Solo-Person prüft (Kartensatz Fassung 2):** (1) Wiedererkennen ersetzt die Theorie; daher die Spender-Regel in Nr. 1. (2) Eine Lüge trägt, wenn man aus der Vorderseite und Allgemeinwissen etwas über sie folgern kann (Karte 7: Tal gegen Ebene). **Rohbogen nachgesehen (Mike, 2026-10-01):** Die erste Person hat bei Karte 3 und 10 Gundelfingen nicht genannt. Vermutung (1) ist damit nicht gestützt; widerlegt ist sie nicht, denn Wiedererkennen muss nicht ausgesprochen werden. Die Spender-Regel bleibt, weil sie ein Leck schließt, das es der Sache nach gibt; als Erklärung des ersten Tests trägt sie nicht. Für Karte 10 bleiben drei andere Lecks (Widerspruch zur Vorderseite, fehlende Jahreszahl, Lüge zum dritten Mal an dritter Stelle). Für Karte 3 gibt es keine Erklärung aus der Karte; auffällig ist nur, dass die Karten 2 und 3 die jeweils erste Karte ihrer Familie waren und beide ohne Theorie blieben, die jeweils zweite (9 und 7) mit. Ob das Eingewöhnung ist, zeigt die zweite Person.
3. **Theorie-Formulierung:** Jede Option als Theorie formulierbar (§1 Schritt 2).
4. **Anschluss, zwei Klassen:**
   - **(a) Vergleichsanschluss, v1:** aus Achsenwerten des aktuellen Orts und des letzten gespielten Pins: Einwohner, Ersterwähnung, Höhe, Entfernung, Kennzeichen-Kreis, Namensendung, Landkreis-Zugehörigkeit. („Doppelt so groß, 9 km weiter, und trotzdem hat der kleinere das Freibad.") Generierbar.
   - **(b) Erzählanschluss, Kann-Klasse:** gemeinsame Geschichte zweier Orte („teilten bis 1810 denselben Gerichtshof"). Nur wo die Datenbank ihn zufällig liefert, vermutlich selten. Kein Versprechen des Konzepts, kein Bauauftrag an die Pipeline, keine Feldtest-Aussage darf allein darauf beruhen. Der erste Solo-Test zeigt, dass (b) gut wirkt, wenn er da ist; das ändert nichts an seinem Status (Mike, 2026-10-01).
   - Höchstens ein Anschluss pro Reveal. Kein Fallback. Beobachtung, keine Frage.
5. **Reveal-Vertrag:** Eingabe ist die gewählte Option, **ein Optionssatz** (gespalten) oder **„uneinig"** (zersplittert), und optional ein Anschluss-Pin. Vier Template-Fälle (einstimmig richtig, einstimmig falsch, gespalten, zersplittert), Rotation der Einwebungs-Muster.
6. **Bekanntheitsfilter (neu, aus Feldtest Solo Freiburg, Protokoll 019):** Ein Fakt mit überregionaler Bekanntheit darf **nicht die Frage** tragen, wohl aber den Reveal. „Glottertal war Drehort der Schwarzwaldklinik" ist Allgemeinwissen; als Frage erzeugt es Wissensabruf (T1) statt Theorie (T2), als Steckbrief-Satz überrascht es trotzdem im Detail (der Klinikbetrieb lief während der Dreharbeiten weiter). Pipeline: eine Eigenschaft „Bekanntheit", die einen Fakt als Frage ausschließt, nicht als Reveal. **Gemessen wird der Fakt, nicht der Ort:** Glottertal ist klein, die Serie ist berühmt. Der Proxy ist die Bekanntheit der Sache, auf die der Fakt zeigt (Sprachversionen und Abrufe des Artikels über Serie, Person, Bauwerk), nicht die Prominenz des Gemeinde-Artikels; das Verfahren dafür liegt mit dem Fame-Index aus MixMi vor (Perzentil-Normierung, Schwelle als Parameter). Was Gemeinde-Achsen v0.5 §8.4 als Singleton-Gold führt (Drehort, prominente Persönlichkeit), gehört damit in Reveal und Steckbrief und trägt die Frage nur unterhalb der Schwelle. Die Schwelle ist publikumsabhängig und ergibt sich aus den W-Werten je Karte über mehrere Testpersonen (§10). Das ist die Content-Seite des begründbaren Ratens: Was man weiß, kann man nicht raten.

**Begriffe gegenüber Gemeinde-Achsen v0.5 (für Nr. 1–6 und §11 Nr. 6):** „Achse" heißt in diesem Dokument eine Eigenschaft im Sinne von v0.5 (Fakten-Typ mit Wert); v0.5 nennt „Achsen" dagegen seine Frageformen A–D. Die Fragefamilien A/B/C hier sind nicht die Frage-Achsen A/B/C dort: Radar ist hier Familie A und dort Achse C. Schicht 0 und 1 sind hier wie dort gemeint (frühere Fassungen dieses Konzepts zählten 0/1/2). Für Theorie-Distraktoren nach Nr. 1b setzt der Abstand von 50–100 km die erste Stufe des Distraktor-Pools aus v0.5 §10 (30 km) aus. Die Folgen für die Datenbank stehen in `gemeinde-achsen-entscheidungen-2026-10-01.md` (E4–E8).

**Vor dem Feldtest zu beantworten, aus den Daten der Gemeinde-Achsen Iteration 1, nicht im Feldtest:** Wie viele Orte haben ≥ 2 belastbare Schicht-2-Fakten (B-Quote)? Wie viele Orts-Paare liefern einen Vergleichsanschluss (fast alle) und wie viele einen Erzählanschluss (vermutlich wenige)?

### 8a. Was die Content-Seite schon mitbringt (Mike, 2026-10-01)

Zur Einordnung der Regeln oben, keine neue Entscheidung:

- **Vorhandene Datenbasis aus dem QuizAway-Vorgänger:** strukturierte Fakten aus mehreren Quellen für die größeren Orte, darunter Distanzen untereinander, Einwohnerzahlen, Bahnhöfe. Das ist Schicht 0 im Sinne der Gemeinde-Achsen und deckt für die größeren Orte Familie C, den Vergleichsanschluss (a), die Bingo-Felder und das Radar-Material (Nachbarn, Entfernungen). **PC-Befund 2026-10-01:** `data/staedte.json` enthält 2.051 Orte mit Stadtrecht; von den zehn Freiburg-Orten ist nur Staufen dabei. Die Spalte Kfz-Kennzeichen ist im Raum Freiburg fehlerhaft (Bad Krozingen und Staufen „FDS", Todtnau „TÜ"), und ein Eintrag „Gundelfingen a.d.Donau" trägt die Koordinaten von Gundelfingen im Breisgau. Für kleine Orte kommt Schicht 0 deshalb aus Wikidata, und der Vergleichsanschluss über den Kennzeichen-Kreis ist bis zur Bereinigung nicht belastbar.
- **Kleine Orte, Ziel ~80.000 (Ortsschild-Ebene):** Wissen aus den Internetauftritten der Gemeinden selbst. Eine Zeile dort ist zugleich Frage und Antwort: „Der älteste Einwohner von Mühlhausen ist 107, ein Mann mit Vornamen Jürgen" liefert „Wie alt ist der älteste Einwohner?" samt Auflösung und Steckbrief-Satz. Das ist Schicht 1 und die Quelle für Familie A und B. Gegenüber Gemeinde-Achsen v0.5 (§11 Nr. 5, §14: Gemeinde-Webseiten „nicht in v0.x") ist das eine neue Entscheidung; sie ist als E4 nachgetragen. Die Datenbank wächst sukzessive; das Spiel muss mit lückenhafter Abdeckung leben, deshalb die Material-Regel in §1a.
- **Kategorien:** Solche Zeilen werden zu Fakten-Typen (Achsen) gesammelt. Mit wachsender Abdeckung entstehen Kategorien, die nicht einen Ort betreffen, sondern mehrere („ältester Einwohner" über alle Orte der Fahrt, „Ort mit den meisten Bahnhöfen"). Im Spiel sind das: der Vergleichsanschluss (zwei Orte), die Große Fahrtfrage (alle gespielten Orte) und Radar (Nachbarn). Mehr-Orte-Fragen brauchen keinen neuen Fragetyp; sie sind Familie A oder C mit Orten als Optionen.
- **Folge für den Negativnachweis:** Weil jede Zeile einer Achse zugeordnet ist, ist die Prüfung „welchen Wert hat diese Achse am Zielort?" eine Abfrage, keine Recherche. Das macht den Kontext-Spiegel (Nr. 1b) praktikabel, in den dort genannten Grenzen: Ein anderer Wert ist ein Nachweis, ein fehlender Wert nur bei vollständiger Quelle.
- **Granularität** (F1 aus dem Achsen-Konzept, politische Gemeinde vs. Ortsschild-Ebene) ist für die Spielmechanik unerheblich: Die Streckenquelle liefert „nächster Ort mit Material", egal auf welcher Ebene. Sie entscheidet aber, wie dicht die Fahrtkarte wird.

---

## 9. Berührungspunkte mit dem Transfer-Konzept v1.1

Ausgeschrieben in v0.2.4 (v0.2.3 verwies auf v0.2; zwei Punkte von dort gelten nicht mehr und sind berichtigt).

- **Kern-Interface (berichtigt):** v0.2 schrieb „ein Klick, vier Strings". Es gilt: zwei bis vier Optionen (Familie B im Auto: zwei), ein Tap im Grundfall. Zuruf ist Beifahrer-Tap nach Ruf.
- **Antwortform (berichtigt):** Die Antwort ist eine Option, ein Optionssatz (gespalten) oder „uneinig" (zersplittert). Das sind die Erweiterungen der Kern-Schnittstelle. Wer-glaubt-wem ist keine zweite Abgabe mehr; die Einschätzungen bleiben mündlich und unaufgezeichnet (§3.2, §6).
- **Kipp-Kriterium v1.1 §2 ist ausgelöst:** v1.1 legt immer vier Optionen, genau einen `chosenIndex` und einen Zeit-Score fest und nennt als Kipp einen „realen Konsumenten mit anderer Antwortform". Der Reise-Modus ist dieser Konsument: andere Optionszahl, Antwort als Menge oder „uneinig", kein Zeit-Score. Das Schema wird in der PC-Session (§11 Nr. 7) neu geschnitten, nicht vorher.
- **Projektion:** Radar ist dieselbe Frage mit anderer Darstellung und auch ohne Karte stellbar.
- **Leiter:** Ablaufmodifikator über C, kein Fragetyp. Modellieren als Sequenz über dem Kern.
- **Reveal-Vertrag:** Eingabe ist Option, Optionssatz oder „uneinig", dazu optional ein Anschluss-Pin; vier Template-Fälle (§8 Nr. 5). Erweiterung gegenüber dem MixMi!-SteckbriefModal.
- **Host-Screen (Auto):** Mehrfachauswahl, „uneinig"-Button, „Gleich"- und „Jetzt"-Tap als Push-Korrektur.
- **Streckenquelle:** eigener Baustein vor dem Kern, liefert „nächster Ort mit Material", führt intern zwei Zähler (passiert, ausgespielt). Prüfen, ob die v5-Route so geschnitten ist.
- **Push/Pull:** ein Flag beim Start, kein eigener Modus.
- **elapsedMs:** vorhanden, nie angezeigt, nie gewertet. Fern-Duell unverändert.
- **Rahmen:** verändern den Core-Loop nicht; die Fahrtkarte hält Zustand, Bingo nimmt Eingaben. Fahrtende ist ein eigener Zustand mit „Ort der Fahrt".
- **Gemeinde-Achsen v0.5, Status-Satz „Spielmechanik 1:1 aus bestehendem QuizAway":** für den Reise-Modus überholt.

---

## 10. Feldtest

**Zwei Content-Stufen, getrennt ausgewiesen:**
- **Stufe 1, handgeschrieben (Obergrenze):** Mike schreibt die Karten. Misst, ob der **Kern** überhaupt trägt, wenn der Content so gut ist, wie ein Mensch ihn macht. Fällt K1 hier, liegt es am Kern, nicht an der Pipeline.
- **Stufe 2, generiert (Pipeline):** Karten aus Gemeinde-Achsen Iteration 1 (Prompt, Achsen-Regeln, Negativnachweis), Mike kuratiert nur. Misst, ob die **Pipeline** liefern kann, was der Kern braucht. Stufe 2 ist die Hauptaussage für die Implementierung; Stufe 1 darf sie nicht ersetzen. **Voraussetzungen (v0.2.4):** Iteration 1 liefert Fakten, keine Karten; dazwischen liegt ein Karten-Prompt (Frage, Theorie-Optionen, Reveal, Anschluss), der in `quizaway-stufe2-vorbereitung-2026-10-01.md` steht. Die zehn Freiburg-Orte liegen höchstens 27 km auseinander; für den Kontext-Spiegel laufen deshalb zehn Spenderorte im Band 50–100 km mit. Zähringen und Günterstal werden als Ortsteile von Freiburg geführt.
- Jede Karte trägt ihre Stufe und bei Anschluss ihre Klasse (a/b).

**Theorie-Klassifikation vor dem Reveal, in allen Tests:** T0 keine Theorie („keine Ahnung"), T1 Auswahl ohne Begründung („ich nehme die Zwei"), T2 konkrete Theorie mit Begründung („Zwei, weil der Name wohl vom Bach kommt"), **W gewusst oder wiedererkannt** (aus Allgemeinwissen oder aus einer früheren Karte der Fahrt; mit Vermerk, woher). W ist kein Durchtippen und keine Theorie; W je Karte über mehrere Personen ist das Maß für den Bekanntheitsfilter (§8 Nr. 6) und für die Spender-Regel (§8 Nr. 1). Im Auto stellt der Beobachter fest, ob aus Zuruf und Diskussion T2 hervorgeht; Begründung bleibt freiwillig.

**Reihenfolge:** Solo am Tisch zuerst, dann Bahn-Gruppe am Tisch, dann Auto auf der Straße.

**Solo am Tisch:** gewürfelte Strecke, 10 Orte aus einem der Testperson unbekannten Raum (im Bogen vor Beginn notieren: kennt die Person den Raum?). Mindestens drei Karten mit Vergleichsanschluss (a), höchstens eine mit Erzählanschluss (b), zwei Radar verbal. Leere Streckenkarte zum Pinnen. **Methode: Think-Aloud.** Die Testperson wird vor Beginn instruiert, alles laut zu sagen, was ihr durch den Kopf geht, vom Lesen der Frage bis nach dem Umdrehen; der Beobachter fragt nicht nach, er protokolliert nur. Das liefert T0/T1/T2 vor dem Umdrehen (K3b) und die drei K1-Teile nach dem Umdrehen, ohne dass Nachfragen die Immersion stören. Erst wenn Think-Aloud versiegt, darf der Beobachter einmal pro Ort nachfragen („erklär mir den Ort"), und das wird als Nachfrage markiert. K3a nur mit drei simulierten Unterbrechungen, sonst entfällt. Abschluss mit „Drei Dinge".

**Bahn-Gruppe am Tisch:** gewürfelte Strecke, 8 Orte, zwei bis drei Personen. 3 Radar mit Punktekarte, 3 Lügen-Steckbriefe (drei Aussagen, formgleich), 2 Wer-glaubt-wem mündlich. Eine Bingokarte nur für eine künstliche ortsarme Strecke von drei Orten. Protokoll: Zeigen, Diskussionsdauer, Bingo-Ablenkung, Nachschlag-Wunsch ohne Angebot, Formerkennung der Lüge.

**Auto auf der Straße:** echte Fahrt, 10 Orte, Beifahrer liest, möglichst zwei Besetzungen (zwei Personen und drei bis vier Personen). 5 Behauptungen (2 Radar verbal mit Fahrtrichtung, 2 mit flachen Distraktoren als Kontrolle: **Hypothese** T2-Rate und Kommentar nach dem Ergebnis sind bei Theorie-Distraktoren höher), 3 Lügen zu zwei Aussagen, 2 Leitern (nur bei drei und mehr Personen). Protokoll: gleichzeitiges Rufen, **Spaltungen und Zersplitterungen getrennt**, „Jetzt"- und „Gleich"-Taps (Papier: Beifahrer sagt es an), Wiederholungen bei B **als Belastungsindikator**, Kommentar nach dem Ergebnis, Dauer pro Schritt, Beifahrer nach fünf Orten, Leiter-Begründungen, am Fahrtende der Ort der Fahrt und ob die Trefferzahl kommentiert wird, abends Weitererzählen.

**Übergreifende Frage:** Erzeugt „Ich habe eine Theorie" (T2) einen anderen Spielzustand als „Ich möchte die Information wissen" (T0/T1)? Dazu: Macht der Reveal aus der Theorie eine Geschichte (K1 Teil 3)? Erzeugt der Anschluss Neugier auf den nächsten Ort, ohne künstlich zu wirken (K7)? Wenn eines scheitert, ist erkennbar welches, ohne Kern, Modi, Streckenquelle oder Rahmen wieder aufzubrechen.

---

## 11. Nächste Schritte

1. ~~Mike-Freigabe~~ erteilt. ~~Erster Solo-Test Stufe 1~~ gelaufen (Protokoll 019): Theoriebildung findet statt (6 von 10 T2), Erzählanschluss wirkt, Bekanntheitsfilter als neue Content-Regel. ~~PC-Prüfung~~ gelaufen (Anhang D).
2. Zweite Solo-Testperson mit **Kartensatz Fassung 2** (`quizaway-feldtest-solo-kartensatz-freiburg-v2-2026-10-01.md`): Lügen der Karten 3 und 10 streckenfremd ersetzt, Karte 6 als Bekanntheits-Kontrolle, acht Karten unverändert als Vergleichsbasis. Bogen vollständig (K1 dreiteilig, K3a, Lesedauer, Formerkennung, Kürzel W, Raumkenntnis). Vorher im Rohbogen der ersten Person nachsehen, ob bei Karte 3 oder 10 Gundelfingen genannt wurde. **Die Karten bleiben im Format des ersten Tests (A6).** Papier-Screens der Oberfläche (Telefon-Ausschnitt, neue Reihenfolge der Rückseite) sind ein eigener Test mit einer weiteren Person oder am Bahn-Gruppen-Tisch; im zweiten Solo-Test würden sie den Vergleich mit der ersten Person zerstören.
3. Bahn-Gruppe am Tisch mit derselben Strecke.
4. Gemeinde-Achsen Iteration 1 mit den zehn Freiburg-Orten **und zehn Spenderorten**, danach Karten-Prompt (`quizaway-stufe2-vorbereitung-2026-10-01.md`); liefert B-Quote, Anschluss-Quoten und Stufe-2-Karten. **Erzählanschlüsse (b) sind eine Kann-Klasse (Mike, 2026-10-01):** Sie werden gespielt, wo die Daten sie zufällig hergeben, und sonst nicht; kein Prüf- oder Bauauftrag an die Pipeline, keine Abhängigkeit des Solo-Modus davon. Ob eine Achse „gehörte zu" sie billig liefert, darf Iteration 1 nebenbei notieren, mehr nicht.
5. Protokolle beider Stufen → Spielkonzept v1.0 → Implementierungsfreigabe.
6. Content-Regeln §8 (jetzt sechs) ins Achsen-Regelwerk; die Begriffs-Übersetzung aus §8 gilt dabei.
7. Danach PC-Session gegen Transfer-Konzept v1.1 und Code; Ausgangspunkt ist das ausgelöste Kipp-Kriterium (§9).
8. **Parallel: Benutzungsoberfläche und Design.** Die UI-Runde mit den Reviewpartnern ist gelaufen (Handy, 2026-10-01); maßgeblich ist das **UI-Konzept v0.2** (`quizaway-ui-konzept-reise-modus-v0.2-2026-10-01.md`). Offen daraus: eine kurze Nachfrage zu vier Themen (`quizaway-oberflaeche-review-briefing-runde5-2026-10-01.md`), der Blick auf Hell und Dunkel im Auto, und ein eigener Papier-Test der Screens. Das betrifft die Oberfläche, nicht die Mechanik.

Keine weitere Review-Runde über die Mechanik. Runde 4 ist mit fünf Reviews vollständig.

---

**These:** Ein Reiseführer, der erst eine eigene Theorie verlangt und danach die Antwort erzählt. Das Fundament ist entschieden, in jeder Situation gleich. Der Witz liegt im Festlegen, pro Sitzplatz anders. Beides ist jetzt so geschrieben, dass der Feldtest es widerlegen kann. Das ist der Zweck dieser Version.

*Ende Spielkonzept v0.2.5. Anhang A (Rulings Runde 3) steht in v0.2 (`quizaway-spielkonzept-reise-modus-v0.2-2026-10-01.md`).*

---

## Anhang B — Rulings Runde 4

Vier Reviews (R4-A bis R4-D). Alle vier: feldtestfähig nach Schließungen, keine neue Mechanik. Übereinstimmend als wichtigste Punkte genannt: Anschluss begrenzen und definieren (A, B, C, D), Auto-Beifahrer als Nadelöhr (A, B), Fahrtbilanz ehrlich (A, B, C).

### Angenommen

| Finding | Von | Ruling |
|---|---|---|
| „Reveal verändern" vs. Anschluss | A | Semantischer Reveal identisch, Ergänzungen erlaubt (§3.4) |
| „Genau drei Dinge" stimmt nicht | A | Modus definiert Bedienung und Festlegung, Rest folgt, Zusatzschichten separat (§3) |
| Anschluss §1 allgemein vs. §3.3 solo | B | Kernbaustein in allen Modi, solo besonders wichtig (§1, §3.3) |
| Anschluss: kein Fallback, nur eigenständig interessant | A | §1, §5 |
| Anschluss: Beobachtung, keine neue Frage | A | §1 |
| Anschluss: unterdefiniert, welche Achsen | B | Content-Regel §8 Nr. 4 mit Achsenliste |
| Anschluss: zwei Klassen, Erzählanschluss nicht generierbar | C (Blocker 2) | Vergleichs- und Erzählanschluss getrennt, kein Versprechen auf (b) (§8) |
| Anschluss: Kette bricht bei übersprungenem Ort | D | Bezug auf letzten tatsächlich gespielten Pin (§1) |
| Zwei-Personen-Auto ist Betriebsgrenze, nicht Kipp | B | Eingeschränkter Modus: keine Leiter, C nur Spannen (§3.1). TTS-Vorziehen abgelehnt, Mike hat entschieden. |
| Familie B im Auto von vornherein zwei Aussagen | B (Konsequenz aus R3-E) | Angenommen; Drei-Aussagen bleibt Bahn (§2, §3.1). Revidiert gegenüber v0.2, weil der Kipp „Beobachtung nach Schaden" war. |
| Gespalten-Fall UI unspezifiziert | B, D | Multi-Select zwei Haken plus Bestätigen (§3.1) |
| Verbal-Radar ohne Himmelsrichtungen | C | Fahrtrichtung und Entfernung (§2) |
| Fahrtende fehlt | B | Eigener Schritt (§4) |
| Fahrtbilanz: „Lacher" kein Datenpunkt, Zahl ehrlich benennen | A, B, C | „Spaltungen" statt „Lacher"; Bilanz mit Zahl, kein Wettkampf-Score, Feldtest fragt nach Druck (§4) |
| Leiter-Taktung inkonsistent | B | „jede zweite C-Frage" (§2, §5) |
| Wortzahlen verbindlich | B | §1 Schritt 2 |
| „Gleich"-Tap für Push-Unterbrechungen | B | §1, §3.1 |
| Varianzregel | B | §1 Schritt 2 |
| GPS-Verlust → Route | B | §1a |
| Bahn-Definition „Ort an der Strecke" | B | Korridor-Regel (§1a) |
| Autobahn-Leerläufe | B | „Aus der Nähe"-Ergänzung der echten Fahrt (§1a). Bingo im Auto als Alternative abgelehnt. |
| Stilles Überspringen: intern zählen, UI-Marke per Feldtest | A, D | §1a |
| K5 messbar machen | A | Drittel-Regel oder wahrgenommene Leere (§1a) |
| K1 dreiteilig | A | §7 |
| K3b: Theorie primär, Lesedauer sekundär; T0/T1/T2 | A | §7, §10 |
| K3a am Tisch misst nichts | C | Simulierte Unterbrechungen oder entfällt (§7, §10) |
| K1 solo: wer fragt ab | C | Laut-Wiedergabe an Beobachter (§10) |
| Kontrollbedingung ohne Hypothese | C | Hypothese benannt (§10) |
| Solo-Vorschau: Absicht oder Fehler | C | Absicht, nur Ortsnamen (§3.3) |
| Wer-glaubt-wem: was wird getippt | B, C | Einschätzung mündlich, unaufgezeichnet; getippt wird die Frage-Antwort (§3.2) |
| Familie B: Formgleichheit beobachten | A | Content-Regel und Protokoll (§8, §10) |
| Wiederholungen als Belastungsindikator | A | §10 |
| Bingo solo gleich begrenzen | A | §4 |
| „K5-Ersatz", „K6 (Gesprächswert)", „Fahrtkarte endet" | A | Formulierungen korrigiert |
| Handgeschriebener Content testet Mike, nicht das System | C (Blocker 1) | Zwei Content-Stufen, getrennt ausgewiesen; Stufe 2 aus Iteration 1 ist die Hauptaussage (§10). Nicht übernommen: Stufe 1 erst nach Stufe 2, weil Iteration 1 noch nicht läuft und Stufe 1 den Kern isoliert misst. |
| B-Quote ist Datenbankabfrage | C | §8, als Aufgabe für Iteration 1 |
| Anhang-A-Kosmetik (Radar-Rahmen „überholt" statt „zu früh") | B | Zur Kenntnis; Anhang A bleibt historisch, Ruling gilt als überholt. |

### Abgelehnt

| Finding | Von | Warum nicht |
|---|---|---|
| Mehrheits-Balken aus den Antworten dieser Fahrt ab Frage 5 | B | Ein Balken pro Frage braucht viele Antworten auf **dieselbe** Frage. Antworten dieser Fahrt sind Antworten auf verschiedene Fragen von zwei bis vier Personen. Daraus entsteht keine Verteilung. Bleibt zurückgestellt bis Streckendaten. |
| Bingo im Auto als Lückenfüller | B | Fahrer-Ausschluss und Aufmerksamkeit unverändert; „aus der Nähe" löst das Leerlauf-Problem ohne Parallelspiel. |
| TTS für Zwei-Personen-Betrieb vorziehen | B | Von Mike entschieden: optional, später. Eingeschränkter Modus stattdessen. |
| Patt-Regel „zuletzt gerufen" doch akzeptieren | B | Durch Multi-Select-UI erledigt; „zuletzt gerufen" würde die Spaltung weiter verstecken. |
| „Dramaturgie profitiert" ist Gummiparagraph | B | Bewusst weich: eine harte Regel würde das Urteil nachschieben, wo die Geschichte es schon gesagt hat (A12 aus Runde 3). Feldtest zeigt, ob die Weichheit missbraucht wird. |

*Ende Anhang B.*

---

## Anhang C — Rulings zum nachgereichten Review R4-E

Fünf Findings, gegen Anhang B geprüft. Zwei sind neu, drei präzisieren Bestehendes.

### Angenommen

| Finding | Ruling |
|---|---|
| **Völlige Zersplitterung im Auto** (alle rufen verschieden) ist undefiniert | Neu. Dritter Festlegungs-Fall „zersplittert" mit eigenem „uneinig"-Button und viertem Reveal-Template (§1, §3.1, §8 Nr. 5). **Nicht übernommen:** der Vorschlag, der Beifahrer wähle die „lustigste" Theorie; das wäre die in Runde 3 verworfene „lauteste Theorie" durch die Hintertür. |
| **GPS-Fallback / „Force Push"** | Neu als Gegenstück zum „Gleich"-Tap: „Jetzt"-Tap löst den nächsten Ort mit Material sofort aus (§1, §3.1). Der Wechsel auf geplante Route bei GPS-Verlust (§1a) bleibt daneben bestehen. |
| **Kontext-Spiegel** als praktikable Generierungsregel statt hartem Negativnachweis | Präzisierung von §8 Nr. 1: Weg (b) mit Abstandsregel (außerhalb der direkten Nachbarschaft, 50–100 km, gleiche Größenklasse) plus Achsenprüfung am Zielort. Der Abstand ist das neue Element; die Achsenprüfung war bereits gemeint und ist jetzt ausgeschrieben. |
| **Think-Aloud** für den Solo-Tisch | Präzisierung von §10: Methode benannt, Nachfragen des Beobachters nur als markierter Rückfall. Ersetzt das vage „Laut-Wiedergabe an den Beobachter". |
| **„Welcher Ort war der Lacher der Fahrt?"** als Abstimmung am Ende | Angenommen als optionaler Schritt „Ort der Fahrt" am Fahrtende, Gruppe, ein Tap (§4). Löst das „Lacher"-Problem aus Anhang B anders als dort: Die App zählt keine Lacher, die Gruppe benennt einen. |

### Abgelehnt

| Finding | Warum nicht |
|---|---|
| **Trefferzahl radikal streichen** | Anhang B hat entschieden: Bilanz mit Zahl, ehrlich benannt, Feldtest fragt nach Druck. Neu in v0.2.2 ist die Konsequenz: Fällt die Zahl im Feldtest, besteht die Bilanz aus Orten, Pins und dem Ort der Fahrt (§4). Das Argument „widerspricht ‚Fun vor Korrektheit'" ist stark, aber ein Feldtest-Ergebnis, kein Konzept-Ruling. |
| **„3 Lacher, 2 mal völlig danebengelegen"** als Bilanzzahlen | „Lacher" ist kein Datenpunkt (Anhang B, R4-C). „Völlig danebengelegen" wäre zählbar (Zersplitterung oder einstimmig falsch), ist aber bereits durch „Spaltungen" in der Bilanz vertreten; eine zweite Fehlerzahl macht die Bilanz zum Score mit umgekehrtem Vorzeichen. |

### Ergänzung ohne Review-Herkunft

§8a hält fest, was die Content-Seite aus dem Vorgängerprojekt und dem Gemeinde-Achsen-Konzept bereits mitbringt (Mike, 2026-10-01). Das ändert keine Regel, zeigt aber, dass Kontext-Spiegel, Vergleichsanschluss und Mehr-Orte-Fragen auf Material aufsetzen, das es gibt oder das sowieso entsteht.

*Ende Anhang C.*

---

## Anhang D — Rulings zur PC-Prüfung (2026-10-01)

Grundlage: `quizaway-spielkonzept-v0.2.3-pruefung-pc-2026-10-01.md`, Fassung 2, Befunde B1–B10. Mike: „Die Entscheide alle gemäß den Vorschlägen."

| Befund | Ruling | Wo |
|---|---|---|
| B1 Stufe 2 aus zehn Freiburg-Orten allein nicht baubar | Zehn Spenderorte im Band 50–100 km; Karten-Prompt als eigener Schritt; Zähringen und Günterstal als Ortsteile von Freiburg | §10, §11 Nr. 4, Stufe-2-Vorbereitung |
| B2 „Nicht gesetzt" ist kein Negativnachweis | Kontext-Spiegel nur bei einwertiger Eigenschaft mit anderem Wert oder vollständiger Quelle; Weg (c) für erfundene Theorien benannt | §8 Nr. 1 |
| B3 Lügen-Hypothese vom Kartensatz nicht gedeckt | Hypothese zurückgenommen; Spender-Regel; zwei Vermutungen für Person 2; Kartensatz Fassung 2 | §8 Nr. 1 und 2, §11 Nr. 2 |
| B4 „Kern trägt" stärker als die Messung | Status-Block und §11 Nr. 1 auf das Gemessene zurückgeführt | Status, §11 |
| B5 T-Skala ohne „gewusst" | Kürzel W; Karte 6 bleibt als Kontrolle; Raumkenntnis im Bogen | §7, §10 |
| B6 Bekanntheit des Fakts, nicht des Orts | Proxy über die Sache, auf die der Fakt zeigt; Fame-Index-Verfahren; Abgleich mit v0.5 §8.4 | §8 Nr. 6 |
| B7 Begriffe gegenüber Gemeinde-Achsen v0.5 | Schichten wie v0.5 gezählt; Begriffs-Absatz in §8; E4–E8 im Achsen-Nachtrag | §2, §4, §8, §8a |
| B8 Verweise auf ältere Kriterien-Zählung | K3, K4, K9 durch die Namen der Kriterien ersetzt; Verweis auf Anhang A in v0.2 | §2, §3.1, §3.3, §8 Nr. 6, Anhang B |
| B9 §9 in zwei Punkten überholt | §9 ausgeschrieben und berichtigt; Kipp v1.1 §2 als ausgelöst vermerkt | §9 |
| B10 Radar: Himmelsrichtungen, Länge, Lösung immer der aktuelle Ort | Lösungsregel und eigene Längengrenze; die Testkarten bleiben für Person 2 unverändert (Vergleichsbasis) | §2 |

Nicht übernommen wurde nichts. Die Tatsachenfrage, ob die erste Testperson bei Karte 3 oder 10 Gundelfingen genannt hat, ist beantwortet: nein (Mike, 2026-10-01; Folge in §8 Nr. 2).

*Ende Anhang D.*

---

## Anhang E — Rulings zur PC-Prüfung des UI-Konzepts (2026-10-01)

Grundlage: `quizaway-ui-konzept-v0.1-pruefung-pc-2026-10-01.md` (U1–U12), Abschnitt C. Mike hat alle sechs Punkte mit „OK" entschieden. Hier stehen nur die Folgen für die Spielmechanik; die Folgen für die Oberfläche stehen im UI-Konzept v0.2.

| Entscheid | Folge im Spielkonzept | Wo |
|---|---|---|
| 1. Ziffern statt Buchstaben, „zwo" | Beschriftungsregel; Beispiele auf Ziffern umgestellt | §1 Schritt 2, §3.1, §10 |
| 2. Dunkel im Auto erst ansehen; Start nach Systemeinstellung | keine (reine Oberflächenfrage) | UI-Konzept v0.2 |
| 3. Zwei Handlungen zwischen Auflösung und nächster Frage in der Bahn, als Hypothese | Abweichung von „ein Tap" vermerkt, mit Kipp | §1 Schritt 5 |
| 4. Papier-Screens getrennt vom zweiten Solo-Test | zweiter Solo-Test bleibt im A6-Format | §11 Nr. 2 |
| 5. Auflösung höchstens 70 Wörter einschließlich Anschluss | neue Redaktionsregel; gilt für jede Karte, weil jede in allen Modi spielbar sein muss | §1 Schritt 2 |
| 6. Leiter als „höher / hier steige ich aus" | Form der Leiter bestimmt; kein Stopp mit Bank | §2, §3.1 |

**Nachtrag am selben Tag (Mike, vier weitere Entscheide zu UI-Konzept v0.2 §7):**

| Entscheid | Folge im Spielkonzept | Wo |
|---|---|---|
| 7. Eine Spaltung zählt nicht als Treffer, auch wenn eine Hälfte richtig lag | Zählung der Fahrtbilanz bestimmt | §4 Fahrtende |
| 8. Schrift im Auto fest, in der Bahn mit der Systemeinstellung wachsend | keine (Oberfläche) | UI-Konzept v0.2 |
| 9. Solo: Option wählen, dann „Festlegen" | Festlegung im Solo ist korrigierbar bis „Festlegen" | §3.3 |
| 10. Aussehen des Reise-Modus | keine (Oberfläche) | UI-Konzept v0.2, R-UI-19 |

*Ende Anhang E.*
