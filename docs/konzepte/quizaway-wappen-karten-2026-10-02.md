# QuizAway Reise-Modus – Wappen-Karten (Lauf w0.1), 2026-10-02

Fragenfamilie Wappen nach Mikes Entscheid vom 2. Oktober 2026: Warum-Frage (woher stammt eine Figur, wofür steht sie); ohne belegte Begründung keine Karte. Quelle je Ort: Wappenabschnitt und Wappentabelle des Ortsartikels, Eintrag der Wikipedia-Wappenliste, wo nötig Nachrecherche (LEO-BW, Gemeinde, Stadt Neuwied). Kette: `gemeinde_achsen_wappen.py` → Extraktion → `gemeinde_achsen_fakten.py` → `gemeinde_achsen_wappen_eingabe.py` → Kartenlauf (Prompt v0.7 mit Zusatz `prompt-karten-wappen-v0.1.txt`) → Prüfskript `--lauf w0.1` → Faktencheck (`faktencheck/auftrag-w0.1.txt`), Befunde eingearbeitet.

Ohne Wappen-Karte: Zähringen (nur Blasonierung belegt), Günterstal (kein Ortswappen, nur das des Klosters), Rengsdorf (für die Ortsgemeinde nichts belegt). UNSICHER heißt unten: Die Aussage trägt allein die amtliche Quelle (LEO-BW = Landesarchiv, Gemeinde, Stadt); ich werte das als belegt.

**Fragen an Mike** (Kreuz setzen):

- [ ] Passt die Kartenform (Figur in Alltagsworten, vier Theorien, Herkunft auf der Rückseite)? Wenn nein: was stört?
- [ ] Gundelfingen Karte 1 und Denzlingen Karte 1 fragen beide nach dem badischen Schrägbalken. Beide behalten? (Vorschlag: nur Gundelfingen; Denzlingen hat die Pflugschar.)
- [ ] Kommen die Wappen-Karten in den Vorrat (je Ort ein bis zwei Karten zusätzlich)?

Einzelne Karten streichen: Kreuz in die Zeile „streichen“ der Karte.

## Raum Freiburg

### Umkirch, Karte 1

> Gemeinde mit rund 5.700 Einwohnern, 8 km nordwestlich von Freiburg im Breisgau.
> Im Wappen von Umkirch steht eine Frau in weißem Gewand mit goldener Krone und einem Kind. Woher stammt sie?
> 1. Sie geht auf eine Marienerscheinungs-Sage zurück.
> 2. Sie erinnert an eine Wallfahrt durch den Ort.
> 3. Die Kirche des Ortes ist Maria geweiht.
> 4. Sie geht auf eine fromme Stiftung zurück.

Du hattest [Option] getippt. Eine Legende liegt nahe, denn Marienfiguren haben oft eine fromme Geschichte. Die Madonna steht hier für das Marienpatrozinium der Pfarrkirche Umkirch, also für die Weihe der Kirche an Maria. Sie zeigt schon das erste Gemeindesiegel, entstanden nach 1831. Richtig war 3.  
Quelle: Wikipedia, Artikel „Umkirch“

*Faktencheck: OK*

- [ ] streichen

### Gundelfingen, Karte 1

> Gemeinde mit rund 12.100 Einwohnern, 5 km nördlich von Freiburg im Breisgau.
> Im Wappen von Gundelfingen steht ein roter schräger Balken auf goldenem Grund. Wofür steht er?
> 1. Er erinnert an eine Schlacht in der Nähe.
> 2. Er zeigt die einstige Zugehörigkeit zu Baden.
> 3. Er geht auf das Zeichen einer Zunft zurück.
> 4. Er stellt einen alten Grenzweg zwischen Dörfern dar.

Du hattest [Option] getippt. Ein Schrägstreifen erinnert leicht an einen Weg oder eine Grenzlinie. Hier ist er das badische Herrschaftswappen, das Zeichen der einstigen Zugehörigkeit zu Baden. Richtig war 2.  
Quelle: Wikipedia, Artikel „Gundelfingen (Breisgau)“

