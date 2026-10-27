#!/usr/bin/env bash
# Kette 2026-10-26: wartet, bis der Ortsporträt-Lauf Essen (portraet-2026-10-26-essen2.log) mit „Fertig“ endet, und startet dann
# die Autostrecke Neuwied–Heisingen (35 Orte). Bei „Fertig mit Abbruch“ startet nichts. Nie zwei Läufe gleichzeitig.
B=/d/claude-code/LernApp/data/gemeinde-achsen/bahn
until tail -1 $B/portraet-2026-10-26-essen2.log | grep -q '^Fertig'; do sleep 60; done
if tail -1 $B/portraet-2026-10-26-essen2.log | grep -q 'Abbruch'; then echo "Essen-Lauf abgebrochen – Strecke nicht gestartet"; echo "Fertig mit Abbruch $(date +%T)"; exit 1; fi
echo "Essen fertig $(date +%T), Strecke startet"
/usr/bin/bash $B/portraet-lauf.sh 496-neuwied 140-weissenthurm 404-niederbieber 405-segendorf 497-altwied 408-oberbieber 498-rengsdorf \
  409-melsbach 411-ehlscheid 412-kurtscheid 410-hardert 499-bonefeld 500-strassenhaus 501-oberhonnefeld-gierend 502-willroth \
  503-horhausen 504-huemmerich 505-krunkel 415-breitscheid-westerwald 413-rossbach-wied 340-neustadt-wied 342-vettelschoss \
  341-windhagen 344-hennef 346-siegburg 347-lohmar 348-roesrath 193-leverkusen 349-leichlingen 194-langenfeld 351-hilden \
  352-haan 355-wuelfrath 357-velbert 353-erkrath
