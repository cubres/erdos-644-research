#!/bin/bash
cd "$(dirname "$0")"
for cfg in "21 3 1 1 40 20000 6" "22 4 1 1 40 20000 6" "23 3 2 1 40 15000 5" "24 4 1 2 40 15000 5" "25 4 2 2 40 8000 4" "26 5 1 2 40 8000 4" "27 3 1 2 40 20000 6" "28 5 2 1 40 6000 4"; do
  python3 w5_dense_nonuniform_climb.py $cfg > w5_dense_nu_${cfg// /_}.log 2>&1 &
done
wait
