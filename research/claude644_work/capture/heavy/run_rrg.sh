#!/bin/bash
cd "$(dirname "$0")"
nohup python3 rr_inter_G.py 21 20000 1 4 3 > rrg_1_4.log 2>&1 &
nohup python3 rr_inter_G.py 22 20000 1 6 3 > rrg_1_6.log 2>&1 &
nohup python3 rr_inter_G.py 23 20000 1 8 3 > rrg_1_8.log 2>&1 &
