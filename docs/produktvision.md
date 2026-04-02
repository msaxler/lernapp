# Produktvision — QuizAway & Xalento (Lern-App)

*Version 1.1 · April 2026 · DOK-3 v10*

Produktvision
QuizAway & Medien-Lern-App
Zwei Apps — ein gemeinsames Fundament
Version 1.0 · März 2026 · Konsolidiertes Dokument (DOK-3)
Dieses Dokument beschreibt die Produktvision beider Projekte aus Nutzerperspektive.
Es fasst zusammen was die Apps leisten, für wen sie gemacht sind und wie sie sich zueinander verhalten.
Technische Details sind in DOK-1 (Fundament-Technik) dokumentiert.

## Teil A — Gemeinsame Leitprinzipien

Beide Apps teilen dieselben Leitprinzipien. Sie sind kein Dekor — sie sind Korrektiv. Wann immer eine Entscheidung schwierig wird, liefern sie die Richtung. Das erste Prinzip ist ein Werteprinzip, die übrigen sind Designprinzipien.

### A.1  Dezentralität & individuelle Autarkie
Das übergeordnete Werteprinzip: Dezentrale Organisation so weit wie möglich. Ziel ist die höchste erreichbare Autarkie auf individueller Nutzer-Ebene — kein Nutzer soll von einem zentralen Dienst abhängig sein um die App zu nutzen, seine Daten zu besitzen oder seine Identität zu behalten.

Dieses Prinzip ist kein technisches Detail — es ist eine Grundhaltung die jede Architekturentscheidung prägt. Es zeigt sich auf allen Ebenen:

Ebene
Ausprägung
Konsequenz

Identität
Keypair lokal generiert — kein Account, kein Server, keine E-Mail
Nutzer besitzt seine Identität vollständig

Verbreitung
Out-of-Band via Messenger — kein App-Store, kein Registrierungszwang
App verbreitet sich über Vertrauen, nicht über Infrastruktur

Datenhaltung
Lernfortschritt und Spielstand lokal — kein Cloud-Zwang
Daten gehören dem Nutzer, nicht dem Anbieter

Sync
P2P via WebRTC, Relay via Nostr — kein eigener Server
Synchronisation ohne zentrale Infrastruktur

Payment
Lightning / Nostr-Zap — kein App-Store-Zwang, keine 30% Provision
Monetarisierung ohne Torwächter

Backup
Verschlüsselt, lokal exportierbar, Wiederherstellungsphrase
Datenverlust ausgeschlossen, kein Lock-in

Leitfrage fuer jede neue Entscheidung: Macht das den Nutzer abhaengiger von einer externen Infrastruktur — oder autonomer? Im Zweifel: autonomer.

### A.2  Paretos Gesetz — 80/20
Vilfredo Pareto (1896) beobachtete: 20 % der Ursachen erklären 80 % der Wirkungen. In der Softwareentwicklung übersetzt: 20 % der Funktionen decken 80 % des Nutzens. Der Rest kostet 80 % der Entwicklungszeit für 20 % des Wertes.

Pareto ist das Korrektiv gegen Feature-Creep. Die Frage ist nicht ob eine Funktion nützlich wäre — sondern ob sie zu den 20 % gehört die 80 % des Wertes liefern. Alles andere kommt später, wenn überhaupt.

Ebene
Pareto bedeutet konkret
Anti-Pattern

Funktionsumfang
Die wichtigsten 3–5 Features zuerst vollständig — nicht 20 Features halbfertig
Breite statt Tiefe, nichts ist wirklich fertig

Datenpools
Erst den staedte-Pool vollständig — er deckt 80 % der Quizfragen
Alle 15 Pools gleichzeitig halb befüllen

Plattformen
Smartphone zuerst — es ist 80 % der Nutzung
Desktop und Smartphone gleichzeitig optimieren

Algorithmen
SM2 für Phase 1 reicht — FSRS bringt 20 % mehr Effizienz bei 5× mehr Aufwand
Den perfekten Algorithmus vor dem ersten Nutzer bauen

Pareto + KISS zusammen: Nicht nur weglassen (KISS) — sondern das Richtige zuerst tun (Pareto). Die 20 % die 80 % des Wertes liefern identifizieren und zuerst bauen.

### A.3  KISS — Keep It Simple, Stupid
Geprägt von Kelly Johnson, Chefingenieur bei Lockheed Skunk Works (SR-71 Blackbird): Jedes Design muss von einem Mechaniker unter Kampfbedingungen reparierbar sein. Was nicht einfach genug ist, kostet im Ernstfall Leben — oder Nutzer.

KISS bedeutet nicht Dummheit — es bedeutet Disziplin. Die schwierigste Designentscheidung ist nicht hinzuzufügen, sondern wegzulassen. Einfachheit ist kein Ausgangszustand, sie ist ein Ergebnis harter Arbeit.

Ebene
KISS bedeutet konkret
Anti-Pattern

UX / Interface
Jeder Screen hat eine Hauptaufgabe. Navigation ist intuitiv ohne Anleitung.
Zu viele Optionen gleichzeitig, überladene Screens, versteckte Funktionen

Architektur
Jede Komponente hat eine klar abgegrenzte Verantwortung. Abhängigkeiten sind minimal.
Verschachtelte Abstraktionsebenen, vorauseilende Generalisierung, Over-Engineering

Code
Einfache Lösungen zuerst. Komplexität nur wenn das Problem es wirklich verlangt.
&quot;Kluge&quot; Lösungen die nur der Autor versteht. Frameworks für triviale Probleme.

### A.4  Millers Law — Die Magische Sieben
George A. Miller (1956): Das Arbeitsgedächtnis kann zuverlässig ca. 7 ± 2 Einheiten gleichzeitig im Blick behalten. Mehr führt zu Überlastung, Fehlern und Kontrollverlust. Cowan (2001) präzisiert: die eigentliche Grenze liegt eher bei 4 ± 1 ohne Gedächtnishilfen.

Ebene
Konkrete Regel
Begründung

Explorer / Grid
Max. 3×4 = 12 Knoten sichtbar — 1 hervorgehoben, Rest zurückgetreten
Daumennavigation erfordert minimale kognitive Last pro Schritt

Navigationshierarchie
Empfehlung: max. 7 Ebenen tief
Tiefere Strukturen verlieren den Kontext — der Nutzer weiß nicht mehr wo er ist

Architektur & API
Max. 7 Parameter / Optionen pro Schnittstelle
Mehr als 7 erzwingen Dokumentation statt Intuition — das ist ein Designfehler

Designregel für beide Projekte: Vor jeder neuen Funktion steht die Frage: &quot;Kann ich das weglassen — und hat der Nutzer trotzdem alles was er braucht?&quot; Wenn eine Funktion erklärt werden muss, ist das Design gescheitert.

