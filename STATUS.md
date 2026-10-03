# STATUS — LernApp

**Stand:** 2026-10-02 (QuizAway-Abschnitt; übrige Abschnitte Stand 2026-05-09)
**Status:** Konzeptphase / vor LA-3-Implementation
**Repo:** github.com/msaxler/lernapp (privat)

---

## QuizAway Reise-Modus (wieder aufgenommen 2026-10-01)

**Ein Repo für alle Geräte, der PC führt (Mike, 2026-10-01).** Maßgeblich ist der Stand in diesem Repo (GitHub `msaxler/lernapp`, gespiegelt nach Drive `xcop/lernapp/`). Was am Handy entsteht, kommt als GEOSYNC-Datei an den PC und wird hier eingearbeitet. Versionsnummern der Konzepte vergibt der PC; am Handy bitte auf der hier genannten Fassung aufsetzen und keine eigene Folgeversion anlegen.

Alle Dokumente unter `docs/konzepte/`. Keine Implementierungsfreigabe; die kommt nach Feldtest Stufe 2.

- **Spielkonzept v0.2.8** `quizaway-spielkonzept-reise-modus-v0.2.8-2026-10-03.md` (maßgeblich; v0.2 bis v0.2.7 liegen daneben, Anhang A steht in v0.2). **Achtung für Mobile-Claude:** v0.2.4 bis v0.2.8 sind am PC entstanden. Nicht auf einer älteren Fassung weiterarbeiten; nächste Fassung ist v0.2.9. **Neu in v0.2.8 (Anhang H):** Briefwahl der Verbandsgemeinde – die Politik-Karte fragt dann nach der Verbandsgemeinde (Mike: „so lassen“); Stadtteilergebnis aus Stimmbezirken mit Gegenprobe; **Ausreißer-Karte** (ein Gebiet wählt anders als das übergeordnete; Schwellen von der PC-Seite: höchstens drei Gebiete derselben Ebene im Land, oder mindestens acht Prozentpunkte Abweichung; Erststimme ist nicht Mandat; Probe: Wahlkreis 281 Freiburg einer von zwei in BW mit den Grünen vorn, Waldbreitbach, Leutesdorf, Glottertal, Kirchzarten); keine Wappen-Karten; neue Fragenfamilie zuerst als Probe von drei bis fünf Karten an Mike. **Neu in v0.2.7 (Anhang G, Nachträge vom 2. Oktober):** Keine Karte kommt ohne Faktencheck in den Vorrat, die Sachprüfung liegt bei der Maschine (§8 Nr. 8, neu); die Befunde des Faktenchecks hängen am Fakt, jede Karte ist an ihren Fakt gebunden, „derselbe Fakt" ist eine Abfrage (§8 Nr. 8); sieben Karten je Ort sind die Untergrenze, Grenze vorläufig zwanzig; bei gleichem Fakt bleibt die jüngere Karte; Stadtteil mit eigenem Wahlergebnis; zweite Quelle bei dünnem Artikel; Höhe nur bei einigen Quellen; Kennzeichen nicht einwertig (alles §8 Nr. 7); Anschluss über einen Namensteil als Kann (§8 Nr. 4c). Aus v0.2.6 (Anhang F): Ein bekannter Fakt darf die Frage tragen, die Frage zielt dann auf ein Detail (§8 Nr. 6); jeder Ort hat einen Vorrat von mindestens sieben Karten aus Geschichten und Klassikern samt Politischem, gespielt wird weiter eine Frage je Ort (§8 Nr. 7); Familie C in der Regel aus Grunddaten, eine Zahl aus dem Artikel nur mit Anhalt im Steckbrief (Nachtrag Mike 02.10.); der Anschluss hängt am Ortspaar (Karte höchstens 60 Wörter, Anschluss höchstens 10).
- **Feldtest Stufe 1, Solo:** erste Person gelaufen (Kartensatz, Protokoll). 6 von 10 Karten mit begründeter Theorie; K1 und K3a nicht erhoben.
- **PC-Prüfung** `quizaway-spielkonzept-v0.2.3-pruefung-pc-2026-10-01.md` (B1–B10), Entscheide Mike „alle gemäß Vorschlägen" → v0.2.4 Anhang D.
- **Nächster Schritt Mike:** zweite Solo-Person mit **Kartensatz Fassung 2** `quizaway-feldtest-solo-kartensatz-freiburg-v2-2026-10-01.md` (Lügen der Karten 3 und 10 ersetzt, Kürzel W). Rohbogen der ersten Person: „Gundelfingen" fiel bei Karte 3 und 10 nicht; das Wiedererkennen bleibt eine unbelegte Vermutung (v0.2.5 §8 Nr. 2).
- **Stufe 2 (generierte Karten): zwei Vollläufe gelaufen.** Erster Lauf: Bericht `quizaway-stufe2-volllauf-2026-10-01.md` (V1–V10), Kuratierblatt `quizaway-stufe2-kuratierblatt-2026-10-01.md` (30 Vorschläge, je Ort drei). **Zweiter Lauf (Prompt v0.5, Vorrat):** Bericht `quizaway-stufe2-volllauf2-2026-10-01.md` (G1–G7, W1–W9), Kuratierblatt `quizaway-stufe2-kuratierblatt-v2-2026-10-01.md` (70 Karten, je Ort vier Geschichten und drei Klassiker; kuratiert wird durch Streichen, dazu je Ort die Karte, die zuerst gespielt wird). Alle 70 Karten innerhalb der Redaktionsgrenzen. Schwarzwaldklinik, Faust und Hebungsrisse tragen jetzt je eine Frage auf einem Detail. Schwäche: Die Klassiker sind über die Fahrt gleichförmig (zehnmal zweitstärkste Partei, siebenmal Landkreis). Daten, Prompts und Rohausgaben unter `data/gemeinde-achsen/iter1/` (`grunddaten.json`, `eingabe-v0.5/`, `karten-v0.5/`), Skripte unter `scripts/`.
- **Faktencheck der 100 Karten (2026-10-02):** Bericht `quizaway-stufe2-faktencheck-2026-10-02.md` (F1–F8). Jede Karte gegen den Wikipedia-Artikel, gegen eine zweite Quelle im Netz und auf zufällig wahre falsche Optionen geprüft: 60 bestätigt, 31 korrigiert, 4 unsicher (Beleg nur Wikipedia), 5 gesperrt. Sechs Karten hatten eine „falsche" Antwort, die stimmt; rund 15 Fehler standen schon im Wikipedia-Artikel. Korrekturen als eigene Schicht: `data/gemeinde-achsen/iter1/faktencheck/korrekturen.json`, geprüfte Fassungen in `karten-geprueft/`. Beide Kuratierblätter zeigen das Urteil je Karte. **Mike prüft Auflösungen nicht selbst;** die Sachprüfung liegt bei der Maschine, bei ihm Geschmack, Theorie-Gefühl und die erste Karte je Ort. Sein Kuratierblatt zum ersten Lauf ist angekreuzt (17 Kreuze, kein „keiner"); alle 30 Vorschläge bleiben im Vorrat.
- **Kuratierung und Kartensatz Stufe 2 (2026-10-02):** Mike hat beide Kuratierblätter bearbeitet (Blatt 2: nichts gestrichen, je Ort eine erste Karte; als Daten in `data/gemeinde-achsen/iter1/kuratierung.json`). **Kartensatz für den Tisch:** `quizaway-feldtest-stufe2-kartensatz-freiburg-2026-10-02.md`, gemischte Reihe (A C A B Leiter A B A B A), Mikes übrige erste Karten als Nachschlag, Protokollbogen am Ende. Offen: Ausdruck und Testperson (eine, die Stufe 1 nicht gespielt hat).
- **Karten-Prompt v0.6, Probe und dritter Volllauf (2026-10-02):** Berichte `quizaway-stufe2-probe-v0.6-2026-10-02.md` (P1–P7) und `quizaway-stufe2-volllauf3-2026-10-02.md` (D1–D8). 86 Karten an zehn Orten: 64 bestätigt, 18 korrigiert, 3 unsicher, 1 gesperrt (v0.5: 43, 18, 4, 5 von 70). Neu: Plan gibt die Eigenschaft der Klassiker vor; Wahlergebnis je Freiburger Stadtbezirk; zweite Quelle bei dünnem Artikel; Anschluss über Namensteil als Kann; Höhe nur bei einigen Quellen; Befunde des Faktenchecks als Berichtigungen in der Eingabe; sieben Pflichtkarten und bis zu drei Zusatzkarten je Lauf (Mike: sieben ist die Untergrenze, mehr ist erwünscht, eine Grenze muss es geben; vorläufig zwanzig je Ort).
- **Vorrat nach drei Läufen:** 129 geprüfte Karten, je Ort 11 bis 15, davon 48 Klassiker; 92 bestätigt, 32 korrigiert, 5 unsicher. Bei gleichem Fakt bleibt die Karte des dritten Laufs. **Vorrats-Blatt für Mike:** `quizaway-stufe2-vorrat-2026-10-02.md` (kuratieren durch Streichen; Kreuze im Blatt übernimmt `scripts/data-build/gemeinde_achsen_vorrat.py --kreuze` nach `kuratierung.json`).
- **Gemeinde-Achsen:** v0.5 plus E1–E3 (28.06.) plus **E4–E11** `gemeinde-achsen-entscheidungen-2026-10-01.md`. E9 Bekanntheitsfilter abschwächen; E10 sieben Fragen je Ort, gemeint als Vorrat (geklärt); **E11** Grunddaten als Option: alles, was die Originalvariante als Vorrat führt, dazu Wahl, Bürgermeister, Partnerstädte. Wahlquelle: Wahlbezirksstatistik der Bundeswahlleiterin zur Bundestagswahl 2025, je Gemeinde. Die Kennzeichen des Altbestands (`staedte.json`, `geo.sqlite`) sind unbrauchbar; Wikidata führt.
- **Berichtigungen am Fakt und Bindung Karte → Fakt (2026-10-02):** Bericht `quizaway-stufe2-fakten-bindung-2026-10-02.md` (B1–B9). Jeder der 806 Fakten hat eine feste Kennung (`data/gemeinde-achsen/iter1/fakten/`, Rohextraktion unverändert daneben). Die Befunde des Faktenchecks hängen am Fakt selbst (`faktencheck/berichtigungen.json`: 60 an 48 Fakten, 9 an Grunddaten; kein Befund ohne Fakt). Jede der 186 Karten ist an ihren Fakt gebunden (`karten-fakt.json`); „derselbe Fakt" ist eine Abfrage und trifft 48 der 49 Zuordnungen von Hand, die 49. war eine überholte Karte. Vorrat unverändert 129 Karten. Karten-Prompt v0.7 und `eingabe-v0.7/` lesen die berichtigten Fakten und verlangen je Karte die Zeile `FAKT-ID:`. Probe an Horben mit v0.7: neun Karten, alle mit gültiger Kennung, die Berichtigungen greifen (`karten-v0.7/09-horben.md`; ohne Faktencheck, nicht im Vorrat).
- **Zweiter Raum: Neuwied (2026-10-02):** Bericht `quizaway-stufe2-raum-neuwied-2026-10-02.md` (N1–N18). Fahrt „Rhein und Wied" (Mike): Bendorf, Engers, Heimbach-Weis, Altwied, Rengsdorf, Dierdorf, Waldbreitbach, Linz am Rhein, Bad Hönningen, Leutesdorf. Ganze Kette mit unveränderten Prompts (Extraktion v0.5.1, Karten v0.7): 811 Fakten, 96 Karten, keine Regelverletzung; Faktencheck 70 bestätigt, 17 korrigiert, 9 unsicher, keine gesperrt. Daten unter `data/gemeinde-achsen/neuwied/`; die Skripte wählen den Raum über `GA_RAUM` und lesen `<raum>/orte.json` (Freiburg bleibt `iter1`, Nullprobe ohne Abweichung). Besonderheiten Rheinland-Pfalz: Briefwahl kleiner Gemeinden wird von der Verbandsgemeinde ausgezählt (Dierdorf, Linz: Wahlergebnis gilt für die Verbandsgemeinde); Stadtteile von Neuwied aus den Stimmbezirken summiert (Altwied nur ungefähr). **Vorrats-Blatt Neuwied für Mike:** `quizaway-stufe2-vorrat-neuwied-2026-10-02.md`. **Mikes Entscheide am Abend (Bericht §4):** die vier unsicheren Dierdorfer Karten gestrichen; Wahlergebnis der Verbandsgemeinde „so lassen"; Feldkirchen als elfter Ort nachgezogen (zehn Karten, darunter die fünf früheren Dörfer und Rockenfeld; Mikes Rockenfeld-Legenden nur, wo belegt); **Kartensatz für den Tisch auch für Neuwied:** `quizaway-feldtest-stufe2-kartensatz-neuwied-2026-10-02.md` (elf Orte, A C A B Leiter A B A B C A). Befund N14: Der Wikipedia-Auszug lässt Tabellen weg (Wappenbeschreibungen, in Feldkirchen die Ortsteilgeschichte). Raum Neuwied jetzt elf Orte, 106 Karten (78 bestätigt, 19 korrigiert, 9 unsicher), 102 im Vorrat. Zusammen zwei Räume, 21 Orte, 231 Karten im Vorrat.
- **Wappen als Fragenfamilie verworfen (Mike, 2026-10-03):** Probe mit 25 Warum-Karten samt Faktencheck gebaut (Commit `e9ca645`), Urteil Mike: „bringen keine Spielfreude“ – komplett zurückgenommen (Revert); nachlesbar nur in der Historie. Keine Wappen-Karten, auch nicht als Rückseiten-Beiwerk.
- **Kartenidee Mike (2026-10-02):** Ausreißer bei Wahlen – ein Ort wählt anders als sein Kreis oder Land (Beispiel Mikes, geprüft am amtlichen Ergebnis 2026-10-03: Landtagswahl Sachsen-Anhalt 6. September 2026, Wahlkreis 37 Halle III ist der einzige der 41 Wahlkreise, in dem nicht die AfD die meisten Zweitstimmen hat – Grüne 33,7 %, AfD 18,3 %; das Direktmandat holte dort die Linke, Jannik-Loris Balint, 40,1 % der Erststimmen; landesweit Grüne 8,9 %. Quelle: Statistisches Landesamt, Vergleichstabellen LT 2026). Gehört zur Politik-Regel in v0.2.8; braucht Kreis- und Landesergebnis neben dem des Orts.
- **Rekord-Blick (Mike, 2026-10-03, Nachtrag v0.2.8 §8 Nr. 7):** vom Ort aus fragen, ob eine Eigenschaft in Stadt, Kreis, Land, Staat, Europa oder Welt Ausreißer oder Rekord ist; Ausreißer-Karte ist Sonderfall. Gerechnete Rekorde nur aus vollständiger amtlicher Vergleichsmenge (nicht Wikidata: falsche Höhe Gundelfingen, falsche Fläche Denzlingen; in RLP Wahl nur auf VG-Ebene), Text-Superlative (rund 45 in beiden Räumen) mit Faktencheck. Probe: Umkirch niedrigste Wahlbeteiligung im Landkreis, Glottertal kleinster SPD-Anteil.
- **Ausreißer-Probekarten (2026-10-03):** `quizaway-ausreisser-probekarten-2026-10-03.md`, vier Karten (Zähringen/Wahlkreis Freiburg A, Waldbreitbach C, Leutesdorf B, Glottertal Leiter); Schwellen von Mike bestätigt. **Mike:** drei Kreuze im Blatt.
- **Ausreißer im Vorrat (2026-10-03, Lauf a0.1):** Mike: Karten „mittelmäßig Freude“, bleiben „wegen ihrer Relevanz“, Form A vor B, mit Ausreißer immer im Vorrat; bei Wahlen nur das Gesamtergebnis (Urne + Brief). Skript `gemeinde_achsen_ausreisser.py` schreibt die Karten aus der Wahlbezirksstatistik, `check/gemeinde_achsen_ausreisser_pruefen.py` rechnet unabhängig nach. 8 Karten, alle bestätigt (Wahlkreis Freiburg an vier Orten, Glottertal, Kirchzarten, Waldbreitbach, Leutesdorf); Dierdorf und Linz ohne (kein Gesamtergebnis der Gemeinde). Vorrat: Freiburg 135, Neuwied 104, zusammen 239.
- **Rekord-Probekarten (2026-10-03):** `quizaway-rekord-probekarten-2026-10-03.md`, drei Karten (Waldbreitbach höchster Frauenanteil im Kreis Neuwied, Umkirch niedrigste Wahlbeteiligung im Landkreis, Fahrtrekord Dichte Gundelfingen). Text-Superlative sind schon im Vorrat; neu sind gerechnete Rekorde (Destatis-Gemeindeverzeichnis, Wahlstatistik); Rekord braucht Abstand zum Zweiten. Mike: „Spielfreude geht so“, Abstand zu klein, „da bleibt das Erstaunen aus“ (Frauenanteil über 70 % oder Wahlbeteiligung unter 50 % wäre eine Super-Frage). Folge: Rekord nur bei erstaunlichem Wert, nicht nach Rang; bundesweit gibt es solche Werte nur vereinzelt (höchster Frauenanteil 59,3 %, niedrigste Wahlbeteiligung 66,6 %), in beiden Räumen keinen. Rekord-Familie bleibt Kann-Klasse, Probekarten nicht im Vorrat. Erstaunens-Schwelle (15 Punkte vom Bundesmedian bzw. Faktor zwei) von Mike bestätigt. Ausreißer-Schwelle Ort gegen Kreis auf zehn Punkte angehoben (Mike): fünf Ausreißer-Karten bleiben (Wahlkreis Freiburg an vier Orten, Waldbreitbach); Vorrat 133 + 103 = 236.
- **Seltenheits-Karte (Idee Mike, 2026-10-03):** „Waldbreitbach hat einen Wert, den nur 73 der 10.753 Gemeinden Deutschlands übertreffen – welchen?“ Probe `quizaway-seltenheit-probekarten-2026-10-03.md` (Waldbreitbach Frauenanteil, Horben AfD-Tiefstwert, Kirchzarten Grünen-Höchstwert). Mike: Waldbreitbach „OK“, Horben und Kirchzarten „zu schwach“ (die Gegend erklärt den Wert). Regel: höchstens ein Prozent der Gemeinden Deutschlands **und** mit Abstand Platz eins im eigenen Kreis. Lauf s0.1 (`gemeinde_achsen_seltenheit.py` + Prüfer): nur Waldbreitbach, im Vorrat. Vorrat jetzt Freiburg 133, Neuwied 104, zusammen 237.
- **Nächster Schritt am PC:** offen – Eingabe-Ordner je Lauf, Ersterwähnung, Feldtest-Vorbereitung; Ersterwähnung als Grunddatum breiter holen; dem Eingabe-Skript einen Ordner je Lauf geben. **Offen bei Mike:** Vorrats-Blatt Freiburg und weitere Streichungen in Neuwied; Grenze je Ort (vorläufig zwanzig); Quelle für Seifenkistenrennen und Gaststätten in Rockenfeld, falls er eine kennt; Feldtest Stufe 2 am Tisch (zwei Kartensätze); zweite Solo-Person; Hell und Dunkel im Auto; Nachfrage an die Reviewpartner.
- **Oberfläche und Design:** maßgeblich ist **UI-Konzept v0.2** `quizaway-ui-konzept-reise-modus-v0.2-2026-10-01.md` (v0.1 vom Spaziergang plus PC-Prüfung `quizaway-ui-konzept-v0.1-pruefung-pc-2026-10-01.md`, U1–U12, plus sechs Entscheide Mikes). **Screens v0.2 zum Durchtippen** (Originalgröße, Hell/Dunkel umschaltbar): `docs/konzepte/skizzen/quizaway-reise-modus-screens-v0.2.html`, veröffentlicht unter https://claude.ai/artifact/1MFUd2u45eyLXhGwTGD4n2. Die ältere Skizze „QuizAway Reise-Modus Screens" (Stand vor v0.1) ist überholt. Papier-Screens nicht im zweiten Solo-Test. Nachtrag in v0.2: Spaltung zählt nicht als Treffer; Schrift im Auto fest, in der Bahn mitwachsend; Solo wählt und bestätigt mit „Festlegen"; eigenes Aussehen (Ortsschild-Gelb, hell und dunkel) auf dem Farbsystem von MixMi (R-UI-19). Offen nur noch: Hell/Dunkel im Auto ansehen, Papier-Test der Screens, Nachfrage. Nachfrage an die Reviewpartner (zehn Fragen, ein Paste) liegt bereit: `quizaway-oberflaeche-review-briefing-runde5-2026-10-01.md`.
- **Später:** PC-Session gegen Transfer-Konzept v1.1; dessen Kipp-Kriterium §2 ist durch den Reise-Modus ausgelöst (v0.2.7 §9).

