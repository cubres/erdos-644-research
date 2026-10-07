#!/bin/zsh
# wait until any cx4 log changes (or timeout seconds), then print the last lines
T=${1:-600}
S0=$(cat cx4_*.log 2>/dev/null | wc -l)
for i in $(seq 1 $T); do
  S1=$(cat cx4_*.log 2>/dev/null | wc -l)
  if [ "$S1" != "$S0" ]; then break; fi
  sleep 1
done
for f in cx4_*.log; do echo "== $f: $(grep -E 'round|CERT|STOP' $f | tail -1 | cut -c1-140)"; done
date
