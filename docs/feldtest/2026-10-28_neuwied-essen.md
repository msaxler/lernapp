# Feldtest 28.10.2026: Neuwied – Essen – Neuwied (Auto, geplante Route, vorgelesen)

Drei Protokolle (Hinfahrt 13:18–14:42, Stück Velbert–Heisingen 14:46–14:56, Rückfahrt 17:36–19:08), dazu Mikes Notizen vom Abend.
Erste echte Fahrt mit der geplanten Route (v58) und mit den 35 Orten der Autostrecke (27.10.).

## Zahlen
- **Hinfahrt:** 146,6 km Route, 84 min, 56 Fragen (26 richtig), 26 Orte gespielt, 9× „Jetzt“ von Hand. Ausgefallen: Altwied, Dierdorf,
  Melsbach, Hardert, Bonefeld, Straßenhaus, Willroth, Krunkel, Solingen, Mettmann – alle im Westerwald-Pulk oder beim Ortswechsel
  im Minutentakt. Grundversorgung (Dernbach, Linkenbach) per „Jetzt“ gespielt, viele Grund-Orte verfielen.
- **Rückfahrt:** 147,7 km, 92 min, 61 Fragen, Leverkusen allein 9 (zweimal „Noch mehr“). Beim Start in Essen fielen in einer Minute
  13 Essener Stadtteile aus (siehe GPS-Ausreißer). Am Ziel Neuwied wurden sechs Orte zugleich fällig (Stand-Radius 2 km) →
  fünfmal „Gleich“ hintereinander.
- Antwortzeiten meist 15–45 s; Hilden 7 116 s, Kurtscheid 1 334 s (Fahrsituation).

## Befunde aus den Protokollen (Fehler, nicht Wünsche)
1. **GPS-Ausreißer:** Rückfahrt t=32–42: Fix 5 km entfernt mit 819 km/h und Genauigkeit 354 m. Dadurch „passiert“ für alle Essener
   Orte auf einen Schlag. → Fixe mit Genauigkeit > 50 m oder Sprung > 70 m/s verwerfen.
2. **Stau am Ziel:** im Stand werden alle Orte im 2-km-Radius fällig, einer nach dem anderen. → Im Stand nur der nächste; nach
   „Fahrt abschließen“ nichts mehr; „Gleich“ auf einen Ort verschiebt die anderen mit.
3. **Kein Weg zur Fahrtkarte** aus Frage und Auflösung heraus außer „Gleich“ (das verschiebt). Mike: „scheint mir nicht immer möglich“.
4. Pulk-Orte (Westerwald, Essen-Stadtteile) verfallen nach 60 s Nachlauf, während noch eine Frage läuft. → siehe Wunsch B4/B5.

## Mikes Wünsche, geordnet
**A Inhalt**
- A1 Landkreis-, Kennzeichen- und Wahl-Klassiker überschneiden sich zwischen Gemeinden desselben Kreises. → je Fahrt nur einmal je Kreis.
- A2 Wahlergebnis: Plätze 1, 2, 3 mit Prozentzahlen nennen.
- A3 Fläche und Dichte sind als Zahl nicht anschaulich → Vergleich („so dicht besiedelt wie München“) statt Zahl; sonst weglassen.
- A4 Namensherkunft gezielt suchen („warum heißt der Königsforst Königsforst“) – für Ortsnamen und für Dinge im Ortsporträt;
  eigener Suchlauf über die gesammelten Orte (Modellkosten).
- A5 Das Ortsporträt enthält mehr Stoff als Fragen; Stoff darf auch nur vorgelesen/gezeigt werden (→ C1).

**B Ablauf**
- B1 Nach der Auflösung wählen: weitere Frage zu diesem Ort **oder** erste Frage des nächsten Orts (Orte kommen zügig).
- B2 Bei „daneben“ die richtige Antwort kurz wiederholen (man hat nur den eigenen Tipp im Kopf).
- B3 Tipp = festlegen (Schalter „sofort festlegen“); „Festlegen“ war zu 99 % überflüssig.
- B4 Orte in der Nähe kommen automatisch und dürfen den laufenden Ort unterbrechen, mit Rückfrage.
- B5 Jederzeit zur Fahrtkarte; Ort auf der Karte antippen zum Nachhören oder Nachspielen (auch ausgelassene).
- B6 Vorlesetext aufbereiten: Zahlen und Abkürzungen ausschreiben („1.“ → „erster“), Aussprache deutsch (Devon).

**C Modi**
- C1 **Reiseführer-Modus:** keine Frage, sondern beim Erreichen die Geschichte vorlesen (zu Fuß, Bahn, Auto). Mike: „am leichtesten
  erreichbar mit dem größten Effekt bis zum 5.11.“
- C2 **Duell-Modus:** zwei Tippspalten A und B je Antwort, Ort geht an den, der richtig liegt, bei Gleichstand an den Schnelleren.
- Quiz-Modus bleibt.

