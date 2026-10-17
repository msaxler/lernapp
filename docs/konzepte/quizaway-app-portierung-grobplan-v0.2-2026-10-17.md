# QuizAway Reise-Modus – Grobplan Portierung als App (Apple und Android)

**Version:** 0.2 (nach erster Reviewrunde; löst v0.1.1 ab)
**Datum:** 2026-10-17
**Status:** Vorschlag. Nichts davon ist entschieden; der Prototyp bleibt bis zum 5.11.2026 eine Webseite (Entscheid vom 17.10.).
**Änderungen gegenüber v0.1.1:** siehe Abschnitt 11.

> **An den Reviewer – bitte zuerst lesen**
>
> Du bist Gutachter, nicht Autor und nicht Projektbeteiligter. Erwartet wird **ausschließlich** deine Antwort auf die acht Fragen in Abschnitt 9, in der dort je Frage genannten Form.
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
4. **Datenpakete ohne Browser-Grenzen** (Regionalpakete, später ganz Deutschland mit Karten).

Die Gründe 1 und 2 sind zugleich das, was eine App gegenüber einer „eingewickelten Webseite“ rechtfertigt (Apple-Richtlinie 4.2, Mindestfunktionalität). Fällt Grund 1 weg (etwa weil die Spielerin ohnehin mit offenem Bildschirm spielt), fällt der wichtigste Grund für eine App weg. Das ist Frage 1 an den Reviewer.

## 3. Vier Wege

| Weg | Was passiert mit dem Prototyp | Plattformen | Einschätzung |
|---|---|---|---|
| **A. PWA** (installierbare Webseite) | bleibt unverändert | beide, aber kein Store auf iOS | billig; löst Grund 1 **nicht** (iOS lässt PWAs keine Hintergrund-Ortung) |
| **B. Web-Hülle** (Capacitor) | bleibt weitgehend unverändert; native Bausteine nur für Ortung, Stimme, Wachhalten | beide aus einer Codebasis | **Vorschlag, unter Vorbehalt der Machbarkeitsspitze (Phase 1)** |
| **C. Plattformübergreifend neu** (Flutter / React Native) | Spiel-Logik wird neu geschrieben | beide | kein Gewinn gegenüber B; die Regeln der Betriebssysteme zur Hintergrund-Ortung gelten dort genauso |
| **D. Zweimal nativ** (Swift / Kotlin) | alles neu, zweimal | beide | doppelter Aufwand; auch hier keine Befreiung von den Hintergrund-Regeln; für ein 70-KB-Spiel unverhältnismäßig |

**Vorschlag B.** Begründung: Die Spiel-Logik ist klein, geprüft und im Feldtest erprobt. Sie soll nicht noch einmal entstehen. Alles, was die Webseite nicht kann, sind drei Schnittstellen zum Betriebssystem – genau das ist der Anwendungsfall einer Web-Hülle. „Weitgehend unverändert“ ist eine Annahme, kein Nachweis; die Machbarkeitsspitze prüft sie.

## 4. Zielbild (Weg B)

```
┌───────────────────────────────────────────┐
│ App-Hülle (Capacitor), je Plattform ein   │
│ Projekt (Xcode / Android Studio)          │
│  ├─ WebView: index.html + daten.js (unverändert)
│  ├─ Baustein Ortung    (Hintergrund, Geofence je Korridor)
│  ├─ Baustein Stimme    (native Sprachausgabe, Hintergrund-Audio)
│  ├─ Baustein Wachhalten/Hinweis (Ping, Vibration, Benachrichtigung)
│  └─ Baustein Daten     (Pakete laden, Versionsstand)
└───────────────────────────────────────────┘
```

Die Webseite spricht die Bausteine über eine schmale Schnittstelle an („gib mir die Position“, „sprich diesen Text“, „halte wach“). Im Browser fallen dieselben Aufrufe auf die heutigen Browser-Schnittstellen zurück. **So bleibt die Webseite lauffähig und ist weiterhin die Entwicklungsumgebung.** Die Schnittstelle ist so schmal, dass ein Plugin-Wechsel unter 200 LOC bleibt.

