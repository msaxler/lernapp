# QuizAway Reise-Modus – Grobplan Portierung als App (Apple und Android)

**Version:** 0.3 (nach zweiter Reviewrunde; löst v0.2 ab)
**Datum:** 2026-10-17
**Status:** Vorschlag. Der Prototyp bleibt bis zum 5.11.2026 eine Webseite (Entscheid vom 17.10.). Beide offenen Punkte entschieden (Abschnitt 8, Nr. 3 Akku-Schwelle, Nr. 4 Cloud-Mac mieten). Nächster Schritt erst nach dem 5.11.: Feldtest der Webseite, dann Phase 0.
**Änderungen gegenüber v0.2:** Abschnitt 11. **Auswertung der Reviewrunde:** Abschnitt 12.

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

Die Gründe 1 und 2 sind zugleich das, was eine App gegenüber einer „eingewickelten Webseite“ rechtfertigt (Apple-Richtlinie 4.2, Mindestfunktionalität). Fällt Grund 1 weg (etwa weil die Spielerin ohnehin mit offenem Bildschirm spielt), fällt der wichtigste Grund für eine App weg. Alle sechs Reviewer bejahen Grund 1; den Beleg liefert erst der Feldtest der Webseite.

## 3. Vier Wege

| Weg | Was passiert mit dem Prototyp | Plattformen | Einschätzung |
|---|---|---|---|
| **A. PWA** (installierbare Webseite) | bleibt unverändert | beide, aber kein Store auf iOS | billig; löst Grund 1 **nicht** (iOS lässt PWAs keine Hintergrund-Ortung); bleibt **Plan B** |
| **B. Web-Hülle** (Capacitor) | Spiel bleibt unverändert; native Bausteine für Ortung, Hinweis, Stimme | beide aus einer Codebasis | **Vorschlag (6 von 6 Reviewern), unter Vorbehalt der Machbarkeitsspitze** |
| **C. Plattformübergreifend neu** (Flutter / React Native) | Spiel-Logik wird neu geschrieben | beide | kein Gewinn gegenüber B; die Regeln der Betriebssysteme zur Hintergrund-Ortung gelten dort genauso |
| **D. Zweimal nativ** (Swift / Kotlin) | alles neu, zweimal | beide | doppelter Aufwand; auch hier keine Befreiung von den Hintergrund-Regeln |

## 4. Zielbild (Weg B)

```
┌─────────────────────────────────────────────────────┐
│ App-Hülle (Capacitor), je Plattform ein Projekt      │
│                                                      │
│  WebView: index.html + daten.js  ← nur wenn offen    │
│     ▲ „Quiz zu Ort X zeigen“                         │
│     │                                                │
│  Native Schicht (läuft auch bei Sperre, ohne WebView)│
│  ├─ Ortung:  Geofence-Fenster – die nächsten ≤ 18    │
│  │           Korridore in Fahrtrichtung, bei jedem    │
│  │           Übergang nachgeschoben                   │
│  ├─ Hinweis: Benachrichtigung + Vibration + Stimme   │
│  │           (nativ, ohne JavaScript)                 │
│  ├─ Stimme:  native Sprachausgabe, Hintergrund-Audio │
│  └─ Daten:   Pakete laden, Versionsstand             │
└─────────────────────────────────────────────────────┘
```

**Wichtigste Änderung gegenüber v0.2:** Hinweis und Ortung laufen vollständig nativ. Die WebView ist bei Sperre eingefroren oder entladen; ein Geofence-Ereignis darf nicht auf JavaScript warten. Die native Schicht liest dafür eine kleine Ortsliste (Slug, Koordinate, Korridor, Hinweis-Satz) aus den Paketdaten. Das Quiz selbst bleibt im Web-Teil und kommt erst, wenn die Spielerin das Handy in die Hand nimmt.

**Geofence-Fenster:** iOS überwacht höchstens 20 Regionen je App, Android 100. 417 Orte passen nicht auf einmal. Die native Schicht hält deshalb ein Fenster der nächsten Korridore (Reihenfolge aus `orte.json` entlang der Strecke oder nach Entfernung und Fahrtrichtung) und schiebt bei jedem Übergang nach. Geofences sind Kreise; die Korridore (`korridor_m`, 5–7 km) sind das bereits.

