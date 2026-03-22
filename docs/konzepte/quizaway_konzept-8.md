# Quiz Away

**Status:** Entwurf / Designphase
**Version:** 1.1
**Datum:** März 2026
**Arbeitstitel:** Quiz Away / RoadQuiz

---

## 1. Vision

Quiz Away ist ein standortbasiertes Geo-Quiz — "GeoGuessr trifft Quizduell" mit echtem geografischem Ortsbezug. Spieler beantworten Fragen zu deutschen Städten, abhängig von ihrem aktuellen Standort oder einer gewählten Route.

**Leitsatz:** Reisen sinnvoll nutzen — geografisches Wissen spielerisch erleben.

---

## 2. Architektonisches Fundament

Quiz Away basiert auf denselben drei Stützpfeilern wie die universelle Lernplattform (siehe lernplattform_v3.md):

- **Daten** — Städtedatenbank + vorgenerierte Fragendatenbank (SQLite)
- **Didaktik** — Explorer, Spaced Repetition, Gamification
- **Player** — Geo-Player (Quiz-Player mit ortsbezogenen Erweiterungen)

Der wesentliche Unterschied zur Lernplattform: Fragen werden nicht manuell erstellt sondern am PC aus der Städtedatenbank vorgeneriert und als fertige Einträge in die Inhaltsdatenbank geladen. Kein Algorithmus zur Laufzeit.

---

## 3. Inhalt & Datenbasis

### Städtedatenbank
Ca. 2.100 deutsche Städte mit folgenden Feldern:

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
| lat, lon, bundesland, einwohner, flaeche, hoehe, kfz | Destatis / GeoNames | 1 |
| fluesse | GeoNames / OSM | 1 |
| bahnhof_kategorie | DB Netz Open Data | 1 |
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

**Empfehlung Phase 1:** BKG als Ersatz für manuell eingetragene Höhendaten — liefert präzise Werte für alle 2.100 Zielstädte als offener Datensatz.

### Fragekategorien

Kategorien sind in drei Gruppen eingeteilt je nach Datenquelle und Implementierungsaufwand. Das Prinzip ist immer gleich: seriöse Datenquelle → strukturierte Fakten → vorgenerierte Fragen. Besonders stark sind Kategorien deren richtige Antwort kontraintuitiv ist — diese überraschen und bleiben im Gedächtnis.

---

#### Gruppe A — Rein mathematisch generierbar (Phase 1)
*Nur Koordinaten und Basisdaten nötig — keine externe Datenquelle.*

**Distanz**
Wie weit ist es von hier nach Frankfurt? — Haversine-Formel auf Koordinaten.
Beispiel: *„Wie weit ist es ungefähr von Koblenz nach Frankfurt?"* (4 Optionen)

**Himmelsrichtung**
In welcher Richtung liegt Berlin von hier? — Bearing-Formel auf Koordinaten.
Beispiel: *„In welcher Himmelsrichtung liegt Berlin von Frankfurt aus?"*

**Einwohner-Vergleich**
Welche Stadt hat mehr Einwohner? — direkter Vergleich zweier Datenbankeinträge.
Beispiel: *„Welche Stadt ist größer — Mainz oder Wiesbaden?"*

**Bevölkerungsdichte**
Welche Stadt ist dichter besiedelt? — Einwohner ÷ Fläche. Ergibt oft kontraintuitive Ergebnisse: Wolfsburg ist riesig mit wenig Einwohnern, München klein aber sehr dicht.
Beispiel: *„Wo leben mehr Menschen pro km² — in München oder Wolfsburg?"*

**Höhenunterschied**
Wer muss beim Wandern mehr schnaufen? — Höhe über NN aus Wikidata P2044. Wird fast immer falsch eingeschätzt.
Beispiel: *„Welche Stadt liegt höher — Freiburg oder München?"*

**Grenzentfernung**
Welches Nachbarland liegt dieser Stadt am nächsten? — Distanz zu Staatsgrenz-Koordinaten. Für Grenzstädte wie Flensburg, Aachen oder Görlitz besonders intuitiv.
Beispiel: *„Welches Nachbarland liegt Aachen am nächsten?"*

**Sonnenaufgang**
Wo geht die Sonne früher auf? — aus dem Längengrad berechenbar. Deutschland liegt in einer Zeitzone, aber zwischen Görlitz (östlichster Punkt) und Aachen (westlichster Punkt) ist der Sonnenaufgang fast eine Stunde versetzt. Fast niemand denkt daran — und es stimmt trotzdem.
Beispiel: *„Wo geht die Sonne heute früher auf — in Aachen oder Görlitz?"*

**Namenslogik**
Fragen die nur den Stadtnamen selbst brauchen — kein externes Wissen nötig.
Beispiele: *„Welche Stadt hat den längsten Namen?"* / *„Welche Stadt beginnt mit demselben Buchstaben wie Berlin?"* / *„Welche Stadt hätte beim Scrabble den höheren Punktwert?"*

**Nächste Nachbarstadt**
Welche Stadt liegt am nächsten an X? — Haversine-Vergleich aller Kandidaten.
Beispiel: *„Welche Stadt liegt am nächsten an Koblenz?"* → Neuwied (12 km)

