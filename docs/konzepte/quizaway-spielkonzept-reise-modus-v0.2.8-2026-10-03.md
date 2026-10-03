# QuizAway — Spielkonzept Reise-Modus v0.2.8

**Story-Satz:**
*Ein Ort wird zum nächsten Spielort. Das Spiel wirft eine Behauptung auf, die man sich zurechtlegen kann. Man legt sich fest. Der Ort erzählt, was wirklich ist, nimmt die eigene Theorie mit und knüpft, wenn es sich lohnt, an einen Ort davor an. Der Reiseführer ist das Fundament; wie man sich festlegt, ist pro Sitzplatz anders, und dort sitzt der Witz.*

---

## Status-Block

| | |
|---|---|
| **Version** | v0.2.8 (v0.2.7 plus die Politik-Regel für Rheinland-Pfalz, die Ausreißer-Karte und das Aus für Wappen-Karten, Anhang H). v0.2.7 war v0.2.6 plus die Nachträge vom 2. Oktober nach Faktencheck, Probe und drittem Volllauf, Anhang G). v0.2.6 war v0.2.5 plus zwei Vorgaben Mikes nach dem Stufe-2-Volllauf und zwei Antworten dazu, Anhang F. v0.2.5 war v0.2.4 plus zehn Entscheide Mikes zur PC-Prüfung des UI-Konzepts, Anhang E; die letzten vier als Nachtrag am selben Tag). v0.2.4 war v0.2.3 plus PC-Prüfung gegen Kartensatz, Protokoll, Gemeinde-Achsen v0.5 und Transfer-Konzept v1.1 (Anhang D). **Achtung Zählung:** v0.2.4 und v0.2.5 sind am PC entstanden; eine am Handy geplante „v0.2.4" ist nicht diese. |
| **Datum** | 2026-10-03 |
| **Status** | v0.2.2 von Mike freigegeben als Feldtest-Grundlage (2026-10-01, 12:29). Erster Solo-Test gelaufen (15:17): Theoriebildung findet statt (6 von 10 T2, kein Ermüdungstrend); K1 und K3a sind noch nicht einzeln erhoben. Stufe-2-Volllauf gelaufen (30 Vorschläge, alle regelgerecht; Bericht `quizaway-stufe2-volllauf-2026-10-01.md`). Seither drei Kartenläufe mit Faktencheck (Berichte `quizaway-stufe2-volllauf2-2026-10-01.md`, `-faktencheck-2026-10-02.md`, `-probe-v0.6-2026-10-02.md`, `-volllauf3-2026-10-02.md`); der Vorrat für den Raum Freiburg hat 129 geprüfte Karten, je Ort 11 bis 15. v0.2.7 ist die Grundlage für die zweite Solo-Person (Kartensatz Fassung 2), für den Feldtest Stufe 2 am Tisch (Kartensatz `quizaway-feldtest-stufe2-kartensatz-freiburg-2026-10-02.md`), für den nächsten Kartenlauf (Karten-Prompt v0.7) und für das UI-Konzept v0.2. Keine Implementierungsfreigabe; die kommt nach Stufe 2 (§11). |
| **Scope** | Spielmechanik des Reise-Modus: Auto-Gruppe, Bahn-Gruppe, Bahn-Solo, drei Streckenquellen. „Sofa" ist gewürfelte Strecke plus Display-Modus. Fern-Duell nicht Gegenstand. |
| **Provenance** | v0.2 → Runde 4 (R4-A bis R4-D) → Rulings Anhang B → v0.2.1 → R4-E → Rulings Anhang C → v0.2.2 → Feldtest Solo Freiburg → v0.2.3 (§8 Nr. 2, Nr. 4b und Nr. 6, §11) → PC-Prüfung → Rulings Anhang D → v0.2.4 → UI-Runde (Handy) → UI-Konzept v0.1 → PC-Prüfung → Rulings Anhang E → v0.2.5 → Stufe-2-Volllauf → Vorgaben Mike (E9, E10) → Rulings Anhang F → v0.2.6 → zweiter Volllauf → Faktencheck der 100 Karten → Entscheide Mike (2026-10-02) → Probe und dritter Volllauf mit Karten-Prompt v0.6 → Rulings Anhang G → v0.2.7 → zweiter Raum Neuwied → Wappen-Probe (verworfen) → Rulings Anhang H → v0.2.8. |
| **Entschieden (Mike)** | Ein Gerät. Beifahrer liest, TTS optional später. Kein Solo im Auto. |
| **Offen** | Nichts auf Konzeptebene. Alles Weitere entscheidet der Feldtest. |

**TL;DR gegenüber v0.2:** Keine neue Mechanik. Nur Schließungen: Der Anschluss ist Kernbaustein in allen Modi, hat zwei Klassen (Vergleich aus Achsen, Erzählung nur wo vorhanden), ist Beobachtung und nie neue Frage, bezieht sich auf den letzten gespielten Pin, und es gibt keinen Fallback. Familie B läuft im Auto als Zwei-Aussagen-Variante. Der Zwei-Personen-Betrieb im Auto ist ein eingeschränkter Modus, kein Kipp. Verbal-Radar nutzt Fahrtrichtung und Entfernung, keine Himmelsrichtungen. Fahrtende ist ein eigener Schritt. Wortzahlen sind verbindlich. Der Feldtest unterscheidet handgeschriebenen Content (Obergrenze, misst den Kern) von generiertem Content (misst die Pipeline) und klassifiziert Theorien in T0/T1/T2. Vier Formulierungsfehler sind korrigiert.

**Zusätzlich in v0.2.2 (aus R4-E):** Die Festlegung im Auto kennt jetzt drei Fälle statt zwei: einstimmig, gespalten, zersplittert. Ein „Jetzt"-Tap ist das Gegenstück zum „Gleich"-Tap, damit ein verspäteter GPS-Trigger den Moment nicht verpasst. Der Kontext-Spiegel ist als zulässige Generierungsregel für Distraktoren präzisiert. Think-Aloud ist die Methode für den Solo-Tisch. Am Fahrtende darf die Gruppe den „Ort der Fahrt" wählen, als Ersatz für die nicht zählbaren Lacher.

**Zusätzlich in v0.2.4 (aus der PC-Prüfung, Anhang D):** Keine neue Mechanik. Der Negativnachweis für gespiegelte Distraktoren gilt nur noch, wo er einer ist (einwertige Eigenschaft mit anderem Wert, oder vollständige Quelle). Der Spender eines gespiegelten Fakts darf kein Ort der Fahrt sein. Die Lügen-Hypothese aus v0.2.3 ist zurückgenommen und durch zwei prüfbare Vermutungen ersetzt. Die Theorie-Klassifikation bekommt das Kürzel W (gewusst oder wiedererkannt). Der Bekanntheitsfilter misst den Fakt, nicht den Ort. Radar bekommt eine Lösungsregel und eine eigene Längengrenze. §9 ist ausgeschrieben und in zwei Punkten berichtigt. Die Schicht-Begriffe folgen jetzt Gemeinde-Achsen v0.5; die Verweise auf eine ältere Kriterien-Zählung (K3, K4, K9) sind durch die Namen der Kriterien ersetzt.

**Zusätzlich in v0.2.5 (aus der Prüfung des UI-Konzepts, Anhang E):** Optionen tragen Ziffern 1–4, im Auto gerufen und vorgelesen mit „zwo". Die Auflösung hat jetzt eine Längenregel: höchstens 70 Wörter einschließlich Anschluss. Die Leiter ist bestimmt: je Stufe „höher" oder „hier steige ich aus"; es gibt kein Stopp, das etwas sichert. In der Bahn liegen zwischen Auflösung und nächster Frage zwei Handlungen statt einer, als Hypothese mit Kipp. Papier-Screens der Oberfläche werden getrennt vom zweiten Solo-Test geprüft.

