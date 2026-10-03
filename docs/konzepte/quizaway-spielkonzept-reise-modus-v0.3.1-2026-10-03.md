# QuizAway — Spielkonzept Reise-Modus v0.3.1

**Story-Satz:**
*Ein Ort kommt näher. Das Spiel wirft eine Behauptung über ihn auf, die man sich zurechtlegen kann. Man legt sich fest, allein oder nach einer Diskussion im Auto, am Ende mit genau einem Urteil. Der Ort erzählt, was wirklich ist, nimmt die eigene Theorie mit und knüpft, wenn es sich lohnt, an einen Ort davor an. Der Reiseführer ist das Fundament; der Witz liegt im Zurechtlegen, und das geschieht im Kopf oder im Gespräch, nicht in der App.*

---

## Status-Block

| | |
|---|---|
| **Version** | v0.3.1: v0.3 plus Mikes Entscheide zu Anhang J (J1–J4 bestätigt, J5 Vorlesen, J6 Bingo als eigene Variante, J7 die übrigen Folgerungen bestätigt). v0.3 war der Neustart der Mechanik (Mike, 2026-10-03). Ersetzt v0.2.9 in §1 bis §7 und §9 bis §11. Die Inhaltsregeln aus v0.2.9 §8 gelten weiter, verdichtet in §8; neu ist dort die Quellen- und Prüfregel (§8 Nr. 9). Die Rulings der Runden 3 bis I stehen in v0.2 und v0.2.9 und werden hier nicht wiederholt. |
| **Datum** | 2026-10-03 |
| **Status** | Grundlage für den Umbau des Fahrt-Prototyps und für den Feldtest im Auto und in der Bahn. Keine Implementierungsfreigabe; die kommt nach dem Feldtest (§11). |
| **Scope** | Spielmechanik des Reise-Modus für alle Situationen (Auto, Bahn, Sofa), drei Streckenquellen, das wandernde Zielfenster. Fern-Duell nicht Gegenstand. |
| **Provenance** | v0.2 bis v0.2.9 (Runde 4, Feldtest Solo, PC-Prüfungen, drei Volllauf-Runden, zweiter Raum, Prototyp, Kosten-Pareto) → Neustart Mike 2026-10-03 (Anhang J) → v0.3. |
| **Entschieden (Mike)** | Ein Gerät. Ein Urteil je Frage, in jeder Situation (neu). Push bei echter Fahrt, mit „Gleich“ und „Jetzt“, in Auto **und** Bahn (neu). Wanderndes Zielfenster um die Position (neu). Geschichten aus Gemeinde-Webseite und Landesportal statt aus Wikipedia (neu). Schalter „Vorlesen“: in v1 liest ein Mensch, Ziel ist auch Sprachausgabe der App (J5). Bingo als eigene Spielvariante, zurückgestellt (J6). |
| **Offen** | Startwerte des Zielfensters (§1a) misst der Feldtest. Landesportal außerhalb Baden-Württembergs (§8 Nr. 9). |

**TL;DR gegenüber v0.2.9:** Es gibt keine Präsentationsmodi mehr. Die App kennt nur ein Spielmodell: eine Frage, ein Urteil, eine Auflösung. Ob vorher eine Person nachgedacht oder vier gestritten haben, sieht die App nicht und muss es nicht sehen. Damit fallen weg: einstimmig, gespalten und zersplittert, Mehrfachauswahl, der Knopf „uneinig“, der eingeschränkte Zwei-Personen-Modus, der Rollenwechsel, Wer-glaubt-wem als Funktion und die Spaltungen in der Bilanz. „Kein Solo im Auto“ ist aufgehoben. Was eine Situation von der anderen unterscheidet, sind nur noch zwei Schalter, die das Urteil nicht berühren: die **Streckenquelle** (echte Fahrt → Push, sonst Pull) und **Vorlesen** (eine Person liest anderen vor → kürzere Darstellung). Neu ist das **wandernde Zielfenster**: Orte laufen vorne ein und hinten aus, die App spielt aus dem, was gerade drin ist. Auf der Inhaltsseite werden Geschichten künftig aus Gemeinde-Webseite und Landesportal gezogen; der Faktencheck wird dadurch für die meisten Fakten zum Abgleich mit dem Quelltext ohne Netzsuche.

---

## 1. Der Core-Loop

Fünf Schritte, in jeder Situation gleich.

**1. Auslöser.** Ein Ort wird zum nächsten Spielort, bestimmt durch das Zielfenster (§1a). Bei echter Fahrt drängt sich die Frage auf (**Push**): Sie erscheint von selbst, mit einem kurzen Hinweis (Ton oder Vibration; in der Bahn leise, weil das Gerät oft in der Tasche ist). Bei geplanter oder gewürfelter Strecke wartet sie (**Pull**), bis jemand tippt. Zwei Korrektur-Taps gelten bei Push in jeder Situation:
- **„Gleich“** stellt die anstehende Frage einmal hinten an (Kurve, Baustelle, Gespräch, Umsteigen). Der Ort bleibt spielbar, solange er im Nachlauf des Fensters ist.
- **„Jetzt“** startet den nächsten Ort der Vorschau sofort, wenn das Schild oder der Bahnhof schon da ist und das GPS hinterherhinkt (Tunnel, Einschnitt, Funkloch).