Im Browser fallen dieselben Aufrufe auf die heutigen Browser-Schnittstellen zurück. **So bleibt die Webseite lauffähig und ist weiterhin die Entwicklungsumgebung.** Die Schnittstelle ist so schmal, dass ein Plugin-Wechsel unter 200 LOC bleibt; die native Hinweis-Logik ist eigener Code (geschätzt 200–300 LOC je Plattform).

**Plugin für die Ortung** (6 von 6 Reviewern): `@capgo/background-geolocation` – kostenlos, an Capacitor 8 gekoppelt, dokumentiert native Geofences auf beiden Plattformen. Ersatz: `@capacitor-community/background-geolocation` (4 Reviewer; Ursprung des obigen, ohne Geofences, nur Rückfall) oder `@transistorsoft/capacitor-background-geolocation` (2 Reviewer; kommerziell, ausgereift). Ob Geofence-Übergänge bei entladener WebView die native Hinweis-Schicht erreichen, prüft Phase 1 ausdrücklich.

**Datenhaltung:** JS-Dateien wie bisher (Entscheid 12.10.; 6 von 6 Reviewern: beibehalten). Zu unterscheiden sind **Paketdaten** (im App-Bundle) und **nachladbare Pakete** (Regionalpakete, Knopf „Strecke für die Fahrt laden“). Gemessen wird: Größe des installierten Pakets, Zeit bis zum Spielstart, Abfragezeit je Ortswechsel. Nachgeladene Pakete tragen eine Version; Spielstand und Paket werden beim Start gegeneinander geprüft.

## 5. Phasen

| Phase | Ergebnis | Grobaufwand* |
|---|---|---|
| **0 Entscheid** | Review dieses Plans; nach dem 5.11.: Feldtest der Webseite zeigt, ob Grund 1 im Alltag trägt. Vorher keine Portierung. | – |
| **1 Machbarkeitsspitze** | Capacitor-Gerüst mit dem unveränderten Prototyp; Capgo-Plugin; native Hinweis-Schicht in Rohform; Geofence-Fenster; echte Fahrt mit iPhone **und** Android-Gerät. Noch keine Datenpakete, keine Schnittstellen-Abstraktion. Ergebnis: Messung nach 5a. | 6–9 Tage + Fahrten |
| **Go/No-Go** | Weiter nur, wenn beide Plattformen 5a erfüllen oder ein dokumentierter Kompromiss steht (z. B. nur iOS, oder Plan B). | – |
| **2 Schnittstelle** | `index.html` ruft Ortung/Stimme/Wachhalten über eine Abstraktion; Browser-Rückfall; Webseite weiterhin spielbar; Spielstand nach jedem Zug gesichert | 3–5 Tage |
| **3 Ortung fertig** | Erklärbildschirm vor der Berechtigungsfrage; Umgang mit „nur ungefähr“ / „nur bei Nutzung“ / Entzug / zweiter Android-Dialog; sichtbarer Ortungszustand; Hinweis „App nicht wegwischen“; Akku-Takt; Hintergrund-Audio; Vibrations-Rückfall | 6–8 Tage |
| **4 Daten** | Paketdaten vs. nachladbare Pakete, Versionsstand, Aktualisierung ohne App-Update | 3–4 Tage |
| **5 Store-Vorbereitung** | Entwicklerkonten, Datenschutzerklärung, Berechtigungstexte, Quellenseite, Markenprüfung, Screenshots, Store-Texte, Video für Google, iPad-Darstellung | 3–5 Tage + Wartezeiten |
| **6 Beta** | TestFlight und interner Test mit 3–5 Personen, mindestens eine mehrstündige Fahrt je Plattform, Android auf zwei Herstellern | 2 Wochen Laufzeit |
| **7 Veröffentlichung** | Freigabe durch beide Stores | nicht planbar; Googles Prüfung des Hintergrund-Standorts kann Wochen dauern |

\* Arbeitstage einer Person. Phasen 1 + 3 zusammen: Reviewer-Spannen 10–16, 10–15, 12–16, 10–14, 12–18, 12–16 → **12–16 Tage** angesetzt. Für die übrigen Phasen hielt kein Reviewer die Schätzung für falsch. **Die Schätzung wird nach Phase 1 neu gesetzt.** Phasen 1–2 ergeben schon eine nutzbare App ohne Hintergrund-Ortung – Plan B.

### 5a. Messbare Kriterien für die Machbarkeitsspitze

Je Plattform, auf einer Fahrt von mindestens 90 Minuten mit gesperrtem Bildschirm, Handy in der Tasche:

