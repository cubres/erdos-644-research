#!/bin/bash
cd "$(dirname "$0")"
for cfg in "11 20000 24 4" "12 20000 40 4" "13 20000 60 4" "14 20000 32 4"; do
  python3 w5_dense_twopart_theorem_check2.py $cfg > w5_dense_check2_${cfg// /_}.log 2>&1 &
done
wait