**Plugin-Kandidaten für die Ortung** (Stand Oktober 2026, zu prüfen in Phase 1):
- `@capgo/background-geolocation` – kostenlos, an Capacitor 8 gekoppelt; soll native Geofences auf beiden Plattformen bieten. Geofences wären für QuizAway ideal: Das Betriebssystem weckt die App beim Betreten eines Korridors, auch wenn sie nicht läuft. **Erste Wahl, falls die Geofence-Angabe stimmt.**
- `@capacitor-community/background-geolocation` – Ursprung des obigen, dokumentiert bis Capacitor 7. Vergleichskandidat.
- Capawesome Background Geolocation (kostenpflichtig) und Transistorsoft (kommerzielle Lizenz) – ausgereift, aber für ein Spiel ohne Server-Übertragung überdimensioniert.

Prüfpunkte je Kandidat: unterstützte Capacitor/iOS/Android-Versionen, letzte Releases, Lizenz, Verhalten nach Sperre, nach Prozessende, nach Neustart, nach Berechtigungsentzug, Akkuverbrauch, nötige native Konfiguration.

**Datenhaltung:** JS-Dateien wie bisher (Entscheid 12.10.: kein SQLite aufs Handy; beide Reviewer sehen keinen harten Grund dagegen). Zu unterscheiden sind **Paketdaten** (im App-Bundle, ändern sich nur mit App-Update) und **nachladbare Pakete** (Regionalpakete, Knopf „Strecke für die Fahrt laden“). Die bisherige 5-MB-Marke war eine Faustregel für `daten.js` im Browser-Artifact; für die App gilt sie nicht. Gemessen wird stattdessen: Größe des installierten Pakets, Zeit bis zum Spielstart, Abfragezeit je Ortswechsel.

## 5. Phasen

| Phase | Ergebnis | Grobaufwand* |
|---|---|---|
| **0 Entscheid** | Review dieses Plans; nach dem 5.11.: Feldtest der Webseite zeigt, ob Grund 1 (Abschnitt 2) im Alltag trägt. Vorher keine Portierung. | – |
| **1 Machbarkeitsspitze** | Capacitor-Gerüst mit dem unveränderten Prototyp; ein Kandidaten-Plugin; Hintergrund-Ortung und Hinweis auf echten Geräten (iPhone **und** ein Android-Gerät) während einer echten Fahrt. **Noch keine Datenpakete, keine Schnittstellen-Abstraktion.** Ergebnis: Messung nach Abschnitt 5a. | 5–8 Tage + Fahrten |
| **Go/No-Go** | Weiter nur, wenn beide Plattformen die Kriterien in 5a erfüllen oder ein dokumentierter Kompromiss steht (z. B. nur iOS, oder nur Vordergrund + bessere Stimme). | – |
| **2 Schnittstelle** | `index.html` ruft Ortung/Stimme/Wachhalten über eine Abstraktion; Browser-Rückfall; Webseite weiterhin spielbar; Spielstand überlebt Prozessende | 3–5 Tage |
| **3 Ortung fertig** | Erklärbildschirm vor der Berechtigungsfrage, Umgang mit „nur ungefähr“ / „nur bei Nutzung“ / Entzug, Hinweis „App nicht wegwischen“, Akku-Takt, Hintergrund-Audio für die Stimme | 5–8 Tage |
| **4 Daten** | Paketdaten vs. nachladbare Pakete, Versionsstand, Aktualisierung ohne App-Update | 3–4 Tage |
| **5 Store-Vorbereitung** | Entwicklerkonten, Datenschutzangaben, Berechtigungstexte, Quellenseite, Screenshots, Store-Texte, iPad-Darstellung | 3–5 Tage + Wartezeiten |
| **6 Beta** | TestFlight (iOS) und interner Test (Android) mit 3–5 Personen, mindestens eine mehrstündige Fahrt je Plattform | 2 Wochen Laufzeit |
| **7 Veröffentlichung** | Freigabe durch beide Stores | nicht planbar; Apple meist Tage, Google prüft Hintergrund-Standort gesondert |