**Zusätzlich in v0.2.6 (aus dem Stufe-2-Volllauf, Anhang F):** Keine neue Mechanik, zwei Content-Regeln. Ein bekannter Fakt darf die Frage tragen; die Frage zielt dann auf ein Detail (§8 Nr. 6, neu gefasst). Jeder Ort hat einen Vorrat von mindestens sieben Karten, gemischt aus Geschichten und Klassikern der Grunddaten samt Politischem (§8 Nr. 7, neu). Gespielt wird weiter eine Frage je Ort. Familie C nimmt ihre Zahl in der Regel aus den Grunddaten; eine Zahl aus dem Artikel ist erlaubt, wenn der Steckbrief einen Anhalt zum Schätzen gibt (Nachtrag 2026-10-02). Der Anschluss hängt am Ortspaar, nicht an der Karte.

**Zusätzlich in v0.2.7 (aus Faktencheck, Probe und drittem Volllauf, Anhang G):** Keine neue Mechanik; die Content-Seite bekommt ihr viertes Glied und drei Schärfungen. Keine Karte kommt ohne Faktencheck in den Vorrat; der Check ist Sache der Maschine, nicht des Kurators (§8 Nr. 8, neu). Seine Befunde hängen am Fakt selbst, und jede Karte ist an ihren Fakt gebunden; „derselbe Fakt" ist damit eine Abfrage (§8 Nr. 8). Sieben Karten je Ort sind die Untergrenze, nicht das Ziel; die Grenze nach oben liegt vorläufig bei zwanzig (§8 Nr. 7). Ein Stadtteil bekommt sein eigenes Wahlergebnis, ein dünner Ortsartikel eine zweite Quelle, die Höhe trägt nur bei einigen Quellen eine Karte, und das Kennzeichen gilt nicht mehr als einwertig (§8 Nr. 7). Nennt ein Fakt den Ort davor nur als Teil eines Namens, darf das den Anschluss tragen, als Kann (§8 Nr. 4c).