*Faktencheck: OK*

- [ ] streichen

### Gundelfingen, Karte 2

> Gemeinde mit rund 12.100 Einwohnern, 5 km nördlich von Freiburg im Breisgau.
> Im Wappen von Gundelfingen steht eine silberne Tanne in einem silbernen Zaun. Woher stammt sie der Überlieferung nach?
> 1. Eine Sage erzählt von einem Wunderbaum im Ort.
> 2. Sie erinnert an einen großen Waldbrand.
> 3. Sie steht für ein altes Holzgewerbe der Dorfbewohner.
> 4. Ein alemannischer Fürst soll hier Land besessen haben.

Du hattest [Option] getippt. Zu einer Tanne passen Wald und Holz. Die Überlieferung nennt aber Besitz: Der alemannische Fürst Gundolf soll hier Land besessen haben, später habe der Basler Bischof Adalbero das Wildbannrecht, das Jagdrecht, gehabt. Richtig war 4.  
Quelle: Wikipedia, Artikel „Gundelfingen (Breisgau)“

*Faktencheck: OK*

- [ ] streichen

### Denzlingen, Karte 1

> Gemeinde mit rund 13.700 Einwohnern, 8 km nördlich von Freiburg im Breisgau.
> Im Wappen von Denzlingen steht ein roter schräger Balken auf Gold. Woher stammt er?
> 1. Er ist ein Herrschaftszeichen, das mehrere Orte teilen.
> 2. Er stammt vom Familienzeichen eines Dorfgründers.
> 3. Er stellt eine Weidegrenze zwischen zwei Dörfern dar.
> 4. Er stammt aus einer Sage über einen Kampf.

Du hattest [Option] getippt. Ein Balken wirkt wie ein Zeichen für eine Grenze, eine Sage oder einen Gründer. Hier ist er ein herrschaftliches Wappenbild, wie es auch andere markgräfliche Orte führen. Es erscheint auf Siegeln von 1458, aus dem 16. und aus dem 18. Jahrhundert. Richtig war 1.  
Quelle: Wikipedia, Artikel „Denzlingen“

*Faktencheck: OK*

- [ ] streichen

### Denzlingen, Karte 2

> Gemeinde mit rund 13.700 Einwohnern, 8 km nördlich von Freiburg im Breisgau.
> Im Wappen von Denzlingen steht ein silbernes Pflugeisen auf blauem Grund. Woher stammt es?
> 1. Es kam erst bei einer Wappenänderung neu hinzu.
> 2. Es erinnert an die Gründung des ersten Hofs.
> 3. Es ist ein altes Dorfzeichen aus Grenzbeschreibungen.
> 4. Es ist das Zeichen einer Zunft im Ort.

Du hattest [Option] getippt. Ein Pflugeisen wirkt wie das Zeichen von Bauern oder einem Hof. Die Pflugschar ist ein altes Denzlinger Dorfzeichen, belegt in Banngrenzbeschreibungen des 18. Jahrhunderts. Schon das älteste Siegel des Gerichts Denzlingen von 1458 zeigt sie. Richtig war 3.  
Quelle: Wikipedia, Artikel „Denzlingen“

*Faktencheck: OK*

- [ ] streichen

### St. Peter, Karte 1

> Gemeinde mit rund 2.700 Einwohnern, 14 km östlich von Freiburg im Breisgau.
> Im Wappen von St. Peter stecken zwei gekreuzte goldene Schlüssel am Baumstamm. Woher stammen sie?
> 1. Sie erinnern an das einstige Wirtshaus des Ortes.
> 2. Sie stammen aus einer Sage vom Schlüssel.
> 3. Sie stammen aus dem Klosterwappen des Ortes.
> 4. Sie stehen für das Schlosserhandwerk im Ort.

