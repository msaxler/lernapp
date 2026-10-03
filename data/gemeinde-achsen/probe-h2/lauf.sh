#!/usr/bin/env bash
# Probe H2: Kartenlauf als direkter, isolierter Aufruf (claude -p ohne Werkzeuge, ohne Projektgedächtnis).
# Gleicher Prompt (prompt-karten-v0.7.txt) und gleiche Eingabe wie der Agentenlauf v0.7.
export CLAUDE_CODE_GIT_BASH_PATH="D:\\Programme\\Git\\bin\\bash.exe"
unset ANTHROPIC_BASE_URL CLAUDECODE CLAUDE_CODE_SESSION_ID CLAUDE_CODE_HOST_SESSION_ID CLAUDE_CODE_CHILD_SESSION \
      CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH CLAUDE_CODE_SDK_HAS_OAUTH_REFRESH CLAUDE_CODE_ENTRYPOINT CLAUDE_AGENT_SDK_VERSION
for v in $(env | grep -o '^CLAUDE_CODE_[A-Z_]*' | grep -v GIT_BASH_PATH); do unset "$v"; done
cd "$(dirname "$0")"
GA="D:/claude-code/LernApp/data/gemeinde-achsen"
for ort in "iter1 09-horben" "neuwied 07-waldbreitbach"; do
  set -- $ort
  {
    echo "Du bekommst eine Anleitung und eine Eingabe. Schreibe die Karten genau nach der Anleitung. Gib nur die Ausgabe im verlangten Format zurück, ohne Vorrede."
    echo; echo "=== ANLEITUNG ==="; cat "$GA/iter1/prompt-karten-v0.7.txt"
    echo; echo "=== EINGABE ==="; cat "$GA/$1/eingabe-v0.7/$2.txt"
  } > "eingabe-$2.txt"
  start=$(date +%s)
  claude -p --model opus --output-format json --disallowedTools "Bash,Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Agent,Task,NotebookEdit,TodoWrite" \
    < "eingabe-$2.txt" > "antwort-$2.json" 2> "fehler-$2.txt" &
  echo "$2 gestartet um $start"
done
wait
for f in antwort-*.json; do echo "== $f"; python -X utf8 -c "
import json,sys
d=json.load(open('$f',encoding='utf-8'))
print('fehler:',d.get('is_error'),'| dauer s:',round(d.get('duration_ms',0)/1000),'| kosten USD:',d.get('total_cost_usd'))
print('usage:',json.dumps(d.get('usage',{})))
open('$f'.replace('antwort-','karten-').replace('.json','.md'),'w',encoding='utf-8').write(d.get('result',''))
"; done