| Messgröße | Bestanden, wenn | Reviewer |
|---|---|---|
| Erkannte Orte | ≥ 90 % der durchfahrenen Korridore lösen einen Hinweis aus (Tunnelabschnitte ausgenommen) | 5 passt, 1 wollte 80 % |
| Verspätung | Hinweis kommt, solange das Fahrzeug noch im Korridor ist; Korridore unter 3 Minuten Fahrzeit gelten nicht | 6 passt (1 mit dieser Ergänzung) |
| Fehlalarme | ≤ 1 je Stunde | 5 passt, 1 wollte 0,5 |
| Akku | **Abbruch bei > 10 %/h** zusätzlich; **Ziel ≤ 6 %/h** (mit Geofence statt Dauer-GPS erreichbar) | 3 passt, 2 wollten 5–6 %, 1 wollte 15 % |
| Hinweis | Text wird bei Sperre vollständig gesprochen **oder** Vibration + Benachrichtigung kommen an; Stimme allein darf nicht das einzige Signal sein | 6 passt (1 mit Vibrations-Zusatz) |
| Wiederaufnahme | Nach Beenden durch das System: beim nächsten Öffnen steht der letzte Spielstand innerhalb von 30 s, keine neue Runde. Ein selbsttätiger Neustart der App wird nicht verlangt. | 5 passt, 1 mit dieser Präzisierung |

Protokoll: Zeit, GPS-Position, ausgelöster Ort, gesprochener Text – als Datei auf dem Gerät, danach am PC ausgewertet, **dann gelöscht** (Bewegungsprofil).

## 6. Plattform-Besonderheiten

**Apple (iOS)**
- Hintergrund-Ortung braucht den Hintergrund-Modus `location` und die Berechtigung „Immer“. Der Dialog für „Immer“ kommt pro Installation nur einmal; eine Ablehnung ist nur über die Einstellungen zu heilen → Erklärbildschirm vor dem Dialog (Phase 3).
- Höchstens 20 überwachte Regionen je App → Geofence-Fenster (Abschnitt 4).
- Die Begründungstexte für die Berechtigungen (in der Info.plist) müssen den Zweck konkret nennen; vage Texte sind ein häufiger Ablehnungsgrund.
- Sprachausgabe bei Sperre braucht zusätzlich den Hintergrund-Modus `audio`; Apple prüft dessen Verwendung getrennt von der Ortung.
- Wird die App von der Spielerin weggewischt, endet die Ortung bis zum nächsten Öffnen – Regel des Systems, kein Plugin-Fehler. Hinweis in die Einführung.
- Richtlinie 4.2 (Mindestfunktionalität): Hintergrund-Ortung und native Stimme sind der Mehrwert gegenüber der Webseite; so in den Prüfer-Notizen begründen.
- Richtlinie 5.2 (geistiges Eigentum): Quellenseite in der App beugt Rückfragen vor.
- Drei getrennte Pflichten: (1) Datenschutzangaben im Store, (2) Berechtigungstexte in der App, (3) Privacy Manifest – ob und wofür (3) nötig ist, hängt von den genutzten APIs und Plugins ab und wird in Phase 5 anhand der konkreten Toolchain geprüft.
- Build nur auf macOS mit Xcode oder über einen Cloud-Build-Dienst (Abschnitt 8, Nr. 4). iPad: Die App muss dort zumindest sinnvoll laufen; Hochformat-Layout genügt.
- Entwicklerkonto 99 USD/Jahr.

**Android**
- Hintergrund-Ortung über Geofences des Systems, ergänzt um einen Vordergrund-Dienst mit dauerhafter Benachrichtigung während der Fahrt; „Standort im Hintergrund“ ist seit Android 10 eine **zweite, getrennte** Berechtigungsfrage – eine Ablehnung dort macht die Ortung stumm, ohne dass die Spielerin es merkt → Zustand sichtbar anzeigen (Phase 3).
- Höchstens 100 Geofences je App.
- Play Console 25 USD einmalig; Datensicherheits-Formular; Google verlangt für Hintergrund-Standort eine gesonderte Begründung und ein Video des Anwendungsfalls; die Prüfung kann Wochen dauern.
- Akku-Sparmodi einzelner Hersteller beenden Dienste; Offline-Sprachausgabe klingt je Hersteller unterschiedlich oder fehlt → Vibration + Benachrichtigung als Rückfall, Beta auf mindestens zwei Herstellern.

