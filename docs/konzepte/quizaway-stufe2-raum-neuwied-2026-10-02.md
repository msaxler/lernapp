# QuizAway — Stufe 2, zweiter Raum (Neuwied): Bericht

**Datum:** 2026-10-02 · **Auftrag:** Mike, 2026-10-02 („zweiter Raum außerhalb Freiburg ist Neuwied"; Ortsliste „Rhein und Wied" gewählt; „so weit als möglich durchziehen") · **Grundlage:** Spielkonzept v0.2.7, Karten-Prompt v0.7, Bericht `quizaway-stufe2-fakten-bindung-2026-10-02.md` · **Daten:** `data/gemeinde-achsen/neuwied/`

**Ergebnis in einem Satz:** Die Kette trägt in einem zweiten Raum ohne Änderung an Prompts und Regeln: zehn Orte, 96 Karten, keine Regelverletzung, im Faktencheck 70 bestätigt, 17 korrigiert, 9 unsicher, keine gesperrt; nachzustellen waren die Skripte, die Freiburg fest verdrahtet hatten, und zwei Lücken der Wahlstatistik in Rheinland-Pfalz.

---

## 1. Was gelaufen ist

| Glied | Was | Ergebnis |
|---|---|---|
| Ortsliste | Bendorf, Engers, Heimbach-Weis, Altwied, Rengsdorf, Dierdorf, Waldbreitbach, Linz am Rhein, Bad Hönningen, Leutesdorf (Reihenfolge der Fahrt); Spender Kirchberg, Gerolstein, Bad Camberg | drei Stadtteile von Neuwied, vier Städte, drei Gemeinden; höchstens 27 km auseinander; Spender 51 bis 79 km entfernt |
| Quellen | Wikipedia-Artikel, Wikidata, Infobox, Wahlstatistik | drei Artikel unter 1.000 Wörtern, dazu fünf Zweitquellen |
| Extraktion | Prompt `prompt-stufe1-v0.5.1.txt` unverändert, kleines Modell, 18 Texte | 811 Fakten an den Zielorten (Freiburg: 806), 280 an den Spendern |
| Kartenlauf | Prompt `prompt-karten-v0.7.txt` unverändert, je Ort ein Lauf | 96 Karten (siebenmal zehn, zweimal neun, Rengsdorf acht); 26 Zusatzkarten |
| Regelprüfung | `gemeinde_achsen_karten_pruefen_v05.py --lauf v0.7` | 0 Fehler; jede Karte mit gültiger `FAKT-ID` |
| Faktencheck | Auftrag `neuwied/faktencheck/auftrag-v0.7.txt` (Pfade und Quellenhinweise angepasst) | 70 OK, 16 korrigieren, 10 unsicher |
| Korrekturen | `neuwied/faktencheck/korrekturen.json` | 70 bestätigt, 17 korrigiert, 9 unsicher, 0 gesperrt |
| Berichtigungen | `neuwied/faktencheck/berichtigungen.json` | 37 an 32 Fakten, 2 an Grunddaten; kein Befund ohne Fakt |
| Bindung, Vorrat | `karten-fakt.json`, `vorrat-liste.json` | 96 Karten im Vorrat, je Ort 8 bis 10; Blatt `quizaway-stufe2-vorrat-neuwied-2026-10-02.md` |

**Vergleich mit dem dritten Freiburger Lauf (86 Karten):** bestätigt 73 % (Freiburg 74 %), korrigiert 18 % (21 %), unsicher 9 % (3 %), gesperrt 0 (1 Karte).

---

## 2. Befunde

**N1. Prompts und Regeln brauchten keine Änderung.** Extraktions-Prompt, Karten-Prompt und Spielregeln liefen, wie sie für Freiburg standen. Die Kartenläufe hörten wieder von selbst auf, wo die Fakten ausgingen (Rengsdorf acht Karten, Altwied und Waldbreitbach neun).

**N2. Nachgestellt sind die Skripte, nicht die Regeln.** Freiburg war an vielen Stellen fest verdrahtet: Ordner, Ortsliste, Spender, „Stadtkreis Freiburg", Baden-Württemberg als Vorgabe, die Wikidata-Kennung der Stadt, das Wahlportal. Die Skripte lesen jetzt den Raum aus `GA_RAUM` und seine Einstellungen aus `<raum>/orte.json`. Nullprobe: Mit den umgebauten Skripten kommt für Freiburg derselbe Stand heraus (Grunddaten, Eingaben, geprüfte Karten, Vorrat 129, alle Dateien unverändert).

**N3. In Rheinland-Pfalz zählt oft die Verbandsgemeinde die Briefwahl aus.** Für Dierdorf und Linz am Rhein enthält die Gemeinde-Summe der Wahlstatistik nur die Urnenstimmen; ein vollständiges Ergebnis gibt es nur für die Verbandsgemeinde. Das Skript hätte das ohne Prüfung als Gemeinde-Ergebnis ausgegeben. Jetzt trägt die Zeile den Vermerk „GILT FÜR DIE VERBANDSGEMEINDE …", und beide Karten fragen ausdrücklich nach der Verbandsgemeinde. In Freiburg gab es den Fall nicht (alle acht Gemeinden zählen selbst aus; nachgeprüft).

**N4. Die Neuwieder Stadtteile haben ein eigenes Wahlergebnis, aber kein Open-Data-Angebot.** Die Bundesstatistik führt die Stimmbezirke nur mit Nummern; die Stimmbezirkseinteilung der Stadt nennt zu jeder Nummer den Stadtteil und den Briefwahlbezirk. Daraus sind Engers, Heimbach-Weis und Altwied summiert. In Altwied zählt der Briefwahlbezirk 244 Stimmen bei 236 ausgegebenen Wahlscheinen: Das Ergebnis ist nur ungefähr, und SPD und AfD liegen zwei Stimmen auseinander. Der Plan fragt dort deshalb nach dem Anteil der stärksten Partei als Spanne, und die Karte sagt „rund 34 Prozent" und warum.

**N5. Die Einwohnerzahlen der Stadtteile stehen nicht in Wikidata, aber in der Infobox der Stadtteil-Artikel** (Quelle dort: Stadt Neuwied, Stand 6. Juli 2026): Engers 5.202, Heimbach-Weis 7.337, Altwied 674. Fläche und damit Dichte fehlen den Stadtteilen; die Eigenschaft fehlt dann, geraten wird nichts.

**N6. Die Ersterwähnung fehlt in acht von zehn Grunddaten** (Freiburg: in fünf). Wikidata führt sie selten, und das Skript findet sie in der Extraktion nur, wenn sie im Ortsblock unter einem erwarteten Namen steht. Die Karten haben sie trotzdem, wo der Artikel sie nennt, als Geschichte. Als Klassiker „Jahr der ersten Erwähnung" kam sie nur in Waldbreitbach vor.

**N7. Dünne Artikel tragen mit zweiter Quelle.** Heimbach-Weis (685 Wörter, 15 Fakten, dazu 8 aus dem Kirchenartikel) bekam zehn Karten, sieben bestätigt, drei mit kleiner Korrektur. In Altwied hängen fünf der neun Karten am Artikel über die Burg. Neun der 96 Karten stammen aus einer Zweitquelle.

**N8. Was der Faktencheck fand.** Drei Fehler der Extraktion: An der Brücke von Engers wurden aus „hunderten Menschen" „ca. 100"; Engers ging nicht in der Sühne von 1371 verloren, sondern wurde dem Grafen zuvor abgenommen; das Deutschordenshaus in Waldbreitbach wurde 1809 von Nassau eingezogen und nicht von Fürst Hermann zu Wied gekauft, der erst 1814 geboren wurde. Verlorene Vorbehalte: der Steinbruch in der Burg Altwied („soll"), die Namensdeutung von Engers („scheint"), die Haft des Schwarzen Peter im Linzer Pulverturm (eine Legende; hier hatte schon der Wikipedia-Artikel den Vorbehalt verloren). Veraltet: die drei Leutesdorfer Weinlagen, seit 2006 eine. Strittige Jahreszahlen an mehreren Karten (Orgel von Heimbach-Weis, Schloss Arenfels, die Linzer Stadttore). **Keine Karte hatte eine falsche Option, die stimmt** (Freiburg, erster Faktencheck: sechs).

**N9. Mehr unsichere Karten als in Freiburg.** Neun Auflösungen stehen nur in Wikipedia, vier davon in Dierdorf (Kupferhaus, Tilly als Taufpate, Schüleraustausch, Wirtschaftsordnung von 1598). Für kleine Orte gibt es oft keine zweite Quelle im Netz. Die Karten bleiben spielbar und tragen den Vermerk; wo es ging, steht jetzt „soll" oder „überliefert".

**N10. Stichprobe der Befunde.** Fünf Befunde selbst im Netz nachgeprüft (Leutesdorfer Lagen 2006, Neutor nach 1391, Hoinga im März 2021 veröffentlicht, Sühne von 1371, Legende vom Schwarzen Peter): fünf von fünf stimmen.

**N11. Die Spender spielen keine Rolle.** Eine von 96 Karten nutzt einen gespiegelten Fakt. Die drei Spender waren ein Sechstel des Extraktionsaufwands.

**N12. Die Eingabe eines Laufs muss stehen bleiben.** Nach dem Eintragen der Berichtigungen schrieb das Eingabe-Skript die Eingaben neu, mit berichtigten Fakten; damit wäre nicht mehr nachzulesen gewesen, was die Kartenläufe gesehen haben. Die Eingaben sind in der gelesenen Fassung wiederhergestellt. Das Skript braucht für einen weiteren Lauf am selben Ort einen eigenen Ordner.

**N13. Die Orts-Anschlüsse stimmen.** Alle 18 Anschlüsse hat der Faktencheck bestätigt; sie sind Vergleiche aus den Grunddaten (Einwohner, Höhe, Wahl, nächste Großstadt).

---

## 3. Aufwand

Extraktion 18 Texte, rund 1,1 Millionen Tokens mit dem kleinen Modell. Kartenläufe zehn, je fünf bis sieben Minuten, zusammen rund 1,5 Millionen Tokens. Faktencheck zehn, je drei bis sechs Minuten, zusammen rund 1,3 Millionen Tokens. Höchstens zwei Läufe zugleich; von der Ortsliste bis zum Vorrats-Blatt rund anderthalb Stunden. Von Hand: 26 Korrekturen an Karten, 39 Berichtigungen an Fakten und Grunddaten, die Skripte.

### Wo ein Mensch mehr bringt als die Automatik

- **Die neun unsicheren Karten.** Wer eine Ortschronik zur Hand hat oder im Ort nachfragt, klärt das Kupferhaus oder die Wirtschaftsordnung von Dierdorf in Minuten. Du kennst die Gegend: Ein Blick auf diese neun im Vorrats-Blatt lohnt mehr als jede weitere Suche im Netz.
- **Das Hundertwasser-Haus in Bendorf.** Ob es das Haus gibt, sieht man vor Ort.
- **Die Ortsliste.** Welche Orte eine Fahrt wert sind, weiß, wer dort fährt.

---

## 4. Was Mike entschieden hat (2026-10-02 abends)

| Frage | Entscheid | Umsetzung |
|---|---|---|
| Vorrats-Blatt Neuwied | „die unsicheren Karten Dierdorf weglassen" | die vier Dierdorfer Karten, deren Auflösung nur in Wikipedia steht (Kupferhaus, Tilly als Taufpate, Fountain Hills, Wirtschaftsordnung von 1598), als Streichung in `neuwied/kuratierung.json`; Dierdorf hat sechs Karten im Vorrat |
| Wahlergebnis der Verbandsgemeinde statt der Stadt | „so lassen" | Dierdorf und Linz fragen nach der Verbandsgemeinde und sagen das; als Regel für Rheinland-Pfalz vorgemerkt für Spielkonzept v0.2.8 |
| Feldkirchen | „als Ort nachziehen", dazu Mike: Feldkirchen besteht aus Wollendorf, Fahr, Hüllenberg, Gönnersdorf und Rockenfeld; Rockenfeld ist „in jedem Fall eine Besonderheit" | elfter Ort der Fahrt (§5) |
| Kartensatz für den Tisch aus Neuwied | „Kartensatz auch für Neuwied" | `quizaway-feldtest-stufe2-kartensatz-neuwied-2026-10-02.md` (§6) |

---

## 5. Nachtrag: Feldkirchen als elfter Ort

**N14. Der Auszug der Wikipedia-Schnittstelle lässt Tabellen weg.** Alle Quelltexte beider Räume kommen über die Schnittstelle TextExtracts; sie liefert Fließtext, aber keine Tabellen. Im Artikel Feldkirchen stehen die Abschnitte zu den fünf Ortsteilen in Tabellen (Wappen links, Text rechts); im Quelltext standen nur die Überschriften. Gemessen an allen 21 Zielorten: Meist fehlen Wahltabellen, Buslinien und Navigationsleisten. Inhaltlich verloren sind die Wappenbeschreibungen von sieben Orten (Umkirch, Bendorf, Engers, Dierdorf, Linz, Bad Hönningen, Leutesdorf) und in Feldkirchen die ganze Ortsteilgeschichte. Für Feldkirchen ist der Text der Tabellen als eigene Quelle nachgeholt (`quellen/11-feldkirchen+3.txt`). Die Wappen wären eine eigene Fragenfamilie („Was zeigt das Wappen, und warum?"); das Quellen-Skript holt sie noch nicht.

**N15. Rockenfeld hat einen eigenen Artikel.** Er kam als vierte Quelle dazu (`quellen/11-feldkirchen+4.txt`). Belegt sind dort und in einer zweiten Quelle: erstmals 1280 als „Rukenvelt" erwähnt, 1846 elf Familien, nach dem Krieg noch rund 50 Menschen, 1965 Auflösung wegen Abwanderung, 1969 brannte die Feuerwehr die verlassenen Häuser ab, 1995 wurde das letzte Haus abgerissen, seit den 1990er Jahren die Kirmes am 1. Mai (Junggesellenverein Rheinbrohl; Rhein-Zeitung, NR-Kurier, Blick aktuell). Von Rockenfeld soll sich der Name Rockefeller ableiten (Wikipedia; Rhein-Zeitung 2013).

**Zu Mikes Hinweisen:** Nur in Suchauszügen, nicht gesichert: 1966 noch 25 Einwohner; der letzte Bewohner, ein Gastwirt mit lebenslangem Wohnrecht, starb 1993 (NR-Kurier 2014 nennt das Todesjahr); eine Gaststätte „Zur Waldesruh". Das trifft Mikes Erinnerung, dass jahrelang nur ein Haus bewohnt war. **Nicht gefunden:** „20 Einwohner und drei Gaststätten" (Mike: „sagt die Legende") und das Seifenkistenrennen; die Berichte über die Kirmes (Rhein-Zeitung vom 2. Mai 2026, Blick aktuell) nennen kein Rennen. Beides trägt deshalb keine Karte, solange keine Quelle es belegt.

**N16. Der Abfragedienst von Wikidata antwortete dreimal mit 504.** Das Grunddaten-Skript wiederholt jetzt auch bei Serverfehlern (502 bis 504); beim vierten Lauf ging es durch. An den zehn übrigen Orten hat sich in den Grunddaten nichts geändert. Für Feldkirchen führt der Altbestand (`geo.sqlite`) die Kennzeichen MÜ und M, ein Zuordnungsfehler dort; das Kennzeichen eines Stadtteils trägt ohnehin keine Karte.

**N17. Feldkirchen trägt zehn Karten, beide Wünsche Mikes sind darunter.** Quellen: Ortsartikel (911 Wörter), Artikel zur Feldkirche, zum Heimatverein, die Ortsteiltexte und der Artikel Rockenfeld; zusammen 133 Fakten. Karte 1 fragt, welches der fünf Dörfer heute zu Feldkirchen gehört (Hüllenberg; die falschen Optionen sind Nachbarorte). Karte 7 gilt Rockenfeld: Was geschah 1969 mit den leeren Häusern? (Die Feuerwehr brannte sie ab; die Rückseite nennt die Herkunft des Namens Rockefeller, Rukenvelt 1280, elf Familien 1846 und den Abriss des letzten Hauses 1995.) Der Plan bekam dafür eine Zeile „Wunsch"; der Kartenlauf hat sie wie den übrigen Plan befolgt. Der Lauf lief mit Claude Opus statt Fable (Modellwechsel in der Sitzung); Format und Regeln hielten, die Regelprüfung meldet keinen Fehler.

**N18. Faktencheck Feldkirchen:** 8 bestätigt, 2 korrigiert. Der Liedtitel heißt „Mosellied". Die Entdeckung des eiszeitlichen Fundplatzes Gönnersdorf beim Aushub für ein Einfamilienhaus fand der Faktencheck nur in Wikipedia (unsicher); **Mike hat die Entdeckung 1968 selbst miterlebt** und bestätigt sie als Augenzeuge. Auf seinen Hinweis steht jetzt auch Monrepos auf der Karte: Die Funde aus Gönnersdorf gaben mit anderen Fundplätzen im Neuwieder Becken den Anstoß zum Forschungsbereich Altsteinzeit (1984) und zum Museum für die Archäologie des Eiszeitalters (1988) im Schloss Monrepos (Wikipedia, Artikel zum Fundplatz und zum Forschungszentrum; das Haus selbst nennt nur „seit über 30 Jahren"). Die Grabungsfläche ist gerundet. Die Rockenfeld-Karte ist durch zwei Quellen bestätigt (NR-Kurier, Treffpunkt Feldkirchen); der NR-Kurier bestätigt auch die Herkunft des Namens Rockefeller. Ein Orts-Anschluss war schief: Die evangelischen Leutesdorfer gehören nicht nur „einst", sondern bis heute zur Kirchengemeinde der Feldkirche. Das Korrektur-Skript kann jetzt auch den Anschluss berichtigen (Eintrag mit `"karte": "anschluss"`).

**Raum Neuwied jetzt:** elf Orte, 106 Karten, Faktencheck 78 bestätigt, 19 korrigiert, 9 unsicher, keine gesperrt; nach Mikes Streichung 102 Karten im Vorrat, davon 5 unsicher.

---

## 6. Kartensatz für den Tisch

`quizaway-feldtest-stufe2-kartensatz-neuwied-2026-10-02.md`, gebaut mit demselben Skript wie der Freiburger Satz (`gemeinde_achsen_kartensatz_stufe2.py`, jetzt raumfähig; der Freiburger Satz kommt unverändert heraus). Elf Orte in der Reihenfolge der Fahrt, Familien A C A B Leiter A B A B C A, gemischt wie in Freiburg. Nur Karten, die der Faktencheck bestätigt oder korrigiert hat, keine unsichere: Großbrand von Bendorf, Höhe von Engers, „Bauernfreistaat" Heimbach, Lügen-Karte zur Burg Altwied, Leiter zur Einwohnerdichte von Rengsdorf, Steine des Dierdorfer Schlosses, Lügen-Karte Waldbreitbach, Meerberg bei Linz, Lügen-Karte Bad Hönningen, Einwohnerdichte von Leutesdorf, Rockenfeld. Die Reihe steht als Daten in `neuwied/kuratierung.json`. Testperson: jemand, der den Raum Neuwied nicht gut kennt; wer den Freiburger Satz gespielt hat, darf hier spielen, die Orte sind andere.

---

## 7. Was Mike entscheidet

1. **Vorrats-Blatt Neuwied:** weiter streichen, was nicht gefällt; neu sind die Karten von Feldkirchen.
2. **Rockenfeld:** Wenn du für das Seifenkistenrennen oder die drei Gaststätten eine Quelle weißt (Vereinsseite, Zeitungsbericht, Ortschronik), wird daraus eine Karte.

Ohne Entscheid, als nächste Schritte am PC: Tabellentext in das Quellen-Skript (N14), danach Wappen als Fragenfamilie prüfen; Ersterwähnung als Grunddatum breiter holen (N6); dem Eingabe-Skript einen Ordner je Lauf geben (N12); die Nachträge des 2. Oktober als E12 ff. ins Achsen-Entscheidungsdokument; die Befunde N3 und N4 samt Mikes Entscheid ins Spielkonzept v0.2.8 (§8 Nr. 7, Politik-Karte).

---

## 8. Was ab jetzt da ist

Zwei Räume, 21 Orte, 231 Karten im Vorrat (Freiburg 129, Neuwied 102), zwei Kartensätze für den Tisch. Die Kette läuft für einen neuen Raum mit einer Ortsliste in `orte.json` und dem Aufruf `GA_RAUM=<raum>`; was dabei an Wahlstatistik und Stadtteilen anders ist als in Baden-Württemberg, meldet das Grunddaten-Skript selbst.

*Ende Bericht.*
