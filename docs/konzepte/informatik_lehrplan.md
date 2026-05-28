# Informatik Sek I — Lehrplan & Modulstruktur

*Version 1.0 · April 2026 · Konzeptdokument für LA-12, LA-13, LA-23*

---

## 1. Überblick

Xalento zielt auf **Informatik Sekundarstufe I** als strategisches Ziel-Fach (DOK-3 C.9).
Grundlage ist der Lehrplan Gymnasium RLP Informatik Sek I — gegliedert in vier Kompetenzbereiche,
verteilt auf Klasse 5–10. Die Plattform deckt zunächst Klasse 5–8 ab (5 Module, Pareto-Startpunkt: Modul 1).

**Technologischer Differenziator:** Informatik erlaubt Player-Typen die kein anderes Schulfach so kann:
Sortierverfahren animieren, Pseudocode debuggen, Blockly-Puzzle lösen — aktives Tun statt passives Lesen.

**UX-Prinzip:** 70 % Interaktion — 30 % Erklärung (siehe DOK-3 C.9).

---

## 2. Modul-Kurationsraster Klasse 5–8

Fünf Module strukturieren die Inhaltspipeline (LA-12). Jedes Modul entspricht einem Schulhalbjahr
und einem Themenblock aus dem Lehrplan RLP. Die Reihenfolge folgt dem didaktischen Spiralcurriculum:
einfache Konzepte zuerst, Wiederaufgreifen auf höherem Niveau.

---

### Modul 1 — Algorithmen & Problemlösen (Klasse 5/6)

**Lehrplan-Bereich:** Algorithmen & Programmierung (Grundstufe)
**Kernfrage:** Was ist ein Algorithmus? Wie beschreibt man Abläufe präzise?

**Inhalte:**
- Begriff Algorithmus: Eindeutigkeit, Endlichkeit, Allgemeinheit
- Darstellungsformen: Umgangssprache → Struktogramm → Ablaufdiagramm
- Grundstrukturen: Sequenz, Auswahl (wenn-dann-sonst), Wiederholung (Zählschleife, Bedingungsschleife)
- Sortierverfahren: Bubblesort, Selectionsort — Schritt für Schritt
- Suchalgorithmen: Lineare Suche, Binäre Suche (Vorbereitung)

**Player-Typen (LA-11):**
- Sortier-Player: Sortierschritte von Bubblesort in richtige Reihenfolge bringen
- Fehler-finden: Fehlerhaftes Struktogramm — welche Zeile ist falsch?
- Lückentext: Algorithmus-Beschreibung mit Lücken (Schlüsselbegriffe einsetzen)
- Quiz-Player: Begriffe + Definitionen, Eigenschaften von Algorithmen

**Startmodul (Pareto):** Modul 1 ist das erste zu kuratierende Modul.
Bubblesort als Sortier-Player ist sofort demonstrierbar und visuell überzeugend.

---

### Modul 2 — Daten & Codierung (Klasse 5/6)

**Lehrplan-Bereich:** Daten & Codierung
**Kernfrage:** Wie speichert und überträgt ein Computer Information?

**Inhalte:**
- Zahlensysteme: Dezimal → Dual (Binär) → Hexadezimal, Umrechnung
- Informationseinheiten: Bit, Byte, Kilobyte, Megabyte
- Zeichenkodierung: ASCII, UTF-8 (Grundprinzip)
- Bildkodierung: Pixel, Farbtiefe, RGB-Modell, einfache Rastergrafik
- Datenkompression: verlustfrei (RLE als Einstieg) vs. verlustbehaftet (JPEG-Prinzip)
- Grundprinzip Verschlüsselung: Caesar-Chiffre, Schlüssel-Begriff

**Player-Typen:**
- Quiz-Player: Binär ↔ Dezimal Umrechnung, Einheiten
- Sortier-Player: Codierungsschritte in richtige Reihenfolge (z.B. RLE-Kompression)
- Lückentext: Umrechnungsschema mit Lücken

---

### Modul 3 — Erste Programmierung (Klasse 6/7)

