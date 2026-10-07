"""Fully lazy CEGAR search for a GRID counterexample (discovery only).
Variables: grid types (integer, sum D, a_i <= X_i, not homogeneous-Fano).
Lazy constraint families:
  * covering: when the model A has tau*(A) <= T, take the exact blocking witness (thresholds g) and add
    the clause "some chosen type lies in the corresponding residual box" (a_i < g_i on blocked coords);
  * pairs: 42 certified two-type functions, checked on the model, violated pairs added;
  * multi-type: all-support MILP on the model; the distinct types of a found tuple are forbidden jointly.
usage: python3 w4_typeclosed_lazy.py D X1,X2,... [T] [maxiter]
Returns CANDIDATE (tau*>T, no pair, MILP infeasible) or UNSAT (no grid counterexample; relies on the
numerical MILP only for learned multi-type clauses, and on the exact tau* witness for covering).
"""
import sys, time, json, itertools
import numpy as np
from fractions import Fraction as F
from pysat.solvers import Solver
from w4_typeclosed_lib import tau_star_witness, bad_tuple_milp, load_cap42
from w4_typeclosed_search import grid_types

def main(D, X, T=None, maxiter=200000, milp_limit=120, log_every=50):
    p = len(X)
    if T is None: T = (3*D)//4
    types = [t for t in grid_types(D, X) if not all(7*t[i] <= 4*X[i] for i in range(p))]
    n = len(types); Tarr = np.array(types, dtype=np.int64)
    idx = {t: k+1 for k, t in enumerate(types)}
    cap = load_cap42()
    # precompute per-function integer coefficients
    funcs = []
    for f in cap:
        rows = []
        for (u, v) in f:
            den = u.denominator*v.denominator
            rows.append((u.numerator*v.denominator, v.numerator*u.denominator, den))
        funcs.append(rows)
    def pair_bad_idx(a, b):
        A = Tarr[a]; B = Tarr[b]
        for rows in funcs:
            if all(all(cu*A[i] + cv*B[i] <= X[i]*den for (cu, cv, den) in rows) for i in range(p)):
                return True
        return False
    S = Solver(name='cadical153')
    S.add_clause(list(range(1, n+1)))
    stats = {'cover': 0, 'pair': 0, 'multi': 0}
    t0 = time.time(); it = 0
    while it < maxiter:
        it += 1
        if not S.solve():
            return {'status': 'UNSAT', 'iter': it, 'stats': stats, 'sec': round(time.time()-t0, 1)}
        model = [v for v in S.get_model() if 0 < v <= n]
        A = [v-1 for v in model]
        # 1. covering
        ts, gs = tau_star_witness([types[k] for k in A], X)
        if ts <= T:
            # residual box: blocked coords i (gs[i] not None) need a_i < gs[i]; others unconstrained
            mask = np.ones(n, dtype=bool)
            for i, g in enumerate(gs):
                if g is not None: mask &= Tarr[:, i] < g
            cl = [int(k)+1 for k in np.nonzero(mask)[0]]
            if not cl:
                return {'status': 'UNSAT-cover', 'iter': it, 'box': gs, 'stats': stats}
            S.add_clause(cl); stats['cover'] += 1
            if it % log_every == 0: print(f'it {it} |A|={len(A)} tau*={ts} stats={stats} ({time.time()-t0:.0f}s)', flush=True)
            continue
        # 2. pairs
        added = False
        for a, b in itertools.combinations_with_replacement(A, 2):
            if pair_bad_idx(a, b):
                S.add_clause([-(a+1)] if a == b else [-(a+1), -(b+1)]); stats['pair'] += 1; added = True
        if added:
            if it % log_every == 0: print(f'it {it} |A|={len(A)} tau*={ts} stats={stats} ({time.time()-t0:.0f}s)', flush=True)
            continue
        # 3. multi-type MILP on a minimised model
        chosen = list(A)
        for k in sorted(chosen, key=lambda k: -max(types[k])):
            trial = [c for c in chosen if c != k]
            if trial and tau_star_witness([types[c] for c in trial], X)[0] > T: chosen = trial
        An = [tuple(F(v, D) for v in types[k]) for k in chosen]; xn = [F(v, D) for v in X]
        st, assign, cells = bad_tuple_milp(An, xn, time_limit=milp_limit)
        if st == 'BAD':
            used = sorted(set(chosen[j] for j in assign))
            S.add_clause([-(k+1) for k in used]); stats['multi'] += 1
            print(f'it {it} MULTI |A|={len(chosen)} tau*={ts} uses {len(used)} types stats={stats} ({time.time()-t0:.0f}s)', flush=True)
            continue
        return {'status': 'CANDIDATE' if st == 'NONE' else 'UNKNOWN', 'A': [types[k] for k in chosen],
                'tau*': str(tau_star_witness([types[k] for k in chosen], X)[0]), 'iter': it, 'stats': stats}
    return {'status': 'MAXITER', 'stats': stats}

if __name__ == '__main__':
    D = int(sys.argv[1]); X = [int(v) for v in sys.argv[2].split(',')]
    T = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] != '-' else None
    res = main(D, X, T)
    print(json.dumps(res, default=str))