---

## Architektur-Fundament (verbindlich)

- **Drei Stützpfeiler:** Daten · Didaktik · Player (siehe `docs/pwa_lernapp.md`)
- **Player-agnostische Architektur:** ein Lerninhalt, mehrere Player als auswechselbare Sicht (siehe `docs/choir-player-referenzmodell.md`)
- **Fünfstufige Hierarchie:** Schulfach → Werk → Programm → Lerneinheit → Übungsabschnitt
- **FSRS-Karte = Übungsabschnitt** (kleinste sinnvolle Wiederholungs-Einheit)
- **Knotenmodell:** Lernraumtopologie aus Knoten + 3 Verbindungstypen (Autor / Attribut / Pfad) — siehe `docs/produktvision.md` Sektion C.4 „Die Lernraumtopologie"

## Aktiv

- LA-1 ✅ — Projektgerüst
- LA-2 ✅ — FSRS-Engine + Dexie Store

## Pending

| LA | Beschreibung | Blocker |
|---|---|---|
| **LA-3** | Quiz-Player | **(1) Wissenstransfer Choir-Trainer-Stack → QuizAway-Domänen-Layout (2) Lernarchitektur-ADR fehlt** |
| LA-4 | Export/Import | LA-3 |
| LA-5 | Chorübung-Inhalte | LA-3 |

