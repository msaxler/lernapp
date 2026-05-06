# ADR-001: Copilot-Architektur-Pattern

**Status:** Proposed
**Datum:** 2026-05-06
**Revision:** 3 (Rev 2: Pilot QuizAway, Zwei-Zeitstempel-Modell, dreistufige Verfallslogik, Test-Disziplin · Rev 3: Feld-2-Regel auf Primärquellenreferenz generalisiert für Cross-Domain-Übertragbarkeit)
**Geltungsbereich:** Übergreifend für alle domänenspezifischen Copilot-Systeme.
Aktuelle Instanzen: GeoClaude/P2F2 (Geologie), LernApp inkl. QuizAway (Lernen),
Mike-Copilot (eigene Entwicklungsprojekte), zukünftige KMU-Industrieberatung
Region Neuwied.

---

## 1. Kontext

**Problem:** Mobiler Zugriff auf fragmentiertes Projektwissen.
Entscheidungen, Konzepte und aktuelle Arbeitsstände liegen verteilt in ADRs,
Konzeptdokumenten, Code-Repos und impliziten Kontexten. In mobilen Situationen
(Voice-Eingabe, Ad-hoc-Fragen) ist tiefes Retrieval zu langsam und führt zu
unspezifischen oder veralteten Antworten.

**Ziel:** Entscheidungsfähige Antworten in Echtzeit, mit klarem Quellenbezug
und expliziter Unsicherheitskennzeichnung. Das System muss konsistent über
mehrere Domänen und Nutzergruppen funktionieren (Geologen, Lernende, Mike
selbst, KMU-Inhaber).

**Nicht-Problem:** Reine Wissensspeicherung — dafür existieren Primärquellen
(ADRs, Konzepte, Vault-Einträge) bereits.

---

## 2. Entscheidung

Einführung eines einheitlichen Copilot-Patterns für alle domänenspezifischen
Assistenzsysteme. Das Pattern besteht aus vier gekoppelten Bestandteilen:

1. **Antwort-Kontrakt** — verbindliche 5-teilige Struktur jeder Antwort
2. **STATUS.md** — pro Projekt ein komprimiertes Statuspapier als primärer
   Einstiegspunkt für Retrieval
3. **Ableitungsregel** — STATUS.md ist Projektion, keine Primärquelle
4. **Verfallslogik** — dreistufiges Laufzeitverhalten bei nicht bestätigtem
   Aktivem Fokus

Die vier Bestandteile sind operativ untrennbar und werden gemeinsam in diesem
ADR festgelegt.

---

## 3. Antwort-Kontrakt

Jede Antwort eines Copilot-Systems folgt dieser Struktur:

1. **Kurzantwort** — die konkrete Maßnahme oder Aussage, ein bis zwei Sätze
2. **Kontext** — wann, wo, in welchem Projekt/Modul/Fall
3. **Quellen** — Verweis auf konkrete Primärquellen (ADR-Nummer, Vault-ID,
   Konzept, Dokument, Beratungsprotokoll)
4. **Empfehlung** — konkreter nächster Schritt
5. **Unsicherheitshinweis** — explizite Kennzeichnung bei unvollständiger oder
   nicht bestätigter Datenlage

**Verpflichtende Regel zum Unsicherheitshinweis (Feld 5) — dreistufig:**

Berechnet gegen das `Bestätigt`-Datum in STATUS.md Feld 0
(siehe Abschnitt 4). N = heute − `Bestätigt`.

Die Schwellwerte sind **domänenspezifisch konfigurierbar** (siehe Abschnitt 10).
Standardwerte (Mike, Software-Projekte):

- **Stufe 1 — N ≤ 3 Tage:** kein Hinweis erforderlich.
- **Stufe 2 — N > 3 Tage:**
  > „Aktiver Fokus seit N Tagen nicht bestätigt. Stand kann unverändert
  > sein oder überholt."
- **Stufe 3 — N > 10 Tage:**
  > „Aktiver Fokus seit N Tagen nicht bestätigt. Hohe Wahrscheinlichkeit,
  > dass Kontext unvollständig oder überholt ist."

