#!/bin/zsh
# run boxes from a list with at most NP parallel jobs
list=$1; NP=$2; TL=$3; prefix=$4
cd /Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c
while read lo hi; do
  tag=${prefix}_$(echo $lo | tr ',/' '_d')
  if grep -q "^$tag " summary_$prefix.txt 2>/dev/null; then continue; fi
  while [ $(pgrep -f boxrun3.py | wc -l) -ge $NP ]; do sleep 5; done
  (python3 -u boxrun3.py $lo $hi 6 3 $TL $tag >> summary_$prefix.txt 2>> err_$prefix.txt &)
  sleep 1
done < $list
