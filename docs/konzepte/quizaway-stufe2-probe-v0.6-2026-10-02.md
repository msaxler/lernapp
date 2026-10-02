# QuizAway — Stufe 2, Karten-Prompt v0.6: Probe an drei Orten

**Datum:** 2026-10-02 · **Grundlage:** Bericht zum zweiten Volllauf (W3, W8), Faktencheck-Bericht (F1–F5), Entscheide Mike vom 2026-10-02 · **Daten:** `data/gemeinde-achsen/iter1/` (`prompt-karten-v0.6.txt`, `eingabe-v0.6/`, `karten-v0.6/`, `faktencheck-v0.6/`)

**Ergebnis in einem Satz:** An den drei Probeorten (Zähringen, St. Peter, Horben) schreibt der Prompt v0.6 21 Karten, von denen der Faktencheck 14 bestätigt, 4 korrigiert und 3 als nur durch Wikipedia belegt führt; keine muss gesperrt werden, und keine „falsche" Option trifft mehr die Wirklichkeit.

Was die Probe nicht zeigt: wie es an den übrigen sieben Orten aussieht, und ob die Karten am Tisch tragen.

---

## 1. Was Mike entschieden hat (2026-10-02)

| Frage | Entscheid | Umsetzung |
|---|---|---|
| Anschluss, wenn der Fakt den Ort davor nur als Teil eines Namens nennt | ja, als Kann | Regel 10; der Anschluss trägt den Vermerk „(Namensteil)", der Faktencheck prüft den Bezug |
| Zweite Quelle bei dünnem Ortsartikel | ja | unter 1.000 Wörtern werden bis zu drei verlinkte Artikel mit dem Ortsnamen im Titel geholt und extrahiert (`scripts/data-fetch/gemeinde_achsen_zweitquellen.py`) |
| Politik-Karte bei Stadtteilen | „Die amtlichen Ergebnisse gibt es auch immer auf Ebene der Kommune, also Stadtteilergebnis holen" | Freiburg veröffentlicht die Bundestagswahl 2025 je Stadtbezirk als Open Data seines Wahlportals; Zähringen und Günterstal haben jetzt ihr eigenes Ergebnis |
| Höhe als Zahlen-Karte | nur wenn die Quellen sich einig sind | Der Plan vergibt die Höhe nur, wenn die Quellwerte höchstens fünf Prozent auseinanderliegen |
| Zahl aus dem Artikel als Zahlen-Karte | ja, wenn der Steckbrief einen Anhalt gibt | Regel 6; Karte 7 des Plans darf eine solche Zahl nehmen |

---

## 2. Was sich gegenüber v0.5 ändert

**Grunddaten** (`grunddaten.json`): Wahlergebnis je Stadtbezirk (Zähringen: Grüne 30,2, CDU 20,3, SPD 15,1, Linke 14,1, AfD 8,7 Prozent; Wahlbeteiligung 87,0 Prozent); alle Parteien ab fünf Prozent statt der vier stärksten; die Lage als Entfernung und Richtung von der nächsten Großstadt; das Kennzeichen als Hauptkennzeichen und nicht mehr einwertig.

**Eingabe** (`scripts/data-build/gemeinde_achsen_karten_eingabe.py`): Der Plan nennt für jeden Klassiker die Eigenschaft und wechselt sie von Ort zu Ort (Zahl: Einwohner, Ersterwähnung, Fläche, Höhe, Dichte; Politik: zweitstärkste Partei, Wahlbeteiligung, Anteil der stärksten Partei; Zugehörigkeit: Landkreis, Kennzeichen, Partnerstadt, Eingemeindung, Luftlinie zur Landeshauptstadt). Dazu Lage und Artikeltitel, die Fakten der zweiten Quelle, ein Spender statt zwei, und ein Block Berichtigungen (§5).

