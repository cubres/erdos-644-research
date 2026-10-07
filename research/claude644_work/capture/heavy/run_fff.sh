#!/bin/bash
cd "$(dirname "$0")"
( for s in 1 2 3; do python3 fp_from_fanofree.py $s 30000 0 0; done > fff_0.log 2>&1 ) &
( for s in 4 5 6; do python3 fp_from_fanofree.py $s 30000 0 2; done > fff_0x.log 2>&1 ) &
( for s in 7 8 9; do python3 fp_from_fanofree.py $s 30000 1 0; done > fff_1.log 2>&1 ) &
( for s in 10 11; do python3 fp_from_fanofree.py $s 30000 2 2; done > fff_2.log 2>&1 ) &
