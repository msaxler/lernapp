# Quiz Away

**Status:** Prototyp aktiv / Iteration
**Version:** 1.2
**Datum:** März 2026
**Arbeitstitel:** Quiz Away / RoadQuiz

---

## Änderungsprotokoll

| Version | Datum | Änderung |
|---|---|---|
| 1.0 | Feb 2026 | Erstfassung |
| 1.1 | März 2026 | Synchronisationsarchitektur, Sicherheit, DHT |
| 1.2 | März 2026 | Prototyp-Status aktualisiert, Schwierigkeitsgrad, Timer, Build-Pipeline, Screens |

---

## 1. Vision

Quiz Away ist ein standortbasiertes Geo-Quiz — "GeoGuessr trifft Quizduell" mit echtem geografischem Ortsbezug. Spieler beantworten Fragen zu deutschen Städten, abhängig von ihrem aktuellen Standort oder einer gewählten Route.

**Leitsatz:** Reisen sinnvoll nutzen — geografisches Wissen spielerisch erleben.

---

## 2. Architektonisches Fundament

Quiz Away basiert auf denselben drei Stützpfeilern wie die universelle Lernplattform (siehe `pwa_lernapp.md`):

- **Daten** — Städtedatenbank + vorgenerierte Fragendatenbank (SQLite)
- **Didaktik** — Explorer, Spaced Repetition, Gamification
- **Player** — Geo-Player (Quiz-Player mit ortsbezogenen Erweiterungen)

Der wesentliche Unterschied zur Lernplattform: Fragen werden nicht manuell erstellt sondern am PC aus der Städtedatenbank vorgeneriert und als fertige Einträge in die Inhaltsdatenbank geladen. Kein Algorithmus zur Laufzeit.

**Abgrenzung zur Lernplattform:** Quiz Away ist eine eigenständige separate App. Sie teilt die Spielmechanik (Timer, Punktesystem, Zwangsweiterschaltung, Duell-Modus, Liga) mit dem Quiz-Player der Lernplattform, aber nicht die Codebasis. GPS-Logik, Städtedatenbank und geografische Falschantwort-Generierung sind zu spezifisch für eine Integration.

**Übertragbarkeit:** Die Spielmechanik von Quiz Away ist direkt auf andere Quiz-Themen übertragbar: Führerschein-Theorie (amtlicher BMDV-Fragenkatalog), Sprachenlernen (sprachagnostisches Fragen-JSON), Jagdschein. Das Duell-Framework, das Ligasystem und die Auto-Timer-Architektur sind domain-neutral.

---

## 3. Inhalt & Datenbasis

### Städtedatenbank

Ca. 2.051 deutsche Städte mit folgenden Feldern:

```json
{
  "name": "Koblenz",
  "lat": 50.3569,
  "lon": 7.5889,
  "bundesland": "Rheinland-Pfalz",
  "einwohner": 114000,
  "flaeche": 105.0,
  "hoehe": 64,
  "kfz": "KO",
  "ars": "07137086001",
  "fluesse": ["Rhein", "Mosel"],
  "bahnhof_kategorie": 2,
  "bruecken_anzahl": null,
  "universitaetsstadt": false,
  "partnerstaedte_anzahl": 5,
  "erst_erwaehnt": 866,
  "wikidata_id": "Q3138"
}
```

| Feld | Quelle | Phase |
|---|---|---|
| lat, lon, bundesland, einwohner, flaeche, hoehe, kfz, ars | Destatis / GeoNames | 1 ✅ |
| fluesse | GeoNames / OSM | 1 ✅ |
| bahnhof_kategorie | DB Netz Open Data | 1 ✅ |
| bruecken_anzahl | OpenStreetMap Overpass API | 1 |
| erst_erwaehnt, universitaetsstadt, partnerstaedte_anzahl | Wikidata | 2 |
| wikidata_id | Wikidata | 2 |

### Datenquellen

Neben Destatis und Wikidata kommen folgende Open-Data-Portale als Erweiterungsquellen in Betracht:

