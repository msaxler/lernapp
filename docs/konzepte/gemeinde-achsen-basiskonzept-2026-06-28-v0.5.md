# Gemeinde-Achsen — Basiskonzept v0.5 (final)

**Story-Satz:**
*Wir bauen eine Faktendatenbank für ~10.000 deutsche Gemeinden, deren tragende Struktur nicht aus vordefinierten Spalten besteht, sondern aus einem iterativ entdeckten **Katalog von Entitätstypen mit Eigenschaften**. Datenmodell, Identität, Metadaten, Zeit-Dimension und Versionierung sind explizit modelliert. Sobald der Katalog stabil ist, ist die Vollbefüllung mechanisch — mit beliebigen KI-Modellen austauschbar.*

---

## Status-Block

| | |
|---|---|
| **Version** | v0.5 (final, implementations-freigegeben) |
| **Datum** | 2026-06-28 |
| **Status** | Mike-Freigabe für Iteration 1 |
| **Scope** | NUR Datenbank-Aufbau (Inhaltsschicht). Spielmechanik = 1:1 aus bestehendem QuizAway übernommen. Einhängung ins QuizAway-Gesamtkonzept = separate Baustelle (siehe §20). |
| **Vorgänger** | v0.4. Schwächen: Identitäts-Lebenszyklus unmodelliert (`instance_status` fehlte); Ortsteil-String ohne ID-Anbindung; Vertrauen vermischte Quellen- und Extraktionsgüte; Canonicalization nicht ausgelegt für namenlose Entitäten; Achse-C-Distraktor-Spezifik fehlte; Snapshot-Rhythmus unbestimmt; Architekturprinzipien nicht explizit. |
| **Provenance** | Drei Multi-AI-Review-Runden (Claude / ChatGPT / Gemini parallel) auf v0.2, v0.3 und v0.4. Synthese nach stärkstem Argument, Konvergenzen über Reviewer als Vertrauenssignal. Runde 3 attestierte Implementations-Reife. |
| **Bewusst offen** | App-Identität (Edition in QuizAway oder eigenständige App); KI-Modell-Wahl; finales DB-Backend (entscheidet sich nach Iteration 2). |

**TL;DR:** v0.5 ist final. Sieben Architekturprinzipien (§1) verankern unveränderliche Leitplanken. Datenmodell um Identitäts-Lebenszyklus, Vertrauens-Trennung, Zeitraum-Datentyp und Wertgenauigkeit erweitert. Canonicalization deckt namenlose Entitäten und Disambiguierung ab. Snapshot-Rhythmus festgelegt (initial einmalig, danach jährlich). Nächster Schritt: Iteration 1 über 10 Gemeinden. Einhängung in QuizAway und App-Umstellung sind separate Baustellen.

---

## 1. Architekturprinzipien

Diese sieben Prinzipien sind die unveränderlichen Leitplanken. Spätere Detailentscheidungen werden an ihnen ausgerichtet; Vorschläge, die sie verletzen, werden zurückgewiesen.

**P1 — Struktur wächst aus Daten, nicht umgekehrt.**
Das Schema ist Ergebnis der Iterationen 1–3, nicht ihre Voraussetzung.

**P2 — Provenienz geht niemals verloren.**
Jeder Wert trägt Quelle, Abrufdatum, Extraktions-Versionen und Vertrauen. Re-Extraktionen ersetzen nicht, sondern ergänzen.

**P3 — Neue Eigenschaften sind additive Erweiterungen.**
Schema-Migrationen sind Katalog-Versionssprünge, keine Strukturbrüche. JSON-Lines und JSON-Spalten machen dies möglich.

**P4 — Historie wird nie überschrieben.**
Zeitlich begrenzte Werte werden über `gueltig_ab`/`gueltig_bis` erfasst. Frühere Bürgermeister bleiben in der DB.

**P5 — Schichten werden nach Ableitbarkeit getrennt, nicht nach Quelle.**
Wikidata kann sowohl Schicht 0 als auch Schicht 1 beliefern. Maßgeblich ist, ob LLM-Interpretation nötig ist.

**P6 — Quizlogik kennt keine Quellen.**
Die Quizfragen-Auswahl filtert nach Metriken, `quiz_tauglich`, Zeit-Gültigkeit und Distraktor-Pool — *nicht* nach Quelle. Provenienz bleibt für Debugging, nicht für Spielmechanik.

**P7 — Manuelle Kuration schlägt automatische Heuristik.**
Bei Konflikten zwischen Automatik und manueller Entscheidung gewinnt die Kuration. Automatische Heuristiken sind Vorschläge, nicht Urteile.

**P8 (operativ) — Anbieter-Unabhängigkeit.**
Extraktion läuft mit reinem Freitext-Prompt. Kein Tool-Use, kein Structured-Output, keine modellspezifischen Features. Jede LLM-Familie ist austauschbar.

