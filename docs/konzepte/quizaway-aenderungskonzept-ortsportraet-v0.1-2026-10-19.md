# QuizAway Reise-Modus – Änderungskonzept „Ortsporträt“ v0.1

**Status:** Änderungskonzept zu Reise-Modus v0.2.2 (GEOSYNC 007–017). Konzeptbasis, keine Implementierungsfreigabe.
**Provenienz:** Mobile Session Michi/Claude, 2026-10-19, nach zwei realen Auto-Feldtests mit dem aktuellen Prototyp.
**Review-Verfahren:** Seed für paralleles Review (Claude, Kimi, ChatGPT) → Synthese → Freigabe durch Michi.

## TL;DR

Der Prototyp stellt Datenfragen (Einwohner, Bahnhof, Wahlbeteiligung). Im Feldtest: wenig spannend, wenig unterhaltsam, kein bleibendes Bild vom Ort. Kernänderung: **Der Ort wird zur Spieleinheit, nicht die Frage.** Jeder Ort wird über so viele Fragen erschlossen, wie er hergibt; der Nutzer entscheidet, wie tief er geht. Ziel ist das Gefühl, den Ort danach „ganz gut kennengelernt“ zu haben. Harte Zahlen bleiben – aber als Einordnung in der Antwort, nicht als Frage.

## 1. Befund aus dem Feldtest

- Zahlenfragen haben kein Gedächtnis: richtig/falsch wird registriert, der Ort nicht erinnert.
- Es entsteht kein Gespräch im Auto; die Frage erzeugt kein Bild.
- Das verfehlt die Ursprungsidee („unterwegs etwas über die berührten Orte erfahren“).

## 2. Leitidee

Ein Ort wird durch **Charakteristika** kennengelernt, die eine kleine Geschichte tragen (Herrschaftsgeschichte, Partnerstadt, prägender Betrieb, Fluss, Wanderweg, Fest). Die Frage ist Vehikel; **die Antwort mit Einordnungssatz ist das Produkt.** Am Ortsschild schließt sich der Kreis.

## 3. Änderungen gegenüber v0.2.2

| Aspekt | v0.2.2 | Ortsporträt v0.1 |
|---|---|---|
| Spieleinheit | Frage | Ort |
| Fragen pro Ort | wenige, zufällig | so viele, wie der Ort hergibt; Nutzer steuert Tiefe |
| Fragetyp | Datenwerte | Charakteristika; Daten nur als Einordnung |
| Orte je Fahrt | alle Ortsschilder | Auswahl nach Ergiebigkeit; übrige als Einzeiler |
| Abschluss | – | Steckbrief pro Ort, unabhängig von Abbruch |
| Reihenfolge | Zufall | Rangliste nach Ungewöhnlichkeit, Facetten gemischt |

Unverändert: ein Gerät pro Runde, kein P2P im Reise-Modus, Beifahrer liest vor, Streckenquellen (GPS / geplante Route / gewürfelte Strecke), Bingo nur Bahn.

## 4. Facettenmodell (Kategorien je Ort)

1. **Lage & Landschaft** – Fluss, Höhe, Naturpark, Weinbau, Nachbarstadt, Grenz-/Dialektraum
2. **Geschichte & Identität** – Ersterwähnung, Stadtrechte, Herrschaft, Namensherkunft, Wappen, Söhne/Töchter, Ereignis
3. **Wirtschaft & Alltag** – prägender Arbeitgeber/Produkt, Markt, Brauerei/Winzer, Pendlerort
4. **Kultur & Freizeit** – Museen, Burg/Schloss, Wander-/Radwege, Feste, Baudenkmäler, Vereine mit Bekanntheit
5. **Infrastruktur** – Bahnhof, Autobahn, Schulen, Kirchen, Krankenhaus, Hochschule, Theater, Bad, Partnerstädte
6. **Politik & Demografie** – Wahlergebnis, Wahlbeteiligung (nur bei Auffälligkeit), Altersdurchschnitt, Bevölkerungsentwicklung

Jede Facette sollte in einer vollständigen Runde vorkommen; kein Zwang zur Gleichverteilung.

## 5. Rangliste und Qualitätsmaß

Da der Nutzer jederzeit abbrechen kann, müssen die ersten Fragen die besten sein.