Die App muss nicht wissen, wann das Schild kommt; sie muss bereit sein, wenn jemand es sagt.

**2. Behauptung aufwerfen.** Frage oder Aussage über den Ort mit zwei bis vier Optionen. **Qualitätsregel:** Jede Option ist als eigenständige plausible Theorie formulierbar („Der Name kommt vom Bach“, nicht „wegen eines Flusses“). **Redaktionsregel, verbindlich für jede Karte:** Frage ≤ 25 Wörter, Option ≤ 8 Wörter, Vorlesezeit ≤ 20 Sekunden, Auflösung ≤ 70 Wörter einschließlich Anschluss (Karte ≤ 60, Anschluss ≤ 10). Jede Karte muss vorlesbar sein, auch wenn sie still gelesen wird. **Beschriftung:** Ziffern 1–4; vorgelesen und gerufen wird „zwo“. **Varianzregel:** nicht zweimal hintereinander dieselbe Fragefamilie, nicht zweimal derselbe Fakten-Typ (abgelesen an der Bindung Karte → Fakt, §8 Nr. 8).

**3. Theorie bilden und festlegen.** Ein Urteil je Frage. Ein Tap wählt eine Option, „Festlegen“ löst auf; bis dahin lässt sich die Wahl ändern (Mike, 2026-10-01). Im Auto tippt, wer das Gerät hält, nachdem die Runde sich geeinigt hat; wie sie sich einigt (Zuruf auf „3-2-1“, Mehrheit, Diskussion), ist ihre Sache und nicht Teil der App. Begründen ist Angebot, nie Pflicht.

**4. Auflösung.** (a) Das Urteil wird aufgegriffen: richtig oder falsch, zwei Fälle. (b) Die Geschichte des Orts wird erzählt und webt die gewählte Theorie ein; drei bis vier Einwebungs-Muster rotieren, die Theorie wird auch mal ernst genommen. (c) Das Urteil wird nach der Erklärung eindeutig und nicht nachgeschoben, wenn die Geschichte es schon gesagt hat. (d) **Anschluss:** höchstens einer, an den letzten tatsächlich gespielten Ort, nur wenn der Zusammenhang eigenständig interessant ist; kein Fallback; Beobachtung, nie neue Frage. Quelle sichtbar.
**Die Auflösung ist für alle so pointiert, wie sie bisher nur solo sein musste.** Sie ist die Belohnung; ein Gespräch im Auto kommt dazu, ersetzt sie aber nicht.

**5. Nachhall.** Der Ort wandert auf die Fahrtkarte. Kein „Weiter“ innerhalb von Frage und Auflösung. Nach der dritten Frage eines Orts fragt das Spiel „Noch mehr zu diesem Ort?“ (§5). Nachschlag zu einem früheren Ort nur durch Tippen auf seinen Pin, nie automatisch.

**Was der Loop nicht hat:** Zeitdruck als Spannung, Punkte je Frage, Rangliste, Leben, Streaks, Statistiken als Belohnung.

### 1a. Streckenquelle und Zielfenster

| Quelle | Wie | Takt | Wofür |
|---|---|---|---|
| **Echte Fahrt** | GPS, Zielfenster um die Position | Push | Auto, Bahn |
| **Geplante Route** | Streckenliste (Kartenroute, Bahnverbindung); ein Positionspunkt wandert per Tap oder Zeittakt | Pull | Bahn ohne GPS, Vorbereitung, Nachspielen |
| **Gewürfelte Strecke** | x Orte aus einem Raum, zu einer Strecke verbunden | Pull | Sofa, Wartezimmer, Feldtest |

**Das Zielfenster (neu, Mike 2026-10-03).** Um die aktuelle Position liegt ein Fenster, das mitfährt. Orte mit Material laufen vorne ein und hinten aus; die App wählt immer aus dem, was gerade im Fenster liegt. Das gilt für Auto und Bahn gleich. Das Fenster ist **in Fahrzeit bemessen, nicht in Kilometern**, weil die Geschwindigkeiten zu verschieden sind: Eine Bahn mit 200 km/h ist in einer Minute an einem Dorf vorbei, ein Auto in der Ortsdurchfahrt braucht fünf.

| Teil | Startwert (Hypothese) | Wozu |
|---|---|---|
| **Vorschau** (voraus) | was in den nächsten **3 Minuten** erreicht wird | Namen der kommenden Orte zeigen; „Jetzt“ greift hierauf |
| **Auslösepunkt** | **30 Sekunden** Fahrzeit vor dem nächsten Vorbeikommen | hier erscheint die Push-Frage |
| **Nachlauf** (hinten) | **1 Minute** nach dem Vorbeikommen | so lange darf ein verpasster oder verschobener Ort noch starten |
| **Korridor** (seitlich) | **5 km** | Orte neben der Linie, die man sieht, aber nicht durchfährt (in der Bahn häufig) |
| **Stillstand** | unter 10 km/h: festes Fenster von 2 km | Stau, Bahnhof, Pause |

