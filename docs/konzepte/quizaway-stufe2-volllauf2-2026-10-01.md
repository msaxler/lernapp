# QuizAway — Stufe 2, zweiter Volllauf Raum Freiburg: Bericht

**Datum:** 2026-10-01 (spätabends) · **Grundlage:** Spielkonzept v0.2.6, Gemeinde-Achsen v0.5 plus E1–E11, Bericht zum ersten Volllauf `quizaway-stufe2-volllauf-2026-10-01.md` · **Auftrag (Mike):** Vorrat von sieben Fragen je Ort; Bekanntheitsfilter abschwächen; Grunddaten erweitern um Kennzeichen, Fläche, Ersterwähnung, Wahl „und eben alles das, als Option, was wir in der Originalvariante als Vorrat in Datenbanken schon angelegt haben" · **Daten:** `data/gemeinde-achsen/iter1/`

**Ergebnis in einem Satz:** Alle zehn Zielorte haben jetzt einen Vorrat von sieben Karten (70 Karten, je Ort vier Geschichten und drei Klassiker, alle innerhalb der Redaktionsgrenzen), und die drei Fakten, die der erste Lauf gesperrt hatte (Schwarzwaldklinik, Faust, Hebungsrisse), tragen ohne jeden Hinweis an die Kartenläufe je eine Frage auf einem Detail.

Was der Lauf nicht zeigt: ob die Karten am Tisch eine Theorie hervorrufen, und ob jede falsche Option wirklich falsch ist. Das erste misst der Feldtest, das zweite liest Mike beim Kuratieren gegen.

---

## 1. Was gelaufen ist

| Glied | Womit | Ergebnis |
|---|---|---|
| Grunddaten (Schicht 0) | `scripts/data-fetch/gemeinde_achsen_grunddaten.py`: Wikidata, Wikipedia-Infobox, Wahlbezirksstatistik der Bundeswahlleiterin, Altbestand der Originalvariante | `grunddaten.json`: 20 Orte, 19 Eigenschaften im Katalog, je Ort 14 bis 17 belegt |
| Extraktion (Schicht 1) | unverändert vom ersten Lauf | 758 Blöcke an den zehn Zielorten |
| Eingabe je Ort | `scripts/data-build/gemeinde_achsen_karten_eingabe.py` | `eingabe-v0.5/`: Grunddaten, Plan der sieben Karten, letzter Pin, Fahrt, Fakten, zwei Spender |
| Karten | `prompt-karten-v0.5.txt`, großes Modell, ein Durchlauf je Zielort, der nur Prompt und Eingabedatei las | 70 Karten in `karten-v0.5/`, kein „KEINE KARTE" |
| Prüfung | `scripts/check/gemeinde_achsen_karten_pruefen_v05.py` | 70 Karten, kein Verstoß (§3) |
| Kuratierblatt | `scripts/data-build/gemeinde_achsen_kuratierblatt_v05.py` | `quizaway-stufe2-kuratierblatt-v2-2026-10-01.md` |

Der Plan je Ort gab Sorte, Familie und Stelle der Lösung vor: Geschichte A, Klassiker Zahl (C, in St. Peter und Kirchzarten als Leiter), Geschichte B, Klassiker Politik, Geschichte A, Klassiker Zugehörigkeit oder Lage, Geschichte A oder B. Welchen Fakt eine Karte nimmt, entschied der Durchlauf.

---

## 2. Grunddaten: was es für die Orte gibt

Katalog nach E11, jede Eigenschaft optional. Abdeckung an den zehn Zielorten:

| Eigenschaft | Herkunft | Zielorte | Quelle |
|---|---|---|---|
| Bundesland, Landkreis | Originalvariante (geo) | 10 | Infobox, Wikidata |
| Einwohner, Fläche, Dichte | Originalvariante (ew) | 10 | Wikidata, berechnet |
| Kfz-Kennzeichen | Originalvariante (kfz) | 10 | Wikidata |
| Höhe | Originalvariante (hoehe) | 10 | Wikidata, Infobox, Altbestand |
| Nächste Großstadt, Luftlinie zur Landeshauptstadt | Originalvariante (dist) | 10 | berechnet |
| Ersterwähnung | Originalvariante (gesch) | 5 | Extraktion, Wikidata |
| Bahnhöfe und Haltepunkte | Originalvariante (bahn) | 5 | Wikidata |
| Postleitzahl, Vorwahl | Altbestand / neu | 10 | Wikidata |
| Wahlergebnis Bundestagswahl 2025 | neu (Politik) | 10 | Bundeswahlleiterin, amtlich |
| Bürgermeister | neu (Politik) | 8 | Infobox, Aktualität ungeprüft |
| Partnerstädte | neu | 3 | Wikidata |
| Eingemeindung | neu (Stadtteile) | 2 | Infobox |

**G1. Die Kategorien der Originalvariante tragen, ihre Werte für kleine Orte nicht.** `staedte.json` kennt von den zehn Zielorten nur Staufen, `geschichte.json` und `bahnhof.json` keinen. `geo.sqlite` liefert Höhe und teils Einwohner. Die Werte kommen deshalb aus Wikidata, Infobox und amtlicher Quelle; der Altbestand läuft als zweite Quelle mit.

