python3 solve_proof.py $B.cnf $B.drat glucose4 > /dev/null 2>&1
../tools/drat-trim $B.cnf $B.drat -L $B.lrat -t 50000 > /dev/null 2>&1
rm -f $B.drat
python3 -B p644_lrat_rup_check.py $B.cnf $B.lrat > lrat_spot_32.log 2>&1
rm -f $B.lrat
