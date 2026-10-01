# QuizAway — Vorbereitung Feldtest Stufe 2 (generierte Karten, Raum Freiburg)

**Datum:** 2026-10-01 · **Status:** Vorbereitung und Probe an einem Ort (§6). **Der Volllauf ist am selben Tag gelaufen; Ergebnis in `quizaway-stufe2-volllauf-2026-10-01.md`, Auswahl im Kuratierblatt `quizaway-stufe2-kuratierblatt-2026-10-01.md`.** Die Prompts des Volllaufs liegen als Dateien unter `data/gemeinde-achsen/iter1/` (Stufe 1 v0.5.1 mit den Zusatzregeln aus §4, Karten v0.4 mit bis zu drei Vorschlägen je Ort); §5 zeigt noch v0.3. · **Grundlage:** Spielkonzept v0.2.4 §10/§11 Nr. 4, Gemeinde-Achsen v0.5 §9.1 und §21, Entscheide Mike 2026-10-01 (`gemeinde-achsen-entscheidungen-2026-10-01.md`).

**Zweck von Stufe 2:** Dieselben zehn Orte wie im handgeschriebenen Kartensatz laufen durch die Pipeline; die generierten Karten werden neben die handgeschriebenen gelegt. Der Unterschied ist die Messung der Pipeline.

**Die Kette hat drei Glieder, nicht zwei:** (1) Fakten extrahieren (Gemeinde-Achsen Iteration 1), (2) aus Fakten eine Karte schreiben (Karten-Prompt, neu, §5), (3) Mike kuratiert. Glied 2 war bisher nirgends beschrieben; Gemeinde-Achsen v0.5 legt die Frage-Generierung ausdrücklich nicht in die Datenbank (§14, §20).

---

## 1. Ortsliste

### 1.1 Zielorte (die zehn Karten)

| Nr. | Ort | Einheit | Quelle Schicht 1 |
|---|---|---|---|
| 1 | Umkirch | Gemeinde | dewiki Umkirch |
| 2 | Gundelfingen (Breisgau) | Gemeinde | dewiki Gundelfingen (Breisgau) |
| 3 | Denzlingen | Gemeinde | dewiki Denzlingen |
| 4 | Zähringen | **Ortsteil von Freiburg** | dewiki Zähringen (Freiburg im Breisgau) |
| 5 | St. Peter (Hochschwarzwald) | Gemeinde | dewiki St. Peter (Hochschwarzwald) |
| 6 | Glottertal | Gemeinde | dewiki Glottertal |
| 7 | Kirchzarten | Gemeinde | dewiki Kirchzarten |
| 8 | Günterstal | **Ortsteil von Freiburg** | dewiki Günterstal |
| 9 | Horben | Gemeinde | dewiki Horben |
| 10 | Staufen im Breisgau | Stadt | dewiki Staufen im Breisgau |

Zähringen und Günterstal haben keinen eigenen Gemeindeschlüssel. Sie werden nach Gemeinde-Achsen v0.5 §4.6 als Entität `ortsteil` der Gemeinde Freiburg geführt; ihre Fakten tragen `ortsteil_bezug`. Quelltext ist der Stadtteil-Artikel, nicht der Freiburg-Artikel (Entscheid E7).

Die zehn Orte liegen höchstens 27 km auseinander (St. Peter – Staufen, Luftlinie aus Näherungskoordinaten).

### 1.2 Spenderorte für den Kontext-Spiegel

Bedingung: von **jedem** der zehn Zielorte 50–100 km entfernt, 2.000–20.000 Einwohner, kein Ort der Strecke. Ermittelt aus `data/staedte.json` (deshalb lauter Orte mit Stadtrecht; für die Probe unerheblich). Ausgewählt nach Verschiedenheit der Landschaft, damit die Katalog-Saat nicht nur Breisgau enthält (Vielfaltskriterium v0.5 §8).

