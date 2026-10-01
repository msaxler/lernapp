# QuizAway — Stufe 2, Volllauf Raum Freiburg: Bericht

**Datum:** 2026-10-01 · **Grundlage:** `quizaway-stufe2-vorbereitung-2026-10-01.md`, Spielkonzept v0.2.5, Gemeinde-Achsen v0.5 plus E1–E8 · **Freigabe:** Mike, 2026-10-01 („1, 2, 3 ja, Volllauf starten": Zusatzregel übernehmen, Ton der Umkirch-Karte passt, je Ort bis zu drei Vorschläge) · **Daten:** `data/gemeinde-achsen/iter1/`

**Ergebnis in einem Satz:** Die Kette aus Quelltext, Extraktion und Karten-Prompt läuft für alle zehn Zielorte durch und liefert 30 regelgerechte Kartenvorschläge; zwei treffen denselben Fakt wie die handgeschriebene Karte, zwei bauen die Lüge auf dieselbe Art, und bei drei Orten sperrt eine Regel oder die Quelle genau das Material, das die handgeschriebene Karte trug.

Was der Lauf nicht zeigt: ob eine generierte Karte am Tisch eine Theorie hervorruft. Das misst erst der Feldtest mit den ausgewählten Karten.

---

## 1. Was gelaufen ist

| Glied | Womit | Ergebnis |
|---|---|---|
| Quelltexte | `scripts/data-fetch/gemeinde_achsen_quellen.py`: Klartext der Wikipedia-Artikel | 20 Orte, 570 bis 6.423 Wörter je Artikel |
| Grunddaten (Schicht 0) | dasselbe Skript, Wikidata: Einwohner, Höhe, Fläche, Koordinaten, Zugehörigkeit | `schicht0.json`; Zähringen ohne Höhe |
| Extraktion (Schicht 1) | Prompt v0.5 §9.1 plus Warum- und Superlativ-Regel (`prompt-stufe1-v0.5.1.txt`), kleines Modell, ein Durchlauf je Ort | 1.696 Blöcke, davon 758 an den zehn Zielorten |
| Auszählung | `scripts/data-explore/gemeinde_achsen_zaehlen.py` | `zaehlung.json` |
| Karten | `prompt-karten-v0.4.txt`, großes Modell, ein Durchlauf je Zielort, der nur Prompt und Fakten las | 30 Vorschläge in `karten/`, kein „KEINE KARTE" |
| Prüfung | `scripts/check/gemeinde_achsen_karten_pruefen.py` | alle Grenzen eingehalten (§3) |
| Kuratierblatt | `scripts/data-build/gemeinde_achsen_kuratierblatt.py` | `quizaway-stufe2-kuratierblatt-2026-10-01.md` |

Die Familie je Ort folgt der handgeschriebenen Karte (A C B A C A B A C B). Für die zwei Radar-Karten (Glottertal, Günterstal) wurde Familie A erzeugt, siehe V7.

---

## 2. Extraktion in Zahlen

| Ort | Wörter Quelle | Blöcke | Entitätstypen | Warum-Fakten |
|---|---|---|---|---|
| Umkirch | 1.487 | 60 | 34 | 7 |
| Gundelfingen | 1.722 | 47 | 17 | 9 |
| Denzlingen | 6.423 | 151 | 63 | 25 |
| Zähringen | 570 | 19 | 13 | 3 |
| St. Peter | 1.721 | 89 | 43 | 11 |
| Glottertal | 1.754 | 49 | 27 | 13 |
| Kirchzarten | 2.671 | 86 | 36 | 16 |
| Günterstal | 2.513 | 79 | 12 | 16 |
| Horben | 2.392 | 71 | 33 | 13 |
| Staufen | 5.351 | 107 | 37 | 14 |

Spenderorte: 47 bis 165 Blöcke, 4 bis 20 Warum-Fakten.

- **Warum-Fakten** sind Eigenschaften, deren Name Herkunft, Grund, Anlass, Ursache oder Benennung trägt. Gezählt am Eigenschaftsnamen; die Zahl ist eine Untergrenze, weil frei benannte Eigenschaften durchrutschen.
- **Entitätstypen:** 431 frei benannte Typen über alle 20 Orte, davon 48 in mindestens drei Orten (Kirche, Schule, Bahnhof, Wappen, Persönlichkeit und so weiter, teils doppelt in zwei Schreibweisen). Das Kipp-Kriterium K1 aus v0.5 (weniger als zehn Typen) ist nicht ausgelöst. Die Zusammenführung zum Katalog (v0.5 §9.2) steht aus; für die Karten war sie nicht nötig.
- **B-Quote:** Alle zehn Zielorte haben weit mehr als zwei belastbare Fakten; Familie B ist an keinem Ort an der Datenmenge gescheitert.

---

## 3. Die 30 Vorschläge, mechanisch geprüft

- Rückseite: 49 bis 69 Wörter, keine über 70.
- Optionen: keine über 8 Wörter. Fragen: 7 bis 24 Wörter.
- Die wahre Option beziehungsweise die Lüge steht überall an der vorgegebenen Stelle.
- Negativnachweise: Weg (a), aus den Fakten widerlegt, in 21 Vorschlägen; Weg (c), erfundene Theorie gegen einen einwertigen Fakt, in 12; Weg (b), gespiegelter Fakt eines Spenderorts, in 3.
- Bekanntheit nach Einschätzung des Modells: 25 niedrig, 5 mittel, keine hoch.
- Anschluss: in 11 von 30 Vorschlägen.

Geprüft ist die Form. Ob jede falsche Option wirklich falsch ist, steht je Vorschlag als Negativnachweis in der Kartendatei und gehört beim Kuratieren gegengelesen.

---

## 4. Neben den handgeschriebenen Karten

| Ort | Handgeschrieben | Stufe 2 |
|---|---|---|
| Umkirch (A) | Namensherkunft | **Derselbe Fakt** (Vorschlag 1), mit „vermutlich" wie die Quelle |
| Gundelfingen (C) | Einwohner, größte Gemeinde ohne Stadtrecht | **Derselbe Fakt** (Vorschlag 3), mit Anschluss zu Umkirch |
| Denzlingen (B) | Zigarrenfabriken, Bahnhof; Lüge Straßenbahn | **Gleiche Bauart wie Fassung 2:** Lüge über die Herrschaft („400 Jahre österreichisch"), Zigarrenfabriken als Wahrheit |
| Zähringen (A) | Herzöge benannten sich nach der Burg | **Nicht erreichbar:** steht nicht im Artikel des Stadtteils |
| St. Peter (Leiter) | Höhe des Orts; Erzählanschluss an Zähringen | Andere Zahlen (Alter des Klosters, höchster Punkt, Übernachtungen); **Erzählanschluss verworfen** |
| Glottertal (Radar) | Schwarzwaldklinik | **Gesperrt wie gewollt;** stattdessen Bergbau, höchster Weinberg, Scheffelwein |
| Kirchzarten (B) | Tarodunum, WM 1995; Lüge Rheintalbahn | **Gleiche Bauart:** Lüge über die Bahnstrecke (Schwarzwaldbahn), WM 1995 als Wahrheit |
| Günterstal (Radar) | Kloster | Schauinsland auf Günterstaler Gemarkung, südlichste Straßenbahnhaltestelle, Namensherkunft |
| Horben (C) | Einwohner | Baujahr der Kirche, Dammhöhe, Verluste im Gefecht 1848 |
| Staufen (B) | Faust, Hebungsrisse; Lüge Stadtrecht | **Faust und Hebungsrisse gesperrt** (Bekanntheit hoch); stattdessen Hohenstaufen-Verwandtschaft, Vulkankegel, Partnerstadt |

---

## 5. Befunde

**V1. Die Warum-Regel trägt.** Jeder Zielort hat mindestens drei Fakten zu Herkunft oder Grund, neun von zehn mindestens sieben. Ohne die Regel fehlte in der Probe genau der Fakt, den die Karte braucht.

**V2. Bei Stadtteilen ist der Artikel zu dünn.** Zähringen hat 570 Wörter und drei Warum-Fakten; der Fakt der handgeschriebenen Karte steht dort nicht. Er steht vermutlich im Artikel über die Burg oder das Herzogsgeschlecht. Das ist der Fall, für den E4 eine zweite Quelle vorsieht; näher als die Gemeinde-Webseite liegen hier die Artikel, auf die der Ortsartikel verweist.

**V3. Der Bekanntheitsfilter sperrt genau die großen Fakten.** Das Modell stufte die Schwarzwaldklinik, Fausts Tod und die Hebungsrisse als „hoch" ein und hielt sie aus den Fragen. Das ist die Regel aus §8 Nr. 6 und deckt sich mit dem ersten Test (Karte 6 gewusst, Karte 10 ohne Theorie). Die Folge sieht man an Staufen: Die drei Vorschläge sind regelgerecht und deutlich leiser als die handgeschriebene Karte. Ob das am Tisch besser oder schlechter spielt, ist offen. In keiner der 30 Rückseiten kommt einer der drei gesperrten Fakten vor; als Reveal-Material, wie die Regel es vorsieht, wurden sie nicht genutzt.

**V4. Der Kontext-Spiegel spielt kaum eine Rolle.** Nur 3 von 30 Vorschlägen nutzen einen gespiegelten Fakt eines Spenderorts, alle in Familie B. In 21 Vorschlägen widerlegen die Fakten des Zielorts die falsche Option selbst. Die zehn Spenderorte waren die Hälfte des Extraktionsaufwands. Für Familie A sind sie entbehrlich; für B reichen wenige.

**V5. Anschlüsse entstehen, der wirksamste nicht.** 9 der 11 Anschlüsse sind Vergleiche aus Grunddaten (Klasse a). Zwei kommen aus Fakten, die den letzten Ort ausdrücklich nennen: Glottertal wird 1112 in einer Güterbeschreibung des Klosters St. Peter zuerst erwähnt; der Bohrer-Bach aus Horben heißt ab Günterstal Hölderlebach. Der Anschluss St. Peter – Zähringen, der im ersten Test gut wirkte, fiel aus: Die Fakten nennen „Herzog Berthold II. von Zähringen", also das Geschlecht, und die Regel verlangt den Ort.

**V6. Radar ist aus extrahierten Fakten nicht erzeugbar.** „Welcher dieser Orte hat X?" braucht für die übrigen Orte den Nachweis, dass sie X nicht haben. Nach E5 geht das nur aus einer vollständigen Quelle. Aus Wikipedia-Extraktionen folgt es nie. Radar braucht Schicht 0 mit vollständiger Erfassung (etwa OpenStreetMap für Freibad, Bahnhof, Burg).

**V7. Familie C zieht nach unten.** Für Spannen und Leiter greift der Prompt zu jeder Zahl, die er findet: Dammhöhe 13,5 m, Verluste „etwa 20", Übernachtungen 85.375. Formal richtig, aber kaum etwas, worüber man eine Theorie hat. Die handgeschriebenen C-Karten nahmen Einwohner und Höhe, also Zahlen, zu denen der Steckbrief Anhaltspunkte gibt.

**V8. Was die Durchläufe selbst als Regelverstoß oder Lücke meldeten:**
- Gundelfingen, Vorschlag 1: Hebels Geburtsjahr stammt aus Allgemeinwissen, nicht aus den Fakten.
- Denzlingen, Vorschlag 2: Die Lüge ist teilwahr (die Kirche kam wirklich aus Emmendingen, nur nicht per Bahn).
- Zähringen, Vorschlag 2: handelt weitgehend von Gundelfingen, einem Ort der Fahrt, und doppelt sich mit dessen Karte.
- Umkirch, Vorschlag 1: Die Übersetzung „Kirche in den Wellen" stand diesmal nicht in den Fakten; die falsche Option „um die Kirche" ist aus dem Ortsnamen gebildet.
- Leiter: Was die Ziffer in „Richtig war N." bedeutet, regelt der Prompt nicht.
- Weg (a) bei „ältester Nachweis um 1580": widerlegt streng genommen nur den Beleg, nicht das Bestehen davor.

**V9. Schicht 0 hat eigene Fehler.** Horben: Wikidata 495 m, Artikel und handgeschriebene Karte 607 m. Der Durchlauf hat die Höhe deshalb gemieden. Die Zugehörigkeit aus Wikidata enthält historische Einheiten ohne Enddatum (Landamt Freiburg, Bezirksamt Neustadt). Nach E3 sind widersprüchliche Werte gleichwertig; für Spannen-Fragen heißt das: Ein Wert mit zwei Belegen in verschiedenen Spannen trägt keine C-Karte.

**V10. Dieselbe Extraktion ist nicht wiederholbar gleich.** In der Probe am Nachmittag stand die Übersetzung „Kirche in den Wellen" in den Umkirch-Fakten, im Volllauf nicht (anderer Durchlauf, anderes Modell, Klartext statt Webseite). Die Karte entstand trotzdem.

---

## 6. Aufwand

- Extraktion: 20 Durchläufe, je 1 bis 7,5 Minuten, zusammen rund 1,5 Millionen Tokens mit dem kleinen Modell.
- Karten: 10 Durchläufe, je 2 bis 4 Minuten, zusammen rund 1,1 Millionen Tokens mit dem großen Modell.
- Das sind Obergrenzen: Die Durchläufe liefen als eigenständige Agenten mit ihrem ganzen Rahmen. Ein nackter Aufruf mit Prompt und Artikel braucht einen Bruchteil. Der Versuch, die Extraktion als Skript über die Kommandozeile laufen zu lassen, hing ohne Ausgabe und ist offen.

### Wo ein Mensch mehr bringt als die Automatik

- **Auswahl je Ort:** zehn Kreuze im Kuratierblatt. Das ersetzt eine Bewertung „ruft eine Theorie hervor", die der Prompt nicht leistet (V7).
- **Bekanntheit:** Das Modell hat ohne Schwelle entschieden. Ob Faust in Staufen wirklich zu bekannt ist, sagt der Tisch (Kürzel W), nicht der Prompt.
- **Negativnachweise:** je gewählter Karte zwei bis drei Zeilen gegenlesen; die Durchläufe haben ihre Zweifelsfälle selbst markiert.

---

## 7. Was Mike entscheidet

1. **Auswahl:** im Kuratierblatt je Ort einen Vorschlag ankreuzen oder „keiner".
2. **Bekanntheit:** Soll der Filter so streng bleiben, dass Faust und Hebungsrisse in Staufen nicht einmal als wahre Aussage einer Lügen-Karte vorkommen? Vorschlag: für den Feldtest zwei Staufen-Karten spielen, eine mit und eine ohne, und W zählen.
3. **Anschluss:** Darf ein Anschluss auch gelten, wenn der Fakt den Namen des letzten Orts als Teil eines anderen Namens nennt (Herzog von Zähringen, Kloster St. Peter)? Vorschlag: ja, als Kann, mit Gegenlesen beim Kuratieren.
4. **Zweite Quelle bei dünnen Artikeln:** Dürfen die im Ortsartikel verlinkten Artikel (Burg Zähringen) mitgelesen werden? Vorschlag: ja, wenn der Ortsartikel unter 1.000 Wörtern liegt.
5. **Familie C:** Nur Zahlen aus den Grunddaten (Einwohner, Höhe, Fläche, Ersterwähnung) zulassen? Vorschlag: ja.

**Mikes Antwort am selben Abend (zwei Vorgaben, als E9 und E10 in `gemeinde-achsen-entscheidungen-2026-10-01.md`):**
- Zu Punkt 2: Der Bekanntheitsfilter wird stark abgeschwächt. Ein Glückstreffer ist erwünscht; lieber die Frage auf ein Detail legen, als den Fakt zu sperren.
- Neu: Ziel sind sieben Fragen je Ort, auch für kleine Orte, mit Klassikern (Größe, Kennzeichen) und Politischem (stärkste Partei). Das deckt Punkt 5 mit ab: Zahlen aus den Grunddaten werden ausdrücklich gewollt.
- Die Punkte 1, 3 und 4 sind noch offen.

Nächster Schritt, in einer neuen Sitzung: Spielkonzept v0.2.6, Grunddaten erweitern (Kennzeichen, Fläche, Wahl), Karten-Prompt v0.5, zweiter Volllauf auf den zehn Zielorten.

*Ende Bericht.*
