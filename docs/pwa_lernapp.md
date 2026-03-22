Projektskizze: Generische Medien-Lern-App (PWA)
**Status:** Entwurf / Designphase  
**Version:** 2.1  
**Datum:** März 2026  
**Arbeitstitel:** noch offen  

## 1. Vision & Generalisierung

Die App ist eine
inhaltsneutrale Medien-Lern-App
– nicht auf einen bestimmten Lernbereich beschränkt, sondern für jeden
strukturierten Lerninhalt nutzbar der aus Mediendateien besteht.
Das Grundprinzip ist immer gleich:
Ein
Inhaltsersteller
bereitet Mediendateien vor und legt sie strukturiert in einer Cloud-Ordnerstruktur ab
Der
Lernende
navigiert mit der App durch diese Struktur und spielt die Inhalte gezielt ab

### Anwendungsbeispiele

| Anwendungsfall | Typische Inhalte |
|---|---|
| Chorübung | MusicXML, MP3 (Stimmen getrennt), Rhythmustext |
| Jagdscheinprüfung | PDF, kurze Videos, Audio (Wildrufe) |
| Führerschein-Theorie | JSON-Fragenkatalog (amtlicher BMDV-Datensatz) |
| Sprachenlernen | JSON-Fragen, Audio, PDF |
| Nachhilfe Mathematik | Erklär-Videos, PDF-Aufgabenblätter, Audio-Erklärungen |
| Instrumentalübung | MusicXML, MP3, Video |

Die App selbst muss von den Inhalten nichts wissen – sie spielt ab was in der Cloud liegt.

### Entwicklungsphasen

Phase 1:
Nur für den Entwickler (Mike) – erster Anwendungsfall: Chorübung
Phase 2:
Für alle Nutzer weltweit – jeder bringt eigenen Cloud-Account mit
Phase 3 (Ausblick):
Einfache Vorbereitungsoberfläche für Inhaltsersteller

## 2. Layout & Bedienung


### Grundprinzip

Smartphone: immer
Hochformat
Bildschirm aufgeteilt in zwei Bereiche:
Obere 60%:
Inhaltsdarstellung
Untere 40%:
Steuerung (Einhandbedienung mit dem Daumen)
Steuerung umschaltbar für
Rechts- oder Linkshänder
Tablet und PC werden ebenfalls unterstützt (Responsive Design, Maus+Tastatur)
Gerät
Bedienung
Layout
Smartphone
Touch, Einhand, Hochformat
60/40 wie beschrieben
Tablet
Touch + optional Tastatur
Größeres Grid, größerer Inhaltsbereich
PC/Desktop
Maus + Tastatur
Klassisches UI, Seitenleiste für Navigation
Zwei Modi
Die App wechselt zwischen zwei Zuständen:
Modus
Oben 60%
Unten 40%
Explorer
Icon-Grid (Ordnerstruktur)
Navigationspfeile + Auswahltaste
Player
Inhaltsdarstellung
Player-Steuerung
Wechsel Explorer → Player: durch Auswahl einer Datei
Wechsel Player → Explorer: durch „Zurück"-Funktion in der Player-Steuerung
Bei Rückkehr landet man an der
zuletzt fokussierten Position
im Explorer.

## 3. Explorer-Modus

Icon-Grid (obere 60%)
Icons in einem Grid, z.B. 3×4, 4×4 – je nach verfügbarem Platz
Fokussiertes Element zeigt seinen
Namen
ein, alle anderen nur das Icon
Erstes Element oben links
= immer „
..
" (Ordner-hoch-Symbol) für Navigation zum übergeordneten Ordner
Auswahl eines Ordners → Navigation hinein
Auswahl einer Datei → Wechsel in Player-Modus
Steuerung (untere 40%)
Navigationspfeile: links / rechts / hoch / runter
Mittlerer Button: Auswahl / Enter
Anordnung kreisförmig wie beim Amazon Fire Stick
Einhandbedienung mit dem Daumen, umschaltbar für Links-/Rechtshänder

## 4. Player-Modus

Inhaltsdarstellung (obere 60%)
Abhängig vom Dateityp:
MP3:
Audio-Visualisierung (Details noch offen)
Video:
Videoplayer
PDF:
PDF-Anzeige
Bild:
Bildanzeige
MusicXML:
Gerenderte Notenansicht (Score), synchron zur Wiedergabe mitlaufend
Kontextsensitives Layout
Während
die Übung läuft ist das Layout 60/40. Sobald der Nutzer eingreift
(Steuerung, Konfiguration) wird die Übung unterbrochen und
nahezu 100% des Bildschirms
stehen für die Steuerung zur Verfügung – der Inhalt wird ausgeblendet oder stark reduziert.
Ausnahme:
Kontextabhängig bleibt ein Teil des Inhalts sichtbar, z.B.:
Beim A-B-Loop setzen: Fortschrittsbalken oder Score muss sichtbar sein um Punkte A und B zu platzieren
Beim Zeitsprung konfigurieren: Fortschrittsbalken hilfreich
Player-Steuerung (untere 40% im Normalbetrieb)
Grundsteuerung:
Play / Pause
Abspielgeschwindigkeit erhöhen / verringern
Navigation:
Sprung vorwärts / rückwärts um einen
frei definierbaren Zeitabschnitt
Sprung an den Anfang / ans Ende
Nächstes / vorheriges Objekt in der Sequenz
Wiederholung:
Aktuellen Abschnitt einmal wiederholen
Aktuellen Abschnitt endlos loopen
Gesamte Sequenz wiederholen
A-B-Loop:
Punkt A setzen, Punkt B setzen → Bereich einmal oder endlos wiederholen

## 5. Unterstützte Medientypen

Die App ist inhaltsneutral – grundsätzlich können alle gängigen Medientypen abgespielt werden:
Audio:
MP3 (auch mehrspurig / Mehrkanal)
Video:
gängige Videoformate
Dokumente:
PDF
Bilder:
gängige Bildformate
Noten:
MusicXML (gerendert via OSMD oder ähnliche Library)
Welche Typen konkret in Phase 1 implementiert werden, wird beim Prototyp entschieden.

## 6. Chorübung – Spezifische Erweiterungen

