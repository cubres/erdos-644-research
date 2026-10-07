#!/bin/bash
cd "$(dirname "$0")"
( for s in 1 2; do python3 m3menu_climb.py $s 20000 0; done ) > m3_s0.log 2>&1 &
( for s in 3 4; do python3 m3menu_climb.py $s 20000 1; done ) > m3_s1.log 2>&1 &
( for s in 5 6 7; do python3 m3menu_climb.py $s 20000 2; done ) > m3_s2.log 2>&1 &
