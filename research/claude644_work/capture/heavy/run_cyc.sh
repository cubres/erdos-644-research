#!/bin/bash
cd "$(dirname "$0")"
nohup python3 cyc_climb.py 1 15000 1 6 > cyc_k1.log 2>&1 &
nohup python3 cyc_climb.py 2 15000 2 6 > cyc_k2.log 2>&1 &
nohup python3 cyc_climb.py 3 15000 3 5 > cyc_k3.log 2>&1 &
