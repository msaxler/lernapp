# Projektplanung — QuizAway & Xalento

*Version 2.4 · März 2026 · DOK-2 v17 · AP1–AP13 abgeschlossen · Xalento LA-1–LA-12*

Projektplanung
QuizAway & Medien-Lern-App
Arbeitspakete · Abhängigkeiten · Status
Version 2.4 · März 2026 · Stand: AP1–AP12 abgeschlossen · AP13 aktiv · KFZ-Datenqualität geprüft · 0 Lücken >20k EW
Leitprinzip: Jedes Arbeitspaket ist in sich abgeschlossen und liefert ein konkretes, testbares Ergebnis.
Abhängigkeiten sind explizit — wer kein Vorgänger-AP braucht, kann sofort gestartet werden.
Pareto-Regel: Der kritische Pfad QuizAway spielbar hat Vorrang vor allem anderen.

## 1.  Übersicht aller Arbeitspakete

AP
Name
Status
Voraussetzungen
Projekte

AP1
GeoNames Basispools
abgeschlossen
—
QuizAway, Lern-App

AP2
Geometrie-Pipelines
offen
AP1
QuizAway, Lern-App

AP3
DE-spezifische Pools
offen
AP1
QuizAway

AP4
Translations & Schablonen
abgeschlossen
AP1
QuizAway, Lern-App

AP5
Event-Ledger-Modul
abgeschlossen
—
QuizAway, Lern-App

AP6
WebRTC PoC
abgeschlossen
—
QuizAway, Lern-App

AP7
Nostr Relay PoC
abgeschlossen
—
QuizAway, Lern-App

AP8
Ledger-Merge P2P
abgeschlossen
AP5 + AP6
QuizAway, Lern-App

AP9
Fragengerator PoC
abgeschlossen
AP1
QuizAway, Lern-App

AP10
SQLite Build-Pipeline
abgeschlossen
AP1–AP4
QuizAway, Lern-App

AP11
PWA Shell
abgeschlossen
—
QuizAway, Lern-App

AP12
QuizAway spielbar
abgeschlossen
AP1+5+6+9+10+11
QuizAway

AP13
Duel-Modus
aktiv
AP5+6+7+8+12
QuizAway

Legende: grün = abgeschlossen · gelb = aktiv · weiß/grau = offen
Parallel startbar ohne jede Voraussetzung: AP1, AP5, AP7, AP11.

Abhängigkeitsketten
Kritischer Pfad QuizAway spielbar: AP1 → AP9 + AP10 (parallel) → AP12
Kritischer Pfad Duel-Modus: AP6 ✓ → AP8 → AP13 (parallel zu Datenpools)
Lern-App Fundament: AP1 + AP5 + AP7 → AP4 + AP8 (alle parallel startbar)

## 2.  QuizAway — Kritischer Pfad

QuizAway ist der erste fertigzustellende Anwendungsfall — und Testbed für das gemeinsame Fundament.
Pareto: AP1 → AP9 → AP12 sind die 20% die 80% des Wertes liefern. Alles andere ist nachrangig.
Jedes AP das für QuizAway gebaut wird, ist direkt für die Lern-App wiederverwendbar.

Schritt-für-Schritt zum spielbaren QuizAway
Schritt
AP
Was entsteht

1
AP1  (sofort startbar)
SQLite mit staat, bundesland, kreis, stadt — Basis für alle Fragen

2a
AP9  (nach AP1)
Fragengerator: generateQuestion() liefert erste echte Geo-Fragen

2b
AP5  (parallel)
EventLedger-Klasse: Spielstand überlebt Browser-Reload

2c
AP11 (parallel)
PWA Shell: App installierbar, läuft offline

3
AP3  (nach AP1)
KFZ-Kennzeichen, Bahnhöfe, Bahnstrecken — DE-spezifische Kategorien

4
AP4  (nach AP1)
Translations: name_de, name_en für alle Pools

