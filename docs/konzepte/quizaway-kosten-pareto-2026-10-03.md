# QuizAway Reise-Modus – Kosten nach Pareto (2026-10-03)

**Frage (Mike, 2026-10-03):** „Wie bekomme ich 95 % des Erfolgs mit 5 % des Aufwands?“ (oder 90/10, 80/20).

**Antwort in einem Satz:** Der Aufwand steckt zu 80 % in der Hülle, nicht im Inhalt (Agentenläufe statt direkter Aufrufe), in Karten, die nie gespielt werden (je Fahrt drei bis sechs Karten je Ort, der Vorrat hat bis zu zwanzig; berichtigt nach Mikes Hinweis, siehe Abschnitt 7), und in Orten, die nie jemand befährt. Wer diese drei Stellen schließt, kommt bei gleicher Kartenqualität auf deutlich unter 10 % des heutigen Aufwands je gefahrenem Ort. Der Erfolg selbst ist noch nicht gemessen; Maßstab sind bis zum Feldtest Mikes Urteile und der Faktencheck.

Grundlage: Faktenblatt aus allen Kartendateien, Faktencheck-Urteilen, Kuratierungen und den Aufwandsangaben der Berichte (Stand 2026-10-03; 21 Orte, 298 Karten, 237 im Vorrat). Alle Tokenzahlen der Berichte sind Obergrenzen.

---

## 1. Was heute ein Ort kostet

| Stufe | heute je Ort (Raum Neuwied) | was davon Inhalt ist |
|---|---|---|
| Extraktion (Haiku, als Agent) | rund 110.000 Token (1,1 Mio für 10 Orte samt 3 Spendern) | je Text rund 3.000 Token Eingabe und 3.000 Ausgabe |
| Kartenlauf (als Agent) | rund 150.000 Token, 5–7 min | Prompt rund 4.000 Token, Eingabe je Ort rund 15.000, Ausgabe rund 5.000: zusammen rund 24.000 |
| Faktencheck (als Agent mit Netzsuche) | rund 130.000 Token, 3–6 min | hier ist die Hülle Teil der Arbeit (Suchen, Lesen) |
| **zusammen** | **rund 390.000 Token, rund 9 min Wanduhr** | für 10 Karten, davon wird je Fahrt **eine** gespielt |
| Handarbeit PC | 26 Korrekturen an Karten, 39 Berichtigungen an Fakten je 10 Orte | |
| Handarbeit Mike | Blätter lesen, Kreuze, Urteile | |

Gemessen an der Kartenqualität ist der Ablauf gut (Faktencheck in den späten Läufen 26 % Befunde, Klassiker 5 %). Teuer ist er an drei Stellen, die mit Qualität wenig zu tun haben.

## 2. Wo der Erfolg sitzt

- **Geschichten tragen den Erfolg.** Mikes Lieblinge und erste Karten sind fast nur Geschichten: im ersten Blatt 17 von 30 angekreuzt (nur Geschichten), als erste Karte je Ort 10 von 10 Geschichten, 0 von 30 Klassikern. In den Kartensätzen für den Tisch stehen Klassiker, weil das Familienmuster sie verlangt.
- **Die erste Geschichte je Ort trägt am meisten.** Als „zuerst“ wählte Mike in 8 von 10 Orten Karte 1 des Laufs. Die Karten 7 bis 10 eines Laufs bekamen fast nie ein Signal.
- **Geschichten tragen auch die Fehler.** 94 % aller Befunde des Faktenchecks liegen bei Geschichten (85 von 90), alle unsicheren und gesperrten Karten. Klassiker aus den Grunddaten haben 5 % Befunde, Skript-Karten keine.
- **Gespielt werden drei bis sechs Karten je Ort und Fahrt** (Spielkonzept v0.2.9: drei, dann auf Wunsch drei weitere). Ein Vorrat von sieben bis zehn Karten wird damit in ein bis zwei Fahrten ausgeschöpft. *(Die erste Fassung dieses Dokuments rechnete mit einer Karte je Fahrt; das war falsch, siehe Abschnitt 7.)*
- **Nur jeder zehnte Fakt trägt eine Karte** (8–10 % der 1.750 Fakten). Die Extraktion erfasst alles.
- **Die Spender bringen fast nichts.** Eine von 96 Karten in Neuwied nutzt einen gespiegelten Fakt; die Spender kosteten in Freiburg die Hälfte, in Neuwied ein Sechstel der Extraktion.
- **Was Erstaunen auslöst, ist selten und nicht planbar** (Mike zu Wappen, Ausreißer, Rekord, Seltenheit). Mehr gerechnete Familien erhöhen den Erfolg kaum.

