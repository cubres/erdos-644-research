#!/bin/bash
cd "$(dirname "$0")"
nohup python3 fp_general_climb.py 11 45000 2 5 3 > fpg_W5.log 2>&1 &
nohup python3 fp_general_climb.py 12 45000 2 6 3 > fpg_W6.log 2>&1 &
nohup python3 fp_general_climb.py 13 45000 1 5 3 > fpg_r5.log 2>&1 &
nohup python3 fp_general_climb.py 14 30000 1 6 4 > fpg_r6p4.log 2>&1 &