5
AP10 (nach AP1–AP4)
Build-Pipeline: vollständige questions.sqlite für alle Kategorien

6
AP12 (nach allem)
QuizAway spielbar: Fragen aus DB, Spielstand persistent, offline

7
AP7  (parallel)
Nostr PoC: asynchrones Signaling — Basis für Duel ohne Rendezvous-Server

8
AP8  (nach AP5+AP6)
Ledger-Merge: zwei Geräte tauschen Spielstände — Basis für Rangliste

9
AP13 (nach AP12+AP7+AP8)
Duel-Modus: zwei Spieler, deterministisch, Echtzeit

## 3.  Arbeitspakete — Details

### 3.1  Datenpools (AP1–AP4)

### AP1  —  GeoNames Basispools    [abgeschlossen]

Voraussetzungen
Keine — sofort startbar

Projekte
QuizAway, Lern-App

Output
SQLite: staat, bundesland, kreis, stadt (ebene='stadt')

Technologie
Python, GeoNames-Dump (allCountries.zip), Destatis-CSV

Testkriterium
SELECT COUNT(*) FROM stadt WHERE staat_id='DE' → ca. 12.000 Einträge

Aufgaben
GeoNames allCountries.zip herunterladen und parsen
Filter: featureCodes P/PPL*, P/PPLA*, A/ADM* für politische Einheiten
staat, bundesland, kreis, stadt befüllen · ISO-3166-Codes als IDs
Referenzintegrität prüfen: alle FK-Verweise auflösbar

### AP2  —  Geometrie-Pipelines (PLZ)    [abgeschlossen]

Voraussetzungen
AP1 abgeschlossen

Projekte
QuizAway

Output
### 8.174 PLZ · plz_stadt-Verknüpfung · München 80331–80999 ✓ · 10/10 Checks ✓

Technologie
Python, suche-postleitzahl.org CSV (OSM-basiert), GeoPandas + BKG VG250 vorbereitet

Testkriterium
SELECT plz FROM plz_stadt WHERE stadt_id=München → 80331, 80333... ✓

Aufgaben
zuordnung_plz_ort.csv (suche-postleitzahl.org): 8.174 PLZ mit Ort + Bundesland
plz-Tabelle: id, staat_id, osm_id — 8.174 Einträge
plz_stadt-Tabelle: PLZ↔Stadt über deutschen Ortsnamen verknüpft
Pareto: CSV-Ansatz statt räumlicher Verschneidung — ausreichend für Fragengerator
geo.sqlite jetzt 17.7 MB mit allen Datenpools
PLZ-Fragengerator: 2 Typen × 1500 Städte = 3000 Fragen · Leicht/Mittel/Schwer
Ladezeit optimiert: GROUP BY MIN statt korrelierten Subquery → ~1s Gesamtladezeit
Phase 2: räumliche Verschneidung mit BKG VG250 Polygonen für spätere Erweiterung

### AP3  —  DE-spezifische Pools    [abgeschlossen]

Voraussetzungen
AP1 abgeschlossen

Projekte
QuizAway

Output
400 KFZ-Kennzeichen · 419 Landkreise · BKG VG250-Matching · 4000 KFZ-Fragen spielbar

Technologie
Python, Destatis GV100, KBA AGS5-KFZ-Tabelle, BKG VG250 GeoPackage, GeoPandas

Testkriterium
M→München ✓ · FR→Freiburg ✓ · HD→Heidelberg ✓ · HN→Heilbronn ✓ · 9/9 Checks ✓