**Beide**
- Ein Nachweis auf einer Plattform gilt nicht für die andere; die Kriterien in 5a werden je Plattform erfüllt.
- Ortung beginnt nur nach bewusstem „Fahrt starten“ und endet mit „Fahrt beenden“ – kein Dauer-Tracking. Das ist zugleich das Argument gegenüber beiden Store-Prüfungen.
- Wake Lock wird in der App überflüssig; im Browser-Rückfall bleibt er.
- Datenschutz: Positionen werden nur auf dem Gerät verarbeitet, nichts geht an einen Server. Damit entfällt eine Einwilligung über die Systemberechtigung hinaus; eine Datenschutzerklärung (Store-Pflicht beider Anbieter) ist trotzdem nötig und sagt genau das.
- Quellen- und Lizenzseite in der App (Wikipedia CC BY-SA 4.0, GeoBasis-DE/BKG, Wikidata CC0) – gilt bereits für die Webseite.
- Name „QuizAway“: Ein Reviewer nennt eine US-Marke (Klasse 41, 2019), unbelegt. **Fester Termin vor Phase 5:** DPMA/EUIPO prüfen, auch „Quiz-Away“ und „Quiz Away“.

## 7. Risiken

Jedes Risiko hat einen Prüfzeitpunkt und ein Abbruchkriterium.

| Risiko | Folge | Gegenmittel | Prüfung | Abbruch, wenn |
|---|---|---|---|---|
| Hintergrund-Ortung unzuverlässig | Hauptgrund für die App entfällt | Machbarkeitsspitze zuerst; Plan B | Phase 1 | Kriterien 5a auf iOS verfehlt |
| Geofence-Ereignis erreicht bei entladener WebView keinen Hinweis | App schweigt genau im Zustand, für den sie gebaut wird | Hinweis-Schicht nativ (Abschnitt 4); in Phase 1 ausdrücklich mit entladener WebView testen | Phase 1 | Hinweis braucht JavaScript |
| Geofence-Grenze (iOS 20, Android 100) | Orte verpasst | Geofence-Fenster mit Nachschub bei jedem Übergang; Rückfall: periodische Positionsprüfung | Phase 1 | Fenster-Nachschub verpasst Orte |
| Akku und Wärme über 3 Stunden Fahrt | Spielerin schaltet ab | Geofence statt Dauer-GPS; Takt dicht/normal/ruhig | Phase 1, Beta | > 10 %/h |
| GPS ungenau, Ort übersprungen, Hinweis zu spät | Spiel wirkt kaputt | Korridor je Ort weiten; verpasster Ort beim nächsten Halt nachholen („Du bist eben durch X gefahren“) | Phase 1 | < 90 % erkannt |
| Stimme bei Sperre stumm oder je Gerät schlecht | Hinweis geht unter | Hintergrund-Modus `audio`; Vibration + Benachrichtigung immer zusätzlich | Phase 1, Beta | Apple lehnt `audio` ab **und** Vibration reicht nicht |
| Berechtigung nur „bei Nutzung“ / „ungefähr“ / zweiter Android-Dialog abgelehnt / später entzogen | App schweigt ohne Erklärung | Erklärbildschirm; Zustand sichtbar („Ortung aus – antippen“) | Phase 3 | – (Gestaltung) |
| App vom System beendet oder weggewischt | Runde verloren, Ortung aus | Spielstand nach jedem Zug sichern; Hinweis in der Einführung | Phase 2 | – |
| Nachgeladenes Paket passt nicht zum Spielstand | Karten fehlen oder doppeln | Paketversion im Spielstand; Prüfung beim Start | Phase 4 | – |
| Kein Mac verfügbar | iOS-Build nur über Cloud, Fehlersuche mühsam | Abschnitt 8 Nr. 4 vor Phase 1 klären | Phase 0 | – |
| Plugin verwaist (ein Maintainer) oder bricht mit neuer iOS/Android-Version | Wartungslast auf eine Person | schmale Schnittstelle (< 200 LOC Wechsel); Ersatz-Plugins benannt; jährlicher Prüftermin nach den Herbst-Releases | Phase 1, dann jährlich | – |
| Store-Richtlinien verschärfen sich nach Veröffentlichung | App fliegt aus dem Store oder Update blockiert | Plan B bleibt veröffentlichbar; jährlicher Prüftermin | jährlich | – |
| Apple lehnt „Immer“-Ortung als unnötig ab | Kernfunktion fehlt auf iOS | Ortung nur nach „Fahrt starten“; Begründung im Prüfer-Hinweis; **Plan B:** Zwischenstand nach Phase 2 (Vordergrund + Wake Lock + Hinweis „Bildschirm an lassen“) | Phase 7 | zweite Ablehnung nach Nachbesserung |
| Google-Prüfung des Hintergrund-Standorts dauert Wochen | Termin rutscht | Phase 5 früh einreichen; kein fester Veröffentlichungstermin versprechen | Phase 5 | – |
| Fahrtprotokoll als Bewegungsprofil | Datenschutz | lokal, nach Auswertung löschen | Phase 1 | – |
| Store-Texte, Screenshots, Datenschutz unterschätzt | Verzögerung | Phase 5 mit Checkliste | Phase 5 | – |
| Karten mit wörtlichen Quellsätzen | Richtlinie 5.2 | Prüfskript auf lange gleiche Wortfolgen (ohne Modell), vor Phase 5 | Phase 5 | – |

