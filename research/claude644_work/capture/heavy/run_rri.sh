#!/bin/bash
cd "$(dirname "$0")"
nohup python3 rr_inter_climb.py 1 20000 1 4 4 > rri_1_4.log 2>&1 &
nohup python3 rr_inter_climb.py 2 20000 1 6 4 > rri_1_6.log 2>&1 &
nohup python3 rr_inter_climb.py 3 20000 2 6 4 > rri_2_6.log 2>&1 &