| Quelle | Inhalt | Einsatz |
|---|---|---|
| **BKG** (Bundesamt für Kartographie) | Präzise Höhendaten, Stadtgrenzen, Geodaten | Höhenlage, Fläche |
| **GovData.de** | Aggregator aller Bundesländer-Portale | Kommunaldaten allgemein |
| **OpenData NRW** | Kommunaldaten, Kreiszugehörigkeit | Regionale Fragen NRW |
| **Bayern Open Data** | Gemeindedaten, Höhenmodell | Regionale Fragen Bayern |
| **DB Netz Open Data** | Bahnhofskategorien (7 Klassen) | Bahnhofsgröße-Fragen |
| **OpenStreetMap Overpass API** | Brücken, Flüsse, POIs | Brücken, Flüsse |

**Empfehlung Phase 1:** BKG als Ersatz für manuell eingetragene Höhendaten — liefert präzise Werte für alle 2.051 Zielstädte als offener Datensatz.

### Fragekategorien

Kategorien sind in drei Gruppen eingeteilt je nach Datenquelle und Implementierungsaufwand. Das Prinzip ist immer gleich: seriöse Datenquelle → strukturierte Fakten → vorgenerierte Fragen. Besonders stark sind Kategorien deren richtige Antwort kontraintuitiv ist — diese überraschen und bleiben im Gedächtnis.

---

#### Gruppe A — Rein mathematisch generierbar (Phase 1)
*Nur Koordinaten und Basisdaten nötig — keine externe Datenquelle.*

**Distanz** ✅
Wie weit ist es von hier nach Frankfurt? — Haversine-Formel auf Koordinaten.
Beispiel: *„Wie weit ist es ungefähr von Koblenz nach Frankfurt?"* (4 Optionen)

**Himmelsrichtung** ✅
In welcher Richtung liegt Berlin von hier? — Bearing-Formel auf Koordinaten.
Beispiel: *„In welcher Himmelsrichtung liegt Berlin von Frankfurt aus?"*

**Einwohner-Vergleich** ✅
Welche Stadt hat mehr Einwohner? — direkter Vergleich zweier Datenbankeinträge.
Beispiel: *„Welche Stadt ist größer — Mainz oder Wiesbaden?"*

**Bevölkerungsdichte** ✅
Welche Stadt ist dichter besiedelt? — Einwohner ÷ Fläche. Ergibt oft kontraintuitive Ergebnisse: Wolfsburg ist riesig mit wenig Einwohnern, München klein aber sehr dicht.
Beispiel: *„Wo leben mehr Menschen pro km² — in München oder Wolfsburg?"*

**Höhenunterschied** ✅
Wer muss beim Wandern mehr schnaufen? — Höhe über NN aus Wikidata P2044.
Beispiel: *„Welche Stadt liegt höher — Freiburg oder München?"*

**Grenzentfernung** ✅
Welches Nachbarland liegt dieser Stadt am nächsten? — Distanz zu Staatsgrenz-Koordinaten.
Beispiel: *„Welches Nachbarland liegt Aachen am nächsten?"*

**Sonnenaufgang**
Wo geht die Sonne früher auf? — aus dem Längengrad berechenbar. Deutschland liegt in einer Zeitzone, aber zwischen Görlitz (östlichster Punkt) und Aachen (westlichster Punkt) ist der Sonnenaufgang fast eine Stunde versetzt.
Beispiel: *„Wo geht die Sonne heute früher auf — in Aachen oder Görlitz?"*

**Namenslogik**
Fragen die nur den Stadtnamen selbst brauchen — kein externes Wissen nötig.
Beispiele: *„Welche Stadt hat den längsten Namen?"* / *„Welche Stadt beginnt mit demselben Buchstaben wie Berlin?"*

**Nächste Nachbarstadt** ✅
Welche Stadt liegt am nächsten an X? — Haversine-Vergleich aller Kandidaten.
Beispiel: *„Welche Stadt liegt am nächsten an Koblenz?"* → Neuwied (12 km)

**Routenreihenfolge** ✅
Welche Stadt kommt nach X, wenn du von A nach B fährst? — Projektion auf Routenlinie.
Beispiel: *„Du fährst von Hamburg nach München — welche Stadt kommt nach Kassel?"*