Die Werte sind geschätzt; der Feldtest im Auto und in der Bahn stellt sie ein (§10).

**Welcher Ort drankommt.**
- Vorrang hat der nächste ungespielte Ort **auf der Strecke** (Abstand zur Linie höchstens 1 km). Orte im übrigen Korridor kommen nur dran, wenn auf der Strecke im Fenster keiner liegt. Sie tragen den Vermerk „aus der Nähe“; das ersetzt die bisherige Sonderregel für ortsarme Abschnitte.
- **Eine laufende Frage wird nie abgebrochen.** Erreicht ein neuer Ort seinen Auslösepunkt, während eine Frage läuft, wartet er, bis sie aufgelöst ist.
- **Ein Ort spielt seine drei Fragen, bis der nächste Ort ansteht.** Steht er an, endet der laufende Ort nach der aktuellen Frage; „Noch mehr zu diesem Ort?“ wird dann nicht angeboten. Ungespielte Karten bleiben im Vorrat.
- **Ein Ort, der den Nachlauf verlässt, ohne gestartet zu sein, fällt still aus.** Er bekommt auf der Fahrtkarte einen blassen Pin „passiert“, über den man ihn nachspielen kann. Rauscht in der Bahn eine Kette kleiner Orte vorbei, kommt eben nur jeder zweite dran; das Fenster wählt von selbst aus.
- Bei Pull wandert der Positionspunkt mit jedem Weiterschalten; Fenster und Regeln sind dieselben, nur ohne Auslösepunkt.

**Weitere Regeln.**
- Die Quelle liefert nur Orte **mit Material**; ein Ort ohne Material wird still übersprungen. Intern zählen zwei Größen: Orte im Fenster gewesen, Orte gespielt.
- **Vorladen:** Unabhängig vom Spielfenster lädt die App den Vorrat der nächsten rund 30 Minuten Strecke vorab, damit Funklöcher (in der Bahn häufig) das Spiel nicht anhalten.
- **GPS-Verlust:** Wechsel auf geplante Route mit einem Tap; die Fahrtkarte läuft weiter. „Jetzt“ überbrückt kurze Ausfälle.
- Keine Ortsschilderkennung, keine Kamera.
- **Folge für die Inhaltsseite:** Das Fenster legt fest, für welche Orte überhaupt Karten gebraucht werden, nämlich nur für Orte im Korridor wirklich gefahrener Strecken (Kosten-Pareto, Hebel H1).

---

## 2. Die drei Fragefamilien und ein Ablaufmodifikator

Alle Familien sind „ein Tap, zwei bis vier Optionen“; die Leiter ist eine Folge solcher Taps. Schicht 0 ist deterministisch ableitbar (Zahlen, Lage, Zugehörigkeit), Schicht 1 aus Text extrahiert (Geschichten, Namensherkunft).

| Familie | Form | Datenquelle | Einsatz |
|---|---|---|---|
| **A — Behauptung** | Frage, bis zu vier Theorien als Optionen | Schicht 1, bei Klassikern Schicht 0; Distraktoren mit Negativnachweis (§8 Nr. 1) | Standard |
| **B — Lüge** | drei Aussagen, eine gelogen; **beim Vorlesen zwei** („Eine der beiden stimmt nicht“) | ≥ 2 belastbare Schicht-1-Fakten; Lüge mit Negativnachweis | nur wo Daten reichen, sonst A; Aussagen ≤ 8 Wörter, formgleich |
| **C — Größenordnung** | Zahlenfrage ohne Zahlen: Epochen, Spannen | Schicht 0; Zahl aus dem Text nur mit Anhalt im Steckbrief | höchstens jede dritte Frage, nie zwei hintereinander |

**Radar** ist Familie A mit Nachbarorten als Optionen. **Mit Display** auf einer schematischen Karte (nummerierte Punkte). **Beim Vorlesen** relativ zur Fahrt, nie mit Himmelsrichtungen: „Auf eurer Strecke, 4 km vor euch: X. Weiter, 15 km: Y. Welcher hat ein Freibad?“ Das Zielfenster liefert die Nachbarn und ihre Entfernungen. Die Auflösung kehrt zum aktuellen Ort zurück; die richtige Option ist nicht immer der aktuelle Ort (sonst gewinnt „der nächste Ort auf der Vorschau“). Radar beim Vorlesen fällt nicht unter die Wortzahl-Regel; Startwert drei Orte.

**Leiter** ist ein Ablaufmodifikator über Familie C: mindestens drei Stufen („Höher als 400 m? Höher als 600 m? …“), unter 60 Sekunden, höchstens jede zweite C-Frage. Je Stufe zwei Antworten, „höher“ oder „hier steige ich aus“ (gerufen: „raus“); der Ausstieg ist das Urteil. Kein Stopp, keine Bank, kein Einsatz. **Neu:** Die Leiter steht in jeder Situation zur Verfügung; die Sperre für zwei Personen im Auto entfällt mit dem Zwei-Personen-Modus. Kipp K6 bleibt.