**G2. Die Kennzeichen des Altbestands sind unbrauchbar.** Die Kfz-Spalte in `staedte.json` ist in zehn von elf geprüften Orten falsch (Staufen „FDS", Oberkirch „TUT", Engen „EM"); nur Dornstetten stimmt. Der Kennzeichen-Tabelle in `geo.sqlite` fehlen ganze Kreise (Breisgau-Hochschwarzwald, Konstanz). Wikidata führt das Kennzeichen an allen 20 Orten.

**G3. Die Wahl hat eine amtliche Quelle für alle Gemeinden.** Die Wahlbezirksstatistik der Bundeswahlleiterin zur Bundestagswahl 2025 enthält rund 95.000 Wahlbezirke mit Gemeindeschlüssel; je Gemeinde werden Urnen- und Briefwahlbezirke summiert. In allen acht Gemeinden ist die CDU stärkste Partei (26 bis 41 Prozent), in Freiburg sind es die Grünen. Zweite sind meist die Grünen, in Umkirch und Glottertal die AfD. Für Zähringen und Günterstal gibt es nur das Ergebnis der ganzen Stadt; die Freiburger Wahlbezirke tragen in der Datei keine Stadtteilnamen.

**G4. Die Höhe eines Orts ist keine sichere Zahl.** Bei vier von zehn Zielorten nennen die Quellen Werte, die um mehr als fünf Prozent auseinanderliegen: Horben 607 und 495 m, Glottertal 350, 306 und 403 m, Gundelfingen 266 und 235 m, Umkirch 219 und 206 m. Bei einer Talgemeinde hängt die Zahl davon ab, wo gemessen wird.

**G5. Ersterwähnung nur an fünf Orten.** Wikidata führt sie fast nie (nur Zähringen); aus der Extraktion kommt sie, wenn der Artikel sie im Ortsblock nennt.

**G6. Bürgermeister ohne geprüfte Aktualität.** Die Infoboxen von Horben und Staufen nennen am Abruftag denselben Namen. Die Angabe trägt deshalb keine Frage (Spielkonzept v0.2.6 §8 Nr. 7).

**G7. Nicht übernommen:** das nächste Nachbarland. Die Grenzpunkt-Tabelle der Originalvariante ist zu grob; ihr Punkt „Breisach" liegt rund 48 km neben Breisach, und für Staufen käme die Schweiz statt Frankreich heraus. Alle Abweichungen und Lücken stehen in `grunddaten.json` unter `maengel` (30 Einträge).

---

## 3. Die 70 Karten, mechanisch geprüft

- Je Ort sieben Karten: vier Geschichten, drei Klassiker. Auch in Zähringen (570 Wörter Quelle) reichten die Fakten für vier Geschichten; kein Ort brauchte Ersatz.
- Rückseite: 36 bis 59 Wörter, keine über 60. Fragen höchstens 21 Wörter (Grenze 25), Optionen höchstens 8.
- Die Lösung steht überall an der Stelle, die der Plan vorgab.
- Familien: 50 mal A, 10 mal B, 8 mal C mit Spannen, 2 Leitern.
- Negativnachweise: Weg (a) in 52 Karten, Weg (c) in 23, Weg (b) mit Spender-Fakt in 7.
- Bekanntheit nach Einschätzung des Modells: 46 niedrig, 17 mittel, 7 hoch.
- Orts-Anschlüsse: 18 für neun Ortspaare, alle höchstens 10 Wörter.

Geprüft ist die Form. **Nachtrag 2026-10-02:** Der Inhalt ist inzwischen geprüft, siehe `quizaway-stufe2-faktencheck-2026-10-02.md`: von den 70 Karten 43 bestätigt, 18 korrigiert, 4 unsicher, 5 gesperrt.

---

## 4. Neben den handgeschriebenen Karten

| Ort | Handgeschrieben | Erster Lauf | Zweiter Lauf |
|---|---|---|---|
| Umkirch | Namensherkunft | derselbe Fakt | derselbe Fakt (Karte 1) |
| Gundelfingen | Einwohner, größte Gemeinde ohne Stadtrecht | derselbe Fakt | „ohne Stadtrecht" als wahre Aussage der Lügen-Karte (3) |
| Denzlingen | Zigarrenfabriken, Bahnhof | Zigarrenfabriken als Wahrheit | nicht gewählt; vier andere Geschichten (Kirche per Ochsenkarren, Storchenturm, Spiraltreppe, Grimmelshausen) |
| Zähringen | Herzöge benannten sich nach der Burg | nicht erreichbar | weiter nicht erreichbar; Karte 5 fragt nach der Burg der Herzöge |
| St. Peter | Höhe als Leiter | andere Zahlen | **dieselbe Karte:** Höhe als Leiter (Karte 2) |
| Glottertal | Schwarzwaldklinik | gesperrt | **Karte 1:** Was war der Carlsbau der „Schwarzwaldklinik" in Wirklichkeit? |
| Kirchzarten | Tarodunum, WM 1995 | Bahn-Lüge, WM als Wahrheit | **Tarodunon** (Karte 1) und **WM 1995** (Karte 7) |
| Günterstal | Kloster | nicht gewählt | Kloster in der Lügen-Karte (3) |
| Horben | Einwohner | andere Zahlen | Höhe statt Einwohner |
| Staufen | Faust, Hebungsrisse | beide gesperrt | **Faust** (Karte 1: Was führte ihn in die Stadt?) und **Hebung** (Karte 5: Was sollten die Bohrungen heizen?) |

Fünf Orte tragen jetzt den Fakt der handgeschriebenen Karte als eigene Frage (Umkirch, St. Peter, Glottertal, Kirchzarten, Staufen), zwei weitere als Aussage einer Lügen-Karte. Im ersten Lauf waren es zwei.

---

## 5. Befunde

**W1. Der Vorrat von sieben Karten ist an jedem der zehn Orte erreicht.** Die Klassiker füllen auf, was die Quelle nicht hergibt; nötig war das an keinem Ort, weil selbst Zähringen vier Geschichten trug. Wie es bei Orten ohne eigenen Artikel aussieht, zeigt dieser Lauf nicht.

**W2. „Bekanntheit sperrt nicht" wirkt, und zwar von selbst.** Die Kartenläufe wussten nichts von Faust, Hebung oder Klinik. Die Regel „der bekannteste Fakt gehört in den Vorrat, die Frage aufs Detail" hat alle drei hereingeholt. Sieben Karten tragen die Einschätzung „hoch": die drei genannten, dazu die Rennfahrer-Prinzen aus Umkirch, die Burg der Zähringer, der Film „Schwarzwaldmädel" in St. Peter und die Douglasie „Waldtraut" in Günterstal. Ob die Detail-Fragen zu schwer oder gerade recht sind, sagt der Tisch (Kürzel W).

**W3. Die Klassiker sind über die Fahrt gleichförmig.** Alle zehn Politik-Karten fragen nach der zweitstärksten Partei. Sieben von zehn Zugehörigkeits-Karten fragen „Zu welchem Landkreis gehört …?". Sechs von zehn Zahlen-Karten fragen nach der Höhe. Der Grund ist die Bauart: Jeder Durchlauf sieht nur seinen Ort und greift zur selben naheliegenden Eigenschaft. Ungenutzt blieben Fläche, Dichte, Wahlbeteiligung, Bahnhof, Vorwahl und Partnerstädte. Abhilfe ohne Mehraufwand: Der Plan gibt je Ort die Eigenschaft vor und wechselt sie von Ort zu Ort.

**W4. Die stärkste Partei ist hier keine Frage, die zweitstärkste schon.** Achtmal CDU hintereinander wäre witzlos; die Durchläufe sind von selbst auf den zweiten Platz ausgewichen. Dort liegt die Überraschung: neben Freiburg erwartet man die Grünen, in Umkirch und Glottertal ist es die AfD. Für die beiden Stadtteile fragt die Karte nach ganz Freiburg; das ist eine Freiburg-Karte, keine über Zähringen oder Günterstal.

**W5. Die Höhe trägt wegen G4 nur breite Spannen.** In Horben musste die wahre Spanne von 450 bis unter 650 m reichen, damit beide Quellwerte hineinpassen. Die Regel „alle Werte in derselben Spanne" hat gehalten; gut wird die Karte dadurch nicht.

**W6. Der Anschluss am Ortspaar geht auf.** 15 der 18 Anschlüsse sind Vergleiche aus Grunddaten, drei kommen aus einem Fakt, der den letzten Ort nennt (S-Bahn über Denzlingen, Schauinslandradweg über Kirchzarten, Bohrer-Bach ab Günterstal). Neu tragen Wahl und Kennzeichen: „In Umkirch wurde die AfD Zweite, hier die Grünen." Die Rückseiten blieben dafür unter 60 Wörtern.

**W7. Drei Anschluss-Kandidaten über einen Namensteil liegen jetzt ausformuliert vor** (nicht verwendet, sie warten auf den Entscheid aus dem ersten Bericht): das Kloster St. Peter, gegründet vom Zähringerherzog Berthold II.; die Ersterwähnung Glottertals in der Güterbeschreibung des Klosters St. Peter; das Kloster Günterstal, gegründet von den Herren von Horwen. Ein vierter (Denzlinger Straße in Zähringen) ist ohne Gehalt.

**W8. Was die Durchläufe als Lücke des Prompts meldeten:**
- „Kein Fakt aus einem Ort der Fahrt als falsche Option" wurde auch auf Klassiker angewandt. Landkreis-Karten mieden deshalb Emmendingen und den Stadtkreis Freiburg, also die besten falschen Optionen. Die Regel ist für Geschichten gemeint und muss das sagen.
- Die Grunddaten nennen nur die vier stärksten Parteien; für eine fünfte Option fehlt der Wert.
- Lage des Orts und Titel des Artikels fehlen in der Eingabe; der Steckbrief holt die Lage aus den Fakten.
- Fachwörter (Deichel, Wildbann, Seminarist) werden aus Allgemeinwissen erklärt.
- Zähringen, Karte 7: Die Sperrung „ab Anfang 2026" ist ein zeitabhängiger Fakt aus dem Artikel, dessen Vollzug nicht belegt ist.
- Staufen: Die Fakten nennen für Fausts Tod 1539 als Legende und Lebensdaten bis etwa 1541.
- Das Format der Optionen schwankt („1." und „1 "); Kirchzarten schrieb „STELLE: 2" auf die Vorderseite. Prüf- und Blattskript fangen beides ab.

**W9. Die Spender bleiben Randfiguren.** Weg (b) kommt in 7 von 70 Karten vor. Die zwei Spender-Extraktionen machten je nach Ort ein Drittel bis drei Viertel der Eingabe aus.

---

## 6. Aufwand

- Grunddaten: ein Skriptlauf von rund einer Minute für 20 Orte; die Wahldatei (6 MB) wird einmal geladen.
- Karten: zehn Durchläufe, je 4,5 bis 7 Minuten, zusammen rund 1,4 Millionen Tokens mit dem großen Modell, also rund 20.000 Tokens je Karte. Wie beim ersten Lauf ist das eine Obergrenze, weil jeder Durchlauf als eigenständiger Agent mit seinem ganzen Rahmen lief.

### Wo ein Mensch mehr bringt als die Automatik

- **Streichen statt wählen.** Im neuen Kuratierblatt bleibt im Vorrat, was nicht angekreuzt ist. Das kostet nur dort eine Handlung, wo etwas nicht stimmt, und ersetzt eine Bewertungsfunktion, die es nicht gibt.
- **Eine Zahl je Ort:** welche Karte im Feldtest zuerst gespielt wird. Das ist die Lieblingsfrage; mehr Auswahl braucht der Vorrat nicht.
- **Höhe und Bürgermeister:** Wer die Orte kennt, klärt in einer Zeile, was die Quellen offen lassen (Horben liegt auf 607 m; wer ist in Horben Bürgermeister). Eine automatische Aktualitätsprüfung wäre teurer als diese Zeile.
- **Negativnachweise bei Weg (c):** 23 Karten tragen frei erfundene falsche Theorien. Ob eine davon zufällig stimmt, sieht nur, wer die Gegend kennt.

---

## 7. Was Mike entscheidet

1. **Kuratierblatt zum zweiten Lauf:** streichen, was nicht stimmt oder nicht gefällt; je Ort die Karte nennen, die zuerst gespielt wird.
2. **Anschluss über einen Namensteil** (offen seit dem ersten Bericht): Die drei Kandidaten aus W7 liegen vor. Vorschlag unverändert: ja, als Kann, mit Gegenlesen.
3. **Zweite Quelle bei dünnem Artikel** (offen seit dem ersten Bericht): Seit dem Vorrat drängt es weniger, weil Zähringen sieben Karten hat. Der Fakt der handgeschriebenen Karte bleibt ohne den Artikel zur Burg unerreichbar. Vorschlag unverändert: ja, unter 1.000 Wörtern.
4. **Politik-Karte bei Stadtteilen:** die Freiburg-weite Karte behalten oder streichen, bis es Ergebnisse je Stadtteil gibt? Vorschlag: streichen; die Stadt Freiburg veröffentlicht Stadtteil-Ergebnisse selbst, das wäre eine eigene Quelle.
5. **Höhe als Zahlen-Karte:** nur zulassen, wenn die Quellen sich einig sind? Vorschlag: ja.

Ohne Entscheid, als nächster Schritt am Prompt (v0.6): Eigenschaft der Klassiker je Ort im Plan vorgeben (W3), Fahrt-Regel auf Geschichten beschränken, alle Parteien ab fünf Prozent in die Grunddaten, Lage und Artikeltitel in die Eingabe (W8).

---

## 8. Was ab jetzt da ist

Für die Feldtest-Strecke Raum Freiburg liegt ein spielbarer Vorrat: 70 Karten aus dem zweiten Lauf, dazu die 30 Vorschläge aus dem ersten, zusammen 100 Karten für zehn Orte, alle innerhalb der Redaktionsgrenzen. Jeder Ort hat Geschichten und Klassiker, jede Karte ist einzeln spielbar, und zu jedem Ortspaar der Strecke gibt es zwei Anschlüsse. Faust, die Hebung und die Schwarzwaldklinik sind dabei.

*Ende Bericht.*