- **Ungewöhnlichkeitsscore** je Fakt: Abweichung vom Erwartbaren für die Ortsgröße (Bahnhof im 800-Einwohner-Dorf hoch, in der Kreisstadt niedrig). Erweiterung des bereits beschlossenen Prinzips für die Wahlbeteiligung (2026-10-19) auf alle Fakten.
- **Facettenmix**: Sortierung nach Score, aber keine zwei aufeinanderfolgenden Fragen derselben Facette, solange Alternativen vorhanden.
- **Verbindungsbonus**: Fakten, die mehrere Orte der Fahrt verbinden (gleicher Fluss, gleiche Herrschaft), steigen im Rang.
- **Offen (Entscheidung später):** ob das Spiel die Rangfolge allein definiert oder ob der Nutzer sie setzen bzw. übersteuern kann (z. B. Facetten gewichten: „mehr Geschichte, weniger Infrastruktur“). Das Schema in Abschnitt 9 muss beides zulassen.

## 6. Nutzersteuerung der Tiefe

- **Voreinstellung pro Fahrt**: kurz / mittel / alles (Auto typisch kurz, Bahn alles).
- **Jederzeit „Nächster Ort“** – faktische Entscheidung pro Ort ohne Vorüberlegung.
- Obergrenze ist allein der Vorrat des Ortes.

## 7. Ortsauswahl auf der Strecke

- Gespielt werden Orte nach **Ergiebigkeit** (Anzahl und Score der Fakten) und Fahrtempo; Autobahnstunde ≈ 4–5 Orte.
- Nicht gespielte Orte laufen als **Einzeiler** durch („Dierdorf – Wied-Residenz, 6.000 Einwohner“), damit die Fahrt lückenlos bleibt.

## 8. Steckbrief

Nach jedem Ort – auch bei Abbruch nach der ersten Frage – ein Steckbrief in ca. 5 Zeilen: eine Zeile pro Facette, soweit Daten vorhanden. Hier landen die harten Zahlen.

## 9. Auswirkungen auf die Wissensbasis

Der Schwerpunkt verschiebt sich von Spielmechanik zu Inhaltserschließung.

**Bestandsschutz:** Alle bisher gesammelten Daten, Fakten und Fragen bleiben erhalten. Sie werden in das neue Schema migriert (Datenwerte → Steckbrief und Score-Basis; bestehende Fragen → Facette zugeordnet, Score ergänzt), nicht verworfen.

Benötigtes Fakten-Schema (Vorschlag):
`ort_id · facette · fakt (Aussage) · frageform · antwort · einordnungssatz · score_ungewoehnlichkeit · rang_nutzer (optional) · quelle · verbindungen[]`

Quellenlage:
- Wikidata/Wikipedia/OSM: Lage, Geschichte, Partnerstädte, Söhne/Töchter, Wappen, Infrastruktur – strukturiert verfügbar.
- Gemeinde-Websites: Vereine, Feste, prägender Betrieb, Alltag – nur dort; bestätigt den Ansatz „eine Zeile ist Frage und Antwort“.
- QuizAway-Vorgänger-DB: Distanzen, Einwohner, Bahnhöfe → gehen in Steckbrief und Score-Basis ein.

## 10. Auswirkungen auf die Präsentationsmodi

- **Auto (Beifahrer liest vor):** Einordnungssatz muss vorlesbar kurz sein (≤ 2 Sätze); Steckbrief als Vorlese-Text.
- **Bahn Gruppe:** volle Tiefe, Steckbrief auf dem Display.
- **Bahn Solo:** unbegrenzte Tiefe; Steckbrief als Lese-Modus ohne Frage denkbar.

## 11. Offene Fragen für das Review

1. Score-Formel: Abweichung von Größenklasse vs. Seltenheit im Gesamtkorpus vs. redaktionelle Gewichtung?
2. Fragenformate: Multiple Choice, Schätzfrage, „Welcher der heutigen Orte …“ – welche eignen sich zum Vorlesen?
3. Mindestvorrat: ab wie vielen Fakten wird ein Ort überhaupt gespielt?
4. Wie werden fehlende Facetten im Steckbrief behandelt (weglassen vs. „keine Angabe“)?
5. Papier-Feldtest: Protokollvorlage von v0.2.2 anpassen (Abbruchpunkt, Steckbrief-Wirkung)?
6. Rangfolge: nur vom Spiel berechnet, oder vom Nutzer setzbar/übersteuerbar (Facettengewichtung pro Fahrt, manuelle Reihung einzelner Fakten)?
7. Migrationspfad der Bestandsdaten: automatische Facettenzuordnung möglich, oder redaktioneller Durchgang nötig?

## 12. Ablehnungen / Nicht übernommen

- „Ein bis zwei Fragen pro Ort“ (Zwischenvorschlag Claude): abgelehnt, weil zu wenig für das Kennenlernen; Kipp-Kriterium wäre nur ein Fahrtempo, bei dem auch die Nutzersteuerung nicht mehr greift.
- Feste Spanne „5–8 Fragen“: abgelehnt zugunsten „so viele, wie der Ort hergibt“ + Nutzersteuerung.