**Stadtfläche**
Welche Stadt hat die größte/kleinste Fläche? — direkter Vergleich aus Destatis-Daten.
Beispiel: *„Welche dieser Städte hat die größte Stadtfläche?"* → Berlin (891 km²)

**Einwohner-Schwelle** ✅
Welche Stadt überschreitet eine bestimmte Einwohnerzahl? — einfacher Schwellenwertvergleich.
Beispiel: *„Welche dieser Städte hat über 200.000 Einwohner?"*

**Höhenlage** ✅ *(eigene Kategorie)*
Welche Stadt liegt am höchsten/tiefsten? In welchem Höhenbereich? Größter Höhenunterschied?
Beispiel: *„Welche dieser Städte liegt über 300 m?"* / *„Welche Kombination hat den größten Höhenunterschied?"*

---

#### Gruppe B — Aus strukturierten Open-Data-Quellen (Phase 1)
*Einmaliger Import, danach lokal verfügbar.*

**Geografie** ✅ — Quelle: Destatis, GeoNames
In welchem Bundesland liegt diese Stadt? An welchem Fluss?
Beispiel: *„In welchem Bundesland liegt Fulda?"*

**KFZ-Kennzeichen** ✅ — Quelle: KBA-Faltblatt / eigene Tabelle
Welches Kennzeichen gehört zu welcher Stadt — und umgekehrt. Mit Erklärung des Zulassungsbereichs.
Beispiel: *„Für welche Stadt steht das Kennzeichen ‚KO'?"*

**Bahnhofsgröße** ✅ — Quelle: DB Netz Stationsdaten / bahnhof.json
Die Deutsche Bahn kategorisiert Bahnhöfe in 7 Klassen. Klasse 1–2 = Fernverkehrshalt. ICE-Strecken mit Zwischenhalten als Quiz-Quelle.
Beispiel: *„Ist Kassel-Wilhelmshöhe ein ICE-Halt?"*

**Geschichte** ✅ — Quelle: Wikidata P571 / geschichte.json
Erste urkundliche Erwähnung, Epochenzuordnung, Städtevergleich.
Beispiel: *„Welche Stadt wurde früher gegründet — Trier oder Köln?"*

**Brücken** — Quelle: OpenStreetMap (Overpass API)
Hamburg hat mehr Brücken als Venedig und Amsterdam zusammen — fast niemand glaubt das.
Beispiel: *„Hat Hamburg mehr oder weniger als 2.500 Brücken?"*

**Fläche-Vergleich** — Quelle: Destatis
Welche Stadt nimmt geografisch mehr Fläche ein?
Beispiel: *„Welche Stadt ist flächenmäßig größer — Berlin oder München?"*

---

#### Gruppe C — Aus Wikidata (Phase 2)
*Strukturierter Import über Wikidata-API — kein Textscraping, nur Properties.*

**Persönlichkeiten** — Wikidata P19 (Geburtsort)
Beispiel: *„Welcher Komponist wurde in Bonn geboren?"*

**Universitätsstadt** — Wikidata P571 (Hochschulgründung)
Beispiel: *„Ist diese Stadt eine Universitätsstadt?"*

**Partnerstädte** — Wikidata P190
Beispiel: *„Hat Tübingen eine Partnerstadt in Frankreich?"*

**Kulinarik** — Wikidata / eigene kuratierte Liste
Beispiel: *„Welche Spezialität ist typisch für Nürnberg?"*

**Sport** — Wikidata P6801 (Heimstadion), eigene Liste
Beispiel: *„Wie heißt das Stadion von Borussia Dortmund?"*

**Wirtschaft** — Wikidata / Destatis
Beispiel: *„Welche Automarke hat ihren Stammsitz in Stuttgart?"*

---

#### Gruppe D — Persönlicher Ortsbezug (Duell-Modus, Phase 2)

Aus den Koordinaten beider Spieler werden Fragen generiert die eine persönliche Bindung schaffen:

- *„Wer von euch beiden wohnt näher an der Nordsee?"*
- *„Zwischen euren Standorten — welche Stadt liegt genau in der Mitte?"*
- *„Wessen Stadt liegt höher über dem Meeresspiegel?"*

#### Gruppe E — GPS-basierte Echtzeitfragen (Live-Modus, Phase 2)

- *„Welche Stadt liegt am nächsten an deiner aktuellen Route?"*
- *„Welche Stadt kommt als nächste auf deiner Route?"*

---

### Fragegenerierung (Build-Pipeline)

Fragen werden einmalig am PC aus der Städtedatenbank generiert und als fertige JSON-Einträge in die HTML-Datei eingebettet. Die Build-Pipeline besteht aus vier Schritten:

```
fetch_staedte.py      →  staedte.json      (2.051 Städte mit allen Feldern)
fetch_kfz.py          →  kfz in staedte.json (AGS5-basierte KFZ-Zuordnung)
generate_questions.py →  fragen.json       (789 Fragen mit sw-Feld)
inject_questions.py   →  quizaway_v3.html  (Fragen eingebettet)
check_quiz.py         →  Konsistenzprüfung (30 Checks)
```

**Schwierigkeitsfeld `sw`:** Jede Frage erhält ein Feld `sw: "L" | "M" | "S"` basierend auf der Einwohnerzahl der Fragestadt. Falschantworten werden ebenfalls aus dem jeweiligen Pool gezogen.

| Stufe | Pool | EW-Grenze | Fragen |
|---|---|---|---|
| 🟢 L — Leicht | ~335 Städte | ≥ 35.000 EW | 30 pro Kategorie |
| 🟡 M — Mittel | ~521 Städte | ≥ 25.000 EW | 50 pro Kategorie |
| 🔴 S — Schwer | 2.051 Städte | alle | 50 pro Kategorie |

**Qualitätsprinzipien:**
- **Relativ** — Fragen vergleichen Städte miteinander
- **Schätzbar** — begründete Vermutung möglich, kein blindes Raten
- **Kontraintuitiv** — die richtige Antwort überrascht

**Entwicklungsrichtung:** Im Prototyp werden Fragen vorab generiert und als JSON eingebettet. In der Produktivversion werden Fragen zur Laufzeit direkt aus den Städtedaten berechnet — kein festes Fragen-JSON mehr, sondern ein generativer Layer der immer aktuelle Daten nutzt und unbegrenzt viele Varianten erzeugen kann.

---

## 4. Spielmechanik

### Rundenstruktur
- **5 Runden** pro Spiel
- 3 Fragen pro Runde
- Vor jeder Runde: Kategoriewahl aus 3 zufällig angebotenen Kategorien
- Im Duell-Modus: abwechselnde Kategoriewahl (wie Quizduell)
- Beide Spieler erhalten dieselben Fragen — zeitversetzt (asynchron)

### Zeitlimit
- **Kategoriewahl:** 28 Sekunden (Auto-Weiter auf Zufallskategorie)
- **Frage:** 14 Sekunden Timer
- **Feedback:** 14 Sekunden (Auto-Weiter zur nächsten Frage)
- **Rundenabschluss:** 14 Sekunden (Auto-Weiter zur nächsten Runde)

### Punktesystem
- Richtige Antwort: 0–3s → 120 Punkte, danach −7 Punkte pro Sekunde, bei 14s → 0 Punkte
  - Formel: `vergangen ≤ 3 ? 120 : max(0, 120 − (vergangen − 3) × 7)`
- Falsche Antwort: 0 Punkte
- Timeout (14s abgelaufen): 0 Punkte — daher lohnt Raten immer (25 % Chance)
- Sieg im Duell: +1 bis +24 Ranglistenpunkte (abhängig vom Gegner-Rang)
- Niederlage: 0 bis −9 Punkte

### Spielmodi

**Sofa-Modus** — Zufällige Deutschland-Tour ohne Ortsbindung.

**Virtuelle Route** ✅ — Start- und Zielstadt eingeben, Fragen zu Städten entlang der Strecke (Luftlinie + Haversine-Abstandsfilter). Pool-Info und Kartenansicht vor Spielbeginn.

