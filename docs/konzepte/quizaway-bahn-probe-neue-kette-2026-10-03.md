# QuizAway — Probe der neuen Kette: Bahn Freiburg–Neuwied (10 Orte)

**Stand:** 2026-10-03 · **Grundlage:** Spielkonzept v0.3.1 §8 Nr. 9 (Quellen und Prüfstufen), Kosten-Pareto H2/H5 · **Daten:** `data/gemeinde-achsen/bahn/`

**In einem Satz:** Die neue Kette kostet im Mittel rund 236.000 Token je Ort statt rund 390.000 (−40 %). Bei Orten mit guter Gemeinde-Webseite sind es nur 115.000 bis 215.000 (−45 bis −70 %), bei Orten mit dünner Webseite 220.000 bis 400.000, weil dort Wikipedia einspringt und Prüfstufe 2 mit Netzsuche nötig wird. Die Befundquote liegt bei 11 % (bisher 26 %), ist aber noch nicht gegengeprüft.

---

## 1. Was gelaufen ist

Strecke: rechte Rheinseite (Rheintalbahn, RB10). Zehn Orte in drei Ländern: Kenzingen, Achern, Rastatt (BW); Eltville, Rüdesheim, Lorch (HE); Kaub, St. Goarshausen, Braubach, Vallendar (RP). Keine Spender.

| Schritt | wie | Werkzeug |
|---|---|---|
| Quellen | Gemeinde-Webseite (Adresse aus Wikidata), Seiten zu Geschichte, Porträt, Sehenswürdigkeiten; regionalgeschichte.net für drei RP-Orte | Skript `scripts/data-fetch/gemeinde_achsen_quellen_amtlich.py`, kein Modell |
| Extraktion | jeder Fakt mit Zeile `QUELLE: <Adresse> \| <Art>`; Wikipedia nur bei amtlicher Quelle unter 12.000 Zeichen | Direktaufruf Haiku, Prompt `prompt-stufe1-v0.6.txt` |
| Karten | Prompt v0.8 (v0.7 ohne Weg b, mit PRÜFSTUFE und ERFUNDEN je Karte) | Direktaufruf Opus (claude-opus-4-6, wie Probe H2) |
| Prüfstufe 1 | Abgleich mit dem Quelltext, ohne Netz | Direktaufruf Sonnet, `prompt-pruefung-v0.1.txt` |
| Prüfstufe 2 | Netzsuche nur für weitergereichte Karten, nur vertrauenswürdige Quellen | Direktaufruf Sonnet mit WebSearch/WebFetch, `prompt-stufe2-v0.1.txt` |

Läufe: `scripts/data-build/gemeinde_achsen_direkt.py`; Aufwand je Aufruf in `aufwand/`.

## 2. Aufwand je Ort

| Stufe | bisher (Raum Neuwied, Agenten) | neu (Mittel der 10 Orte) | Spanne neu |
|---|---|---|---|
| Quellen suchen | im Agenten enthalten | 0 Token, rund 15 s Skript | |
| Extraktion | rund 110.000 | **36.000** | 22.000–52.000 |
| Kartenlauf | rund 150.000 | **90.000** | 54.000–184.000 |
| Faktencheck | rund 130.000 (alles mit Netz) | **45.000** Stufe 1 + **65.000** Stufe 2 = **110.000** | 28.000–266.000 |
| **zusammen** | **rund 390.000** | **rund 236.000** (−40 %) | 115.000–397.000 |
| Kosten | nicht erfasst | 2,17 USD je Ort (21,70 USD für 10) | |
| Wanduhr | rund 9 min je Ort (bei Parallelbetrieb) | rund 25 min je Ort einzeln, 10 Orte parallel in rund 75 min | |

Je Ort:

| Ort | Quelle | Extr. | Karten | Stufe 1 | Stufe 2 | zusammen |
|---|---|---|---|---|---|---|
| Kenzingen | Gemeinde | 22k | 59k | 34k | – | **116k** |
| Achern | Gemeinde (dünn) | 22k | 62k | 30k | – | **115k** |
| Rastatt | Gemeinde | 34k | 92k | 44k | – | **170k** |
| Kaub | Gemeinde + Portal | 47k | 112k | 52k | – | **213k** |
| St. Goarshausen | Gemeinde + Portal | 42k | 92k | 55k | 43k | 233k |
| Lorch | Gemeinde | 52k | 76k | 62k | 58k | 249k |
| Vallendar | Gemeinde + Wikipedia | 29k | 74k | 33k | 83k | 221k |
| Braubach | Wikipedia (Gemeinde dünn) | 30k | 54k | 28k | 152k | 266k |
| Eltville | Gemeinde | 35k | 184k | 53k | 98k | 371k |
| Rüdesheim | Gemeinde + Wikipedia | 44k | 86k | 53k | 213k | 397k |