**Routenreihenfolge**
Welche Stadt kommt nach X, wenn du von A nach B fährst? — Projektion auf Routenlinie.
Beispiel: *„Du fährst von Hamburg nach München — welche Stadt kommt nach Kassel?"*

**Stadtfläche**
Welche Stadt hat die größte/kleinste Fläche? — direkter Vergleich aus Destatis-Daten.
Beispiel: *„Welche dieser Städte hat die größte Stadtfläche?"* → Berlin (891 km²)

**Einwohner-Schwelle**
Welche Stadt überschreitet eine bestimmte Einwohnerzahl? — einfacher Schwellenwertvergleich.
Beispiel: *„Welche dieser Städte hat über 200.000 Einwohner?"*

**Höhenlage** *(eigene Kategorie — siehe unten)*
Welche Stadt liegt am höchsten/tiefsten? In welchem Höhenbereich? Größter Höhenunterschied?
Beispiel: *„Welche dieser Städte liegt über 300 m?"* / *„Welche Kombination hat den größten Höhenunterschied?"*

---

#### Gruppe B — Aus strukturierten Open-Data-Quellen (Phase 1)
*Einmaliger Import, danach lokal verfügbar.*

**Geografie** — Quelle: Destatis, GeoNames
In welchem Bundesland liegt diese Stadt? An welchem Fluss?
Beispiel: *„In welchem Bundesland liegt Fulda?"*

**KFZ-Kennzeichen** — Quelle: Destatis / eigene Tabelle
Welches Kennzeichen gehört zu welcher Stadt — und umgekehrt.
Beispiel: *„Für welche Stadt steht das Kennzeichen ‚KO'?"*

**Bahnhofsgröße** — Quelle: DB Netz Stationsdaten (offen)
Die Deutsche Bahn kategorisiert Bahnhöfe in 7 Klassen. Klasse 1–2 = Fernverkehrshalt.
Beispiel: *„Ist Kassel-Wilhelmshöhe ein ICE-Halt?"*

**Brücken** — Quelle: OpenStreetMap (Overpass API)
Hamburg hat mehr Brücken als Venedig und Amsterdam zusammen — fast niemand glaubt das.
Beispiel: *„Hat Hamburg mehr oder weniger als 2.500 Brücken?"*

**Fläche-Vergleich** — Quelle: Destatis
Welche Stadt nimmt geografisch mehr Fläche ein?
Beispiel: *„Welche Stadt ist flächenmäßig größer — Berlin oder München?"*

---

#### Gruppe C — Aus Wikidata (Phase 2)
*Strukturierter Import über Wikidata-API — kein Textscraping, nur Properties.*

**Geschichte** — Wikidata P571 (Gründungsdatum), P856 (erste urkundliche Erwähnung)
Beispiel: *„Welche Stadt wurde früher gegründet — Trier oder Köln?"*

**Persönlichkeiten** — Wikidata P19 (Geburtsort)
Beispiel: *„Welcher Komponist wurde in Bonn geboren?"*

**Universitätsstadt** — Wikidata P571 (Hochschulgründung)
Überraschend oft verblüffend: Clausthal-Zellerfeld hat eine TU — wer hätte das gedacht.
Beispiel: *„Ist diese Stadt eine Universitätsstadt?"*

**Partnerstädte** — Wikidata P190
Oft überraschende Kombinationen.
Beispiel: *„Hat Tübingen eine Partnerstadt in Frankreich?"*

**Kulinarik** — Wikidata / eigene kuratierte Liste
Beispiel: *„Welche Spezialität ist typisch für Nürnberg?"*

**Sport** — Wikidata P6801 (Heimstadion), eigene Liste
Beispiel: *„Wie heißt das Stadion von Borussia Dortmund?"*

**Wirtschaft** — Wikidata / Destatis
Größter Arbeitgeber, Automobilstandort, traditionelle Industrie.
Beispiel: *„Welche Automarke hat ihren Stammsitz in Stuttgart?"*

---

#### Gruppe D — Persönlicher Ortsbezug (Duell-Modus, Phase 2)
*Das konzeptionell stärkste Alleinstellungsmerkmal — verbindet die Spieler direkt.*

Aus den Koordinaten beider Spieler werden Fragen generiert die eine persönliche Bindung schaffen die kein anderes Quiz hat:

- *„Wer von euch beiden wohnt näher an der Nordsee?"*
- *„Zwischen euren Standorten — welche Stadt liegt genau in der Mitte?"*
- *„Wessen Stadt liegt höher über dem Meeresspiegel?"*
- *„Wer ist weiter von Berlin entfernt?"*
- *„Wie weit liegen eure beiden Heimatstädte auseinander?"*

Diese Fragen brauchen nur die Koordinaten beider Spieler — kein zusätzlicher Datenimport.

#### Gruppe E — GPS-basierte Echtzeitfragen (Live-Modus, Phase 2)
*Erfordern den aktuellen Standort des Spielers.*

- *„Welche Stadt liegt am nächsten an deiner aktuellen Route?"*
- *„Welche Stadt liegt nördlich deiner Route?"*
- *„Welche Stadt kommt als nächste auf deiner Route?"*
- *„Welche Stadt liegt höher als dein aktueller Standort?"*
- *„Welche kommende Stadt auf der Route liegt über 200 m höher?"*

