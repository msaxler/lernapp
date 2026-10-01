# QuizAway — PC-Prüfung Spielkonzept v0.2.3 und Feldtest-Protokoll Solo Freiburg

**Datum:** 2026-10-01 · **Fassung 2** (nach Eingang von Kartensatz 018 und Spielkonzept v0.2; B3 neu gefasst, B10 neu, B1/B2/B8/B9 ergänzt) · **Geprüft:** `quizaway-spielkonzept-reise-modus-v0.2.3-2026-10-01.md` (GEOSYNC 020), `quizaway-feldtest-protokoll-solo-freiburg-2026-10-01.md` (019), `quizaway-feldtest-solo-kartensatz-freiburg-2026-10-01.md` (018) · **Gegen:** Spielkonzept v0.2 (015), Gemeinde-Achsen v0.5 + Iter-1-Entscheidungen (E1–E3), Transfer-Konzept v1.1, PC-Session-Fokus 21.06.

**Urteil:** v0.2.3 reicht als Arbeitsgrundlage für alles bis einschließlich Stufe 2; v0.2 wird nur für §9 und Anhang A gebraucht. Das Protokoll ist rechnerisch sauber, und der Kartensatz erfüllt die Vorgaben aus §10. Die Lügen-Hypothese in §8 Nr. 2 steht aber auf einer Beschreibung der Karten 3 und 10, die der Kartensatz nicht deckt (B3). Schritt 4 (Stufe 2 aus Iteration 1) geht so, wie er dasteht, nicht auf (B1, B2).

---

## A. Was stimmt

- **Zahlen:** 6 × T2 (Karten 1, 4, 5, 7, 8, 9), Familie A 3 von 4, B 1 von 3, C 2 von 3. Stimmt mit der Tabelle überein.
- **Kartensatz gegen §10 Solo:** drei Vergleichsanschlüsse (2, 6, 9), ein Erzählanschluss (5), zwei Radar verbal (6, 8). Erfüllt.
- **Taktung §5:** Folge A C B A C A B A C B, keine Familie zweimal hintereinander; C auf 2, 5, 9; eine Leiter auf drei C-Fragen. Erfüllt.
- **Rechnungen in den Anschlüssen:** Gundelfingen/Umkirch 12.168 zu 5.755 (gut doppelt), Glottertal/St. Peter 3.225 zu 2.727 (498 mehr), Horben/Günterstal 607 zu 330 m (277 m) und 1.204 zu 2.159 Einwohner. In sich stimmig. Die Fakten selbst habe ich nicht gegen Quellen nachgeprüft.
- **Kein Ermüdungstrend:** Die Karten ohne Theorie liegen auf 2, 3, 6, 10, die Karten 7, 8, 9 tragen alle T2. Das spricht gegen „Durchtippen" (K3b).
- **Anschluss-Bezug:** Karte 5 (St. Peter) knüpft an Karte 4 (Zähringen) an, also an den letzten gespielten Pin. Regelkonform.
- **Änderungsumfang:** v0.2.3 setzt Protokoll §5 um (Bekanntheitsfilter, Lügen-Hypothese, Kann-Status für Klasse b).

---

## B. Befunde

### B1. Stufe 2 lässt sich aus den zehn Freiburg-Orten allein nicht bauen (§11 Nr. 4)

1. **Kein Kontext-Spiegel möglich.** §8 Nr. 1b verlangt Spenderorte 50–100 km entfernt. Der Kartensatz nennt als Raum „Freiburg mit Stadtteilen und Umland bis 20 km". Iteration 1 mit nur diesen zehn Orten liefert keinen einzigen zulässigen Spiegel-Distraktor. Es braucht zusätzlich Spenderorte im Abstandsband (etwa Ortenau, Hochrhein, Baar).
2. **Iteration 1 liefert Fakten, keine Karten.** Gemeinde-Achsen v0.5 legt die Frage-Generierung ausdrücklich in die Edition (§20 B1) und schließt eine Generator-Bibliothek aus (§14). Der Schritt „aus Fakten wird Karte" (Frage, Theorie-Optionen, Reveal mit Einwebung, Anschluss) ist nirgends beschrieben. §10 nennt ihn nur in Klammern („Prompt, Achsen-Regeln, Negativnachweis"). Ohne diesen Karten-Prompt misst Stufe 2 nichts.
3. **Zähringen und Günterstal sind Stadtteile von Freiburg,** keine Gemeinden, also ohne eigenen AGS. In v0.5 hängen sie als `ortsteil` an der Gemeinde Freiburg (§4.6); der Stufe-1-Prompt erwartet einen Quelltext „über die Gemeinde". Für diese zwei Karten muss der Stadtteil-Artikel als Quelle festgelegt werden. §8a nennt die Granularität „für die Spielmechanik unerheblich"; für die Pipeline ist sie es hier nicht.
4. **Vielfaltskriterium:** v0.5 §8/§21 sieht für Iteration 1 zehn bewusst verschiedene Orte vor (Katalog-Saat, K1). Zehn Orte aus einem Raum verengen den Katalog (Zähringer, Schwarzwald, Breisgau). Die Spenderorte aus Punkt 1 mildern das, wenn sie verschieden gewählt werden.