**Befund A1.** Die Hypothese trägt dort, wo die Gemeinde gute Seiten hat: Vier Orte brauchten keine Netzsuche, ihr Faktencheck kostete 30.000–52.000 Token statt 130.000.
**Befund A2.** Prüfstufe 2 ist teuer (43.000–213.000 Token je Ort) und fällt dort an, wo Wikipedia einspringen musste (Rüdesheim, Braubach, Vallendar) oder Superlative stehen (Eltville, Lorch, St. Goarshausen). Der Hebel ist also die Quellenlage, nicht die Prüfregel.
**Befund A3.** Der größte Posten ist jetzt der Kartenlauf (38 %). Opus denkt lange nach (Ausgabe 38.000–70.000 Token für rund 6.000 Token Karten), wie schon in der Probe H2. Nächster Hebel: Sonnet oder begrenzte Denktiefe für die Karten.

## 3. Qualität

96 Karten (9–10 je Ort; je Ort 3 Klassiker, Rest Geschichten).

| Urteil | Karten | Anteil |
|---|---|---|
| bestätigt in Stufe 1 | 69 | 72 % |
| korrigiert in Stufe 1 | 3 | 3 % |
| bestätigt in Stufe 2 | 10 | 10 % |
| korrigiert in Stufe 2 | 7 | 7 % |
| unsicher nach Stufe 2 (spielbar mit Vermerk) | 6 | 6 % |
| gesperrt | 1 | 1 % |
| **Befunde (korrigiert + gesperrt)** | **11** | **11 %** (bisher 26 % in den späten Läufen) |

**Befund Q1 — noch nicht gegengeprüft.** Stufe 1 prüft, ob die Karte zur Webseite passt, nicht, ob die Webseite stimmt. 69 Bestätigungen ohne Netz können also zu nachsichtig sein. Vorgeschlagene Gegenprobe: zehn in Stufe 1 bestätigte Karten zusätzlich mit voller Netzsuche prüfen (rund 100.000 Token). Erst danach ist die Befundquote vergleichbar.
**Befund Q2 — dünne Seiten ziehen die Karten weg vom Ort.** Achern: Die Seite „Historisches“ liefert Fehler 404; Karte 1 fragt deshalb nach der Namensherkunft der Partnerstadt Morez. Sachlich richtig, aber keine Karte über Achern. Regel für den nächsten Lauf: Eine Geschichte handelt vom Zielort; Fakten über Partnerstädte tragen höchstens einen Klassiker.
**Befund Q3 — Anschlüsse im alten Ton.** Die Läufe starteten vor der neuen Anschluss-Regel (Prompt v0.8, Regel 10, Nachtrag 2026-10-03); „Doppelt so viele Einwohner wie Achern …“ steht ohne Ortsnamen. Berichtigung wie bei Freiburg und Neuwied über `anschluss-berichtigt.json`.

## 3a. Nachtrag: Gegenprobe und Sonnet (2026-10-03, Entscheide Mike)

**Gegenprobe zu Q1.** Je Ort eine in Stufe 1 bestätigte Geschichten-Karte, zufällig (Startwert 20261003; Braubach hatte keine), mit voller Netzsuche geprüft (Prompt `prompt-gegenprobe-v0.1.txt`, Sonnet, rund 42.000 Token je Karte). Ergebnis: **3 von 9 mit Fehler**, alle in einer Zahl der Rückseite, alle schon in der vertrauenswürdigen Quelle:

| Ort | Karte | Quelle sagt | unabhängige Quellen sagen |
|---|---|---|---|
| Vallendar | Marienburg erbaut | 1779 (Stadtseite) | 1773 (Rhein-Zeitung, alleburgen.de, Blick aktuell; Goethe 1774 dort) |
| St. Goarshausen | Höhe Viereckiger Turm | 34 m (Stadtseite) | 23 m (KuLaDig) |
| Kaub | Tote des Bergsturzes 1876 | 26 (regionalgeschichte.net) | 25 (Gartenlaube 1876 u. a.) |

Die Kernaussagen hielten in 9 von 9 Karten. Folgerung: Die Annahme „vertrauenswürdige Quelle, also genügt der Abgleich ohne Netz“ hält für Kernaussagen, nicht für Zahlen und Jahre in Nebensätzen. Hochgerechnet läge die Befundquote ohne Gegenmaßnahme bei 30–35 %.

**Entscheid Mike (2026-10-03): Zahlenregel, „ohne dass es teurer wird“.** Prompt v0.8.1, Regel 9: Die Rückseite nennt eine Zahl, ein Jahr oder ein Maß nur, wenn die Frage danach fragt oder die Geschichte sie braucht; keine Zierzahlen. Prüfung v0.2, Punkt 3a: jede weitere Zahl auf der Rückseite geht an Stufe 2. Die drei Karten sind nach der Regel berichtigt (Zahl gestrichen statt ersetzt; `korrekturen-hand.json`).

**Sonnet für den Kartenlauf (A3).** An fünf Orten gemessen, dann abgebrochen: Kenzingen 161.000 Token, 17 min, 1,26 USD (Opus: 59.000, 12 min, 1,13 USD); Achern, Rastatt, Eltville und Rüdesheim liefen bis an die Ausgabegrenze von 128.000 Token Nachdenken (je 33 min, 2,00 USD) und lieferten **keine einzige Karte**. Sonnet ist für diesen Prompt kein Hebel; der Kartenlauf bleibt bei Opus. Der nächste Hebel dort ist die Denktiefe, nicht das Modell.

