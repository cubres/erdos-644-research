#!/bin/bash
cd "$(dirname "$0")"
for cfg in "31 1 1 40 15000 14" "32 1 2 40 15000 14" "33 1 3 40 15000 14" "34 2 1 40 15000 14" "35 2 2 40 15000 14" "36 1 2 32 15000 18" "37 2 2 32 15000 18" "38 3 1 40 15000 14"; do
  python3 w5_dense_milp_climb.py $cfg > w5_dense_milpclimb_${cfg// /_}.log 2>&1 &
done
wait