## 8. Was Mike entscheidet und von Hand macht (Hebel)

1. **Ob überhaupt** – reicht die Webseite mit Wake Lock für den Alltag? Der Feldtest auf dem iPhone (liegt bei Mike) zeigt das. Vor dieser Antwort wird nichts gebaut.
2. **Wann** – nicht vor dem 5.11.; danach konkurriert die App mit weiteren Orten und Regionen um das Tagesbudget.
3. **Go/No-Go nach Phase 1** – Mike liest das Fahrtprotokoll und entscheidet gegen die Kriterien in 5a. **Entschieden (Mike 17.10.):** Akku-Abbruch bei 10 %/h, Ziel 6 %/h.
4. **Mac für Phase 1** – die Reviewer sind 3:3 zwischen „Mac leihen“ und „Cloud-Build (GitHub-Actions-macOS-Runner oder Codemagic)“. **Mike 17.10.: kein Mac zum Leihen.** Ein Mac ist nicht zwingend: Build, Signatur und TestFlight-Upload laufen über einen macOS-Runner in der Cloud; getestet wird auf dem iPhone über TestFlight; Fehler in der App-WebView kommen über das Fahrtprotokoll (Logdatei mit Teilen-Knopf) ans Licht, weil ohne Mac der Safari Web Inspector fehlt. **Entschieden (Mike 17.10.):** für Phase 1 einen Mac mini in der Cloud **mieten** (Scaleway oder MacinCloud, Remote-Desktop, voller Xcode) – schnelle Build-Zyklen ohne Kauf; Kauf eines gebrauchten Mac mini erst nach bestandenem Go/No-Go. Apple-Entwicklerkonto in jedem Fall nötig.
5. **Entwicklerkonten** anlegen (Apple, Google) – Identität, Zahlung, Verträge: nur Mike.
6. **Fahrten für Phase 1 und Beta** – nur echte Fahrten zeigen, ob Pings bei Sperre ankommen. **Testgerät (Mike 17.10.: kein eigenes iPhone, nur iPad):** Für Build, TestFlight und Bedienung genügt das iPad. Für die Messung in 5a braucht es ein Gerät mit GPS – das haben nur iPad-Modelle „Wi-Fi + Cellular“; ein reines Wi-Fi-iPad ortet nur über WLAN und ist im Auto und in der Bahn blind. **Entschieden (Mike 17.10.):** Testgerät ist das iPad Air 4. Generation (2020, Wi-Fi + Cellular, eigener GPS-Empfänger, aktuelles iPadOS; keine SIM nötig, GPS arbeitet ohne Mobilfunk). Phase 1 misst damit; Akkuwerte sind nur Richtwert, weil der iPad-Akku größer ist. Die Beta läuft zusätzlich auf dem iPhone der Tochter (TestFlight-Einladung), weil das die Zielplattform ist.
7. **Markenprüfung, Store-Texte, Screenshots** – fester Termin vor Phase 5.
8. **Beta-Tester** auswählen (Familie, Freunde; mindestens ein Android-Gerät eines zweiten Herstellers).

## 9. Fragen an den Reviewer

Die zweite Reviewrunde (6 Antworten) ist ausgewertet (Abschnitt 12). Offen bleiben nur die zwei Punkte bei Mike (Abschnitt 8, Nr. 3 und 4). Eine dritte Runde ist erst nach Phase 1 sinnvoll, mit dem Fahrtprotokoll als Grundlage.