Diese Fragetypen sind konzeptionell bereits definiert und im Generator vorbereitet — Implementierung erfolgt in Phase 2 mit GPS-Integration.

---

### Fragegenerierung

Fragen werden einmalig am PC aus der Städtedatenbank generiert (Python-Script) und als fertige `geo_question`-Einträge in die Inhaltsdatenbank geladen. Falschantworten werden aus dem restlichen Datenbestand gezogen — plausibel aber eindeutig falsch. Qualitätssicherung erfolgt manuell vor dem Import.

**Designprinzip für starke Fragen:** Die besten Kategorien sind jene deren richtige Antwort kontraintuitiv ist — Bevölkerungsdichte, Höhe, Brücken, Sonnenaufgang. Fragen die jeder sofort richtig beantwortet erzeugen kein Spielgefühl.

**Qualitätskriterien für Geo-Quiz-Fragen:**
- **Relativ** — Fragen vergleichen Städte miteinander, nicht mit abstrakten Absolutwerten
- **Vergleichend** — immer mindestens zwei Größen gegenüberstellen
- **Schätzbar** — der Spieler soll eine begründete Vermutung haben können, nicht raten müssen
- **Kontraintuitiv** — die richtige Antwort überrascht und bleibt im Gedächtnis

---

## 4. Spielmechanik

### Rundenstruktur
- 7 Runden pro Spiel
- 3 Fragen pro Runde
- Vor jeder Runde: Kategoriewahl aus 3 zufällig angebotenen Kategorien
- Im Duell-Modus: abwechselnde Kategoriewahl (wie Quizduell)
- Beide Spieler erhalten dieselben Fragen — zeitversetzt (asynchron)

### Zeitlimit
20–30 Sekunden pro Frage (konfigurierbar)

### Spielmodi

**Sofa-Modus** — Zufällige Deutschland-Tour ohne Ortsbindung. Für zu Hause oder unterwegs ohne GPS.

**Virtuelle Route** — Start- und Zielstadt eingeben, Fragen zu Städten entlang der Strecke.

**Live-Modus** (Phase 2) — GPS erkennt aktuelle Stadt, Fragen beziehen sich auf die Umgebung.

**Duell-Modus** (Phase 2) — 1:1, zwei Varianten: asynchron (Gegner spielt Stunden später) und Fast-Echtzeit (beide gleichzeitig online, Ergebnis in 3–5 Sekunden sichtbar).

### Punktesystem
- Sieg: +1 bis +24 Punkte (abhängig von Ranglistenposition des Gegners)
- Niederlage: 0 bis −9 Punkte
- Schnelle richtige Antwort: Zeitbonus
- Neue Bundesländer: Entdecker-Bonus
- Serien richtige Antworten: Streak-Bonus

---

## 5. Ligasystem

### Wöchentliches Liga-Modell (nach Duolingo-Prinzip)

Jede Liga-Woche kämpft der Spieler in einer zufällig zusammengestellten Gruppe von 20–30 Spielern auf ähnlichem Niveau. Am Ende der Woche steigen die besten 5 in die nächste Liga auf, die letzten 5 steigen ab, der Rest bleibt. Neue Woche — neue Gruppe, neues Spiel von vorne innerhalb der Liga.

Dieses Modell erzeugt Spannung bis zum letzten Tag weil man immer gegen konkrete Menschen kämpft die man in der Wochentabelle sehen kann — nicht gegen eine abstrakte Gesamtpunktzahl.

### Liga-Stufen

| Liga | Symbol | Aufstieg | Abstieg |
|---|---|---|---|
| Einsteiger | ⚪ | Top 5 | — |
| Bronze | 🥉 | Top 5 | Letzte 5 |
| Silber | 🥈 | Top 5 | Letzte 5 |
| Gold | 🥇 | Top 5 | Letzte 5 |
| Platin | 💎 | Top 5 | Letzte 5 |
| Geo-Meister | 🏅 | — | Letzte 5 |

### Persönliche Bestmarke
Die höchste jemals erreichte Liga bleibt als persönliche Bestmarke im Profil sichtbar — unabhängig vom wöchentlichen Reset. Gesamtpunkte aller gespielten Duelle werden ebenfalls kumuliert festgehalten.

---

## 6. Technischer Stack

### Lokal auf dem Gerät (immer verfügbar, auch offline)
- **Frontend:** React + TypeScript, PWA
- **Fragedatenbank:** SQLite via WebAssembly (sql.js oder OPFS) — ~2.100 Städte, ~50.000 vorgenerierte Fragen
- **Lernfortschritt & Spielhistorie:** SQLite lokal
- **Spiellogik:** vollständig im Browser, kein Server nötig

### Synchronisationsarchitektur

#### Grundprinzip: minimale Übertragung, lokale Rekonstruktion

Das Kernprinzip beider Mechanismen — Bitset-Sync und Event-Ledger-Sync — ist dasselbe: nicht der komplette Datensatz wird verteilt, sondern nur extrem kleine Änderungsinformationen. Jeder Client rekonstruiert daraus selbst den aktuellen Zustand. Bei kleinen Datenmengen wie einer Wochenliga kann das Netzwerkaufkommen dadurch auf wenige Bytes pro Änderung reduziert werden.

---

#### Bitset-Synchronisation