(Erster konkreter Anwendungsfall, Phase 1)
Übungsobjekte
Audio – Mehrkanal:
Kanal A: Eigene Stimme (hervorgehoben)
Kanal B: Begleitstimmen (im Hintergrund)
Dynamischer Lautstärkeregler zwischen A und B (Crossfader-Prinzip)
Rhythmustext:
Text im Rhythmus dargestellt, inklusive Pausen
Unabhängig von der Melodie – zum Erlernen von Textrhythmus
Visuell mitlaufend während der Wiedergabe
Wird synthetisch aus MusicXML erzeugt und vorproduziert bereitgestellt
Score (Notenansicht):
Vollständige Notenansicht aller Stimmen (aus MusicXML gerendert)
Optional: isolierte Ansicht nur der eigenen Stimme
Aktuelle Position wird mitlaufend markiert
Vorverarbeitung (lokal am PC zu Hause)
Die Aufbereitung der Stücke erfolgt
vor dem Upload
, nicht im Player:
MusicXML-Quelldatei liegt vor
Python-Script extrahiert eine bestimmte Stimme (z.B. Bass 2, Sopran, Alt)
Script teilt das Stück in sinnvolle Übungsabschnitte (nach Phrasen, Fermaten, Wiederholungszeichen)
Ergebnis: mehrere kleine MusicXML-Dateien pro Stimme
Zusätzlich: Rhythmustext-Datei wird synthetisch erzeugt
Upload aller aufbereiteten Dateien in die Cloud
Das Vorverarbeitungs-Script könnte später mit einer einfachen GUI ausgestattet werden.
Rendering-Strategie
Designentscheidung:
MusicXML wird direkt auf dem Smartphone gerendert (z.B. via OSMD).
Kein Server-Rendering, keine Vorab-Konvertierung zu Video
Bei Performance-Problemen: optionale eingebaute Performance-Messung als Diagnosewerkzeug
Video-Fallback bleibt als spätere Option im Hinterkopf, wird in Phase 1 nicht implementiert

## 7. Cloud-Anbindung

Dateien liegen in der Cloud, App navigiert durch die Ordnerstruktur
Cloud-Dienst noch nicht festgelegt
Präferenz:
europäischer, kostenfreier Dienst
, DSGVO-konform
Kandidaten:
Nextcloud
(selbst gehostet oder über europäischen Anbieter),
Infomaniak kDrive
(Schweiz)
Die Cloud-Abstraktion soll austauschbar sein – kein Lock-in auf einen bestimmten Dienst

## 8. Zwei Zugangswege: Freier Modus und Geführter Modus

Grundidee
Neben den in Ordnerstrukturen gegliederten Lerninhalten existiert parallel eine
didaktische Struktur
– eine separate Ebene die dem Lernenden vorschlägt was als nächstes
sinnvoll zu lernen ist. Die beiden Ebenen sind unabhängig voneinander
aber aufeinander abgestimmt:
Ebene 1: Inhalte
(was existiert)
Ordnerstruktur in der Cloud mit Mediendateien
Zugang über den Explorer (freie Navigation)
Ebene 2: Didaktik
(wie gelernt wird)
Separate Struktur die Lernschritte in didaktisch sinnvoller Reihenfolge vorschlägt
Kennt den Lernfortschritt des Nutzers
Basiert auf den lernwissenschaftlichen Prinzipien (Kapitel 9)
Zwei Zugangswege
Freier Modus
Der Nutzer navigiert selbst durch den Explorer und wählt aus was er üben möchte. Volle Kontrolle, kein vorgegebener Pfad.
Geführter Modus
Die App schlägt den jeweils nächsten sinnvollen Lernschritt vor – z.B.
„heute: Abschnitt 3 von Stück X wiederholen, dann Abschnitt 1 von Stück Y
neu lernen". Der Nutzer folgt einem didaktisch durchdachten Pfad ohne
selbst planen zu müssen.
Didaktische Struktur als Datei
Die didaktische Struktur wird – analog zu den Inhalten –
zu Hause am PC vorbereitet
und ebenfalls in der Cloud abgelegt. Sie referenziert die vorhandenen Inhaltsdateien und definiert:
Welche Inhalte in welcher Reihenfolge gelernt werden sollen
Welche Wiederholungsabstände empfohlen werden (Spaced Repetition)
Welche Aufgabentypen gemischt werden sollen (Interleaving)
Welche Abhängigkeiten zwischen Lernschritten bestehen (erst A verstehen, dann B)
Lernfortschritt
Der
Geführte Modus erfordert dass die App sich merkt was der Nutzer bereits
gelernt hat und wie gut. Dieser Fortschritt wird lokal auf dem Gerät
oder in der Cloud gespeichert und fließt in den nächsten Vorschlag ein.
Einordnung
Damit wird die App im Kern zu einem
schlanken mobilen Lernmanagementsystem
– vollständig auf eigenen Inhalten basierend, ohne externe
Plattformabhängigkeit. Die Trennung von Inhalten und didaktischer
Struktur hält das System flexibel: dieselben Inhalte können mit
unterschiedlichen didaktischen Strukturen kombiniert werden.
Noch offen:
Dateiformat und konkrete Struktur der didaktischen Datei, Integration des Lernfortschritts, UI für den Geführten Modus.

## 9. Lernwissenschaftlicher Grundsatz

Die
App soll langfristig auf der empirisch am besten gestützten
Lernstrategie basieren. Als Leitprinzip gilt die folgende
minimalistische evidenzbasierte Lernroutine:
Stoff durcharbeiten
– Verstehen sichern (Inhalte konsumieren: Audio, Video, PDF, Score)
Sofort erste Abrufübung ohne Unterlagen
– aktives Erinnern direkt nach dem Lernen (nicht nochmals nachschauen)
Verteilte Wiederholungen in wachsendem Abstand
– Spaced Repetition: heute, morgen, in einer Woche, in einem Monat
Unterschiedliche Aufgabentypen mischen
– Interleaving: nicht dasselbe Schema endlos wiederholen
Fehler analysieren und gezielt schließen
– Schwachstellen identifizieren und gezielt üben, nicht das Bekannte wiederholen
Was
diese Prinzipien konkret für den jeweiligen Lerninhalt bedeuten
(Chorübung, Jagdschein, Mathematik, ...) ist noch offen und wird separat
erarbeitet.
Bezug zu den aktuellen Defiziten (Kapitel 9):
Die Punkte „Kein Feedback", „Kein Lernfortschritt" und „Keine Notizen"
sind direkte Konsequenzen daraus, dass Punkte 2–5 dieser Lernroutine in
der App noch nicht abgebildet sind. Der aktuelle Funktionsumfang deckt
primär Punkt 1 ab.

## 10. Kritische Analyse – Defizite des aktuellen Konzepts

Das
aktuelle Konzept funktioniert gut für Lerninhalte die aus fertigen
Mediendateien bestehen. Für eine wirklich generische Lern-App fehlen
jedoch folgende Aspekte – noch nicht entschieden ob und wie diese
umgesetzt werden, aber bewusst festgehalten:

## 1. Nur Konsum, kein Feedback

