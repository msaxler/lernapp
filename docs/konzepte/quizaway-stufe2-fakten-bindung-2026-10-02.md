# QuizAway — Stufe 2, Berichtigungen am Fakt und Bindung Karte → Fakt: Bericht

**Datum:** 2026-10-02 · **Grundlage:** Bericht zum dritten Volllauf (`quizaway-stufe2-volllauf3-2026-10-02.md`, §5 „als nächste Schritte am PC"), Spielkonzept v0.2.7 §8 Nr. 8 · **Daten:** `data/gemeinde-achsen/iter1/` (`fakten/`, `faktencheck/berichtigungen.json`, `karten-fakt.json`, `eingabe-v0.7/`, `prompt-karten-v0.7.txt`)

Kein neuer Kartenlauf über die zehn Orte, keine neue Karte im Vorrat. Umgebaut ist, woran die Befunde des Faktenchecks hängen und woher der Vorrat weiß, dass zwei Karten denselben Fakt tragen.

---

## 1. Was gebaut ist

1. **Jeder Fakt hat eine feste Kennung.** `scripts/data-build/gemeinde_achsen_fakten.py` liest die Rohextraktion (`extraktion/`, bleibt unverändert) und schreibt `fakten/<ort>.txt`: je Fakt eine Zeile `ID: 09-horben/011`. Die Nummer ist die Stelle des Fakts in der Rohextraktion. 806 Fakten an den zehn Orten samt den drei Zweitquellen von Zähringen.
2. **Die Berichtigungen hängen am Fakt.** `faktencheck/berichtigungen.json` nennt je Befund die Kennung, die Eigenschaft und was geschieht: Wert ersetzen, Eigenschaft streichen, Hinweis anbringen, Fakt sperren. Das Skript bringt sie in `fakten/` an und bricht ab, wenn eine Berichtigung ihre Stelle nicht trifft. Im Fakt steht danach der richtige Wert und am Ende die Zeile `BERICHTIGT: …` oder `NICHT VERWENDEN: …`.
3. **Jede Karte ist an ihren Fakt gebunden.** `scripts/data-build/gemeinde_achsen_karten_fakt.py` sucht zu jeder der 186 Karten aus dem Feld GEWÄHLTER FAKT die Kennung und schreibt `karten-fakt.json`. Klassiker bekommen die Kennung der Grunddaten (`01-umkirch/G.einwohner`).
4. **„Derselbe Fakt" ist eine Abfrage.** `gemeinde_achsen_vorrat.py` liest die Bindung: Bei gleichem Schlüssel bleibt die Karte des jüngsten Laufs. `vorrat.json` führt nur noch, was aus anderem Grund raus ist.
5. **Mikes Streichungen sind Daten.** `kuratierung.json` bekommt den Abschnitt `vorrat`; `gemeinde_achsen_vorrat.py --kreuze` liest die Kreuze `[x] streichen` aus dem Vorrats-Blatt, legt sie dort ab und baut das Blatt neu.
6. **Eingabe und Prompt v0.7.** Die Eingabe nimmt die Fakten aus `fakten/`; der Block BERICHTIGUNGEN am Ende entfällt. Der Prompt verlangt je Karte die Zeile `FAKT-ID:`; damit bringt ein neuer Lauf seine Bindung mit, und die Suche wird für ihn nicht mehr gebraucht.

---

## 2. Zahlen

| | |
|---|---|
| Fakten mit Kennung | 806 |
| Berichtigungen an Fakten | 60 an 48 Fakten |
| Berichtigungen an Grunddaten | 9 (Einwohner Umkirch, Eingemeindung Günterstal, Kennzeichen in den sieben Orten des Landkreises) |
| Befunde des Faktenchecks ohne Fakt | 0 von 66 (vier betreffen nur den Steckbrief und sind im Eingabe-Skript behoben) |
| Karten gebunden | 186: 171 durch die Suche, 15 von Hand |
| Handzuordnungen „derselbe Fakt" vom Vormittag | 49 |
| davon durch die Abfrage gefunden | 48 |
| Vorrat vorher und nachher | 129 Karten, Liste gleich |

---

## 3. Befunde

**B1. Die Abfrage trifft die Handarbeit.** 48 der 49 Zuordnungen findet sie. Die 49. war kein gleicher Fakt: Günterstals Politik-Karte des zweiten Laufs fragte nach der zweitstärksten Partei in ganz Freiburg, die des dritten nach der Wahlbeteiligung im Stadtbezirk. Die alte Karte ist jetzt als überholt aus dem Vorrat genommen; das Ergebnis ist dasselbe, der Grund stimmt.

**B2. Drei Fakten tragen mehr als eine Sache.** Das Kloster Günterstal (erste Erwähnung, Flucht vor den Schweden, Aufhebung), der Carlsbau im Glottertal (was er zur Drehzeit war, Leerstand) und die Kirche St. Agatha in Horben (Bau, Herkunft des Portals). Ohne Eingriff hätte die Abfrage dort sieben Karten zu dreien zusammengelegt. Diese Karten tragen einen eigenen Schlüssel aus Kennung und Eigenschaft, mit Grund, in `karten-fakt-von-hand.json`.

**B3. Ein Ding steht zweimal da.** Staufens Partnerstadt Bonneville steht in den Grunddaten und in der Extraktion. `fakten-gleich.json` führt solche Paare zusammen; bisher ist es das eine.

**B4. Die Suche ist bei sieben Karten unsicher und bei einer falsch.** Unsicher, wo der Fakt keine Bezeichnung hat (Kirchzarten: Ortsgeschichte, Bürgerentscheid, keltische Befestigung) oder zwei Fakten fast gleich gut passen. Falsch bei Denzlingens Lügen-Karte des ersten Laufs, wo sie die Konfession einer wahren Aussage griff statt der Herrschaft, an der die Lüge hängt. Alle acht sind von Hand geprüft und eingetragen. Ab Prompt v0.7 nennt der Kartenlauf die Kennung selbst.

**B5. Eine Berichtigung gehört oft nicht zu dem Fakt, den die Karte gewählt hat.** Das abgeschossene Flugzeug war bei Umkirch nur eine wahre Aussage neben der Lüge über das Schloss; der Fehler mit dem Kirchenportal fiel an einer Karte über das Rathaus auf. Die 60 Berichtigungen sind deshalb einzeln dem Fakt zugeordnet, an dem der Fehler steht, nicht dem der Karte.

**B6. Drei Fehler der Extraktion sind an der Wurzel behoben.** Horben: 1805/06 wurde die Spitalkirche aufgehoben, wann das Portal kam, ist nicht belegt. Gundelfingen: 1661 ist das Jahr des ersten Schulmeisters, kein Gründungsjahr. Dazu ein dritter aus dem dritten Lauf: Die 303 Mark Silber gehören zum Verkauf von 1327, nicht zum Viertelkauf der Burg Zähringen.

**B7. Das Kennzeichen ist für den ganzen Landkreis berichtigt.** Der Faktencheck fand den Befund an Horben; er gilt für jeden Ort im Landkreis Breisgau-Hochschwarzwald. Der Hinweis steht jetzt in allen sieben.

**B8. Probe an Horben mit Prompt v0.7: Die Berichtigungen greifen, und die Kennung kommt mit.** Ein Kartenlauf, der nur `prompt-karten-v0.7.txt` und `eingabe-v0.7/09-horben.txt` gelesen hat, schrieb neun Karten (sieben Pflicht, zwei Zusatz; `karten-v0.7/09-horben.md`). Die Regelprüfung meldet keinen Fehler; alle neun nennen eine gültige `FAKT-ID`. Was an Horben in drei Läufen dreimal abgefangen werden musste, steht jetzt von selbst richtig da:
- Kirchenportal: „Wann es nach Horben kam, ist nicht belegt"; kein 1805/06, „aufgehoben" ist keine Option mehr, die Glocke ist von 1731, das strittige Baujahr bleibt ungenannt.
- Kennzeichen: Der Plan sah die Kennzeichen-Karte vor; der Lauf nahm wegen des Vermerks die Ersatz-Eigenschaft (Luftlinie nach Stuttgart).
- Liegen gelassen, mit Verweis auf den Vermerk: der Eingemeindungsversuch nach dem Bau der Talstation und der Ritt Napoleons III.
- Hotel Luisenhöhe: Abriss 2019.

Über die Kennung zeigt sich sofort, was neu ist: Sechs der neun Karten liegen auf einem Fakt, der im Vorrat schon eine Karte trägt, drei auf einem neuen (Luftlinie nach Stuttgart, Eduardshöhe, Marina Zwetajewa in Horben). **Die neun Karten sind nicht im Vorrat:** Sie haben keinen Faktencheck, und die Probe galt der Mechanik.

**B9. Ein Loch, das die Probe gezeigt hat und das gestopft ist.** Nennt ein Kartenlauf die Kennung eines Fakts, der mehr als eine Sache trägt (B2), muss die Eigenschaft mitzählen; sonst läge die neue Portal-Karte neben der alten statt an ihrer Stelle. Das Bindungs-Skript behandelt solche Fakten jetzt wie den Ort selbst.

---

## 4. Aufwand

Kein Volllauf, kein Faktencheck; ein Probe-Lauf an einem Ort (B8; rund sechs Minuten, rund 135.000 Tokens). Von Hand: 60 Berichtigungen zuordnen (einmalig, weil sie für drei Läufe nachzuholen waren), 15 Bindungen prüfen.

### Wo ein Mensch mehr bringt als die Automatik

- **Nichts an der Bindung.** Sie ist Buchhaltung; ein Fehler darin zeigt sich im Vorrats-Blatt als Karte, die fehlt oder doppelt ist.
- **Bei B2:** Ob zwei Karten zum selben Bauwerk „dieselbe Frage" sind, ist Geschmack. Die Zeilen „Ersetzt" am Ende jedes Orts im Vorrats-Blatt zeigen, was zusammengelegt ist; wer dort eine Karte vermisst, sagt es.
- **Künftig:** Ein Befund des Faktenchecks wird beim Auswerten gleich an den Fakt gehängt. Das Skript meldet jeden Befund, der noch an keinem Fakt hängt.

---

## 5. Was Mike entscheidet

1. **Vorrats-Blatt** (`quizaway-stufe2-vorrat-2026-10-02.md`): streichen, was nicht gefällt. Ein Kreuz im Blatt genügt (`[x] streichen`), oder eine Liste in zwei Zeilen.
2. **Die Grenze je Ort:** vorläufig zwanzig. Vorschlag: so lassen, bis ein Ort sie erreicht.
3. **Gestrichene Karte und älterer Fakt:** Streichst du eine Karte des dritten Laufs, kommt die ältere Karte zum selben Fakt nicht von selbst zurück. Vorschlag: so lassen; wer die ältere lieber hat, sagt es beim Streichen.

---

## 6. Was ab jetzt da ist

Die Kette für einen neuen Raum: Grunddaten und Quellen holen → Extraktion → `gemeinde_achsen_fakten.py` → `gemeinde_achsen_karten_eingabe.py` → Kartenlauf (Prompt v0.7) → Regelprüfung → Faktencheck → Korrekturen an die Karten und Berichtigungen an die Fakten → `gemeinde_achsen_karten_fakt.py` → `gemeinde_achsen_vorrat.py`. Ein zweiter Lauf am selben Ort liest die berichtigten Fakten. Welche Fakten schon eine Karte tragen, sagt ihm die Eingabe noch nicht; die Bindung gibt die Liste her. Ob ein neuer Lauf die belegten Fakten meiden soll (mehr Breite) oder sie wieder nehmen darf (die jüngere Karte ersetzt die ältere), ist nicht entschieden und kostet bis zum nächsten Lauf am selben Ort nichts.

*Ende Bericht.*
