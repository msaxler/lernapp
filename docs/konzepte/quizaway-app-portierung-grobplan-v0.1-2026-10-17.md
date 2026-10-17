# QuizAway Reise-Modus – Grobplan Portierung als App (Apple und Android)

**Version:** 0.1.1 (Entwurf für externen Review)
**Datum:** 2026-10-17
**Status:** Vorschlag. Nichts davon ist entschieden; der Prototyp bleibt bis zum 5.11.2026 eine Webseite (Entscheid vom 17.10.).

> **An den Reviewer – bitte zuerst lesen**
>
> Du bist Gutachter, nicht Autor und nicht Projektbeteiligter. Erwartet wird **ausschließlich** deine Antwort auf die sieben Fragen in Abschnitt 9, in der dort je Frage genannten Form.
>
> Nicht erwünscht: eine Zusammenfassung des Plans, eine überarbeitete Fassung des Plans, Vorschläge zum Aufbau des Dokuments, Handlungen im Projekt (nichts committen, nichts anlegen, keine Rückfrage „wie weiter?“).
>
> Ergänzungen zum Plan, die keiner Frage zuzuordnen sind, gehören in die Antwort auf Frage 7, sonst nirgends.
>
> Länge: insgesamt höchstens eine Seite. Lieber ein klares Urteil mit Begründung als eine Auflistung aller Möglichkeiten.

---

## 1. Ausgangslage

Der Prototyp ist eine einzelne Webseite:

| Bestandteil | Größe | Inhalt |
|---|---|---|
| `index.html` | 70 KB | Spiel, Oberfläche, GPS-Logik, Sprachausgabe – ein Stück, ohne Framework |
| `daten.js` | 4,4 MB | 417 Geschichten-Orte, 3.591 Karten (Stand 17.10.) |
| `grund-de.js` | 1,7 MB | Grundversorgung: 10.754 Gemeinden ohne Modell-Karten |

Genutzte Browser-Schnittstellen: Geolocation, Wake Lock, Sprachausgabe (`speechSynthesis`), Vibration, `localStorage`, AudioContext, Zwischenablage. Kein Server, kein Login, keine Bilder, keine Landkarte.

Das Spiel läuft heute auf dem iPhone im Browser. Bekannte Grenze: **Pings kommen nur bei offenem Bildschirm** (Wake Lock). Bei gesperrtem Handy oder in der Tasche gibt es keinen Hinweis auf einen neuen Ort.

## 2. Warum überhaupt eine App

Nur Gründe, die die Webseite nicht erfüllen kann:

1. **Ortung bei gesperrtem Bildschirm** – der Hauptgrund. Eine Auto- oder Bahnfahrt dauert Stunden; das Handy liegt in der Tasche.
2. **Zuverlässige Sprachausgabe** – im Browser auf iOS wird die Stimme bei Bildschirmsperre abgeschnitten.
3. **Installation über den Store** – Auffindbarkeit, Vertrauen, Update-Mechanik, Zugriff ohne Link.
4. **Datenpakete größer als 5 MB** ohne Browser-Grenzen (Regionalpakete, später ganz Deutschland mit Karten).

Fällt Grund 1 weg (etwa weil die Spielerin ohnehin mit offenem Bildschirm spielt), fällt der wichtigste Grund für eine App weg. Das ist Frage 1 an den Reviewer.

## 3. Vier Wege

| Weg | Was passiert mit dem Prototyp | Plattformen | Einschätzung |
|---|---|---|---|
| **A. PWA** (installierbare Webseite) | bleibt unverändert | beide, aber kein Store auf iOS | billig; löst Grund 1 **nicht** (iOS lässt PWAs keine Hintergrund-Ortung) |
| **B. Web-Hülle** (Capacitor) | bleibt zu ~90 % unverändert; native Bausteine nur für Ortung, Stimme, Wachhalten | beide aus einer Codebasis | **Vorschlag** |
| **C. Plattformübergreifend neu** (Flutter / React Native) | Spiel-Logik wird neu geschrieben | beide | kein Gewinn gegenüber B, hoher Aufwand |
| **D. Zweimal nativ** (Swift / Kotlin) | alles neu, zweimal | beide | beste Hintergrund-Ortung, doppelter Aufwand; für ein 70-KB-Spiel unverhältnismäßig |

**Vorschlag B.** Begründung: Die Spiel-Logik ist klein, geprüft und im Feldtest erprobt. Sie soll nicht noch einmal entstehen. Alles, was die Webseite nicht kann, sind drei Schnittstellen zum Betriebssystem – genau das ist der Anwendungsfall einer Web-Hülle.

## 4. Zielbild (Weg B)