---

## 3. Ein Spielmodell, zwei Schalter

Es gibt keine Präsentationsmodi mehr. Was sich zwischen Sofa, Bahn und Auto unterscheidet, sind zwei Schalter. Keiner berührt Frage, Urteil oder Auflösung.

**Schalter 1 — Streckenquelle** (§1a): echte Fahrt → Push mit „Gleich“ und „Jetzt“; geplante oder gewürfelte Strecke → Pull. Die App setzt ihn aus der gewählten Quelle; es gibt keine eigene Frage danach.

**Schalter 2 — Vorlesen** (beim Start, jederzeit umschaltbar; Mike, 2026-10-03: „Schalter ist gut“): Eine Person liest anderen vor (typisch: Beifahrer im Auto). **Wer vorliest (J5):** In v1 ein Mensch vom Bildschirm. Ziel ist, dass auch die App selbst vorlesen kann (Sprachausgabe des Geräts), wahlweise neben dem Menschen; das kommt nach v1. **Zwei Pflichten in beiden Fällen (Mike):** Der Originaltext steht beim Vorlesen immer lesbar auf dem Bildschirm, und das Vorgelesene lässt sich wiederholen. In v1 heißt das: Frage und Optionen bleiben stehen, bis aufgelöst ist, nichts blendet sich nach dem Vorlesen aus; mit Sprachausgabe kommt eine Taste „Nochmal“ dazu. Wirkung des Schalters nur auf die Darstellung:
- Familie B mit zwei statt drei Aussagen
- Radar verbal statt auf der Karte
- feste große Schrift (Vorlesegröße), kein Scrollen
- die Vorschau der kommenden Ortsnamen bleibt; sie verrät keine Lösung (Radar-Lösungsregel, §2)

Ohne Vorlesen liest jede Person selbst, die Schrift wächst mit, B hat drei Aussagen, Radar zeigt die Karte.

*Folgerung ohne eigenen Entscheid:* Der Schalter „Vorlesen“ ist der Rest der alten Modus-Wahl. Er ist nötig, weil drei Aussagen vorgelesen im Fahrgeräusch nicht zu behalten sind (v0.2.2) und eine Karte im Auto nicht auf Augenhöhe der Mitfahrenden liegt. Er verändert keine Karte, nur ihre Darstellung; jede Karte ist in beiden Stellungen spielbar.

**Fahrer-Ausschluss:** Die fahrende Person bedient nichts und blickt nicht aufs Gerät. Ohne Ausnahme. Wer allein im Auto fährt, spielt nicht; das ist eine Grenze, solange es kein TTS mit Spracheingabe gibt (§6).

**Quelle des Moments.** Die tragende Säule ist in jeder Situation die Auflösung, die die eigene Theorie aufnimmt und eine Geschichte erzählt. In der Gruppe kommt das Gespräch dazu: das Streiten vor dem Tap, das Lachen danach. Das entsteht ohne die App und wird von ihr weder gezählt noch abgebildet. Gruppen, die es wollen, können weiter laut reihum tippen lassen oder „Wer glaubt wem?“ spielen; die App braucht dafür keine Funktion.

**Was ein Schalter nicht darf:** einen eigenen Fragetyp einführen, die Auflösung verändern, Punkte je Frage zeigen, eine Karte verlangen, die in der anderen Stellung nicht spielbar wäre.

---

## 4. Rahmen und Fahrtende

Rahmen verändern den Core-Loop nicht.

**Fahrtkarte.** Schematische Streckenlinie; ein Pin je gespieltem Ort (Name, ein Satz Steckbrief, Ergebnis als Farbe), ein blasser Pin je passiertem, nicht gespieltem Ort. Nachschlag durch Tippen auf einen Pin.

**Fahrtende (eigener Schritt).** Durch einen Tap „Fahrt abschließen“ oder am Streckenende bei Pull. Dann:
1. **Fahrtbilanz:** „Neuwied–Kassel: 14 Orte, 38 Fragen, 24 richtig.“ Nur erfasste Ereignisse. Seit drei Fragen je Ort gespielt werden, zählt die Bilanz Fragen, nicht Orte. Die Zahl ist kein Wettkampf-Score (nie je Frage angezeigt, keine Rangliste, keine Einordnung); der Feldtest fragt, ob sie als Druck wirkt, und wenn ja, fällt sie.
2. **Ort der Fahrt** (optional, für alle): ein Pin, der den Moment der Fahrt markiert, ein Tap, keine Begründung.
3. **„Drei Dinge, die ich nicht wusste“** (optional, für alle): aus den gespielten Auflösungen, teilbar als Bild.
4. Optional **Große Fahrtfrage** als Leiter über die gespielten Orte.
5. Bild-Export.

Eine Fahrt, die nicht abgeschlossen wird, kann später fortgesetzt werden.

---

## 5. Taktung (Hypothesen)