**Designprinzip:** Der Assistent macht keine Aussage über Veralterung
(epistemisch nicht haltbar bei reinem Zeitdelta), sondern über fehlende
Bestätigung. Diese Unterscheidung ist verpflichtend.

---

## 4. STATUS.md-Schema

Pro Projekt existiert genau ein STATUS.md. **Keine Aufsplittung pro Modul,
Feature oder Sub-Projekt.** Sub-Projekte erhalten Erwähnung im Hauptpapier,
aber kein eigenes Statuspapier.

```markdown
# Projekt: <Name>
## Stand: YYYY-MM-DD

> Projektion aus Primärquellen (ADRs, Konzepte, Vault-Einträge, Tasks).
> Bei Widerspruch gilt die Primärquelle.

## 0. Aktiver Fokus
Geändert: YYYY-MM-DD
Bestätigt: YYYY-MM-DD
[1–2 Sätze, genau ein laufender Arbeitsstrang.
 Beschreibt operative Tätigkeit, nicht Ziel oder Kontext.]

## 1. Aktueller Zustand (max 5 Bulletpoints)
- ...

## 2. Letzte Entscheidungen
- YYYY-MM-DD: <Kurzbeschreibung> (<Primärquellenreferenz>)

## 3. Offene Punkte (entscheidungsrelevant)
- ...

## 4. Nächste Schritte (konkret)
- ...

## 5. Relevante Artefakte (max 5)
- <Typ> <Titel> → <Pfad/URL>
```

**Feldregeln im Detail:**

- **Feld 0 (Aktiver Fokus):** genau ein Strang, 1–2 Sätze, operative
  Tätigkeit. Negativbeispiele: „Wir arbeiten an Performanceverbesserung",
  „Ziel ist bessere UX". Positivbeispiel: „Seit 2026-05-04: Debugging
  Oboe-Decode-Stall auf A34, Hypothese B wird getestet."
- **Feld 0 — Zwei-Zeitstempel-Modell:**
  - `Geändert` springt nur, wenn der Inhalt sich ändert.
  - `Bestätigt` springt jedes Mal, wenn STATUS.md gespeichert wird, auch
    ohne Inhaltsänderung. Damit zählt das bewusste Öffnen und Speichern als
    Bestätigung, dass der Stand nach wie vor gilt.
  - Beide Felder zeilenbasiert, je ein Wert pro Zeile (für Parsing-
    Stabilität in Phase 2).
- **Feld 1:** maximal 5 Bulletpoints. Längere Listen brechen mobile Nutzung.
- **Feld 2:** jeder Eintrag *muss* eine Primärquellenreferenz tragen
  (siehe Abschnitt 5). Art der Referenz ist domänenspezifisch.
- **Feld 5:** maximal 5 Einträge mit Pfad/URL. Sonst wird das Feld zur
  Linkhalde.

---

## 5. Ableitungsregel

**STATUS.md ist eine Projektion aus Primärquellen, nie selbst Primärquelle.**

Konkret heißt das:

- Eine Entscheidung, die nur in STATUS.md steht und nirgendwo sonst, ist
  *keine getroffene Entscheidung*. Sie gehört in Feld 3 (Offene Punkte) als
  „Entscheidung X getroffen, Primärquelle fehlt noch", bis sie als
  Primärquelle existiert.
- Eine Konzeptaussage, die nur in STATUS.md steht, ist nicht autoritativ.
- Bei Widerspruch zwischen STATUS.md und einer Primärquelle gewinnt immer die
  Primärquelle.

**Harte Folgeregel — keine Entscheidung ohne Primärquellenreferenz:**
Feld 2 darf keine Einträge ohne Primärquellenreferenz enthalten. Diese Regel
operationalisiert das Ableitungsverbot und verhindert, dass Entscheidungen
nur in STATUS.md verschwinden.

**Domänenspezifische Primärquellen:**

| Domäne | Primärquelle | Referenz-Format |
|---|---|---|
| Software-Projekte (Mike) | ADR | `ADR-NNN` |
| Geodaten / P2F2 | Vault-Eintrag, Gutachten | `Vault-ID` / `Gutachten-Nr.` |
| KMU-Beratung | Beratungsprotokoll | `Protokoll-YYYY-MM-DD` |

