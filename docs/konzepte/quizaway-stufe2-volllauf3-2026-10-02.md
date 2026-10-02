# QuizAway — Stufe 2, dritter Volllauf Raum Freiburg: Bericht

**Datum:** 2026-10-02 · **Grundlage:** Probe-Bericht `quizaway-stufe2-probe-v0.6-2026-10-02.md`, Spielkonzept v0.2.6 · **Freigabe:** Mike, 2026-10-02 („JA" zum dritten Volllauf auf den übrigen sieben Orten; „JA" dazu, dass die v0.6-Karten zum Vorrat kommen und bei gleichem Fakt die v0.6-Karte bleibt) · **Daten:** `data/gemeinde-achsen/iter1/` (`prompt-karten-v0.6.1.txt`, `eingabe-v0.6/`, `karten-v0.6/`, `faktencheck-v0.6/`, `vorrat.json`)

**Ergebnis in einem Satz:** Mit dem dritten Lauf hat jeder der zehn Orte zwischen 11 und 15 geprüfte Karten im Vorrat, zusammen 129; von den 86 Karten des Prompts v0.6 bestätigt der Faktencheck 64, korrigiert 18, führt 3 als nur durch Wikipedia belegt und sperrt eine.

Was der Lauf nicht zeigt: ob die Karten am Tisch eine Theorie hervorrufen. Das misst der Feldtest mit dem Kartensatz, der unverändert bereitliegt.

---

## 1. Was gelaufen ist

| Glied | Womit | Ergebnis |
|---|---|---|
| Eingabe | `gemeinde_achsen_karten_eingabe.py`: Plan mit vorgegebener Klassiker-Eigenschaft, Lage, Berichtigungen aus dem Faktencheck, ein Spender | sieben Eingabedateien (die drei Probeorte waren fertig) |
| Karten | `prompt-karten-v0.6.1.txt`: sieben Pflichtkarten, bis zu drei Zusatzkarten | 65 Karten an sieben Orten, davon 16 Zusatzkarten; mit der Probe 86 |
| Prüfung | `gemeinde_achsen_karten_pruefen_v05.py --lauf v0.6` | ein Verstoß in 86 Karten (eine Aussage mit neun Wörtern, korrigiert) |
| Faktencheck | `faktencheck/auftrag-v0.6.txt`, je Ort ein Durchlauf mit Netz | `faktencheck-v0.6/` |
| Korrekturen | `faktencheck/korrekturen.json`, `gemeinde_achsen_korrekturen_anwenden.py` | `karten-geprueft/v0.6/` |
| Vorrat | `vorrat.json`, `gemeinde_achsen_vorrat.py` | `quizaway-stufe2-vorrat-2026-10-02.md`, `vorrat-liste.json` |

**v0.6.1 gegenüber v0.6 der Probe:** zwei Zusätze. Der Block Berichtigungen (Befunde früherer Faktenchecks gehen den Fakten vor) und die Zusatzkarten 8 bis 10 nach Mikes Hinweis vom selben Tag: Sieben ist die Untergrenze, mehr ist erwünscht, wenn die Fakten es hergeben.

---

## 2. Zahlen

**Faktencheck der Läufe im Vergleich:**

| | v0.5 (70 Karten) | v0.6 (86 Karten) |
|---|---|---|
| bestätigt | 43 (61 %) | 64 (74 %) |
| korrigiert | 18 | 18 |
| unsicher (nur Wikipedia) | 4 | 3 |
| gesperrt | 5 | 1 |
| „falsche" Antwort, die stimmt oder der Wahrheit nahekommt | 6 | 2 |

**Karten je Ort im dritten Lauf:** Umkirch 9, Gundelfingen 8, Denzlingen 9, Glottertal 9, Kirchzarten 10, Günterstal 10, Staufen 10; die Probeorte Zähringen, St. Peter und Horben je 7 (sie liefen vor dem Hinweis zu den Zusatzkarten).

**Der Vorrat nach dem Zusammenführen:**

| Ort | im Vorrat | davon Klassiker | ersetzt | herausgenommen | gesperrt |
|---|---|---|---|---|---|
| Umkirch | 11 | 4 | 8 | 0 | 0 |
| Gundelfingen | 13 | 5 | 5 | 0 | 0 |
| Denzlingen | 15 | 6 | 2 | 0 | 2 |
| Zähringen | 12 | 4 | 3 | 0 | 2 |
| St. Peter | 14 | 6 | 3 | 0 | 0 |
| Glottertal | 15 | 5 | 4 | 0 | 0 |
| Kirchzarten | 13 | 5 | 7 | 0 | 0 |
| Günterstal | 12 | 4 | 7 | 0 | 1 |
| Horben | 12 | 4 | 2 | 2 | 1 |
| Staufen | 12 | 5 | 8 | 0 | 0 |
| **zusammen** | **129** | **48** | **49** | **2** | **6** |

Von den 129 Karten sind 92 bestätigt, 32 korrigiert und 5 unsicher. 85 stammen aus dem dritten Lauf, 30 aus dem zweiten, 14 aus dem ersten. Familien: 73 Behauptungen, 20 Lügen, 29 Spannen, 7 Leitern.

---

## 3. Befunde

**D1. Mehr als sieben geht, und die Läufe hören von selbst auf.** Alle sieben Orte nutzten Zusatzkarten, drei alle drei. Vier Läufe hörten vor der zehnten Karte auf, weil kein tragfähiger Fakt mehr da war. Die Zusatzkarten sind keine schwächeren: Von den 16 sind 11 bestätigt und 5 korrigiert.