**Lehrplan-Bereich:** Algorithmen & Programmierung (Anwendung)
**Kernfrage:** Wie setzt man Algorithmen in Programmcode um?

**Inhalte:**
- Variable, Datentyp, Zuweisung
- Ein-/Ausgabe (input/print)
- Bedingte Anweisungen (if/elif/else)
- Zählschleife (for) + Bedingungsschleife (while)
- Einfache Funktionen (def, Parameter, Rückgabewert)
- Debugging: Laufzeitfehler lesen, Fehler lokalisieren

**Player-Typen:**
- **Blockly-Player (LA-23):** Hauptwerkzeug für dieses Modul
  - Puzzle-Modus: Blöcke in richtige Reihenfolge
  - Ergänzungs-Modus: Parameter/Werte in Blöcke eintragen
- Fehler-finden-Player: Fehlerhafter Pseudocode / fehlerhafter Python-Code
- Lückentext: Codezeile mit Lücken (Operatoren, Schlüsselwörter)

**Hinweis:** Modul 3 ist der Hauptanwendungsfall für LA-23 (Blockly). Erst Blockly (Kl. 6/7),
dann Text-Python (Kl. 8+, nach Launch).

---

### Modul 4 — Informatiksysteme (Klasse 7/8)

**Lehrplan-Bereich:** Informatiksysteme
**Kernfrage:** Wie ist ein Computer aufgebaut? Wie kommunizieren Geräte?

**Inhalte:**
- Hardware-Komponenten: CPU, RAM, Festplatte, Bus, Mainboard — Funktion und Zusammenspiel
- Von-Neumann-Architektur: Vereinfachtes Modell, Fetch-Decode-Execute-Zyklus
- Betriebssystem: Prozesse, Dateisystem, Benutzerverwaltung (Grundprinzipien)
- Netzwerke: Client-Server-Modell, IP-Adresse, DNS-Grundprinzip
- Internet-Protokolle: HTTP/HTTPS (Request-Response), TCP/IP vereinfacht
- WLAN, Bluetooth: Übertragungsprinzipien

**Player-Typen:**
- Zuordnungs-Player (LA-10): Hardware-Komponenten → Funktion zuordnen
- Quiz-Player: Fachbegriffe + Definitionen
- Sortier-Player: Fetch-Decode-Execute als Ablauf

---

### Modul 5 — Informatik & Gesellschaft (Klasse 8)

**Lehrplan-Bereich:** Informatik, Mensch & Gesellschaft
**Kernfrage:** Welche gesellschaftliche Rolle spielt Informatik? Was sind Chancen und Risiken?

**Inhalte:**
- Datenschutz: Personenbezogene Daten, DSGVO-Grundprinzipien (informiert/vereinfacht)
- Soziale Netzwerke: Algorithmen in Feeds, Filterblasen, Datensparsamkeit
- KI-Grundlagen: Was ist Maschinelles Lernen? Trainingsdata, Bias, Grenzen
- Algorithmen-Fairness: Wie können Algorithmen diskriminieren?
- Urheberrecht & Open Source: Creative Commons, Lizenzen vereinfacht
- Cybersicherheit: Phishing, sichere Passwörter, 2FA — praktische Hygiene

**Player-Typen:**
- Quiz-Player: Begriffe, Definitionen, Fallbeispiele
- Sortier-Player: Datenschutz-Checkliste in richtige Reihenfolge
- Lückentext: Gesetzestexte / Definitionen mit Lücken

---

## 3. OER-Quellen pro Modul

