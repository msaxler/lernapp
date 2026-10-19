# QuizAway Ortsporträt – Quellenbefund (19.10.2026)

**Anlass:** Konzept „Ortsporträt“ v0.1 (Mobile-Session nach zwei echten Fahrten); Mike: *Qualität und Spielfreude zuerst, Region Freiburg, lieber fünf gute Orte am 5.11. als viele mittlere.* Pilotstrecke Freiburg–Breitnau (Tochter: Höllentalbahn, B31, Rad; Breitnauer Hof): Ebnet, Littenweiler, Kirchzarten, Stegen, Buchenbach, Oberried, Hinterzarten, Breitnau, Titisee-Neustadt.
**Frage:** Geben die Quellen die *Charakteristika* her, die das Konzept verlangt (Bad, Betrieb, Fest, Weg, Fluss, Klinik, Schanze …) – nicht nur Jahreszahlen?

## 1. OpenStreetMap (Overpass, benannte Objekte in der Gemeindegrenze)
Skript `scripts/data-explore/osm_ortsportraet_probe.py`, Ergebnisse `data/gemeinde-achsen/probe-ortsportraet/osm-<ort>.json`.

| Ort | Objekte | Was heraussticht |
|---|---|---|
| Kirchzarten | 106 | Dreisambad, Tarodunum-Rundweg (Keltenstadt), Burg, Römerhaus, Rainmühle, Golfclub, Mediathek, 13 Bäche, 66 Wanderwege |
| Staufen | 125 | Burg Staufen, Keramikmuseum, Faustforum, Schladerer, 4 Weingüter, Alemannenbad, Kletterwald, Naturpark |
| Buchenbach | 150 | Friedrich-Husemann-Klinik, Siko, Wandres, Transportbetonwerk, Ibentalhalle, 97 Wanderwege |
| Hinterzarten | 221 | Adler-Skistadion, Földi-Klinik, Klinik in der Zarten, Barfußpfad, Hinterzartener Moor, 8 Schutzgebiete, Westweg, 159 Wanderwege |
| Breitnau | 193 | Hallenbad, **vier Skisprungschanzen**, Ravennaviadukt/-schlucht, Weißtannenhöhe 1191 m, Großjockenmühle (1883), Hirschenmoor, 142 Wanderwege |

**Befund:** OSM ist die **Zeugenliste** – es sagt verlässlich, *was es gibt* (mit Koordinate, oft Baujahr, Höhe, Webseite), aber fast nie *warum es bemerkenswert ist*. Wanderwege sind zahlreich, aber nur die mit Namen wie Westweg, Tarodunum-Rundweg, Türkenlouispfad taugen für Karten; die 100 Verbindungsstücke („Höfener Hütte – Holzeck“) sind Rauschen. Flüsse: der erste (Dreisam, Neumagen) trägt, der Rest nicht.

## 2. Gemeinde-Webseiten (`gemeinde_achsen_quellen_amtlich.py`)
| Ort | Seiten | Zeichen | Treffer |
|---|---|---|---|
| Breitnau | 10 | 25.400 | Dorfchronik, Kurzportrait, Heimatpfad, Türkenlouispfad, Hirschsprung, Ravennaschlucht/St. Oswald, **Windkraft und Walmdächer** |
| Kirchzarten | 8 | 31.800 | Geschichte, Portrait, Burg, Persönlichkeiten und Ehrungen, Zahlen |

**Befund:** Hier stehen die Geschichten zu den OSM-Zeugen. Das Skript sucht heute nach Geschichte, Porträt, Sehenswertes, Zahlen (`STICH`); für das Ortsporträt fehlen **Freizeit/Bäder, Vereine, Feste/Märkte, Wirtschaft/Gewerbe, Wanderwege** als Suchwörter – die Seiten existieren (Breitnau hat „freizeit-in-breitnau“), werden aber nur über „sehenswertes“ gefunden.

## 3. Wikipedia
Breitnau 9,6 KB, Kirchzarten 21 KB – wie bisher die Rückfall- und Faktencheck-Quelle (Ersterwähnung, Eingemeindung, Söhne/Töchter, Infobox).

## 4. Folgerung für die Kette
1. **OSM als dritte Quelle** je Ort: Zeugenliste gefiltert (Wanderwege nur mit Fernweg-/Themenweg-Namen, Flüsse nur der größte, Hallen/Studios raus) als Block `ZEUGEN (OpenStreetMap)` in Extraktion und Karteneingabe. Jeder Zeuge, der in Webseite oder Wikipedia vorkommt, wird ein Charakteristikum mit Geschichte; die übrigen gehen in den Steckbrief („Hallenbad, vier Schanzen, 142 km Wanderwege“).
2. **Webseiten-Suche erweitern** um Freizeit, Bad, Verein, Fest, Markt, Gewerbe, Betrieb, Wanderweg, Radweg; `MAX_SEITEN` 14 → 20.
3. **Neuer Karten-Prompt v0.9 „Ortsporträt“:** Facetten (Lage · Geschichte · Wirtschaft/Alltag · Kultur/Freizeit · Infrastruktur · Politik), je Karte ein Charakteristikum, Frage als Vehikel, **Rückseite = Einordnungssatz** (≤ 2 Sätze, vorlesbar), Zahlen nur als Einordnung; Rangfolge nach Ungewöhnlichkeit für die Ortsgröße; am Ende ein **Steckbrief** (5 Zeilen, eine je Facette). Wahlbeteiligung nur auffällig (schon so).
4. **Probekarten** zuerst: Kirchzarten (433) und Breitnau (432) mit dem neuen Prompt, 3–5 Karten je Ort an Mike und Tochter – erst dann die übrigen sieben Orte der Pilotstrecke.

## 5. Was Mike entscheidet (Hebel)
- Ob die Probekarten das „Echt?!“ auslösen – das kann nur der Mensch im Auto beurteilen.
- Reihenfolge der Facetten nach Geschmack (mehr Freizeit, weniger Politik?).
- Ob Kirchzarten im Raum bahn den alten iter1-Vorrat (12 Karten) ersetzt oder ergänzt.
