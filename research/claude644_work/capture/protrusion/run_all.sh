#!/bin/bash
# usage: run_all.sh budgets mlist outfile
B=$1; ML=$2; OUT=$3
: > $OUT
while read -r line; do
  row=""
  for m in $ML; do v=$(./game "$line" $B $m | sed 's/.*value=\([0-9]*\).*/\1/'); row="$row $v"; done
  echo "$row | $line" >> $OUT
done < orders.txt