| Modul | Primärquellen | Lizenz |
|-------|--------------|--------|
| M1 Algorithmen | CS Unplugged (csunplugged.org) — "Sorting Networks", "Searching Algorithms" | CC BY 4.0 |
| M1 Algorithmen | inf-schule.de — Struktogramme, Sortierverfahren | CC BY-SA |
| M2 Daten | CS Unplugged — "Binary Numbers", "Text Compression" | CC BY 4.0 |
| M2 Daten | Lehrerfreund / Leifi (geprüfte Rechte) | fallweise |
| M3 Programmierung | Code.org — Blockly-basierte Einheiten | CC BY-NC-SA |
| M3 Programmierung | Open Roberta (Fraunhofer) — visuelle Programmierung | Apache 2.0 |
| M3 Programmierung | Python-Tutorial python.org | PSF Lizenz |
| M4 Systeme | inf-schule.de — Rechnerarchitektur, Netzwerke | CC BY-SA |
| M4 Systeme | Klexikon / Schülerlexikon (Grundbegriffe) | CC BY-SA |
| M5 Gesellschaft | Bundeszentrale für politische Bildung — Datenschutz, KI | Freie Nutzung Bildung |
| M5 Gesellschaft | Verbraucherzentrale Materialien | freie Nutzung |

**Rechtliche Absicherung:** Alle Inhalte werden inhaltlich reformuliert, nicht kopiert.
Lehrplan (RLP) ist Landesrecht und gemeinfrei. OER-Inhalte mit CC-Lizenz sind explizit für
Bildungszwecke freigegeben. Kein Material ohne geprüfte Lizenz in Produktion.

---

## 4. Didaktische Designregeln

### 70/30-Prinzip (DOK-3 C.9)
- **70 % Interaktion:** Sortieren, Lücken füllen, Fehler finden, Blockly-Puzzle
- **30 % Erklärung:** Einleitungstext, Feedback nach Aufgabe, Tooltip
- Umsetzung: Max. 1 Erklärkarte pro 3 Interaktionskarten in jedem Deck

### Bloom-Raster pro Aufgabentyp

| Player-Typ | Bloom-Stufe | Beispiel |
|-----------|-------------|---------|
| Quiz (Definition) | 1 Erinnern | "Was ist ein Algorithmus?" |
| Quiz (Anwenden) | 2–3 Verstehen/Anwenden | "Welches Sortierverfahren ist effizienter bei 10 Elementen?" |
| Lückentext | 2–3 Verstehen | Pseudocode mit Lücken |
| Sortier-Player | 3 Anwenden | Bubblesort-Schritte sortieren |
| Fehler-finden | 4 Analysieren | Fehlerhaften Pseudocode debuggen |
| Blockly-Puzzle | 3–4 Anwenden/Analysieren | Schleife zusammensetzen |

### Unmittelbares Feedback
Informatik hat einen Vorteil: "Es läuft oder es läuft nicht." Jede Aufgabe liefert sofortiges,
klares Feedback — kein Warten, keine Interpretation. Feedback-Text erklärt *warum*, nicht nur *was*.

---

## 5. Kurationsprozess (Copyright-konform)

### Rechtliche Grundlage

**Was frei ist:** Themen, Kompetenzbereiche, didaktische Ideen aus dem Lehrplan —
Ideen sind nicht urheberrechtlich geschützt.

**Was geschützt ist:** Die konkrete sprachliche Formulierung von Aufgabenstellungen,
Kompetenzformulierungen und didaktischen Beschreibungen im Lehrplan-Dokument.

**Goldene Regel:** Inhalt nutzen — Formulierung neu erfinden.
Prüffrage: "Könnte jemand den Lehrplan-Text wiedererkennen?" → Ja: umformulieren.

Konsequenz: Aufgaben in Xalento werden nie aus dem Lehrplan kopiert, sondern
auf Basis der Themen-Idee **originär formuliert** — durch KI-Assist + Redaktions-Review.

---

### KI-gestützter Kurationsprozess (LA-12 Workflow)

```
Schritt 1: Thema aus Lehrplan-Gliederung entnehmen
           (Gliederung = Idee, gemeinfrei)
           Beispiel: "Bubblesort, Klasse 6, Grundprinzip"

           ↓

Schritt 2: Claude / LLM generiert 10–15 Aufgaben-Varianten
           Prompt-Vorlage (→ siehe unten)
           Output: originäre Formulierungen in verschiedenen Player-Formaten

           ↓

Schritt 3: Redaktions-Review (15–30 min)
           - Fachliche Korrektheit prüfen
           - Schwierigkeitsgrad anpassen (Klasse 6 vs. Klasse 8)
           - 3–5 beste Aufgaben auswählen
           - Feedback-Text formulieren ("Warum ist das richtig?")

           ↓

Schritt 4: JSON-Deck befüllen
           Skript oder manuell → Deck-JSON für Xalento
```

