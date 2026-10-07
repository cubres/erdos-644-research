#!/bin/zsh
# tally certificate status of every *.cnf with audit/dtrim files
cd logs/astra_continuous_type_cells
for c in *.cnf; do b=${c%.cnf}; a=$( [ -f $b.audit.txt ] && tail -1 $b.audit.txt | cut -c1-5 || echo "-"); d=$( [ -f $b.dtrim.txt ] && (grep -o 's VERIFIED\|s NOT VERIFIED' $b.dtrim.txt | tail -1) || echo "-"); echo "$b | $a | $d"; done
