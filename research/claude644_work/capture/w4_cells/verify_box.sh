#!/bin/zsh
# usage: verify_box.sh BASE   (BASE = logs/astra_continuous_type_cells/<key> without extension)
# 1) exact input audit  2) fresh glucose4 DRAT proof  3) drat-trim verification (+LRAT)  4) cleanup
B=$1
python3 -B gql_box_check.py $B > $B.audit.txt 2>&1
python3 solve_proof.py $B.cnf $B.drat glucose4 > $B.solve.txt 2>&1
../tools/drat-trim $B.cnf $B.drat -t 50000 > $B.dtrim.txt 2>&1
rm -f $B.drat
echo "$(basename $B) | $(tail -1 $B.audit.txt | cut -c1-40) | $(head -1 $B.solve.txt) | $(grep '^s ' $B.dtrim.txt)" >> verify_summary.txt