\* Arbeitstage einer Person. Für Phase 1 und 3 ist die Zahl der Codezeilen kein Maßstab; der Aufwand steckt in Betriebssystem-Eigenheiten, Fahrten und Fehlersuche. Kimi schätzt die Ortung insgesamt auf 8–12 Tage; die Spanne hier (Phase 1 + 3 = 10–16) liegt darüber, weil die Machbarkeitsspitze eigene Fahrten braucht. **Die Schätzung wird nach Phase 1 neu gesetzt.** Phasen 1–2 ergeben schon eine nutzbare App ohne Hintergrund-Ortung – ein möglicher Zwischenstand.

### 5a. Messbare Kriterien für die Machbarkeitsspitze

Je Plattform, auf einer Fahrt von mindestens 90 Minuten mit gesperrtem Bildschirm, Handy in der Tasche:

| Messgröße | Bestanden, wenn |
|---|---|
| Erkannte Orte | ≥ 90 % der durchfahrenen Korridore lösen einen Hinweis aus |
| Verspätung | Hinweis kommt, solange das Fahrzeug noch im Korridor ist (Korridor 5–7 km, bei 100 km/h ≈ 3–4 min) |
| Fehlalarme | ≤ 1 je Stunde |
| Akku | ≤ 10 % je Stunde zusätzlich gegenüber Fahrt ohne App |
| Stimme | Text wird bei Sperre vollständig gesprochen |
| Wiederaufnahme | Nach Beenden durch das System: App startet mit dem letzten Spielstand, keine neue Runde |

Protokoll: Zeit, GPS-Position, ausgelöster Ort, gesprochener Text – als Datei auf dem Gerät, danach am PC ausgewertet.

## 6. Plattform-Besonderheiten

**Apple (iOS)**
- Hintergrund-Ortung braucht den Hintergrund-Modus `location` und die Berechtigung „Immer“. Der Dialog für „Immer“ kommt pro Installation nur einmal; eine Ablehnung ist nur über die Einstellungen zu heilen → Erklärbildschirm vor dem Dialog (Phase 3).
- Die Begründungstexte für die Berechtigungen (in der Info.plist) müssen den Zweck konkret nennen; vage Texte sind ein häufiger Ablehnungsgrund.
- Sprachausgabe bei Sperre braucht zusätzlich den Hintergrund-Modus `audio`; Apple prüft dessen Verwendung getrennt von der Ortung.
- Wird die App von der Spielerin weggewischt, endet die Ortung – Regel des Systems, kein Plugin-Fehler. Hinweis in die Einführung.
- Richtlinie 4.2 (Mindestfunktionalität): Hintergrund-Ortung und native Stimme sind der Mehrwert gegenüber der Webseite; so in den Prüfer-Notizen begründen.
- Richtlinie 5.2 (geistiges Eigentum): Quellenseite in der App beugt Rückfragen vor.
- Drei getrennte Pflichten, nicht verwechseln: (1) Datenschutzangaben im Store, (2) Berechtigungstexte in der App, (3) Privacy Manifest – ob und wofür (3) nötig ist, hängt von den genutzten APIs und Plugins ab und wird in Phase 5 anhand der konkreten Toolchain geprüft.
- Build nur auf macOS mit Xcode oder über einen Cloud-Build-Dienst (Frage 4). iPad: Die App muss dort zumindest sinnvoll laufen; Hochformat-Layout genügt.
- Entwicklerkonto 99 USD/Jahr.