**Live-Modus** (Phase 2) — GPS erkennt aktuelle Stadt, Fragen beziehen sich auf die Umgebung.

**Duell-Modus** ✅ (Simulation) — 1:1 gegen simulierten Gegner. Echter asynchroner Duell-Modus in Phase 2.

### Schwierigkeitsgrad ✅

Auswahl vor jedem Spiel — gilt für alle Modi und alle Kategorien:

| Grad | Pool | Wirkung |
|---|---|---|
| 🟢 Leicht | L-Fragen | Nur Großstädte (≥ 35k EW) als Fragestadt und Falschantworten |
| 🟡 Mittel | L+M-Fragen | Städte ≥ 25k EW |
| 🔴 Schwer | Alle | Alle 2.051 Städte |

---

## 5. Screens (Prototyp v3)

### Screen 0 — Schwierigkeitsgrad *(neu in v3)*
Zwischen Startscreen und Spiel. 3 Karten: 🟢 Leicht / 🟡 Mittel (Standard) / 🔴 Schwer. Auto-Weiter nach 28s auf Mittel.

### Screen 1 — Start
Logo, Spielmodus-Auswahl (Sofa-Modus, Virtuelle Route, Duell). Fußzeile mit Links zu Rangliste, Duell und Profil.

### Screen 2 — Kategoriewahl
Rundenzähler als Fortschritts-Dots (5 Runden). Aktueller Modus und Schwierigkeitsgrad als Header. 3 zufällig gewählte Kategorien als Karten. Weiter-Button aktiviert sich nach Auswahl. Auto-Weiter 28s.

### Screen 3 — Frage
Symbolische Karte oben mit pulsierendem Stadtpin, Stadtname und Bundesland. Timer (14s). Fortschrittsbalken Frage 1/3–3/3. Kategorie-Badge. Modus+Schwierigkeit-Badge. Fragetext. 4 Antwort-Buttons (A–D). Bei Timeout: richtige Antwort grün.

### Screen 4 — Feedback
Großes Icon (✓/✕). Punkteanzeige. Richtige Antwort. Erklärungstext. Auto-Weiter 14s.

### Screen 5 — Rundenabschluss
Trefferquote (z.B. 2/3). Mini-Vorschau der 3 Fragen. Gesamtpunkte. Auto-Weiter 14s.

### Screen 6 — Spielende
Gesamtpunktzahl. Statistik-Kacheln. Liga-Fortschritt. Buttons: Nochmal / Startbildschirm.

### Screen 7 — Duell starten
Gegner-Auswahl (Freundesliste + Zufallsgegner). Scoreboard.

### Screen 8 — Duell-Kategoriewahl
Scoreboard mit Rundenpunkten als Dots. Kategorieauswahl wie Screen 2.

### Screen 9 — Duell-Ergebnis
Sieg/Niederlage-Banner. Direktvergleich. Liga-Fortschritt.

### Screen 10 — Rangliste
Global / Freunde / Region. Top-3 farbig hervorgehoben.

### Screen 11 — Liga
Aktuelle Liga mit Fortschrittsbalken. Alle 6 Ligen: Einsteiger → Bronze → Silber → Gold → Platin → Geo-Meister.

### Screen 12 — Profil
Avatar, Spielername, Liga, Rang, Statistiken, Abzeichen-Sammlung.

### Screen 13 — Virtuelle Route ✅
Start- und Zielstadteingabe mit Fuzzy-Suche. Kartenvorschau mit Routenlinie und Pool-Städten. Pool-Info (Anzahl verfügbarer Fragen). Auto-Zufallsroute nach 28s.

---

## 6. Technischer Stack

### Prototyp (aktuell)
- **Format:** Single-file HTML (`quizaway_v3.html`), kein Install nötig
- **Fragendatenbank:** `fragen.json` (789 Fragen, 7 Kategorien, sw-Feld)
- **Build-Pipeline:** Python 3.11, fünf Scripts
- **Deployment:** Live Server (VS Code) auf PC und Smartphone im Browser