Du hattest [Option] getippt. Schlüssel zieren oft Wirtshäuser oder Handwerker. Hier sind es Petersschlüssel aus dem Wappen des Klosters St. Peter. Auch auf dem Siegel der Klostervogteien gegen Ende des 18. Jahrhunderts erscheinen Schlüssel. Richtig war 3.  
Quelle: LEO-BW, Ortslexikon St. Peter

*Faktencheck: UNSICHER – Kernaussage steht nur in LEO-BW (zugleich die Quelle der Karte) und ist plausibel (Petrusschlüssel als Klostersymbol), aber nicht unabhängig bestätigt; daher UNSICHER, keine Änderung nötig. Die Karte ist in Ordnung, wenn*

- [ ] streichen

### Glottertal, Karte 1

> Gemeinde mit rund 3.200 Einwohnern, 10 km nordöstlich von Freiburg im Breisgau.
> Im Wappen von Glottertal stehen unten sechs schwarze Hügel. Woran erinnern sie?
> 1. Sie erinnern an die Kohlenmeiler der früheren Köhler.
> 2. Sie erinnern an eine frühere Herrschaft.
> 3. Sie gehen auf eine Sage vom Berg zurück.
> 4. Sie stehen für einen großen Hof im Tal.

Du hattest [Option] getippt. Schwarz im Schwarzwald legt Köhler oder Wald nahe. Der Sechsberg stand auch in den Wappen von Ober- und Unterglottertal und erinnert daran, dass diese Orte einst zur Herrschaft Schwarzenberg gehörten. Richtig war 2.  
Quelle: LEO-BW, Ortslexikon Glottertal