Aufgaben
Destatis GV100: 419 Landkreise mit AGS5 (Satzart 4, feste Breite, Pos 10-14)
AGS5_KFZ-Tabelle (KBA Stand 09/2025): 400 Kennzeichen verknüpft
BKG VG250 GeoPackage: 10.956 Gemeinden mit deutschen Namen → sauberes Stadt→Kreis-Matching
build_ags_mapping.py: VG250 → ags_gemeinde_kreis.csv (AGS8 + Name + Kreis-AGS5)
KFZ-Fragengerator: 2 Fragetypen × 2000 Städte = 4000 Fragen, alle Schwierigkeiten
Hessen-Korrekturen: GI/GG/LM/LDK/VB/MTK/RÜ — systematisch via GV100 geprüft
Manuelle Fixes: Limburg an der Lahn, Mülheim an der Ruhr, Oldenburg (Oldenburg)
check_kfz_luecken.py: 0 Städte >20.000 ohne Kennzeichen ✓
KFZ-Kategorie freigeschaltet und vollständig spielbar
AP2/PLZ Phase 2: BKG VG250 Polygone für räumliche Verschneidung vorgemerkt

### AP4  —  Translations & Schablonen befüllen    [abgeschlossen]

Voraussetzungen
AP1 abgeschlossen

Projekte
QuizAway, Lern-App

Output
geo.sqlite: 7.063 deutsche Alternativnamen + 5 Schablonen · QuizAway liest Fragetexte aus DB

Technologie
Python, GeoNames alternateNamesV2.zip, ap1_build_pools.py + quizaway_v4.html

Testkriterium
getSchablone('attributabfrage','bundesland_id') → DB-Eintrag ✓ · München statt Munich ✓ · 8/8 Checks ✓

Aufgaben
alternateNamesV2.zip: 7.063 Städtenamen auf Deutsch aktualisiert (München, Köln, Nürnberg…)
schablonen-Tabelle: 5 Einträge für attributabfrage, schaetzung_bereich, vergleich_max
QuizAway v4: getSchablone() + applySchablone() — Fragetext aus DB, nicht aus Code
Architektur-Beweis DOK-1 C.2a: neue Sprache = neue DB-Zeilen, kein Code-Change
Fallback-Logik eingebaut: alte DB ohne schablonen-Tabelle funktioniert weiter
Pareto: lang='en' und Wikidata zurückgestellt — für spätere Internationalisierung

### 3.2  Kommunikation & Core (AP5–AP8)

### AP5  —  Event-Ledger-Modul    [abgeschlossen]

Voraussetzungen
Keine — sofort startbar

Projekte
QuizAway, Lern-App

Output
JS-Modul: EventLedger-Klasse mit append(), getAll(), merge(), exportDelta()

Technologie
Vanilla JS, IndexedDB (idb-Wrapper optional)

Testkriterium
Zwei Ledger-Instanzen, Events einfügen, merge() → keine Duplikate, korrekte Reihenfolge

Aufgaben
EventLedger-Klasse: append(event), getAll(), getSince(timestamp)
IndexedDB-Store: 'events', keyPath: 'id', Index auf 'timestamp'
merge(otherLedger): Union per UUID, sortiert nach timestamp
exportDelta(since): nur neue Events seit Zeitstempel — für Sync
Unit-Tests: append, merge, delta, Duplikat-Erkennung

### AP6  —  WebRTC PoC    [abgeschlossen]

Voraussetzungen
Keine

Projekte
QuizAway, Lern-App

Output
ap6_webrtc_poc.html + rendezvous.py: zwei Geräte verbinden sich per PIN, tauschen Nachrichten aus

Technologie
Vanilla JS, WebRTC (RTCPeerConnection, RTCDataChannel), Python-Rendezvous-Server

Testkriterium
Zwei Geräte im LAN, Nachricht von A nach B, Nachricht von B nach A — P2P-Verbindung aktiv ✓

Aufgaben
RTCPeerConnection + RTCDataChannel — funktioniert im LAN ohne STUN
Signaling via 6-stelligem PIN über lokalen Python-Rendezvous-Server (Port 8080)
SDP-Austausch vollständig automatisiert — kein manuelles Kopieren
DataChannel bidirektional bestätigt — Basis für AP8 (Ledger-Merge)
Erkenntnisse: ICE-Gathering-Timeout nötig, setup:actpass→active beim Answerer, Firewall-Regel für Port 8080
Nächster Schritt: Rendezvous-Server durch Nostr-Signaling ersetzen (AP7)