## 10. Nicht Teil dieses Plans

- Mehrspieler / Duell (eigene Konzepte unter `docs/konzepte/quizaway-7a-*`, ruhen)
- Neue Spielfamilien oder Regionen (laufen in der Daten-Kette weiter, unabhängig von der App)
- Einnahmen, Preismodell, Werbung
- Ein Beginn der Phasen 1–2 vor dem 5.11.

## 11. Änderungen v0.2 → v0.3

- **Zielbild:** Hinweis-Schicht nativ, ohne JavaScript (3 Reviewer: Geofence-Ereignis erreicht die entladene WebView nicht). Geofence-Fenster wegen der Grenze von 20 (iOS) / 100 (Android) Regionen (3 Reviewer). Phase 1 um 1 Tag, Phase 3 um 1 Tag erhöht.
- **Plugin:** Capgo festgelegt (6/6); Ersatz Community oder Transistorsoft.
- **Aufwand Phase 1 + 3:** 12–16 Tage (Mitte der sechs Spannen).
- **5a:** Tunnel ausgenommen; Korridore unter 3 min gelten nicht; Akku als Abbruch 10 %/h + Ziel 6 %/h (Entscheid Mike offen); Hinweis = Stimme **oder** Vibration + Benachrichtigung; Wiederaufnahme präzisiert („beim nächsten Öffnen, 30 s“); Protokoll löschen.
- **Risiken neu:** Geofence-Ereignis ohne WebView, Geofence-Grenze, Paketversion vs. Spielstand, Store-Richtlinien später, Google-Prüfdauer, Fahrtprotokoll, zweiter Android-Dialog, Android-Stimmqualität.
- **Markenprüfung** mit festem Termin vor Phase 5.
- **Abschnitt 9** geschlossen; Abschnitt 12 neu.

## 12. Auswertung der zweiten Reviewrunde (6 Antworten)

| Frage | Ergebnis | Übernommen |
|---|---|---|
| 1 App lohnt? | 6× Ja | ja |
| 2 Capacitor? | 6× Ja | ja |
| 3 Plugin | 6× Capgo erste Wahl; Ersatz 4× Community, 2× Transistorsoft; 6× „Geofences ja“ (alle nach Dokumentation, keiner nach Test) | ja, Test in Phase 1 |
| 4 Mac Phase 1 | 3× leihen, 3× Cloud; danach 3× Cloud, 2× kaufen, 1× leihen | Entscheid Mike (8.4) |
| 5 Aufwand 1+3 | 10–16 / 10–15 / 12–16 / 10–14 / 12–18 / 12–16 | 12–16 |
| 6 SQLite | 6× beibehalten | ja |
| 7 Risiken | 20 Stichpunkte, 8 neue Risiken übernommen (Abschnitt 11) | teilweise |
| 8 Kriterien | Erkannt: 5 passt / 1× 80 % · Verspätung: 6 passt · Fehlalarm: 5 passt / 1× 0,5 · Akku: 3 passt / 5 % / 6 % / 15 % · Stimme: 6 passt · Wiederaufnahme: 5 passt / 1 präzisiert | Mehrheit, Akku offen |

**Nicht übernommen nach Faktencheck:**
- „Google Play untersagt seit Ende Oktober 2026 Vordergrunddienste nur für Geofencing“ (DeepSeek) – Datum liegt nach dem heutigen Tag, nicht belegbar; die Android-Umsetzung nutzt ohnehin System-Geofences und den Dienst nur während „Fahrt“.
- „iOS 26 startet nach Force-Quit Region-Monitoring nicht mehr neu“ (DeepSeek) – das war nie anders: Nach Wegwischen ruht jede Ortung bis zum nächsten Öffnen (steht in Abschnitt 6). Die Präzisierung des Kriteriums „Wiederaufnahme“ ist trotzdem richtig und übernommen.
- Erkannte Orte 80 % (GLM) – Tunnel werden ausgenommen, damit bleibt 90 % haltbar.
- Akku 15 %/h (Qwen) – widerspricht dem Zweck der Geofences; abgelehnt.
- „Offline-Fähigkeit nachladbarer Pakete durch Store-Restriktionen gefährdet“ (Qwen) – kein bekannter Mechanismus.
- Ersatz Transistorsoft als Paketname: `@transistorsoft/capacitor-background-geolocation` (von GLM/Qwen richtig genannt; in Runde 1 falsch).