**Korrektur Mike (28.10. abends):** Das fünffache „Gleich“ am Ziel war kein Stand-Problem – er wollte die Fahrt beenden und hatte aus
der Frage heraus keinen Knopf dafür. → Befund 2 und 3 fallen zusammen: ein Weg zur Fahrtkarte (und damit zu „Fahrt abschließen“)
aus jedem Bildschirm, mit kurzer Ruhe vor neuen Pushs.

**Schritt 1 gebaut 28.10. (Artifact v71):** GPS-Filter (Genauigkeit > 50 m oder Sprung > 70 m/s verworfen, Zahl im Protokoll
`gps_verworfen`), Knopf „Karte“ auf Frage und Auflösung (30 s Push-Ruhe, Ereignis `karte`), Startwahl „Tippen: Tipp zählt sofort“
(Standard an; Protokoll `tipp_sofort`), bei „daneben“ die richtige Antwort im Wortlaut im Urteil-Chip (wird mit vorgelesen).
Mike hat Schritte 1–3 freigegeben.

**Schritt 2 gebaut 28.10. (Artifact v72):** Nach der Auflösung immer zwei Knöpfe – „Noch eine zu <Ort>“ (im Dreierblock Hauptknopf,
„2 von 3“) und „Weiter: <Ort> ist in Sicht“ bzw. „Zur Fahrtkarte“. Jeder Ort der Fahrtkarte ist antippbar: freie Karte → spielen
(Ereignis `jetzt`/`nachschlag`), keine mehr → Steckbrief vorlesen (`nachhoeren`). Unterbrechung: wartet während einer Frage ein
Geschichten-Ort, zeigt die Kopfzeile „Ort in Sicht: X – antippen zum Wechseln“ (einmal Ton/Vibration, keine Sprache, weil die
Frage sonst abbräche); Antippen stellt die laufende Frage zurück wie „Gleich“ (Ereignis `wechsel`). Grundversorgung unterbricht nie.

**Schritt 3 gebaut 28.10. (Artifact v73):** Startwahl „Spielart: Quiz / Reiseführer“. Im Reiseführer erzählt `erzaehlen()` beim
Erreichen statt zu fragen: beim ersten Mal der Steckbrief, dann die Geschichten der besten Karten nach Rang (zu Fuß eine je Punkt,
im Auto zwei je Ort, „Noch eine zu …“ für mehr), jede mit dem Charakteristikum als Überschrift. `erzaehltext()` kürzt die
Quiz-Rückseite regelbasiert: Tipp-Satz weg, bis zu zwei Quiz-Sätze am Anfang weg (`QUIZSATZ`: „läge nahe“, „klingt“, „tippt“,
„denkt man“ …), Gegensatzwort im ersten Satz weg („kommt aber von“ → „kommt von“), Zahlen mit Punkt bleiben ganz. Messung über die
1.207 Rang-Karten: 959 gekürzt, 8 noch quizhaft (Scratchpad `erz_check.js`). Gespielte Karten gelten als gespielt (Status
`erzaehlt`, Protokoll `modus`). Zweite Fassung später: eigener Erzähltext je Ort per Modell.

## Schätzung und Vorschlag der Reihenfolge (Mike entscheidet)
| Schritt | Inhalt | Zeilen | Bemerkung |
|---|---|---|---|
| 1 | Fehler 1–3 (GPS-Filter, Stau am Ziel, Knopf „Zur Fahrtkarte“) + B2 + B3 | ≈ 60 | ein Vormittag, danach Fahrt-Test |
| 2 | B1 (zwei Knöpfe nach der Auflösung) + B5 (Antippen, auch Nachhören) + B4 (Unterbrechung mit Rückfrage) | ≈ 80 | Ablauf, ein Tag |
| 3 | **C1 Reiseführer** regelbasiert: Ortsname, Steckbrief, Geschichte der besten Karten ohne Tipp-Sätze („Du hattest … getippt“, „… läge nahe“) | ≈ 120 | ein Tag; Erzähltext später per Modell je Ort schöner (eigener Lauf, ~0,3 USD/Ort) |
| 4 | B6 Vorlese-Lexikon + A1 Kreis-Dedupe + A2 Prozentplätze (Grundversorgung hat die Zahlen) | ≈ 70 | halber Tag |
| 5 | A4 Namensherkunft-Lauf (Modell, alle 505 Orte: Quelle Wikipedia-Abschnitt „Etymologie/Name“, sonst Suche Stufe 2) | Lauf | ≈ 1 USD/Ort geschätzt, erst Probe an 10 Orten |
| 6 | C2 Duell | ≈ 150 | nach dem 5.11.? |
| – | A3 Vergleichsanker für Dichte | später | braucht Ankerliste (Städte, Landkreise) |

Alles hinter Schaltern, die Auto-Logik bleibt; `index.html` wächst damit auf ≈ 1 800 Zeilen (Grenze 2 000 → danach aufteilen).
