#!/bin/bash
# usage: run_gc.sh <strategy name> <pi0> [extra args]   -> logs_caseA/gc_<name>_<pi0>.log
cd /Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/
n=$(echo $2 | tr '/' '_')
nohup python3 gen_cert2.py strategies/$1.json $2 "${@:3}" > logs_caseA/gc_$1_$n.log 2>&1 &
echo started $1 $2 pid $!