### B2. Der „Negativnachweis light" ist bei lückenhafter Datenbank keiner (§8 Nr. 1b, §8a)

§8 Nr. 1 sagt zuerst: „nicht als richtig bekannt" reicht nicht. Weg (b) akzeptiert danach „Achse für den Zielort nicht gesetzt", und §8a nennt das „eine Abfrage, keine Recherche". In einer Datenbank, die laut §8a lückenhaft wächst, heißt „nicht gesetzt" aber „unbekannt", nicht „falsch". Bei Vorhandensein-Fragen (Freibad, Burg) kann der Spiegel-Distraktor also wahr sein, und dann bekommt eine Person mit richtiger Antwort „falsch" gesagt. Das ist der eine Fehler, den auch „Fun vor Korrektheit" nicht deckt.

Der Spiegel trägt in zwei Fällen:
- **Einwertige Eigenschaften, am Zielort mit anderem Wert gesetzt** (Namensherkunft, Ersterwähnung, Landkreis): Der fremde Wert ist dann belegt falsch.
- **Eigenschaften aus einer vollständigen Quelle** (Schicht 0, zum Beispiel OSM für Freibad oder Bahnhof): Dort ist „nicht gesetzt" tatsächlich „nicht vorhanden".

Der Kartensatz stützt genau diese Eingrenzung: Die drei handgemachten Negativnachweise sind „Stadtrecht: ja" (Karte 10) und „Bahnstrecke: Höllentalbahn" (Karte 7), beides einwertig und anders belegt, sowie „Straßenbahn: nein" (Karte 3), ein ausdrückliches Nein aus einem vollständig bekannten Netz. Keiner beruht auf „nicht gesetzt".

Vorschlag für den Wortlaut: „… dessen Eigenschaft am Zielort entweder mit einem anderen Wert belegt ist oder aus einer vollständigen Quelle stammt und dort fehlt."

### B3. Lügen-Hypothese (§8 Nr. 2, §11 Nr. 2) — mit dem Kartensatz neu gefasst

