# ADR — Erkenntnisse aus Wettbewerbsanalyse

*Quellen: lern-battle.de · Duolingo · Übergabe für Einarbeitung in DOK-2 und DOK-3 · April 2026*

---

## Empfehlung 1 — KI-gestützte PDF → Karteikarten-Generierung

**Zieldokument:** DOK-3 Produktvision · neuer Abschnitt C.7a

**Was fehlt:** Kein Ingestion-Pfad für Lehrkräfte/Redakteure, die eigene Dokumente als Ausgangsmaterial nutzen wollen. Learn Battle macht genau das und senkt damit die Content-Erstellungshürde erheblich.

**Formulierungsvorschlag für DOK-3 C.7a:**

> KI-gestützte Inhaltsgenerierung (Phase 2+): Redakteure und Lehrkräfte können PDFs, Lehrpläne oder Textdokumente hochladen. Die Anthropic-API extrahiert daraus Karteikarten, MC-Fragen und Lückentext-Aufgaben. Alle generierten Inhalte durchlaufen die kuratierte Redaktions-Pipeline (digitale Signatur) bevor sie in den P2P-Pool eingehen. Kein Nutzer erhält unkuratierte KI-Inhalte.

**Warum Pareto-kompatibel:** Für BioLearn könnten Lehrkräfte Lehrplankapitel als PDF einreichen, für den Chor-Coach Probennotizen — sofort Karten, kein manueller Aufwand. Technisch kein neuer Stack, Anthropic-API bereits genutzt.

---

## Empfehlung 2 — LA-15 Analytics-Tiefe: Inhalt statt Aktivität

**Zieldokument:** DOK-2 Projektplanung · LA-15 Klassen-Dashboard

**Was fehlt:** LA-15 zeigt bisher wer aktiv war. Learn Battle zeigt welche Inhalte der Klasse Probleme bereiten — das ist pädagogisch wertvoller.

**Ergänzung im Output-Abschnitt von LA-15:**

