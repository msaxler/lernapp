# Gemeinde-Achsen — Entscheidungen 2026-10-01 (E4–E11)

**Status:** Ergänzt das Basiskonzept v0.5 und die Iteration-1-Entscheidungen E1–E3 vom 2026-06-28. Bei Abweichung gilt diese Notiz (jünger). **Herkunft:** E4 ist Mikes Aussage im Spielkonzept Reise-Modus §8a; E5–E8 sind seine Entscheide zur PC-Prüfung des Spielkonzepts („alle gemäß den Vorschlägen", Prüfbericht B1, B2, B3, B6, B7).

**Leitlinie unverändert:** Unterhaltung für die lange Fahrt, kein Prüfungswissen. Fun vor Korrektheit. Die eine Ausnahme steht in E5.

---

## E4 — Gemeinde-Webseiten werden Quelle; Ziel ist die Ortsschild-Ebene

- v0.5 schloss Gemeinde-Webseiten aus (§11 Nr. 5 „nicht in v0.x", §14 „kein Crawler"). Für kleine Orte sind sie jetzt die vorgesehene Quelle für Geschichten und Gründe (Schicht 1): Eine Zeile dort ist zugleich Frage, Auflösung und Steckbrief-Satz.
- Zielgröße ist die Ortsschild-Ebene (rund 80.000 Orte), nicht mehr nur die rund 10.700 Gemeinden. Die Datenbank wächst schrittweise; das Spiel überspringt Orte ohne Material.
- Unverändert: kein Crawler in Iteration 1. Webseiten kommen dort von Hand dazu, wo der Wikipedia-Artikel zu wenig hergibt.
- Offen und hier nicht entschieden: ob bei 80.000 Orten die flache Ortsteil-Modellierung aus v0.5 §4.6 trägt.

## E5 — Negativnachweis für gespiegelte Distraktoren

- Ein Fakt eines anderen Orts darf am Zielort nur dann als falsche Option dienen, wenn die Eigenschaft dort **mit einem anderen Wert belegt** ist (einwertig: Landkreis, Herrschaft, Bahnstrecke, Namensherkunft) **oder aus einer vollständigen Quelle stammt und dort fehlt** (Schicht 0).
- „Am Zielort nicht gesetzt" genügt nicht. Die Datenbank ist lückenhaft; ein wahrer Distraktor bestraft die richtige Antwort. Das ist der Fall, den „Fun vor Korrektheit" nicht deckt.
- Folge für den Katalog: Jede Eigenschaft braucht die Angabe, ob sie einwertig ist und ob ihre Quelle vollständig ist. v0.5 §4.1 kennt `multiplicity` auf dem Entitätstyp; für Eigenschaften kommt das dazu.

## E6 — Spender und Abstand

- Für Theorie-Distraktoren gilt der Abstand 50–100 km; die erste Stufe des Distraktor-Pools aus v0.5 §10 (30 km) ist dafür ausgesetzt. Für Zahlen-Distraktoren (Werte gleicher Eigenschaft) bleibt §10.
- Der Spender darf kein Ort der laufenden Fahrt sein. Das prüft die Edition zur Laufzeit, nicht die Datenbank.

## E7 — Stadtteile großer Städte

Zähringen und Günterstal (Freiburg) werden als Entität `ortsteil` der Gemeinde geführt (v0.5 §4.6). Quelltext ist der Stadtteil-Artikel. Ihre Fakten tragen `ortsteil_bezug`; gespielt werden sie wie ein eigener Ort.

## E8 — Bekanntheit ist eine Eigenschaft des Fakts

- Bekanntheit schließt einen Fakt als Frage aus, nicht als Reveal oder Steckbrief-Satz.
- Gemessen wird die Bekanntheit der Sache, auf die der Fakt zeigt (Sprachversionen und Abrufe ihres Artikels), nicht die des Orts. Verfahren wie beim Fame-Index in MixMi: Perzentil-Normierung, Schwelle als Parameter.
- Was v0.5 §8.4 als Singleton-Gold führt (Drehort, prominente Persönlichkeit), ist damit zunächst Reveal-Material.
- Die Schwelle kommt aus dem Feldtest (Kürzel W je Karte über mehrere Personen), nicht aus einer Formel vorab.

---

## E9 — Bekanntheitsfilter stark abschwächen (Mike, 2026-10-01, nach dem Stufe-2-Volllauf; ersetzt E8 in seiner Strenge)

„Der Bekanntheitsfilter muss stark abgeschwächt werden: man freut sich, wenn man auch mal Glück mit einer Frage hat. Ggf. kann die Frage ja auch leicht modifiziert und ergänzt werden, so dass die Frage nicht mehr ganz so leicht ist (Anzahl der Einwohner, Name der Klinik, die es wirklich gibt – irgendwie so etwas)."

- Bekannte Fakten dürfen die Frage tragen. Der Volllauf hatte Schwarzwaldklinik, Fausts Tod und die Hebungsrisse aus allen Fragen gehalten; die Staufen-Karten wurden dadurch blass.
- Statt zu sperren: die Frage auf ein weniger bekanntes Detail desselben Fakts richten oder mit einer zweiten Angabe verbinden.
- Folge: Spielkonzept §8 Nr. 6 und Karten-Prompt Regel 7 sind neu gefasst (Spielkonzept v0.2.6, Karten-Prompt v0.5). Das Kürzel W im Feldtest bleibt als Messung, ist aber kein Ausschlussgrund.

## E10 — Ziel sieben Fragen je Ort (Mike, 2026-10-01)

„Wenn ein Ort mit einer Frage praktisch erschöpft ist, dann ist das zu wenig, dann müssen zumindest die Klassiker Größe, Kennzeichen e. a. hinzugenommen werden, stärkste Partei – auf jeden Fall gerne auch was Politisches. Ziel sind 7 Fragen je Ort, auch wenn er klein ist. Für größere Orte darf es auch mehr sein."

- Je Ort ein Vorrat von mindestens sieben Karten, gemischt aus Geschichten-Fakten (Schicht 1) und Klassikern aus den Grunddaten (Schicht 0): Einwohner, Kfz-Kennzeichen, Landkreis, Höhe, Fläche, Ersterwähnung, dazu Politik (stärkste Partei, Wahl, Bürgermeister; v0.5 §12).
- Quellen dafür: Wikidata und amtliche Wahlergebnisse. `data/staedte.json` taugt für Kennzeichen nicht.
- **Geklärt (Mike, 2026-10-01 abends):** „Sieben Fragen" meint den Vorrat je Ort, nicht mehrere Fragen hintereinander. „Eine Frage pro Ort" (Spielkonzept §5) bleibt. Aufgenommen in Spielkonzept v0.2.6 §8 Nr. 7.

- **Nachtrag 2026-10-02 (Mike):** Zahlen-Karten nehmen ihre Zahl in der Regel aus den Grunddaten. Eine Zahl aus dem Artikel ist erlaubt, wenn der Steckbrief einen Anhalt zum Schätzen gibt (Übernachtungen in St. Peter neben der Einwohnerzahl: „für so ein kleines Dorf eine schöne überraschende Zahl"). Im Karten-Prompt v0.5 steht noch die strenge Fassung; v0.6 zieht nach.

## E11 — Grunddaten: als Option alles, was die Originalvariante schon als Vorrat führt (Mike, 2026-10-01)

Auf den Vorschlag „Grunddaten erweitern: Kennzeichen, Fläche, Ersterwähnung, Wahl und stärkste Partei": „und eben alles das, als Option, was wir in der Originalvariante als Vorrat in Datenbanken schon angelegt haben."

- **Katalog der Grunddaten** (Schicht 0), jede Eigenschaft optional. Aus den Kategorien der Originalvariante (`data/fragen.json`: geo, ew, kfz, hoehe, dist, gesch, bahn): Bundesland, Landkreis, Einwohner, Fläche, Einwohnerdichte, Kfz-Kennzeichen, Höhe, nächste Großstadt und Luftlinie zur Landeshauptstadt, Ersterwähnung, Bahnhöfe. Aus `data/geo.sqlite`, bisher ohne Frage: Postleitzahl, Küstenort. Neu: Wahlergebnis (stärkste Partei, Anteile, Wahlbeteiligung), Bürgermeister, Partnerstädte, Vorwahl, Eingemeindung bei Stadtteilen.
- **„Option" heißt:** Fehlt eine Eigenschaft für einen Ort, fehlt sie. Nichts wird geraten oder aus dem Nachbarort übernommen.
- **Quellen:** Der Altbestand trägt für kleine Orte nur Höhe und teils Einwohner (Befund in Spielkonzept v0.2.6 §8a). Führend sind Wikidata, die Wikipedia-Infobox und für die Wahl die Wahlbezirksstatistik der Bundeswahlleiterin zur Bundestagswahl 2025 (amtlich, alle Gemeinden, je Gemeinde aus Urnen- und Briefwahlbezirken summiert). Der Altbestand läuft als zweite Quelle mit; weicht er ab, wird das vermerkt und der Wert nicht gespielt.
- **Folge aus E5:** Der Katalog führt je Eigenschaft, ob sie einwertig ist, ob ihre Quelle vollständig ist und ob sie zeitabhängig ist.
- **Stadtteile (E7):** Kennzeichen, Landkreis und Wahlergebnis gelten für die Gemeinde und sind so gekennzeichnet. Die Wahlbezirke Freiburgs tragen in der amtlichen Datei keine Stadtteilnamen.
- **Nicht übernommen:** das nächste Nachbarland (die Grenzpunkt-Tabelle der Originalvariante ist zu grob; der Punkt „Breisach" liegt rund 48 km neben Breisach, in den Vogesen) und die ICE-Strecken (nur große Städte).
- **Offen:** Kommunalwahl und Landtagswahl je Gemeinde gibt es amtlich nur bei den Statistischen Landesämtern, je Land in eigener Form. Für den Bürgermeister gibt es keine amtliche bundesweite Quelle; die Infobox ist ohne Aktualitätsprüfung.
- Skript und Ergebnis: `scripts/data-fetch/gemeinde_achsen_grunddaten.py`, `data/gemeinde-achsen/iter1/grunddaten.json`.

## Begriffe zwischen den beiden Konzepten

| Spielkonzept Reise-Modus | Gemeinde-Achsen v0.5 |
|---|---|
| „Achse" (Fakten-Typ mit Wert) | Eigenschaft eines Entitätstyps |
| Fragefamilie A Behauptung / B Lüge / C Größenordnung | keine Entsprechung; die Frage-Achsen A–D in v0.5 §6 sind etwas anderes |
| Radar (Familie A mit Orten als Optionen) | Frage-Achse C (Merkmal fest, Ort gesucht) |
| Schicht 0, Schicht 1 (ab v0.2.4) | Schicht 0, Schicht 1 |
| „Schicht 2" (bis v0.2.3) | Schicht 1 |

## Überholt in v0.5

- Status-Block „Spielmechanik = 1:1 aus bestehendem QuizAway übernommen": Für den Reise-Modus gilt das Spielkonzept v0.2.4.
- §11 Nr. 5 und §14 erster Punkt: durch E4 ersetzt.

## Nicht entschieden, nur gemessen

Der Stufe-1-Prompt (v0.5 §9.1) erfasst Herkunft und Gründe nicht zuverlässig; zwei Zusatzregeln beheben das an einem Ort (Umkirch). Vorschlag und Messung stehen in `quizaway-stufe2-vorbereitung-2026-10-01.md` §4.

*Ende.*
