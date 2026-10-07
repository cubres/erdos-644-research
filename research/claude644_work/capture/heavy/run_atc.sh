#!/bin/bash
cd "$(dirname "$0")"
( for s in 1 2 3 4; do python3 atc_climb.py $s 30000 3 3; done > atc_3_3.log 2>&1 ) &
( for s in 5 6 7; do python3 atc_climb.py $s 30000 5 3; done > atc_5_3.log 2>&1 ) &
