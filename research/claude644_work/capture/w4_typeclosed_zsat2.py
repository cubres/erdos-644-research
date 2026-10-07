"""Z-encoding driver v2: learned clauses from REQUEST-augmented MILP (fewer actual rows), with
greedy grid ENLARGEMENT of each actual row's upper bound (stronger clauses).  Discovery; every
learned clause is stored with its support cells, requested-row bounds and enlarged actual bounds so
that an exact audit (w4_typeclosed_zaudit.py) can re-verify it.
usage: python3 w4_typeclosed_zsat2.py D X1,X2,.. [maxiter]
"""
import sys, time, json, itertools
import numpy as np
from fractions import Fraction as F
from pysat.solvers import Solver
from scipy.optimize import linprog
from w4_typeclosed_lib import bad_tuple_milp_req, CELLS
from w4_typeclosed_zsat import build, minimal_true_corners

def downset(cells):
    out = set()
    for S in cells:
        sub = S
        while True:
            out.add(sub)
            if sub == 0: break
            sub = (sub - 1) & S
    out.discard(0)
    return sorted(out)

def feasible(loads_by_part, cells, x):
    """exists y>=0 on cells, sum y <= x_i, sum_{C ni j} y_C >= load_j, per part (LP, float)."""
    for i, loads in enumerate(loads_by_part):
        nc = len(cells)
        A = [[-(1.0 if (C >> j) & 1 else 0.0) for C in cells] for j in range(7)] + [[1.0]*nc]
        b = [-float(l) for l in loads] + [float(x[i])]
        r = linprog(np.zeros(nc), A_ub=A, b_ub=b, bounds=(0, None), method='highs')
        if r.status != 0: return False
    return True

def enlarge(rows_actual, req_bounds, cells, X, D):
    """rows_actual: dict row -> grid vector (ints); req_bounds: dict row -> float vector (units of D).
    Greedily raise actual bounds (grid units) keeping per-part feasibility with fixed cell downset."""
    p = len(X); xs = [float(v) for v in X]
    cur = {j: list(u) for j, u in rows_actual.items()}
    def loads():
        out = []
        for i in range(p):
            l = []
            for j in range(7):
                if j in cur: l.append(cur[j][i])
                else: l.append(req_bounds[j][i])
            out.append(l)
        return out
    assert feasible(loads(), cells, xs)
    for j in sorted(cur):
        for i in range(p):
            lo, hi = cur[j][i], X[i]
            while lo < hi:
                mid = (lo + hi + 1)//2
                old = cur[j][i]; cur[j][i] = mid
                ok = feasible(loads(), cells, xs)
                cur[j][i] = old
                if ok: lo = mid
                else: hi = mid - 1
            cur[j][i] = lo
    return {j: tuple(v) for j, v in cur.items()}

def run(D, X, maxiter=100000, tag='r'):
    p = len(X); t0 = time.time()
    pts, vid, clauses, corners, npair, T = build(D, X)
    print(f'D={D} X={X} T={T}: {len(pts)} vars, {len(clauses)} clauses ({npair} pair) {time.time()-t0:.1f}s', flush=True)
    S = Solver(name='cadical153', bootstrap_with=clauses)
    learned = []
    for it in range(maxiter):
        if not S.solve():
            json.dump({'D': D, 'X': X, 'T': T, 'learned': learned}, open(f'w4_tc_zsat2_{D}_{"_".join(map(str,X))}.json', 'w'))
            return {'status': 'UNSAT', 'iter': it, 'learned': len(learned), 'sec': round(time.time()-t0, 1)}
        model = set(v for v in S.get_model() if v > 0)
        cs = minimal_true_corners(model, pts, vid, D, p)
        rowsF = [tuple(F(v, D) for v in u) for u in cs]
        st, rows, cells = bad_tuple_milp_req(rowsF, [F(v, D) for v in X], F(T, D), time_limit=120)
        if st != 'BAD':
            json.dump({'D': D, 'X': X, 'T': T, 'learned': learned, 'corners': cs}, open(f'w4_tc_zsat2_{D}_{"_".join(map(str,X))}.json', 'w'))
            return {'status': 'SAT_RELAXATION' if st == 'NONE' else 'UNKNOWN', 'corners': cs, 'iter': it, 'learned': len(learned)}
        used_cells = downset(set(S_ for (i, S_), v in cells.items() if v > 1e-9))
        actual = {j: cs[r[1]] for j, r in enumerate(rows) if r[0] == 'type'}
        req = {j: [v*D for v in r[1]] for j, r in enumerate(rows) if r[0] == 'req'}
        try:
            big = enlarge(actual, req, used_cells, X, D)
        except AssertionError:
            big = actual
        lits = sorted(set(-vid[tuple(u)] for u in big.values() if tuple(u) in vid))
        S.add_clause(lits)
        learned.append({'actual': {str(j): list(u) for j, u in big.items()}, 'req': {str(j): v for j, v in req.items()},
                        'cells': used_cells})
        if len(learned) % 10 == 0:
            print(f'  it {it}: corners {len(cs)} learned {len(learned)} last-lits {len(lits)} ({time.time()-t0:.0f}s)', flush=True)
    return {'status': 'MAXITER'}

if __name__ == '__main__':
    D = int(sys.argv[1]); X = [int(v) for v in sys.argv[2].split(',')]
    print(json.dumps(run(D, X), default=str))
