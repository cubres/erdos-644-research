#!/bin/bash
cd "$(dirname "$0")"
nohup python3 h3s_climb.py 1 60000 0 9 3 > h3s_0_1.log 2>&1 &
nohup python3 h3s_climb.py 2 60000 1 5 3 > h3s_r5_2.log 2>&1 &
nohup python3 h3s_climb.py 3 60000 1 7 3 > h3s_r7_3.log 2>&1 &
nohup python3 h3s_climb.py 4 60000 1 6 4 > h3s_r6p4_4.log 2>&1 &
