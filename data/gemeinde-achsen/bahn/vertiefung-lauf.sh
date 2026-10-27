#!/usr/bin/env bash
# Vertiefung (Freiburg, Mike 2026-10-27): zusätzliche Karten zu Orten mit Ortsporträt-Karten (v0.9) aus quellen-vertiefung/.
# Je Ort: Extraktion der neuen Quellen (Haiku) → fakten/<slug>-tief.txt, Eingabe eingabe-v0.9-tief (bisherige Karten, PLAN),
# Karten mit Prompt v0.9-tief (Opus 5.5), Prüfstufe 1 und 2 (Opus 5.5), Tag "tief".
# Voraussetzung: freiburg_vertiefung_quellen.py hat quellen-vertiefung/<slug>.txt geschrieben; die Orte haben karten-geprueft/v0.9.
# Danach von Hand: GA_LAUF=v0.9-tief GA_TAG=-tief gemeinde_achsen_bahn_geprueft.py, Export, Artifact, Pages.
# Aufruf losgelöst: portraet-lauf-start.ps1 -Skript vertiefung-lauf.sh -Orte "<slugs> [slug=N]" -Name <logname>
cd /d/claude-code/LernApp || exit 1
# GA_TIEF=tief2: weitere Runde desselben Orts (eigene Quellen-, Fakten-, Eingabe- und Kartendateien; Lauf v0.9-tief2)
export GA_TIEF=${GA_TIEF:-tief}
export GA_RAUM=bahn GA_VERTIEFUNG=1 GA_EINGABE=eingabe-v0.9-$GA_TIEF GA_PROMPT_EXTRAKTION=prompt-stufe1-v0.7.txt \
       GA_PROMPT_KARTEN=prompt-karten-v0.9-tief.txt GA_PROMPT_PRUEFUNG=prompt-pruefung-v0.2.txt
# Angaben „slug=N“ (Zahl der neuen Karten) gehen nur an das Eingabe-Skript
ALLE="$*"
N=$(for a in $ALLE; do echo "${a%%=*}"; done | tr '\n' ' ')
[ -n "$N" ] || { echo "keine Orte"; exit 1; }
D=scripts/data-build/gemeinde_achsen_direkt.py
M=claude-opus-5-5
echo "Orte: $ALLE (Runde $GA_TIEF)"
echo "== Extraktion neue Quellen (Haiku) $(date +%T)"
python -X utf8 $D extraktion --model haiku --parallel 3 $N
python -X utf8 scripts/data-build/gemeinde_achsen_fakten.py | tail -1
echo "== Eingabe v0.9-$GA_TIEF $(date +%T)"
python -X utf8 scripts/data-build/gemeinde_achsen_vertiefung_eingabe.py $ALLE
for s in $N; do
  [ -f data/gemeinde-achsen/bahn/eingabe-v0.9-$GA_TIEF/$s.txt ] || { echo "ABBRUCH: keine Eingabe für $s"; echo "Fertig mit Abbruch $(date +%T)"; exit 1; }
done
echo "== Karten v0.9-tief ($M) $(date +%T)"
python -X utf8 $D karten --model $M --parallel 3 --tag $GA_TIEF $N
echo "== Prüfstufe 1 ($M) $(date +%T)"
python -X utf8 $D pruefung --model $M --parallel 3 --tag $GA_TIEF $N
echo "== Stufe 2 ($M) $(date +%T)"
python -X utf8 $D stufe2 --model $M --parallel 3 --tag $GA_TIEF $N
echo "Fertig $(date +%T)"
