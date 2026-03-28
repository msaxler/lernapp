# Quiz Away

**Status:** Prototyp v4 abgeschlossen / Iterationsphase
**Version:** 1.3
**Datum:** März 2026
**Arbeitstitel:** Quiz Away / RoadQuiz

---

## Änderungsprotokoll

| Version | Datum | Änderung |
|---|---|---|
| 1.0 | Feb 2026 | Erstfassung |
| 1.1 | März 2026 | Synchronisationsarchitektur, Sicherheit, DHT |
| 1.2 | März 2026 | Prototyp-Status aktualisiert, Schwierigkeitsgrad, Timer, Build-Pipeline, Screens |
| 1.3 | März 2026 | Echtzeit-Duell, GPS-Warteraum und Live-Modus als implementiert markiert; Warteraum-Architektur ergänzt; offene Punkte aktualisiert |

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

Der wesentliche Unterschied zur Lernplattform: Fragen werden nicht manuell erstellt sondern am PC aus der Städtedatenbank vorgeneriert und als fertige Einträge in die HTML-Datei eingebettet. Kein Algorithmus zur Laufzeit.

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

#### Gruppe D — Persönlicher Ortsbezug (Duell-Modus) ✅ *(GPS-Duell implementiert)*

Aus den Koordinaten beider Spieler werden Fragen generiert die eine persönliche Bindung schaffen:

- *„Wer von euch beiden wohnt näher an der Nordsee?"*
- *„Zwischen euren Standorten — welche Stadt liegt genau in der Mitte?"*
- *„Wessen Stadt liegt höher über dem Meeresspiegel?"*

Im Prototyp werden beide GPS-Koordinaten kombiniert und schränken den Fragenpool beider Spieler auf die jeweiligen Regionen ein. Vollständige personalisierte Fragen (obige Beispiele) sind noch nicht implementiert.

#### Gruppe E — GPS-basierte Echtzeitfragen (Live-Modus) ✅ *(implementiert)*

- *„Welche Stadt liegt am nächsten an deiner aktuellen Route?"*
- *„Welche Stadt kommt als nächste auf deiner Route?"*

Im Prototyp: GPS-Standort → nächste Quiz-Stadt ermitteln → Fragenpool auf Städte im einstellbaren Radius einschränken.

---

### Fragegenerierung (Build-Pipeline)

Fragen werden einmalig am PC aus der Städtedatenbank generiert und als fertige JSON-Einträge in die HTML-Datei eingebettet.

