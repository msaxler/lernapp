#!/usr/bin/env bash
# Vertiefung Freiburg, voller Lauf (Mike 2026-10-27: „voller Lauf über die 11 Stadtteile mit genug Material, und eine zweite
# Altstadt-Runde“). Nacheinander, nie zwei Läufe zugleich. Zahl der neuen Karten nach Umfang der neuen Quellen.
# 14:00 brach Runde tief bei der Eingabe ab (slug=N verlor den Ort); Altstadt tief2 lief 14:05–14:19 durch. 14:20 Neustart nur tief.
cd /d/claude-code/LernApp/data/gemeinde-achsen/bahn || exit 1
echo "== Runde tief: 11 Stadtteile $(date +%T)"
GA_TIEF=tief bash vertiefung-lauf.sh 449-bruehl-freiburg=6 451-haslach-freiburg=6 452-sankt-georgen=6 446-neuburg-freiburg=5 \
  447-herdern=5 450-oberau=4 455-betzenhausen=4 463-munzingen=4 457-landwasser=3 440-waldsee=3 454-weingarten-freiburg=3
echo "Fertig Kette $(date +%T)"
