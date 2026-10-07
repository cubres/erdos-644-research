#!/bin/bash
cd "$(dirname "$0")"
nohup python3 rr_climb.py 1 45000 1 4 > rr_1_4.log 2>&1 &
nohup python3 rr_climb.py 2 45000 1 6 > rr_1_6.log 2>&1 &
nohup python3 rr_climb.py 3 45000 2 6 > rr_2_6.log 2>&1 &