```
┌───────────────────────────────────────────┐
│ App-Hülle (Capacitor), je Plattform ein   │
│ Projekt (Xcode / Android Studio)          │
│  ├─ WebView: index.html + daten.js (unverändert)
│  ├─ Baustein Ortung    (Hintergrund, Korridor-Prüfung)
│  ├─ Baustein Stimme    (native Sprachausgabe)
│  ├─ Baustein Wachhalten/Hinweis (Ping, Vibration, Benachrichtigung)
│  └─ Baustein Daten     (Pakete laden, Versionsstand)
└───────────────────────────────────────────┘
```

Die Webseite spricht die Bausteine über eine schmale Schnittstelle an („gib mir die Position“, „sprich diesen Text“, „halte wach“). Im Browser fallen dieselben Aufrufe auf die heutigen Browser-Schnittstellen zurück. **So bleibt die Webseite lauffähig und ist weiterhin die Entwicklungsumgebung.**

Datenhaltung: wie bisher JS-Dateien im Paket (Entscheid 12.10.: kein SQLite aufs Handy). Ab > 5 MB Regionalpakete mit Knopf „Strecke für die Fahrt laden“ – das ist im Spielkonzept v0.3.x schon vorgesehen und wird durch die App nicht anders.

## 5. Phasen

| Phase | Ergebnis | Grobaufwand* |
|---|---|---|
| **0 Entscheid** | Review dieses Plans; Mike entscheidet Weg und Zeitpunkt | – |
| **1 Hülle** | Prototyp läuft unverändert in der App auf iOS-Simulator und Android-Emulator | 2–3 Tage |
| **2 Schnittstelle** | `index.html` ruft Ortung/Stimme/Wachhalten über eine Abstraktion; Browser-Rückfall; Webseite weiterhin spielbar | 3–4 Tage |
| **3 Hintergrund-Ortung** | Ping bei gesperrtem Bildschirm auf beiden Plattformen; Feldtest im Auto und in der Bahn | 5–8 Tage (das Risiko-Stück) |
| **4 Daten** | Pakete, Versionsstand, Aktualisierung ohne App-Update | 3–4 Tage |
| **5 Store-Vorbereitung** | Entwicklerkonten, Datenschutzangaben, Quellenseite, Screenshots, Texte | 2–3 Tage + Wartezeiten |
| **6 Beta** | TestFlight (iOS) und interner Test (Android) mit 3–5 Personen | 2 Wochen Laufzeit |
| **7 Veröffentlichung** | Freigabe durch beide Stores | Apple-Prüfung 1–7 Tage |

\* Arbeitstage bei 150 LOC/Tag und einer Person; Wartezeiten der Stores nicht enthalten. Phasen 1–2 ergeben zusammen schon eine nutzbare App ohne Hintergrund-Ortung – ein möglicher Zwischenstand.

## 6. Plattform-Besonderheiten

**Apple (iOS)**
- Hintergrund-Ortung braucht die Berechtigung „Immer“ und eine Begründung im Store-Text; Apple prüft, ob der Zweck sie rechtfertigt. „Quiz zum Ort, an dem du gerade bist“ ist ein nachvollziehbarer Zweck, wird aber geprüft.
- Blauer Balken / Hinweis „App nutzt Standort“ ist sichtbar – gewollt, kein Fehler.
- Build nur auf macOS mit Xcode, oder über einen Build-Dienst in der Cloud. **Offen: steht ein Mac zur Verfügung?** (Frage 4.)
- Entwicklerkonto 99 USD/Jahr. Prüfungsrichtlinie 5.2 (geistiges Eigentum): Quellenseite in der App beugt Rückfragen vor.
- Datenschutz-Manifest (Privacy Manifest) für Standort erforderlich.

**Android**
- Hintergrund-Ortung über einen Vordergrund-Dienst mit dauerhafter Benachrichtigung („QuizAway hört mit“); seit Android 10 Berechtigung „Standort im Hintergrund“ getrennt abzufragen.
- Play Console 25 USD einmalig; Datensicherheits-Formular; Google prüft Hintergrund-Standort gesondert und verlangt ein Video des Anwendungsfalls.
- Große Gerätevielfalt; Akku-Sparmodi einzelner Hersteller können den Dienst beenden (bekanntes Problem, dokumentierte Workarounds).

**Beide**
- Sprachausgabe nativ: bessere Stimmen, läuft bei Sperre weiter.
- Quellen- und Lizenzseite in der App (Wikipedia CC BY-SA 4.0, GeoBasis-DE/BKG, Wikidata CC0) – gilt bereits für die Webseite.

## 7. Risiken