---

## 2. Kern-These

Eine gute Quiz-Datenbank über ~10.000 Gemeinden hat **nicht** vorher ein festes Schema. Sie hat einen **Katalog von Entitätstypen mit Eigenschaften**, der aus den Quellen herauswächst.

```
  Gemeinde → Entitätsinstanz (von Entitätstyp T) → Eigenschaft → Wert
```

Drei zentrale Modellentscheidungen:
1. **Typ vs. Instanz** getrennt. Zwei Kirchen im selben Ort sind zwei Instanzen desselben Typs.
2. **Eigenschaften** statt „Adjektive" (viele Eigenschaften sind Substantive: Baujahr, Höhe, Material).
3. **Metadaten** (Quelle, Zeit-Dimension, Aktualitäts-Heuristik, getrenntes Vertrauen für Quelle und Extraktion) sind Bestandteil jedes Werts.

---

## 3. Zwei-Schichten-Modell — nach Ableitbarkeit

Der Schichtschnitt erfolgt nach *„Ist der Wert deterministisch ableitbar oder LLM-extrahiert?"*, **nicht** nach Quelle.

### 3.1 Schicht 0 — Deterministisch ableitbare Strukturdaten

Werte ohne LLM-Interpretation: AGS, Bundesland, Landkreis, Geometrien, Centroide, Nachbarschaftsgraph, Distanzen, Skalardaten aus Destatis/Wahlleiter-CSV, Wikidata-Properties mit eindeutigem Statement.

### 3.2 Schicht 1 — LLM-extrahiert oder semantisch interpretiert

Alles, was Textverständnis erfordert: Wikipedia-Volltext-Fakten, Wikidata-Properties mit mehrdeutigen Statements (siehe §3.3).

### 3.3 Wikidata-Property-Schichteinordnung (Implementierungsnotiz)

Wikidata-Properties mit Werten, die über SPARQL direkt abrufbar sind und keiner Auswahl aus mehreren möglichen Werten bedürfen, gehören zu Schicht 0. Beispiele: P2044 (Höhe ü.NN), P131 (Verwaltungseinheit), P1082 (Einwohnerzahl mit Stichtags-Qualifier).