### Zielsystem (Phase 1)
- **Frontend:** React + TypeScript, PWA
- **Fragedatenbank:** SQLite via WebAssembly (sql.js oder OPFS) — ~2.051 Städte, ~50.000 vorgenerierte Fragen
- **Lernfortschritt & Spielhistorie:** SQLite lokal
- **Spiellogik:** vollständig im Browser, kein Server nötig

### Synchronisationsarchitektur

#### Grundprinzip: minimale Übertragung, lokale Rekonstruktion

Das Kernprinzip beider Mechanismen — Bitset-Sync und Event-Ledger-Sync — ist dasselbe: nicht der komplette Datensatz wird verteilt, sondern nur extrem kleine Änderungsinformationen. Jeder Client rekonstruiert daraus selbst den aktuellen Zustand.

#### Bitset-Synchronisation

Für boolesche Zustände (Badge freigeschaltet, Streak aktiv, Aufstiegsplatz erreicht). 2–4 Bytes pro Änderung.

#### Event-Ledger-Synchronisation

Unveränderliche Liste von Ereignissen. 8–10 Bytes pro Duell-Ergebnis. Append-only — keine Konflikte möglich.

#### Delta-State-Gossip mit Bloom-Filtern

Peers tauschen Bloom-Filter (~256 Bytes) und übertragen nur fehlende Events. Gossip verbreitet Änderungen in log(N) Kontaktrunden durch die Liga-Gruppe.

#### Merkle-Tree-Synchronisation

Für neue Peers beim Erststart: kompakter Zustandsabgleich via Root-Hash-Vergleich. O(log n) statt O(n).

#### Gesamtarchitektur

| Situation | Mechanismus | Aufwand |
|---|---|---|
| Zwei Peers kurz offline | Bloom-Filter + fehlende Events | ~300 Bytes |
| Neuer Peer tritt Liga bei | Merkle-Tree Snapshot laden | ~5 KB |
| Einzelne Änderung (Badge) | Bitset-Update | 2–4 Bytes |
| Duell-Ergebnis | Event-Ledger-Eintrag | 8–10 Bytes |
| Wöchentlicher Liga-Reset | Neuer Merkle-Tree Snapshot | ~5 KB einmalig |

#### Synchronisationsebenen

**Ebene 1 — Datenbankupdates** (asynchron, selten): Neue Fragen via WebDAV als SQLite-Patch.

**Ebene 2 — Asynchrones Duell:** Event-Ledger-Einträge via WebDAV oder Messaging. Stunden Verzögerung möglich.

**Ebene 3 — Fast-Echtzeit-Duell:** WebSocket-Relay-Server als reiner Postbote. Spiellogik bleibt lokal. Eine wesentliche Grundlage ist bereits im Prototyp aktiv: die automatische Zwangsweiterschaltung synchronisiert beide Spieler ohne explizites Warten aufeinander.

**Ebene 4 — Rangliste:** Event-Ledger + Bitset + Bloom-Filter-Gossip. Jeder Peer trägt nur die eigene Liga-Gruppe (~30 Spieler).

#### Phasenplan

| Phase | Sync-Ebenen aktiv | Backend |
|---|---|---|
| Phase 1 | 1 (Datenupdates) | keiner |
| Phase 2 | 1 + 2 (asynchrones Duell) | WebDAV |
| Phase 3 | 1 + 2 + 3 + 4 (Fast-Echtzeit + Liga) | minimaler WebSocket-Relay |

---

### Sicherheitsarchitektur

**Signierte Events:** Jedes Event trägt eine digitale Signatur. Schlüsselpaar pro Spieler. Manipulation bricht die Hash-Kette.

**Content-Hashing:** Spielinhalte werden über ihren Hash referenziert — Manipulation ändert den Hash und macht alle Verweise ungültig.

**Feed-ID = hash(public_key):** Identität = öffentlicher Schlüssel. Fälschung ohne privaten Schlüssel unmöglich.

**Rate-Limiting, Reputation-System, Proof-of-Work (optional), Sybil-Schutz, Snapshot-Verifikation via Merkle-Tree.**

### Peer-Discovery via DHT (Kademlia)

