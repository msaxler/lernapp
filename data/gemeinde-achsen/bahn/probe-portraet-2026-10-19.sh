#!/usr/bin/env bash
# Probekarten Ortsporträt (Mike 2026-10-19: Qualität zuerst, Strecke Freiburg–Breitnau): Breitnau und Kirchzarten.
# Extraktion Haiku mit Prompt v0.7 (ZEUGEN + Charakteristika), Karten Opus 5.5 mit Prompt v0.9, Tag "portraet"
# (Ausgabe karten-v0.8-portraet/). Noch keine Prüfstufen – erst Mike und Tochter urteilen über die Sorte.
cd /d/claude-code/LernApp || exit 1
export GA_RAUM=bahn GA_PORTRAET=1 GA_EINGABE=eingabe-v0.9 GA_PROMPT_EXTRAKTION=prompt-stufe1-v0.7.txt GA_PROMPT_KARTEN=prompt-karten-v0.9.txt
N="${*:-432-breitnau 433-kirchzarten}"
D=scripts/data-build/gemeinde_achsen_direkt.py
echo "Orte: $N"
echo "== Extraktion v0.7 (Haiku) $(date +%T)"
python -X utf8 $D extraktion --model haiku --parallel 2 $N
python -X utf8 scripts/data-build/gemeinde_achsen_fakten.py | tail -1
echo "== Eingabe v0.9 $(date +%T)"
python -X utf8 scripts/data-build/gemeinde_achsen_karten_eingabe.py $N | grep -E "Zeichen|FACETTE" | head -20
echo "== Karten v0.9 (Opus) $(date +%T)"
python -X utf8 $D karten --model claude-opus-5-5 --parallel 2 --tag portraet $N
echo "Fertig $(date +%T)"