1. **Die Beschreibung im Protokoll passt nicht zu den Karten.** Protokoll §2 sagt: Bei 3 und 10 war die Lüge die „zu gut, um wahr zu sein"-Aussage, bei 7 die unspektakulärste. Im Kartensatz ist die Lüge von Karte 10 „Ist die größte Gemeinde ohne Stadtrecht", neben Fausts Tod und der angehobenen Altstadt; die Rückseite sagt selbst: „Die beiden unglaublichen Aussagen stimmen." Bei Karte 3 ist die Lüge die Straßenbahn seit 2014, neben sieben Zigarrenfabriken. Die Lüge war also in Karte 10 eindeutig und in Karte 3 wohl auch schon die unauffällige Aussage. Das Muster, das §8 Nr. 2 empfiehlt, lag in allen drei Karten vor und hat nur bei Karte 7 eine Theorie erzeugt. Der Test stützt die Hypothese damit nicht.
2. **Was 3 und 10 von 7 tatsächlich unterscheidet:** Beide Lügen sind gespiegelte Fakten aus Gundelfingen (so die Anmerkungen im Kartensatz), und Gundelfingen war Karte 2. Deren Rückseite nennt beides wörtlich: „seit 2014 sogar Endhaltestelle der Freiburger Straßenbahn" und „die größte Gemeinde im Landkreis, die keine Stadt ist". Karte 3 folgt unmittelbar darauf. Die Person konnte die Lüge wiedererkennen und brauchte keine Theorie. Karte 7 (Rheintalbahn) verlangt dagegen eine Überlegung zur Lage im Tal. Dazu kommt bei Karte 10 ein Formleck: Die Lüge ist die einzige Aussage ohne Jahreszahl.
3. **Das ist eine Vermutung aus den Karten, keine Messung.** Entscheiden kann es der Rohbogen (Spalte „Wortlaut der Theorie"): Hat die Person bei 3 oder 10 Gundelfingen erwähnt?
4. **Folge für die Regel:** Trägt die Vermutung, heißt die Regel nicht „Lüge unspektakulärer", sondern „Der Spender eines gespiegelten Fakts darf kein Ort dieser Fahrt sein". Die Abstandsregel 50–100 km deckt das meist ab, auf langen Fahrten aber nicht. Der handgemachte Spiegel hat die Abstandsregel selbst verletzt: Gundelfingen grenzt an Denzlingen.
5. **Test mit Person 2:** In den Karten 3 und 10 die Lüge durch eine gleich unauffällige ersetzen, die aus keinem Ort der Strecke stammt (in Karte 10 mit Jahreszahl); Karte 7 und die übrigen sieben Karten bleiben. Entsteht bei 3 und 10 jetzt eine Theorie, war es das Wiedererkennen. Die Karten 1, 4, 8, 9 zeigen, ob Person 2 vergleichbar spielt. „Derselbe Kartensatz" und „umgedrehtes Muster" in §11 Nr. 2 schließen sich ohnehin aus.
6. **Aussage stärker als die Messung.** Das Konzept schreibt als Tatsache: „wurde per Ausschluss getippt". Das Protokoll führt Formerkennung unter „nicht erhoben" (§4). Gemessen ist nur: bei 3 und 10 keine Theorie, bei 7 eine.
7. **Wortlaut:** „die beiden Wahrheiten" gilt nur für die Bahn; im Auto hat B eine Wahrheit.

### B4. „Kern trägt" ist mehr, als das Protokoll hergibt (Status-Block, §11 Nr. 1)

Nach §7 ist K1 Teil 3 „das Spiel", und die drei Teile werden getrennt protokolliert. Erhoben wurden sie nicht (Protokoll §3), K3a ebenfalls nicht (§4), obwohl der Bogen im Kartensatz beides vorsieht. Belegt ist: K3b nicht ausgelöst (6 von 10 T2, kein Ermüdungstrend), K6 nicht ausgelöst (eine Leiter), Reveals pauschal positiv. Das Protokoll sagt das selbst („Beobachtungen, keine Befunde"); der Status-Block des Konzepts sollte dieselbe Vorsicht tragen, zum Beispiel: „Theoriebildung findet statt (6 von 10 T2), K1 noch nicht einzeln erhoben."

### B5. Die T-Skala hat keinen Platz für „gewusst" (§10, Protokoll Karte 6)

Karte 6 steht als T1. T1 ist aber „Auswahl ohne Begründung"; die Person hatte einen Grund, sie wusste es. Ein eigenes Kürzel **W (gewusst oder wiedererkannt)** hält K3b sauber und macht den Bekanntheitsfilter messbar: W je Karte über mehrere Personen ist genau die Zahl, die der Proxy später treffen muss. Es würde auch den Fall aus B3 erfassen. Dafür sollte Karte 6 bei Person 2 im Satz bleiben. Protokoll §5.4 Nr. 1 ließ das offen, Konzept §11 Nr. 2 hat die Frage nicht übernommen. Außerdem fehlt im Protokoll, ob der Raum Freiburg der Testperson unbekannt war (Vorgabe aus §10 und aus dem Kartensatz).

### B6. Bekanntheitsfilter (§8 Nr. 6)