Ein Bitset ist ein Datenarray in dem jeder Zustand nur 1 Bit benötigt. Für Quiz Away eignet sich das für boolesche Zustände — Dinge die entweder eingetreten sind oder nicht.

Beispiel für Spieler-Zustände in einer Wochenliga:

```
Bit  Bedeutung
0    Hat diese Woche mindestens 1 Duell gespielt
1    Hat Aufstiegsplatz erreicht (Top 5)
2    Badge "Blitzantwort" freigeschaltet
3    Alle 16 Bundesländer in dieser Woche abgedeckt
4    Streak aktiv (3+ Tage in Folge)
```

Wenn ein Spieler z.B. Bit 2 aktiviert (Badge freigeschaltet):

```
vorher:  00010000
nachher: 00110000
```

Im Netzwerk wird nur übertragen:

```
Index: 2 · Value: 1
```

Das sind 2–4 Bytes. Alle Peers setzen dieses Bit ebenfalls. Beim Verbinden vergleichen zwei Peers ihre Bitsets und übertragen nur die Differenz — also genau die Bits die beim anderen fehlen.

---

#### Event-Ledger-Synchronisation

Hier wird nicht der Zustand gespeichert sondern eine unveränderliche Liste von Ereignissen — ähnlich einem Buchungsjournal. Der aktuelle Zustand ergibt sich immer aus der Summe aller Events.

Für Quiz Away relevante Event-Typen:

```
Typ 0x01  Duell gestartet      [spieler_a][spieler_b][liga_id]
Typ 0x02  Duell abgeschlossen  [gewinner][punkte][zeitstempel]
Typ 0x03  Liga-Aufstieg        [spieler][von_liga][nach_liga]
Typ 0x04  Badge freigeschaltet [spieler][badge_id]
Typ 0x05  Wochenliga-Snapshot  [liga_id][ranglistenstand komprimiert]
```

Ein einzelnes Duell-Ergebnis in Binärkodierung:

```
0x02 · 0x1A · 0x12 · 18 · [timestamp 4 Bytes]
```

Das sind 8–10 Bytes. 10.000 Events ergeben ~30–80 KB Gesamtlog — der gesamte Spielverlauf einer aktiven Community über Wochen in Briefmarkengröße.

**Synchronisationsprinzip:**

Jeder Client führt ein append-only Log — Ereignisse werden nur angehängt, nie verändert oder gelöscht. Wenn zwei Peers sich verbinden:

```
Peer A hat Events 1–52
Peer B hat Events 1–47
→ A sendet nur Events 48–52 an B
```

Kein Konflikt möglich weil Events unveränderlich sind. Ein Peer der lange offline war lädt beim Wiederverbinden einfach die fehlenden Events nach — keine Konfliktauflösung nötig.

**Wöchentlicher Snapshot:** Zum Ligastart wird der aktuelle Ranglistenstand als komprimierter Snapshot (Event-Typ 0x05) eingefroren. Danach beginnt ein neuer Ledger bei Null. Das verhindert unbegrenztes Wachstum und passt exakt zum Liga-Reset.

---

#### Kombination beider Mechanismen in Quiz Away

| Datenkategorie | Mechanismus | Größe pro Änderung |
|---|---|---|
| Badge freigeschaltet | Bitset | 2–4 Bytes |
| Streak aktiv/inaktiv | Bitset | 2–4 Bytes |
| Duell-Ergebnis | Event-Ledger | 8–10 Bytes |
| Liga-Aufstieg | Event-Ledger | 6–8 Bytes |
| Wochenrangliste gesamt | Snapshot (wöchentlich) | ~2–5 KB |

Einfache boolesche Zustände → Bitset. Alles mit zeitlichem Verlauf oder Kausalität → Event-Ledger.

---

#### Skalierung bei wachsender Nutzerzahl

Bei vielen Spielern muss verhindert werden dass jeder alle Events bekommt. Lösung: Topic-Partitionierung — Peers abonnieren nur Events der eigenen Liga-Gruppe:

```
Liga Bronze Woche 12 Gruppe 4  →  nur ~30 Spieler, ~100 Events/Woche
Liga Silber Woche 12 Gruppe 7  →  nur ~30 Spieler, ~100 Events/Woche
```

Jeder Peer empfängt also maximal ein paar hundert Events pro Woche unabhängig von der Gesamtnutzerzahl. Das ist der Grund warum diese Architektur stark skaliert.

Reale Systeme die dieses Prinzip nutzen: Secure Scuttlebutt, Hypercore Protocol, Automerge, sowie viele Multiplayer-Spieleserver.

---

#### Delta-State-Gossip mit Bloom-Filtern

Dieses Verfahren kombiniert drei Mechanismen zu einer besonders effizienten Lösung für die Ranglisten-Synchronisation in Quiz Away.

**Das Problem ohne Optimierung:**

Wenn zwei Peers synchronisieren müssten sie eigentlich ihre kompletten Event-Listen vergleichen. Bei vielen Peers würde das unnötigen Netzwerkverkehr erzeugen — Peer A schickt eine Liste mit 100 Event-IDs nur damit Peer B herausfinden kann welche ihm fehlen.

**Bloom-Filter als Lösung:**