**Android**
- Hintergrund-Ortung über einen Vordergrund-Dienst mit dauerhafter Benachrichtigung; „Standort im Hintergrund“ ist seit Android 10 eine getrennte Berechtigung.
- Play Console 25 USD einmalig; Datensicherheits-Formular; Google verlangt für Hintergrund-Standort eine gesonderte Begründung und ein Video des Anwendungsfalls.
- Akku-Sparmodi einzelner Hersteller beenden Dienste; ein Test auf einem Gerät beweist nichts für andere. Die Machbarkeitsspitze läuft deshalb auf einem gängigen Gerät, die Beta auf mindestens zwei Herstellern.

**Beide**
- Ein Nachweis auf einer Plattform gilt nicht für die andere; die Kriterien in 5a werden je Plattform erfüllt.
- Ortung beginnt nur nach bewusstem „Fahrt starten“ und endet mit „Fahrt beenden“ – kein Dauer-Tracking. Das ist zugleich das Argument gegenüber beiden Store-Prüfungen.
- Wake Lock wird in der App überflüssig: Hinweise kommen aus dem Ortungs-Baustein, nicht aus dem wachen Bildschirm. Im Browser-Rückfall bleibt er.
- Datenschutz: Positionen werden nur auf dem Gerät verarbeitet, nichts geht an einen Server. Damit entfällt eine Einwilligung über die Systemberechtigung hinaus; eine Datenschutzerklärung (Store-Pflicht beider Anbieter) ist trotzdem nötig und sagt genau das.
- Quellen- und Lizenzseite in der App (Wikipedia CC BY-SA 4.0, GeoBasis-DE/BKG, Wikidata CC0) – gilt bereits für die Webseite.
- Name „QuizAway“: Ein Reviewer nennt eine US-Marke (Klasse 41, 2019), unbelegt. Vor Phase 5 bei DPMA/EUIPO prüfen, auch die Schreibweisen „Quiz-Away“ und „Quiz Away“.

## 7. Risiken

Jedes Risiko hat einen Prüfzeitpunkt und ein Abbruchkriterium.

| Risiko | Folge | Gegenmittel | Prüfung | Abbruch, wenn |
|---|---|---|---|---|
| Hintergrund-Ortung unzuverlässig oder von Apple abgelehnt | Hauptgrund für die App entfällt | Machbarkeitsspitze zuerst; Zwischenstand nach Phase 2 trotzdem nutzbar | Phase 1 | Kriterien 5a auf iOS verfehlt |
| Akku und Wärme über 3 Stunden Fahrt | Spielerin schaltet ab | Geofence statt Dauer-GPS; Takt dicht/normal/ruhig gibt es schon | Phase 1, Beta | > 10 %/h |
| GPS ungenau, Ort übersprungen, Hinweis zu spät | Spiel wirkt kaputt | Korridor je Ort (`korridor_m`) weiten; verpasster Ort wird beim nächsten Halt nachgeholt („Du bist eben durch X gefahren“) | Phase 1 | < 90 % erkannt |
| Stimme bei Sperre stumm | Hinweis geht unter | Hintergrund-Modus `audio`; Vibration als Rückfall | Phase 1 | Stimme bricht ab und Apple lehnt `audio` ab |
| Berechtigung nur „bei Nutzung“ oder „ungefähr“, später entzogen | App schweigt ohne Erklärung | Erklärbildschirm; Zustand sichtbar anzeigen („Ortung aus – antippen“) | Phase 3 | – (Gestaltung, kein Abbruch) |
| App vom System beendet oder weggewischt | Runde verloren, Ortung aus | Spielstand nach jedem Zug sichern; Hinweis in der Einführung | Phase 2 | – |
| Kein Mac verfügbar | iOS-Build nur über Cloud, Fehlersuche mühsam | Frage 4 vor Phase 1 klären | Phase 0 | – |
| Plugin verwaist oder bricht mit neuer iOS/Android-Version | Wartungslast auf eine Person | schmale Schnittstelle (< 200 LOC Wechsel); jährlicher Prüftermin nach den Herbst-Releases von iOS und Android | Phase 1, dann jährlich | – |
| Apple lehnt „Immer“-Ortung als unnötig ab | Kernfunktion fehlt auf iOS | Ortung läuft nur nach bewusstem „Fahrt starten“ und endet mit „Fahrt beenden“; Begründung im Prüfer-Hinweis; **Plan B:** Zwischenstand nach Phase 2 (Vordergrund + Wake Lock + Hinweis „Bildschirm an lassen“) wird veröffentlicht | Phase 7 | zweite Ablehnung nach Nachbesserung |
| Store-Texte, Screenshots, Datenschutz unterschätzt | Verzögerung | Phase 5 mit Checkliste | Phase 5 | – |
| Karten mit wörtlichen Quellsätzen | Richtlinie 5.2 | Prüfskript auf lange gleiche Wortfolgen (ohne Modell), vor Phase 5 | Phase 5 | – |

