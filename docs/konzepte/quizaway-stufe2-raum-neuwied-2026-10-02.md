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

## 4. Was Mike entscheidet

1. **Vorrats-Blatt Neuwied** (`quizaway-stufe2-vorrat-neuwied-2026-10-02.md`): streichen, was nicht gefällt.
2. **Wahlergebnis der Verbandsgemeinde** statt der Stadt (Dierdorf, Linz): so lassen, oder die Politik-Karte dort weglassen? Vorschlag: so lassen; die Karte sagt, wofür sie gilt.
3. **Feldkirchen als elfter Ort?** Deine Idee: die früheren Orte, die heute Feldkirchen bilden, als Frage. Feldkirchen ist nicht in der Fahrt; der Artikel hat 911 Wörter. Vorschlag: Feldkirchen als elften Ort nachziehen (ein Lauf je Glied). Die Frage „welcher dieser Orte gehört zu …" passt als Familie A auch zu Heimbach-Weis (aus Heimbach und Weis 1960 zusammengelegt).
4. **Kartensatz für den Tisch aus Neuwied?** Für eine Testperson, die den Raum Freiburg kennt, wäre Neuwied der unbekannte Raum, und umgekehrt.

Ohne Entscheid, als nächste Schritte am PC: Ersterwähnung als Grunddatum breiter holen (N6); dem Eingabe-Skript einen Ordner je Lauf geben (N12); die Nachträge des 2. Oktober als E12 ff. ins Achsen-Entscheidungsdokument; die Befunde N3 und N4 ins Spielkonzept (§8 Nr. 7, Politik-Karte), wenn Mike Nr. 2 entschieden hat.

---

## 5. Was ab jetzt da ist

Zwei Räume, 20 Orte, 225 geprüfte Karten (Freiburg 129, Neuwied 96). Die Kette läuft für einen neuen Raum mit einer Ortsliste in `orte.json` und dem Aufruf `GA_RAUM=<raum>`; was dabei an Wahlstatistik und Stadtteilen anders ist als in Baden-Württemberg, meldet das Grunddaten-Skript selbst.

*Ende Bericht.*
