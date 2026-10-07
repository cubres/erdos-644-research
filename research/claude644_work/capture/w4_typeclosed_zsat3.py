"""Z-encoding driver v3 = v1 (plain all-support MILP on minimal true corners) + greedy grid
enlargement of every row bound (fixed cell downset) -> stronger learned clauses.  Learned rows are
saved (as enlarged integer load vectors) for the exact audit w4_typeclosed_zaudit.py.
usage: python3 w4_typeclosed_zsat3.py D X1,..,Xp [T]"""
import sys, time, json
from fractions import Fraction as F
from pysat.solvers import Solver
from w4_typeclosed_lib import bad_tuple_milp
from w4_typeclosed_zsat import build, minimal_true_corners
from w4_typeclosed_zsat2 import downset, feasible

def enlarge_rows(rows, cells, X):
    p = len(X); xs = [float(v) for v in X]; cur = [list(r) for r in rows]
    def loads(): return [[cur[j][i] for j in range(7)] for i in range(p)]
    if not feasible(loads(), cells, xs): return [tuple(r) for r in rows]
    for j in range(7):
        for i in range(p):
            lo, hi = cur[j][i], X[i]
            while lo < hi:
                mid = (lo + hi + 1)//2; old = cur[j][i]; cur[j][i] = mid
                ok = feasible([ [cur[jj][ii] for jj in range(7)] for ii in [i] ], cells, [xs[i]])
                cur[j][i] = old
                if ok: lo = mid
                else: hi = mid - 1
            cur[j][i] = lo
    return [tuple(r) for r in cur]

def run(D, X, T=None, maxiter=100000):
    p = len(X); t0 = time.time()
    pts, vid, clauses, corners, npair, T = build(D, X, T)
    print(f'D={D} X={X} T={T}: {len(pts)} vars, {len(clauses)} clauses ({npair} pair) {time.time()-t0:.1f}s', flush=True)
    S = Solver(name='cadical153', bootstrap_with=clauses)
    learned = []; out = f'w4_tc_zsat3_{D}_{"_".join(map(str,X))}_T{T}.json'
    for it in range(maxiter):
        if not S.solve():
            json.dump({'D': D, 'X': X, 'T': T, 'learned': learned}, open(out, 'w'))
            return {'status': 'UNSAT', 'iter': it, 'learned': len(learned), 'sec': round(time.time()-t0, 1)}
        model = set(v for v in S.get_model() if v > 0)
        cs = minimal_true_corners(model, pts, vid, D, p)
        st, assign, cells = bad_tuple_milp([tuple(F(v, D) for v in u) for u in cs], [F(v, D) for v in X], time_limit=120)
        if st != 'BAD':
            json.dump({'D': D, 'X': X, 'T': T, 'learned': learned, 'corners': cs}, open(out, 'w'))
            return {'status': 'SAT_RELAXATION' if st == 'NONE' else 'UNKNOWN', 'corners': cs, 'iter': it, 'learned': len(learned)}
        rows = [cs[j] for j in assign]
        used = downset(set(Sx for (i, Sx), v in cells.items() if v > 1e-9))
        big = enlarge_rows(rows, used, X)
        big = [b for b in big]
        lits = sorted(set(-vid[b] for b in big))
        S.add_clause(lits); learned.append({'rows': [list(b) for b in big]})
        if len(learned) % 10 == 0:
            print(f'  it {it}: corners {len(cs)} learned {len(learned)} lits {len(lits)} ({time.time()-t0:.0f}s)', flush=True)
            json.dump({'D': D, 'X': X, 'T': T, 'learned': learned, 'partial': True}, open(out, 'w'))
    return {'status': 'MAXITER'}

if __name__ == '__main__':
    D = int(sys.argv[1]); X = [int(v) for v in sys.argv[2].split(',')]
    T = int(sys.argv[3]) if len(sys.argv) > 3 else None
    print(json.dumps(run(D, X, T), default=str))
