#!/bin/zsh
# usage: verify3.sh KEY   (KEY = b3_... ; files in logs/astra_continuous_type_cells/)
# 1) exact input audit  2) fresh glucose4 DRAT proof  3) drat-trim (-L LRAT)  4) std-lib LRAT RUP replay
B=logs/astra_continuous_type_cells/$1
python3 -B box3_check.py $B > $B.audit.txt 2>&1
python3 solve_proof.py $B.cnf $B.drat glucose4 > $B.solve.txt 2>&1
../tools/drat-trim $B.cnf $B.drat -L $B.lrat -t 50000 > $B.dtrim.txt 2>&1
rm -f $B.drat
python3 -B p644_lrat_rup_check.py $B.cnf $B.lrat > $B.lratcheck.txt 2>&1
rm -f $B.lrat
echo "$1 | $(tail -1 $B.audit.txt | cut -c1-30) | $(head -1 $B.solve.txt) | $(tr '\r' '\n' < $B.dtrim.txt | grep -a '^s ' | tail -1) | $(tail -1 $B.lratcheck.txt | cut -c1-60)" >> verify3_summary.txt
