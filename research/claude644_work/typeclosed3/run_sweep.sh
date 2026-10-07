#!/bin/bash
cd /Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/
for s in mb mbL; do for k in 0 1 2 3 4; do
  python3 adv_dfs.py strategies/sw_${s}_band$k.json 0 sw_${s}_band$k budget=20000 >> logs_caseA/sweep_weak.log 2>&1
done; done
echo SWEEPDONE >> logs_caseA/sweep_weak.log
