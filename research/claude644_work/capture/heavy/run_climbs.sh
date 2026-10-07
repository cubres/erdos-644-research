#!/bin/bash
cd "$(dirname "$0")"
nohup python3 h3red_climb.py 3 3 6 1 > climb_red_3_3.log 2>&1 &
nohup python3 h3red_climb.py 3 4 6 2 > climb_red_3_4.log 2>&1 &
nohup python3 h3red_climb.py 3 5 5 3 > climb_red_3_5.log 2>&1 &
nohup python3 h3red_climb.py 3 6 4 4 > climb_red_3_6.log 2>&1 &
nohup python3 h3red_climb.py 4 4 5 5 > climb_red_4_4.log 2>&1 &
nohup python3 h3red_climb.py 4 6 4 6 > climb_red_4_6.log 2>&1 &
nohup python3 h3red_climb.py 3 4 6 7 1 > climb_sum1_3_4.log 2>&1 &
nohup python3 h3red_climb.py 3 6 4 8 1 > climb_sum1_3_6.log 2>&1 &
