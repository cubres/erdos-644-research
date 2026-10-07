#!/bin/zsh
# certify + check every tree in trees7 without a certificate
cd /Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c
for t in trees7/*.json; do
  b=$(basename $t)
  if [ -e certs7/$b ]; then continue; fi
  python3 certify5.py $t certs7/$b >> logs_cert7.log 2>&1 && python3 check5.py certs7/$b >> logs_check7.log 2>&1 || echo "FAILED $b" >> logs_check7.log
done
