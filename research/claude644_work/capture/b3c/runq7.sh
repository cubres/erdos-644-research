#!/bin/zsh
# run boxes from a list with at most NP parallel jobs (search6 engine, CPU-time limit TL)
list=$1; NP=$2; TL=$3; prefix=$4
cd /Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c
while read lo hi; do
  tag=${prefix}_$(echo $lo | tr ',/' '_d')
  if [ -e s2logs/${tag}.out ]; then continue; fi
  while [ $(pgrep -f boxrun7.py | wc -l) -ge $NP ]; do sleep 5; done
  ( python3 -u boxrun7.py $lo $hi 6 3 $TL $tag -v > s2logs/${tag}.out 2>&1; tail -1 s2logs/${tag}.out >> summary_$prefix.txt ) &
  sleep 2
done < $list