## 8. Was Mike entscheidet und von Hand macht (Hebel)

Automatik erzeugt hier wenig Nutzen; die folgenden Punkte sind Menschensache:

1. **Ob überhaupt** – reicht die Webseite mit Wake Lock für den Alltag? Der Feldtest auf dem iPhone (liegt bei Mike) zeigt das. Vor dieser Antwort wird nichts gebaut.
2. **Wann** – nicht vor dem 5.11.; danach konkurriert die App mit weiteren Orten und Regionen um das Tagesbudget.
3. **Go/No-Go nach Phase 1** – Mike liest das Fahrtprotokoll und entscheidet gegen die Kriterien in 5a. Erst danach Plugin festlegen, erst danach über einen Mac entscheiden.
4. **Entwicklerkonten** anlegen (Apple, Google) – Identität, Zahlung, Verträge annehmen: nur Mike.
5. **Fahrten für Phase 1 und Beta** – nur echte Fahrten zeigen, ob Pings bei Sperre ankommen.
6. **Store-Texte und Screenshots** nach Geschmack; Name „QuizAway“ auf Markenkonflikte prüfen lassen.
7. **Beta-Tester** auswählen (Familie, Freunde; mindestens ein Android-Gerät eines zweiten Herstellers).

## 9. Fragen an den Reviewer

Beantworte jede Frage **direkt und in der angegebenen Form**. Wo „Ja/Nein“ steht, beginnt die Antwort mit Ja oder Nein. Keine Rückfragen, keine Bedingungen anstelle einer Antwort – wenn etwas unbekannt ist, schreibe „weiß ich nicht“.

**Frage 1 – Lohnt die App?**
Form: *Ja/Nein + höchstens drei Sätze.*
Ist die Ortung bei gesperrtem Bildschirm (Abschnitt 2, Grund 1) nach deiner Einschätzung Grund genug für eine Store-App, oder reicht Weg A (PWA mit offenem Bildschirm)?

**Frage 2 – Weg B (Capacitor)?**
Form: *Ja/Nein + höchstens drei Sätze. Bei Nein: welcher Weg aus Abschnitt 3 stattdessen und der eine wichtigste Grund.*

**Frage 3 – Welches Plugin für Hintergrund-Ortung?**
Form: *Genau ein Paketname als erste Wahl, optional ein zweiter als Ersatz, je ein Satz Begründung. Zusätzlich Ja/Nein: Bietet die erste Wahl native Geofences auf iOS und Android?*

**Frage 4 – iOS-Build ohne Mac?**
Form: *Eine der drei Antworten „Mac kaufen“, „Mac leihen“ oder „Cloud-Build-Dienst“ – getrennt für Phase 1 und für die Phasen danach – plus je ein Satz. Bei Cloud-Build: welcher Dienst.*

**Frage 5 – Aufwand Phase 1 + 3 (Ortung)?**
Form: *Eine Zahl in Arbeitstagen (Spanne erlaubt) für beide Phasen zusammen, plus ein Satz. Für die übrigen Phasen nur dann eine Zahl, wenn du die Schätzung in Abschnitt 5 für falsch hältst.*

**Frage 6 – JS-Dateien oder SQLite?**
Form: *„Entscheid beibehalten“ oder „Entscheid ändern“. Bei „ändern“: der eine harte Grund in einem Satz. Ohne harten Grund keine Erörterung.*