- **Drei Fragen je Ort, dann „Noch mehr zu diesem Ort?“** für je drei weitere, solange der Vorrat reicht (Mike, 2026-10-03). Das Angebot entfällt, wenn der nächste Ort schon ansteht (§1a). Bei Pull kommt es immer.
- Varianzregel auch innerhalb der drei Fragen eines Orts.
- Familie C höchstens jede dritte Frage, nie zwei hintereinander; Leiter höchstens jede zweite C-Frage; Radar höchstens jede zweite Frage.
- Anschluss nur bei eigenständig interessantem Zusammenhang; keine Quote, kein Fallback.
- **Zeitbudget je Frage:** beim Vorlesen ≤ 60 Sekunden, sonst frei. Drei Fragen dauern damit beim Vorlesen bis zu drei Minuten; die Vorschau von drei Minuten (§1a) ist darauf abgestimmt.
- Mikro-Feedback erlaubt („Ort 4“, „Frage 2 von 3“).

---

## 6. Anti-Rucksack

Nicht in v1: Ortsschilderkennung, Kamera; Sprachausgabe (Ziel nach v1, J5) und Spracheingabe (dann auch für Alleinfahrende); Mehrheits-Balken und jede Prozentstatistik; p2p oder zweites Gerät; Erfassung einzelner Stimmen in der Gruppe (gespalten, uneinig, Wer-glaubt-wem); Fenster-Detektiv als Pflicht; Lokal-Rätsel; Team-Schätzung mit Rechnen; Kartenkacheln; Badges, Level, Achievements, Streaks; automatischer Nachschlag; Fallback-Anschluss.

**Bingo als eigene Spielvariante, zurückgestellt (J6; Mike, 2026-10-03):** „Bingo funktioniert immer! Sollte einfach als Spielvariante gewählt werden können.“ Bingo ist damit kein Füller für ortsarme Strecken mehr (so bis v0.2.9), sondern eine eigene Variante, beim Start **statt** des Reise-Quiz wählbar, auf jeder Strecke und in jeder Situation. Nebenher zum Quiz läuft es nicht, weil es die Aufmerksamkeit von der Frage abzöge. Gebaut wird es erst, wenn die Hauptanwendung trägt („zurückgestellt, bis die Hauptanwendung OK ist“). Felder bleiben Eigenschaften mit Schwellwert aus Schicht 0, automatisch prüfbar.

---

## 7. Kipp-Kriterien

- **K1 — Kernversprechen (dreiteilig):** Nach der Auflösung kann die Person (1) ihre Theorie nennen, (2) den tatsächlichen Grund nennen, (3) sagen, warum ihre Theorie plausibel oder falsch war. Fehlt (3) regelmäßig, trägt der Kern nicht. Die drei Teile werden getrennt protokolliert.
- **K2 — Schnitt:** Eine Karte ist nur in einer Stellung des Schalters „Vorlesen“ spielbar.
- **K3a — Abbruch:** An natürlichen Pausen wird abgebrochen statt weitergespielt; ab zwei Abbrüchen vor dem geplanten Ende. Nur auf echter Fahrt messbar.
- **K3b — Durchtippen:** Vor der Auflösung wird keine konkrete Theorie mehr gebildet (T2, §10). Gewusst (W) zählt nicht dagegen; ein Glückstreffer ist erwünscht.
- **K4 — Vorleser:** Die vorlesende Person spielt nach fünf Orten nicht mehr mit, sondern liest nur noch.
- **K5 — Fenster (neu gefasst):** Push-Fragen kommen regelmäßig zu spät (Ort schon vorbei) oder zu früh (Ort noch nicht in Sicht), oder mehr als rund ein Drittel der Orte im Fenster fällt aus, obwohl Material da war, oder Abschnitte wirken leer, obwohl Orte im Korridor lagen.
- **K6 — Leiter:** Leiter-Urteile werden nie begründet.
- **K7 — Anschluss:** Anschlüsse wirken aufgesetzt oder erzeugen Nachfragen, die eine zweite Frage erwarten.
- **K8 — Push in der Bahn (neu):** Der Hinweis stört (wird abgeschaltet oder mit „Gleich“ weggedrückt) häufiger, als er angenommen wird.

---

## 8. Schnittstelle zu den Inhalten

Die Inhaltsregeln aus v0.2.9 §8 Nr. 1 bis 8 und §8a gelten unverändert, mit zwei Anpassungen an das neue Spielmodell (Nr. 5) und an die neuen Quellen (Nr. 8, Nr. 9). Hier die Kurzfassung; Begründungen, Befunde und Beispiele stehen in v0.2.9.