Ein Bloom-Filter ist eine kompakte probabilistische Datenstruktur die mit wenigen hundert Bytes tausende Event-IDs repräsentiert. Er beantwortet die Frage "Kenne ich dieses Event bereits?" mit einer wichtigen Eigenschaft: keine False Negatives (ein vorhandenes Event wird nie als fehlend markiert), aber mögliche False Positives (ein fehlendes Event könnte fälschlich als vorhanden gemeldet werden — im schlimmsten Fall wird ein Event doppelt übertragen, nie verloren).

Ablauf:

```
Peer A baut Bloom-Filter aus seinen Events 1–100    → ~256 Bytes
Peer A sendet Filter an Peer B
Peer B prüft welche seiner Events im Filter fehlen
Peer B sendet nur die fehlenden Events an A         → z.B. 3 × 10 Bytes
```

Gesamtaufwand für eine Synchronisation: ~286 Bytes statt einer Liste mit 100 IDs.

**Gossip-Protokoll als Verbreitungsmechanismus:**

Jeder Peer spricht periodisch mit wenigen zufälligen anderen Peers der eigenen Liga-Gruppe. Neue Daten verbreiten sich wie eine Epidemie durch das Netz:

```
Peer A ↔ Peer B  →  B hat jetzt Events von A
Peer B ↔ Peer C  →  C hat jetzt Events von A und B
Peer C ↔ Peer D  →  D hat jetzt alle Events
```

Ein Gossip-System kontaktiert typischerweise log(N) Peers pro Runde. Bei 10.000 Peers genügen ~14 Kontakte damit sich eine Änderung im gesamten Netz verbreitet. Keine zentrale Koordination nötig.

**Delta-State — nur Änderungen übertragen:**

Statt vollständiger Zustände wird immer nur das Delta übertragen — die Änderungen seit dem letzten Kontakt:

```
Zustand t0  →  Zustand t1  →  Δ = t1 − t0
```

Jeder Client speichert lokal: aktueller Zustand + Event-Log. Beim Wiederverbinden nach Offline-Phase: Bloom-Filter vergleichen → nur fehlende Events nachladen. Kein vollständiger Datensatz nötig.

**Datenvolumen in der Praxis für Quiz Away:**

```
Bloom-Filter:          256 Bytes
10 fehlende Events:     80 Bytes  (10 × 8 Bytes)
─────────────────────────────────
Gesamtaufwand:         336 Bytes
```

Bei 50 KB Gesamtzustand einer Liga-Gruppe erreicht dieses System typisch 1–5 Bytes pro Änderung und hält trotzdem tausende Clients synchron.

**Architektur je Client:**

```
Client
 ├─ lokaler Zustand (SQLite)
 ├─ Event-Log (append-only)
 ├─ Bloom-Filter (aus eigenem Log)
 └─ Gossip-Synchronisation (periodisch, liga-partitioniert)
```

Reale Systeme die diese Kombination nutzen: Cassandra (verteilte Datenbank), Secure Scuttlebutt (dezentrales Social Network), IPFS.

---

#### Merkle-Tree-Synchronisation

Während der Event-Ledger den zeitlichen Verlauf abbildet und Bloom-Filter-Gossip die effiziente Verbreitung übernimmt, löst der Merkle-Tree ein anderes Problem: zwei Peers müssen feststellen können welche Daten unterschiedlich sind — ohne den gesamten Datensatz zu übertragen. Das ist besonders wichtig für neue Peers die nach langer Offline-Phase oder beim Erststart synchronisieren müssen.

Das Verfahren wird verwendet in Git, IPFS und BitTorrent.

**Grundprinzip — Hashbaum:**

Alle Daten werden in Blöcke aufgeteilt, jeder Block erhält einen Hashwert. Diese Hashes werden zu einem Baum kombiniert:

```
        Hroot
       /     \
     H12     H34
    /   \   /   \
  h1   h2  h3   h4
```

Berechnung:
```
H12   = hash(h1 + h2)
H34   = hash(h3 + h4)
Hroot = hash(H12 + H34)
```

Der Root-Hash repräsentiert den gesamten Datensatz in einem einzigen Wert. Ändert sich ein einziger Block ändern sich automatisch alle darüber liegenden Hashes bis zur Wurzel.

**Vergleich zweier Peers:**

Peers vergleichen zuerst nur den Root-Hash — das sind 32 Bytes:

```
Root gleich    →  keine Synchronisation nötig
Root verschieden  →  Baumvergleich, nur abweichender Ast wird untersucht
```

Beispiel: Peer A hat Block C geändert.

```
Peer A:  Hroot_A → H12 (gleich) · H34_A (verschieden) → h3' (verschieden)
Peer B:  Hroot_B → H12 (gleich) · H34_B (verschieden) → h3  (verschieden)
Ergebnis: nur Block C wird übertragen
```

Bei 50 KB Gesamtdaten in 1-KB-Blöcken (50 Blöcke) kostet eine Synchronisation: einige Hashwerte à 32 Bytes + den einen geänderten Block. Die Komplexität ist O(log n) statt O(n) — bei doppelter Datenmenge wächst der Aufwand nur um einen Schritt im Baum.

**Vorteil gegenüber dem Event-Ledger alleine:**

Event-Logs wachsen unbegrenzt — nach einem Jahr gibt es tausende Events. Ein Merkle-Tree repräsentiert immer nur den aktuellen Zustand, unabhängig davon wie viele Änderungen dazu geführt haben.

