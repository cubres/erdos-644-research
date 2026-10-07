#!/bin/bash
cd "$(dirname "$0")"
nohup python3 h2_climb.py 1 4 6 1 > h2c_1_4.log 2>&1 &
nohup python3 h2_climb.py 1 5 6 2 > h2c_1_5.log 2>&1 &
nohup python3 h2_climb.py 1 6 5 3 > h2c_1_6.log 2>&1 &
nohup python3 h2_climb.py 2 5 5 4 > h2c_2_5.log 2>&1 &
