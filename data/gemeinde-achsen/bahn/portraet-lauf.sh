#!/usr/bin/env bash
# Ortsporträt-Kette (seit 2026-10-19, Mike: Qualität zuerst): je Ort OSM-Zeugen, Gemeinde-Webseite (erweiterte Suche),
# Extraktion v0.7 (Haiku), Eingabe v0.9, Karten v0.9 (Opus 5.5), Prüfstufe 1 und 2 (Opus 5.5), Tag "portraet".
# Voraussetzung: Ort in orte.json, Wikipedia-Quelle (gemeinde_achsen_quellen.py) und Grunddaten liegen vor.
# Danach von Hand: GA_LAUF=v0.9 GA_TAG=-portraet gemeinde_achsen_bahn_geprueft.py, Export, Artifact, Pages.
# Aufruf losgelöst: portraet-lauf-start.ps1 -Orte "<slugs>" -Name <logname>
cd /d/claude-code/LernApp || exit 1
export GA_RAUM=bahn GA_PORTRAET=1 GA_EINGABE=eingabe-v0.9 GA_PROMPT_EXTRAKTION=prompt-stufe1-v0.7.txt \
       GA_PROMPT_KARTEN=prompt-karten-v0.9.txt GA_PROMPT_PRUEFUNG=prompt-pruefung-v0.2.txt
N="$*"
[ -n "$N" ] || { echo "keine Orte"; exit 1; }
D=scripts/data-build/gemeinde_achsen_direkt.py
M=claude-opus-5-5
echo "Orte: $N"
# GA_OSM_FERTIG=1: Zeugen wurden vorab geholt (2026-10-27: Overpass so langsam, dass sie parallel vorab liefen)
if [ "$GA_OSM_FERTIG" = 1 ]; then echo "== OSM-Zeugen übersprungen (vorab geholt) $(date +%T)"; else
echo "== OSM-Zeugen $(date +%T)"
python -X utf8 scripts/data-fetch/gemeinde_achsen_osm.py $N
fi
echo "== Gemeinde-Webseiten $(date +%T)"
python -X utf8 scripts/data-fetch/gemeinde_achsen_quellen_amtlich.py $N | tail -n +1
echo "== Extraktion v0.7 (Haiku) $(date +%T)"
python -X utf8 $D extraktion --model haiku --parallel 3 $N
python -X utf8 scripts/data-build/gemeinde_achsen_fakten.py | tail -1
echo "== Eingabe v0.9 $(date +%T)"
python -X utf8 scripts/data-build/gemeinde_achsen_karten_eingabe.py $N | grep Zeichen
for s in $N; do
  [ -f data/gemeinde-achsen/bahn/eingabe-v0.9/$s.txt ] || { echo "ABBRUCH: keine Eingabe für $s"; echo "Fertig mit Abbruch $(date +%T)"; exit 1; }
done
echo "== Karten v0.9 ($M) $(date +%T)"
python -X utf8 $D karten --model $M --parallel 3 --tag portraet $N
echo "== Prüfstufe 1 ($M) $(date +%T)"
python -X utf8 $D pruefung --model $M --parallel 3 --tag portraet $N
echo "== Stufe 2 ($M) $(date +%T)"
python -X utf8 $D stufe2 --model $M --parallel 3 --tag portraet $N
echo "Fertig $(date +%T)"