---

#### Gesamtarchitektur: Kombination aller Mechanismen

Die robusteste Lösung für Quiz Away kombiniert alle vier Mechanismen:

```
Lokaler Client
 ├─ SQLite (aktueller Zustand)
 ├─ Event-Log (append-only, Änderungshistorie)
 ├─ Merkle-Tree Snapshot (kompakter Zustandsabgleich)
 ├─ Bloom-Filter (aus eigenem Event-Log)
 └─ Gossip-Synchronisation (liga-partitioniert, periodisch)
```

**Zusammenspiel:**

| Situation | Mechanismus | Aufwand |
|---|---|---|
| Zwei Peers kurz offline | Bloom-Filter + fehlende Events | ~300 Bytes |
| Neuer Peer tritt Liga bei | Merkle-Tree Snapshot laden | ~5 KB |
| Peer lange offline | Snapshot + neue Events nachladen | Snapshot + Δ |
| Einzelne Änderung (Badge) | Bitset-Update | 2–4 Bytes |
| Duell-Ergebnis | Event-Ledger-Eintrag | 8–10 Bytes |
| Wöchentlicher Liga-Reset | Neuer Merkle-Tree Snapshot | ~5 KB einmalig |

**Ablauf bei Peer-Verbindung:**

```
1. Root-Hash vergleichen (32 Bytes)
2a. Gleich → nichts zu tun
2b. Verschieden → Bloom-Filter tauschen (~256 Bytes)
3. Fehlende Events identifizieren und übertragen
4. Merkle-Tree lokal aktualisieren
```

**Skalierung:**

Bei tausenden Nutzern bleibt das System effizient weil jeder Peer nur Events der eigenen Liga-Gruppe (20–30 Spieler) verarbeitet. Gossip verbreitet Änderungen in log(N) Kontaktrunden. Das Gesamtsystem erreicht bei 50 KB Zustand typisch 1–5 Bytes pro Änderung über alle Peers.

Reale Systeme die diese vollständige Kombination nutzen: Git (Merkle-Tree + Delta), IPFS (Merkle-Tree + P2P-Gossip), Cassandra (Gossip + Bloom-Filter), Secure Scuttlebutt (Event-Log + Gossip).

---

#### Synchronisationsebenen

**Ebene 1 — Datenbankupdates (asynchron, selten)**
Neue Fragen, neue Kategorien, Korrekturen. Übertragung via WebDAV (z.B. Nextcloud) als SQLite-Patch-Datei. Kein Server-Code nötig.

**Ebene 2 — Asynchrones Duell**
Beide Spieler müssen nicht gleichzeitig online sein. Duell-Einladung, Fragen-IDs und Rundenergeb­nisse werden als Event-Ledger-Einträge übertragen (8–80 Bytes). Übertragungsweg: WebDAV oder leichtgewichtiges Messaging. Der Spieler sieht das Ergebnis wenn der Gegner seine Runde abgeschlossen hat — Stunden später möglich.

**Ebene 3 — Fast-Echtzeit-Duell**
Beide Spieler sind gleichzeitig online. Nach jeder Frage erscheint das Ergebnis des Gegners in 3–5 Sekunden. Technisch: WebSocket-Relay-Server der ausschließlich Event-Ledger-Einträge weiterleitet — kein Spielzustand, keine Datenbank auf dem Server, nur ein Postbote. Die Spiellogik bleibt vollständig lokal. Das Datenformat ist identisch zu Ebene 2 — nur der Übertragungsweg ändert sich.

**Ebene 4 — Rangliste (Event-Ledger + Bitset + Bloom-Filter-Gossip)**
Jedes Gerät trägt eine lokale Kopie des aktuellen Wochen-Ledgers der eigenen Liga-Gruppe. Beim Verbinden tauschen Peers Bloom-Filter aus und übertragen nur wirklich fehlende Events (~256 Bytes Filter + wenige Bytes pro Event). Bitsets übertragen boolesche Zustände (Badges, Streak) in 2–4 Bytes. Gossip verbreitet Änderungen epidemisch durch die Liga-Gruppe ohne zentrale Koordination.

---

### Phasenplan

| Phase | Sync-Ebenen aktiv | Backend |
|---|---|---|
| Phase 1 | 1 (Datenupdates) | keiner |
| Phase 2 | 1 + 2 (asynchrones Duell) | WebDAV |
| Phase 3 | 1 + 2 + 3 + 4 (Fast-Echtzeit + Liga) | minimaler WebSocket-Relay |

---

### Sicherheitsarchitektur

Ein dezentrales P2P-System ohne zentralen Server braucht kryptografische Mechanismen um Fälschung, Spam und Missbrauch zu verhindern. Die folgenden Maßnahmen bilden die Minimalarchitektur für Quiz Away.

**Signierte Events**
Jedes Event trägt eine digitale Signatur des Absenders. Ein Spieler besitzt ein Schlüsselpaar (public/private key). Events werden mit dem privaten Schlüssel signiert, alle Peers prüfen die Signatur mit dem öffentlichen Schlüssel. Gefälschte oder manipulierte Events werden sofort erkannt und verworfen.

```
Event-Struktur:
{ sequence, timestamp, event_type, data, previous_hash, signature }
```