## Migration QuizAway → Xalento-Zielarchitektur (Spaziergang 8.5.)

**Verfahrensrichtlinie (ENTWURF, finalisierung pending):**
1. QuizAway als erste Anwendung der Xalento-Zielarchitektur
2. Architektur abgeleitet aus Choir Trainer + Xalento (operativ) + V8 (architektonisch)
3. **Vorbedingung:** dokumentierter Wissenstransfer Choir Trainer → QuizAway
4. Architektur-Detailfragen erst nach Wissenstransfer
5. **Schutzraum Choir Trainer:** in Stabilisierung (LA-21+22), keine rückwirkenden Änderungen während Migration
6. QuizAway v5 als funktionaler Vergleichspunkt — Migration abgeschlossen wenn alle 4 Modi (Sofa/Route/Live/Duell) gleichwertig

**Reihenfolge:** Schritt 0 (Verfahrensrichtlinie finalisieren) → Schritt 1 (Wissenstransfer) → Schritt 2 (Architektur-ADRs) → Schritt 3 (LA-3 starten)

## Player-Schnittstelle Zwei-Modi-Modell (Spaziergang 8.5., ENTWURF)

- **Freier Modus:** Player autonom, kein FSRS-Feedback
- **Auftragsgebundener Modus:** Übung innerhalb von Didaktik-Auftrag, EvaluationEvent zurück, FSRS-Update

→ als ADR-PLAYER-07-modi vor LA-3 zu formalisieren

## Wichtige Dokumente

| Bereich | Pfad |
|---|---|
| Produktvision (mit Knotenmodell) | `docs/produktvision.md` Sektion C.4 |
| PWA-Lernapp-Konzept | `docs/pwa_lernapp.md` |
| Player-agnostische Architektur | `docs/choir-player-referenzmodell.md` |
| Projektplanung (LA-Reihenfolge) | `docs/projektplanung.md` |
| QuizAway Konzept v9 | `docs/konzepte/quizaway_konzept-9.md` |
| ADR-001 Copilot-Architektur-Pattern | `docs/adr/ADR-001-Copilot-Architektur-Pattern.md` |

## Drive-Sync

- Sub-Ordner: `xcop/lernapp/`
- 16 Doku-Files synct via post-commit-Hook