| Ort | Abstand zu den Zielorten (km) | Einwohner | Landschaft |
|---|---|---|---|
| Oberkirch | 54–77 | 19.847 | Ortenau, Renchtal |
| Renchen | 59–81 | 7.582 | Ortenau, Rheinebene |
| Rheinau | 67–89 | 11.346 | Rhein, Hanauerland |
| Dornstetten | 61–87 | 8.194 | Nordschwarzwald |
| Sulz am Neckar | 59–86 | 12.847 | oberer Neckar |
| Oberndorf am Neckar | 50–77 | 14.853 | oberer Neckar |
| Spaichingen | 53–78 | 13.714 | Baar, Albrand |
| Mühlheim an der Donau | 63–88 | 3.649 | obere Donau |
| Engen | 58–78 | 11.311 | Hegau |
| Tengen | 52–71 | 4.818 | Hegau, Randen |

---

## 2. Quellen

- **Schicht 1 (Geschichten, Herkunft, Gründe):** deutschsprachiger Wikipedia-Artikel je Ort, wie v0.5 §11.
- **Schicht 0 (Einwohner, Höhe, Landkreis, Lage):** Wikidata. Die Vorgänger-Datenbasis `data/staedte.json` trägt hier nicht: Sie enthält 2.051 Orte mit Stadtrecht, von den zehn Zielorten nur Staufen. Ihre Spalte Kfz-Kennzeichen ist im Raum Freiburg fehlerhaft (Bad Krozingen und Staufen „FDS", Todtnau „TÜ", Ettenheim „TUT"), und der Eintrag „Gundelfingen a.d.Donau" (Bayern) trägt die Koordinaten von Gundelfingen im Breisgau.
- **Gemeinde-Webseiten (E4):** in dieser Probe nicht. Sie kommen dazu, wenn der Wikipedia-Artikel für einen kleinen Ort zu wenig Warum-Fakten hergibt; das zählt §7 mit.

---

## 3. Was Stufe 2 misst

| Messgröße | Woraus |
|---|---|
| Warum-Fakten je Ort (Herkunft, Grund, Anlass) | Extraktion |
| B-Quote: Orte mit ≥ 2 belastbaren Schicht-1-Fakten | Extraktion |
| Karten, für die kein zulässiger Distraktor zu finden war | Karten-Prompt, Ausgabe „KEINE KARTE" |
| Vergleichsanschlüsse (a) je Ortspaar; Erzählanschlüsse (b) nebenbei | Schicht 0; Extraktion |
| Abstand zur handgeschriebenen Karte: gleicher Fakt gewählt? gleiche Familie möglich? | Karten nebeneinander |
| Am Tisch: T2-Anteil und W je Karte, wie in Stufe 1 | Feldtest |

---

## 4. Zusatz zum Stufe-1-Prompt (gemessen an Umkirch)

Der Prompt aus v0.5 §9.1 fragt nach Entität, Eigenschaft, Wert. Das erfasst, **was** es gibt, aber nicht, **warum** etwas so ist oder so heißt. Im Lauf 1 für Umkirch fehlte genau der Fakt, auf dem die handgeschriebene Karte 1 beruht: Der Artikel deutet den Namen als „Ecclesia in Undis", Kirche in den Wellen; die Extraktion behielt nur den alten Namen „Untkilicha". Theorie-Fragen leben von solchen Warum-Fakten.

Zwei Zusatzregeln, an denselben Artikel angelegt (Lauf 2), holen die Namensdeutung und drei weitere Gründe heraus:

```
  - WARUM-FAKTEN: Nennt der Text eine Herkunft, Deutung, Ursache oder einen Anlass
    (Namensherkunft, "geht zurück auf", "benannt nach", "weil", "deshalb",
    "spielt an auf", Grund einer Zerstörung, Grund einer Gründung), dann nimm sie
    als eigene Eigenschaft auf (z.B. namensherkunft, grund, anlass, benannt_nach)
    und gib die Deutung in eigenen Worten als Freitext wieder. Steht im Text
    "vermutlich", "soll", "der Sage nach", dann setze genauigkeit: "vermutlich".
  - SUPERLATIVE UND EINZIGKEIT: "älteste", "größte", "einzige", "erste", "letzte"
    mit Bezugsraum als eigene Eigenschaft (z.B. superlativ: "älteste Pfarrkirche
    des Breisgaus").
```

Das ist ein Vorschlag mit einer Messung an einem Ort, kein Entscheid. Rohausgaben beider Läufe: `data/gemeinde-achsen/probe-2026-10-01/`.

Nebenbefund: Der Artikel schreibt „spielt vermutlich auf die Lage der Kirche auf einer Insel zwischen zwei Bächen an". Die handgeschriebene Karte 1 erzählt es als Tatsache und nennt die Dreisam. Mit der Regel „vermutlich" trägt die generierte Karte die Vorsicht der Quelle.

---

## 5. Karten-Prompt v0.3

Freitext, ohne modellspezifische Mittel (v0.5 P8). Ein Aufruf je Karte. v0.2 nach dem ersten Probelauf (§6): Das Beispiel in Regel 3 ist ausgetauscht, „belegt" und „vermutlich" sind in Regel 1 und 4c geklärt, Regel 8 sagt, was zur Wortzahl zählt und was Erläuterung sein darf. **v0.3 nach Spielkonzept v0.2.5:** Die Rückseite hat höchstens 70 Wörter einschließlich Anschluss (vorher 50 bis 90, eine Zahl ohne Freigabe), und Optionen tragen Ziffern. Die Probe in §6 lief noch mit v0.2; die beiden generierten Rückseiten haben 79 und 76 Wörter und wären jetzt etwas zu lang.

```
ROLLE: Du schreibst eine Spielkarte für ein Reise-Quiz über deutsche Orte.
Die Spielenden sollen sich vor der Auflösung eine eigene Theorie bilden
können. Danach erzählt die Karte, was wirklich ist.

EINGABE:
  ZIELORT: Name, Einwohner, Höhe, Lage in einem Satz.
  FAKTEN: extrahierte Fakten zum Zielort (Entität, Eigenschaft, Wert).
  FAMILIE: A (Behauptung, vier Theorien), B (drei Aussagen, eine gelogen)
    oder C (Größenordnung, vier Spannen).
  LETZTER_PIN (optional): Name, Einwohner, Höhe, Landkreis des zuletzt
    gespielten Orts.
  SPENDER (optional): Fakten aus Orten, die 50 bis 100 km entfernt liegen und
    nicht zur Fahrt gehören.
  FAHRT (optional): Namen aller Orte dieser Fahrt.

AUFGABE: Wähle aus FAKTEN den Fakt, der am ehesten eine Theorie hervorruft
(ein Warum, eine Herkunft, eine überraschende Zugehörigkeit), und schreibe
daraus eine Karte mit Vorderseite und Rückseite.

REGELN:
  1. Die wahre Aussage stammt aus FAKTEN. Füge über den Ort nichts hinzu, was
     dort nicht steht. Trägt der Fakt "vermutlich", sagt auch die Rückseite
     "vermutlich". Als belegt gilt, was FAKTEN nennen, auch mit "vermutlich".
  2. Vorderseite: Ortsname, ein Satz Steckbrief (Einwohner, Lage), dann die
     Frage. Der Steckbrief verrät die Lösung nicht und widerspricht keiner
     Option. Frage höchstens 25 Wörter, jede Option höchstens 8 Wörter.
  3. Jede Option ist eine eigenständige, plausible Theorie als ganzer Satz
     (also "Der Berg war früher ein Weinberg", nicht "wegen Weinbau"),
     keine Stichworte.
  4. Jede falsche Option muss nachweislich falsch sein. Zulässig sind genau
     drei Wege; nenne zu jeder falschen Option den Weg und den Beleg:
     (a) FAKTEN widerlegen sie ausdrücklich.
     (b) Sie ist ein wahrer Fakt eines SPENDER-Orts, und die Eigenschaft ist
         am Zielort mit einem anderen Wert belegt (Landkreis, Herrschaft,
         Bahnstrecke, Namensherkunft).
     (c) Die wahre Antwort ist einwertig (FAKTEN nennen genau eine Herkunft,
         genau einen Grund); dann darf die falsche Theorie frei erfunden
         sein.
     Nicht zulässig: "in FAKTEN steht nichts dazu". Kein Fakt aus einem Ort
     der FAHRT als falsche Option.
     Findest du keine drei zulässigen falschen Optionen, wähle einen anderen
     Fakt. Geht es mit keinem, gib "KEINE KARTE" und den Grund aus.
  5. Familie B: drei Aussagen gleicher Länge und gleicher Machart (alle mit
     Zahl oder alle ohne). Nicht immer ist die Lüge die unauffälligste und
     nicht immer die auffälligste Aussage. Über die Lüge muss sich aus der
     Vorderseite und Allgemeinwissen etwas folgern lassen. Die Stelle der
     Lüge (und in Familie A die Stelle der wahren Option) gibt der Aufrufer
     vor; sie wechselt von Karte zu Karte.
  6. Familie C: vier Spannen ohne Lücke und ohne Überlappung; keine Zahl in
     der Frage, die die Spanne verrät.
  7. Bekanntheit: Ist ein Fakt vermutlich überregional bekannt (Fernsehen,
     prominente Person, Werbespruch der Region), trägt er nicht die Frage; er
     darf in die Rückseite. Gib BEKANNTHEIT: niedrig, mittel oder hoch mit
     einem Satz Begründung an.
  8. Rückseite: höchstens 70 Wörter, Platzhalter, Schlusssatz und Anschluss
     mitgezählt, Quelle nicht. Optionen tragen die Ziffern 1 bis 4. Erster
     Satz ist der Platzhalter
     "Du hattest [Option] getippt." Dann die Geschichte; sie greift die
     naheliegendste falsche Theorie auf und sagt, warum sie naheliegt. Diese
     Begründung ist Erläuterung und darf über FAKTEN hinausgehen; Aussagen
     über den Ort dürfen es nicht. Letzter Satz: "Richtig war N." Darunter
     die Quelle.
  9. Anschluss: höchstens einer, nur wenn LETZTER_PIN gegeben ist und der
     Vergleich für sich interessant ist. Nur aus Zahlen und Zugehörigkeiten
     beider Orte. Eine Beobachtung, keine Frage. Sonst "ANSCHLUSS: keiner".

AUSGABE:
  FAMILIE: ...
  GEWÄHLTER FAKT: ... (Entität, Eigenschaft, Wert)
  BEKANNTHEIT: ...
  VORDERSEITE: ...
  RÜCKSEITE: ...
  ANSCHLUSS: ...
  NEGATIVNACHWEISE: je falscher Option Weg (a/b/c) und Beleg
  NICHT GEWÄHLT: bis zu zwei weitere Fakten, die auch eine Karte tragen würden
```

---

## 6. Probe an einem Ort: Umkirch

Glied 1 (Extraktion) siehe §4. Glied 2 (Karte) schrieb jeweils ein eigener Durchlauf, der nur die Faktendatei las und die handgeschriebene Karte 1 nicht kannte. Rohausgaben: `data/gemeinde-achsen/probe-2026-10-01/`.

**Lauf 1 (Karten-Prompt v0.1) ist nicht ganz blind.** Das Beispiel in Regel 3 lautete „Die Häuser stehen rund um die Kirche"; das ist die erste Option der handgeschriebenen Karte 1. Der Durchlauf hat den Satz als Option übernommen und es selbst gemeldet. Deshalb v0.2 mit neutralem Beispiel und Lauf 2.

**Lauf 2 (Karten-Prompt v0.2), unbeeinflusst:**

| | Handgeschrieben (Karte 1) | Generiert (Lauf 2) |
|---|---|---|
| Gewählter Fakt | Namensherkunft | Namensherkunft |
| Frage | Woher kommt der Name Umkirch? | Woher hat Umkirch vermutlich seinen Namen? |
| Wahre Option | Die Kirche stand in den Wellen der Dreisam. | Die Kirche lag auf einer Insel zwischen Bächen. |
| Falsche Optionen | Häuser rund um die Kirche · Kirche komplett umgebaut · erster Pfarrer hieß Ummo | Dorf wuchs rings um die Kirche · Siedler namens Umbo stiftete die Kirche · Name bedeutete „untere Kirche" |
| Rückseite | erzählt als Tatsache, nennt die Dreisam | sagt „vermutlich", nennt zwei Bäche, greift die „um die Kirche"-Theorie auf |
| Weitere Kandidaten | — | Eigenständigkeit 1974 gegen Freiburgs Eingemeindungswunsch · Wasserschloss, heute Rathaus |

**Was die Probe zeigt, an einem Ort:**
- Mit der Warum-Regel wählt die Pipeline denselben Fakt wie der Mensch und findet von selbst zwei der drei falschen Theorien („um die Kirche", ein Personenname).
- Ohne die Warum-Regel wäre die Karte nicht entstanden; der Fakt fehlte in der Extraktion (§4).
- Die generierte Karte ist vorsichtiger als die handgeschriebene („vermutlich", kein Fluss, den die Quelle nicht nennt).
- **Ein Fehlermuster für das Kuratieren:** Die erfundene Option „untere Kirche" lehnt sich an die belegte Altform *Untkilicha* an und könnte einer echten Deutung zufällig nahekommen. Der Durchlauf hat das selbst angemerkt. Folge für v0.3 des Prompts: erfundene Theorien nicht aus dem Wortmaterial der Fakten bauen; bis dahin prüft Mike genau solche Optionen.

**Was die Durchläufe am Prompt als ungeregelt meldeten** (offen für v0.3): ob „vermutlich" auch auf die Vorderseite gehört; ob weitere Fakten aus der Liste in die Rückseite dürfen (beide Läufe nahmen Ersterwähnung und „älteste Pfarrkirche des Breisgaus" auf); ob „Richtig war N" die Nummer oder den Text meint.

**Was die Probe nicht zeigt:** ob das für Familie B und C trägt, ob kleine Orte genug Warum-Fakten haben, und ob eine generierte Karte am Tisch eine Theorie hervorruft. Das ist ein Ort und eine Familie.

---

## 7. Ablauf des Volllaufs (noch nicht gestartet)

1. Extraktion für 20 Orte (10 Ziel, 10 Spender) mit Stufe-1-Prompt plus Zusatzregeln; Wikidata für Schicht 0. Ausgabe als JSON-Lines nach v0.5 §4.2.
2. Zählen: Entitätstypen (K1 aus v0.5: mindestens zehn), Warum-Fakten je Ort, B-Quote, Anschluss-Quoten.
3. Karten-Prompt je Zielort in der Familie der handgeschriebenen Karte (A C B A C A B A C B), damit die Karten vergleichbar sind.
4. Mike kuratiert.
5. Karten nebeneinander legen; dann Feldtest Stufe 2 am Tisch.

### Wo ein Mensch mehr bringt als die Automatik

- **Fakt-Auswahl:** Der Karten-Prompt gibt unter „NICHT GEWÄHLT" bis zu zwei weitere Fakten aus. Mike wählt je Ort aus bis zu drei Vorschlägen; das kostet zehn Entscheidungen und ersetzt eine Bewertungsfunktion für „ruft eine Theorie hervor", die es nicht gibt.
- **Bekanntheit:** In Stufe 2 schätzt ein Mensch; die Schwelle für den späteren Proxy kommt aus den W-Werten am Tisch, nicht aus einer Formel vorab.
- **Negativnachweis:** Je Karte drei Zeilen Weg und Beleg. Mike liest sie beim Kuratieren gegen; eine automatische Prüfung lohnt erst, wenn die Fehlerarten bekannt sind.
- **Spender:** zehn Orte von Hand gewählt (§1.2), keine Auswahlregel gebaut.

---

## 8. Offen

- Zusatzregeln aus §4 in den Stufe-1-Prompt übernehmen? Bisher eine Messung an einem Ort.
- Liefert der Wikipedia-Artikel für Horben (1.200 Einwohner) genug Warum-Fakten, oder braucht es dort die Gemeinde-Webseite (E4)?
- Wer extrahiert im Volllauf: wie in der Probe ein kleines Modell über den Artikel, oder ein größeres mit dem Volltext? Die Probe zeigt nur, dass der Prompt mit einem kleinen Modell trägt.

*Ende Stufe-2-Vorbereitung.*