**Aufwandsschätzung:** 5 Module × 8 Themen × 30 min = ~20 Stunden Gesamtkuration.
Das ist machbar als Parallelarbeit zur technischen Entwicklung.

---

### Prompt-Vorlage für Aufgaben-Generierung

```
Thema: [Thema, z.B. "Bubblesort — Grundprinzip"]
Zielgruppe: Gymnasium Klasse [X], Informatik Sek I
Player-Typ: [Quiz / Sortier / Lückentext / Fehler-finden]
Anzahl: 10 Aufgaben

Anforderungen:
- Eigenständige Formulierung (nicht aus Lehrplan kopiert)
- Altersgerecht, verständlich ohne Vorkenntnisse über Klasse [X] hinaus
- Konkretes Beispiel statt abstrakte Definition
- Für [Player-Typ] geeignet (z.B. Sortier: 4–6 sortierbare Elemente)
- Feedback-Text (1–2 Sätze): warum ist die Antwort richtig?
- Schwierigkeit: leicht / mittel / schwer markieren
```

**Wichtig beim Prompt:** Das Thema nennen, nicht den Lehrplan-Text einfügen.
Der LLM erzeugt originäre Inhalte — das ist copyright-sicher.

---

### Transformationsbeispiel

| Lehrplan-Idee | ❌ zu nah am Original | ✅ Xalento-Aufgabe |
|--------------|----------------------|-------------------|
| Algorithmus entwickeln | "Entwickle einen Algorithmus zur Lösung eines Problems" | "Bring die Schritte in die richtige Reihenfolge, damit die Figur das Ziel erreicht" |
| Sortierverfahren verstehen | "Beschreibe die Funktionsweise von Bubblesort" | "Was passiert in Schritt 3? Welche zwei Zahlen werden hier verglichen?" |
| Fehler im Code finden | "Analysiere einen fehlerhaften Algorithmus" | "In welcher Zeile steckt der Fehler? Wähle die richtige Korrektur." |
| Schleife anwenden | "Implementiere eine Schleife in einem Programm" | "Baue die Schleife zusammen — ziehe die richtigen Blöcke an die richtige Stelle" |

---

### Qualitätskriterien pro Aufgabe

Jede Aufgabe muss vor Aufnahme ins Deck erfüllen:

- [ ] Formulierung ist originär (kein Lehrplan-Text erkennbar)
- [ ] Fachlich korrekt (von Fachkundigen überprüft = Entwickler + ggf. Lehrkraft)
- [ ] Altersgerecht: Sprache, Abstraktionsniveau, Beispiele passen zu Klasse X
- [ ] Feedback-Text erklärt das Prinzip, nicht nur die Antwort
- [ ] Schwierigkeit ist eingestuft (leicht / mittel / schwer)
- [ ] Player-Format ist sinnvoll gewählt (kein Quiz wo Sortieren besser wäre)

---

## 6. Verlinkung zu Arbeitspaketen

| LA | Beschreibung | Modul-Bezug |
|----|-------------|-------------|
| LA-11 | Lückentext-, Sortier-, Fehler-finden-Player | M1, M2, M3, M4 |
| LA-12 | Inhaltspipeline: Kuration nach Modul-Raster | M1–M5 |
| LA-13 | Vollständiges Informatik-Deck Kl. 7–8 | M1 (Start) → M4 |
| LA-23 | Blockly-Programmierumgebung | M3 (Hauptmodul) |

Startmodul (Pareto): **Modul 1 → LA-11 Sortier-Player → Bubblesort** —
sofort demonstrierbar, visuell überzeugend, lehrplankonform, kein Backend nötig.