**Zusätzlich in v0.2.8 (zweiter Raum, Wappen-Probe, Anhang H):** Keine neue Mechanik, drei Content-Regeln. Zählt die Verbandsgemeinde die Briefwahl für ihre Gemeinden, gibt es kein vollständiges Gemeindeergebnis; die Politik-Karte fragt dann nach der Verbandsgemeinde und sagt das (§8 Nr. 7). Neu ist die Ausreißer-Karte: ein Gebiet, das anders wählt als das Gebiet, zu dem es gehört, als Klassiker der Politik mit eingebauter Theorie (§8 Nr. 7). Wappen tragen keine Karte; eine neue Fragenfamilie geht zuerst als kleine Probe an Mike (§8 Nr. 7). Nachtrag am selben Tag: Die Ausreißer-Karte ist Sonderfall eines Rekord-Blicks – vom Ort aus wird gefragt, ob er auf einer Ebene von Kreis bis Welt an der Spitze, am Ende oder allein steht (§8 Nr. 7).

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
- Die Quelle liefert nur Orte **mit Material**. Ein Ort ohne Material wird still übersprungen, nie als leere Frage ausgeliefert. **Intern** werden zwei Größen geführt: relevante Orte passiert, Orte ausgespielt. Ob das Überspringen im UI sichtbar wird (dezente Marke „Ort passiert, kein Material"), entscheidet der Feldtest: Fragt jemand, warum die App stumm blieb, kommt die Marke. **Seit v0.2.6** hat jeder Ort mit Grunddaten Material, weil die Klassiker zum Vorrat gehören (§8 Nr. 7). Die Frage verschiebt sich damit von „gibt es Material?" zu „welche der passierten Orte spielt die Fahrt?"; das ist nicht entschieden (§11 Nr. 9).
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
| **A — Behauptung** | Frage, vier Theorien als Optionen | Schicht 1 für die wahre Option, bei Klassikern Schicht 0 (§8 Nr. 7); Distraktoren mit Negativnachweis (§8) | Standard |
| **B — Lüge** | Bahn: drei Aussagen, eine gelogen. **Auto: zwei Aussagen, eine gelogen** („Eine der beiden stimmt nicht") | ≥ 2 belastbare Schicht-1-Fakten; Lüge mit Negativnachweis (§8) | Nur wo Daten reichen, sonst A. Aussagen ≤ 8 Wörter, gleich lang, gleich detailliert. |
| **C — Größenordnung** | Zahlenfrage ohne Zahlen: Epochen, Spannen | Schicht 0 numerisch; Zahlen aus dem Artikel nur mit Anhalt im Steckbrief (§8 Nr. 7) | Höchstens jede dritte Frage, nie zwei hintereinander |

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

- Eine Frage pro Ort. Nachschlag nur über den Pin. Frage und Nachschlag kommen aus dem Vorrat des Orts (mindestens sieben Karten, §8 Nr. 7); der Vorrat ändert die Taktung nicht.
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
- **K3b — Solo, Durchtippen:** **Primär:** Wird vor dem Reveal noch eine konkrete Theorie gebildet (T2, §10)? **Sekundär:** Lesedauer Ort 2 vs. Ort 10, nur als Indikator. Wenn nur noch durchgetippt wird, ist es Informationsabfrage, kein Spiel. Eine gewusste oder wiedererkannte Antwort (W, §10) ist kein Durchtippen und zählt nicht gegen den Kern. Seit v0.2.6 zählt sie auch nicht mehr gegen die Karte: Ein Glückstreffer ist erwünscht (§8 Nr. 6); W bleibt Messung.
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
   - **(c) Namensteil-Anschluss, Kann-Klasse (neu in v0.2.7; Mike, 2026-10-02: „ja, als Kann"):** Nennt ein Fakt den Ort davor nur als Teil eines Namens (der Herzog von Zähringen in St. Peter, kurz nach Zähringen), darf das den Anschluss tragen. Er trägt den Vermerk „(Namensteil)", und der Faktencheck prüft, ob der Name wirklich auf den Ort zurückgeht. Wie bei (b): kein Versprechen, kein Bauauftrag.
   - Höchstens ein Anschluss pro Reveal. Kein Fallback. Beobachtung, keine Frage.
5. **Reveal-Vertrag:** Eingabe ist die gewählte Option, **ein Optionssatz** (gespalten) oder **„uneinig"** (zersplittert), und optional ein Anschluss-Pin. Vier Template-Fälle (einstimmig richtig, einstimmig falsch, gespalten, zersplittert), Rotation der Einwebungs-Muster.
6. **Bekanntheit (neu gefasst in v0.2.6; Mike, 2026-10-01, E9):** Ein bekannter Fakt **darf die Frage tragen**. „Man freut sich, wenn man auch mal Glück mit einer Frage hat." Die Fassung bis v0.2.5 sperrte Fakten mit überregionaler Bekanntheit als Frage und ließ sie nur im Reveal zu. Im Stufe-2-Volllauf hielt das die Schwarzwaldklinik, Fausts Tod und die Hebungsrisse aus allen 30 Vorschlägen; die Staufen-Karten wurden regelgerecht und blass. Stattdessen gilt:
   - **Die Frage zielt auf ein Detail des bekannten Fakts**, das man nicht mitweiß, oder verbindet ihn mit einer zweiten Angabe: nicht „Wo wurde die Schwarzwaldklinik gedreht?", sondern etwa der Name der Klinik, die es dort wirklich gibt. So bleibt Raum für eine Theorie, und wer es trotzdem weiß, hat einen Glückstreffer.
   - **Der bekannteste Fakt eines Orts gehört in dessen Vorrat** (Nr. 7), nicht nur in den Reveal.
   - **Gemessen wird weiter, gesperrt wird nicht:** Jede Karte trägt eine Einschätzung der Bekanntheit, und das Kürzel W (§10) wird je Karte gezählt. Beides ist Messung und kein Ausschlussgrund. Wie viele leichte Karten eine Fahrt verträgt, ist nicht festgelegt; Mike hat keine Zahl genannt, der Feldtest zeigt es an W je Fahrt.
   - Unverändert aus v0.2.4: Gemeint ist die Bekanntheit der Sache, auf die der Fakt zeigt, nicht die des Orts (Glottertal ist klein, die Serie ist berühmt). Das Fame-Index-Verfahren aus MixMi bleibt der vorgesehene Proxy, jetzt als Angabe an der Karte und nicht als Schwelle.
7. **Fragenvorrat je Ort (neu in v0.2.6; Mike, 2026-10-01, E10):** Jeder Ort hat einen **Vorrat von mindestens sieben Karten**, auch ein kleiner; größere Orte dürfen mehr haben. „Sieben Fragen" meint den Vorrat, nicht sieben Fragen hintereinander (Mike, 2026-10-01): Gespielt wird weiter eine Frage je Ort (§5); der Nachschlag über den Pin und jede spätere Fahrt ziehen aus dem Rest. **Sieben ist die Untergrenze, nicht das Ziel (Mike, 2026-10-02):** Die Fragen seien so interessant gemacht, dass es auch für einen kleinen Ort mehr als sieben geben darf, wenn die Fakten das hergeben, „also fast beliebig viele – wobei es irgendwo eine Grenze geben muss". Eine Zahl für die Grenze hat Mike nicht genannt. Vorläufig gilt, von der PC-Seite gesetzt und von Mike noch zu bestätigen: je Kartenlauf höchstens zehn Karten (sieben Pflicht, bis zu drei Zusatzkarten), im Vorrat eines Orts höchstens zwanzig; wonach bei mehr als zwanzig ausgewählt wird, ist offen (§11 Nr. 10). **Stand nach drei Läufen (v0.2.7):** Die Grenze ist nirgends erreicht; der vollste Vorrat hat 15 Karten. Die Zusatzkarten sind keine schwächeren (von 16 sind 11 bestätigt und 5 korrigiert), und vier von sieben Läufen hörten vor der zehnten Karte von selbst auf, weil kein tragfähiger Fakt mehr da war.
   - **Derselbe Fakt, eine Karte (neu in v0.2.7; Mike, 2026-10-02):** Tragen zwei Kartenläufe denselben Fakt, bleibt die Karte des jüngeren Laufs im Vorrat. Ein Fakt mit mehreren Sachen (ein Kloster mit erster Erwähnung, Flucht und Aufhebung) darf mehrere Karten tragen. Was „derselbe Fakt" ist, steht in Nr. 8.
   - **Zwei Sorten Karten.** *Geschichten-Karten* aus Schicht 1 (Herkunft, Grund, Ereignis) wie bisher. *Klassiker* aus den Grunddaten (Schicht 0): Einwohner, Fläche, Höhe, Kfz-Kennzeichen, Landkreis, Ersterwähnung, Entfernungen, Bahnhof; dazu **Politisches**: stärkste Partei, Wahlergebnis, Bürgermeister. Die Klassiker gibt es für jeden Ort. Ein dünner Artikel (Zähringen: 570 Wörter) ist damit kein Grund mehr für einen leeren Ort.
   - **Kein neuer Fragetyp** (§3.4). Zahlen laufen als Familie C (Spannen oder Leiter), Zugehörigkeiten (Kennzeichen, Landkreis, Partei) als Familie A. Für Familie C sind die Grunddaten der Normalfall. **Eine Zahl aus dem Artikel ist erlaubt, wenn der Steckbrief einen Anhalt zum Schätzen gibt** (Mike, 2026-10-02): Die Übernachtungen in St. Peter, gemessen an der Einwohnerzahl, sind „für so ein kleines Dorf eine schöne überraschende Zahl". Ohne Anhalt (eine Dammhöhe) bleibt eine Zahl aus dem Artikel draußen. Die erste Fassung von v0.2.6 hatte Zahlen aus dem Artikel ganz ausgeschlossen; das war eine Folgerung, kein Entscheid, und Mike hat im Kuratierblatt zwei solche Karten zu seinen liebsten gewählt.
   - **Negativnachweis bei Klassikern:** Die Eigenschaften sind einwertig und stammen aus vollständigen Quellen (Nr. 1b); jede andere Partei und jeder andere Landkreis ist damit falsch. **Das Kennzeichen ist nicht einwertig (berichtigt in v0.2.7; Faktencheck F4):** Kreise geben frühere Kennzeichen wieder aus, der Landkreis Breisgau-Hochschwarzwald seit dem 2. Oktober 2023 neben FR auch MÜL und NEU an alle Einwohner. Eine Kennzeichen-Karte fragt deshalb nach dem Hauptkennzeichen und führt kein weiteres Kennzeichen desselben Kreises als falsche Option; das ist eine Folgerung aus dem Befund, kein eigener Entscheid. Nennen die Quellen zu einer Zahl verschiedene Werte (Höhe von Horben: 495 m und 607 m), trägt sie nur dann eine Karte, wenn alle Werte in derselben Spanne liegen. **Die Höhe trägt nur eine Karte, wenn die Quellen sich einig sind (Mike, 2026-10-02);** umgesetzt als: Die Quellwerte liegen höchstens fünf Prozent auseinander.
   - **Politik-Karte bei Stadtteilen (neu in v0.2.7; Mike, 2026-10-02):** „Die amtlichen Ergebnisse gibt es auch immer auf Ebene der Kommune, also Stadtteilergebnis holen." Ein Stadtteil fragt nach seinem eigenen Wahlergebnis, nicht nach dem der ganzen Stadt. Für Freiburg kommt es aus dem Open-Data-Angebot des städtischen Wahlportals, Ebene Stadtbezirke; Zähringen und Günterstal haben seit dem dritten Lauf ihr eigenes Ergebnis.
   - **Briefwahl der Verbandsgemeinde (neu in v0.2.8; Mike, 2026-10-02: „so lassen“):** In Rheinland-Pfalz zählen kleine Gemeinden ihre Briefwahl oft nicht selbst aus; das tut die Verbandsgemeinde für alle zusammen. Die Summe der Gemeinde enthält dann nur die Urnenstimmen und ist kein Ergebnis der Gemeinde. Die Politik-Karte fragt in diesem Fall nach dem Ergebnis der Verbandsgemeinde und sagt das in Frage und Auflösung (Dierdorf, Linz am Rhein). Erkannt wird der Fall an der Briefwahlzugehörigkeit in der Wahlbezirksstatistik, nicht am Land; dieselbe Lage kann es auch anderswo geben, wo Gemeinden die Briefwahl gemeinsam auszählen. In Freiburg zählen alle acht Gemeinden selbst aus (nachgeprüft). **Es zählt immer nur das Gesamtergebnis, Urne und Brief (Mike, 2026-10-03);** ein Ergebnis nur aus den Urnen trägt weder eine Karte noch einen Vergleich. Der Landeswahlleiter Rheinland-Pfalz begründet die Lage so: Briefwahlbezirke in jeder Ortsgemeinde zu bilden, sei organisatorisch nicht leistbar; die bei der Verbandsgemeinde ausgezählten Briefwahlstimmen können den einzelnen Ortsgemeinden nicht zugeordnet werden, für die allermeisten Ortsgemeinden gibt es daher nur das Ergebnis der Urnenwahl (wahlen.rlp.de, Ergebnisservice, abgerufen 2026-10-03). Ein Gesamtergebnis gibt es dort für die Verbandsgemeinde und für die Gemeinden mit eigenem Briefwahlbezirk (Waldbreitbach, Leutesdorf).
   - **Stadtteil ohne Open Data (Folgerung in v0.2.8, ohne eigenen Entscheid):** Bietet die Stadt keine Ergebnisse je Stadtteil an (Neuwied), wird das Stadtteilergebnis aus den Stimmbezirken der Wahlbezirksstatistik und der Stimmbezirkseinteilung der Stadt summiert, Briefwahlbezirke eingeschlossen. Gegenprobe: Ein Briefwahlbezirk hat höchstens so viele Wählende, wie Wahlscheine ausgegeben sind. Hält die Gegenprobe nicht (Altwied: 244 gegen 236), gilt das Ergebnis nur ungefähr; dann trägt es nur eine Spanne mit „rund“, und ein knapper Rang trägt keine Karte.
   - **Ausreißer-Karte (neu in v0.2.8; Mike, 2026-10-02):** „Bei den Wahlergebnissen kann es interessante Ausreißer in Stadt/Kreis/Land geben.“ Ein Ausreißer ist ein Gebiet, das anders wählt als das Gebiet, zu dem es gehört. Mikes Beispiel, am amtlichen Ergebnis geprüft: Bei der Landtagswahl in Sachsen-Anhalt am 6. September 2026 ist Halle III der einzige der 41 Wahlkreise, in dem nicht die AfD die meisten Zweitstimmen hat (Grüne 33,7 %, AfD 18,3 %); das Direktmandat holte dort die Linke. So eine Karte ist ein Klassiker der Politik, der eine Theorie hervorruft: Man fragt sich, warum gerade hier.
     - *Was als Ausreißer zählt (Schwellen von der PC-Seite vorgeschlagen, von Mike bestätigt am 2026-10-03):* (a) Das Gebiet hat eine andere stärkste Partei als das übergeordnete Gebiet, und das ist selten: Höchstens drei Gebiete derselben Ebene im Land haben dieselbe Abweichung. (b) Oder ein Anteil weicht um mindestens acht Prozentpunkte vom übergeordneten Gebiet ab. Ebenen: Wahlkreis gegen Land, Gemeinde oder Stadtteil gegen Kreis. Ein Stadtteil gegen das Land zählt nicht, wenn seine Stadt als Ganzes schon so wählt (Zähringen, Günterstal: Stadtkreis Freiburg).
     - *Wahlkreis ist kein Ort:* Eine Karte über einen Wahlkreis hängt an ihm, gespielt wird sie an einem seiner Orte und höchstens einmal je Fahrt. Der Steckbrief nennt den Wahlkreis.
     - *Kein neuer Fragetyp:* Familie A („Welche Partei lag im Wahlkreis vorn?“, die Seltenheit steht in der Frage oder der Auflösung), Familie C (wie viele Wahlkreise des Landes, als Spannen), Familie B nur mit unangreifbaren wahren Aussagen.
     - *Urteil über die Probekarten (Mike, 2026-10-03):* „Machen mittelmäßig Freude und sollen wegen ihrer Relevanz dennoch drin bleiben.“ Form: Familie A zuerst, dann B, dann C und Leiter. **Hat ein Ort einen Ausreißer, steht die Karte in seinem Vorrat** (Pflicht, nicht Zusatz). Bei einem Wahlkreis-Ausreißer steht sie im Vorrat jedes seiner Orte der Fahrt; gespielt wird sie höchstens einmal je Fahrt.
     - *Erststimme ist nicht Mandat:* Seit der Bundestagswahl 2025 bekommt nicht jeder Wahlkreissieger einen Sitz; ohne Zweitstimmendeckung gingen 23 leer aus. Die Karte sagt „lag bei den Erststimmen vorn“; „Direktmandat“ nur, wenn der Sitz belegt ist. Vorn bei den Zweitstimmen und vorn bei den Erststimmen sind zwei verschiedene Aussagen (Halle III).
     - *Zählungen sind Superlative:* „Der einzige“, „einer von zwei“ werden aus dem amtlichen Ergebnis über die ganze Ebene gezählt, nie aus einer Meldung übernommen. Die Frage nennt Wahl und Jahr, die Auflösung den Stand. Nach der nächsten Wahl derselben Art ist die Karte veraltet und fällt aus dem Vorrat.
     - *Quellen:* Bundestagswahl aus der Wahlbezirksstatistik der Bundeswahlleiterin, summiert zu Gemeinde, Kreis, Wahlkreis und Land; Landtagswahlen von den Statistischen Landesämtern, als Option, wo eine Fahrt sie braucht.
     - *Probe an den beiden Räumen (Bundestagswahl 2025, Zweitstimmen, 2026-10-03):* Wahlkreis 281 Freiburg ist einer von zwei Wahlkreisen in Baden-Württemberg mit den Grünen vorn (26,6 %; der andere ist Karlsruhe-Stadt), bundesweit sind es neun von 299; bei den Erststimmen lagen die Grünen dort ebenfalls vorn (32,5 %). Er trägt eine Karte an Umkirch, Zähringen, Günterstal oder Horben. Im Raum Neuwied wählt kein Ort mit anderer stärkster Partei als der Kreis; Abweichungen nach (b) gibt es: Waldbreitbach CDU 43,8 % gegen 31,9 % im Kreis Neuwied, Leutesdorf AfD 13,2 % gegen 21,2 %; in Freiburg Glottertal CDU 40,9 % gegen 32,0 % im Kreis Breisgau-Hochschwarzwald, Kirchzarten Grüne 25,7 % gegen 17,3 %. Außerhalb der Fahrt, nur zur Einordnung: Kaiserslautern ist der einzige Wahlkreis in Rheinland-Pfalz mit der AfD vorn (25,9 %), bei den Erststimmen lag dort die SPD vorn.
   - **Rekord-Blick (Nachtrag 2026-10-03; Mike):** „Ausreißer kann es noch auf vielen anderen Gebieten geben. Ist ja irgendwie so etwas wie ein ‚Rekord‘: die kleinste Gemeinde Deutschlands … Wir gehen immer vom Lokalen aus, sehen also den Ort, zu dem wir Fragen entwerfen, und könnten von diesem Ort aus überlegen, ob er Eigenschaften hat, die in Stadt/Kreis/Land/Staat/Europa/Welt Ausreißer oder Rekord sind.“ Die Ausreißer-Karte ist damit ein Sonderfall.
     - *Der Blick:* Für jede Eigenschaft und jeden Fakt des Orts wird gefragt, auf welcher Ebene er an der Spitze, am Ende oder allein steht: Stadt, Kreis, Land, Staat, Europa, Welt. Die höchste Ebene, auf der das belegt ist, trägt die Karte. Ausgangspunkt bleibt der Ort; gesucht wird nicht nach Rekorden, die dann einen Ort bekommen.
     - *Zwei Quellen.* (1) **Gerechnete Rekorde** aus vollständigen amtlichen Vergleichsdaten: Wahl, Einwohner, Fläche, Dichte, Höhe; als Rekord zählt Platz eins oder der letzte Platz, Ausreißer nach (a) und (b) gehören dazu. (2) **Superlative aus dem Text:** Der Extraktions-Prompt sammelt sie schon („älteste“, „größte“, „einzige“ mit Bezugsraum). Sie brauchen den Faktencheck, und ihr Vorbehalt bleibt stehen („gilt als“, §8 Nr. 8).
     - *Die Vergleichsmenge muss vollständig sein und benannt werden* („unter den 50 Gemeinden des Landkreises“). Zwei Grenzen aus der Probe: In Rheinland-Pfalz zählen nur rund 250 Gemeinden ihre Briefwahl selbst aus; ein Wahl-Rekord auf Gemeindeebene ist dort nicht zu begründen, nur auf Ebene der Verbandsgemeinden. Und Wikidata taugt nicht als Vergleichsmenge: Sie führt für Gundelfingen eine Höhe von 1.277 m und für Denzlingen eine Fläche von 75 km², beides falsch, und hätte daraus Kreisrekorde gemacht. Gerechnete Rekorde kommen aus der amtlichen Gemeindestatistik der Landesämter.
     - *Rekorde veralten:* Die Karte nennt Stand und Bezugsraum; ein Rekord, der sich ändern kann, steht mit Jahr da.
     - *Kein neuer Fragetyp:* Familie A (welcher Ort der Fahrt hält den Rekord, als Mehr-Orte-Frage nach §8a, oder welche Eigenschaft), Familie C (Rang oder Wert), Familie B (ein Rekord als Lüge oder Wahrheit).
     - *Probe an beiden Räumen (2026-10-03):* Die Fakten der 21 Orte tragen schon rund 45 Superlative mit Bezugsraum, auf allen Ebenen (aus der Extraktion, nur zum Teil schon faktengeprüft): Welt (gilt als älteste Spiraltreppe auf einem Kirchturm, Denzlingen; größte Clownsparade, größte Eierkrone), Deutschland (drittältestes Gasthaus, höchster Baum, Esskastanien mit dem größten Umfang), Land (zweitältestes Freibad Baden-Württembergs, nach dem Lorettobad), Kreis (älteste Mühle im Landkreis), Region (älteste Pfarrkirche des Breisgaus, größter zusammenhängender Weinberg am Mittelrhein). Gerechnet aus der Wahlstatistik, Landkreis Breisgau-Hochschwarzwald, alle 50 Gemeinden: Umkirch hat die niedrigste Wahlbeteiligung (79,7 %), Glottertal den kleinsten SPD-Anteil (10,7 %), Horben die drittgrößte Wahlbeteiligung. Ungeprüft und deshalb nicht verwendet: Rangfolgen nach Einwohnern und Fläche, solange sie nur aus Wikidata kommen.
   - **Keine Wappen-Karten (Mike, 2026-10-03):** Eine Probe mit 25 Warum-Karten zu Wappenfiguren, faktengeprüft, ist verworfen: „Die Wappen können komplett wieder weg – die bringen keine Spielfreude.“ Die Figuren laufen fast immer auf Herrschaft, Kloster oder Kirchenpatron hinaus, die Karten werden gleichförmig. Eine neue Fragenfamilie geht deshalb zuerst als Probe von drei bis fünf Karten an Mike, bevor Kette und Faktencheck für alle Orte gebaut werden.
   - **Zweite Quelle bei dünnem Ortsartikel (neu in v0.2.7; Mike, 2026-10-02: „ja"):** Hat der Ortsartikel weniger als 1.000 Wörter, werden bis zu drei Artikel dazugeholt, auf die er verweist und die den Ortsnamen im Titel tragen (eine Burg, eine Kirche, ein Geschlecht). Ihre Fakten zählen wie die des Ortsartikels, wenn sie den Ort betreffen; die Quellenzeile der Karte nennt dann jenen Artikel.
   - **Verschiedene Klassiker von Ort zu Ort (v0.2.7, aus dem zweiten Volllauf):** Ohne Vorgabe greift jeder Kartenlauf zum selben Klassiker (zehnmal zweitstärkste Partei, siebenmal Landkreis). Der Plan je Ort gibt deshalb die Eigenschaft jedes Klassikers vor und wechselt sie über die Fahrt. Bei einem Stadtteil tragen Landkreis und Kennzeichen keine Karte: Sie sind die der Stadt und durch den Steckbrief verraten.
   - **Auch ein Klassiker soll eine Theorie zulassen.** „Welches Kennzeichen?" ist Abruf. „Wer war hier stärkste Partei, so nah an der Universitätsstadt?" lässt sich begründen. Wo es geht, stellt die Karte den Klassiker so, dass Steckbrief und Allgemeinwissen einen Anhalt geben.
   - **Zeitabhängige Angaben** (Wahl, Bürgermeister, Einwohner) tragen ihren Stand in der Auflösung. Eine Angabe, deren Aktualität nicht geprüft ist, trägt keine Frage (Gemeinde-Achsen v0.5 §6.1).
   - **Welche Daten:** als Option alles, was die Originalvariante in ihren Datenbanken schon als Vorrat angelegt hat (Mike, 2026-10-01). Die Liste steht in §8a und als E11 in den Achsen-Entscheiden. „Option" heißt: Fehlt eine Eigenschaft für einen Ort, fehlt sie; nichts wird geraten.
   - **Folge für den Anschluss:** Im Vorrat ist nicht bekannt, welcher Ort vorher gespielt wird. Der Anschluss hängt deshalb am Ortspaar und nicht an der Karte; die Fahrt setzt ihn zur gespielten Karte dazu. Damit die 70 Wörter aus §1 Schritt 2 halten, hat die Karte ohne Anschluss höchstens 60 Wörter und der Anschluss höchstens 10. Das ist eine Folgerung aus dem Vorrat und von Mike nicht eigens entschieden; der zweite Volllauf fährt so.
   - **Auswahl aus dem Vorrat** während der Fahrt: nach der Varianzregel (§1 Schritt 2) und der Taktung (§5). Wie viele Klassiker eine Fahrt verträgt, ist nicht festgelegt (§11 Nr. 9).
8. **Faktencheck und Bindung an den Fakt (neu in v0.2.7):** Die Kette der Content-Seite hat vier Glieder: **Extraktion, Karte, Faktencheck, Kuratieren.** Keine Karte kommt ohne Faktencheck in den Vorrat.
   - **Warum:** Wikipedia allein reicht nicht. Im Faktencheck der ersten 100 Karten waren 60 bestätigt, 31 zu korrigieren, 4 unsicher und 5 zu sperren. Sechs Karten hatten eine „falsche" Antwort, die stimmt; das ist der Fehler, der am Tisch am meisten kostet, weil er die richtige Theorie bestraft. Rund 15 Fehler standen schon im Artikel, zwei kamen aus der Extraktion, und die Kartenläufe glätteten Vorbehalte weg („gilt als älteste" wurde „ist die älteste").
   - **Was geprüft wird:** jede Karte gegen den Artikel, gegen eine zweite Quelle im Netz und darauf, ob eine falsche Option zufällig wahr ist. Eine frei erfundene Theorie nach Nr. 1c über einen Grund oder Anlass ist erst nach dem Faktencheck zulässig: Der Kartenlauf darf sie schreiben, der Check muss sie freigeben.
   - **Vier Urteile:** *bestätigt* (nichts zu ändern), *korrigiert* (die Karte steht in der berichtigten Fassung im Vorrat), *unsicher* (die Auflösung ist nur durch Wikipedia belegt; die Karte bleibt spielbar und trägt den Vermerk), *gesperrt* (so nicht spielbar; nicht im Vorrat).
   - **Wer prüft (Mike, 2026-10-02):** Die Sachprüfung liegt vollständig bei der Maschine. Der Kurator prüft keine Auflösungen; bei ihm liegen Geschmack, Theorie-Gefühl und die erste Karte je Ort. Kuratiert wird durch Streichen.
   - **Für den Kartenlauf folgt daraus:** Vorbehalte der Quelle bleiben stehen („gilt als", „der Sage nach"); Vergangenes steht in der Vergangenheit; ein Superlativ trägt in einer Lügen-Karte keine wahre Aussage; eine Frage nach etwas, das sich geändert hat, nennt ihren Zeitpunkt.
   - **Die Befunde hängen am Fakt.** Was der Faktencheck an einer Karte findet, wird am Fakt selbst berichtigt (falscher Wert ersetzt, Vorbehalt ergänzt, „nur in Wikipedia belegt" vermerkt, unbelegter Fakt gesperrt), nicht nur an der Karte. Sonst kehrt der Fehler mit jedem Kartenlauf wieder und muss jedes Mal neu abgefangen werden. Die Rohextraktion bleibt unverändert daneben liegen. Stand Raum Freiburg: 60 Berichtigungen an 48 von 806 Fakten, dazu 9 an Grunddaten; kein Befund des Faktenchecks ist ohne Fakt geblieben.
   - **Jede Karte ist an ihren Fakt gebunden.** Jeder Fakt hat eine feste Kennung, jede Karte nennt die Kennung des Fakts, an dem ihre Auflösung hängt (bei einer Lügen-Karte: an dem die Lüge hängt). „Derselbe Fakt" ist damit eine Abfrage und keine Zuordnung von Hand. Bei einem Fakt, der viele Sachen trägt (der Ort selbst, die Grunddaten), zählt die Eigenschaft mit. Geprüft ist die Abfrage an den 49 Zuordnungen, die nach dem dritten Lauf von Hand getroffen waren: Sie findet 48 davon; die 49. war kein gleicher Fakt, sondern eine überholte Karte (Wahlergebnis der ganzen Stadt statt des Stadtbezirks).
   - **Für das Spiel folgt daraus zweierlei.** Der Vorrat führt je Fakt eine Karte (Nr. 7), und die Varianzregel „nicht zweimal derselbe Fakten-Typ" (§5) kann an der Bindung abgelesen werden statt am Kartentext. Beides ist Content-Seite; am Core-Loop ändert sich nichts.

**Begriffe gegenüber Gemeinde-Achsen v0.5 (für Nr. 1–8 und §11 Nr. 6):** „Achse" heißt in diesem Dokument eine Eigenschaft im Sinne von v0.5 (Fakten-Typ mit Wert); v0.5 nennt „Achsen" dagegen seine Frageformen A–D. Die Fragefamilien A/B/C hier sind nicht die Frage-Achsen A/B/C dort: Radar ist hier Familie A und dort Achse C. Schicht 0 und 1 sind hier wie dort gemeint (frühere Fassungen dieses Konzepts zählten 0/1/2). Für Theorie-Distraktoren nach Nr. 1b setzt der Abstand von 50–100 km die erste Stufe des Distraktor-Pools aus v0.5 §10 (30 km) aus. Die Folgen für die Datenbank stehen in `gemeinde-achsen-entscheidungen-2026-10-01.md` (E4–E11).

**Vor dem Feldtest zu beantworten, aus den Daten der Gemeinde-Achsen Iteration 1, nicht im Feldtest:** Wie viele Orte haben ≥ 2 belastbare Schicht-2-Fakten (B-Quote)? Wie viele Orts-Paare liefern einen Vergleichsanschluss (fast alle) und wie viele einen Erzählanschluss (vermutlich wenige)?

### 8a. Was die Content-Seite schon mitbringt (Mike, 2026-10-01)

Zur Einordnung der Regeln oben, keine neue Entscheidung:

- **Vorhandene Datenbasis aus dem QuizAway-Vorgänger:** strukturierte Fakten aus mehreren Quellen für die größeren Orte, darunter Distanzen untereinander, Einwohnerzahlen, Bahnhöfe. Das ist Schicht 0 im Sinne der Gemeinde-Achsen und deckt für die größeren Orte Familie C, den Vergleichsanschluss (a), die Bingo-Felder und das Radar-Material (Nachbarn, Entfernungen). **PC-Befund 2026-10-01:** `data/staedte.json` enthält 2.051 Orte mit Stadtrecht; von den zehn Freiburg-Orten ist nur Staufen dabei. Die Spalte Kfz-Kennzeichen ist im Raum Freiburg fehlerhaft (Bad Krozingen und Staufen „FDS", Todtnau „TÜ"), und ein Eintrag „Gundelfingen a.d.Donau" trägt die Koordinaten von Gundelfingen im Breisgau. Für kleine Orte kommt Schicht 0 deshalb aus Wikidata, und der Vergleichsanschluss über den Kennzeichen-Kreis ist bis zur Bereinigung nicht belastbar.
- **Was der Altbestand als Vorrat führt, und was davon die kleinen Orte erreicht (PC-Befund 2026-10-01, v0.2.6):** Die Originalvariante hat sieben Fragekategorien (`data/fragen.json`): Bundesland, Einwohner und Dichte, Kfz-Kennzeichen, Höhe, Entfernungen, Geschichte (Ersterwähnung, Gründung), Bahn (Bahnhofskategorie, ICE-Halt). Dazu liegen in `data/geo.sqlite` 77.052 Orte mit Koordinaten und Höhe (Einwohner bei rund 13.000), Postleitzahlen und eine Kennzeichen-Tabelle je Kreis. Für die kleinen Orte trägt davon direkt nur die Höhe und teils die Einwohnerzahl: `staedte.json` kennt nur Orte mit Stadtrecht, `geschichte.json` und `bahnhof.json` je rund 50 große Städte, und der Kennzeichen-Tabelle fehlen ganze Kreise (Breisgau-Hochschwarzwald, Konstanz). Die Kfz-Spalte in `staedte.json` war in zehn von elf geprüften Orten falsch. **Die Kategorien werden deshalb übernommen, die Werte kommen für kleine Orte aus Wikidata, der Wikipedia-Infobox und amtlichen Quellen;** der Altbestand läuft als zweite Quelle mit, wo er den Ort kennt. Neu gegenüber dem Altbestand: Wahlergebnis (Bundeswahlleiterin, je Gemeinde), Bürgermeister, Partnerstädte, Vorwahl. Stand und Lücken: `data/gemeinde-achsen/iter1/grunddaten.json`.
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
- **Stufe 2, generiert (Pipeline):** Karten aus Gemeinde-Achsen Iteration 1 (Prompt, Achsen-Regeln, Negativnachweis), Mike kuratiert nur; seit v0.2.7 liegt zwischen Karte und Kuratieren der Faktencheck (§8 Nr. 8). Misst, ob die **Pipeline** liefern kann, was der Kern braucht. Stufe 2 ist die Hauptaussage für die Implementierung; Stufe 1 darf sie nicht ersetzen. **Voraussetzungen (v0.2.4):** Iteration 1 liefert Fakten, keine Karten; dazwischen liegt ein Karten-Prompt (Frage, Theorie-Optionen, Reveal, Anschluss), der in `quizaway-stufe2-vorbereitung-2026-10-01.md` steht. Die zehn Freiburg-Orte liegen höchstens 27 km auseinander; für den Kontext-Spiegel laufen deshalb zehn Spenderorte im Band 50–100 km mit. Zähringen und Günterstal werden als Ortsteile von Freiburg geführt.
- Jede Karte trägt ihre Stufe und bei Anschluss ihre Klasse (a/b).

**Theorie-Klassifikation vor dem Reveal, in allen Tests:** T0 keine Theorie („keine Ahnung"), T1 Auswahl ohne Begründung („ich nehme die Zwei"), T2 konkrete Theorie mit Begründung („Zwei, weil der Name wohl vom Bach kommt"), **W gewusst oder wiedererkannt** (aus Allgemeinwissen oder aus einer früheren Karte der Fahrt; mit Vermerk, woher). W ist kein Durchtippen und keine Theorie; W je Karte über mehrere Personen misst die Bekanntheit (§8 Nr. 6) und prüft die Spender-Regel (§8 Nr. 1). Seit v0.2.6 schließt W keine Karte aus; W je Fahrt zeigt, wie viele Glückstreffer eine Fahrt hatte. Im Auto stellt der Beobachter fest, ob aus Zuruf und Diskussion T2 hervorgeht; Begründung bleibt freiwillig.

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
6. Content-Regeln §8 (jetzt acht) ins Achsen-Regelwerk; die Begriffs-Übersetzung aus §8 gilt dabei.
7. Danach PC-Session gegen Transfer-Konzept v1.1 und Code; Ausgangspunkt ist das ausgelöste Kipp-Kriterium (§9).
8. **Parallel: Benutzungsoberfläche und Design.** Die UI-Runde mit den Reviewpartnern ist gelaufen (Handy, 2026-10-01); maßgeblich ist das **UI-Konzept v0.2** (`quizaway-ui-konzept-reise-modus-v0.2-2026-10-01.md`). Offen daraus: eine kurze Nachfrage zu vier Themen (`quizaway-oberflaeche-review-briefing-runde5-2026-10-01.md`), der Blick auf Hell und Dunkel im Auto, und ein eigener Papier-Test der Screens. Das betrifft die Oberfläche, nicht die Mechanik.

9. **Nach v0.2.6 (Stufe 2, zweiter Volllauf):** Grunddaten für die zwanzig Orte erweitert (`scripts/data-fetch/gemeinde_achsen_grunddaten.py`), Karten-Prompt v0.5 (sieben Karten je Ort, Bekanntheit sperrt nicht, C nur aus Grunddaten), zweiter Volllauf auf den zehn Zielorten. **Offen und nicht entschieden:** welche der passierten Orte eine Fahrt spielt, wenn jeder Ort Material hat (§1a), und wie viele Klassiker eine Fahrt verträgt (§8 Nr. 7). Beides zeigt erst der Auto-Test.

10. **Nach v0.2.7 (Stufe 2, Stand 2026-10-02):** ~~Zweiter Volllauf~~, ~~Faktencheck~~, ~~Probe und dritter Volllauf~~ gelaufen; Vorrat Raum Freiburg 129 geprüfte Karten. **Als Nächstes:** Feldtest Stufe 2 am Tisch mit dem Kartensatz `quizaway-feldtest-stufe2-kartensatz-freiburg-2026-10-02.md` (eine Person, die Stufe 1 nicht gespielt hat). **Offen bei Mike:** das Vorrats-Blatt (`quizaway-stufe2-vorrat-2026-10-02.md`, streichen, was nicht gefällt) und die Grenze je Ort (vorläufig zwanzig; Vorschlag: so lassen, bis ein Ort sie erreicht). **Offen und nicht entschieden:** wonach ausgewählt wird, wenn ein Ort mehr als zwanzig Karten hergibt; ob eine gestrichene Karte den Fakt freigibt, sodass eine ältere Karte zum selben Fakt zurückkommt (vorläufig: nein). **Danach:** ein zweiter Raum außerhalb Freiburgs, damit sich zeigt, ob Kette und Regeln ohne Nachstellen tragen.

11. **Nach v0.2.8 (Stand 2026-10-03):** ~~Zweiter Raum~~ gelaufen (Neuwied, elf Orte, 102 Karten im Vorrat; Bericht `quizaway-stufe2-raum-neuwied-2026-10-02.md`): Prompts und Regeln trugen ohne Änderung, nachgestellt wurden nur Skripte und die Politik-Regel. ~~Wappen als Fragenfamilie~~ geprüft und verworfen. **Als Nächstes:** drei bis fünf Probekarten zur Ausreißer-Karte für Mike (Freiburg Wahlkreis 281, Waldbreitbach, Leutesdorf, Glottertal); erst nach seinem Urteil kommt die Familie in Grunddaten-Skript, Kartenplan und Faktencheck. **Entschieden (2026-10-03):** Ausreißer-Karte bleibt, Form A vor B, mit Ausreißer immer im Vorrat. ~~Ausreißer in den Vorrat~~ (Lauf a0.1, 2026-10-03): `scripts/data-build/gemeinde_achsen_ausreisser.py` schreibt die Karten selbst aus der Wahlbezirksstatistik (Klassiker, Form A, kein Kartenlauf); `scripts/check/gemeinde_achsen_ausreisser_pruefen.py` rechnet jede Zahl unabhängig nach und schreibt das Urteil im Format des Faktenchecks (Gegenprobe mit verfälschten Karten: falsche Zahl und falsche Lösungsstelle werden erkannt). Acht Karten, alle bestätigt: Wahlkreis Freiburg an Umkirch, Zähringen, Günterstal und Horben; Glottertal (CDU), Kirchzarten (Grüne), Waldbreitbach (CDU), Leutesdorf (AfD). Dierdorf und Linz tragen keine, weil es dort kein Gesamtergebnis der Gemeinde gibt. Vorrat jetzt Freiburg 135, Neuwied 104. ~~Rekord-Probekarten~~ geschrieben (`quizaway-rekord-probekarten-2026-10-03.md`, drei Karten: Waldbreitbach höchster Frauenanteil im Kreis, Umkirch niedrigste Wahlbeteiligung im Landkreis, Fahrtrekord Dichte). Befunde dort: Die Text-Superlative tragen schon alle eine Karte; neu sind gerechnete Rekorde aus dem Gemeindeverzeichnis des Statistischen Bundesamts und der Wahlstatistik; ein Rekord braucht Abstand zum Zweiten (Vorschlag: ein Prozentpunkt bei Anteilen, sonst zwei Prozent des Werts). **Urteil (Mike, 2026-10-03):** „Spielfreude geht so“; der Abstand sei zu klein, „da bleibt das Erstaunen aus“ – ein Frauenanteil über 70 % oder eine Wahlbeteiligung unter 50 % wäre eine Super-Frage. **Folge: Ein gerechneter Rekord trägt nur, wenn der Wert erstaunt, nicht weil er Platz eins ist.** Maßstab ist der Abstand zu dem, was man ohnehin erwartet, nicht der Rang. Die Gegenprobe über alle 9.586 Gemeinden ab 300 Einwohnern zeigt, wie selten das ist: Der höchste Frauenanteil liegt bei 59,3 % (Untermarchtal), die niedrigste Wahlbeteiligung bei 66,6 %; Waldbreitbach ist mit 54,4 % statistisch unter den obersten 0,2 % und erstaunt trotzdem nicht. Erstaunliche Werte gibt es bundesweit nur vereinzelt (Freistatt 23 % Frauen, Schnaudertal 58 % AfD, Eslohe 56 % CDU, Merzhausen 33 % Grüne bei einem Median von 8 %). Vorschlag der PC-Seite, von Mike zu bestätigen: Ein gerechneter Wert trägt eine Rekord-Karte, wenn er mindestens 15 Prozentpunkte vom Bundesmedian entfernt liegt oder das Doppelte oder die Hälfte einer Größe ohne Prozent erreicht; Plausibilitätsprüfung vorweg (Wahlbeteiligung über 100 % in Kruft, „CDU 0 %“ in Bayern, wo die CSU antritt). In beiden Räumen erfüllt das bisher kein Ort; die Rekord-Familie bleibt deshalb eine Kann-Klasse wie der Erzählanschluss: gespielt, wo die Daten sie hergeben, ohne Bauauftrag. Die drei Probekarten kommen nicht in den Vorrat. **Offen bei Mike:** weiter Vorrats-Blatt Freiburg, Grenze je Ort, Feldtest Stufe 2 am Tisch.

Keine weitere Review-Runde über die Mechanik. Runde 4 ist mit fünf Reviews vollständig.

---

**These:** Ein Reiseführer, der erst eine eigene Theorie verlangt und danach die Antwort erzählt. Das Fundament ist entschieden, in jeder Situation gleich. Der Witz liegt im Festlegen, pro Sitzplatz anders. Beides ist jetzt so geschrieben, dass der Feldtest es widerlegen kann. Das ist der Zweck dieser Version.

*Ende Spielkonzept v0.2.8. Anhang A (Rulings Runde 3) steht in v0.2 (`quizaway-spielkonzept-reise-modus-v0.2-2026-10-01.md`).*

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

---

## Anhang F — Rulings nach dem Stufe-2-Volllauf (2026-10-01)

Grundlage: `quizaway-stufe2-volllauf-2026-10-01.md` (V1–V10, §7) und `gemeinde-achsen-entscheidungen-2026-10-01.md` (E9–E11).

| Entscheid (Mike) | Folge im Spielkonzept | Wo |
|---|---|---|
| E9: Bekanntheitsfilter stark abschwächen; ein Glückstreffer ist erwünscht, die Frage lieber auf ein Detail legen | Bekannte Fakten tragen die Frage; W ist Messung, kein Ausschlussgrund | §8 Nr. 6, §7 K3b, §10 |
| E10: Ziel sieben Fragen je Ort, auch für kleine; Klassiker und Politisches gehören dazu | Fragenvorrat je Ort; Klassiker als Familie A oder C aus Schicht 0 | §8 Nr. 7, §2, §5 |
| „Sieben Fragen" meint den Vorrat je Ort, nicht mehrere Fragen hintereinander | „Eine Frage pro Ort" bleibt | §5, §8 Nr. 7 |
| Grunddaten: als Option alles, was die Originalvariante als Vorrat in ihren Datenbanken angelegt hat | Kategorien des Altbestands übernommen; Befund zu dessen Reichweite | §8a, E11 |

**Folgerungen ohne eigenen Entscheid (zur Kenntnis, im zweiten Volllauf so gefahren):**

- ~~Familie C nur aus Grunddaten.~~ **Berichtigt am 2026-10-02 (Mike):** Grunddaten sind der Normalfall; eine Zahl aus dem Artikel ist erlaubt, wenn der Steckbrief einen Anhalt zum Schätzen gibt (§8 Nr. 7). Anlass: Im Kuratierblatt des ersten Laufs hat Mike die Übernachtungen in St. Peter und die Verluste im Gefecht bei Horben gewählt. Der zweite Volllauf lief noch mit der strengen Fassung.
- Der Anschluss hängt am Ortspaar; Karte höchstens 60 Wörter, Anschluss höchstens 10 (§8 Nr. 7).
- Eine zeitabhängige Angabe ohne geprüfte Aktualität trägt keine Frage (§8 Nr. 7). Anlass: Die Wikipedia-Infoboxen von Horben und Staufen nennen am 2026-10-01 denselben Bürgermeister.
- Jeder Ort mit Grunddaten hat jetzt Material (§1a). Was das für die Auswahl der Orte einer Fahrt heißt, ist offen (§11 Nr. 9).

**Weiter offen bei Mike (Bericht §7 Nr. 1, 3, 4):** Auswahl im Kuratierblatt; Anschluss, wenn der Fakt den letzten Ort nur als Namensteil nennt (Herzog von Zähringen); zweite Quelle bei dünnem Artikel. **Alle drei am 2026-10-02 entschieden, siehe Anhang G.**

*Ende Anhang F.*

---

## Anhang G — Rulings nach Faktencheck, Probe und drittem Volllauf (2026-10-02)

Grundlage: `quizaway-stufe2-volllauf2-2026-10-01.md` (W1–W9), `quizaway-stufe2-faktencheck-2026-10-02.md` (F1–F8), `quizaway-stufe2-probe-v0.6-2026-10-02.md` (P1–P7, §1), `quizaway-stufe2-volllauf3-2026-10-02.md` (D1–D8).

| Entscheid (Mike, 2026-10-02) | Folge im Spielkonzept | Wo |
|---|---|---|
| Kuratierblatt des ersten Laufs: 17 Kreuze, kein „keiner"; Blatt des zweiten Laufs: nichts gestrichen, je Ort eine erste Karte | Alle Karten bleiben im Vorrat; der Kartensatz für den Tisch läuft als gemischte Reihe, die verdrängten ersten Karten als Nachschlag | §10, §11 Nr. 10 |
| Sachprüfung ist nicht Sache des Kurators | Faktencheck als viertes Glied; vier Urteile; kuratiert wird nach Geschmack und durch Streichen | §8 Nr. 8 |
| Sieben ist die Untergrenze; mehr, wenn die Fakten es hergeben, „wobei es irgendwo eine Grenze geben muss" | Zusatzkarten im Kartenlauf; Grenze je Ort vorläufig zwanzig | §8 Nr. 7 |
| Anschluss über einen Namensteil: ja, als Kann | dritte Anschluss-Klasse (c), mit Vermerk und Prüfung im Faktencheck | §8 Nr. 4 |
| Zweite Quelle bei dünnem Ortsartikel: ja | unter 1.000 Wörtern bis zu drei verlinkte Artikel mit dem Ortsnamen im Titel | §8 Nr. 7 |
| Politik-Karte bei Stadtteilen: Stadtteilergebnis von der Kommune holen | eigenes Wahlergebnis je Stadtbezirk | §8 Nr. 7 |
| Höhe als Zahlen-Karte: nur wenn die Quellen sich einig sind | Quellwerte höchstens fünf Prozent auseinander | §8 Nr. 7 |
| Zahl aus dem Artikel: ja, wenn der Steckbrief einen Anhalt gibt | stand als Nachtrag schon in v0.2.6 | §8 Nr. 7 |
| Dritter Volllauf: ja. Karten des dritten Laufs kommen zum Vorrat; bei gleichem Fakt bleibt die Karte des dritten Laufs | Derselbe Fakt, eine Karte | §8 Nr. 7 |

**Folgerungen ohne eigenen Entscheid (zur Kenntnis; so gebaut):**

- Das Kennzeichen ist nicht einwertig; eine Kennzeichen-Karte fragt nach dem Hauptkennzeichen (§8 Nr. 7). Anlass: Faktencheck F4.
- Der Plan gibt die Eigenschaft jedes Klassikers vor und wechselt sie von Ort zu Ort (§8 Nr. 7). Anlass: zweiter Volllauf, zehnmal zweitstärkste Partei.
- Je Kartenlauf höchstens zehn Karten, im Vorrat höchstens zwanzig je Ort (§8 Nr. 7). Die Zahlen sind von der PC-Seite gesetzt.
- Die Befunde des Faktenchecks hängen am Fakt, und jede Karte ist an ihren Fakt gebunden (§8 Nr. 8). Anlass: Der dritte Lauf fing bekannte Fehler nur über einen Block in der Eingabe ab, und „derselbe Fakt" war 49-mal von Hand zugeordnet.
- Eine gestrichene Karte gibt ihren Fakt nicht frei; die ältere Karte zum selben Fakt kommt nicht von selbst zurück (§11 Nr. 10). Vorläufig, bis Mike es anders will.

**Weiter offen bei Mike:** Vorrats-Blatt; Grenze je Ort; Feldtest Stufe 2 am Tisch.

*Ende Anhang G.*

---

## Anhang H — Rulings nach dem zweiten Raum und der Wappen-Probe (2026-10-02/03)

Grundlage: `quizaway-stufe2-raum-neuwied-2026-10-02.md` (N1–N18, §4), die Wappen-Probe (Lauf w0.1, Commit `e9ca645`, zurückgenommen mit `fb68351`) und die Probe der Ausreißer an beiden Räumen (Bundestagswahl 2025, Wahlbezirksstatistik der Bundeswahlleiterin).

| Entscheid (Mike) | Folge im Spielkonzept | Wo |
|---|---|---|
| Wahlergebnis der Verbandsgemeinde statt der Stadt: „so lassen“ (2026-10-02) | Briefwahl-Regel: Die Karte fragt nach der Verbandsgemeinde und sagt das | §8 Nr. 7 |
| Ausreißer bei Wahlen als Karte; Beispiel Halle III (2026-10-02, am amtlichen Ergebnis geprüft 2026-10-03) | Ausreißer-Karte als Klassiker der Politik, kein neuer Fragetyp | §8 Nr. 7 |
| Rekord-Blick: vom Ort aus fragen, ob eine Eigenschaft in Stadt, Kreis, Land, Staat, Europa oder Welt Ausreißer oder Rekord ist (2026-10-03) | Ausreißer-Karte wird Sonderfall; gerechnete Rekorde nur aus vollständiger amtlicher Vergleichsmenge, Text-Superlative mit Faktencheck | §8 Nr. 7 |
| Ausreißer-Probekarten: „mittelmäßig Freude“, bleiben „wegen ihrer Relevanz“; Form A, dann B, dann die anderen; mit Ausreißer immer im Vorrat (2026-10-03) | Ausreißer-Karte als Pflicht im Vorrat des Orts; Plan wählt Familie A oder B | §8 Nr. 7 |
| Wappen-Karten: „können komplett wieder weg – die bringen keine Spielfreude“ (2026-10-03) | keine Wappen-Familie; Probe zurückgenommen | §8 Nr. 7 |
| Feldkirchen als elfter Ort, Kartensatz auch für Neuwied, die vier unsicheren Dierdorfer Karten weglassen (2026-10-02) | Content, keine Regeländerung | §11 Nr. 11 |

**Folgerungen ohne eigenen Entscheid (zur Kenntnis; so gebaut oder vorgeschlagen):**

- Die Schwellen der Ausreißer-Karte (höchstens drei Gebiete derselben Ebene im Land; mindestens acht Prozentpunkte Abweichung) sind von der PC-Seite vorgeschlagen; Mike: „Schwellen Ausreißer OK“ (2026-10-03). Probekarten: `quizaway-ausreisser-probekarten-2026-10-03.md`.
- Erststimme ist nicht Mandat; vorn bei Erst- und bei Zweitstimmen sind zwei Aussagen (Wahlrecht 2025: 23 Wahlkreissieger ohne Sitz).
- Stadtteilergebnis ohne Open Data: aus Stimmbezirken summiert, mit Gegenprobe Wählende ≤ Wahlscheine (Befund N4, Altwied).
- Eine neue Fragenfamilie geht zuerst als Probe von drei bis fünf Karten an Mike. Anlass: Die Wappen-Familie wurde mit Quelle, Nachrecherche, Extraktion, Kartenlauf und Faktencheck für 21 Orte gebaut und fiel erst am fertigen Blatt durch.

**Weiter offen bei Mike:** Erstaunens-Schwelle für gerechnete Rekorde (Vorschlag: 15 Prozentpunkte vom Bundesmedian bzw. Faktor zwei); Vorrats-Blatt Freiburg; Grenze je Ort; Feldtest Stufe 2 am Tisch.

*Ende Anhang H.*