1. **Negativnachweis Distraktoren (A):** Eine falsche Option muss falsch sein. Wege: (a) harter Negativnachweis, (b) Kontext-Spiegel (wahrer Fakt eines Orts 50–100 km entfernt, nur bei einwertiger Eigenschaft mit anderem Wert oder vollständiger Quelle; Spender kein Ort der Fahrt), (c) erfundene Theorie gegen einen belegten einwertigen Fakt, erst nach Freigabe durch den Faktencheck.
2. **Negativnachweis Lüge (B):** Lüge widerlegt oder eindeutig einem anderen Ort zugeordnet; Formgleichheit (Länge, Detail, Auffälligkeit unabhängig von der Wahrheit, Stelle wechselt, kein Widerspruch zur Vorderseite).
3. **Theorie-Formulierung:** jede Option als Theorie.
4. **Anschluss:** (a) Vergleichsanschluss aus Grunddaten, generierbar; (b) Erzählanschluss und (c) Namensteil-Anschluss als Kann-Klassen. Höchstens einer, kein Fallback. Der Anschluss hängt am Ortspaar, nicht an der Karte.
5. **Reveal-Vertrag (vereinfacht in v0.3):** Eingabe ist **genau eine gewählte Option** (bei der Leiter: die Stufe des Ausstiegs) und optional ein Anschluss-Ort. Zwei Template-Fälle: richtig, falsch. Die Fälle „gespalten“ und „zersplittert“ und der Optionssatz entfallen.
6. **Bekanntheit:** Ein bekannter Fakt darf die Frage tragen; die Frage zielt auf ein Detail. W wird gemessen, nicht gesperrt.
7. **Vorrat je Ort:** mindestens sieben Karten, vorläufig höchstens zwanzig; Geschichten und Klassiker (Grunddaten, Politik nur als Gesamtergebnis Urne + Brief, Ausreißer, Seltenheit); verschiedene Klassiker von Ort zu Ort; Kennzeichen nicht einwertig; Höhe nur bei einigen Quellen; zeitabhängige Angaben mit Stand; keine Wappen-Karten; eine neue Familie zuerst als Probe von drei bis fünf Karten an Mike; ein gerechneter Rekord nur, wenn der Wert erstaunt.
8. **Faktencheck und Bindung an den Fakt:** Keine Karte ohne Faktencheck in den Vorrat; die Sachprüfung liegt bei der Maschine, beim Kurator Geschmack und Theorie-Gefühl. Befunde hängen am Fakt, jede Karte ist an ihren Fakt gebunden. Vier Urteile: bestätigt, korrigiert, unsicher, gesperrt. **Geändert in v0.3:** *Wie* geprüft wird, regelt die Prüfstufe aus Nr. 9; die bisherige Pflicht zur zweiten Quelle im Netz gilt nur noch für Stufe 2.
9. **Quellen und Prüfstufen (neu in v0.3; Mike, 2026-10-03).**
   - **Hauptquelle für Geschichten** sind die eigene Webseite der Gemeinde und das Landesportal für Landeskunde, nicht mehr Wikipedia. Wikipedia bleibt Ergänzung und Wegweiser. Begründung aus dem Faktencheck der ersten 100 Karten (v0.2.9 §8 Nr. 8): Rund 15 Fehler standen schon im Wikipedia-Artikel; die Gemeinde hat mehrfach berichtigt (Wildtal 72 % statt „Dreiviertelmehrheit“, Denzlinger Störche seit 1993 statt 1983, Staufens Brücke „eine der wenigen“ statt „letzte“).
   - **Vertrauenswürdige Quellen** (vorläufige Liste): eigene Webseite der Gemeinde (amtliche Domain mit Impressum der Gemeinde oder Verbandsgemeinde; nicht automatisch Tourismusvereine), Landesportal (Baden-Württemberg: LEO-BW), Landesarchive, amtliche Statistik und Wahlleitungen. Die Liste wird um die Quellen ergänzt, die sich in den bisherigen Faktenchecks bewährt haben; ausgezählt wird das aus den Urteilen, nicht aus dem Gedächtnis (§11 Nr. 2). Lokale Quellen, die Mike kennt, kommen dazu.
   - **Offen:** das Gegenstück zu LEO-BW in anderen Ländern. Für Rheinland-Pfalz liegt das landeskundliche Portal des Mainzer Instituts für geschichtliche Landeskunde nahe (regionalgeschichte.net); geprüft ist das nicht.
   - **Prüfstufen:**

     | Stufe | Wann | Prüfung | Kosten |
     |---|---|---|---|
     | 0 | Klassiker aus Grunddaten | Skript gegen die Grunddaten (wie Ausreißer und Seltenheit) | keine |
     | 1 | Fakt steht in einer vertrauenswürdigen Quelle | Abgleich der Karte mit dem Quelltext, **ohne Netzsuche**; fängt geglättete Vorbehalte, Extraktionsfehler und Tempusfehler | gering |
     | 2 | Fakt nur in Wikipedia oder einer anderen Quelle, **oder ein Superlativ** | Suche nach zweitem Beleg, nur in vertrauenswürdigen Quellen | mittel |
     | immer | erfundene falsche Optionen (Nr. 1c) und Lügen | Gegenprobe, ob sie nicht doch zutreffen | mittel |

   - **Zwei Grenzen der Glaubwürdigkeit.** Erstens hängt sie an der Art der Aussage: Die Gemeinde ist stark bei Zahlen, Gegenwart und Ortsgeschehen, schwach bei Superlativen und Sagen, wo Lokalstolz mitschreibt („älteste“, „einzige“, „der Sage nach“). Superlative gehen deshalb immer in Stufe 2, auch von der Gemeinde, und Vorbehalte der Quelle bleiben stehen. Zweitens fängt keine Quellenliste den teuersten Fehler: eine „falsche“ Option, die stimmt (sechs von 100 Karten, fünf davon erfundene Gründe). Diese Gegenprobe bleibt Pflicht.
   - **Vor der Umstellung: Gegenprobe ohne neue Läufe.** Die rund 90 Befunde der bisherigen Faktenchecks werden nachgespielt: Wie viele hätte die Stufenregel gefunden, wie viele wären durchgerutscht? Messlatte: Ein Faktencheck nur nach Risikomerkmalen fände 60 % der Befunde (Kosten-Pareto); die Stufenregel muss deutlich darüber liegen.