```
scripts/data-fetch/fetch_staedte.py     →  staedte.json       (2.051 Städte)
scripts/data-fetch/fetch_kfz.py         →  kfz in staedte.json
scripts/data-build/ap1_build_pools.py   →  geo.sqlite Pools
scripts/data-build/generate_questions.py→  fragen.json        (~10.800 Fragen)
scripts/data-build/inject_questions.py  →  quizaway_v4.html   (Fragen eingebettet)
scripts/check/check_quizaway.py         →  Validierung (137 Checks)
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

**Entwicklungsrichtung:** Im Prototyp werden Fragen vorab generiert und als JSON eingebettet. In der Neubau-Version werden Fragen zur Laufzeit direkt aus den Städtedaten berechnet — kein festes Fragen-JSON mehr, sondern ein generativer Layer der immer aktuelle Daten nutzt und unbegrenzt viele Varianten erzeugen kann.

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
- **Duell Rundenvergleich:** 3 s Mindest-Delay (Ergebnis anzeigen), dann 5 s Auto-Weiter für den Spieler mit Wahlrecht

### Punktesystem
- Richtige Antwort: 0–3s → 120 Punkte, danach −7 Punkte pro Sekunde, bei 14s → 0 Punkte
  - Formel: `vergangen ≤ 3 ? 120 : max(0, 120 − (vergangen − 3) × 7)`
- Falsche Antwort: 0 Punkte
- Timeout (14s abgelaufen): 0 Punkte — daher lohnt Raten immer (25 % Chance)

### Spielmodi

**Sofa-Modus** ✅ — Zufällige Deutschland-Tour ohne Ortsbindung.

**Virtuelle Route** ✅ — Start- und Zielstadt eingeben, Fragen zu Städten entlang der Strecke (Luftlinie + Haversine-Abstandsfilter). Pool-Info und Kartenansicht vor Spielbeginn.

**Live-Modus** ✅ — GPS erkennt aktuellen Standort, Karte zeigt Städte im einstellbaren Radius (5–50 km), Stadt antippen → Quiz startet sofort.

**Duell-Modus** ✅ — Echter P2P-Duell via WebRTC DataChannel. Verbindungsaufbau über Warteraum und Signaling-Server. Spiellogik vollständig P2P.

### Schwierigkeitsgrad ✅

Auswahl vor jedem Spiel — gilt für alle Modi und alle Kategorien:

| Grad | Pool | Wirkung |
|---|---|---|
| 🟢 Leicht | L-Fragen | Nur Großstädte (≥ 35k EW) als Fragestadt und Falschantworten |
| 🟡 Mittel | L+M-Fragen | Städte ≥ 25k EW |
| 🔴 Schwer | Alle | Alle 2.051 Städte |

---

## 5. Screens (Prototyp v4)

### Screen 0 — Schwierigkeitsgrad
Zwischen Startscreen und Spiel. 3 Karten: 🟢 Leicht / 🟡 Mittel (Standard) / 🔴 Schwer. Auto-Weiter nach 28s auf Mittel.

### Screen 1 — Start
Logo, Spielmodus-Auswahl (Sofa-Modus, Virtuelle Route, Live-Modus, Duell).

### Screen 2 — Kategoriewahl
Rundenzähler als Fortschritts-Dots (5 Runden). Aktueller Modus und Schwierigkeitsgrad als Header. 3 zufällig gewählte Kategorien als Karten. Auto-Weiter 28s.

### Screen 3 — Frage
Symbolische Karte oben mit pulsierendem Stadtpin, Stadtname und Bundesland. Timer (14s). Fortschrittsbalken Frage 1/3–3/3. Kategorie-Badge. Fragetext. 4 Antwort-Buttons (A–D). Bei Timeout: richtige Antwort grün.

### Screen 4 — Feedback
Großes Icon (✓/✕). Punkteanzeige. Richtige Antwort. Erklärungstext. Auto-Weiter 14s.

### Screen 5 — Rundenabschluss
Trefferquote (z.B. 2/3). Mini-Vorschau der 3 Fragen. Gesamtpunkte. Auto-Weiter 14s.

### Screen 6 — Spielende
Gesamtpunktzahl. Statistik-Kacheln. Buttons: Nochmal / Startbildschirm.

### Screen 7 — Duell: Warteraum
Liste aktiver Spieler. GPS-Button (📍). Eigener Eintrag sichtbar. Gegner antippen → Duell starten. Auto-Weiter gegen virtuellen Gegner nach 14s.

### Screen 8 — Duell: Verbindungsaufbau
WebRTC-Verbindung wird hergestellt. Gegner-Info (Name, Liga). Countdown.

### Screen 9 — Duell: Kategoriewahl
Scoreboard mit Rundenpunkten als Dots. Kategorieauswahl für den Spieler mit Wahlrecht. Warteanzeige für den anderen Spieler.

### Screen 10 — Duell: Rundenvergleich
Direktvergleich beider Spieler für die abgeschlossene Runde. Rundensieger hervorgehoben. Auto-Weiter nach 5s (für Spieler mit Wahlrecht).

### Screen 11 — Duell: Endergebnis
Sieg/Niederlage/Unentschieden-Banner. Gesamtpunkte beider Spieler. Direktvergleich aller 5 Runden.

### Screen 12 — Live-Modus: Kartenauswahl
GPS-Standort auf Karte. Städte im Radius als Pins. Radius-Schieberegler (5–50 km). Stadt antippen → Spiel startet.

---

## 6. Technischer Stack (v4, aktuell)

### Prototyp (live)
- **Format:** Single-file HTML (`apps/quizaway/quizaway_v4.html`), kein Build-Schritt für den Client
- **Fragendatenbank:** ~10.800 Fragen (5 Kategorien, 3 Schwierigkeitsgrade) direkt in der HTML eingebettet
- **Geodatenbank:** `data/geo.sqlite` (17,7 MB), geladen via sql.js (WebAssembly) im Browser
- **Build-Pipeline:** Python 3, sechs Scripts (siehe Abschnitt 3)
- **Server:** `scripts/sync/rendezvous.py` — Python 3 stdlib, kein Framework
- **P2P:** WebRTC DataChannel, STUN (Google) + TURN (OpenRelay)
- **PWA:** Service Worker, Cache-First, Cache-Name `quizaway-v4`
- **Deployment:** Render Free Tier, GitHub Releases (geo.sqlite)

### Warteraum-Architektur
- Heartbeat-basierter Aktivitätsfilter: Server zeigt nur Spieler die in den letzten 30 s einen Heartbeat gesendet haben
- Clients senden alle 10 s `POST /warteraum/heartbeat`
- sessionStorage-Retry beim Wiedereintritt: vergessene Abmeldungen werden nachgeholt

### Neubau (geplant, noch nicht begonnen)
- **Frontend:** React 18 + TypeScript 5 + Vite 5, PWA
- **Fragedatenbank:** generativ zur Laufzeit — kein festes JSON
- **Spielhistorie:** SQLite lokal (OPFS)
- **Sync:** Event-Ledger + Bloom-Filter-Gossip + Merkle-Tree

---

### Synchronisationsarchitektur (Zielbild für Neubau)

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

---

### Sicherheitsarchitektur (Zielbild)

**Signierte Events:** Jedes Event trägt eine digitale Signatur. Schlüsselpaar pro Spieler. Manipulation bricht die Hash-Kette.

**Content-Hashing:** Spielinhalte werden über ihren Hash referenziert — Manipulation ändert den Hash und macht alle Verweise ungültig.

**Feed-ID = hash(public_key):** Identität = öffentlicher Schlüssel. Fälschung ohne privaten Schlüssel unmöglich.

**Rate-Limiting, Reputation-System, Proof-of-Work (optional), Sybil-Schutz, Snapshot-Verifikation via Merkle-Tree.**

---

## 7. Ligasystem (geplant, Neubau)

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

## 8. Ausblick (Neubau)

Der Prototyp (v4) hat die Kernmechanik von QuizAway vollständig validiert. Alle vier Spielmodi laufen stabil. Der Neubau als Teil der universellen Lernplattform (Xalento) setzt auf dieser Erfahrung auf.

**Laufzeit-generierte Fragen:** Fragen werden nicht mehr vorab fest gespeichert sondern zur Laufzeit direkt aus den Städtedaten berechnet — kein festes Fragen-JSON, unbegrenzte Varianten, immer aktuelle Daten, dynamische Schwierigkeitsanpassung.

**Neue Fragekategorien:** Persönlichkeiten und Geburtsorte, kulinarische Spezialitäten, Sportstätten, Wirtschaft, Partnerstädte (Wikidata-Import Phase 2). Sonnenaufgang, Namenslogik, Stadtfläche, Brücken.

**Neue Orte und Länder:** Erweiterung über Deutschland hinaus — zunächst DACH, perspektivisch Europa. Dazu kommt ein "Heimatort"-Feature das persönliche Fragen zur eigenen Region ermöglicht.

**Ligasystem:** P2P Event-Ledger + Bloom-Filter-Gossip. Wöchentlicher Liga-Reset. 6 Ligen: Einsteiger → Geo-Meister.

---

## 9. Offene Punkte (Prototyp v4)

### Noch nicht implementiert (Prototyp-Abschluss)
- Runde-5-Tiebreaker: bei Punktgleichstand nach 4 Runden entscheidet kürzere Gesamtspielzeit (deterministisch)
- Sieger-Anzeige: Grenzwert `<=` statt `<` prüfen + HOST-Fallback
- Ligasystem / Rangliste: Screens vorhanden, aber keine Datenbasis
- PLZ-Kategorie: Fragen technisch vorhanden, Qualität noch nicht geprüft

### Bekannte Datenfehler (behoben via geo_patch())
- Simmern/Hunsrück: kreis_id war 07143 (Westerwaldkreis/WW) statt 07140 (Rhein-Hunsrück-Kreis/SIM) — behoben

### Für Neubau
- check_quizaway.py: Checks für v4 aktualisieren (sw-Feld, 5 Runden, 14s/28s-Timer, Punkteformel 120 Punkte)
- Umkreis-Filter für Route/Duell nach Schwierigkeitsgrad (Leicht = 150 km, Mittel = 300 km)
- Flüsse für ~1.200 Städte nachholen (fluesse: [] in staedte.json)
- Bahn/Geschichte: M/S-Pool erweitern (aktuell nur L-Daten vorhanden)
- Wikidata-Import für Geschichte automatisieren (fetch_wikidata.py)