> Inhalts-Heatmap: Welche Karten sitzen in der Klasse am schlechtesten? Anzeige als Ranking der 5 schwächsten Karten mit Beherrschungsquote (z. B. „Zellkern: nur 3 von 18 Schülern sicher"). Kein Schüler-Ranking, keine öffentlichen Vergleiche.

**Aufwand:** Gering — FSRS-Daten liegen bereits in Dexie, nur neue Aggregations-Abfrage.

---

## Empfehlung 3 — Naming: «Battle» als Marketing-Begriff offen halten

**Zieldokument:** DOK-3 Produktvision · B.3 Spielmodi

**Hinweis einfügen:**

> Naming offen: Der Duell-Modus kann extern unter einem anderen Namen (z. B. „Lernbattle") vermarktet werden. Entscheidung bis LA-16 (Launch). Interner Code-Name bleibt „duell".

---


## Empfehlung 4 — Fortschritt sofort sichtbar machen beim Onboarding (Duolingo)

**Zieldokument:** DOK-3 Produktvision · neuer Abschnitt A.6 (Onboarding-Prinzip)

**Was Duolingo macht:** Nutzer kommen beim ersten Start so schnell wie möglich zur ersten Erfolgserfahrung — kein Setup, keine Registrierung, direkt spielen ("Magic Fast").

**Was bei Xalento fehlt:** Das Onboarding ist noch nicht explizit spezifiziert. Gefahr: erster Start zeigt leere Decks, FSRS-Erklärungen, Einstellungen — Nutzer springt ab bevor er den Wert erlebt hat.

**Formulierungsvorschlag für DOK-3 A.6:**

> Erster Start: Nutzer spielen sofort 3 Beispielkarten des gewählten Themas — ohne Setup, ohne Registrierung, ohne Erklärung. FSRS-Feedback erscheint nach der ersten Karte. Erst danach optional: Deck wählen, Einstellungen. Ziel: Erfolgserlebnis in unter 60 Sekunden.

**Warum wichtig:** Xalento hat keinen Streak-Zwang als Rückkehrer-Mechanismus. Das macht das erste Erlebnis umso kritischer — wer beim ersten Start keinen Wert sieht, kommt nicht wieder.

---

## Empfehlung 5 — Pause kommunizieren statt bestrafen (Duolingo-Lernfehler vermeiden)

**Zieldokument:** DOK-2 Projektplanung · LA-3 und LA-4 Gamification-Designregeln

**Was Duolingo falsch macht:** Wer seinen Streak bricht, verliert alles. Der Streak Freeze ist nur ein Pflaster auf einem selbst geschaffenen Problem.

**Xalentos struktureller Vorteil:** FSRS bestraft Pausen nicht — Karten werden neu terminiert, nicht gelöscht. Das ist bereits im System. Es fehlt nur die explizite Kommunikation davon.

**Formulierungsvorschlag als Ergänzung zur Gamification-Tabelle (DOK-2 LA-3):**

> Pausen-Kommunikation: Kehrt ein Nutzer nach einer Pause zurück, zeigt Xalento aktiv: „Du hast 2 Wochen pausiert — kein Problem. FSRS hat deine Karten nicht vergessen, nur neu geplant. Heute sind X Karten fällig." Kein Schuldgefühl, keine verlorene Arbeit.

**Aufwand:** Minimal — eine Willkommens-zurück-Nachricht auf dem Deck-Dashboard, ausgelöst wenn letzte Aktivität > 7 Tage.

---

## Bewusste Nicht-Übernahmen

| Feature | Quelle | Grund |
|---|---|---|
| Soziale Profile + Freundschaftsanfragen | Learn Battle | Widerspricht DOK-3 A.1 (Dezentralität) |
| Pflicht-Streaks + Punkte für Aktivität | Duolingo / Learn Battle | Explizit verboten in Gamification-Leitprinzipien |
| Ligen und globale Ranglisten | Duolingo | Erzeugt leeres Grinding, kein Lernwert |
| Herzen/Leben-System (Fehler bestrafen) | Duolingo | Erzeugt Druck statt Neugier, gegen DOK-2 Designregeln |
| Community-Features / Lioverse-Welt | Learn Battle | Kein Pareto-Verhältnis, massive Komplexität |
| App-Store als Primärkanal | Duolingo / Learn Battle | Widerspricht DOK-3 A.5 (Verbreitungsstrategie) |

---

## Strategische Einordnung

Duolingo löst das Problem: *Wie bringe ich jemanden dazu, heute zu lernen, obwohl er es nicht muss?* — und löst es mit Verlustaversion und Habit-Engineering.

Xalentos Zielgruppen haben dieses Problem nicht in derselben Form. Choristas üben weil der Auftritt kommt. Schulkinder lernen weil die Klassenarbeit kommt. Der externe Druck existiert bereits. Xalento muss ihn nicht ersetzen — sondern das angenehmste, ehrlichste Werkzeug für diesen Druck sein.

Das ist der strategische Unterschied: **Duolingo schafft künstliche Dringlichkeit. Xalento zeigt echten Fortschritt.**

---

## Strategische Entscheidungen (April 2026)

### StimmBild — Pause bis externe Unterstützung gesichert

StimmBild bleibt auf dem aktuellen Stand. Gründe:

- Zeitdruck Berlin-Wahl September 2026 zu hoch für Solo-Entwicklung
- Auflagen für politische Apps (Neutralität, Quellentransparenz, rechtliche Absicherung) ohne externe Unterstützung nicht erfüllbar
- Halbfertiger Launch wäre schlimmer als kein Launch

StimmBild ist nicht aufgegeben — nur entkoppelt vom Berliner Wahltermin. Wiederaufnahme sinnvoll wenn: Uni-Kooperation steht, externe Redakteure verfügbar, mehr Entwicklungskapazität.

### Neue Prioritätsreihenfolge

1. Xalento Fundament (LA-1–LA-3) — läuft
2. Chorübung (LA-6–LA-8) — erster echter Anwendungsfall
3. BioLearn RLP (LA-9–LA-13 + LA-15) — erste öffentliche Priorität, erster Schulmarkt-Auftritt
4. Kooperation Universität Koblenz (Informatik-Didaktik + Institut für Pädagogik) — nach LA-15, mit laufender App und echten Nutzungsdaten
5. StimmBild — Wiederaufnahme mit akademischer Rückendeckung, ohne Wahltermin-Druck

### Uni Koblenz — Kooperationsidee (mittelfristig)

Zieltermin: nach Fertigstellung LA-13 + LA-15, voraussichtlich 2027.

Was bis dahin vorzubereiten ist:
- Laufende BioLearn-App mit echten Schülerinhalten, lehrplankonform RLP Klasse 5–6
- Klassen-Dashboard (LA-15) mit Inhalts-Heatmap — das ist der Differenziator gegenüber Quizlet & Co.
- FSRS-Nutzungsdaten aus SingOn-Chor als erster Beleg für Lernwirksamkeit

Ansprechpartner: Fachbereich Informatik (Professur Informatik und ihre Didaktik) + Institut für Pädagogik (Prof. Dr. Pätzold, Prof. Dr. Hoffmann).
