#!/bin/bash
cd "$(dirname "$0")"
( for s in $(seq 300 311); do python3 fp3_climb.py $s 40000 3; done > fp3_p3.log 2>&1 ) &
( for s in $(seq 400 407); do python3 fp3_climb.py $s 40000 4; done > fp3_p4.log 2>&1 ) &