**Implizite Konsequenz (explizit benannt):**
Ein Projekt ohne aktuelle Primärquellen kann keinen stabilen Copilot haben.
Bevor ein Projekt produktiv im Copilot eingebunden wird, müssen mindestens
die zentralen Architektur-/Fach-Entscheidungen als Primärquellen vorliegen.

---

## 6. Verfallslogik

**Referenzzeitpunkt:** `Bestätigt`-Datum aus STATUS.md Feld 0.
N = heute − `Bestätigt`.

**Dreistufiges Laufzeitverhalten des Assistenten:**

| Stufe | Bedingung | Verhalten in Antwort-Feld 5 |
|-------|-----------|-----------------------------|
| 1 | N ≤ S1 | kein Hinweis |
| 2 | S1 < N ≤ S2 | „Aktiver Fokus seit N Tagen nicht bestätigt. Stand kann unverändert sein oder überholt." |
| 3 | N > S2 | „Aktiver Fokus seit N Tagen nicht bestätigt. Hohe Wahrscheinlichkeit, dass Kontext unvollständig oder überholt ist." |

S1 und S2 sind domänenspezifisch konfiguriert (siehe Abschnitt 10).

**Begründung der Standardschwellen (Mike, Software):**

- **S1 = 3 Tage:** Mike arbeitet typischerweise in Sprintzyklen von wenigen Tagen.
  Innerhalb von 3 Tagen ist eine fehlende Bestätigung normal und kein Signal.
- **S2 = 10 Tage:** klare binäre Schwelle, ausreichend Abstand zu Stufe 2.

**Designprinzip — keine Pseudo-Diagnose:**
Der Assistent kann aus reinem Zeitdelta nicht ableiten, ob ein Stand
veraltet *ist*. Er kann nur ableiten, dass er nicht bestätigt *wurde*.

---

## 7. Betriebsregeln

**Phase 1 — manuelle Pflege (initial):**

- STATUS.md wird manuell aktualisiert, primär am Ende einer Arbeitssession
  am PC.
- Feld 2 (Letzte Entscheidungen) wird manuell befüllt mit Primärquellenreferenz.
- **Update-Disziplin:** maximal 1 STATUS.md-Update pro Arbeitssession.
  Keine Live-Nachführung während der Arbeit.
- **Bestätigt-Disziplin:** `Bestätigt` wird beim Speichern auf das aktuelle
  Datum gesetzt — entweder = heute oder unverändert. Kein Rückdatieren,
  kein Vorausdatieren.
- Aufnahme weiterer Projekte in den Copilot erst nach erfolgreichem
  Pilot-Review (siehe Abschnitt 8).

**Phase 2 — Teilautomatisierung (später):**

- Custom Command `/status-update` in Claude Code: liest letzte Commits +
  Primärquellen-Änderungen, schlägt STATUS.md-Diff vor, Nutzer bestätigt oder editiert.
  Setzt `Bestätigt` automatisch.
- Custom Command `/extract-decisions`: liest neue Primärquellen der letzten 14 Tage
  und schlägt Diff für Feld 2 vor.
- Vollautomatische Aktualisierung ist explizit kein Ziel.

**Übergang Phase 1 → Phase 2:** erst nach erfolgreichem Pilot und nach
mindestens 14 Tagen stabilem manuellem Betrieb.

---

## 8. Validierung

**Pilot-Projekt:** QuizAway.

**Begründung:** Reale Änderungsdynamik durch bevorstehende Umstrukturierung,
vorhandene Artefakte (P2P-Architektur, Nostr-Signaling, ICE/TURN-Konfiguration,
Geo.sqlite-Distribution), erzwungene Primärquellen-Disziplin durch laufende
Entscheidungen, mittlere Komplexität ohne Selbstreferenzialität.

**Validierungskriterien (alle drei müssen erfüllt sein):**

1. **Initialaufbau:** STATUS.md für QuizAway ist in maximal 30 Minuten
   befüllbar.
2. **Pflegbarkeit über Zeit:** Nach 14 Tagen realer Nutzung ist das Schema
   ohne strukturelle Änderung weiter pflegbar.