1. **Bekannt ist der Fakt, nicht der Ort.** Glottertal ist klein, die Schwarzwaldklinik ist berühmt. Ein Proxy über den Ort (Wikipedia-Prominenz des Gemeinde-Artikels) trifft daneben. Messbar ist die Bekanntheit der Sache, auf die der Fakt zeigt (Sprachversionen und Abrufe des Artikels über Serie, Person, Bauwerk). Dafür liegt mit dem Fame-Index aus MixMi ein fertiges Verfahren vor (Perzentil-Normierung, Schwelle als Parameter), das laut Notiz vom 30.06. ohnehin auf die Gemeinde-Achsen übertragen werden sollte.
2. **Reibung mit v0.5 §8.4:** Dort stehen „Drehort" und „prominente Persönlichkeit" als Singleton-Gold für das Quiz. Kein Widerspruch, aber es braucht einen Satz: Gold gehört in Reveal und Steckbrief; die Frage trägt es nur unterhalb der Bekanntheitsschwelle.
3. **Publikumsabhängig:** Eine Person, eine Karte. Die Schwarzwaldklinik kennt die eine Generation, die nächste nicht. Die Schwelle ergibt sich erst aus W-Werten mehrerer Personen (B5).

### B7. Begriffe an der Naht zu Gemeinde-Achsen v0.5 (betrifft §11 Nr. 6)

| Im Spielkonzept | In Gemeinde-Achsen v0.5 | Folge |
|---|---|---|
| Schicht 0 / 1 / 2 (§2, §4, §8a) | Zwei Schichten: 0 deterministisch, 1 LLM-extrahiert. Eine Schicht 2 gibt es nicht. | „Schicht 2" verweist ins Leere; gemeint ist vermutlich v0.5-Schicht 1 |
| „Achse" = Eigenschaft oder Fakten-Typ („Achse Bekanntheit", „Achse nicht gesetzt") | „Achsen" = Frageformen A–D; Fakten-Typen heißen „Eigenschaften" | Doppelbelegung |
| Fragefamilien A / B / C | Frage-Achsen A / B / C / D | Gleiche Buchstaben, andere Bedeutung. Radar ist hier Familie A, dort Achse C |
| Kontext-Spiegel: Spender 50–100 km entfernt | §10 Distraktor-Pool beginnt bei 30 km, „Geografie schlägt Administration" | Für Theorie-Distraktoren muss Stufe 1 des Pools ausdrücklich ausgesetzt werden |
| §8a: Gemeinde-Webseiten als Quelle für A und B; Ziel ~80.000 Orte | §11 Nr. 5 und §14: Webseiten „nicht in v0.x", kein Crawler; ~10.000 Gemeinden | §8a nennt sich „keine neue Entscheidung", ist gegenüber v0.5 aber eine. Gehört als E4 in die Iter-1-Entscheidungen |

