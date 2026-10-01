# QuizAway — Stufe 2, Faktencheck der 100 Karten: Bericht

**Datum:** 2026-10-02 · **Anlass:** Mike zur Prüffrage „Stimmt die Auflösung?": „da müsste ich selbst im Internet recherchieren – das kannst du effizienter." · **Gegenstand:** die 70 Karten des zweiten Volllaufs (Prompt v0.5) und die 30 Vorschläge des ersten (Prompt v0.4), zehn Zielorte Raum Freiburg · **Daten:** `data/gemeinde-achsen/iter1/faktencheck/`

**Ergebnis in einem Satz:** Von 100 Karten sind 60 bestätigt, 31 korrigiert, 4 nur durch Wikipedia belegt und 5 gesperrt; sechs Karten hatten eine „falsche" Option oder eine „Lüge", die in Wirklichkeit stimmt oder der Wahrheit nahekommt.

Was der Check nicht leistet: Er beweist keine Karte. „Bestätigt" heißt, dass Artikel und eine zweite Quelle übereinstimmen und sich kein Widerspruch fand.

---

## 1. Wie geprüft wurde

Je Ort ein Durchlauf mit Netzzugang, Auftrag in `faktencheck/auftrag.txt`. Je Karte fünf Schritte:

1. Jede Tatsachenbehauptung gegen den Klartext des Wikipedia-Artikels, aus dem die Fakten extrahiert wurden (die Kartenläufe hatten den Artikel nie gesehen).
2. Die Kernaussage gegen mindestens eine Quelle außerhalb von Wikipedia: Gemeinde-Webseite, LEO-BW, Landesarchiv, Badische Landesbibliothek, Zeitung, Fachseite.
3. Jede falsche Option und jede Lüge: Ist sie wirklich falsch?
4. Aktualität: Stimmt es heute noch?
5. Die Anschlüsse.

Urteil je Karte: OK, KORRIGIEREN oder UNSICHER, mit Beleg. Rohurteile: `faktencheck/<ort>.md`, zusammengeführt in `urteile.json`.

**Gegenprobe der Prüfer:** Fünf Befunde habe ich selbst im Netz nachgeprüft (Störche in Denzlingen seit 1993; Carlsbau erst ab 1960 Klinik der Landesversicherungsanstalt; St. Peter Anfang 1806 württembergisch besetzt; Wildtal 72 Prozent; Altkennzeichen MÜL und NEU seit Oktober 2023). Alle fünf stimmen. Einen sechsten (Grimmelshausen und Denzlingen) konnte auch ich nicht bestätigen.

---

## 2. Zahlen

| | bestätigt | korrigiert | unsicher | gesperrt |
|---|---|---|---|---|
| Zweiter Lauf (70 Karten) | 43 | 18 | 4 | 5 |
| Erster Lauf (30 Vorschläge) | 17 | 13 | 0 | 0 |
| **zusammen** | **60** | **31** | **4** | **5** |

- Die Klassiker (30 Karten aus Grunddaten) sind bis auf zwei bestätigt: Wahl, Landkreis, Höhe und Entfernung halten. Die zwei Ausnahmen sind ein Steckbrief-Satz und das Kennzeichen (F4).
- Bei einer bestätigten Karte (Günterstal, Ortshöhe) fand sich keine zweite Quelle; sie stützt sich auf die Grunddaten allein.
- Aufwand: zehn Durchläufe, je vier bis sechs Minuten, zusammen rund 1,4 Millionen Tokens, also etwa so viel wie das Schreiben der 70 Karten.

---

## 3. Befunde

**F1. Sechs Karten hatten eine „falsche" Antwort, die stimmt.** Das ist der Fehler, der am Tisch am meisten kostet, weil er die richtige Theorie bestraft.

| Karte | Was als falsch galt | Was stimmt | Folge |
|---|---|---|---|
| St. Peter, Lügen-Karte | „1806 kam das Dorf zu Württemberg" | St. Peter war vom 12. Januar bis 18. Februar 1806 württembergisch besetzt | Lüge ersetzt (Bayern) |
| Glottertal, Klinik-Karte | „Grandhotel für wohlhabende Sommergäste" | Bis 1960 war der Carlsbau ein Sanatorium für wohlhabende Kurgäste | Frage auf die Zeit der Dreharbeiten gelegt |
| Günterstal, Straßenbahn | „Eine deutsche Stadt weiter südlich baute eine Straßenbahn" | Weil am Rhein ließ den deutschen Abschnitt der Basler Linie 8 bauen | Option ersetzt (Konstanz) |
| Zähringen, Unterführung | „zu eng", „Anwohner haben es durchgesetzt" | Engstelle und Anwohnerinitiative gehören zur wirklichen Vorgeschichte | gesperrt |
| Zähringen, Burg | „Eine Urkunde nennt einen Herzog als Bauherrn" | Burgen-Quellen nennen Berthold II. als Erbauer vor 1100 | gesperrt |
| Horben, Eingemeindung | „Freiburg suchte Bauland", „wollte den Wald" | Der Antrag von 1935 wurde mit der Stadtentwicklung begründet; um den Wald stritt man lange | gesperrt |

Fünf der sechs Fälle sind frei erfundene Theorien nach Weg (c). Der Weg setzt voraus, dass die Fakten „genau einen Grund" nennen; ob es in der Wirklichkeit weitere gibt, kann der Kartenlauf nicht wissen.