Der Lernende spielt ab und wiederholt – die App weiß jedoch nie ob er
etwas verstanden hat. Für viele Anwendungsfälle (Jagdschein, Mathe,
Fremdsprachen) wäre ein einfaches Quiz nach einem Lernabschnitt sehr
wertvoll. Beispiel: „Welches Tier war das?" nach einem Wildlaut. Dieser
Aspekt fehlt im aktuellen Konzept vollständig.

## 2. Kein Lernfortschritt

Es gibt keine Möglichkeit zu markieren „das kann ich schon" oder „das
muss ich noch üben". Keine Häkchen, keine Statistiken, kein
Fortschrittsindikator. Nach einer Pause weiß der Nutzer nicht wo er
aufgehört hat und was bereits gut beherrscht wird.

## 3. Keine Notizen oder Markierungen

Der Lernende kann nichts annotieren – kein „hier war ich unsicher",
keine Lesezeichen im PDF, keine persönliche Notiz zu einem Stück oder
Thema. Alles Gelernte bleibt flüchtig.

## 4. Inhalte sind statisch

Alle Inhalte müssen vorher vom Inhaltsersteller vorbereitet werden. Es
gibt keinen Mechanismus für den Lernenden selbst etwas hinzuzufügen –
z.B. eine eigene Gesangsaufnahme zum Vergleich mit dem Original, oder
eigene Ergänzungen zu einem Lernthema.

## 5. Keine Suchfunktion

Bei wachsender Inhaltssammlung (viele Chorstücke, viele
Jagdschein-Themen) wird die Navigation durch Ordner mühsam. Eine
Volltextsuche oder Filterung nach Tags fehlt im aktuellen Konzept.

## 6. Kein kollaboratives Element

Für Nachhilfe wäre es wertvoll wenn der Lehrer sehen könnte was der
Schüler geübt hat und wie oft. Für den Chor wäre es interessant wenn der
Chorleiter Inhalte direkt für einzelne Stimmen freigeben könnte. Beides
ist bisher nicht vorgesehen.
Bewertung für Phase 1:
Für den persönlichen Gebrauch (Chorübung) sind diese Defizite zunächst
kein Problem. Für eine wirklich universelle Lern-App wären
Lernfortschritt
und
Quiz/Feedback
die wichtigsten fehlenden Bausteine – und decken sich direkt mit den lernwissenschaftlichen Grundsätzen aus Kapitel 9.

## 11. Technologie-Entscheidungen

Frontend: React + TypeScript
Entscheidung:
Das Frontend wird mit React und TypeScript gebaut.
Begründung:
Größtes Ökosystem für PWAs – alle benötigten Libraries existieren bereits (OSMD für MusicXML, Audio-Libraries, PDF-Viewer)
TypeScript gibt Typsicherheit für ein wachsendes Projekt
Läuft auf Smartphone, Tablet und PC gleichermaßen gut
Bei späterer App-Store-Verteilung kann React Native viel Code wiederverwenden
PWA statt native App
Entscheidung:
Die App wird als Progressive Web App realisiert – keine native App, kein App-Store-Prozess.
Bekannte
erfolgreiche PWAs als Referenz: Twitter/X, Pinterest, Starbucks
(inklusive Offline-Bestellung), Spotify (open.spotify.com), Uber (für
Märkte mit schwacher Verbindung), Trivago.
Vorteile für dieses Projekt:
Kein App-Store-Prozess, keine Abhängigkeit von Apple oder Google
Updates sofort beim nächsten Aufruf verfügbar
Trotzdem auf dem Homescreen installierbar
Offline-Fähigkeit über PWA-Cache-Strategie möglich
Hinweis:
iOS/Safari unterstützt PWA-Features etwas eingeschränkter als
Android/Chrome – für Audio und Video ist die Unterstützung jedoch
ausreichend.
Backend
Entscheidung (vorläufig):
Kein eigenes Backend in Phase 1. Das Frontend kommuniziert direkt mit
der Cloud-API (Nextcloud/WebDAV). Das hält Phase 1 schlank und
wartungsarm.
Architekturdiagramm
Bild anzeigen
MusicXML-Rendering
Entscheidung:
OSMD (OpenSheetMusicDisplay) als Library für das Rendering von MusicXML
direkt im Browser. Performance wird beim Prototyp gemessen;
Video-Fallback bleibt als spätere Option.

## 12. Gamification – Motivation und Nutzerbindung

Gamification-
Elemente die sich wissenschaftlich als effektiv für prüfungsorientiertes
Lernen erwiesen haben und gleichzeitig den kommerziellen Erfolg einer
App steigern. Die Elemente ergänzen die lernwissenschaftlichen
Grundsätze aus Kapitel 9 und schließen teilweise die Defizite aus
Kapitel 10.

## 1. Fortschrittsbalken / Levelsystem

Visualisiert
den Lernfortschritt. Motivation durch sichtbare Erfolge. Studien
zeigen: Nutzer bleiben länger aktiv wenn Fortschritt sichtbar ist.
Beispiel: Führerschein-App zeigt wie viele Fragen pro Thema erledigt
sind.
Verbindung:
Schließt Defizit „Kein Lernfortschritt" (Kapitel 10) direkt.
Phase:
1 (einfach umsetzbar, hoher Nutzen auch für Einzelnutzer)

## 2. Punkte und Abzeichen (Badges)

Belohnung
für das Erreichen von Lernzielen. Verstärkt intrinsische Motivation
durch kleine, sofortige Erfolgserlebnisse. Nutzer kehren häufiger zurück
um „alle Abzeichen" zu sammeln.
Verbindung:
Unterstützt Grundsatz 3 (verteilte Wiederholungen) aus Kapitel 9.
Phase:
1 für persönliche Abzeichen, Phase 2 für soziale Vergleiche

## 3. Quiz-Challenges und Mini-Tests