Vor Schritt 6 („Content-Regeln ins Achsen-Regelwerk") lohnt eine kleine Übersetzungstabelle, sonst wandern die Doppelbelegungen in beide Dokumente.

### B8. Verweise innerhalb von v0.2.3

- **K3, K4, K9:** §2 „Fragilster Baustein (K3)", §8 Nr. 6 „Kriterium K3 ‚begründbares Raten'", §3.3 „K4 ist die tragende Säule", §3.1 und Anhang B „K9". In §7 gibt es K1–K7 mit K3a/K3b, K4 ist dort der Beifahrer (im Solo sinnlos), K9 fehlt. v0.2 zeigt die Herkunft: Dort steht „K4 (Reveal trägt Geschichte)", „K5-Ersatz", „K6 (Gesprächswert)". Das ist eine zweite Zählung (Qualitätskriterien) aus einer Fassung vor v0.2, die auch v0.2 nicht mehr aufführt. Am einfachsten: die Kriterien an diesen vier Stellen beim Namen nennen statt bei der Nummer.
- **Anhang A** steht in v0.2 und liegt jetzt vor. Ein Verweis darauf in v0.2.3 genügt.
- **§9 „unverändert aus v0.2"** stimmt in zwei Punkten nicht mehr, siehe B9.
- **Status-Block:** Die Freigabe 12:29 galt v0.2.2, steht jetzt aber unter v0.2.3 (das erst nach dem Test um 15:17 entstand). Die Provenance nennt „nur §8 Nr. 2 und Nr. 6, §11"; geändert ist auch §8 Nr. 4b.

### B9. §9 und Vorgriff auf Schritt 7 (Transfer-Konzept v1.1)

v0.2 §9 enthält zwei Aussagen, die v0.2.3 mit „unverändert" übernimmt, obwohl der eigene Text sie überholt hat:
- **„Kern-Interface bleibt: ein Klick, vier Strings."** v0.2.3 hat zwei bis vier Optionen (Familie B im Auto: zwei Aussagen), Mehrfachauswahl mit Bestätigen und den „uneinig"-Button ohne Option.
- **„Wer-glaubt-wem: zweite Abgabe; einzige Erweiterung der Kern-Schnittstelle."** Seit v0.2.1 werden die Einschätzungen nicht aufgezeichnet (§3.2, §6). Es gibt keine zweite Abgabe mehr; die Erweiterungen der Schnittstelle sind jetzt Optionssatz und „uneinig".

Damit löst der Reise-Modus das Kipp-Kriterium aus v1.1 §2 aus („realer Konsument mit anderer Antwortform → Schema revisiten"): v1.1 schreibt immer vier Optionen, genau einen `chosenIndex` und einen Zeit-Score vor. Auch der Status-Satz in Gemeinde-Achsen v0.5 („Spielmechanik 1:1 aus bestehendem QuizAway") ist überholt. Kein Handlungsbedarf vor Stufe 2; §9 sollte in der nächsten Fassung ausgeschrieben werden, und die PC-Session in Schritt 7 beginnt mit diesem Befund.

### B10. Radar-Karten 6 und 8 (neu, aus dem Kartensatz)

1. **Himmelsrichtungen.** §2 schreibt für Radar verbal vor: „relativ zur Fahrt, nie Himmelsrichtungen". Karte 6 sagt „13 km nordwestlich" und „10 km südlich", Karte 8 „südwestlich Richtung Freiburg". Am Tisch stört das nicht, aber der Satz „Radar verbal funktioniert" (Protokoll §2) gilt nur für diese Form, nicht für die Auto-Form.
2. **Länge.** Die Vorderseite von Karte 6 hat rund 60 Wörter, einzelne Optionen neun. Die verbindliche Redaktionsregel (Frage ≤ 25 Wörter, Option ≤ 8, Vorlesezeit ≤ 20 s) ist für Radar verbal so nicht einzuhalten. Radar braucht eine eigene Grenze, und die lässt sich erst im Auto-Test messen.
3. **Die richtige Antwort ist beide Male der aktuelle Ort.** Im Solo sieht die Person die Namen der kommenden Orte (§3.3, im Test die Streckenkarte). „Der nächste Ort auf meiner Karte" gewinnt damit jede Radar-Frage. Bei zwei Karten fällt das nicht auf, als Bauregel für die Pipeline wäre es ein Leck. Das Beispiel in §2 (Freibad bei einem der Nachbarn, Reveal kehrt zum aktuellen Ort zurück) vermeidet es; die Karten sollten dem folgen und die Lösung auch mal beim Nachbarn haben.

---

## C. Was Mike entscheiden muss

1. **Rohbogen nachsehen:** Fiel bei Karte 3 oder 10 der Name Gundelfingen (B3)? Davon hängt ab, welche Regel in §8 Nr. 2 gehört.
2. **Zweite Solo-Person:** Lügen in 3 und 10 gegen streckenfremde tauschen, Karte 6 als Bekanntheits-Kontrolle behalten, Kürzel W einführen (B3, B5)?
3. **Stufe 2:** Spenderorte im Band 50–100 km dazunehmen, Zähringen/Günterstal als Ortsteile von Freiburg führen (B1), und den Kontext-Spiegel auf einwertige Eigenschaften und vollständige Quellen begrenzen (B2)?

**Entschieden (Mike, 2026-10-01): alle drei gemäß Vorschlag.** Umsetzung: Spielkonzept v0.2.4 (Anhang D), Kartensatz Fassung 2, `quizaway-stufe2-vorbereitung-2026-10-01.md`, `gemeinde-achsen-entscheidungen-2026-10-01.md`. Punkt 1 (Rohbogen), beantwortet am selben Tag: Gundelfingen fiel bei Karte 3 und 10 nicht. Die Vermutung aus B3 Nr. 2 (Wiedererkennen) ist damit nicht gestützt, aber auch nicht widerlegt; Folge in Spielkonzept v0.2.5 §8 Nr. 2.

*Ende Prüfbericht.*