Sequence-Nummern und previous_hash verketten Events zu einer Kette — ein nachträgliches Einfügen oder Löschen würde die Kette brechen und sofort auffallen.

**Content-Hashing**
Spielinhalte (Fragen, Kategorien, Snapshots) werden über ihren Hash referenziert, nicht über einen Pfad oder Namen. Ein Peer der einen Inhalt empfängt kann durch Nachberechnen des Hashes sofort prüfen ob der Inhalt integer ist. Manipulation ist nicht möglich ohne den Hash zu ändern — und damit alle Verweise ungültig zu machen.

**Feed-ID = hash(public\_key)**
Die Identität eines Publishers ist sein öffentlicher Schlüssel. Die Feed-ID wird direkt aus dem Public Key berechnet. Clients abonnieren Feeds vertrauenswürdiger Publisher (trusted\_feeds) und prüfen bei jedem Eintrag die Signatur. Ein Angreifer kann keinen Feed fälschen ohne den privaten Schlüssel des Publishers zu besitzen.

**Rate-Limiting**
Jeder Peer begrenzt die Anzahl Events die er von einem einzelnen Absender pro Zeiteinheit akzeptiert. Das verhindert Spam-Floods die das Netz überlasten würden.

**Reputation-System**
Peers führen lokal eine einfache Bewertung anderer Peers: wie oft hat dieser Peer valide Events geliefert, wie oft ungültige? Peers mit schlechter Reputation werden seltener kontaktiert und ihre Events mit mehr Skepsis behandelt.

**Proof-of-Work (optional)**
Als zusätzliche Spam-Bremse kann ein minimaler Rechenaufwand pro Event verlangt werden — ähnlich wie bei E-Mail-Spam-Filtern. Legitime Spieler merken davon nichts (Millisekunden), massenhaftes Einschleusen von Events wird aber rechenintensiv.

**Sybil-Angriffe**
Ein Angreifer könnte viele gefälschte Identitäten (Sybil-Peers) erstellen um die Rangliste zu manipulieren. Gegenmaßnahmen: Diversity (Peers bevorzugen Kontakte aus unterschiedlichen Netzregionen), Proof-of-Work erschwert massenhafte Identitätserstellung, Reputation-System isoliert verdächtige Peers.

**Snapshot-Verifikation**
Wöchentliche Liga-Snapshots werden per Merkle-Tree verifiziert. Ein neuer Peer der einen Snapshot lädt kann dessen Integrität durch Vergleich des Root-Hash mit mehreren unabhängigen Peers prüfen bevor er ihn als Ausgangszustand akzeptiert.

---

### Peer-Discovery via DHT

Damit Peers sich in einem vollständig dezentralen Netz finden können ohne zentralen Verzeichnisserver wird ein Distributed Hash Table (DHT) nach dem Kademlia-Protokoll verwendet. Kademlia wird eingesetzt in BitTorrent, IPFS und vielen anderen P2P-Systemen.

**Grundprinzip:**

Jeder Peer und jeder Feed hat eine eindeutige ID. Der DHT speichert Zuordnungen:

```
hash(feed_id)   →  peer_ids  (wer hat diesen Feed?)
hash(keyword)   →  feed_ids  (welche Feeds enthalten dieses Keyword?)
```

Ein Peer der einen bestimmten Feed sucht berechnet hash(feed\_id) und fragt den DHT — der ihn zu den Peers führt die diesen Feed halten.

**Dezentraler Suchindex:**

Keywords zu Spielkategorien oder Liga-Gruppen werden ebenfalls im DHT indiziert. Ein Spieler der einer bestimmten Liga beitreten möchte sucht:

```
hash("liga_bronze_woche12_gruppe4")  →  peer_ids der Liga-Mitglieder
```

Multi-Keyword-Suche durch Schnittmengen. Ranking nach Popularität, Vertrauen und Aktualität. Optional können Supernodes als stabile Cache-Knoten dienen um häufig gesuchte Einträge schnell verfügbar zu halten.

**Lokale Datenstrukturen je Client:**

```
Client
 ├─ keyword_index: keyword → feed_ids
 ├─ feed_info: feed_id, publisher_key, latest_sequence, content_hashes
 ├─ event_ledger: lokaler Lernfortschritt und Duell-Historie
 └─ content_cache: lokal gespeicherte Inhalte (Fragen, Snapshots)
```

**Ablauf Peer-Join:**

```
1. Neuer Peer bootstrapped via bekannte Start-Peers
2. Kademlia Routing Table aufbauen
3. Liga-Keyword suchen → feed_ids finden
4. Feed-Einträge laden, Signaturen prüfen
5. Inhalte (Fragen, Snapshot) von Peers abrufen, lokal speichern
6. Event-Ledger mit Liga-Peers synchronisieren
7. Peer vollständig synchronisiert — kann neue Inhalte finden und weitergeben
```

**Ablauf Suche & Synchronisation:**

```
1. Keyword eingeben (z.B. "kfz-kennzeichen" oder "liga_bronze_12_4")
2. hash(keyword) → DHT.find_value → feed_ids
3. Feeds von Peers laden, Signaturen prüfen
4. Content-Hashes abrufen, lokal speichern
5. Event-Ledger synchronisieren
```

---

