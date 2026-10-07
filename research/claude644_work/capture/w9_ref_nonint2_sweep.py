"""Referee w9 [nonint#2]: sweep of w9_ref_nonint2_sat.decide over instances satisfying the (corrected) conditions,
and over literal-condition degenerate instances (c<=delta) which must be BAD. Usage: python3 w9_ref_nonint2_sweep.py kmin kmax [dmin]"""
import sys, time
from w9_ref_nonint2_conds import conds
from w9_ref_nonint2_sat import decide
kmin, kmax = int(sys.argv[1]), int(sys.argv[2]); dmin = int(sys.argv[3]) if len(sys.argv) > 3 else 1
for k in range(kmin, kmax+1):
    for s in range(k):
        for c in range(k+1):
            for d in range(dmin, k):
                if not conds(k, s, c, d): continue
                t0 = time.time(); ok, res = decide(k, s, c, d)
                kind = 'corrected' if c >= d+1 else 'DEGENERATE(c<=d)'
                print(f'{kind} k={k} s={s} c={c} d={d}: {"HOLDS" if ok else "BAD "+str(res[-1][0])} [{time.time()-t0:.1f}s]', flush=True)