**Frage 7 – Fehlende Risiken**
Form: *Höchstens fünf Stichpunkte, je ein Risiko in einem Satz mit seiner Folge. Nur Risiken, die in Abschnitt 7 fehlen. Keine Umformulierung bestehender Zeilen.*

**Frage 8 – Kriterien in 5a**
Form: *Je Zeile der Tabelle 5a: „passt“ oder ein anderer Schwellwert mit einem Satz Begründung.*

## 10. Nicht Teil dieses Plans

- Mehrspieler / Duell (eigene Konzepte unter `docs/konzepte/quizaway-7a-*`, ruhen)
- Neue Spielfamilien oder Regionen (laufen in der Daten-Kette weiter, unabhängig von der App)
- Einnahmen, Preismodell, Werbung
- Ein Beginn der Phasen 1–2 vor dem 5.11. (von einem Reviewer vorgeschlagen; widerspricht dem Entscheid vom 17.10. und bleibt draußen)

## 11. Änderungen v0.1.1 → v0.2

Eingearbeitet aus der ersten Reviewrunde (ChatGPT, Kimi, Nachtrag Qwen; drei Reviewer haben nicht geantwortet, sondern den Plan zusammengefasst):

- **Machbarkeitsspitze als Phase 1** vor jeder Portierungsarbeit, mit Go/No-Go und messbaren Kriterien (neuer Abschnitt 5a). Aufwandschätzung wird danach neu gesetzt.
- **Beide Plattformen eigener Nachweis**; Android auf mehr als einem Hersteller in der Beta.
- **Plugin-Kandidaten** benannt (Capgo erste Wahl wegen Geofences – Angabe zu prüfen; Community-Plugin als Vergleich; Capawesome/Transistorsoft als Überdimensionierung).
- **5-MB-Marke** als Browser-Faustregel eingeordnet; Paketdaten vs. nachladbare Pakete unterschieden; Messgrößen statt Grenze.
- **Datenschutz dreigeteilt** (Store-Angaben, Berechtigungstexte, Privacy Manifest nach Toolchain).
- **Apple-Richtlinie 4.2**, Hintergrund-Modus `audio`, einmaliger „Immer“-Dialog, Force-Quit beendet Ortung, Info.plist-Begründungen, iPad.
- **Risiken** mit Prüfzeitpunkt und Abbruchkriterium; neu: GPS-Lücken, Stimme bei Sperre, Berechtigungsablauf, Wiederaufnahme nach Prozessende, Plugin-Wartung.
- **Mac-Frage** getrennt für Phase 1 (leihen oder Cloud-Build, z. B. GitHub-Actions-macOS-Runner oder Codemagic) und danach.
- **Frage 8** neu (Kriterien 5a).
- Aus Qwen: **Plan B** bei Apple-Ablehnung (Zwischenstand nach Phase 2 veröffentlichen); Ortung nur nach „Fahrt starten“; Wake Lock in der App überflüssig; Datenschutz bei rein lokaler Verarbeitung; Markenprüfung mit Schreibvarianten.
- Nicht übernommen: Phasen 1–2 vor dem 5.11. beginnen (Kimi).
- Nicht übernommen nach Faktencheck (Qwen): Paketname `@capacitor/background-geolocation` für Transistorsoft (heißt `@transistorsoft/capacitor-background-geolocation`) und `@capgo/capacitor-native-background-geolocation` (heißt `@capgo/background-geolocation`); „Privacy Manifest mit `NSLocation…UsageDescription`“ (das sind Info.plist-Texte, kein Manifest); „Apple verlangt Video-Demo“ (verlangt Google); „Vordergrund-Dienst muss binnen 60 s starten“ (so nicht belegt); Eigenbau in Swift/Kotlin als Plugin-Ersatz (widerspricht dem Zweck von Weg B, bleibt als Ausweg in Abschnitt 7 „Plugin verwaist“ gedeckt).