| Risiko | Folge | Gegenmittel |
|---|---|---|
| Hintergrund-Ortung auf iOS unzuverlässig oder von Apple abgelehnt | Hauptgrund für die App entfällt | Phase 3 früh und mit echtem Feldtest; Zwischenstand nach Phase 2 ist trotzdem nutzbar |
| Akku: Dauer-GPS über 3 Stunden Fahrt | Spielerin schaltet ab | „Significant location change“ (iOS) / Intervall statt Dauer-GPS; Takt dicht/normal/ruhig gibt es schon |
| Kein Mac verfügbar | iOS-Build nur über Cloud-Dienst, Fehlersuche mühsam | Frage 4 vor Phase 1 klären |
| Capacitor-Plugins für Hintergrund-Ortung sind Drittanbieter-Pflege | Plugin verwaist | Plugin-Wahl im Review bestätigen lassen; Schnittstelle so schmal, dass ein Austausch < 200 LOC kostet |
| Store-Texte, Screenshots, Datenschutz – unterschätzter Aufwand | Verzögerung | Phase 5 als eigene Phase mit Checkliste |
| Karten mit wörtlichen Quellsätzen | Richtlinie 5.2 | Prüfskript auf lange gleiche Wortfolgen (ohne Modell), vor Phase 5 |

## 8. Was Mike entscheidet und von Hand macht (Hebel)

Automatik erzeugt hier wenig Nutzen; die folgenden Punkte sind Menschensache:

1. **Ob überhaupt** – reicht die Webseite mit Wake Lock für den Alltag? Erst der Feldtest auf dem iPhone (liegt bei Mike) zeigt das.
2. **Wann** – nicht vor dem 5.11.; danach konkurriert die App mit weiteren Orten und Regionen um das Tagesbudget.
3. **Entwicklerkonten** anlegen (Apple, Google) – Identität, Zahlung, Verträge annehmen: nur Mike.
4. **Feldtest Phase 3** – nur echte Fahrten zeigen, ob Pings bei Sperre ankommen. Niemand kann das am Schreibtisch nachstellen.
5. **Store-Texte und Screenshots** nach Geschmack; Name „QuizAway“ auf Markenkonflikte prüfen lassen.
6. **Beta-Tester** auswählen (Familie, Freunde).

## 9. Fragen an den Reviewer

Beantworte jede Frage **direkt und in der angegebenen Form**. Wo „Ja/Nein“ steht, beginnt die Antwort mit Ja oder Nein. Keine Rückfragen, keine Bedingungen anstelle einer Antwort – wenn etwas unbekannt ist, schreibe „weiß ich nicht“.

**Frage 1 – Lohnt die App?**
Form: *Ja/Nein + höchstens drei Sätze.*
Ist die Ortung bei gesperrtem Bildschirm (Abschnitt 2, Grund 1) nach deiner Einschätzung Grund genug für eine Store-App, oder reicht Weg A (PWA mit offenem Bildschirm)?

**Frage 2 – Weg B (Capacitor)?**
Form: *Ja/Nein + höchstens drei Sätze. Bei Nein: welcher Weg aus Abschnitt 3 stattdessen und der eine wichtigste Grund.*

**Frage 3 – Welches Plugin für Hintergrund-Ortung?**
Form: *Genau ein Paketname als erste Wahl, optional ein zweiter als Ersatz, je ein Satz Begründung. Stand 2026, Wartung und Eignung für die Apple-Prüfung sind die Kriterien.*

**Frage 4 – iOS-Build ohne Mac?**
Form: *Eine der drei Antworten „Mac kaufen“, „Mac leihen“ oder „Cloud-Build-Dienst“, plus ein Satz Begründung. Bei Cloud-Build: welcher Dienst.*

**Frage 5 – Aufwand Phase 3 (Hintergrund-Ortung)?**
Form: *Eine Zahl in Arbeitstagen (Spanne erlaubt), plus ein Satz. Für die übrigen Phasen nur dann eine Zahl, wenn du die Schätzung in Abschnitt 5 für falsch hältst.*

**Frage 6 – JS-Dateien oder SQLite?**
Form: *„Entscheid beibehalten“ oder „Entscheid ändern“. Bei „ändern“: der eine harte Grund in einem Satz. Ohne harten Grund keine Erörterung.*

**Frage 7 – Fehlende Risiken**
Form: *Höchstens fünf Stichpunkte, je ein Risiko in einem Satz mit seiner Folge. Nur Risiken, die in Abschnitt 7 fehlen. Keine Umformulierung bestehender Zeilen.*

## 10. Nicht Teil dieses Plans

- Mehrspieler / Duell (eigene Konzepte unter `docs/konzepte/quizaway-7a-*`, ruhen)
- Neue Spielfamilien oder Regionen (laufen in der Daten-Kette weiter, unabhängig von der App)
- Einnahmen, Preismodell, Werbung
