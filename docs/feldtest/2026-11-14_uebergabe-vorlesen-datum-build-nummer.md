# Übergabe: Datum beim Vorlesen + Build-Nummer (Reise-Prototyp)

- Stand: 2026-11-14, mobil erstellt (Feldtest zu Fuß), am PC übernommen am selben Tag
- Herkunft: Google Drive `GEOSYNC__019__quizaway__docs__uebergabe-vorlesen-datum-build-nummer.md` (Handy-Claude); hier gekürzt um den Codeblock, der jetzt in `apps/quizaway-reise/index.html` steht
- Referenz damals: Claude-Artifact „QuizAway Reise-Prototyp“, Build 75

## Anlass

Im Feldtest las die Handystimme „vom 31. Juli 1743“ als „31“, Pause, „Juli“ (Bendorf-Karte, Verlustliste). Ursache ist die Stimme selbst, nicht der Satzschnitt und nicht der Cache. Auf quizaway.pages.dev lag ein älterer Stand ohne Build-Nummer.

## Änderungen (übernommen)

1. **Tag im Datum als Ordnungszahl sprechen:** `tagWort()` + `fuerSprache()` vor `sprich()`; `sprich` schneidet `fuerSprache(text)` in Sätze. Angezeigter Text unverändert. Nicht abgedeckt: rein numerische Daten („31.7.1743“); nach „und“ (z. B. „zwischen dem 1. und 3. Mai“) kommt „dritter“ statt „dritten“.
2. **Build-Nummer in der Kopfzeile**, von Hand hochzuzählen bei jeder Veröffentlichung.

Höreindruck am Handy bestätigt (Nachtrag 14.11., 12:03): Build 75 liest das Datum flüssig.

## Übernahme am PC (14.11.2026)

- Artifact Build 75 gegen den Repo-Stand (v73) verglichen: genau diese zwei Änderungen, sonst nichts; `daten.js`/`grund-de.js` unverändert.
- Ins Repo übernommen, Build auf **76** gesetzt; Probe der Umwandlung mit Node an 9 Fällen, 0 Fehler; lokal im Browser geladen, keine Konsolenfehler.
- Veröffentlicht: **quizaway.pages.dev** (Deploy `53bb3792`) und das Artifact (Version 76) – beide zeigen „Build 76“.
- Festlegung: **Feldtest-Adresse ist quizaway.pages.dev** (im Artifact geht GPS nicht, der Dienst bettet ohne Ortungsrecht ein). Beide Adressen werden aus `apps/quizaway-reise/index.html` veröffentlicht, gleiche Build-Zählung. Änderungen künftig im Repo machen, nicht direkt im Artifact – sonst laufen die Stände auseinander.
