#!/bin/bash
# usage: launch.sh <tags> <name> [key=value...]   (runs bal_run.py in background, log in logs_caseA/<name>.log)
cd /Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/
nohup python3 bal_run.py "$@" > logs_caseA/$2.log 2>&1 &
echo started $2 pid $!
