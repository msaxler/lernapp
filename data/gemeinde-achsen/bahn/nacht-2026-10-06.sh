#!/usr/bin/env bash
# Nachtlauf 2026-10-06: 10 Orte Renchen + Rheinbahn Rastatt–Mannheim + Ladenburg (Quellen und Grunddaten liegen schon).
# Extraktion Haiku, alle weiteren Stufen Opus 5.5 (Mike 06.10.: kein Sonnet). Danach geprüfte Fassung und Export in
# den Prototyp (ohne Modell); das Artifact veröffentlicht Claude in der nächsten Session.
# Start losgelöst (PowerShell), Log: data/gemeinde-achsen/bahn/nacht-2026-10-06.log; letzte Zeile „Fertig“.
cd /d/claude-code/LernApp || exit 1
export GA_RAUM=bahn GA_PROMPT_KARTEN=prompt-karten-v0.8.1.txt GA_PROMPT_PRUEFUNG=prompt-pruefung-v0.2.txt
M=claude-opus-5-5
N="32-renchen 33-durmersheim 34-karlsruhe 35-stutensee 36-graben-neudorf 37-waghaeusel 38-hockenheim 39-schwetzingen 40-mannheim 41-ladenburg"
D=scripts/data-build/gemeinde_achsen_direkt.py
echo "== Extraktion (Haiku) $(date +%T)"
python -X utf8 $D extraktion --model haiku --parallel 5 $N
python -X utf8 scripts/data-build/gemeinde_achsen_fakten.py | tail -1
GA_EINGABE=eingabe-v0.8 python -X utf8 scripts/data-build/gemeinde_achsen_karten_eingabe.py $N | grep Zeichen
echo "== Karten ($M) $(date +%T)"
python -X utf8 $D karten --model $M --parallel 5 $N
echo "== Prüfstufe 1 ($M) $(date +%T)"
python -X utf8 $D pruefung --model $M --parallel 5 $N
echo "== Stufe 2 ($M) $(date +%T)"
python -X utf8 $D stufe2 --model $M --parallel 5 $N
echo "== Geprüfte Fassung und Export $(date +%T)"
python -X utf8 scripts/data-build/gemeinde_achsen_bahn_geprueft.py
python -X utf8 scripts/data-build/quizaway_prototyp_export.py | tail -4
python -X utf8 -c "
import json,glob
s=0
for f in glob.glob('data/gemeinde-achsen/bahn/aufwand/*-3[2-9]-*.json')+glob.glob('data/gemeinde-achsen/bahn/aufwand/*-4[01]-*.json'):
  s+=json.load(open(f,encoding='utf-8')).get('kosten_usd') or 0
print('Kosten 10 Orte: %.2f USD' % s)"
echo "Fertig $(date +%T)"
