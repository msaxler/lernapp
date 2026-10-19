#!/usr/bin/env bash
# Prüfstufen 1 und 2 für die Ortsporträt-Karten (Tag portraet): Breitnau, Kirchzarten. Opus 5.5, Prompts v0.2 / stufe2 v0.1.
cd /d/claude-code/LernApp || exit 1
export GA_RAUM=bahn GA_PORTRAET=1 GA_EINGABE=eingabe-v0.9 GA_PROMPT_KARTEN=prompt-karten-v0.9.txt GA_PROMPT_PRUEFUNG=prompt-pruefung-v0.2.txt
N="${*:-432-breitnau 433-kirchzarten}"
D=scripts/data-build/gemeinde_achsen_direkt.py
M=claude-opus-5-5
echo "Orte: $N"
echo "== Prüfstufe 1 ($M) $(date +%T)"
python -X utf8 $D pruefung --model $M --parallel 2 --tag portraet $N
echo "== Stufe 2 ($M) $(date +%T)"
python -X utf8 $D stufe2 --model $M --parallel 2 --tag portraet $N
echo "Fertig $(date +%T)"
