#!/bin/bash
cd "$(dirname "$0")"
for k in 0 1 2 3; do
  ( for s in $(seq $((100+k*10)) $((109+k*10))); do python3 otp3_climb.py $s 60000 1; done > otp3_sum1_$k.log 2>&1 ) &
done
( for s in $(seq 200 209); do python3 otp3_climb.py $s 60000 0; done > otp3_sub.log 2>&1 ) &
