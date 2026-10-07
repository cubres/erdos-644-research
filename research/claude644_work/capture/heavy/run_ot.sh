#!/bin/bash
cd "$(dirname "$0")"
nohup python3 onetype_climb.py 3 8 1 1 0 > ot_3_sum1_m0.log 2>&1 &
nohup python3 onetype_climb.py 3 8 2 0 0 > ot_3_sub_m0.log 2>&1 &
nohup python3 onetype_climb.py 4 6 3 1 0 > ot_4_sum1_m0.log 2>&1 &
nohup python3 onetype_climb.py 3 8 4 1 1 > ot_3_sum1_m1.log 2>&1 &