Kurze,
wiederholbare Aufgaben („Micro-Learning"). Sofortiges Feedback fördert
Abrufübungen die die Langzeitspeicherung verbessern. Beispiel: Tägliche
Jagdschein-Quizfrage → tägliche App-Öffnung.
Verbindung:
Setzt Grundsätze 2 und 5 (Abrufübung,
Fehler analysieren) aus Kapitel 9 direkt um. Schließt Defizit „Kein
Feedback" (Kapitel 10).
Phase:
1 (Kernfunktion für prüfungsorientiertes Lernen)

## 4. Ranglisten / Leaderboards

Wettbewerbsanreiz
gegen andere Nutzer. Steigert Engagement besonders bei jüngeren
Zielgruppen. Bewirkt höhere Nutzungsfrequenz und längere App-Sitzungen.
Verbindung:
Schließt Defizit „Kein kollaboratives Element" (Kapitel 10) teilweise.
Phase:
2 (erfordert mehrere Nutzer)

## 5. Missionen / Tagesaufgaben

Nutzer
erhalten kleine, überschaubare Lernziele. Psychologisch: Commitment
durch „kleine Schritte" → kontinuierliches Lernen. Beispiel: „Beantworte
heute 10 Fragen im Modul Fischkunde".
Verbindung:
Unterstützt den Geführten Modus (Kapitel 8) und Grundsatz 4 (Aufgabentypen mischen) aus Kapitel 9.
Phase:
1 (passt direkt in den Geführten Modus)

## 6. Sofortiges Feedback

Korrekte/
falsche Antworten direkt visualisieren. Fördert Fehlerkorrektur und
gezielte Wiederholung. Erhöht die Wirksamkeit von Spaced Repetition.
Verbindung:
Setzt Grundsätze 2 und 5 aus Kapitel 9 um. Schließt Defizit „Kein Feedback" (Kapitel 10).
Phase:
1 (Voraussetzung für effektives Lernen)

## 7. Storytelling / Kontextuelle Szenarien

Lernstoff
wird in eine narrative Struktur eingebettet. Beispiel: Jagdschein-App
als „Jagdabenteuer", Führerschein-App als „Fahrschule-Simulation".
Steigert Motivation und Behaltensleistung.
Verbindung:
Wird durch die Ordnerstruktur und
didaktische Struktur (Kapitel 8) vorbereitet – der Inhaltsersteller kann
narrative Pfade anlegen.
Phase:
2–3 (erfordert aufwändigere Inhaltsvorbereitung)

## 8. Belohnung von Konsistenz (Streaks)

Tägliche Login-Belohnungen, Streaks. Erhöht langfristige Nutzung und damit Kaufbereitschaft für Vollversionen oder Abonnements.
Verbindung:
Unterstützt Grundsatz 3 (verteilte Wiederholungen) aus Kapitel 9 durch externe Motivation.
Phase:
1–2 (technisch einfach, hoher Effekt auf Nutzerbindung)

### Zusammenfassung

Effektive
Gamification kombiniert sichtbare Fortschritte, kleine Belohnungen,
wiederholbares Feedback und Wettbewerbsanreize. Besonders erfolgreich
bei Apps mit klar definierten Lernzielen (Führerschein, Jagdschein,
Angelschein, AEVO, Chorübung). Ergebnis: höhere Nutzerbindung, bessere
Lernerfolge, stabiler Umsatz.
Für Phase 1 priorisiert:
Elemente 1, 3, 5, 6 und 8 – da sie auch für einen Einzelnutzer sofort Mehrwert bringen.
Für Phase 2:
Elemente 2, 4 und 7 – da sie von mehreren Nutzern oder mehr Aufwand abhängen.

## 13. Spaced Repetition Engine

Das
technische Herzstück des Geführten Modus (Kapitel 8). Die Engine
entscheidet welches Lern-Item als nächstes wiederholt werden soll –
adaptiv, fehlergewichtet und domain-neutral.
Grundprinzipien
Item-Level Tracking
– jedes Lern-Item hat einen eigenen Wiederholungsstatus
Fehlerbasierte Gewichtung
– falsch beantwortete Items werden öfter wiederholt
Vergessensmodell
– nächste Wiederholung wird berechnet wenn die Vergessenswahrscheinlichkeit steigt
Adaptive Abstände
– erfolgreiche Wiederholungen erhöhen den Abstand exponentiell
Maximale Intervallbegrenzung
– verhindert dass Items zu selten wiederholt werden
Datenmodell pro Item (UserItemState)
UserItemState {
user_id
item_id
stability_score       // 0–1, wie gut das Item gelernt ist
last_review_date
next_review_date
consecutive_correct   // Anzahl richtiger Antworten hintereinander
difficulty            // 0–1, item-spezifisch
}
Berechnung der Wiederholungsintervalle (SM2-Algorithmus)
Basierend auf dem bewährten SuperMemo SM2-Algorithmus (auch Grundlage von Anki):
Erste Wiederholung:   interval = 1 Tag
Zweite Wiederholung:  interval = 3 Tage
Danach:               interval = previous_interval * factor
factor = 2.5 - 0.5 * difficulty
Bei Fehler  → factor zurücksetzen, minimal 1.5
Bei Erfolg  → factor erhöhen, maximal 5.0
Fehlergewichtung
Richtig: stability_score += (1 - stability_score) * 0.2
Falsch:  stability_score *= 0.5
next_review_date = today + (base_interval * stability_score)
Items mit niedriger Stability werden häufiger wiederholt.
Session-Logik (Engine Logic)
Filterlogik für die nächste Session:
Items deren
next_review_date <= today
Sortierung: niedrigste Stability zuerst, gewichtet nach Schwierigkeit
Session-Limit definieren (z.B. 20 Fragen)
Optional: Zufallseinblendung kritischer Items aus der gesamten Kategorie
Max. 30% bereits stabile Items → verhindert Langeweile
Session Flow
while session_time_remaining and items_remaining:
item = select_next_item()
show_item(item)
response = get_user_answer()
correctness = evaluate(response)
update UserItemState  // stability, interval, next_review_date
Erweiterungsmöglichkeiten
Leistungsprofil
– Nutzer erhält Prognose der Bestehenswahrscheinlichkeit
Kategorienpriorisierung
– z.B. „Schwache Themen zuerst"
Aufgabenvarianten
– Multiple Choice, offene Fragen, Bildfragen
KI-Integration
– Item-Schwierigkeit adaptiv anpassen
Sonderfall: Chorübung
Die
Engine setzt voraus dass Lerninhalte als abfragbare Items mit klarer
Bewertung vorliegen. Für die Chorübung gibt es zwei komplementäre
Bewertungsansätze die beide implementiert werden:
Ansatz 1: Selbsteinschätzung (Phase 1)
Nach jedem Übungsabschnitt bewertet der Sänger sich selbst – analog zu Anki. Beispiel mit vier Stufen:
„Nochmal" → stability_score stark reduzieren
„Fast" → stability_score leicht reduzieren
„Gut" → stability_score erhöhen
„Perfekt" → stability_score stark erhöhen
Die
Engine behandelt diese Selbsteinschätzung wie eine
richtig/falsch-Antwort und berechnet den nächsten Wiederholungstermin
entsprechend.
Ansatz 2: Automatische Messung via Mikrofon (Phase 2)
Das Smartphone-Mikrofon nimmt die Stimme auf und analysiert zwei Dimensionen:
Tonhöhe (Pitch Detection):
Library: pitchy oder aubio im Browser
Toleranz: ±50 Cent = akzeptabel, ±25 Cent = gut (100 Cent = 1 Halbton)
Vergleich der gesungenen Frequenz mit Sollfrequenz aus MusicXML
Technische Anforderung: Metronom läuft
nur über Kopfhörer
damit das Mikrofon nur die Stimme aufnimmt
Rhythmus (Onset Detection):
Misst wann ein Ton beginnt und wie lange er gehalten wird
Vergleich mit Soll-Einsatz und Soll-Dauer aus MusicXML
Metronom über Kopfhörer als gemeinsame Zeitreferenz zwingend erforderlich
Zwei separate Übungsmodi für saubere Messung:
Modus
Gesungener Text
Messung
Didaktisches Ziel
Tonhöhenmodus
Vokalise (Nanana / Aaaa)
Pitch-Detection zuverlässig, da Vokale stabile Frequenzen erzeugen
Erst Töne treffen
Textrhythmusmodus
Echter Liedtext + Metronom
Rhythmus im Vordergrund, Tonhöhe optional
Text und Rhythmus kombinieren
Konsonanten
(P, T, K, S) erzeugen Signalunterbrechungen und stören die
Pitch-Detection – daher die Trennung in zwei Modi. Didaktisch sinnvolle
Reihenfolge: erst Tonhöhenmodus, dann Textrhythmusmodus, dann
kombiniert.

## 14. Dreiphasiger Übungszyklus (Chorübung)

Der Standard-Lernablauf für die Chorübung besteht aus drei Phasen die der Sänger frei kombinieren und konfigurieren kann.
Phase A: Zuhören
Die
Sequenz wird abgespielt – der Sänger hört zu und sieht Score und Text
mitlaufend. Beliebig oft wiederholbar. Keine Aktion außer Zuhören und
Internalisieren.
Phase B: Kontext-Einstieg + Singen/Sprechen
Kontext-Einstieg (tutti):
Vor dem eigenen Einsatz spielt die App automatisch die letzten N Takte
als vollständigen Chorklang (alle Stimmen, tutti). N ist einstellbar: 1,
2, 3 oder 4 Takte. Das entspricht exakt der realen Chorprobe wo der
Dirigent einen Anlauf gibt. Der Kontext-Einstieg gibt automatisch Tempo,
Tonart und Einsatz – kein separates Metronom oder Einstimmton nötig.
Dann nahtloser Übergang in die Aufnahmephase: der Sänger singt oder spricht ins Mikrofon.
Tempovariabilität:
Das Tempo ist stufenlos einstellbar – z.B. 50% bis 150% des
Originaltempos. Da MusicXML keine Audiodatei ist sondern live gerendert
wird, entstehen dabei keinerlei Klangverzerrungen (kein
„Chipmunk"-Effekt wie bei MP3-Streckung). Ideal zum schrittweisen
Herantasten an schwierige Passagen.
Visuelle Unterstützung während des Singens (frei wählbar):
Sichtbarkeit
Beschreibung
Alles
Score + Text mitlaufend
Nur Noten
Score ohne Text
Nur Text
Text ohne Noten
Nichts
Reine Abrufübung – maximaler Lerneffekt
Übungsfokus (frei wählbar):
Fokus
Ziel
Gesungener Text
Gemessen wird
Tonhöhenmodus
Richtige Töne in richtiger Reihenfolge
Vokalise (Nanana/Aaaa)
Pitch, Tempo egal
Rhythmusmodus
Richtiges Tempo und Einsätze
Echter Liedtext
Onset/Dauer, Tonhöhe egal
Sichtbarkeit und Fokus sind frei kombinierbar – insgesamt 8 mögliche Kombinationen. Der Sänger wählt was er gerade üben will.
Phase C: Bewertung
Nach dem Singen erfolgt die Bewertung in zwei Schichten:
Automatisch (Phase 2):
Tonhöhe: Abweichung in Cent von der Sollfrequenz (MusicXML)
Rhythmus: Abweichung der Einsätze und Tondauern vom Soll-Timing
Metronom läuft dabei ausschließlich über Kopfhörer – Mikrofon nimmt nur die Stimme auf
Selbsteinschätzung (Phase 1 + ergänzend in Phase 2):
„Nochmal" / „Fast" / „Gut" / „Perfekt"
Fließt direkt in die Spaced Repetition Engine (Kapitel 14)
Das Ergebnis beider Schichten bestimmt den nächsten Wiederholungstermin für diesen Übungsabschnitt.

## 15. Implementierungsreihenfolge

Reihenfolge
Explorer
– Navigation durch Cloud-Ordnerstruktur, Dateien öffnen
Player Basis
– MusicXML anzeigen, MP3 abspielen, Grundsteuerung (Play/Pause, Sprung, Tempo)
Übungszyklus
– Zuhören, Singen, Selbsteinschätzung (Phase A/B/C ohne Mikrofon)
Spaced Repetition Engine
– Lernrhythmus basierend auf Bewertungen
Automatische Messung
– Mikrofon, Pitch- und Rhythmusanalyse
Nach Schritt 2 ist die App bereits benutzbar. Nach Schritt 3 vollständiges Übungswerkzeug. Schritt 4 macht sie intelligent.
Player – Standard-Libraries
Library
Zweck
OSMD
MusicXML-Rendering
Tone.js
Audio-Wiedergabe, Tempo-Kontrolle, MusicXML-Synthese
PDF.js
PDF-Anzeige
WaveSurfer.js
MP3-Visualisierung
Explorer – Eigenbau
Alle
Standard-Explorer-Komponenten sind auf Desktop/Maus ausgelegt. Die
Anforderungen weichen zu fundamental ab (Einhand-Daumensteuerung,
Fire-Stick-Fokus, Links-/Rechtshänder, kontextsensitives Layout,
WebDAV-Anbindung) – Eigenbau ist effizienter als Anpassung einer
vorhandenen Library.

## 16. Offene Punkte (noch zu besprechen)

~~Entscheidung zu den Defiziten aus Kapitel 10~~ ✓ → Kapitel 10a
~~Player-Bedienelemente im Detail~~ ✓ → Kapitel 16a
~~Technische Architektur~~ ✓ → Kapitel 16b
~~Offline-Fähigkeit~~ ✓ → Kapitel 16c

Noch offen (Fortsetzung folgt):
- MP3-Visualisierung im Player
- Cloud-Dienst final entscheiden
- Ordnerstruktur-Konvention in der Cloud
- Authentifizierung für Phase 2
- Dateiformat und Struktur der didaktischen Datei (Kapitel 8)
- UI-Konzept für den Geführten Modus (Kapitel 8)
- Speicherung des Lernfortschritts (lokal oder Cloud)

Dokument wird laufend ergänzt im Zuge der Projektdiskussion.

---

## 18. Markt und Schutzstrategie

### Reihenfolge: PWA zuerst, App-Store wenn validiert

Der Prototyp läuft als PWA oder HTML-Datei — kein Install, kein App-Store-Prozess. Sobald das Konzept validiert ist und funktioniert, dann der Schritt in den App-Store via React Native oder Flutter (viel Code kann wiederverwendet werden).

### Drei Schutzebenen

**Technisch:** Kompilierter nativer App-Code ist nicht direkt lesbar — deutlich höhere Hürde als eine HTML-Datei.

**Rechtlich:** App-Store-Einträge mit Datum belegen die Erstveröffentlichung. Markenname, ggf. einfaches Gebrauchsmuster für die Spielmechanik.

**Wirtschaftlich:** Netzwerkeffekte, Datenqualität, Community und Reputation sind nicht kopierbar — wer zuerst eine aktive Nutzerbasis hat, gewinnt.

### Freemium-Modell

- **Basis kostenlos:** Kernfunktionen, eine Sprache / ein Themengebiet
- **Premium:** Weitere Sprachen/Themen, unbegrenzte Duelle, erweiterte Statistiken
- **Zielgruppen:** Fahrschüler (klarer Termin, Zahlungsbereitschaft), Sprachlernende, Chorsänger, Jagdschein-Anwärter

---

## 10a. Entscheidungen zu den Defiziten aus Kapitel 10

### Defizit 1: Nur Konsum, kein Feedback
**Entscheidung: Für Phase 1 geschlossen.**
Die Selbsteinschätzung nach jedem Übungsabschnitt ("Nochmal / Knapp / Fast / Gut / Perfekt") übernimmt die Feedback-Funktion für die Chorübung. Ein klassisches Quiz-System (richtig/falsch) wird erst relevant wenn weitere Anwendungsfälle wie Jagdschein oder Mathematik hinzukommen — das ist Phase 2 oder später.

---

### Defizit 2: Kein Lernfortschritt
**Entscheidung: Wird umgesetzt in Phase 1.**
Der Lernfortschritt wird als **farbiger Ring um das Icon** im Explorer visualisiert — 5 Stufen (0 / 20 / 40 / 60 / 80 / 100%), ablesbar an Füllung und Farbe (rot → orange → gelb → hellgrün → grün).

Basis ist der **Stability Score** aus der Spaced Repetition Engine — kein separates Tracking erforderlich.

Drei Ebenen der Aggregation:
- **Abschnitt:** direkt aus dem Stability Score
- **Stück:** Durchschnitt aller Abschnitte
- **Konzert:** Durchschnitt aller Stücke

---

### Defizit 3: Keine Notizen oder Markierungen
**Entscheidung: Für Phase 1 nicht umgesetzt.**
Für die Chorübung nicht erforderlich — Stability Score und Wiederholungslogik der Spaced Repetition Engine ersetzen persönliche Anmerkungen. Notizfunktion wird zurückgestellt für Anwendungsfälle wie Mathematik oder Jagdschein (Phase 2+).

---

### Defizit 4: Inhalte sind statisch
**Entscheidung: Teilweise umgesetzt in Phase 1.**
Die **jeweils letzte Gesangsaufnahme** pro Übungsabschnitt wird gespeichert und kann angehört werden. Ältere Aufnahmen werden überschrieben — es gibt immer genau eine Aufnahme pro Abschnitt.

Details:
- **Speicherort:** lokal auf dem Gerät oder in der Cloud — der Nutzer kann wählen
- **Verwendung:** Nur anhören (kein automatischer Vergleich mit dem Original)
- In Phase 2 bildet die Cloud-Speicherung die Basis für kollaborative Features

---

### Defizit 5: Keine Suchfunktion
**Entscheidung: Wird umgesetzt in Phase 1.**
Suche ist über einen **Suchbutton im Explorer** zugänglich (nicht permanent sichtbar, spart Platz auf dem Smartphone).

Zwei Modi:
- **Textsuche** nach Stückname, Dateiname, Konzert- / Ordnername
- **Lernstandsfilterung** nach Stability Score (z.B. alle schwachen Abschnitte) oder noch nicht geübten Abschnitten

Die Filterfunktion ermöglicht schnellen Zugriff auf das was heute geübt werden sollte — auch ohne den Geführten Modus zu nutzen.

---

### Defizit 6: Kein kollaboratives Element
**Entscheidung: Zurückgestellt auf Phase 2.**
Kollaboration setzt mehrere Nutzer voraus und ist für Phase 1 (Einzelnutzer) nicht relevant.

Für Phase 2 geplant:
- Der Chorleiter sieht den Übungsfortschritt **aggregiert nach Stimmen** (z.B. "70% der Bässe haben Abschnitt 3 gut im Griff") — nicht auf Einzelperson-Ebene, um Kontrollgefühl zu vermeiden
- Einzelne Chormitglieder können ihren persönlichen Fortschritt **freiwillig teilen**
- Detailgrad und genaue Umsetzung wird in Phase 2 erarbeitet

---

## 16a. Player-Bedienelemente im Detail

### Modus-Umschalter

Am oberen Rand des Players ist ein **Toggle immer sichtbar**:

```
[ ▶ Vorspielen ]  [ 🎤 Üben ]
```

Der Toggle bestimmt welche Steuerelemente in der unteren Zone angezeigt werden. Die beiden Modi haben grundlegend unterschiedliche Steuerungen.

---

### Vorspiel-Modus — Kreisförmige Steuerung

Die Steuerung ist kreisförmig angeordnet (analog zur Explorer-Steuerung, inspiriert vom Amazon Fire Stick), optimiert für Einhandbedienung mit dem Daumen:

```
              ▲ Tempo +10%

◀◀           ◀           ▶/⏸           ▶           ▶▶
Abschnitt-  -X Sek      Play/Pause    +X Sek     Abschnitt-
navigation                                        navigation

              ▼ Tempo -10%
```

**Belegung im Detail:**

| Position | Einfacher Druck | Doppelter Druck |
|---|---|---|
| Mitte | Play / Pause | — |
| Links | −X Sekunden (frei konfigurierbar) | — |
| Rechts | +X Sekunden (frei konfigurierbar) | — |
| Ganz links | Anfang des aktuellen Abschnitts | Vorheriger Abschnitt / vorheriges Stück |
| Ganz rechts | Nächster Abschnitt | Nächstes Stück |
| Oben | Tempo +10% | — |
| Unten | Tempo −10% | — |

**Navigationslogik ganz links:**
- Einfach = Anfang des aktuellen Abschnitts
- Doppelt = vorheriger Abschnitt
- Doppelt am ersten Abschnitt = vorheriges Stück
- Doppelt am ersten Abschnitt des ersten Stücks = letztes Stück des Konzerts (Loop)

**Navigationslogik ganz rechts:**
- Einfach = nächster Abschnitt
- Doppelt = nächstes Stück
- Doppelt am letzten Abschnitt des letzten Stücks = erstes Stück des Konzerts (Loop)

**Hinweis Tempo:** Das Tempo wird relativ zum MusicXML-Originaltempo angepasst (z.B. 80% zum Einüben). Metronom und Wiedergabe laufen dabei immer synchron — das Verhältnis bleibt 1:1.

---

### Erweiterte Steuerung (Vorspiel-Modus)

A-B-Loop, Wiederholung und Zurück-zum-Explorer sind **nicht dauerhaft sichtbar** um den Kreis nicht zu überladen. Sie werden durch **Swipe nach oben** oder **Tipp auf einen Anfasser am oberen Rand** der Steuerungszone zugänglich — die Steuerung schiebt sich dann in den Inhaltsbereich hinein (kontextsensitives Layout gemäß Kapitel 4).

Inhalte der erweiterten Steuerung:
- **Wiederholung:** aktuellen Abschnitt einmal / endlos / gesamte Sequenz
- **A-B-Loop:** Punkt A setzen, Punkt B setzen, Bereich einmal oder endlos wiederholen
  - Score/Fortschrittsbalken bleibt dabei sichtbar um A und B platzieren zu können
- **Zurück zum Explorer**

---

### Übungs-Modus

Im Übungs-Modus läuft der dreiphasige Zyklus (Kapitel 14) geführt ab. Die Steuerung ist bewusst schlicht gehalten damit der Inhaltsbereich (Score/Visualisierung) mehr als 60% des Bildschirms einnehmen kann — genaue Aufteilung wird beim Prototyp entschieden.

#### Stimmauswahl

Wird **einmalig beim Öffnen des Stücks** festgelegt (z.B. Bass 2). Die gewählte Stimme wird im Score hervorgehoben und bestimmt die Ausgangslage des Crossfaders. Ein Wechsel der Stimme erfordert das erneute Öffnen des Stücks.

#### Steuerungszone (von oben nach unten)

```
┌─────────────────────────────────────────┐
│  Einstieg: [ Vorlauf-Takte: 2 ] oder   │
│            [ Einstimmton: Grundton/Akkord]│
│  Metronom: [ Ein / Aus ]               │
│  Zählweise: [ ♩♩♩♩ ] [ ♪♪♪♪♪♪♪♪ ]     │
│  Tempo:    [ − ]  80%  [ + ]           │
├─────────────────────────────────────────┤
│                                         │
│           ▶  START ÜBEN                │
│                                         │
├─────────────────────────────────────────┤
│  Begleitung ◄────────●────────► Stimme │
│              Crossfader                 │
└─────────────────────────────────────────┘
```

**Konfiguration (immer sichtbar):**
- **Einstieg:** entweder N Vorlauf-Takte tutti (konfigurierbare Anzahl) — oder Einstimmton (Grundton der eigenen Stimme oder zugehöriger Akkord). Beides zusammen ist nicht vorgesehen.
- **Metronom:** ein/aus — läuft immer synchron zur MusicXML-Wiedergabe, nie unabhängig
- **Zählweise:** passend zur Taktart des Stücks wählbar (z.B. bei 4/4: Viertelnoten oder Achtelnoten)
- **Tempo:** relativ zum Originaltempo in 10%-Schritten — Metronom bleibt immer synchron

**Play-Button:**
- Großer zentraler Button
- Startet Vorlauf oder Einstimmton → Sänger singt → automatischer Stopp am Ende des Abschnitts
- Aufnahme läuft parallel automatisch mit

**Crossfader (unterhalb des Play-Buttons):**
- Stufenloser Schieberegler
- Links = Begleitstimmen laut, eigene Stimme stumm (üben ohne Stütze)
- Rechts = eigene Stimme laut, Begleitstimmen leise (geführtes Üben)
- Kann auch während der Wiedergabe angepasst werden

---

### Bewertungsscreen

Nach dem automatischen Stopp am Ende des Abschnitts erscheint der Bewertungsscreen. Er enthält zwei Schichten die gleichzeitig nutzbar sind:

**Schicht 1 — Automatische Auswertung (Phase 2):**
- Tonhöhen-Abweichung in Cent vom Soll (aus MusicXML)
- Rhythmus-Abweichung der Einsätze und Tondauern vom Soll-Timing
- Wird angezeigt sobald die Mikrofon-Analyse verfügbar ist

**Schicht 2 — Selbsteinschätzung (Phase 1 + ergänzend Phase 2):**

| Stufe | Bedeutung | Effekt auf Stability Score |
|---|---|---|
| Nochmal | Gar nicht geklappt | Stark reduzieren |
| Knapp | Ansatzweise richtig | Reduzieren |
| Fast | Größtenteils richtig | Leicht reduzieren |
| Gut | Richtig mit kleinen Fehlern | Erhöhen |
| Perfekt | Fehlerfrei | Stark erhöhen |

**Aufnahme anhören:**
- Die gespeicherte Aufnahme kann direkt im Bewertungsscreen abgespielt werden
- Anhören und Selbsteinschätzung sind gleichzeitig möglich — der Sänger kann die Aufnahme laufen lassen während er die Stufe antippt
- Die gewählte Stufe löst die Aktualisierung des Stability Scores und den nächsten Wiederholungstermin in der Spaced Repetition Engine aus

---

## 16b. Technische Architektur — PC/Smartphone/Cloud

### Grundprinzip

Zwei grundlegend verschiedene Datentypen werden unterschiedlich behandelt:

| Datentyp | Charakteristik | Speicherort |
|---|---|---|
| Inhalte (MusicXML, MP3, Aufnahmen) | Groß, selten geändert | PC / Cloud / optional lokal |
| Lernfortschritt (Stability Scores, Wiederholungstermine) | Klein, häufig geändert | Immer lokal auf dem Smartphone |

### Phase 1 — PC + Smartphone im Heimnetz

Der PC stellt einen **WebDAV-Server** bereit. Das Smartphone greift über WLAN darauf zu — technisch identisch mit der späteren Cloud-Anbindung, nur dass der Server zu Hause steht.

- Inhalte liegen auf dem PC
- Smartphone streamt aus dem Heimnetz via WebDAV
- Lernfortschritt wird lokal auf dem Smartphone gespeichert und beim Verbinden mit dem PC synchronisiert
- Kein Cloud-Dienst, kein Backend, keine Authentifizierung nötig

### Phase 2 — Wechsel zur Cloud

Da die App WebDAV von Anfang an als Abstraktion nutzt ist der Wechsel zur Cloud nur eine **Konfigurationsänderung** — die URL zeigt dann auf Nextcloud oder kDrive statt auf den Heim-PC. Kein Lock-in auf einen bestimmten Dienst.

---

## 16c. Offline-Fähigkeit

### Lernfortschritt
Immer lokal auf dem Smartphone gespeichert — funktioniert ohne Verbindung. Wird beim nächsten Verbinden mit PC oder Cloud synchronisiert.

### Inhalte
Werden **manuell pro Stück oder Ordner** auf das Smartphone heruntergeladen ("dieses Konzert offline speichern"). Der Nutzer behält die Kontrolle über den Speicherplatz.

- Im Explorer sind offline verfügbare Inhalte erkennbar — z.B. durch ein Download-Symbol am Icon
- Eigene Aufnahmen werden ebenfalls lokal gespeichert und beim nächsten Verbinden synchronisiert
- "Offline speichern" funktioniert unabhängig von der Quelle — Heimnetz oder Cloud

---

## 17. Quiz-Player (zukünftiger Ausbau)

### Grundentscheidung
Die Lern-App unterstützt zwei grundlegend verschiedene Player-Typen. Der Inhaltsersteller legt beim Vorbereiten fest welcher Typ für einen Ordner gilt:

- **Media-Player** — für Mediendateien (MusicXML, MP3, PDF, Video)
- **Quiz-Player** — für Frage-Antwort-Dateien (Multiple Choice)

Explorer, Spaced Repetition Engine, Gamification und Cloud-Anbindung arbeiten für beide identisch.

### Quiz-Player Layout

Kein fester 60/40-Split — dynamisch je nach Frageinhalt:

```
┌─────────────────────────────────────────┐
│  Fortschrittsbalken + Timer             │
│  Frage 7 von 20  ████████░░░░  0:23    │
├─────────────────────────────────────────┤
│                                         │
│  Fragetext                              │
│  (optional: Bild, Audio, Video)         │
│                                         │
├─────────────────────────────────────────┤
│  [ Antwort A                          ] │
│  [ Antwort B                          ] │
│  [ Antwort C                          ] │
│  [ Antwort D                          ] │
└─────────────────────────────────────────┘
```

### Spielvarianten

**Lernmodus** (Einzelspieler, kein Zeitdruck)
- Fragen eines Themas durcharbeiten
- Falsch beantwortete Fragen kommen per Spaced Repetition wieder
- Kein Timer — reines Lernen

**Prüfungsmodus** (Einzelspieler, mit Timer)
- Feste Fragenanzahl, konfigurierbares Zeitlimit
- Keine Erklärungen während der Prüfung — erst danach
- Ergebnis: bestanden / nicht bestanden + Auswertung nach Themen

**Duell-Modus** (Phase 2)
- 1:1 oder Arena (bis zu 5 Spieler)
- 6 Runden à 3 Fragen, Kategoriewahl vor jeder Runde
- Ligasystem, asynchron spielbar

### Dateiformat für Fragen (JSON)

```json
{
  "frage": "Welcher Ruf gehört zum Rothirsch?",
  "media": "rothirsch_ruf.mp3",
  "antworten": [
    { "text": "Röhren", "richtig": true },
    { "text": "Bellen", "richtig": false },
    { "text": "Schreien", "richtig": false },
    { "text": "Pfeifen", "richtig": false }
  ],
  "erklaerung": "Der Rothirsch röhrt während der Brunft.",
  "schwierigkeit": 0.3
}
```

### Anwendungsbeispiel Jagdschein

Ein Jagdschein-Ordner kann beide Player-Typen kombinieren:
- 🎵 Wildrufe anhören → Media-Player
- ❓ Wildkunde Quiz → Quiz-Player

### Anwendungsfall: Führerschein-Theorie

Der amtliche Fragenkatalog für die deutsche Fahrprüfung ist als offener Datensatz verfügbar (BMDV / TÜV/DEKRA). Die Kategorien sind didaktisch bereits vorgegeben: Vorfahrt, Geschwindigkeiten, Abstände, Alkohol/Drogen, Technik, Umwelt, Gefahrenlehre. Der Quiz-Player kann diesen Datensatz ohne weitere Anpassung verarbeiten. Zielgruppe mit hohem Leidensdruck und klarem Prüfungstermin — starke Motivation, ideal für Duell-Modus zwischen Fahrschülern.

### Anwendungsfall: Sprachenlernen

Die Spielmechanik des Quiz-Players passt hervorragend zum Sprachenlernen. Die Fragen-JSON-Struktur ist sprachagnostisch — Sprache ist nur ein Datenpaket. Kategorien pro Sprache: Vokabeln nach Themenfeldern, Grammatik, Redewendungen, Zahlen, Aussprache-Logik. Der Duell-Modus hat hier einen besonders starken sozialen Anreiz: zwei Lernende duellieren sich gegenseitig — das schlägt jeden Vokabeltest. Phasenplan: Phase 1 Deutsch↔Italienisch / Deutsch↔Englisch, Phase 2 beliebige Sprachpaare.

```json
{
  "sprache": "it",
  "level": "A1",
  "kategorie": "vokabeln_essen",
  "frage": "Was bedeutet 'la mela'?",
  "richtig": "der Apfel",
  "falsch": ["die Birne", "die Orange", "die Zitrone"],
  "erklaerung": "La mela — der Apfel. Plural: le mele."
}
```

### Abgrenzung: Quiz Away

Ein standortbasiertes Geo-Quiz ("Quiz Away" / "RoadQuiz") wurde als **eigenständige separate App** ausgelagert. Es teilt die Spielmechanik (Timer, Punktesystem, Zwangsweiterschaltung, Duell, Liga) aber nicht die Codebasis der Lern-App.

Begründung: GPS-Logik, Städtedatenbank, Virtuelle-Route-Berechnung und geografische Falschantwort-Generierung sind so spezifisch dass eine Integration die Lern-App-Architektur unnötig belasten würde.

**Detailkonzept:** Siehe `quizaway_konzept-9.md` — vollständige Beschreibung von Datenbasis, Fragekategorien, Schwierigkeitsgrad-System, Build-Pipeline und Synchronisationsarchitektur.

**Übertragbare Konzepte von Quiz Away in die Lern-App:**
- Schwierigkeitsgrad-Auswahl vor dem Spiel (L/M/S)
- Auto-Timer mit Zwangsweiterschaltung als Grundlage für Echtzeit-Duelle
- sw-Feld in Fragen für Pool-Filterung nach Schwierigkeit
- Modus+Schwierigkeit-Badge im Spielscreen