```
hash(feed_id)   →  peer_ids  (wer hat diesen Feed?)
hash(keyword)   →  feed_ids  (welche Feeds enthalten dieses Keyword?)
```

Ablauf Peer-Join: Bootstrap → Routing Table → Liga-Keyword → Feed laden → Event-Ledger synchronisieren.

---

## 7. Ligasystem

### Wöchentliches Liga-Modell (nach Duolingo-Prinzip)

20–30 Spieler pro Gruppe, gleiche Ebene. Top 5 steigen auf, letzte 5 ab. Persönliche Bestmarke bleibt dauerhaft im Profil.

| Liga | Symbol | Aufstieg | Abstieg |
|---|---|---|---|
| Einsteiger | ⚪ | Top 5 | — |
| Bronze | 🥉 | Top 5 | Letzte 5 |
| Silber | 🥈 | Top 5 | Letzte 5 |
| Gold | 🥇 | Top 5 | Letzte 5 |
| Platin | 💎 | Top 5 | Letzte 5 |
| Geo-Meister | 🏅 | — | Letzte 5 |

---

## 8. Ausblick

Dieser Prototyp zeigt die Kernmechanik von QuizAway — bewusst schlank gehalten um das Spielgefühl früh testen zu können. Alle geplanten Features bauen direkt auf der bestehenden Architektur auf.

**Neue Fragekategorien:** Die sieben bestehenden Kategorien werden deutlich erweitert — geplant sind Fragen zu Persönlichkeiten und Geburtsorten, kulinarischen Spezialitäten, Sportstätten, Wirtschaft und Partnerstädten (Wikidata-Import Phase 2).

**Laufzeit-generierte Fragen:** Fragen werden nicht mehr vorab fest gespeichert sondern zur Laufzeit direkt aus den Städtedaten berechnet. Das ermöglicht unbegrenzte Varianten, immer aktuelle Daten und dynamische Schwierigkeitsanpassung ohne neue Build-Pipeline.

**Neue Orte und Länder:** Erweiterung über Deutschland hinaus — zunächst DACH, perspektivisch Europa. Dazu kommt ein "Heimatort"-Feature das persönliche Fragen zur eigenen Region ermöglicht.

**Live-Modus mit GPS:** Das Spiel liest den aktuellen GPS-Standort und stellt nur Fragen zu nahegelegenen Städten. Besonders wertvoll auf Reisen — das Quiz begleitet die echte Route.

**Echtzeit-Duell:** Der simulierte Gegner wird durch ein echtes synchrones Duell ersetzt. Beide Spieler sehen den Spielstand des anderen nahezu in Echtzeit. Die technische Grundlage (Auto-Timer, Event-Ledger-Architektur) ist bereits im Prototyp aktiv.

---

## 9. Offene Punkte

### Kurzfristig (Prototyp-Iteration)
- check_quiz.py: Checks für quizaway_v3.html (sw-Feld, 5 Runden, 14s/28s-Timer, Punkteformel 120 Punkte)
- Umkreis-Filter für Route/Duell nach Schwierigkeitsgrad (Leicht = 150 km, Mittel = 300 km)
- Flüsse für ~1.200 Städte nachholen (fluesse: [] in staedte.json)
- Bahn/Geschichte: M/S-Pool erweitern (aktuell nur L-Daten vorhanden)

### Mittelfristig (Phase 1 PWA)
- Live-Modus: GPS-Integration, Datenschutz
- Brücken-Kategorie (OpenStreetMap Overpass API)
- Sonnenaufgang, Namenslogik, Stadtfläche als Fragetypen
- Wikidata-Import für Geschichte automatisieren (fetch_wikidata.py)

### Längerfristig (Phase 2)
- Echtes asynchrones Duell (WebDAV-Sync)
- Wikidata Phase 2: Persönlichkeiten, Kulinarik, Sport, Wirtschaft
- Persönlicher Ortsbezug im Duell (Gruppe D)
- Monetarisierung: Freemium-Modell (Basis kostenlos, Premium für Europa-Modus, unbegrenzte Duelle)
- Zielgruppe: Reisende, Quiz-Fans, Schüler (Erdkunde)
