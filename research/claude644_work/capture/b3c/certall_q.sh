#!/bin/zsh
cd /Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c
for f in trees/q_*.json; do
  b=$(basename $f)
  python3 -u certify3.py $f certs_q/$b >> logs_certq.log 2>&1 && python3 -u check3.py certs_q/$b >> logs_checkq.log 2>&1
done
echo ALLDONE >> logs_checkq.log