Properties mit mehreren Statements ohne klare Priorisierung oder mit qualifier-bedürftiger Auswahl (z.B. P31 „ist ein(e)") gehören zu Schicht 1 mit `vertrauen_quelle: 0.90`.

---

## 4. Datenmodell — explizit

### 4.1 Entitätstyp (im Katalog)

```yaml
typ: kirche
multiplicity: 0..n
beschreibung: Christlicher Sakralbau
katalog_version_eingefuehrt: v3
untertyp_aufzaehlung:
  version: 2
  status: vorlaeufig
  werte: [pfarrkirche, kapelle, wallfahrtskirche, klosterkirche]
originalbezeichnungen_beobachtet:
  - Kirche
  - Pfarrkirche
  - Marienkirche
  - Wallfahrtskirche
  - Kapelle
identifikator_pflicht_bei_n_groesser_1: bezeichnung
identifikator_fallback_bei_namenlos:
  - material
  - baujahr
  - lage_im_ort
quiz_tauglich_default: true
eigenschaften:
  - name: bezeichnung
    typ: Name
    pflicht_wenn_multiplicity_n: true
    quiz_tauglich: true
  - name: baujahr
    typ: Jahr
    trefferquote: 0.42
    diskriminationswert: 0.85
    quiz_tauglich: true
  - name: bauzeit
    typ: Zeitraum   # neu in v0.5: Jahr-Jahr für gespannte Errichtungen
    trefferquote: 0.08
    quiz_tauglich: true
  - name: hoehe_turm_m
    typ: Zahl
    einheit: m
    genauigkeit_erlaubt: true   # erlaubt "ca. 47" oder "~47"
    trefferquote: 0.18
    diskriminationswert: 0.91
    quiz_tauglich: true
  - name: material
    typ: Aufzaehlung
    aufzaehlung_version: 1
    aufzaehlung: [stein, ziegel, fachwerk, beton, holz]
    trefferquote: 0.62
    diskriminationswert: 0.41
    quiz_tauglich: false
```

**Aufzählungs- und Untertyp-Versionierung:** Aufzählungslisten wachsen über Iterationen. Jede Aufzählung trägt eine Versionsnummer, damit alte Instanz-Werte ihren Listenbezug behalten. `untertyp_aufzaehlung.status: vorlaeufig` markiert, dass aus Untertypen später eigenständige Entitätstypen werden können.

### 4.2 Entitätsinstanz (in den Daten)

```json
{
  "instance_id": "7f3a8b21-...",
  "instance_status": "canonical",
  "ags": "06631013",
  "typ": "kirche",
  "untertyp": "pfarrkirche",
  "bezeichnung": "St. Marien",
  "originalbezeichnung_im_text": "Marienkirche",
  "ortsteil_bezug": "Kleindorf",
  "ortsteil_instance_id": "2c9d1e44-...",
  "quiz_tauglich_override": null,
  "eigenschaften": {
    "baujahr": {
      "wert": 1270,
      "gueltig_ab": null,
      "gueltig_bis": null,
      "ist_vermutlich_aktuell": true,
      "vertrauen_overlay": null,
      "genauigkeit": null
    },
    "hoehe_turm_m": {
      "wert": 47,
      "genauigkeit": "ca."
    },
    "stilrichtung": {"wert": "gotisch"}
  },
  "quelle": {
    "url": "https://de.wikipedia.org/wiki/Mühlhausen",
    "abruf_datum": "2026-06-28",
    "extraktion": {
      "prompt_version": "stufe1-v0.5",
      "llm": "claude-haiku-4.5",
      "katalog_version": "v3"
    },
    "vertrauen_quelle": 0.75,
    "vertrauen_extraktion": 0.92
  }
}
```

### 4.3 Standard-Eigenschaften (gelten für *jeden* Wert)

| Standard-Eigenschaft | Typ | Bedeutung |
|---|---|---|
| `gueltig_ab` | Jahr | seit wann gilt der Wert |
| `gueltig_bis` | Jahr | bis wann galt der Wert (null = aktuell/unbekannt) |
| `ist_vermutlich_aktuell` | Bool | LLM-Selbsteinschätzung |
| `quelle_overlay` | URL | überschreibt Standard-Quelle der Instanz |
| `vertrauen_overlay` | 0..1 | überschreibt das *Gesamtvertrauen* (siehe §4.5) |
| `genauigkeit` | Aufzählung | null / "ca." / "geschaetzt" / "ungefaehr" |

### 4.4 Identitäts-Lebenszyklus (`instance_status`)

Jede Instanz trägt einen Lebenszyklus-Status:

| Status | Bedeutung |
|---|---|
| `canonical` | aktuelle, kanonische Instanz für ihr Realwelt-Objekt |
| `merged` | wurde mit einer anderen Instanz vereinigt; behält `merged_into: <instance_id>`-Referenz |
| `deprecated` | nicht mehr aktuell, aber für Historie erhalten |

**Warum:** Wenn „Pfarrkirche St. Marien" und „Marienkirche" und „St. Marien" als drei verschiedene Extraktionen entstehen, dürfen die nicht-kanonischen Bezeichnungen nicht verschwinden. Sie zeigen weiterhin per `merged_into` auf die kanonische `instance_id`. Provenienz bleibt erhalten (P2).

### 4.5 Vertrauens-Modell — Quelle vs. Extraktion getrennt

Zwei unabhängige Dimensionen:

- **`vertrauen_quelle`** — Vertrauen in die Datenquelle selbst. Klassen:
  - Wikidata-Property mit Quellenqualifier: 0.95
  - Destatis / Bundeswahlleiter direkt: 0.95
  - Wikidata-Property mit mehrdeutigem Statement: 0.90
  - OSM mit `start_date`-Tag: 0.85
  - Wikipedia-Infobox: 0.85
  - Wikipedia-Volltext: 0.75
  - Gemeinde-Webseite (später): 0.70

- **`vertrauen_extraktion`** — Vertrauen in die Extraktion dieses konkreten Werts. LLM-Selbsteinschätzung über Lesbarkeit des Quellsatzes. Klassen:
  - Direktwert in Infobox, unmissverständlich: 0.95
  - Klar paraphrasierbarer Volltext-Satz: 0.85
  - Indirekt erschlossen, Kontext mehrdeutig: 0.50–0.70

**Gesamtvertrauen** (für Quiz-Filter): `min(vertrauen_quelle, vertrauen_extraktion)`. Wird *nicht* gespeichert, sondern bei Bedarf berechnet. `vertrauen_overlay` überschreibt das Gesamtvertrauen für einen Einzelwert.

### 4.6 Ortsteil-Behandlung

**Schicht 1 bleibt flach.** Entitäten wie `kirche`, `muehle`, `naturdenkmal` hängen direkt an der Gemeinde.

Die Standard-Felder **`ortsteil_bezug`** (String, menschenlesbar) und **`ortsteil_instance_id`** (UUID, maschinenlesbar) erfassen den Ortsteil-Kontext. Bei `null` ist die Entität dem Hauptort zugeordnet. Der Ortsteil selbst existiert *zusätzlich* als Entität vom Typ `ortsteil` (0..n). Die Verknüpfung beider Felder erfolgt in Stufe 2 (Canonicalization-Abgleich gegen `ortsteil`-Instanzen).

### 4.7 Instanz-Identität und Canonicalization

Standard-Heuristik für Match: `ags + typ + bezeichnung_canonical`.

**Canonicalization-Stufen:**

1. Trim, Lowercase, Umlaute normalisieren.
2. Honorific-Präfixe entfernen (Pfarr-, Wallfahrts-, Kloster-, Katholische, Evangelische).
3. Längster gemeinsamer Suffix-Match.

**Fallback bei namenlosen Entitäten** (Brunnen ohne Name, namenloses Naturdenkmal, anonymes historisches Ereignis): Match über `identifikator_fallback_bei_namenlos`-Liste aus dem Entitätstyp (z.B. Brunnen: `material + baujahr + lage_im_ort`). Wenn der Fallback keine eindeutige Identität liefert, wird die Instanz vorerst als Singleton angelegt; ein späterer manueller Merge ist über `instance_status: merged` möglich.

**Disambiguierung bei Mehrdeutigkeit:** Wenn zwei Instanzen den gleichen Canonical-Schlüssel haben (z.B. „St. Marien" in zwei Ortsteilen derselben Gemeinde), wird `ortsteil_bezug` als Disambiguator herangezogen. Bleibt die Mehrdeutigkeit bestehen, wird ein manueller Merge-Entscheid erforderlich.

> Die `instance_id` wird durch Identitätsabgleich (Canonicalization) bestimmt. Die Standard-Heuristik darf durch manuelle Korrekturen oder zusätzliche Regeln ergänzt werden (P7).

### 4.8 `quiz_tauglich`-Modell (zweistufig)

- **Im Katalog (Typ-Ebene):** `quiz_tauglich` pro Eigenschaft. Default für Quiz-Auswahl.
- **Auf der Instanz (Wert-Ebene):** `quiz_tauglich_override` (default `null`). Erlaubt Einzelfall-Ausschluss eines unsicheren Werts, ohne den Katalog zu ändern.

Quiz-Filter-Regel: Instanz-Override gewinnt, falls gesetzt; sonst Katalog-Default.

### 4.9 Speicher-Format Iterationen 1–2

JSON-Lines (eine Zeile pro Entitätsinstanz). Robust gegen Schema-Änderungen, diffbar in Git, verlustfrei nach SQLite/Postgres/DuckDB konvertierbar. Endgültiges DB-Backend nach Iteration 2.

### 4.10 Daten-Versionierung

Jede Instanz trägt `prompt_version`, `llm`, `katalog_version` im `quelle.extraktion`-Block. Re-Extraktionen erzeugen neue Instanzen, vereinigt über `instance_id` und `instance_status: merged`.

### 4.11 Freitext-Promotion

Werte mit Datentyp `Freitext` (typischerweise unter `beschreibung`) sind explizit *promovierbar*. Wenn wiederkehrende Muster destilliert werden können (z.B. „brannte 1923 ab" → strukturierte Eigenschaft `abgebrannt_jahr`), wird die Eigenschaft im Katalog promoviert, betroffene Instanzen re-extrahiert. P3-konform.

### 4.12 Mehrquellen-Modell (Evolutionsrichtung)

v0.5 modelliert *eine* Hauptquelle pro Instanz mit Overlay-Mechanismus pro Wert. Wenn in späteren Iterationen erkennbar wird, dass eine Mehrheit der Werte aus mehreren parallelen Quellen stammt (Wikipedia + Wikidata + OSM + Destatis gemeinsam), wird die `quelle{}`-Struktur zu einer `sources[]`-Liste evolviert. Diese Migration ist additiv (P3) und wird nicht spekulativ in v0.5 vorgenommen.

---

## 5. Datentypen

| Datentyp | Beispiel | Distraktor-Strategie |
|---|---|---|
| **Zahl** | Höhe, Einwohnerzahl, Amtsdauer | Werte gleicher Eigenschaft aus Pool |
| **Jahr** | Baujahr, Ersterwähnung | Werte gleicher Eigenschaft aus Pool |
| **Zeitraum** | Bauzeit 1270–1278, Amtszeit 1998–2012 | gleichformatige Zeiträume aus Pool |
| **Bool** | hat_freibad, ist_parteilos | Pool-Orte mit Gegenwert |
| **Aufzählung** | Partei, Konfession, Stilrichtung | andere zulässige Aufzählungs-Werte |
| **Name** | Bürgermeister-Name, bezeichnung | Namen aus Pool-Orten |
| **Freitext** | Sage-Inhalt, beschreibung | Pool-Orte als ganze Orte (Achse C); promovierbar |

**Wertgenauigkeit:** Eigenschaften vom Typ `Zahl`, `Jahr`, `Zeitraum` können das Standard-Feld `genauigkeit` tragen (null / "ca." / "geschaetzt" / "ungefaehr"). Damit lassen sich ungenaue Quellen-Angaben („Kirchturm etwa 47 m hoch") sauber repräsentieren.

---

## 6. Frage-Achsen

| Achse | Form | Distraktor-Pool |
|---|---|---|
| **A** | Ort fest → Wert gesucht | Werte gleicher Eigenschaft aus Pool |
| **B** | Wert fest → Ort gesucht (Top/Bottom) | Pool-Orte mit Werten gleicher Größenklasse |
| **C** | Entität/Eigenschaft fest → Ort gesucht | Pool-Orte **ohne** das gesuchte Merkmal (§10) |
| **D** | Geo-Relation → Ort gesucht | Bedingungs-Quadranten |

### 6.1 Snapshot-Default-Regel

Ohne expliziten historischen Bezug verwenden Quizfragen Werte mit `gueltig_bis = null` UND `ist_vermutlich_aktuell = true`. Bei `0..1`-Entitäten (Bürgermeister, Wappen) rigoroser Filter: nur Werte mit Wikidata-Bestätigung oder `ist_vermutlich_aktuell = true` gehen in Gegenwarts-Fragen. Historische Fragen nutzen das Gültigkeits-Fenster gezielt.

---

## 7. Zwei Metriken

### 7.1 Trefferquote
Anteil der Orte mit Wert. Bei seltenen Entitätstypen zusätzlich **bedingte Trefferquote** (Anteil innerhalb der Orte mit Entität).

### 7.2 Diskriminationswert — experimentell

> Der Diskriminationswert ist eine *experimentelle* Bewertungsfunktion. Startformeln dienen als Ausgangspunkt, werden nach Iteration 2 anhand empirischer Quizqualität nachjustiert.

- **Bool / Aufzählung**: normalisierte Shannon-Entropie, [0,1].
- **Zahl / Jahr / Zeitraum**: normalisierter Variationskoeffizient. Normalisierung auf [0,1] durch Kappung beim 95-Perzentil oder Division durch (1+CV), je nach Wertebereich.
- **Name / Freitext**: Anteil eindeutiger Werte.

### 7.3 Quiz-Tauglichkeit (Implementierungs-Notiz)

| | hoher Diskriminationswert | niedriger Diskriminationswert |
|---|---|---|
| **hohe Trefferquote** | Achse A/C funktionieren; Achse B problematisch (keine Cluster) | quiz-trivial, `quiz_tauglich: false` |
| **niedrige Trefferquote** | Achse C (Singleton-Gold) | Singleton-Klassifizierung nötig (§8.4) |

Hohe Eindeutigkeit qualifiziert für A/C, nicht für B (B braucht Cluster).

---

## 8. Iterative Katalog-Entdeckung

**Iteration 1 — Saat (~10 Orte):** manuell ausgewählt, parallel LLM-Extraktion + Wikidata-SPARQL. Output: erste Liste von Entitätstypen + Eigenschaften.

**Iteration 2 — Erweiterung (~50 Orte):** Metriken messen, Canonicalization-Heuristik validieren.

**Iteration 3 — Stabilisierung (~200 Orte):** Sättigung bei <~5% neue Typen/Eigenschaften in den letzten 100 Orten.

**Vollausrollung (~10.700 Orte):** Schemagebunden, mit Freitext-Promotion-Mechanismus offen.

### 8.4 Singleton-Klassifizierung

Eigenschaften mit Trefferquote <5%:

- **`sichtbar_oder_historisch`** (Quiz-Gold): Naturdenkmal, historisches Bauwerk, Drehort, prominente Persönlichkeit, kulturelle Eigenheit. *„Würde an einem Ortsschild auffallen?"*
- **`administrativ_oder_trivial`** (`quiz_tauglich: false`): seltene Verwaltungs-Details ohne Außenwirkung.

---

## 9. Anbieter-agnostische Extraktions-Prompts

### 9.1 Stufe 1 — Schemafreie Extraktion (Iterationen 1–3)

```
ROLLE: Du analysierst einen Quelltext über eine deutsche Gemeinde und
extrahierst quizfähige Fakten in einer Entität-Eigenschaft-Wert-Struktur.

EINGABE: Quelltext (Wikipedia-Artikel o.ä.) über die Gemeinde {ORTSNAME}.

AUFGABE: Identifiziere im Text alle Entitäten (Substantive) mit Bezug
zu diesem Ort. Liefere zu jeder Entität die im Text genannten
Eigenschaften mit Werten.

ENTITÄTEN sind z.B.: Ort selbst, Bürgermeister, Kirche, Rathaus,
Mühle, Brunnen, Persönlichkeit, Brand, Sage, Partnergemeinde,
Naturdenkmal, Ortsteil, ...

FORMAT (eine Entitätsinstanz pro Block):
  ENTITÄT: <typ in snake_case>
  BEZEICHNUNG: <z.B. "St. Marien", wenn 0..n>
  ORTSTEIL_BEZUG: <Ortsteil-Name, falls im Ortsteil statt Hauptort>
  EIGENSCHAFTEN:
    <eigenschaft>: <wert> [<einheit>]
    <eigenschaft>: <wert>
  GUELTIG_AB: <Jahr, optional>
  GUELTIG_BIS: <Jahr, optional>
  IST_VERMUTLICH_AKTUELL: <true|false>
  VERTRAUEN_EXTRAKTION: <0..1, Selbsteinschätzung der
    Extraktionssicherheit für diesen Block>

REGELN:
  - Erfinde nichts. Bei Unsicherheit weglassen.
  - Mehrere Entitäten gleichen Typs sind erlaubt: eigener Block
    pro Vorkommen, jeweils mit BEZEICHNUNG.
  - Schließe implizite Ortseigenschaften ein: "Die Kreisstadt
    Mühlhausen" → ENTITÄT: ort, EIGENSCHAFTEN: ist_kreisstadt: true.
  - Zeitlich begrenzte Werte mit GUELTIG_AB / GUELTIG_BIS.
  - IST_VERMUTLICH_AKTUELL: Präsens ohne Enddatum → true. Enddatum
    oder historischer Kontext → false. Unsicher → false.
  - Wertgenauigkeit: Bei ungenauen Angaben Wert mit Modifier
    versehen: "ca. 47" → wert: 47, genauigkeit: "ca.".
  - Zeiträume als <jahr>-<jahr> (z.B. bauzeit: 1270-1278).
  - Triviale Standard-Infrastruktur (Bushaltestelle, Supermarkt)
    nur wenn der Artikel sie hervorhebt.
  - Schreibe Eigenschafts- und Entitätsnamen frei.
  - Wenn ein Fakt nicht in (Entität, Eigenschaft, Wert) passt:
    Eigenschaft "beschreibung" mit Freitext-Wert.

AUSGABE: Nur die Liste.
```

### 9.2 Stufe 2 — Katalog-Konsolidierung

Wie v0.4 §8.2, ergänzt um:
- Aufzählungs-Versionen mitführen.
- Disambiguierung über `ortsteil_bezug` bei doppelten Canonical-Schlüsseln.
- Verknüpfung `ortsteil_bezug` ↔ `ortsteil_instance_id`.
- Konflikte LLM vs. Wikidata markieren (§11.1).

### 9.3 Stufe 3 — Schemagebundene Vollausrollung

Wie v0.4 §8.3.

---

## 10. Distraktor-Pool — räumlich vor administrativ

Pool-Eskalation bis ≥10 Kandidaten:

1. Geo-Nachbarn im 30-km-Radius
2. Geo-Nachbarn im 75-km-Radius
3. Gleiche Gemeindegrößenklasse im selben Bundesland
4. Deutschlandweit (Fallback)

**Geografie schlägt Administration** — Spielgefühl.

### 10.1 Achse-C-Spezifik

Für Achse C („In welchem dieser Orte ist 1623 die Mühle abgebrannt?") werden aus dem Pool nur Orte ausgewählt, die das gesuchte Merkmal **nicht** besitzen. Wenn der Pool dadurch unter 3 negative Kandidaten fällt, wird die Eskalation eine Stufe weitergeschaltet, bis genug Kandidaten vorliegen.

---

## 11. Datenquellen

1. **Wikidata** (SPARQL, CC0) — schon ab Iteration 1 parallel zur LLM-Extraktion.
2. **OSM** (Overpass, ODbL).
3. **Wikipedia-Volltext** — Hauptquelle für LLM-Extraktion.
4. **Destatis, Bundeswahlleiter**.
5. **Gemeinde-Webseiten** — nicht in v0.x.

### 11.1 Konfliktregel Wikidata vs. LLM

1. Wikidata-Wert wird bevorzugt (höheres `vertrauen_quelle`).
2. LLM-Wert wird *nicht verworfen*, sondern als alternativer Wert in `alternativen[]` der Eigenschaft mit eigener Quellenangabe gespeichert. P2.
3. In Stufe 2 manuelle Prüfung der Konflikte.
4. Bei wiederholter Wikidata-Veraltung wird `vertrauen_quelle` für die betroffene Property nach Iteration 2 nachjustiert.

---

## 12. Politik-Daten

Wahldaten als Entität `wahl` mit Eigenschaften `wahlbeteiligung_prozent`, `staerkste_partei`, plus `gueltig_ab`/`gueltig_bis` zur Wahlperiode. Keine parteispezifischen Stimmenanteile.

---

## 13. Snapshot-Rhythmus

- **Initial einmalig** für den Datenbank-Aufbau (Iterationen 1–3 plus Vollausrollung).
- **Danach jährlich** (vorgesehen: Januar, nach Jahreswechsel und nach Kommunalwahlen).
- Inkrementelle Re-Extraktion zwischenzeitlich nur für gezielte Korrekturen oder bei Kipp-Auslösung K6.

---

## 14. Anti-Rucksack-Liste

In v0.5 explizit *nicht* gebaut:

- Keine Gemeinde-Webseiten-Crawler.
- Keine Vektor-DB / Embeddings.
- Keine eigene NLP-Pipeline.
- Keine Live-Aktualisierung — Batch-Snapshot mit Jahresrhythmus.
- Keine Edition-Integration in QuizAway — separate Baustelle (§20).
- Keine Anbieter-Bindung.
- Keine fixe Entität-/Eigenschaft-Liste vorab.
- Keine Entitäts-Vererbung in Iteration 1.
- Keine GPS-Trigger-Integration — App-Schicht.
- Keine separate Ortsteil-Wurzelebene — gelöst via `ortsteil_bezug` + `ortsteil_instance_id`.
- Keine `sources[]`-Mehrquellen-Struktur — Evolution nach Bedarf (§4.12).
- Keine automatische Merge-UI — manuell mit `instance_status`.
- Keine eigenständige Quiz-Generator-Bibliothek — diese baut auf der DB auf, ist nicht Teil der DB.

---

## 15. Kipp-Kriterien

- **K1:** Iteration 1 liefert <10 verschiedene Entitätstypen.
- **K2:** Iteration 3 + 500-Orte-Ausweitung halten Neuigkeitsrate über 5%.
- **K3:** Distraktor-Pools selbst nach §10-Eskalation zu klein/leer.
- **K4:** Singleton-Klassifizierung gelingt in Stufe 2 nicht zuverlässig.
- **K5:** >30% der Fakten lassen sich keiner stabilen Entität/Eigenschaft zuordnen.
- **K6:** Stichprobe 20 zeitabhängige Instanzen nach Iter 2 zeigt >4 aktuell falsche Werte mit `ist_vermutlich_aktuell: true`, die per Wikidata sofort als veraltet erkennbar wären → LLM-only für zeitabhängige Daten ungeeignet, Fallback: Wikidata/Destatis als Primärquelle für `gueltig_bis=null`-Werte.

---

## 16. Entitäts-Katalog als Artefakt

Eigene Markdown-Datei `entitaets-katalog-v<N>.md`, versioniert wie ADRs. Pro Typ Felder gemäß §4.1. Diffs diskutierbar.

---

## 17. Differenz zu v0.4

**Neuer §1 — Architekturprinzipien** (8 Leitplanken).

**Datenmodell-Erweiterungen:**
- `instance_status` (canonical / merged / deprecated) mit `merged_into`-Referenz (§4.4).
- `ortsteil_instance_id` zusätzlich zum String (§4.6).
- Vertrauen aufgeteilt in `vertrauen_quelle` und `vertrauen_extraktion`; Gesamtvertrauen = min (§4.5).
- Datentyp `Zeitraum` (§5).
- Standard-Eigenschaft `genauigkeit` (null / "ca." / "geschaetzt") (§4.3, §5).
- `quiz_tauglich_override` auf Instanz-Ebene (§4.8).
- Aufzählungs-Versionierung (§4.1).
- `identifikator_fallback_bei_namenlos` im Entitätstyp (§4.1, §4.7).

**Canonicalization erweitert:**
- Fallback für namenlose Entitäten (§4.7).
- Disambiguierung via `ortsteil_bezug` (§4.7).

**Operative Regeln:**
- Achse-C-Distraktoren *ohne* Merkmal (§10.1).
- Wikidata-Property-Schichteinordnung als Implementierungsnotiz (§3.3).
- Snapshot-Rhythmus jährlich (§13).
- `sources[]`-Mehrquellen-Struktur als Evolutionsrichtung dokumentiert (§4.12).

**Prompt-Erweiterungen (Stufe 1):**
- `VERTRAUEN_EXTRAKTION` als Selbsteinschätzung pro Block.
- Wertgenauigkeit explizit („ca. 47").
- Zeiträume als `<jahr>-<jahr>`.

---

## 18. Reviewer-Synthese (drei Runden)

Insgesamt 9 Reviews über drei Runden (Claude / ChatGPT / Gemini parallel auf v0.2, v0.3, v0.4). Synthese nach stärkstem Argument, Konvergenzen über Reviewer als Vertrauenssignal.

**Konvergenzen Runde 3** (mehrfach unabhängig genannt):
- `ortsteil_instance_id` neben String (ChatGPT + Gemini) — übernommen.

**Aus Runde 3 übernommen:**
- *ChatGPT:* Architekturprinzipien als eigener Abschnitt; `instance_status` (canonical/merged/deprecated); Vertrauen Quelle vs. Extraktion getrennt; Canonicalization-Fallback für namenlose Entitäten; Datentyp Zeitraum; Wertgenauigkeit; Aufzählungs-Versionierung; `sources[]` als Evolution dokumentiert.
- *Gemini:* `ortsteil_instance_id`-Verknüpfung; `quiz_tauglich_override` auf Instanz; Canonicalization-Disambiguator via `ortsteil_bezug`; Achse-C-Distraktor-Spezifik; Wikidata-Property-Schicht-Notiz; Snapshot-Rhythmus.
- *Claude:* keine neuen Punkte, Bestätigung der Implementations-Reife.

**Aus früheren Runden weiterhin gültig:** Typ/Instanz-Trennung; Quellen-Metadaten; Versionierung; JSON-Lines; Wikidata in Iter 1; Diskriminationswert; Schicht-Trennung nach Ableitbarkeit; Ortsteil als Entität + Bezug; Snapshot-Default-Zeit; Konfliktregel; Distraktor-Eskalation räumlich vor administrativ; K6 operationalisiert; Freitext-Promotion; `quiz_tauglich` allgemein.

---

## 19. Offene Fragen

- **F1 — Granularität:** Gelöst durch `ortsteil_bezug` + `ortsteil_instance_id` + Ortsteil-als-Entität.
- **F2 — App-Identität:** Edition oder eigenständige App? Beeinflusst DB-Modell nicht (§20).
- **F3 — Schwellwerte:** Empirisch in Iteration 2 zu bestätigen.
- **F4 — KI-Modell-Wahl:** anbieter-agnostisch.
- **F5 — DB-Backend:** entschieden nach Iteration 2.
- **F6 — Canonicalization-Tragfähigkeit:** Standard-Heuristik (§4.7) ausreichend, oder Merge-UI nötig? Iteration 1 wird es zeigen.

---

## 20. Einhängung ins QuizAway-Konzept (separate Baustelle)

Dieses Basiskonzept beschreibt **nur die Datenbank-Inhaltsschicht**. Zwei nachgelagerte Baustellen sind davon getrennt:

**B1 — Edition-Einhängung in QuizAway:**
Die Gemeinde-Achsen-Datenbank wird als neue **Edition** in QuizAway eingehängt (Arbeitstitel: „Ortsschild-Edition"). Edition-Konzept analog zu MixMi! mit `editionContext` und Curation-Status (`draft` → `ready`). Die Frage-Generierung (Achsen A/B/C/D aus §6) ist Teil der Edition, nicht der DB. Eigenes Konzeptdokument erforderlich.

**B2 — App-Umstellung QuizAway:**
QuizAway selbst muss auf die neue technische Basis (`@xalento/p2p-tele` Transport, `QuizAwayMatchCoordinator` Domain-Layer, `editionContext`-fähiges Edition-Picking) umgestellt werden, bevor die neue Edition produktiv geht. Bisher: pures 1-of-4-Multiple-Choice mit fester Frage-Quelle. Neu: Edition-Auswahl, Ortsschild-Edition mit GPS-Trigger-Vorschlägen, P2P-Multiplayer mit Mitfahrenden im Auto/Zug. Eigenes Konzeptdokument erforderlich.

Beide Baustellen sind unabhängig von Iteration 1 dieser DB. Sie laufen parallel oder sequenziell, aber stören sich nicht. Iteration 1 der DB liefert frühestens nach 50 Orten (= Iteration 2) belastbare Daten für ein erstes spielbares Edition-Prototyp.

---

## 21. Nächste Schritte

1. **Iteration 1 (10 Orte)** als erstes Implementierungs-Artefakt:
   - 10 Orte auswählen (Vielfaltskriterium §8).
   - Wikidata-SPARQL parallel zur LLM-Extraktion.
   - Stufe-1-Prompt (§9.1) anwenden.
   - JSON-Lines-Output, Schema gemäß §4.2.
   - Canonicalization-Heuristik manuell prüfen.
   - Konflikte (Wikidata vs. LLM) dokumentieren.
2. **Manuelle Stufe 2** (§9.2) über die 10-Orte-Ausgabe → Katalog v1.
3. **Iteration 2 (50 Orte)** mit Katalog v1 — Metriken messen, K1–K6 prüfen, Canonicalization-Tragfähigkeit beurteilen.
4. **Re-Evaluation** nach jeder Iteration.
5. **Parallel:** Konzepte für B1 (Edition-Einhängung) und B2 (App-Umstellung) starten — siehe §20.

---

*Ende v0.5 — final.*
