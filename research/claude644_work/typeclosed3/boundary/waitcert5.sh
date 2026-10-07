#!/bin/zsh
T=${1:-570}
S0=$(cat cx5_*.log 2>/dev/null | grep -cE "CERTIFIED|STOP|NO escape|Traceback")
for i in $(seq 1 $T); do
  S1=$(cat cx5_*.log 2>/dev/null | grep -cE "CERTIFIED|STOP|NO escape|Traceback")
  if [ "$S1" != "$S0" ]; then break; fi
  sleep 1
done
for f in cx5_*.log; do echo "== $f: adv=$(grep -c adversary $f) | $(grep -E 'nodes|CERTIFIED|STOP' $f | tail -1 | cut -c1-120)"; done
date