### Ziel
Frühe Nutzerfeedback-Runde zur Spielmechanik — bevor eine Zeile produktiver Code geschrieben wird.

Format: HTML-Datei (`quizaway_v2.html`), auf PC und Smartphone im Browser bedienbar, kein Install nötig. Inhalt: echte Städtefragen aus mehreren Kategorien.

---

### Stufe 1 — Kernschleife (umgesetzt)

Fokus: Stimmt das Spielgefühl? Ist die Bedienlogik intuitiv?

**Screen 1 — Start**
Logo, Spielmodus-Auswahl (Sofa-Modus, Virtuelle Route, Live-Modus als "kommt bald" ausgegraut), Fußzeile mit Links zu Rangliste, Duell und Profil.

**Screen 2 — Kategoriewahl**
Rundenzähler oben als Fortschrittsbalken (7 Punkte). Aktuelle Runde und Spielmodus als Überschrift. 3 zufällig gewählte Kategorien als große Karten mit Emoji, Name und Beispielfrage. Weiter-Button aktiviert sich nach Auswahl.

**Screen 3 — Frage**
Symbolische Karte oben (Gitternetz, pulsierender Stadtpin, Stadtname und Bundesland als Label). Timer-Kreis (20 Sekunden). Fortschrittsbalken Frage 1/3 bis 3/3. Kategorie-Badge. Fragetext. 4 Antwort-Buttons mit Buchstabe (A–D). Bei Ablauf des Timers: richtige Antwort grün markiert.

**Screen 4 — Feedback**
Großes Icon (✓ grün / ✕ rot). Richtig/Falsch-Label. Punkteanzeige. Box mit richtiger Antwort. Box mit "Wusstest du schon?" — Erklärung zur Frage. Weiter-Button.

**Screen 5 — Rundenabschluss**
Rundenbezeichnung. Kreisring-Anzeige mit Trefferquote (z.B. 2/3). Mini-Vorschau der 3 Fragen (✓/✕). Gesamtpunkte. Button zur nächsten Runde oder zum Ergebnis.

**Screen 6 — Spielende**
Pokal-Icon. Gesamtpunktzahl groß. 3 Statistik-Kacheln (Richtig, Falsch, Bundesländer). Liga-Fortschrittsanzeige. Buttons: Nochmal spielen / Startbildschirm.

---

### Stufe 2 — Soziale Mechanik (umgesetzt)

Fokus: Funktioniert die Duell-Logik? Sind Rangliste und Liga motivierend dargestellt?

**Screen 7 — Duell starten**
Eigenes Profil (links) vs. Gegner-Platzhalter (rechts) mit VS-Label. Freundesliste mit Avatar, Name, letzter Aktivität, Spielanzahl, Liga-Badge. Zufallsgegner als Option. Antippen eines Gegners startet das Duell.

**Screen 8 — Duell-Kategoriewahl**
Scoreboard oben: beide Spieler mit aktuellem Punktestand und 7 Rundenpunkten als Dots (grün = gewonnen, grau = ausstehend). Darunter: Rundennummer und wer wählt. Kategorieauswahl identisch zu Screen 2.

**Screen 9 — Duell-Ergebnis**
Banner: Sieg (grün) oder Niederlage (rot) mit passendem Emoji. Gewonnene oder verlorene Ranglistenpunkte. Direktvergleich beider Spieler: Richtige Antworten, Gesamtpunkte, Durchschnittliche Antwortzeit. Liga-Fortschrittsanzeige. Buttons: Zur Rangliste / Startbildschirm.

**Screen 10 — Rangliste**
Tabs: Global / Freunde / Region. Liste mit Rang, Avatar, Name, Liga-Badge und Punktzahl. Plätze 1–3 farbig hervorgehoben (Gold/Silber/Bronze). Eigener Eintrag am Ende hervorgehoben falls außerhalb der Top-Einträge. Button: Duell starten.

**Screen 11 — Liga**
Aktuelle Liga groß mit Fortschrittsbalken (z.B. 843/1000 Punkte bis Aufstieg). Alle 6 Ligen als Liste: Einsteiger → Bronze → Silber → Gold → Platin → Geo-Meister, mit Punktebereichen. Vergangene Ligen ausgegraut mit Haken, aktuelle hervorgehoben, zukünftige gesperrt (🔒). Button: Duell spielen & aufsteigen.

**Screen 12 — Profil**
Avatar, Spielername, aktuelle Liga und globaler Rang. 4 Statistik-Kacheln: Spiele gesamt, Siege, Trefferquote, Streak. Abzeichen-Sammlung: verdiente Badges voll sichtbar (z.B. "Alle 16 Bundesländer", "Blitzantwort", "7 Tage Streak"), noch nicht verdiente ausgegraut.

---

## 8. Offene Punkte

- Live-Modus: GPS-Integration, Datenschutz
- Virtuelle Route: Routing-Algorithmus (OpenStreetMap oder Linie mit Haversine)
- Fragegenerierungs-Script: Umfang, Qualitätssicherung
- Wikidata-Import für Phase 2 (Geschichte, Persönlichkeiten, Kulinarik)
- Monetarisierung: Freemium-Modell (Basis kostenlos, Premium für Europa-Modus, unbegrenzte Duelle)
- Zielgruppe: Reisende, Quiz-Fans, Schüler (Erdkunde)
