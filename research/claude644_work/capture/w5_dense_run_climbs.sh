#!/bin/bash
cd "$(dirname "$0")"
for cfg in "11 2 2 40 20000 6" "12 3 2 40 20000 6" "13 3 3 40 20000 6" "14 4 3 40 15000 5" "15 4 4 40 10000 5" "16 5 3 40 8000 4" "17 3 4 40 15000 5" "18 5 4 32 6000 4"; do
  python3 w5_dense_anchor_climb.py $cfg > w5_dense_climb_${cfg// /_}.log 2>&1 &
done
wait