3. **Antwortqualität:** Reale mobile Fragen über 14 Tage werden mit
   ausreichender Präzision beantwortet, gemessen am Fehlerprotokoll.

**Test-Disziplin (verpflichtend):**

- **Mindestnutzung:** mindestens 3 echte Abfragen pro Tag, mobil gestellt.
- **Update-Disziplin:** maximal 1 STATUS.md-Update pro Arbeitssession.
- **Fehlerprotokoll:** für jede schlechte Antwort:

  ```
  Abfrage: <Frage>
  Schlechte Antwort? ja/nein
  Wenn ja:
    Symptom: [Kontext fehlt | nicht aktuell | falsche Priorisierung | andere]
    Ursache: [STATUS.md unvollständig | Primärquelle fehlt | Retrieval-Problem | andere]
  ```

**Falsifikationskriterium:** Wenn STATUS.md über 14 Tage nicht konsistent
aktuell gehalten werden kann, oder wenn das Fehlerprotokoll überwiegend
„STATUS.md unvollständig" als Ursache zeigt, ist das Pattern in seiner
aktuellen Form gescheitert.

---

## 9. Konsequenzen

**Positive Wirkungen:**

- Erzwingt Primärquellen-Disziplin durch Kopplung an Feld 2.
- Reduziert Kontextverlust bei mobilen Ad-hoc-Fragen.
- Schafft einheitliche Antwortqualität über alle Copilot-Domänen.
- Liefert ein vorzeigbares Produkt-Artefakt für KMU-Beratungsmandate.

**Negative Wirkungen / Trade-offs:**

- Erhöht initialen Pflegeaufwand pro Projekt.
- Verlangt Disziplin bei der Pflege des Aktiven Fokus.
- Macht Primärquellen-Lücken in bestehenden Projekten sichtbar.

**Risiken:**

- Pflegeaufwand wird unterschätzt → STATUS.md veraltet → Antwortqualität sinkt.
  Gegenmaßnahme: Verfallslogik macht fehlende Bestätigung sichtbar.
- `Bestätigt`-Datum wird aus Bequemlichkeit rückdatiert.
  Gegenmaßnahme: explizite Disziplin-Regel in Abschnitt 7.

---

## 10. Domänen-Konfiguration (Erweiterungspunkt)

Beim Onboarding einer neuen Domäne werden folgende Parameter festgelegt:

| Parameter | Beschreibung | QuizAway/Mike | P2F2/Peter |
|---|---|---|---|
| S1 (Verfallsstufe 2 ab) | Typische Sprintlänge | 3 Tage | 7 Tage |
| S2 (Verfallsstufe 3 ab) | Klare Inaktivitätsgrenze | 10 Tage | 21 Tage |
| Primärquellentyp | Art der Autoritätsquelle | ADR | Vault-ID / Gutachten-Nr. |
| Aktiver-Fokus-Granularität | Wie spezifisch Feld 0 ist | Modul/Feature | Projekt/Gutachten |

P2F2-Werte sind vorläufig und werden beim P2F2-Pilot-Onboarding bestätigt.

---

## 11. Nicht-Ziele

- **Kein Ersatz für Primärdokumente.**
- **Keine vollständige Automatisierung.**
- **Kein eigenes Statuspapier pro Modul oder Sub-Projekt.**
- **Keine Aufnahme von Code in STATUS.md.**
- **Kein generisches Wissenstool.**
- **Keine harte „veraltet"-Aussage.**

---

## Revisionshistorie

| Rev | Datum | Änderung |
|---|---|---|
| 1 | 2026-05-06 | Initialer ADR, einstufige Verfallslogik (3 Tage), einfacher Zeitstempel |
| 2 | 2026-05-06 | Pilot auf QuizAway; Zwei-Zeitstempel-Modell; dreistufige Verfallslogik (≤3 / >3 / >10); Test-Disziplin formalisiert |
| 3 | 2026-05-06 | Feld-2-Regel generalisiert: „ADR-Referenz" → „Primärquellenreferenz" mit Domänen-Tabelle; Abschnitt 10 (Domänen-Konfiguration) ergänzt; S1/S2-Parametrisierung für P2F2 vorläufig eingetragen |
