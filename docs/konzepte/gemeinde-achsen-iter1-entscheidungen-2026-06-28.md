# Gemeinde-Achsen — Iteration-1-Entscheidungen (Mike, 2026-06-28)

**Status:** Ergänzt das Basiskonzept v0.5 (`gemeinde-achsen-basiskonzept-2026-06-28-v0.5.md`).
Bei Abweichung gilt **diese Notiz** (jünger). Hervorgegangen aus der Claude-Prüfung der
drei Wachpunkte + Mike-Entscheidungen.

**Leitlinie (rahmt alles):** *Es ist Unterhaltung für die lange Fahrt, kein Prüfungswissen.
Fun vor Korrektheit.*

---

## E1 — Canonicalization über Patrozinium-Token (ersetzt §4.7 Schritt 3)

Der „längste gemeinsame Suffix-Match" ist das falsche Werkzeug: das unterscheidende Token
(Patrozinium: *Marien*, *Martin*, *Johannes*) sitzt nicht am Suffix, der generische Typ-Suffix
(`-kirche`, `-kapelle`) schon → Falsch-Merges (Johannes**kirche**/Stephan**skirche**) und
Falsch-Splits (St. Marien ↔ Marienkirche).

**Neues Verfahren (deterministisch, kein ML — bleibt in §14/P8):**
1. Trim, lowercase, Umlaute normalisieren.
2. Präfixe **und generische Typ-Suffixe** strippen (`-kirche/-kapelle/-dom/-münster/-basilika`).
   Das Typwort steckt schon in `typ` → im Identitätsschlüssel führt es zu Doppelzählung + beiden Fehlerarten.
3. Stopwords raus (`st.`, `sankt`, `zur/zum`, `unserer lieben frau`→`marien`) → **Token-Set**.
4. Identität = `ags + typ + sortiertes Token-Set`. Match ⇔ Token-Sets gleich (oder Teilmenge ohne
   widersprechendes Patrozinium).
5. Ties: bounded Levenshtein (≤1–2) **nur auf dem Patrozinium** + `ortsteil_bezug` als Disambiguator (§4.7).
6. Kleiner **Patrozinium-Synonym-Map** (Marien=Maria=Liebfrauen, Michael=Michaelis — Top ~10).

Namenlose Entitäten unverändert über §4.7-Fallback (`material+baujahr+lage_im_ort`).

## E2 — Kein Vertrauens-Gate; eine Quelle genügt

- „Wahr genug zum Behaupten" = **≥1 Quelle existiert.** Kein `min()`-Schwellwert als Laufzeit-Filter
  (es geht um Unterhaltung, nicht um Prüfungswissen).
- **Quiz-Eligibility** nur über `quiz_tauglich` (§4.8) + Diskriminationswert (§7.2) + Aktualitätsfilter (§6.1).
  Damit ist auch die **P6-Spannung gelöst** — kein quellen-abgeleiteter Filter mehr (min() zog die
  Quellen-Identität in den Filter und widersprach „Quizlogik kennt keine Quellen").
- `vertrauen_quelle` / `vertrauen_extraktion` bleiben **informativ** (Kuration, Steckbrief-Anzeige,
  K6-Sanity-Check) — **nicht** als Runtime-Schranke.

## E3 — Quellen sind gleichwertige Peers; Zufallsauswahl; Provenienz im Steckbrief

- **Keine Konfliktauflösung** (die §11.1-Konfliktregel „Wikidata bevorzugt, LLM in `alternativen[]`,
  manuelle Prüfung" entfällt fürs Spiel). Mehrere Werte (LLM 1270 / Wikidata 1268) sind **beide wahr**.
- **Datenmodell:** Provenienz uniform **pro Wert als `quellen[]`** — gleichwertige **Peers**, KEINE
  Hauptquelle+`alternativen[]`. Macht die §4.12-`sources[]`-Evolution zum No-op (Listen-Form ist ab Iter 1 da,
  weil §11 Wikidata parallel zur LLM-Extraktion fährt → fast jede Instanz hat sofort ≥2 Quellen).
- **Laufzeit:** **Zufallsauswahl** der Quelle/des Werts pro Frage (Fun zuerst).
- **Steckbrief** (User-facing, analog MixMi! `SteckbriefModal`): zeigt den Fakt **mit Quellenangabe(n)**.
  Provenienz ist damit Feature, nicht nur Debug.
- **Grenze (wichtig):** Zufalls-Quellenwahl gilt nur für *gleichwertig gültige* Werte. **Zeitabhängige
  0..1-Fakten** (Bürgermeister, Wahl) laufen weiter durch den **Aktualitätsfilter** (§6.1) + K6 — kein
  Würfeln zwischen aktuellem und Ex-Bürgermeister.

## Brücke zu „MixMi! iter7a als Basis"

`SteckbriefModal.tsx` aus MixMi! (i-Button, Voll-Overlay, 180°-Auto-Orientierung) ist die direkte
Vorlage für den QuizAway-Steckbrief — konkreter Beleg für die Architektur-Übernahme (B1/B2).

---

*Diese Notiz ist Teil des QuizAway-Bereichs (`apps/quizaway/STATUS.md` verweist darauf). DB-Aufbau
läuft parallel zum QuizAway-Neubau (LA-3) + p2p-tele.*