*Faktencheck: KORRIGIEREN – Satz der Rückseite "Der Sechsberg stammt aus den Wappen von Ober- und Unterglottertal": verzerrt die Quelle. Richtig: Der Sechsberg stand auch in den Wappen von Ober- und Unterglottertal (LEO-BW, Ortslexikon Glottertal, *

- [ ] streichen

### Glottertal, Karte 2

> Gemeinde mit rund 3.200 Einwohnern, 10 km nordöstlich von Freiburg im Breisgau.
> Im Wappen von Glottertal steht ein grüner Nadelbaum, eine Föhre. Woher stammt er?
> 1. Er stammt vom Zeichen einer Sägemühle im Tal.
> 2. Er geht auf eine Waldgeist-Sage zurück.
> 3. Er wurde erst bei der Gemeindebildung neu gewählt.
> 4. Er bildet den Namen eines Ortsteils nach.

Du hattest [Option] getippt. Ein Nadelbaum im Schwarzwald wirkt wie ein bloßes Waldmotiv. Die Föhre ist aber ein redendes Bild für den Namen des Gemeindeteils Föhrental; in dessen Siegel steht sie seit etwa 1850, im Wappen seit 1903. Richtig war 4.  
Quelle: LEO-BW, Ortslexikon Glottertal

*Faktencheck: UNSICHER – Die Kernaussage und die Jahreszahlen stehen nur in der WAPPEN-QUELLE (LEO-BW) und in davon abgeleiteten Seiten; eine unabhängige Prüfung war nicht möglich. Es gibt keinen Widerspruch, und die Namensdeutung ist sprachlich*

- [ ] streichen

### Kirchzarten, Karte 1

> Gemeinde mit rund 10.400 Einwohnern, 8 km südöstlich von Freiburg im Breisgau.
> Im Wappen von Kirchzarten steht ein schwarzer Bär mit einem silbernen Doppelkreuz. Wofür steht er?
> 1. Er erinnert an den Ursprung als Klosterbesitz.
> 2. Er erinnert an die Bärenjagd der ersten Siedler.
> 3. Er war das Zeichen einer Zunft im Ort.
> 4. Er war das Zeichen eines Wirtshauses im Ort.

Du hattest [Option] getippt. Bären zieren oft Wirtshäuser oder erinnern an die Jagd. Hier ist es der St. Gallische Bär: Er weist auf die Ursprünge des Ortes als Besitz des Klosters St. Gallen. Richtig war 1.  
Quelle: Wikipedia, Artikel „Kirchzarten“

*Faktencheck: KORRIGIEREN – Option 3 ("Er stammt aus einer Sage von einem Bären.") ist nicht sicher falsch, weil der St. Gallische Bär auf die Gallus-Legende zurückgeht; die Karte behauptet in den NEGATIVNACHWEISEN "eine Sage ist erfunden", was so *

- [ ] streichen

### Kirchzarten, Karte 2

> Gemeinde mit rund 10.400 Einwohnern, 8 km südöstlich von Freiburg im Breisgau.
> Im Wappen von Kirchzarten steht ein halbes rotes Kreuz auf Silber. Woher stammt es?
> 1. Es erinnert an Kreuzfahrer aus dem Ort.
> 2. Es stellt zwei sich kreuzende Handelswege dar.
> 3. Es geht auf ein Pestgelübde zurück.
> 4. Es erinnert an lange Zugehörigkeit zu einer Stadt.

Du hattest [Option] getippt. Ein Kreuz denkt man gern religiös oder als Wegkreuz. Hier ist es das halbe rote Kreuz aus dem Stadtwappen von Freiburg und steht für die lange Zugehörigkeit des Ortes zur Stadt Freiburg. Richtig war 4.  
Quelle: Wikipedia, Artikel „Kirchzarten“

*Faktencheck: OK*

- [ ] streichen

### Horben, Karte 1

> Gemeinde mit rund 1.200 Einwohnern, 7 km südlich von Freiburg im Breisgau.
> Im Wappen von Horben steht ein silberner Pflug auf rotem Grund. Woher stammt er vermutlich?
> 1. Vermutlich geht er auf eine Bauernsage zurück.
> 2. Vermutlich ist er das Zeichen einer Dorfschmiede.
> 3. Vermutlich stammt er von älteren Siegeln früherer Vögte.
> 4. Vermutlich erinnert er an einen Streit um Ackerland.

Du hattest [Option] getippt. Ein Pflug lädt zu Deutungen ein, von Landwirtschaft bis Sage. Vermutlich stammt er von älteren Siegeln der Horbener Vögte: Alle zeigen Pflugscharen, zum Teil mit dem Anfangsbuchstaben des Vogts. Gemeindesiegel mit Pflug sind ab 1818 nachweisbar. Richtig war 3.  
Quelle: LEO-BW, Wappen von Horben (wiedergegeben auf ortswappen.de)

*Faktencheck: UNSICHER – Kernaussage nur durch die WAPPEN-QUELLE (LEO-BW/Landesarchiv) belegt, unabhängig nicht prüfbar; die Karte gibt sie sauber mit Vorbehalt wieder. Kein Fehler gefunden. Empfehlung: so lassen, "niedrig bekannt" ist plausibel*

- [ ] streichen

### Staufen, Karte 1

> Stadt mit rund 8.400 Einwohnern, 16 km südwestlich von Freiburg im Breisgau.
> Im Wappen von Staufen stehen drei goldene Kelche mit Deckeln auf rotem Grund. Was steckt dahinter?
> 1. Sie erinnern an die Messkelche der Ortskirche.
> 2. Das alte Wort „stauf“ bedeutet Becher und Berg.
> 3. Sie stehen für das Handwerk der Goldschmiede.
> 4. Sie stammen aus einer Sage vom Goldbecher.

Du hattest [Option] getippt. Kelche legen Kirche oder Handwerk nahe. Das Wappen beruht auf dem der Freiherren von Staufen. Das germanische Wort „stauf“ bedeutet Becher und kegelförmigen Berg, namensgebend in alemannischer Zeit; die Kelche beziehen sich auch auf die beherrschende Stellung des Schlossbergs. Richtig war 2.  
Quelle: Wikipedia, Artikel „Staufen im Breisgau“

*Faktencheck: OK*

- [ ] streichen

## Raum Neuwied

### Bendorf, Karte 1

> Bendorf ist eine Stadt mit rund 17.700 Einwohnern, 8 km nördlich von Koblenz.
> Im Wappen von Bendorf steht ein goldener Löwe mit zwei Schwänzen. Woher stammt er?
> 1. Er war das Zeichen eines Handwerks der Stadt.
> 2. Er erinnert an eine Sage von einem Löwen.
> 3. Er stammt aus dem Wappen eines Adelsgeschlechts.
> 4. Er wurde erst im 20. Jahrhundert frei erfunden.

Du hattest [Option] getippt. Ein goldener Löwe lässt an eine Sage oder ein Zunftzeichen denken. Er stammt aber aus dem Wappen der Grafen von Sayn, die im Mittelalter Grund- und Gerichtsherren waren und seit Mitte des 14. Jahrhunderts Vögte des Bendorfer Hofes der Abtei Maria Laach. Das Schöffensiegel der zweiten Hälfte des 14. Jahrhunderts zeigt ihn. Richtig war 3.  
Quelle: Wikipedia, Artikel „Bendorf“

*Faktencheck: OK*

- [ ] streichen

### Engers, Karte 1

> Engers ist ein Stadtteil von Neuwied mit rund 5.200 Einwohnern, 8 km nördlich von Koblenz.
> Im früheren Wappen von Engers stand ein Soldat mit Helm und rotem Umhang, neben ihm ein kleiner kniender Mann. Wofür steht diese Szene?
> 1. Sie erinnert an eine Sage von einem Retter.
> 2. Sie zeigt den Schutzpatron der Ortskirche.
> 3. Sie war das Zeichen einer alten Engerser Zunft.
> 4. Sie stammt aus dem Familienwappen eines Engerser Geschlechts.

Du hattest [Option] getippt. Ein Soldat im Wappen lässt an Krieg oder Sage denken. Tatsächlich ist es St. Martin als römischer Soldat, der Schutzpatron der Kirche zu Engers: Er gibt einem Bedürftigen einen Teil seines Mantels. Das Wappen gehörte der ehemaligen Stadt Engers. Richtig war 2.  
Quelle: Wikipedia, Artikel „Engers“

*Faktencheck: OK*

- [ ] streichen

### Engers, Karte 2

> Engers ist ein Stadtteil von Neuwied mit rund 5.200 Einwohnern, 8 km nördlich von Koblenz.
> Im früheren Wappen von Engers stand ganz unten ein kleines Schild mit rotem Kreuz auf Silber. Wofür steht es?
> 1. Es erinnert an einen Kreuzzug aus dem Ort.
> 2. Es war das Zeichen einer Bruderschaft der Ortskirche.
> 3. Es stammt vom Siegel einer Engerser Bürgerfamilie.
> 4. Es zeigt, zu welchem Herrschaftsgebiet der Ort gehörte.

Du hattest [Option] getippt. Ein rotes Kreuz weckt leicht Gedanken an Kreuzzüge oder fromme Vereinigungen. Hier ist es das Zeichen der Zugehörigkeit zum kurtrierischen Gebiet. Das kleine Schild stand im Schildfuß des Stadtwappens der ehemaligen Stadt Engers. Richtig war 4.  
Quelle: Wikipedia, Artikel „Engers“

*Faktencheck: OK*

- [ ] streichen

### Heimbach-Weis, Karte 2

> Heimbach-Weis ist ein Stadtteil von Neuwied mit rund 7.300 Einwohnern, 11 km nördlich von Koblenz.
> Frühere Ortswappen im heutigen Heimbach-Weis zeigten einen Apfel, einen Winkel und ein Kreuz. Zwei dieser Aussagen stimmen, eine ist gelogen. Welche?
> 1. Der Apfel steht für den Obstanbau des Ortes.
> 2. Das Kreuz steht für eine Pilgerfahrt des Ortes.
> 3. Der Winkel steht für die Bimsbaustein-Industrie.

Du hattest [Option] getippt. Ein Kreuz im Wappen lässt an Kreuzzug oder Pilgerfahrt denken. Hier ist es das kurtrierische Kreuz, Zeichen der Zugehörigkeit zu Kurtrier von 1606 bis 1803. Der Stufensparren erinnert an die Bimsbaustein-Industrie, der Apfel an den Obstanbau des Ortes. Die Lüge war 2.  
Quelle: Stadt Neuwied, Stadtteilseite Heimbach-Weis

*Faktencheck: UNSICHER – Kernaussage nur in der WAPPEN-QUELLE; Jahresangabe 1606 nur indirekt gestützt. Kein Widerspruch gefunden.*

- [ ] streichen

### Altwied, Karte 1

> Altwied ist ein Stadtteil von Neuwied mit rund 670 Einwohnern, 16 km nordwestlich von Koblenz.
> Im früheren Wappen von Altwied stand oben ein Turm mit zerfallenem Zinnenkranz. Was stellt er dar?
> 1. Er erinnert an einen früheren Wachturm des Ortes.
> 2. Er erinnert an eine Sage vom verwunschenen Turm.
> 3. Er war das Zeichen einer Altwieder Bürgerfamilie.
> 4. Er zeigt die Ruine einer Burg des Ortes.

Du hattest [Option] getippt. Ein Turm mit Zinnen wirkt zunächst wie ein Wachturm. Tatsächlich stellt er die Ruine der Burg Altwied dar, der Stammburg der wiedischen Grafen. Das Wappen gehörte der ehemaligen Gemeinde Altwied. Richtig war 4.  
Quelle: Wikipedia, Artikel „Altwied“

*Faktencheck: OK*

- [ ] streichen

### Dierdorf, Karte 1

> Dierdorf ist eine Stadt mit rund 6.200 Einwohnern, 22 km nördlich von Koblenz.
> Im Wappen von Dierdorf steht ein schwarzes Zeichen auf Gold aus zwei Balken unter einem Dreieck. Woher stammt es?
> 1. Es war das Zeichen eines Handwerks der Stadt.
> 2. Das ist bis heute ungeklärt.
> 3. Es erinnert an eine Sage über einen Stadtbrand.
> 4. Es wurde erst im 20. Jahrhundert neu erfunden.

Du hattest [Option] getippt. Ein altes Zeichen im Stadtsiegel lässt an Zunft oder Handwerk denken. Die Quelle nennt die Herkunft unbekannt; mehrere Deutungsversuche sind nicht schlüssig. Vermutlich ist es ein altes Ortskennzeichen oder Gemarkungszeichen. Schon der älteste erhaltene Siegelabdruck von 1651 zeigt es, damals mit der Dreieckspitze nach unten. Richtig war 2.  
Quelle: Wikipedia, Artikel „Dierdorf“

*Faktencheck: KORRIGIEREN – Satz: "Das weiß bis heute niemand." Quelle: Herkunft und Bedeutung unbekannt, Deutungsversuche vorhanden aber nicht schlüssig, wohl Ortskennzeichen. Vorschlag: "Seine Herkunft ist bis heute ungeklärt." Zusätzlich wirkt d*

- [ ] streichen

### Waldbreitbach, Karte 1

> Waldbreitbach ist eine Gemeinde mit rund 1.900 Einwohnern, 25 km nordwestlich von Koblenz.
> Im Wappen von Waldbreitbach steht ein schwarzes Kreuz auf Silber. Woher stammt es?
> 1. Es erinnert an einen Orden im Ort.
> 2. Es erinnert an eine Sage von einem Waldkreuz.
> 3. Es stammt aus dem Familienwappen einer Bürgerfamilie.
> 4. Es wurde erst im 20. Jahrhundert frei erfunden.

Du hattest [Option] getippt. Ein Kreuz lässt an Sagen oder Familien denken. Tatsächlich ist es das Zeichen des Deutschen Ordens, der in Waldbreitbach bis zur Auflösung 1809 eine Kommende mit Komtur unterhielt, laut Gemeinde seit 1260. Die Gemeinde übernahm sein Kreuz zur Erinnerung an die jahrhundertelange Anwesenheit. Richtig war 1.  
Quelle: Gemeinde Waldbreitbach, Wappenbeschreibung

*Faktencheck: KORRIGIEREN – Satz der Rückseite: "der von 1260 bis zur Auflösung 1809 in Waldbreitbach präsent war". Die Gemeindeseite sagt es so, aber zweite Quelle datiert das Deutsche Haus schon auf 1239 (erste Erwähnung); 1260 ist das Jahr der P*

- [ ] streichen

### Waldbreitbach, Karte 2

> Waldbreitbach ist eine Gemeinde mit rund 1.900 Einwohnern, 25 km nordwestlich von Koblenz.
> Im Wappen von Waldbreitbach wächst unten ein halbes silbernes Rad aus einer blauen Spitze. Wofür steht es?
> 1. Es erinnert an Kutschen, die hier Reisende beförderten.
> 2. Es erinnert an eine Sage vom Wagenrad.
> 3. Es erinnert an Mühlen und steht für Handwerk.
> 4. Es stammt aus dem Familienwappen einer Bürgerfamilie.

Du hattest [Option] getippt. Bei einem Rad denkt man leicht an Wagen und Kutschen. Es ist aber ein Mühlrad: Es erinnert an die Öl- und Getreidemühlen des Orts, von denen einige bis etwa zur Mitte des 20. Jahrhunderts liefen, und steht zugleich für Handwerk und mittelständisches Gewerbe. Richtig war 3.  
Quelle: Gemeinde Waldbreitbach, Wappenbeschreibung

*Faktencheck: UNSICHER – Kernaussage nur in der WAPPEN-QUELLE (Gemeinde selbst, an sich zuverlässige Primärquelle); nicht unabhängig geprüft. Kein Widerspruch gefunden.*

- [ ] streichen

### Linz am Rhein, Karte 1

> Linz am Rhein ist eine Stadt mit rund 6.300 Einwohnern, 23 km südöstlich von Bonn.
> Im Wappen von Linz am Rhein steht ein goldener Schlüssel auf rotem Grund. Wofür steht er?
> 1. Er war das Zunftzeichen der Linzer Schlosser.
> 2. Er erinnert an den Schlüssel zum Stadttor.
> 3. Er geht auf das Familienzeichen einer Bürgerfamilie zurück.
> 4. Er ist das Zeichen eines Heiligen und Kirchenpatrons.

Du hattest [Option] getippt. Ein Schlüssel lässt an Stadttor oder Handwerk denken. Hier ist er das Attribut des Heiligen Petrus, des Schutzpatrons der Kölner Kirche. Kreuz und Schlüssel stehen schon in Stadtsiegeln des 14. Jahrhunderts. Richtig war 4.  
Quelle: Wikipedia, Artikel „Linz am Rhein“

*Faktencheck: UNSICHER – Kernaussage (Petrusschlüssel, Köln) unabhängig bestätigt. Die Jahreszahl der Rückseite "ältestes Stadtsiegel von 1340" ist nur durch Wikipedia gedeckt; die regionalgeschichte-Seite kennt als ältesten erhaltenen Abdruck 1*

- [ ] streichen

### Linz am Rhein, Karte 2

> Linz am Rhein ist eine Stadt mit rund 6.300 Einwohnern, 23 km südöstlich von Bonn.
> Im Wappen von Linz am Rhein steht oben ein schwarzes Kreuz auf Silber. Wofür steht es?
> 1. Es erinnert an einen Kreuzzug aus dem Ort.
> 2. Es zeigt, zu welchem Herrschaftsgebiet die Stadt gehörte.
> 3. Es stammt aus dem Familienwappen einer Bürgerfamilie.
> 4. Es wurde erst von einem Heimatforscher frei erfunden.

Du hattest [Option] getippt. Ein schwarzes Kreuz lässt an Kreuzzüge denken. Hier deutet das Balkenkreuz im Schildhaupt, dem oberen Wappenteil, auf die Zugehörigkeit von Linz zum Erzstift Köln hin. Das Wappen ist seit 1857 mit königlich-preußischer Genehmigung rechtsgültig. Richtig war 2.  
Quelle: Wikipedia, Artikel „Linz am Rhein“

*Faktencheck: OK*

- [ ] streichen

### Bad Hönningen, Karte 1

> Bad Hönningen ist eine Stadt mit rund 6.400 Einwohnern, 26 km nordwestlich von Koblenz.
> Im Wappen von Bad Hönningen stehen zwei rote Balken auf Silber. Woher stammen sie?
> 1. Sie erinnern an Bäche, die den Ort teilten.
> 2. Sie erinnern an eine Sage über Brüder.
> 3. Sie stammen aus dem Wappen eines Adelsgeschlechts.
> 4. Sie wurden erst im 20. Jahrhundert frei erfunden.

Du hattest [Option] getippt. Zwei Balken lassen an Grenzen oder Sagen denken. Tatsächlich sind sie das Stammwappen der Edelherren von der niederen Grafschaft Isenburg: Hönningen war seit dem 11. Jahrhundert isenburgische Vogtei und bis 1664 Hauptort der Herrschaft Isenburg-Arenfels. Schon das Schöffensiegel von 1346 zeigt ähnliche Merkmale. Richtig war 3.  
Quelle: Wikipedia, Artikel „Bad Hönningen“

*Faktencheck: OK*

- [ ] streichen

### Leutesdorf, Karte 1

> Leutesdorf ist eine Gemeinde mit rund 1.900 Einwohnern, 17 km nordwestlich von Koblenz.
> Im Wappen von Leutesdorf steht ein Heiliger mit einem schwarzen Rost und einem roten Buch. Warum steht er dort?
> 1. Er erinnert an eine Sage von einer Rettung.
> 2. Er ist der Schutzpatron der Pfarrkirche des Ortes.
> 3. Er war das Zeichen einer Leutesdorfer Zunft.
> 4. Er wurde erst im 20. Jahrhundert eingefügt.

Du hattest [Option] getippt. Ein Heiliger im Wappen lässt an eine Legende oder eine Zunft denken. Es ist der heilige Laurentius, der Schutzpatron der Pfarrkirche von Leutesdorf. Schon das Leutesdorfer Schöffensiegel von 1476 zeigt ihn; die Tradition der Figur reicht mindestens ins 15. Jahrhundert zurück. Richtig war 2.  
Quelle: Wikipedia, Artikel „Leutesdorf“

*Faktencheck: OK*

- [ ] streichen

### Feldkirchen, Karte 1

> Feldkirchen ist ein Stadtteil von Neuwied mit rund 5.200 Einwohnern, 16 km nordwestlich von Koblenz.
> Im früheren Wappen von Feldkirchen (1967 bis 1970) standen oben mehrere kleine Schilde. Wofür standen sie?
> 1. Sie standen für die Ortsteile der damaligen Gemeinde.
> 2. Sie erinnerten an eine Sage von Brüdern.
> 3. Sie standen für die Zünfte des Ortes.
> 4. Sie waren die Zeichen von Familien mit Landbesitz.

Du hattest [Option] getippt. Mehrere kleine Schilde lassen an Zünfte oder Familien denken. Tatsächlich standen die fünf Schildchen für die fünf Ortsteile der Gemeinde Feldkirchen: Fahr, Gönnersdorf, Hüllenberg, Rockenfeld und Wollendorf. Das Wappen galt von 1967 bis 1970; danach wurde Feldkirchen Stadtteil von Neuwied. Richtig war 1.  
Quelle: Stadt Neuwied, Stadtteilseite Feldkirchen

*Faktencheck: UNSICHER – Kernaussage nur durch die WAPPEN-QUELLE gedeckt; Ortsteile stimmen, Wappenbeginn 1967 (Karte) gegen 1966 (Suchtreffer) ungeklärt. Kein sachlicher Fehler gefunden.*

- [ ] streichen