## 3. Die Hebel, nach Wirkung sortiert

| # | Hebel | spart (geschätzt) | kostet an Erfolg | Beleg / Annahme |
|---|---|---|---|---|
| H1 | **Erzeugen nur für befahrene Orte**, auf Abruf je geplanter Strecke, Ergebnis wird gespeichert. Kein Vorab-Lauf über 80.000 Orte. | bei 80.000 Orten fast alles; die Kosten wachsen mit den gefahrenen, nicht mit den vorhandenen Orten | keiner, solange die Erzeugung vor der Abfahrt fertig ist (heute rund 9 min je Ort, parallel weniger) | Anforderung aus dem Spielkonzept: Material nur, wo gefahren wird (§1a); Zahl der je befahrenen Orte unbekannt |
| H2 | **Direkter Modellaufruf statt Agentenlauf** für Extraktion und Kartenlauf (fester Prompt, eine Eingabe, eine Ausgabe; keine Werkzeuge, kein Projektgedächtnis) | Kartenlauf rund 150.000 → rund 25.000 Token, Extraktion je Text rund 60.000 → rund 6.000: **rund 85 % dieser beiden Stufen** | keiner zu erwarten, die Eingabe ist dieselbe; **muss mit einer Probe belegt werden** | Berichte: „ein nackter Aufruf mit Prompt und Artikel braucht einen Bruchteil“; gemessene Eingabegrößen |
| H3 | **Vorrat, der mit dem Spielen wächst:** je Ort zuerst sieben Karten, davon vier bis fünf Geschichten und der Rest Klassiker, Ausreißer und Seltenheit per Skript (kostenlos). Weitere Geschichten erst, wenn ein Ort „Noch mehr“ verlangt hat. | Kartenlauf und Faktencheck rund 40–50 % weniger Geschichten | gering: Karten 7–10 bekamen kaum Signale | Mikes „zuerst“ 8 von 10 = Karte 1; Taktung v0.2.9 |
| H4 | **Faktencheck nur für Geschichten**; Klassiker prüft ein Skript gegen die Grunddaten (wie bei Ausreißer und Seltenheit) | rund ein Drittel des Faktenchecks | 6 % der Befunde (5 Klassiker-Korrekturen) – die fängt die Rechenprüfung | Faktenblatt: Geschichten 94 % der Befunde bei 68 % der Karten |
| H5 | **Spender weglassen** | in Freiburg die Hälfte, in Neuwied ein Sechstel der Extraktion | 1 Karte von 96 | Bericht Neuwied N11 |
| H6 | **Extraktion nur der Warum- und Rekord-Fakten** statt aller Fakten | Ausgabe der Extraktion etwa halbiert | gering, 90 % der Fakten tragen heute keine Karte; aber Klassiker brauchen sie nicht | Faktenblatt: 8–10 % der Fakten mit Karte |
| H7 | **Handarbeit über Regeln statt über Karten:** Mikes Urteile werden Regeln (wie „Erstaunen statt Rang“, „keine Wappen“), nicht Kreuze je Karte | Mikes Zeit je Raum fast null; meine Korrekturen sinken mit jedem Prompt-Stand | keiner; Mike prüft Stichproben und Proben neuer Familien | Verlauf 01.–03.10.: Befundquote 43 % → 26 % durch Regeln im Prompt |

Was ausdrücklich **kein** guter Hebel ist:
- **Faktencheck nur nach Risikomerkmalen** (etwa nur erfundene Optionen, Weg (c)): fände in den späten Läufen nur 60 % der Befunde. Ein Fehler am Tisch kostet mehr als der Check.
- **Billigeres Modell für den Kartenlauf** ohne Probe: Die Karten sind das Produkt; die Qualität hängt am Modell. Erst nach H2 messen, ob ein kleineres Modell mithält.

## 4. Was das zusammen ergibt

Je Ort, bei gleicher Qualität der gespielten Karten (Schätzung, Token):

