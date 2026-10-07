#!/bin/zsh
# wait until a cx4 log reports CERTIFIED / STOP / NO escape (new occurrence) or timeout seconds; then summarise
T=${1:-1200}
S0=$(cat cx4_*.log 2>/dev/null | grep -cE "CERTIFIED|STOP|NO escape")
for i in $(seq 1 $T); do
  S1=$(cat cx4_*.log 2>/dev/null | grep -cE "CERTIFIED|STOP|NO escape")
  if [ "$S1" != "$S0" ]; then break; fi
  sleep 1
done
for f in cx4_*.log; do echo "== $f: $(grep -E 'round|CERT|STOP|NO escape' $f | tail -1 | cut -c1-140)"; done
date
