#!/bin/bash
cd "$(dirname "$0")"
nohup python3 rr_inter_climb.py 11 20000 1 8 3 > rri_1_8.log 2>&1 &
nohup python3 rr_inter_climb.py 12 20000 1 10 3 > rri_1_10.log 2>&1 &
nohup python3 rr_inter_climb.py 13 20000 0 6 3 > rri_0_6.log 2>&1 &
