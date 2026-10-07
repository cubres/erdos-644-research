#!/bin/bash
cd "$(dirname "$0")"
( for s in 1 2 3 4 5; do python3 atc_minmenu_climb.py $s 20000 4 3; done > atcm_4_3.log 2>&1 ) &
( for s in 6 7 8 9; do python3 atc_minmenu_climb.py $s 20000 6 3; done > atcm_6_3.log 2>&1 ) &
( for s in 10 11 12; do python3 atc_minmenu_climb.py $s 20000 6 4; done > atcm_6_4.log 2>&1 ) &