---

## 9. Berührungspunkte mit dem Transfer-Konzept v1.1

- **Antwortform (vereinfacht):** genau eine Option je Frage (`chosenIndex`), bei der Leiter eine Folge von Einzelantworten. Optionssatz und „uneinig“ entfallen.
- **Kipp-Kriterium v1.1 §2 bleibt ausgelöst, aber schwächer:** Abweichend von v1.1 sind die Optionszahl (zwei bis vier) und der fehlende Zeit-Score; die Antwortform selbst passt wieder. Das Schema wird in der PC-Session (§11) neu geschnitten.
- **Reveal-Vertrag:** Option plus optional Anschluss-Ort, zwei Template-Fälle.
- **Streckenquelle:** eigener Baustein vor dem Kern; liefert aus dem Zielfenster „nächster Ort mit Material“ und die Vorschau, führt zwei Zähler (im Fenster, gespielt), lädt vorab.
- **Push/Pull:** folgt aus der Streckenquelle, kein Modus. **Vorlesen:** ein Darstellungs-Flag.
- **Host-Screen:** „Gleich“ und „Jetzt“; Mehrfachauswahl und „uneinig“ entfallen.
- **elapsedMs:** vorhanden, nie angezeigt, nie gewertet.

---

## 10. Feldtest

**Content-Stufen** wie bisher getrennt: Stufe 1 handgeschrieben (Obergrenze, misst den Kern), Stufe 2 generiert (misst die Kette). Jede Karte trägt ihre Stufe und bei Anschluss ihre Klasse.

**Theorie-Klassifikation vor der Auflösung:** T0 keine Theorie, T1 Auswahl ohne Begründung, T2 konkrete Theorie mit Begründung, W gewusst oder wiedererkannt (mit Vermerk, woher). In der Gruppe stellt der Beobachter fest, ob aus der Diskussion T2 hervorgeht.

**Reihenfolge:** Tisch (Kartensätze Stufe 2, laufen weiter wie geplant) → Prototyp im Auto → Prototyp in der Bahn.

**Auto auf der Straße** (Prototyp, echte Fahrt, Push, Vorlesen an): möglichst zwei Besetzungen (zu zweit, zu dritt oder viert). Protokoll: Dauer von der Frage bis zum Tap (Diskussion), „Gleich“ und „Jetzt“, zu frühe und zu späte Push-Fragen (K5), ausgefallene Orte, Wiederholungen bei B, Leiter-Begründungen, Vorleser nach fünf Orten (K4), ob „Noch mehr“ angenommen wird, Kommentar zur Bilanz, abends Weitererzählen.

**Bahn** (neu als eigener Test; Prototyp, echte Fahrt, Push, Vorlesen aus): allein und zu zweit. Protokoll: Hinweis wahrgenommen oder störend (K8), Abbrüche an Pausen (K3a), GPS-Ausfälle und „Jetzt“, Orte aus dem Korridor („aus der Nähe“) als spielbar empfunden, Ketten vorbeirauschender Orte.

**Das Zielfenster wird hier eingestellt:** Der Prototyp schreibt je Ort Auslösezeit, Vorbeikommen, Start, Ende und Ausfall ins Protokoll. Daraus ergeben sich Vorschau, Auslösepunkt, Nachlauf und Korridor für v1.

**Übergreifende Frage:** Erzeugt eine eigene Theorie (T2) einen anderen Spielzustand als „ich möchte es wissen“ (T0/T1)? Macht die Auflösung aus der Theorie eine Geschichte (K1 Teil 3)?

---

## 11. Nächste Schritte