### A.5  Verbreitungsstrategie — Einstiegshürde null
Beide Apps folgen derselben Verteilungsstrategie: kein App-Store-Zwang, keine Registrierung, keine Kreditkarte beim ersten Kontakt. Verbreitung läuft über bestehende Vertrauensnetzwerke — ein Link per Threema, Signal oder E-Mail reicht.

Phase
Trigger
Verbreitung / Payment

1 — Jetzt
Start
Out-of-Band via Messenger · vollständig kostenlos · Einstiegshürde null

2 — Wachstum
### 10.000 aktive Nutzer
Relay-Events + automatische Weitergabe · PayPal / Wero / Lightning nachziehen

3 — Masse
Bewusste Entscheidung
App-Store als Ergänzung · Freemium optional

Payment wird nachgezogen, nicht eingeführt. Die Basisversion bleibt kostenlos. Nur wer mehr will, zahlt. Wer nicht zahlt, verliert nichts.

### A.6  Onboarding-Prinzip — Erfolgserlebnis in unter 60 Sekunden

*Erkenntnisse aus Duolingo-Analyse, April 2026*

Nutzer kommen beim ersten Start so schnell wie möglich zur ersten Erfolgserfahrung — kein Setup, keine Registrierung, keine Erklärung, direkt spielen.

**Erster Start:** Nutzer spielen sofort 3 Beispielkarten des gewählten Themas — ohne Setup, ohne Registrierung, ohne Erklärung. FSRS-Feedback erscheint nach der ersten Karte. Erst danach optional: Deck wählen, Einstellungen. Ziel: Erfolgserlebnis in unter 60 Sekunden.

**Warum kritisch:** Xalento hat keinen Streak-Zwang als Rückkehrer-Mechanismus. Das macht das erste Erlebnis umso entscheidender — wer beim ersten Start keinen Wert sieht, kommt nicht wieder. Der externe Lerndruck (Auftritt, Klassenarbeit) existiert bereits — Xalento muss ihn nicht erzeugen, sondern das angenehmste Werkzeug dafür sein.

## Teil B — QuizAway

QuizAway ist ein Anwendungsfall der Lern-App — spielerisches Geo-Lernen als erste Spezialisierung.
QuizAway wird zuerst fertiggestellt und geht dann in die Lern-App-Plattform auf.
Es teilt Codebasis, Datenpools, Identitätsmodell und Sync-Architektur mit der Lern-App.
Geo-spezifische Features (Virtuelle Route, GTFS, Städtedatenbank) sind Ausprägungen des allgemeinen Lernraum-Modells.

### B.1  Vision
QuizAway ist ein deutsches Geografie-Quiz das sich anfühlt wie eine Reise. Keine trockenen Hauptstadtfragen — sondern lebendige Fragen über Städte, Flüsse, Bahnstrecken, Kennzeichen und Höhenlagen. Die Virtuelle Route verbindet Quizfragen zu einer Reise durch Deutschland: Wer von Hamburg nach München fährt, erlebt die Städte auf dem Weg.

Kernidee: Ein Quiz das wächst. Mit normalisierten Datenpools entstehen neue Fragen automatisch — kein manuelles Erstellen. Neue Daten → sofort neue Fragen.

### B.2  Zielgruppe
Deutschland-Begeisterte: Menschen die gerne mehr über ihr Land wissen möchten
Familien und Freundesgruppen: gemeinsames Spielen im Duel-Modus
Reisende: die Virtuelle Route macht Bahnfahrten zum Quiz-Erlebnis
Schulen: Geografie-Wissen spielerisch auffrischen

### B.3  Spielmodi
Modus
Beschreibung
Status

Sofa-Modus
Alleine spielen, Kategorie wählen, 3 Fragen pro Runde, kein Zeitdruck — kein Timer
Vorhanden

Virtuelle Route
Eine Reise von A nach B — Fragen über Städte entlang der Strecke — kein Timer
In Entwicklung

Live-Modus
Gemeinsam spielen ohne Gegeneinander, gleiche Fragen gleichzeitig — kein Timer
Geplant

Duel-Modus
Zwei Spieler spielen gegeneinander, gleiche Fragen, Echtzeit-Vergleich — **Timer aktiv** (14 s/Frage)
Geplant (AP13)

Liga
Wöchentliche Rangliste über alle Spieler, Auf-/Abstieg
Geplant

**Timer-Designentscheidung:** Der Spieltimer (14 s/Frage) ist bewusst auf den Duell-Modus beschränkt. In allen anderen Modi (Sofa, Virtuelle Route, Live) gibt es keinen Zeitdruck — Lernentscheidungen brauchen Raum. Timer erzeugt nur dort sinnvollen Wettkampf-Reiz, wo er direkt an eine Spielsituation gebunden ist.