**D2. Die Berichtigungen wirken.** Gundelfingen ließ den unbelegten Fakt zum Ersten Weltkrieg liegen und die strittige Prozentzahl von Wildtal weg. Denzlingen mied die im zweiten Lauf gesperrten Stoffe (Spiraltreppe und Dürer, Grimmelshausen). Kirchzarten schrieb „Mountainbike-Weltmeisterschaften" ohne den falschen Superlativ und „an Baden" ohne den falschen Rang. Zwei Nebenwirkungen: Staufen baute eine Karte auf eine Berichtigung (Gusseisenbrücke) und gab dazu die falsche Quelle an; Denzlingen konnte „1993, nicht 1983" nicht zuordnen, weil die Berichtigung ihre Sache nicht nannte. Die Berichtigungen dieses Laufs nennen deshalb Ort und Sache.

**D3. Die Klassiker sind jetzt verschieden.** Zahlen-Karten: Einwohner (2), Ersterwähnung (1), Fläche (3), Höhe (1), Einwohnerdichte (3). Politik: zweitstärkste Partei (4), Wahlbeteiligung (3), Anteil der stärksten Partei (3). Zugehörigkeit: Landkreis (1), Kennzeichen (2), Partnerstadt (2), Eingemeindung (2), Luftlinie nach Stuttgart (1), Fläche (1), Dichte (1). Alle 30 Klassiker des dritten Laufs sind bestätigt oder nur am Rand korrigiert (Stichtag einer Einwohnerzahl, Tag einer Eingemeindung, Straßen- statt Luftlinienkilometer).

**D4. Die Stadtteile haben eigene Wahlergebnisse.** Zähringen fragt nach der zweitstärksten Partei im Stadtbezirk, Günterstal nach der Wahlbeteiligung im Stadtbezirk. Die Freiburg-weiten Karten des zweiten Laufs sind dadurch ersetzt.

**D5. Die Zahl aus dem Artikel kommt einmal vor.** Glottertal fragt nach den Übernachtungen im Jahr (rund 160.000 bei 3.200 Einwohnern). Die Auflösung stimmt; die Bettenzahl daneben war veraltet.

**D6. Was der Faktencheck noch findet, sind Nebensätze.** Typisch für diesen Lauf: Der Denzlinger Kirchturm ist älter als 1547, nur sein Aufbau stammt von da; eine Schule ist falsch benannt; das Flugzeug stürzte über Umkirch ab, abgeschossen wurde es über Freiburg; die Feuerwehr wurde 1994 zusammengelegt, nicht gegründet; ein Hebel-Zitat steht in umgeschriebener Schreibweise. Die Kernaussage war in keinem dieser Fälle falsch.

**D7. Zwei Karten hatten noch eine angreifbare falsche Option.** Horbens Kirchenportal („aus einer aufgehobenen Klosterkirche", korrigiert) und Günterstals Gefecht von 1848 („das Tal sei frei von Truppen", dazu eine Auflösung nur aus Wikipedia; gesperrt). Im zweiten Lauf waren es sechs.

**D8. Die Grenze von zwanzig Karten je Ort ist nirgends erreicht.** Der vollste Vorrat hat 15 Karten. Aus dem Vorrat genommen wurden zwei alte Karten, die den neuen Regeln widersprechen: Horbens Dammhöhe (Zahl ohne Anhalt) und Horbens Ortshöhe (Quellen uneins).

---

## 4. Aufwand

- Kartenläufe an sieben Orten: je 5 bis 7 Minuten, zusammen rund 980.000 Tokens.
- Faktenchecks an sieben Orten: je 3 bis 5 Minuten, zusammen rund 880.000 Tokens.
- Zusammen rund 1,85 Millionen Tokens für 65 Karten, also rund 28.000 je geprüfter Karte. Das ist eine Obergrenze, weil jeder Durchlauf als eigenständiger Agent mit seinem ganzen Rahmen lief.

### Wo ein Mensch mehr bringt als die Automatik

- **„Derselbe Fakt" beim Zusammenführen** habe ich von Hand entschieden (49 Zuordnungen in `vorrat.json`). Eine Regel dafür gibt es nicht; bei zehn Orten kostet die Hand eine halbe Stunde, eine Automatik wäre teurer und unsicherer. Für tausend Orte braucht es eine Lösung an der Wurzel: Jede Karte hängt an einem Fakt der Datenbank, dann ist „derselbe Fakt" eine Abfrage.
- **Streichen im Vorrats-Blatt** bleibt bei Mike und kostet nur, wo etwas nicht gefällt.

---

## 5. Was Mike entscheidet

1. **Vorrats-Blatt:** streichen, was nicht gefällt. Neu sind die 85 Karten des dritten Laufs.
2. **Die Grenze je Ort:** Vorläufig gilt zwanzig. Vorschlag: so lassen, bis ein Ort sie erreicht.

Ohne Entscheid, als nächste Schritte am PC: die Berichtigungen an die Fakten selbst hängen statt an die Eingabe (Extraktion berichtigen, damit der Fehler nicht bei jedem Lauf neu abgefangen werden muss); jede Karte an ihren Fakt binden (siehe §4); Spielkonzept v0.2.7 mit den Nachträgen vom 2. Oktober.

---

## 6. Was ab jetzt da ist

Zehn Orte, 129 geprüfte Karten, je Ort 11 bis 15, in drei Familien und zwei Sorten. Jede Karte trägt das Urteil des Faktenchecks, 92 sind ohne jede Änderung bestätigt. Der Kartensatz für den Tisch liegt bereit, und hinter jeder seiner zehn Karten warten am selben Ort mindestens zehn weitere.

*Ende Bericht.*