1. **Fahrt-Prototyp umbauen** (`apps/quizaway-reise/`): Moduswahl durch die Schalter Streckenquelle und Vorlesen ersetzen; gespalten und uneinig entfernen; Bilanz nach Fragen; Zielfenster mit GPS (echte Fahrt) und mit wanderndem Punkt (gewürfelte Strecke); „Gleich“ und „Jetzt“; Protokoll um die Fenster-Zeiten erweitern. Danach Artifact neu ausspielen.
2. **Gegenprobe zur Prüfstufen-Regel** (§8 Nr. 9) an den rund 90 Befunden der bisherigen Faktenchecks; daraus die Liste der bewährten Quellen.
3. **Probe Gemeinde-Webseite als Hauptquelle:** zwei bis drei Orte je Raum, Extraktion aus Gemeinde-Webseite und Landesportal statt Wikipedia, Karten, Prüfung nach Stufen; Vergleich mit den vorhandenen Karten (Qualität, Befunde, Token).
4. Probe H2 fortsetzen (Denktiefe, kleineres Modell) mit der neuen Eingabe aus Nr. 3.
5. Feldtest (§10) → Spielkonzept v1.0 → Implementierungsfreigabe → PC-Session gegen Transfer-Konzept v1.1.
6. **UI-Konzept** an v0.3 anpassen (Host-Screen ohne Mehrfachauswahl, Schalter Vorlesen, Pins „passiert“, Push-Hinweis in der Bahn).

### Wo der Mensch billiger ist als die Automatik

- **Fensterwerte:** nicht rechnen, sondern fahren. Zwei Fahrten mit dem Prototyp liefern die Startwerte genauer als jedes Modell.
- **Lokale Quellen:** Mike kennt für seine Räume vielleicht Ortschronik, Heimatverein oder Lokalzeitung. Ein Satz von ihm spart Suchläufe.
- **Gemeinde-Webseiten finden:** Die amtliche Adresse je Gemeinde steht in Wikidata und im Gemeindeverzeichnis; hier ist die Automatik billiger. Mike nur fragen, wenn eine Gemeinde keine eigene Seite hat.

---

**These:** Ein Reiseführer, der erst eine eigene Theorie verlangt und danach die Antwort erzählt. Ein Urteil je Frage, in jeder Situation gleich; die Orte kommen und gehen mit der Fahrt. Der Feldtest kann das widerlegen; dafür ist diese Fassung geschrieben.

---

## Anhang J — Neustart (Mike, 2026-10-03)

**J1. Alles als Solomodus.** Mike: Er würde „alles wie ein Solomodus behandeln, auch die Fahrt im Auto: die Diskussion zwischen den Teilnehmern führt letztlich zu genau einem Urteil und das unterscheidet sich nicht davon als hätte ein Einzelspieler auf den Knopf gedrückt“. → §1 Schritt 3 und 4, §3, §4, §8 Nr. 5, §9. Hebt „Kein Solo im Auto“ (Status-Block bis v0.2.9) und die Festlegungsfälle aus v0.2.2 auf.

**J2. Push bleibt, mit den Korrektur-Taps, auch in der Bahn.** Mike: „Push ist gut, beibehalten. mit den Korrekturtipps. Wichtig ist, dass das auf der Bahnfahrt auch funktioniert.“ → §1 Schritt 1, §1a, K8.

**J3. Wanderndes Zielfenster.** Mike: „wir brauchen ja dann ein Radius von dem Punkt aus, dem wir gerade auf der Fahrt sind. Bei beiden Bewegungen bedeutet das, dass es kontinuierlich laufende Ziele gibt und einzelne Ziele verschwinden, während andere neu auftauchen.“ → §1a. Bemessung in Fahrzeit und die Startwerte sind Vorschlag der PC-Seite (im Gespräch vorgestellt, von Mike mit „v0.3 schreiben“ angenommen); eingestellt werden sie im Feldtest.

**J4. Weniger Suchaufwand durch vertrauenswürdige Quellen.** Mike: Quellen, die sich in den Recherchen als glaubwürdig herausgestellt haben, und die eigenen Internetauftritte der Gemeinden als glaubwürdig markieren. Zum Vorschlag, die Geschichten gleich aus Gemeinde-Webseite und LEO-BW zu ziehen, sodass Stufe 1 der Normalfall wird: „genau“. → §8 Nr. 8 und 9.

**Bestätigt (Mike, 2026-10-03):** J1 bis J4 „OK“.

**J5. Vorlesen.** Der Schalter „Vorlesen“ als Rest der Moduswahl: „OK, Schalter ist gut. Wenn ja: Vorlesen soll wiederholt werden können, Originaltext muss auch beim Vorlesen zu lesen sein.“ Auf die Rückfrage, ob ein Mensch, die App oder beide vorlesen: „c), erste Version nur (a)“, also Ziel beides, in v1 nur der Mensch. → §3, §6.

**J6. Bingo.** Zur Folgerung „Bingo zurückgestellt“: „Bingo funktioniert immer! Sollte einfach als Spielvariante gewählt werden können.“ Auf die Rückfrage, ob statt des Quiz oder nebenher: „Bingo als eigene Variante, zurückgestellt, bis die Hauptanwendung OK ist.“ → §6.

**J7. Übrige Folgerungen bestätigt** („OK“): Leiter für alle (§2); Bilanz zählt Fragen (§4); Ort der Fahrt und „Drei Dinge“ für alle (§4); Wer-glaubt-wem nur noch mündlich ohne Funktion (§3); Superlative immer Prüfstufe 2 (§8 Nr. 9).

*Ende Spielkonzept v0.3.1.*
