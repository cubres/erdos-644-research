#!/bin/bash
cd "$(dirname "$0")"
nohup python3 fp_batch.py 1 20 8 3 > fp_b1_N20.log 2>&1 &
nohup python3 fp_batch.py 2 16 20 3 > fp_b2_N16.log 2>&1 &
nohup python3 fp_batch.py 3 12 12 4 > fp_b3_N12_p4.log 2>&1 &