### AP7  —  Nostr Relay PoC    [abgeschlossen]

Voraussetzungen
Keine

Projekte
QuizAway, Lern-App

Output
ap7_nostr_poc.html: WebRTC-Signaling vollständig via Nostr — kein Rendezvous-Server mehr nötig

Technologie
Vanilla JS, WebSocket, NIP-01, Kind-1 Channel, BIP-340 Schnorr, Pure-JS secp256k1 + SHA256

Testkriterium
Gerät A sendet RTC-Offer via Nostr, Gerät B empfängt und antwortet — WebRTC P2P-Verbindung steht ✓

Aufgaben
secp256k1 Keypair komplett eingebettet (kein CDN) — funktioniert auf http:// und https://
BIP-340 Schnorr-Signaturen — Nostr-Relays akzeptieren die Events
Pure-JS SHA256 Fallback — crypto.subtle nicht nötig (http:// kompatibel)
Kind-1 Channel mit #t:quizaway-signaling statt Kind-4 DMs
Peer-Austausch: Public Key einmalig manuell — danach automatische Verbindung via Nostr
Erkenntnisse: Nostr verlangt Schnorr (nicht ECDSA), http:// sperrt crypto.subtle auf Mobilgeräten

### AP8  —  Ledger-Merge P2P    [abgeschlossen]

Voraussetzungen
AP6 + AP7 abgeschlossen

Projekte
QuizAway, Lern-App

Output
ap8_ledger_merge.html: zwei Geräte tauschen Ledger-Events aus und mergen — CRDT-Prinzip bestätigt

Technologie
Vanilla JS, WebRTC DataChannel, localStorage, UUID v4

Testkriterium
PC: 5 Events · Smartphone: 3 Events · Nach Merge: beide haben 8 Events, keine Duplikate ✓

Aufgaben
EventLedger: append(), merge(), renderLedger() — vollständig funktionsfähig
CRDT-Merge: Union per UUID — keine Konflikte, keine Duplikate, reihenfolgeunabhängig
Bidirektionaler Austausch: beide Geräte senden und empfangen vollständigen Ledger
Automatischer Sync beim DataChannel-Open — kein manueller Trigger nötig
Persistenz in localStorage — Events überleben Browser-Reload
Nächste Ausbaustufe: Delta-Sync (nur neue Events seit letztem Sync) für AP12

### 3.3  Gemeinsame Grundlagen (AP9–AP11)

### AP9  —  Fragengerator PoC    [abgeschlossen]

Voraussetzungen
AP1 abgeschlossen

Projekte
QuizAway, Lern-App

Output
ap9_fragengerator.html: drei Fragetypen aus geo.sqlite — Bundesland, Einwohner, Höhe

Technologie
Vanilla JS, sql.js 1.10.2 (SQLite via WebAssembly), geo.sqlite via fetch

Testkriterium
Alle drei Fragetypen funktionieren — echte Fragen aus 77.052 Städten ✓

Aufgaben
generateQuestion(typ, schwierigkeit) → { fragetext, antworten[4], richtig_index, erklaerung }
Typ 'bundesland': attributabfrage — Stadt → Bundesland, 3 Distraktoren aus anderen BL
Typ 'einwohner': schätzung — Größenordnung mit Faktor-Distraktoren (0.3x, 0.5x, 2x, 3x)
Typ 'hoehe': schätzung — Höhenbereiche als Antworten (unter 50m bis über 700m)
Schwierigkeitsfilter: alle Städte / >50.000 / >10.000 Einwohner
Session-Statistik: Richtig/Falsch-Quote live

### AP10  —  SQLite Build-Pipeline    [abgeschlossen]

Voraussetzungen
AP1 abgeschlossen

Projekte
QuizAway, Lern-App

Output
ap1_build_pools.py erzeugt geo.sqlite (15.6 MB) — direkt verwendbar mit sql.js im Browser

Technologie
Python, sqlite3, GeoNames-Daten

Testkriterium
geo.sqlite via fetch geladen, sql.js query liefert korrekte Ergebnisse ✓

Aufgaben
ap1_build_pools.py lädt GeoNames-Daten automatisch und baut geo.sqlite
Indizes vorhanden: stadt(staat_id), translations(pool, objekt_id, lang)
7/7 Validierungs-Checks bestanden
sql.js 1.10.2 via CDN lädt geo.sqlite via fetch — funktioniert über Rendezvous-Server
Hinweis: Landkreise (AP3) noch nicht enthalten — für Pareto-Ziel ausreichend

### AP11  —  PWA Shell    [abgeschlossen]

Voraussetzungen
AP12 abgeschlossen

Projekte
QuizAway

Output
manifest.json + sw.js + Icons: QuizAway als installierbare PWA — Desktop-Icon, offline spielbar

Technologie
Web App Manifest, Service Worker API, Cache-First/Network-First-Strategie

Testkriterium
Chrome zeigt 'Installieren' · Desktop-Icon erstellt · App startet ohne Browser-Chrome ✓

Aufgaben
manifest.json: name, short_name, display:standalone, theme_color, icons (192+512px)
sw.js: Cache-First für App-Shell, Network-First für geo.sqlite (große Datei)
rendezvous.py: --port Parameter + PNG/JS/JSON-Auslieferung ergänzt
Port 80 via netsh urlacl für PWA-Installation nötig (Chrome-Einschränkung bei Nicht-Standard-Ports)
Service Worker cached App-Shell beim Install — danach offline spielbar
Smartphone: 'Zum Startbildschirm hinzufügen' über http://192.168.178.48/quizaway_v4.html

### 3.4  Integration (AP12–AP13)

### AP12  —  QuizAway spielbar    [abgeschlossen]

Voraussetzungen
AP1 + AP9 + AP10

Projekte
QuizAway

Output
quizaway_v4.html: statisches FRAGEN-Array ersetzt durch generativen sql.js-Fragengerator

Technologie
Vanilla JS, sql.js 1.10.2, geo.sqlite, bestehende QuizAway-UI

Testkriterium
3.815 Fragen generiert (2.000 geo + Höhe + Einwohner) — alle Modi funktionieren ✓

Aufgaben
Nur FRAGEN-Array ersetzt — gesamte Spiellogik (Screens, Timer, Runden, Duell) unverändert
3 Fragetypen: Bundesland (geo), Höhenbereich (hoehe), Einwohner-Vergleich (ew)
ladeDB() async beim DOMContentLoaded — Status-Anzeige unter Logo
Bestehende v3-Kategorien geo/hoehe/ew direkt kompatibel
Bekannte Einschränkung: kfz/bahn/dist/gesch noch ohne Fragen (AP3 nötig)

### AP13  —  Duel-Modus    [abgeschlossen]

Voraussetzungen
AP6 + AP12

Projekte
QuizAway

Output
P2P-Duell via WebRTC (PIN-System) — Proof of Concept funktioniert, Neuimplementierung geplant

Technologie
WebRTC DataChannel, PIN-Rendezvous, Mulberry32 PRNG, Seed-Synchronisation

Testkriterium
Kategorie + Seed synchronisiert, gleiche Fragen auf beiden Geräten ✓ — Spiellogik noch fragil

Aufgaben
P2P-Verbindung via PIN (AP6-Mechanismus) — zwei Browserfenster getestet ✓
Host wählt Kategorie + generiert Seed → sendet via DataChannel an Guest
Deterministischer PRNG (Mulberry32): gleicher Seed = gleiche Fragen auf beiden Seiten ✓
Runden-Synchronisation: Nächste-Runde-Button gesperrt bis Gegner-Ergebnis eintrifft ✓
Ergebnis-Vergleich nach jeder Runde ✓
Bekannte Probleme: Spiellogik basiert auf simuliertem Gegner aus v3 — fragil
Nächster Schritt: DOK-3 Duell-Spezifikation (Zustandsdiagramm, Protokoll, Fehlerbehandlung)
Dann: saubere Neuimplementierung basierend auf Spezifikation

### 3.5  Lernapp-Architektur — Xalento
Mit Abschluss von AP13 (Duel-Modus) ist die QuizAway-Prototyp-Phase abgeschlossen. Die naechste Phase ist der Aufbau der generalisierten Lernapp-Plattform Xalento — React/TypeScript/Vite, FSRS, offline-first auf dem Geraet (IndexedDB). Das Startfach ist Chorübung (persoenliche Expertise), das strategische Ziel-Fach ist Biologie Sekundarstufe 1 (offene Datenbasis, Lehrplan als Kurationsraster, grosser Markt).
Entwicklungsumgebung: Claude Code (lokales CLI-Tool) statt Claude.ai Chat — Multi-File-Projekte, direkter Dateizugriff, TypeScript-native. Architektur-Prinzip: offline-first — alle Nutzerdaten liegen in IndexedDB auf dem Geraet. Kein Server, kein Login noetig. Sync zwischen Geraeten ist optionales Feature fuer spaeter (LA-4 Export/Import als erster Schritt, Cloud-Sync erst bei konkretem Nutzerbedarf).

Phase 0 — Fundament
### LA-1  —  Projektgerüst    [offen]

Voraussetzungen
—

Projekt
Lernapp (Xalento)

Output
Vite/React/TypeScript Projekt, ESLint, Prettier, Vitest — lauffähige leere App

Technologie
Vite 5, React 18, TypeScript 5, Vitest

Testkriterium
npm run dev startet, npm test grün

Aufgaben
Vite-Projekt initialisieren · React Router · Basis-Layout · CI-Pipeline

### LA-2  —  FSRS-Engine    [offen]

Voraussetzungen
LA-1

Projekt
Lernapp (Xalento)

Output
Spaced-Repetition-Engine integriert — Karte lernen, Bewertung 1-5, naechste Wiederholung berechnet

Technologie
FSRS 5 (arXiv 2508.03275), IndexedDB via Dexie.js

Testkriterium
100 Test-Karten nach 5 Tagen korrekt eingeplant

Aufgaben
FSRS-Bibliothek einbinden · Datenmodell: Karte, Deck, Lernfortschritt · Basis-Review-Screen

### LA-3  —  Quiz-Player    [offen]

Voraussetzungen
LA-2

Projekt
Lernapp (Xalento)

Output
Quiz-Player Komponente — Multiple Choice, Feedback, Punkte, FSRS-Update

Technologie
React, TypeScript, bestehende QuizAway-Logik portiert

Testkriterium
3 Fragen spielen, FSRS-Werte aktualisiert, Punkte angezeigt

Aufgaben
QuizAway-Quiz-Logik nach React portieren · FSRS-Integration · Basis-UI

Phase 1 — Inhalte
### LA-4  —  Offline-Export / Import    [offen]

Voraussetzungen
LA-2

Projekt
Lernapp (Xalento)

Output
JSON-Export und -Import der eigenen Karten und des Lernfortschritts — kein Server, kein Login, volle Datenkontrolle

Technologie
IndexedDB (Dexie.js), JSON, File System Access API (Chrome) oder Download-Link als Fallback

Testkriterium
Export erzeugt gueltiges JSON · Import stellt Karten und FSRS-Fortschritt korrekt wieder her

Aufgaben
Export-Funktion (JSON-Download) · Import-Funktion (JSON-Upload) · Merge-Logik bei Konflikt (neuerer FSRS-Stand gewinnt) · optionaler iCloud/Google Drive Hinweis

### LA-5  —  Chorübung-Inhalte    [offen]

Voraussetzungen
LA-3

Projekt
Lernapp (Xalento)

Output
Erstes echtes Deck: SingOn-Chor Bass 2 — MusicXML-Rendering via OSMD, MP3-Wiedergabe

Technologie
OSMD 1.9.6, Tone.js, MusicXML

Testkriterium
5 Chorübungen spielbar, Noten korrekt gerendert

Aufgaben
OSMD einbinden · MusicXML-Player-Komponente · Basis-Deck Chorübung · Tempo-Kontrolle

Phase 2 — Player-Ausbau
### LA-6  —  Beschriftungs-Player    [offen]

Voraussetzungen
LA-3

Projekt
Lernapp (Xalento)

Output
SVG-Bild mit nummerierten Pfeilen — Lerner tippt Bezeichnungen

Technologie
React, SVG, Wikimedia Commons Bilder

Testkriterium
Zellbild mit 5 Organellen korrekt beschriftet

Aufgaben
SVG-Overlay-Komponente · Pfeil-Positionen konfigurierbar · Auswertung

### LA-7  —  Zuordnungs-Player    [offen]

Voraussetzungen
LA-3

Projekt
Lernapp (Xalento)

Output
Drag-and-Drop Zuordnung — zwei Spalten verbinden

Technologie
React DnD, Touch-Events

Testkriterium
5 Tier-Lebensraum-Paare korrekt zugeordnet

Aufgaben
DnD-Komponente · Touch-Support · FSRS-Integration

### LA-8  —  Lückentext- und Sortier-Player    [offen]

Voraussetzungen
LA-3

Projekt
Lernapp (Xalento)

Output
Lückentext mit Dropdown/Freitext + Sortieraufgabe für Abläufe

Technologie
React, TypeScript

Testkriterium
Fotosynthese-Lückentext und Nahrungskette-Sortierung spielbar

Aufgaben
Lückentext-Komponente · Sortier-Komponente · FSRS-Integration

Phase 3 — Biologie Sek1
### LA-9  —  Wikidata-Pipeline    [offen]

Voraussetzungen
LA-3

Projekt
Lernapp (Xalento)

Output
Automatisierte Abfrage von Wikidata — Arten, Anatomie, Ökosysteme → JSON-Decks

Technologie
Python, Wikidata SPARQL API, Wikimedia Commons

Testkriterium
500 Biologie-Karten automatisch generiert, Bilder verknüpft

Aufgaben
SPARQL-Abfragen entwickeln · Lehrplan-Kurationsraster · JSON-Deck-Format · Bild-Download

### LA-10  —  Biologie Sek1 Deck    [offen]

Voraussetzungen
LA-6 + LA-7 + LA-8 + LA-9

Projekt
Lernapp (Xalento)

Output
Vollständiges kuratiertes Deck Biologie Klasse 5-6 — alle Player-Typen genutzt

Technologie
Alle Player-Typen, Wikidata-Daten, Wikimedia-Bilder

Testkriterium
Schuler kann Kapitel Zellaufbau komplett durcharbeiten — FSRS plant Wiederholungen

Aufgaben
Deck kuratieren · Karten erstellen · Qualitätssicherung · Lehrplan-Abgleich

Phase 4 — Go-to-Market
### LA-11  —  Social Contract Launch    [offen]

Voraussetzungen
LA-5

Projekt
Lernapp (Xalento)

Output
App öffentlich erreichbar — kostenlos, Teilen-Funktion, Social Contract viral

Technologie
Render/Vercel Deployment, PWA

Testkriterium
10 externe Nutzer aktiv

Aufgaben
Deployment · Share-Link · Onboarding · Feedback-Kanal

### LA-12  —  Zahlung    [offen]

Voraussetzungen
LA-11

Projekt
Lernapp (Xalento)

Output
Bezahlschranke ab ~10.000 aktiven Nutzern — Wero, PayPal, Lightning/Nostr

Technologie
Wero API, PayPal Webhooks, NIP-57 Zaps

Testkriterium
Zahlung funktioniert auf iOS und Android

Aufgaben
Payment-Provider einbinden · Webhook-Handler · Freischalt-Logik · manuelle Fallback-Liste