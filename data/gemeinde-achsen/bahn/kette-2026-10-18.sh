#!/usr/bin/env bash
# Kette 2026-10-18: Essen um Heisingen 418–431 in zwei Blöcken nacheinander (Mike 18.10.: beide Ringe, 2 Blöcke).
# Je Block nacht-2026-10-06.sh mit eigenem Log; Block 2 startet erst nach „Fertig“ von Block 1.
# Start losgelöst (PowerShell Start-Process), Gesamtlog: kette-2026-10-18.log, letzte Zeile „Fertig“.
B=/d/claude-code/LernApp/data/gemeinde-achsen/bahn
export PATH=/usr/bin:$PATH
BLOCK1="418-kupferdreh 419-ueberruhr 420-bergerhausen 421-rellinghausen 422-stadtwald-essen 423-fischlaken 424-werden 425-burgaltendorf"
BLOCK2="426-steele 427-byfang 428-ruettenscheid 429-bredeney 430-huttrop 431-kettwig"
for i in 1 2; do
  eval "N=\$BLOCK$i"
  LOG=$B/lauf-2026-10-18-teil48-essen$i.log
  echo "== Block $i $(date +%T): $N"
  /usr/bin/bash $B/nacht-2026-10-06.sh $N > "$LOG" 2>&1
  tail -3 "$LOG"
  if ! tail -3 "$LOG" | grep -q '^Fertig [0-9]'; then echo "Block $i ohne sauberes Fertig – Kette hält an $(date +%T)"; echo "Fertig mit Abbruch $(date +%T)"; exit 1; fi
done
echo "Fertig $(date +%T)"
