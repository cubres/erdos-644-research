"""Fresh static solve of a CNF with DRAT proof output (pysat CaDiCaL 1.5.3)."""
import sys, time
from pysat.formula import CNF
from pysat.solvers import Solver
cnf = CNF(from_file=sys.argv[1]); t0 = time.time()
with Solver(name=sys.argv[3] if len(sys.argv) > 3 else 'cadical153', bootstrap_with=cnf.clauses, with_proof=True) as S:
    r = S.solve(); print('SAT' if r else 'UNSAT', round(time.time()-t0,1), flush=True)
    if not r:
        with open(sys.argv[2], 'w') as f:
            for line in S.get_proof(): f.write(line + '\n')
print('written', round(time.time()-t0,1))