**Grunddaten.** Rastatts Ergebnis (AfD 31,4 % vor CDU, Beteiligung 75,5 %) an der Pressemitteilung der Stadt bestätigt. Wikidata führt für St. Goarshausen das Kennzeichen „TR“ (falsch; Rhein-Lahn-Kreis: EMS); keine Karte nutzt es.

## 3b. Ausbau auf 29 Orte (2026-10-03 abends)

19 weitere Orte (Rheintal, Bergstraße – Mike: „über die Bergstraße“ –, Rheingau, Mittelrhein), mit Prompt v0.8.1 und Prüfung v0.2 (Zahlenregel). Alle 29 Orte sind im Fahrt-Prototyp (dritter Raum, 273 Karten; Artifact Version 7).

| | erste 10 (v0.8) | Ausbau 19 (v0.8.1) | bisher (Agenten) |
|---|---|---|---|
| Token je Ort | 236.000 | 200.000 (mit verlorenen Läufen rund 209.000) | 390.000 |
| Kosten je Ort | 2,17 USD | 1,85 USD | – |
| Extraktion / Karten / Stufe 1 / Stufe 2 | 36k / 90k / 45k / 65k | 45k / 70k / 43k / 42k | 110k / 150k / 130k |
| Urteile | 76 bestätigt, 13 korrigiert, 6 unsicher, 1 gesperrt | 163 bestätigt, 11 korrigiert, 4 unsicher | |

Die Befundquote des Ausbaus (6 %) ist nicht gegengeprüft; nach der Gegenprobe der ersten 10 ist sie eine Untergrenze. Die Zahlenregel hat die Netzsuche gesenkt (Stufe 2 im Mittel 42.000 statt 65.000 Token je Ort).

**Betriebsbefunde.** (1) Ein Kartenlauf hing über 60 Minuten, das Skript brach daraufhin die ganze Reihe ab; ein anderer verlor bei sehr langer Antwort alles bis auf die letzten zwei Karten (Lahr, 169.000 Token umsonst); einer endete mit „Request timed out“. Das Skript fängt das jetzt ab und wiederholt Läufe mit weniger als sieben Karten einmal (`aufwand/verlorene-laeufe-2026-10-03.json`). (2) Wikidata-Kennzeichen sind mehrfach falsch (Bühl „OG“ statt RA, Lahr „LR“ statt OG, St. Goarshausen „TR“ statt EMS); keine Karte hängt daran, Anschlüsse vergleichen dort den Landkreis. (3) Durch das Einschieben neuer Orte bekamen sieben Messorte einen neuen Vorgänger; Anschlüsse tragen deshalb jetzt ihren Vorgänger (`anschluss-berichtigt.json`, Feld „von“), der Export zeigt sie nur für genau dieses Ortspaar. (4) Lahr wählte wie Rastatt AfD vorn (31,4 %, Beteiligung 75,1 %; Schwarzwälder Bote) – richtig, nicht Datenfehler.

## 4. Quellenlage

| | Orte |
|---|---|
| Gemeinde-Webseite allein reichte (über 12.000 Zeichen) | Kenzingen, Achern, Rastatt, Eltville, Lorch, Kaub, St. Goarshausen |
| dünn, Wikipedia kam dazu | Rüdesheim (knapp unter der Grenze), Braubach, Vallendar |
| Landesportal per Adresse erreichbar | regionalgeschichte.net (Kaub, St. Goarshausen, Braubach); LEO-BW antwortete nicht (504), LAGIS Hessen nur per Skript-Oberfläche |
| Fallen im Skript | Seiten, deren Menü erst ein Skript baut (Kenzingen: über die Sitemap gelöst); Verbandsgemeinde-Seiten (Kaub, Braubach unter welterbe-mittelrheintal.de); Tourismus-Domain statt Stadt (Rüdesheim: stadt-ruedesheim.de gesetzt) |

## 5. Was daraus folgt

1. **Gegenprobe Stufe 1** (Q1) vor jeder Aussage über die Qualität.
2. **Kartenlauf mit Sonnet** an denselben zehn Eingaben messen (A3); erwartet: Kartenlauf deutlich unter 50.000 Token.
3. **Quellen verbessern statt mehr prüfen** (A2): für dünne Orte das Landesportal ernsthaft anbinden (LEO-BW, LAGIS), damit Wikipedia und Stufe 2 seltener werden.
4. Danach Ausbau auf 30–40 Orte für die echte Fahrt.

### Wo der Mensch billiger ist als die Automatik
- Mike kennt für Rheingau und Mittelrhein vielleicht Ortschroniken oder Heimatvereine; eine Adresse je dünnem Ort spart dort die teure Netzsuche.
- Die Gegenprobe Q1 ist Maschinensache; Mike sieht danach drei bis fünf Karten nur nach Geschmack.