| Stand | Extraktion | Karten | Faktencheck | zusammen | gegenüber heute |
|---|---|---|---|---|---|
| heute (10 Karten, Agenten, mit Spendern) | 110.000 | 150.000 | 130.000 | **390.000** | 100 % |
| H2 + H5 (gleicher Vorrat, direkte Aufrufe, ohne Spender) | 12.000 | 25.000 | 90.000 (nur Geschichten, H4) | **127.000** | rund 33 % |
| + H3 (fünf Geschichten zuerst, Rest per Skript) | 12.000 | 20.000 | 65.000 | **97.000** | **rund 25 %** |
| + H1 (nur befahrene Orte) | | | | 97.000 je **befahrenem** Ort | bei 80.000 Orten und z. B. 2.000 befahrenen: **rund 0,6 %** des Vorab-Aufwands |

Damit ist die 80/20-Stufe (H2–H5) sicher erreichbar, und 95/5 entsteht durch H1: Aufwand nur dort, wo gespielt wird. Den Rest des Faktenchecks (Netzsuche) bekommt man nicht weg, ohne Fehler am Tisch in Kauf zu nehmen; er ist danach der größte Posten und gut angelegt.

## 5. Was davon unsicher ist und wie es geprüft wird

1. **H2 ist eine Schätzung.** Probe: zwei Orte (je einer pro Raum) mit unverändertem Prompt als direkter Aufruf (isolierter `claude -p` ohne Werkzeuge und ohne Projektgedächtnis, Tokenverbrauch aus der JSON-Ausgabe) und Vergleich mit den vorhandenen Karten: Regeltreue (Prüfskript), Faktencheck-Befunde, Mikes Blick auf drei Karten. Kosten der Probe: unter 100.000 Token.
2. **H3 setzt voraus, dass die erste Geschichte die beste ist.** Belegt nur über Mikes „zuerst“ in Freiburg (8 von 10). Der Feldtest am Tisch zeigt, ob das hält.
3. **H1 braucht eine Zahl, wie viele Orte gefahren werden.** Unbekannt; sie entscheidet, ob die Erzeugung vor der Abfahrt reicht (heute rund 9 min je Ort) oder ob man häufige Strecken vorab erzeugt.
4. **Der Erfolg ist noch nicht gemessen.** Alle Wert-Aussagen stützen sich auf Mikes Blätter und den Faktencheck, nicht auf Spiele. Der Feldtest Stufe 2 und der Fahrt-Prototyp liefern die erste echte Messung (Protokoll: Treffer und Bedenkzeit je Karte).

## 6. Wo Mike mehr bringt als die Automatik

- Strecken nennen, die wirklich gefahren werden (H1).
- Im Feldtest beobachten, ob die erste Geschichte je Ort trägt (H3).
- Neue Familien und Prompt-Stände als Probe von drei bis fünf Karten beurteilen; jede Regel aus einem Urteil spart danach Handarbeit an allen Orten (H7).

**Vorschlag für den nächsten Schritt:** die Probe zu H2 (zwei Orte, direkter Aufruf, Vergleich). Sie entscheidet über den größten sicheren Posten und kostet weniger als ein heutiger Kartenlauf.

---

## 7. Berichtigung nach Mikes Hinweis (2026-10-03)

Mike: „Von den mindestens sieben vorhandenen Fragen zu einem Ort sollen je Ort drei gespielt werden und dann soll gefragt werden: Noch mehr zu diesem Ort? Für die jeweils nächsten drei Fragen.“ Die erste Fassung dieser Analyse ging von einer Frage je Ort und Fahrt aus (Spielkonzept bis v0.2.8). Neu gilt v0.2.9: drei je Ort, dann auf Wunsch je drei weitere.

Folgen für die Rechnung:
- Der Vorrat wird gebraucht. Sieben Karten reichen für eine Fahrt mit einem „Noch mehr“; für wiederholte Fahrten über dieselbe Strecke wächst er nach (H3 neu gefasst).
- H3 spart weniger: rund 25 % statt 18 % des heutigen Aufwands je Ort. Die übrigen Hebel bleiben unverändert; H1 und H2 tragen weiter den größten Teil.
- Neu wichtig wird die Zahl der Geschichten je Ort: Drei Fragen hintereinander aus den Grunddaten wären blass. Ein Ort mit dünnem Artikel braucht deshalb die zweite Quelle (Spielkonzept §8 Nr. 7) eher als bisher.