**F2. Rund 15 Fehler standen schon im Wikipedia-Artikel** und sind durch Extraktion und Karte unverändert durchgelaufen:
- „Dreiviertelmehrheit" in Wildtal; die Gemeinde nennt 72 Prozent.
- „Großherzogtum Baden" für 1805; Baden war bis 1806 Kurfürstentum (drei Karten).
- „bislang einzige Mountainbike-WM auf deutschem Boden" in Kirchzarten; 2010 gab es die Marathon-Weltmeisterschaft in St. Wendel (zwei Karten).
- Störche auf dem Denzlinger Storchenturm „seit 1983"; die Gemeinde nennt 1993.
- „Befehl Napoleons" zur Auflösung des Klosters Günterstal; es war Baden.
- „Deutschlands letzte erhaltene gusseiserne Straßenbrücke" in Staufen; die Stadt sagt „eine der wenigen".

Eine Karte, die dem Artikel treu folgt, ist damit noch nicht richtig.

**F3. Die Kartenläufe glätten Vorbehalte weg.** „Gilt als älteste Pfarrkirche" wird zu „ist die älteste" (drei Umkirch-Karten). Die Sage, der Burgherr habe Faust als Goldmacher angestellt, wird zur Tatsache. Ein Weinberg des 19. Jahrhunderts „liegt" auf 720 Metern. Das Kloster St. Peter „ist" 930 Jahre alt, obwohl es 1806 aufgehoben wurde. Regel 1 des Prompts deckt „vermutlich" und „soll" ab, greift aber nicht bei „gilt als", bei Sagen und bei Vergangenem.

**F4. Drei Angaben sind veraltet.** Die Bahnagentur im Hofgut Himmelreich ist geschlossen. Die Sperrung der Unterführung in Zähringen ist ein Plan, kein Vollzug. Und das Kennzeichen ist nicht mehr einwertig: Der Landkreis Breisgau-Hochschwarzwald gibt seit dem 2. Oktober 2023 neben FR auch MÜL und NEU an alle Einwohner aus. Wikidata nennt nur FR. Für den Negativnachweis bei Kennzeichen-Karten heißt das: Altkennzeichen des Kreises dürfen nicht als falsche Option auftauchen.

**F5. Zwei Fehler kommen aus der Extraktion.** In Horben machte sie aus „Spitalkirche 1805/06 aufgehoben" ein „Portal kam 1805/06 nach Horben"; in Gundelfingen aus dem ersten Schulmeister 1661 ein Gründungsjahr der heutigen Schule.

**F6. Vier Karten hängen an einem einzelnen Wikipedia-Satz ohne zweiten Beleg** (unsicher): der Ginster-Handel mit Basel und Georg von Sachsen als Seminarist in St. Peter, die Versorgung Freiburgs aus Gundelfingen im Ersten Weltkrieg, der Ritt Napoleons III. durch Horben. Sie bleiben spielbar und tragen den Vermerk.

**F7. Gesperrt sind fünf Karten:** Denzlingen 5 (Spiraltreppe und Dürer: unbelegte Vermutung mit widersprüchlicher Datierung) und 7 (Grimmelshausen: ein unbelegter Satz, nirgends bestätigt), Zähringen 5 und 7, Horben 1 (siehe F1). Denzlingen, Zähringen und Horben haben damit im zweiten Lauf fünf oder sechs statt sieben Karten; mit den Vorschlägen des ersten Laufs bleiben alle Orte über sieben.

**F8. Mikes Favoriten aus dem ersten Blatt halten.** Von den 17 angekreuzten Vorschlägen sind 14 bestätigt und 3 korrigiert (Umkirch 1, Kirchzarten 1, Günterstal 2), keiner gesperrt. Die Korrekturen sind im Blatt nachgezogen; die Kreuze stehen unverändert.

---

## 4. Was daraus folgt

1. **Der Faktencheck wird das vierte Glied der Kette:** Extraktion, Karte, Faktencheck, Kuratieren. Er kostet so viel wie das Kartenschreiben und findet bei vier von zehn Karten etwas.
2. **Korrekturen liegen als eigene Schicht vor.** Die Rohausgaben der Läufe bleiben unverändert; `faktencheck/korrekturen.json` nennt je Karte Status, Grund und Ersetzungen, `scripts/data-build/gemeinde_achsen_korrekturen_anwenden.py` schreibt die geprüften Fassungen nach `karten-geprueft/`. Nach jeder Korrektur sind die Wortgrenzen neu geprüft.
3. **Für den Karten-Prompt v0.6:** Vorbehalte der Quelle bleiben stehen („gilt als", „der Sage nach"); Vergangenes steht in der Vergangenheit; Superlative tragen in einer Lügen-Karte keine wahre Aussage; eine Frage nach etwas, das sich geändert hat, nennt ihren Zeitpunkt.
4. **Für Weg (c):** Eine frei erfundene Theorie über einen Grund oder Anlass ist erst nach dem Faktencheck zulässig. Der Kartenlauf darf sie schreiben, der Check muss sie freigeben.
5. **Für die Grunddaten:** Das Kennzeichen wird als mehrwertig geführt (Altkennzeichen).

### Wo ein Mensch mehr bringt als die Automatik

- **Nichts mehr an der Sachprüfung.** Die liegt jetzt vollständig bei der Maschine; für Mike bleiben Geschmack, Theorie-Gefühl und die erste Karte je Ort.
- **Die fünf gesperrten Karten:** Wer vor Ort die Ortschronik zur Hand hat, klärt Grimmelshausen in Denzlingen oder die Unterführung in Zähringen in einer Minute. Sonst entfallen sie.

---

## 5. Was ab jetzt da ist

Das Kuratierblatt zum zweiten Lauf zeigt jede Karte in der geprüften Fassung mit ihrem Urteil; im Blatt zum ersten Lauf steht das Urteil an jedem Vorschlag. 95 der 100 Karten sind spielbar, 60 davon ohne jede Änderung, und bei jeder korrigierten steht, was geändert wurde und warum.

*Ende Bericht.*