**Naming offen:** Der Duell-Modus kann extern unter einem anderen Namen (z. B. „Lernbattle") vermarktet werden. Entscheidung bis LA-16 (Launch). Interner Code-Name bleibt „duell".

### B.4  Fragenkategorien
Kategorie
Beispielfrage
Status

Geografie
In welchem Bundesland liegt Augsburg?
Aktiv

KFZ-Kennzeichen
Welches Kennzeichen gehört zu Lübbecke?
Aktiv

Einwohner
Welche Stadt hat ungefähr so viele Einwohner wie Rostock?
Aktiv

Distanz & Lage
Welches Nachbarland liegt Saalfeld am nächsten?
Aktiv

Höhenlage
In welchem Höhenbereich liegt Dortmund?
Aktiv

Deutsche Bahn
Welche Stadt liegt an der ICE-Strecke Berlin–Köln?
Aktiv

Geschichte
Welche Stadt ist älter — Jena oder Berlin?
Gesperrt (geplant)

Persönlichkeiten
Geburtsort berühmter Menschen
Gesperrt (geplant)

Sport
Vereine, Stadien, Meisterschaften
Gesperrt (geplant)

Kulinarik
Spezialitäten und Getränke
Gesperrt (geplant)

Historische Persönlichkeiten
Wer hat hier gelebt, wurde hier geboren, gewirkt oder ist hier gestorben? (z. B. „In welcher Stadt wurde Albert Einstein geboren?")
Gesperrt (geplant)

Fun Facts
Wissen das keiner braucht — aber alle wissen wollen (z. B. „Welche Stadt hat den längsten Straßennamen Deutschlands?")
Gesperrt (geplant)

### B.5  Generatives Fragenmodell
Heute sind QuizAway-Fragen statische Text-Strings: Frage, vier Antworten, fertig. Das System weiß nicht was die Frage bedeutet. Das Ziel ist ein generatives System: Fragen entstehen zur Laufzeit aus drei Zutaten — Daten, einem Fragetyp und einer Methode. Neue Daten bedeuten sofort neue Fragen ohne manuelles Erstellen.

Heute — Statisch
Ziel — Generativ

{ text: &quot;Hauptstadt von Bayern?&quot;, antworten: [&quot;München&quot;, ...] }
{ pool: &quot;bundeslaender&quot;, objekt_id: &quot;Bayern&quot;, fragetyp: &quot;attributabfrage&quot;, attribut: &quot;hauptstadt&quot; }

Neue Daten → manuelles Erstellen nötig
Neue Daten → sofort neue Fragen

Frage ist ein Text-String
Frage ist ein beschreibbares Objekt

Distraktoren manuell gewählt
Distraktoren automatisch generiert nach Strategie

### B.6  Ausgangspunkt & Migrationspfad

*Architekturentscheidung April 2026 — aktualisiert gegenüber DOK-3 v9*

QuizAway existiert heute als standalone HTML-Datei — das ist der Ausgangspunkt, nicht das Ziel. Die HTML-Datei ist ein funktionierendes UX und eine funktionierende Spielmechanik.

**Revidiertes Migrationsprinzip: Neubau statt schrittweise Migration**

Die ursprünglich geplante 4-Schritt-Migration (Datenpools → Event-Ledger → Nostr → Player-Typ) wird ersetzt durch einen **Neubau auf dem Xalento-Stack**. Grund: Der Choir Trainer (LA-6–LA-8) hat bewiesen, dass React + TypeScript + Vite + Dexie.js + PWA eine vollständig stabile, offline-fähige App ergibt — ohne Serverabhängigkeiten im Betrieb. QuizAway auf demselben Stack neu zu bauen ist sauberer als die HTML-Datei schrittweise umzubauen.

**Local-First Architektur — Serverabhängigkeiten auf das Minimum reduziert**

```
QuizAway (neu, Xalento-Stack)
│
├── Sofa-Modus          → 100 % lokal · kein Server · offline-fähig
├── Virtuelle Route     → 100 % lokal · kein Server · offline-fähig
├── Live-Modus          → 100 % lokal · kein Server · offline-fähig
│
└── Duell-Modus         → minimaler Server (Signaling + TURN)
                           Spiel selbst läuft P2P nach Handshake
```

Fragenpools (geo.sqlite / JSON) werden gebündelt oder per Service Worker gecacht — genau wie MusicXML-Dateien im Choir Trainer. Nach dem ersten Laden ist kein Netzwerk mehr nötig — außer für den Duell-Modus.

**Die zwei strukturell unvermeidbaren Server-Ausnahmen (nur Duell-Modus):**

| Ausnahme | Warum unvermeidbar | Lösung |
|---|---|---|
| WebRTC Signaling | Zwei Geräte brauchen einen Treffpunkt für den Handshake | Always-On WebSocket (kein Render Free Tier) |
| TURN-Server | NAT-Traversal Mobilnetz ↔ WLAN scheitert ohne Relay | Eigener coturn oder bezahlter Dienst |

Nach dem Verbindungsaufbau läuft das Duell-Spiel vollständig P2P — kein Server mehr involviert.

**Was das konkret bedeutet:**
- Sofa, Route, Live: stabil wie der Choir Trainer — keine Serverabhängigkeit, keine Cold-Start-Probleme
- Duell: zwei klar definierte Serverdienste, beide wartbar und skalierbar
- Alle Stabilitätsprobleme der aktuellen Implementierung (Render Cold Start, OpenRelay, HTTP-Polling) werden strukturell eliminiert

Verteilungsweg heute
Vorteil
Im Zielbild

E-Mail-Anhang
Direkter Kontakt, kein Download-Link nötig
Bleibt als Option — kleinere Datei durch Datentrennung

Google Drive Download
Immer aktuelle Version, beliebige Dateigröße
Bleibt als Option

Nostr / P2P (Ziel)
Viral, kein zentraler Server, automatische Updates
Langfristiges Ziel — nach Neubau auf Xalento-Stack

### B.7  Duel-Modus — Spielablauf & Protokoll
Der Duel-Modus ist ein Echtzeit-Zweispielermodus über WebRTC P2P (DataChannel). Beide Spieler spielen dieselben Fragen — deterministisch generiert aus einem gemeinsamen Seed. Der Rendezvous-Server hat zwei klar getrennte Aufgaben: einmalig den WebRTC-Handshake vermitteln (Signaling), und dauerhaft den Warteraum betreiben in dem sich Duell-Partner finden. Nach dem Verbindungsaufbau ist kein zentraler Server mehr nötig — das gesamte Spiel läuft direkt zwischen den Geräten.

Warteraum & Matchmaking (CAS-Modell)
Die Spieler-Paarung im Warteraum basiert auf einem Compare-and-Swap (CAS)-Modell. Jeder Spieler hat einen Zustand (FREE, CLAIMED, PAIRED, LEFT). Der Server entscheidet atomar innerhalb eines einzigen Locks wer Host und wer Guest wird — Race Conditions sind damit strukturell ausgeschlossen. Die vollständige Spezifikation (Datenstrukturen, Zustandsautomat, Pseudocode, Sequenzdiagramm) ist im separaten Dokument &quot;QuizAway — Warteraum & Matchmaking&quot; beschrieben.
Zustand
Bedeutung

FREE
Im Warteraum, noch nicht gepaart, wählbar

CLAIMED
Kurzzeitiger Zwischenzustand während CAS-Operation — nicht mehr wählbar

PAIRED
Partner zugewiesen, verlässt den Warteraum

LEFT
Manuell verlassen — wird sofort aus dem Pool entfernt

Garantie: Jeder Spieler verlässt den Warteraum garantiert — entweder mit einem echten Partner oder mit dem immer verfügbaren virtuellen Gegner. Livelock und Deadlock sind durch den Zustandsautomaten strukturell ausgeschlossen.

Rollen
Rolle
Beschreibung

Herausforderer (Host)
Erstellt den Raum, erhält die PIN, wählt die Kategorie in Runde 1, 3 und bei Führung in Runde 5

Herausgeforderter (Guest)
Tritt mit PIN bei, wählt die Kategorie in Runde 2 und 4 sowie bei Führung in Runde 5

Rundenstruktur — 5 Runden
Runde
Kategorie-Wahlrecht
Besonderheit

1
Herausforderer
Einstiegsrunde

2
Herausgeforderter
Gegenzug

3
Herausforderer
Mittelteil

4
Herausgeforderter
Spannung aufbauen

5
Führender (Sonderregel)
Entscheidungsrunde — Kategorie noch nicht gespielt

Sonderregel Runde 5 — Wahlrecht
Wahlrecht hat der Spieler mit mehr Punkten nach Runde 4.
Bei Punktegleichstand: der Spieler mit der kürzeren Gesamtantwortzeit (Summe aller Antwortzeiten Runde 1–4).
Bei wiederum Gleichstand: Zufall (coin flip via Seed).
Die gewählte Kategorie muss eine sein, die in Runden 1–4 noch nicht gespielt wurde. Sind alle gespielt: die am wenigsten gespielte Kategorie (bei Gleichstand Zufall).

Synchronisationsprinzip
Jede Runde ist synchronisiert: Beide Spieler spielen ihre 3 Fragen — durch den Spieltimer (14s pro Frage, Zwangsweiterschalten) endet jede Runde spätestens nach 42 Sekunden. Erst wenn beide ihr Runden-Ergebnis gesendet haben, wird der Vergleich angezeigt und die nächste Runde freigeschaltet.
Timer-Übersicht — alle Screens
Screen
Timer
Normal
Debug ×10
Zweck

Schwierigkeit
Initialanzeige
14s
140s
Zwangsweiter ohne Wahl

Schwierigkeit
Nach Klick auf Karte
5s
50s
Kurzer Delay nach Auswahl

Kategorie-Wahl
Runde 1
28s
280s
Mehr Zeit für erste Wahl

Kategorie-Wahl
Runden 2–5
14s
140s
Zwangsauswahl Kategorie

Frage
Pro Frage
14s
140s
Zeitablauf = 0 Punkte

Zwischen-Feedback
Nach Antwort
14s
140s
Zwangsweiter nach Feedback

Rundenabschluss Solo/Route
Zwangsweiter
14s
140s
Nächste Runde starten

Rundenabschluss Duell
Mit Wahlrecht
3s+14s
3s+140s
3s Mindestdelay + 14s Zwangsweiter (eigener Timer)

Rundenabschluss Duell
Wartend (kein Wahlrecht)
30s FB
300s FB
Fallback falls Gegner nicht reagiert (FB = Fallback)

Duell Ping
Verbindungscheck
alle 5s
alle 5s
Gegner erreichbar? Kein ×10

Duell Abbruch
Nach 3 fehlenden Pings
~30s
~30s
Runde mit 0 Punkten werten. Kein ×10

Timeout durch eingebauten Spieltimer: kein separater Timeout nötig.
Nächste-Runde-Button gesperrt bis Gegner-Ergebnis via DataChannel eintrifft.
Bei Verbindungsabbruch: 30s warten, dann Runde mit 0 Punkten für Gegner werten.

Nachrichten-Protokoll (DataChannel)
Nachricht
Sender
Inhalt

hello
beide, beim Verbindungsaufbau
{ type:'hello', name, rolle:'host'|'guest' }

kat
Wähler der Runde
{ type:'kat', katId, seed, runde }

runde
beide, nach Rundenende
{ type:'runde', runde: { richtig, punkte, ergebnisse[], zeitMs } }

ping
beide, alle 5s
{ type:'ping' } — Verbindung überwachen

abbruch
bei Aufgabe
{ type:'abbruch' } — Gegner gewinnt automatisch

Zustandsdiagramm
Beide Spieler durchlaufen denselben Zustandsautomaten synchron:
Zustand
Beschreibung

VERBINDEN
PIN eingeben oder anzeigen — Rendezvous-Handshake

WARTEN_KAT
Warten auf kat-Nachricht (Guest) oder Kategorie wählen (Host/Führender)

SPIELEN
3 Fragen beantworten — Timer läuft

WARTEN_ERGEBNIS
Eigene Runde fertig — warten auf Gegner-Runde-Nachricht

ERGEBNIS
Vergleich anzeigen — beide sehen Punkte und Dots

SPIELENDE
Nach Runde 5: Gesamtergebnis, Gewinner, XP-Vergabe

ABGEBROCHEN
Verbindungsabbruch oder Aufgabe — Gegner gewinnt

Punkte & Zeiterfassung
Punkte pro Frage: 120 minus 3× Antwortzeit in Sekunden, mindestens 10 Punkte bei richtiger Antwort, 0 bei falscher.
Antwortzeit: Zeitstempel bei Fragenanzeige und bei Antwort-Klick — Differenz in ms.
Gesamtzeit pro Spieler: Summe aller Antwortzeiten über alle Runden — Tiebreaker in Runde 5.
Runden-Ergebnis enthält: richtig (0–3), punkte (0–360), ergebnisse[] mit {korrekt, punkte, zeitMs} pro Frage.

Verbindungsaufbau — Ablauf
## 1. Herausforderer öffnet Duell-Screen → klickt 'Raum erstellen' → PIN erscheint
## 2. Herausgeforderter öffnet Duell-Screen → gibt PIN ein → klickt 'Verbinden'
## 3. WebRTC-Handshake via Rendezvous-Server (Offer/Answer/ICE)
## 4. DataChannel offen → hello-Nachrichten → Runde 1 startet automatisch
## 5. Ab jetzt kein zentraler Server mehr nötig — reines P2P

Implementierungs-Hinweise für AP13 Neuimplementierung
Neuer duellP2PState trennen von duellState (Simulation) — kein gemeinsamer State.
Zeiterfassung: frageStartZeit = Date.now() beim Anzeigen, zeitMs = Date.now() - frageStartZeit beim Klick.
Runde-5-Wahlrecht: nach Runde 4 Gesamtpunkte + Gesamtzeit vergleichen, dann kat-Nachricht senden.
Kategorie-Gedächtnis: gespielteKategorienDuell: Set<string> — für Runde-5-Filter.
Verbindungsabbruch: ping alle 5s, bei 3 ausgebliebenen Pings: ABGEBROCHEN-Zustand, Gegner gewinnt.

## Teil C — Medien-Lern-App

Die Medien-Lern-App ist inhaltsneutral — sie spielt ab was in der Lernraumtopologie verknüpft ist. Die App muss von den Inhalten nichts wissen. Dieselbe App funktioniert für Chorübung, Führerschein, Sprachenlernen und Jagdschein.

### C.1  Vision
Eine inhaltsneutrale App für jeden strukturierten Lerninhalt der aus Mediendateien besteht. Das Grundprinzip ist bewusst einfach: Ein Inhaltsersteller bereitet Mediendateien vor und legt sie strukturiert in einer Lernraumtopologie ab. Der Lernende navigiert mit der App durch diese Topologie und spielt die Inhalte gezielt ab.

### C.2  Anwendungsbeispiele
Anwendungsfall
Typische Inhalte
Besonderheit

Chorübung (Phase 1)
MusicXML, MP3 (Stimmen getrennt), Rhythmustext
Erster Anwendungsfall — prägt alle Architekturentscheidungen

Führerschein-Theorie
JSON-Fragenkatalog (amtlicher BMDV-Datensatz)
Klarer Prüfungstermin, hoher Leidensdruck — ideal für Duel-Modus

Sprachenlernen
JSON-Fragen, Audio, PDF
Fragen-JSON ist sprachagnostisch — Sprache ist nur ein Datenpaket

Jagdscheinprüfung
PDF, kurze Videos, Audio (Wildrufe)
Audio-Identifikation als Fragetyp

Nachhilfe Mathematik
Erklär-Videos, PDF-Aufgabenblätter, Audio
Strukturierte Lernpfade nach Themengebieten

Instrumentalübung
MusicXML, MP3, Video
Analog zur Chorübung

### C.3  Entwicklungsphasen
Phase
Zielgruppe
Beschreibung

1 — Jetzt
Nur für den Entwickler
Erster Anwendungsfall: Chorübung. Lokal im Heimnetz, kein Cloud-Account nötig.

2 — Wachstum
Alle Nutzer weltweit
Jeder Nutzer bringt seinen eigenen Cloud-Account mit. Nextcloud, kDrive oder kompatibel.

3 — Inhaltsersteller
Inhaltsersteller
Einfache Vorbereitungsoberfläche direkt in der App — kein PC-Script mehr nötig.

### C.4  Die Lernraumtopologie
Die Lernraumtopologie ist das konzeptionelle Fundament der App. Der Lernraum ist eine Landschaft aus Knoten und Verbindungen — unabhängig von jeder physikalischen Infrastruktur. Täler und Pässe beschreiben natürliche Lernpfade, aber es gibt auch Querwege für Fortgeschrittene. Denselben Gipfel (Lernziel) kann man über verschiedene Routen erreichen.

Knoten — Die Lerneinheit
Inhalt: Mediendatei oder Frageobjekt (MP3, MusicXML, PDF, JSON-Quiz ...)
Schwierigkeit: numerischer Wert 0–1, item-spezifisch kalibriert
Typ: Medien-Knoten oder Quiz-Knoten
Verbindungen: Liste der Kanten zu anderen Knoten
Lernstatus: individuell pro Nutzer

Drei Typen von Verbindungen
Typ
Entstehung
Analogie

Autor-definiert
Inhaltsersteller setzt explizite Kanten
Der markierte Wanderweg

Attribut-basiert
System berechnet Ähnlichkeit automatisch (Themenfeld, Konzeptfeld, Niveau)
Der Kompass

Lernpfad
Entsteht durch echtes Lernverhalten nach Hebbs Regel
Der Trampelpfad

Navigationsmodi
Modus
Analogie
Wer führt?

Freie Navigation (Explorer)
Selbstständige Wanderung ohne Karte
Der Lernende wählt jeden Schritt selbst

Geführter Modus
Geführte Tour mit erfahrenem Guide
Die Spaced-Repetition-Engine schlägt vor

Duel-Modus
Wettrennen durch dieselbe Landschaft
Beide Spieler, gemeinsame Knotenauswahl

### C.5  Layout & Bedienung
Das Layout ist für Smartphone-Hochformat optimiert und funktioniert ebenso auf Tablet und PC. Grundprinzip: 60/40 — obere 60 % Inhaltsdarstellung, untere 40 % Steuerung, optimiert für Einhandbedienung mit dem Daumen.

Modus
Oben 60 %
Unten 40 %

Explorer
Knotenansicht (Topologie-Grid)
Navigationspfeile + Auswahltaste

Player
Inhaltsdarstellung
Player-Steuerung

### C.6  Spaced Repetition Engine
Das technische Herzstück des Geführten Modus. Die Engine entscheidet welcher Lernknoten als nächstes wiederholt werden soll — adaptiv, fehlergewichtet und domain-neutral.

Phase
Algorithmus

Phase 1
SM2-Algorithmus (1987, Grundlage von Anki, Duolingo, Memrise) — einfach, gut dokumentiert

Phase 2
FSRS (Free Spaced Repetition Scheduler) — entwickelt aus 700 Mio. echten Reviews, 20–30% weniger Wiederholungen bei gleicher Retentionsrate

Designprinzip: Belohnungen müssen echten Wissenszuwachs widerspiegeln — nicht Klickzahlen
Die Forschung zeigt: Gamification wirkt, aber nur wenn die spielerischen Elemente direkt zur Lernaufgabe passen. Bedeutungslose Badges und globale Ranglisten koennen die intrinsische Motivation sogar untergraben (Undermining Effect). Xalento verfolgt deshalb einen anderen Ansatz: Gamification die echten Lernfortschritt sichtbar macht.

Ebene 1 — Wissens-Visualisierung
Die staerkste Gamification ist die Scheduling-Transparenz aus dem FSRS-System — konsequent als Fortschrittsanzeige pro Karte visualisiert. Der Lernende sieht nicht abstrakte Punkte sondern konkreten Inhalt:

```
Zellkern      ████████░░  "Sicher"   — wieder in 12 Tagen
Mitochondrium ██████░░░░  "Lernend"  — wieder morgen
Zellmembran   ██░░░░░░░░  "Neu"      — heute noch einmal
```

Das ist Motivation durch Bedeutung: der Lernende versteht zu jedem Zeitpunkt was er weiss und was noch aussteht.

Ebene 2 — Lernkette statt Streak
Duolingo bestraft den Nutzer wenn er einen Tag aussetzt. Das erzeugt Stress und Prokrastination. Xalento macht es anders:
•  Nicht: Tag 7 in Folge — das bestraft Aussetzer
•  Stattdessen: Diese Karte kennst du seit 3 Wochen zuverlaessig — das ist ein Erfolg der bleibt
•  Fokus liegt auf dauerhaftem Wissen, nicht auf taeglicher Disziplin
•  Optionaler Hinweis: Du hast heute noch 8 Karten faellig — als Information, nicht als Pflicht

Ebene 3 — Duell-Modus
Zwei Lernende treten gegeneinander an — technisch aus QuizAway uebernommen, thematisch an den Lerninhalt gebunden. Nicht Geografie-Quiz sondern Biologie-Fragen, Chemie-Fragen, Geschichte. Der Wettbewerb ist sinnvoll weil er direkt am Lerninhalt haengt.
•  Warteraum-Matchmaking: Spieler sehen sich und waehlen ihren Gegner
•  5 Runden, Wahlrecht wechselt nach Rundenergebnis
•  Ergebnis zeigt Punkte und welche Karten beide beherrschen
•  Optional: Runde 5 als Joker-Runde mit Spezialregel

Ebene 4 — Klassen-Dashboard (Lehrer-Ansicht)
Lehrer sieht nicht wer die hoechste Punktzahl hat sondern wer welche Karten sicher beherrscht. Das ist paedagogisch sauber:

```
Klasse 5b — Thema Zellaufbau
Emma  ████████░░  8/10 Karten sicher
Leon  ██████░░░░  6/10 Karten sicher
Mia   ████░░░░░░  4/10 Karten sicher  ← braucht Unterstuetzung
```

| Anzeige | Bedeutung |
|---|---|
| 8/10 Karten sicher | Lernender beherrscht das Thema gut |
| 4/10 Karten sicher | Lernender braucht Unterstuetzung |
| Heute faellig: 5 | Wie viele Wiederholungen stehen an |
| Letzte Aktivitaet: gestern | Wann zuletzt gelernt — ohne Druck |

Bewusst NICHT in Xalento
Element
Grund fuer Ausschluss

Badges fuer Klickzahlen
Bedeutungslos — kein Bezug zum Lerninhalt

Globale Ranglisten
Erzeugen Neid und Ausgrenzung bei schwaecheren Lernenden

Pflicht-Streaks
Bestrafen Aussetzer — erzeugen Stress statt Freude

Leben/Herzen
Bestrafen Fehler — aber Fehler sind Teil des Lernens

Punkte fuer Zeit
Verleitet zu Schnelligkeit statt Verstaendnis

Forschungsbasis
Metaanalyse Bai et al. (2020), 3.202 Schuelerinnen: signifikanter positiver Effekt (g=0.50) auf Lernleistung durch Gamification. Entscheidend: Spielelemente muessen direkt zur Lernaufgabe passen und Belohnungen muessen unmittelbar nach der Aufgabe erfolgen. Globale Ranglisten und isolierte Punktesysteme koennen durch den Undermining Effect die intrinsische Motivation sogar verringern (Ninaus, 2025).

### C.7  KI-gestützte Inhaltsgenerierung (Phase 2+)

*Erkenntnisse aus Learn-Battle-Analyse, April 2026*

Redakteure und Lehrkräfte können PDFs, Lehrpläne oder Textdokumente hochladen. Die Anthropic-API extrahiert daraus Karteikarten, MC-Fragen und Lückentext-Aufgaben. Alle generierten Inhalte durchlaufen die kuratierte Redaktions-Pipeline (digitale Signatur) bevor sie in den P2P-Pool eingehen. Kein Nutzer erhält unkuratierte KI-Inhalte.

**Warum Pareto-kompatibel:** Für BioLearn könnten Lehrkräfte Lehrplankapitel als PDF einreichen, für den Chor-Coach Probennotizen — sofort Karten, kein manueller Aufwand. Technisch kein neuer Stack: Anthropic-API wird bereits genutzt.

**Voraussetzungen:** Redaktions-Pipeline aktiv (nach LA-13) · Anthropic-API-Anbindung · Kurationsprozess definiert

**Zurückgestellt bis:** Phase 2+ (nach LA-13 + LA-15)

### C.8  Chorübung — Erster Anwendungsfall
Die Chorübung ist der erste konkrete Anwendungsfall (Phase 1) und prägt alle Architekturentscheidungen. Entwickelt für den Chor SingOn, Stimme Bass 2.

Dreiphasiger Übungszyklus
Phase
Beschreibung
Nutzeraktion

A — Zuhören
Sequenz wird abgespielt, Score und Text laufen mit
Zuhören, Internalisieren — keine Aktion

B — Singen
App spielt letzten N Takte als Anlauf, dann Aufnahme
Mitsingen, Tempo wählbar 50–150 %

C — Bewertung
Selbsteinschätzung (Phase 1), Mikrofon-Analyse (Phase 2)
Nochmal / Fast / Gut / Perfekt wählen

MusicXML-Rendering
MusicXML wird direkt auf dem Smartphone gerendert via OSMD (OpenSheetMusicDisplay, Version 1.9.6, Stand März 2025). Kein Server-Rendering, keine Vorab-Konvertierung. Da MusicXML live gerendert wird, entstehen keine Klangverzerrungen beim Tempowechsel — kein Chipmunk-Effekt wie bei MP3-Streckung.

### C.9  Strategisches Ziel-Fach: Biologie Sekundarstufe 1
Die Chorübung (C.8) ist der erste Anwendungsfall wegen persönlicher Expertise und überschaubarem Umfang. Als strategisches Ziel-Fach für die Skalierungsphase ist jedoch Biologie Sekundarstufe 1 vorgesehen. Diese Entscheidung ist inhaltlicher Natur — die Plattform-Architektur bleibt identisch.
Warum Biologie Sek1?
Kriterium
Begründung

Offene Datenbasis
Wikidata (Arten, Ökosysteme, Anatomie), Serlo.org (CC-BY-SA), Wikimedia Commons (Bilder) — alles frei lizenziert und automatisiert abrufbar

Lehrplan als Kurationsraster
Öffentliche Lehrpläne (gemeinfrei) definieren klar welche ~50–100 Fakten pro Klassenstufe prüfungsrelevant sind — kein Raten welche Inhalte wichtig sind

Zielgruppe mit Lernbedarf
Klassen 5–10 haben messbaren Lernbedarf (Schulabschluss), Eltern zahlen für Lernhilfe, Markt ist groß und wenig durch offene Angebote abgedeckt

Motivationsvorteil
Biologie ist von Natur aus visuell, lebendig und emotional ansprechend — intrinsische Faszination ohne künstliche Gamification-Krücken

Warum Biologie besonders viel Spaß macht
Mathematik ist abstrakt — Spaß muss erst konstruiert werden. Geographie ist interessant aber statisch. Biologie dagegen hat intrinsische Faszination: es geht um Lebewesen, um den eigenen Körper, um Tiere die man kennt und liebt. Ein Kind das lernt wie das Herz funktioniert lernt gleichzeitig etwas über sich selbst. Das ist motivational ein qualitativer Unterschied zu fast allen anderen Schulfächern.
Dazu hat Biologie auf jeder Klassenstufe emotionale Anker: Grundschule — Schmetterlingskreislauf, Jahreszeiten, Haustiere. Sek1 — eigener Körper, Ökosysteme, Evolution. Das sind Themen die Kinder von sich aus interessieren. Die App muss dieses Interesse nur aufgreifen, nicht erst erzeugen.
Player-Typen für Biologie Sek1
Biologie Sek1 hat drei Wissenstypen die unterschiedliche Player-Formate fordern. Der Quiz-Player der bereits existiert deckt Typ 1 ab. Für Typ 2 und 3 werden neue Player-Typen benötigt:
Player
Wissenstyp
Beispiel
Spaß-Faktor

Quiz-Player ✓
Faktenwissen
Welches Organ produziert Insulin?
Tierfotos, Makroaufnahmen — wirkt wie Sammelkarten

Beschriftungs-Player
Strukturwissen
Bild einer Zelle — nummerierte Pfeile beschriften
Frosch-Skelett, Haifisch-Gebiss — visuell fesselnd

Zuordnungs-Player
Strukturwissen
Tier → Lebensraum zuordnen (Drag & Drop)
Fühlt sich an wie ein Sammelkartenspiel

Lückentext-Player
Prozesswissen
Bei der Fotosynthese wird ___ in ___ umgewandelt
Rätsel-Charakter, niedrige Einstiegshürde

Sortierspiel-Player
Prozesswissen
Nahrungskette in richtige Reihenfolge bringen
Narrative Qualität — Gras → Hase → Fuchs

Der Beschriftungs-Player ist dabei der wertvollste Neuzugang — er deckt den häufigsten Aufgabentyp in Biologie-Schulbüchern ab und existiert in dieser Form kaum als offene Lösung. SVG-Bilder aus Wikimedia Commons liefern die Datenbasis. Langfristig ist auch ein Kamera-Player denkbar: Pflanze fotografieren, bestimmen, einordnen — Biologie als Entdeckungsspiel in der realen Welt.
Strategische Einordnung: Chorübung ist Phase-1-Pilot wegen persönlicher Expertise. Biologie Sek1 ist das strategische Ziel-Fach für die Skalierungsphase — wegen offener Datenbasis, lehrplankonformem Kurationsraster, größerer Zielgruppe, und einem einzigartigen Motivationsvorteil den kein anderes Schulfach in dieser Kombination bietet.
Die Plattform-Architektur bleibt identisch — der Fachwechsel ist eine inhaltliche Entscheidung, kein Umbau.

### C.10  Technologie-Entscheidungen
Bereich
Entscheidung

Frontend
React + TypeScript — größtes PWA-Ökosystem, TypeScript für Typsicherheit

Distribution
PWA statt native App — kein App-Store-Prozess, sofortige Updates, trotzdem auf Homescreen installierbar

Backend Phase 1
Kein eigenes Backend — direkte Kommunikation mit WebDAV / Nextcloud

MusicXML
OSMD — aktiv gepflegt, WebGL-Beschleunigung in Chrome/Edge

Audio
Tone.js — Audio-Wiedergabe, Tempo-Kontrolle, MusicXML-Synthese

Noten-Sync
WaveSurfer.js für MP3-Visualisierung

Explorer
Eigenbau — Standard-Komponenten sind auf Desktop/Maus ausgelegt, Einhandbedienung erfordert Eigenbau

### C.10  Datensouveränität & Identität
Die Identität des Lernenden wird nicht von einem Server vergeben — sie entsteht lokal auf dem Gerät. Ein kryptographisches Schlüsselpaar (secp256k1, identisch mit Nostr) wird beim ersten Start erzeugt, ohne Account, ohne E-Mail, ohne Registrierung. Der öffentliche Schlüssel ist die Identität. Der private Schlüssel bleibt ausschließlich auf den Geräten des Lernenden.

Datenkategorie
Gehört wem / Verlässt die Geräte?

Lernfortschritt (stability, Termine)
Dem Lernenden · nur verschlüsselt (opt-in)

Persönliches Wegenetz (Pfadstärken)
Dem Lernenden · nur anonym aggregiert (opt-in)

Topologie + Inhalte
Dem Autor / Backend · liegt im gewählten Backend

Aggregierte Pfadstatistik
Dem Netz (anonym) · ja — aber ohne Personenbezug

### C.11  Lernformen & Player-Typen
Was unterscheidet Lernformen wirklich? Die Frage ist nicht was man lernt, sondern wie der Lernprozess funktioniert. Dafür gibt es in der Lernwissenschaft ein etabliertes Raster: Blooms Taxonomie der Lernziele, ergänzt durch die Frage nach dem Medientyp und der Interaktionsform.

Drei Dimensionen bestimmen den Lerntyp

Dimension
Ausprägungen

Kognitive Tiefe (Bloom)
Stufe 1 Erinnern · Stufe 2 Verstehen · Stufe 3 Anwenden · Stufe 4 Analysieren · Stufe 5 Bewerten · Stufe 6 Erschaffen

Interaktionsform
Rezeptiv: konsumieren (Zuhören, Lesen, Ansehen) — Reproduktiv: abrufen (Multiple Choice) — Produktiv: erzeugen (Schreiben, Sprechen, Lösen)

Medientyp des Inhalts
Symbolisch: Text, Formeln, Noten — Auditiv: Sprache, Musik, Wildrufe — Visuell: Bilder, Videos — Motorisch: Ausführen, Nachahmen

Konkrete Lernformen im Vergleich
Dieselbe Lernform kann sehr unterschiedliche kognitive Tiefen und Interaktionsformen erfordern — das bestimmt welcher Player-Typ gebraucht wird:

Lernform
Kognitive Tiefe / Interaktion
Benötigter Player

Führerschein-Theorie
Stufe 1–3 · reproduktiv · symbolisch — Fakten und Regeln abrufen
Quiz-Player (95% abgedeckt)

Sprachenlernen Vokabeln
Stufe 1 · reproduktiv · symbolisch/auditiv
Quiz-Player

Sprachenlernen Aussprache
Stufe 3 · produktiv · auditiv — Mikrofon, Pitch, Rhythmus
Performance-Player

Sprachenlernen Grammatik
Stufe 3–4 · produktiv · symbolisch — Umformungen, Lückentexte
Eingabe-Player

Chorübung Zuhören
Stufe 1–2 · rezeptiv · auditiv/symbolisch
Media-Player

Chorübung Singen
Stufe 3 · produktiv · auditiv — Pitch und Rhythmusmessung
Performance-Player

Mathematik Klasse 6
Stufe 3 · produktiv · symbolisch — Rechnen, nicht Multiple Choice
Eingabe-Player (Kern), Quiz-Player (Grundwissen)

Jagdscheinprüfung
Stufe 1–3 · rezeptiv + reproduktiv — Audio-Identifikation
Media-Player + Quiz-Player

Philosophie Bachelor
Stufe 4–6 · produktiv · symbolisch — Analysieren, Argumentieren, Erschaffen
Analyse-Player (Phase 3+)

Fünf Player-Familien
Aus dieser Analyse ergeben sich fünf Player-Familien. Alle teilen dieselbe Infrastruktur — Explorer, Event-Ledger, Spaced Repetition, Gamification, Sync. Nur der Player-Kern variiert:

Player-Typ
Lernform / Beispiele
Phase

Media-Player
Rezeptiv · 60/40-Layout · MusicXML, MP3, Video, PDF · Chorübung Phase A, Jagdschein
1

Quiz-Player
Reproduktiv · Frage + 4 Antworten + Timer · QuizAway, Führerschein, Vokabeln
1

Performance-Player
Produktiv auditiv · Mikrofon + Feedback · Chorübung Phase B/C, Aussprache
1

Eingabe-Player
Produktiv symbolisch · Texteingabe, Formel, Lückentext · Mathematik, Grammatik
2

Analyse-Player
Produktiv komplex · Essay, Argumentation · Philosophie, Jura, Literaturwissenschaft
3+

Architekturprinzip: Die Infrastruktur ist für alle Player identisch.
Was variiert ist ausschließlich der Player-Kern — der Screen zwischen Aufgabe zeigen und Antwort bewerten.
QuizAway ist der Quiz-Player. Er wird als Player-Typ in die Lern-App eingebracht.
Das 60/40-Layout gilt nur für Media-Player und Performance-Player — nicht für Quiz- und Eingabe-Player.

## Teil D — QuizAway als erste Spezialisierung der Lern-App

QuizAway ist kein paralleles Projekt zur Lern-App — es ist ihr erster konkreter Anwendungsfall. Die Lern-App ist die allgemeine Plattform, QuizAway ist die erste Spezialisierung: spielerisches Geo-Lernen. QuizAway wird zuerst fertiggestellt und geht dann in die Lern-App auf.

Architekturprinzip: Generalisierung durch Konkretisierung.
QuizAway löst das allgemeine Problem zuerst für einen spezifischen Fall — Geo-Quiz.
Alles was dabei entsteht (Datenpools, Fragengerator, Event-Ledger, Sync) ist von Anfang an
so gebaut dass es die Lern-App-Plattform trägt.

### D.1  Gemeinsames Fundament — einmal bauen, zweimal nutzen
Baustein
QuizAway nutzt es als...
Lern-App nutzt es als...

Normalisierte Datenpools
Geo-Wissensbasis (staedte, bundeslaender, flüsse ...)
Beliebige Wissensobjekte je Lerninhalt

Generatives Fragenmodell
Geo-Fragen aus Datenpools (attributabfrage, vergleich ...)
Lernfragen aus allen Pool-Typen

Fragenkataloge
Führerschein, Jagdschein als statische Kataloge
Dieselben Kataloge, gleiche Schnittstelle

Event-Ledger
Spielstände, Duel-Ergebnisse, XP
Lernfortschritt, Wiederholungstermine, XP

Nostr-Identität
Spieler-ID, verschlüsselte Duel-Kommunikation
Lernenden-ID, Sync zwischen eigenen Geräten

WebRTC + Nostr-Sync
Duel-Modus, Ranglisten-Sync
Geräte-Sync, Chor-Gruppe, Lern-Duelle

Gamification-Schema
Punkte, Ligen, Streaks für Quiz-Runden
Punkte, Ligen, Streaks für Lerneinheiten

PWA-Shell
Offline-Quiz-App, installierbar
Offline-Lern-App, installierbar

### D.2  Was QuizAway spezialisiert
QuizAway fügt dem allgemeinen Fundament geo-spezifische Ausprägungen hinzu. Diese sind keine Ausnahmen vom Modell — sie sind Instanziierungen davon:

QuizAway-Spezialisierung
Allgemeines Lern-App-Konzept dahinter

Virtuelle Route (Hamburg → München)
Geführter Modus: didaktisch sequenzierter Lernpfad

Geo-Datenpools (staedte, flüsse, bahnstrecken)
Normalisierte Wissensobjekte mit Attributen und Relationen

KFZ-Kennzeichen-Fragen
Zuordnungs-Fragetyp: Pool A → Pool B

Höhenlagen-Vergleich
Vergleichs-Fragetyp: numerisches Attribut über mehrere Objekte

Duel auf der Strecke
Duel-Modus: zwei Lernende, gleiche Fragen, Echtzeit

GTFS-Bahnstrecken
Externe Datenquelle → normalisierter Pool via Pipeline

### D.3  Warum QuizAway zuerst
QuizAway ist weiter fortgeschritten, hat eine existierende Nutzerbasis und klare Anforderungen. Es dient als Testbed für das gemeinsame Fundament — jede Komponente die für QuizAway gebaut wird, wird direkt für die Lern-App wiederverwendet. Der Umweg über QuizAway ist kein Umweg — er ist der schnellste Weg zur Lern-App.

Schritt
Was entsteht — und wer nutzt es

## 1. QuizAway: Datenpools (AP1–AP4)
Normalisierte SQLite-DB · sofort: QuizAway · später: Lern-App als erster Wissenspool

## 2. QuizAway: Event-Ledger (AP5)
JS-Modul · sofort: QuizAway-Spielstände · später: Lern-App-Lernfortschritt

## 3. QuizAway: Nostr-Sync (AP7+8)
Sync-Infrastruktur · sofort: QuizAway-Duel · später: Lern-App-Geräte-Sync

## 4. QuizAway: Fragengerator (AP9)
Generative Engine · sofort: Geo-Fragen · später: alle Fragetypen

## 5. QuizAway: PWA Shell (AP11)
App-Grundgerüst · sofort: QuizAway · später: Lern-App-Basis

## 6. QuizAway fertig (AP12+13)
Vollständige App · Datengrundlage und Erfahrung für Lern-App

## 7. Lern-App Phase 1
Chorübung auf demselben Fundament · Explorer, Player, MusicXML, SM2

## 8. QuizAway geht auf
QuizAway wird Profil der Lern-App · eine Codebasis, viele Anwendungsfälle

Offene Punkte

QuizAway — als erste Spezialisierung
Kategorien Geschichte, Persönlichkeiten, Sport, Kulinarik: zurückgestellt — Pareto, erst wenn Kernkategorien vollständig
Liga-System: öffentlich (entschieden)
Migration: 4-Schritt-Migrationspfad entschieden — Datenpools → Event-Ledger → Nostr-Sync → Quiz-Player als Profil in der Lern-App (schrittweise)

Lern-App
Persistenz-Backend final entscheiden: Nextcloud vs. kDrive vs. lokal
Dateiformat und Struktur der didaktischen Datei (Lernreihenfolge, Spaced Repetition)
UI-Konzept für den Geführten Modus
Kanten-Editor: Wie definiert der Inhaltsersteller Verbindungen zwischen Knoten? (Phase 3)
Aggregationsprotokoll für Schicht 3 (anonyme Pfadstatistik): wieviel Anonymisierung ist genug?

Gemeinsam
Payment-Strategie: Ab wann und wie? PayPal Webhook vs. Lightning / NIP-57 Zap
App-Store: Wann und ob — Abwägung 30% Provision vs. Reichweite
Schutzstrategie: Markenname, ggf. Gebrauchsmuster für die Spielmechanik