**Prompt** (`prompt-karten-v0.6.txt`), die wichtigsten Regeln:
- Vorbehalte der Quelle bleiben stehen („gilt als", „der Sage nach", „soll"); Vergangenes steht in der Vergangenheit; was sich bald ändern kann, trägt keine Karte.
- Hat eine Sache Zweck oder Zugehörigkeit gewechselt, nennt die Frage ihren Zeitpunkt.
- Erfundene falsche Optionen: keine üblichen Mitursachen (Bauland, Anwohner, Platzmangel), nichts, was zu einem anderen Zeitpunkt zutraf, kein Nachbarstaat bei Herrschaftswechseln.
- In Lügen-Karten sind die wahren Aussagen unangreifbar: kein Superlativ, nichts Veränderliches.
- Die Fahrt-Regel gilt nur für Geschichten; bei Klassikern sind Landkreise und Parteien der Nachbarn erlaubt.
- Kennzeichen: gefragt wird nach dem, das die meisten Autos tragen; falsche Optionen aus anderen Kreisen.
- Festes Format der Optionen („1. "), neues Feld PRÜFHINWEIS für den Faktencheck.

---

## 3. Die Probe in Zahlen

| | v0.5, dieselben drei Orte | v0.6 |
|---|---|---|
| Karten | 21 | 21 |
| bestätigt | 10 | 14 |
| korrigiert | 5 | 4 |
| unsicher (nur Wikipedia) | 3 | 3 |
| gesperrt | 3 | 0 |
| „falsche" Antwort, die stimmt oder der Wahrheit nahekommt | 4 | 1 |

Mechanisch: alle Rückseiten höchstens 57 Wörter, Lösung überall an der Stelle des Plans, ein Verstoß (eine Aussage mit neun statt acht Wörtern, korrigiert).

---

## 4. Befunde

**P1. Die Regeln gegen zufällig wahre Optionen greifen.** Die Horben-Karte zur Eingemeindung, im zweiten Lauf gesperrt, fragt jetzt „Welche Folge nennt die Ortsgeschichte?" und stellt nur Optionen dagegen, die den Fakten widersprechen. St. Peters Lügen-Karte hängt am Baustil der Kirche statt an Württemberg. Übrig ist ein Fall: Bei Horbens Kirchenportal lag die Option „aus einer aufgehobenen Klosterkirche" zu nah an der Wahrheit, weil auch die Spitalkirche aufgehoben wurde.

**P2. Die zweite Quelle öffnet Zähringen.** Aus den Artikeln zur Burg und zum Geschlecht kommen vier neue Geschichten: wie Berthold II. zum Herzogstitel kam, die Eroberungen der Burg, die Verlegung auf den Freiburger Schlossberg, die Thomaskirche. Das Thema der handgeschriebenen Karte (Herzöge und ihre Burg) ist damit erreicht. Die Kehrseite: Zwei der vier Korrekturen der Probe stammen aus diesen Artikeln (ein Kaufpreis dem falschen Jahr zugeordnet; 1097 gegen 1098).

**P3. Die Klassiker wechseln.** Der Plan vergibt an den drei Orten Höhe, Einwohnerdichte (zweimal), zweitstärkste Partei, Wahlbeteiligung, Anteil der stärksten Partei, Eingemeindungsjahr, Luftlinie nach Stuttgart und Kennzeichen. Alle neun sind bestätigt. Über die zehn Orte gerechnet kommt jede Politik-Frage drei- bis viermal vor statt eine zehnmal.

**P4. Der Anschluss über den Namensteil kommt zurück.** St. Peter schließt an Zähringen an mit „Das Kloster St. Peter gründete Zähringerherzog Berthold II."; der Faktencheck bestätigt den Bezug. Das ist der Anschluss, der im ersten Solo-Test gut wirkte.

**P5. Fehler der Extraktion kommen wieder, solange die Fakten nicht berichtigt sind.** Horbens „Portal kam 1805/06 nach Horben" stand im zweiten Lauf und steht in der Probe wieder, weil die Extraktion dieselbe ist. Der Faktencheck findet solche Fehler, aber sein Ergebnis floss bisher nicht zurück.

**P6. Unsicher bleibt, was nur Wikipedia sagt.** Dieselben zwei St.-Peter-Karten (Ginster-Handel, Seminarist) sind wieder da und wieder unbelegt. Das ändert kein Prompt; es bräuchte die Einzelnachweise des Artikels oder die Ortschronik.

**P7. Steckbrief bei Stadtteilen.** „3 km nördlich von Freiburg" ist für einen Stadtteil schief. Die Eingabe sagt jetzt „Stadtteil von Freiburg, 3 km nördlich der Stadtmitte".

---

## 5. Folge aus P5: Berichtigungen fließen zurück

Die Eingabe trägt je Ort einen Block BERICHTIGUNGEN mit den Gründen aller bisherigen Korrekturen (`faktencheck/korrekturen.json`); der Prompt lässt sie den Fakten vorgehen. Für Kirchzarten steht dort zum Beispiel, dass Baden 1805 Kurfürstentum war und dass es 2010 eine zweite Mountainbike-Weltmeisterschaft in Deutschland gab. Der Block kam erst nach der Probe dazu; die drei Probeorte liefen ohne ihn, die übrigen sieben Eingaben enthalten ihn.

Für die Faktendatenbank heißt das: Ein Faktencheck-Befund ist eine zweite Quelle zu einem Fakt und gehört an den Fakt, nicht nur an die Karte.

---

## 6. Aufwand

- Zweite Quelle Zähringen: ein Extraktionslauf mit dem kleinen Modell, rund 3 Minuten, 74.000 Tokens.
- Drei Kartenläufe: je 4 bis 6 Minuten, zusammen rund 380.000 Tokens.
- Drei Faktenchecks: je 3,5 bis 5,5 Minuten, zusammen rund 357.000 Tokens.

Hochgerechnet auf die übrigen sieben Orte: rund 1,7 Millionen Tokens für Karten und Faktencheck.

### Wo ein Mensch mehr bringt als die Automatik

- **Welche Stadt ihr Wahlergebnis wo veröffentlicht**, ist je Stadt eine Suche von Minuten; ein Mensch, der die Stadt kennt, nennt die Seite sofort. Für Freiburg ist es gelöst, für jede weitere Stadt mit Stadtteilen steht es wieder an.
- **Die unsicheren Karten** klärt ein Blick in die Ortschronik schneller als jede Netzsuche.

---

## 7. Was Mike entscheidet

1. **Dritter Volllauf auf den übrigen sieben Orten mit v0.6?** Vorschlag: ja. Die drei Probeorte sind fertig und geprüft.
2. **Was geschieht mit den Karten aus v0.5?** Vorschlag: Die v0.6-Karten kommen zum Vorrat dazu; wo beide Läufe denselben Fakt tragen, bleibt die v0.6-Karte. Der Kartensatz für den Tisch bleibt, wie er ist.

*Ende.*
