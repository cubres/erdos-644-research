"""Vectorised version of the grid CEGAR search (discovery only).
usage: python3 w4_typeclosed_search2.py D X1,X2,..  [T] [--pairs-only]
Grid types: integer vectors, sum D, 0<=a_i<=X_i, not homogeneous-Fano (7a<=4X).
Covering: every minimal residual box u with cost sum_{u_i<X_i}(X_i-1-u_i) <= T (default floor(3D/4))
contains a chosen type  <=>  continuous tau*(A) > T (exact for grid A).
Pair exclusions: the 42 certified two-type functions (both orders; a=b included).
CEGAR: MILP over all supports; learned clause = not all distinct types of the found tuple.
"""
import sys, time, itertools, json
import numpy as np
from fractions import Fraction as F
from pysat.solvers import Solver
from w4_typeclosed_lib import load_cap42, bad_tuple_milp, tau_star
from w4_typeclosed_search import grid_types, residual_boxes

def pair_matrix(types, X, cap):
    T = np.array(types, dtype=np.int64)          # n x p
    n, p = T.shape
    bad = np.zeros((n, n), dtype=bool)
    for f in cap:
        ok = np.ones((n, n), dtype=bool)
        for i in range(p):
            m = None
            for (u, v) in f:
                # compare u*a_i + v*b_i <= X_i exactly using integer scaling by lcm of denominators
                den = u.denominator * v.denominator
                val = (u.numerator * v.denominator) * T[:, i][:, None] + (v.numerator * u.denominator) * T[:, i][None, :]
                c = val <= X[i] * den
                m = c if m is None else (m & c)
            ok &= m
            if not ok.any(): break
        bad |= ok
    return bad

def run(D, X, T=None, pairs_only=False, milp_limit=120, max_iter=100000, out=None):
    p = len(X)
    if T is None: T = (3*D)//4
    types = [t for t in grid_types(D, X) if not all(7*t[i] <= 4*X[i] for i in range(p))]
    n = len(types); idx = {t: k+1 for k, t in enumerate(types)}
    boxes = residual_boxes(X, T)
    Tarr = np.array(types)
    S = Solver(name='cadical153')
    cov = []
    for u in boxes:
        mask = np.all(Tarr <= np.array(u)[None, :], axis=1)
        cl = [int(k)+1 for k in np.nonzero(mask)[0]]
        if not cl: return {'status': 'UNSAT-trivial', 'box': u}
        cov.append(cl); S.add_clause(cl)
    t0 = time.time()
    bad = pair_matrix(types, X, load_cap42())
    npair = 0
    for k in range(n):
        if bad[k, k]:
            S.add_clause([-(k+1)]); npair += 1
    I, J = np.nonzero(np.triu(bad | bad.T, 1))
    for a, b in zip(I, J):
        S.add_clause([-(int(a)+1), -(int(b)+1)])
    npair += len(I)
    print(f'D={D} X={X} T={T}: {n} types, {len(boxes)} boxes, {npair} pair excl ({time.time()-t0:.1f}s)', flush=True)
    it = 0
    while it < max_iter:
        it += 1
        if not S.solve():
            return {'status': 'UNSAT', 'iterations': it, 'seconds': time.time()-t0}
        model = S.get_model()
        chosen = set(v for v in model if v > 0 and v <= n)
        for k in sorted(chosen, key=lambda k: -max(types[k-1])):
            chosen.discard(k)
            if not all(any(c in chosen for c in cl) for cl in cov): chosen.add(k)
        A = [types[k-1] for k in sorted(chosen)]
        if pairs_only:
            return {'status': 'PAIRFREE_COVER', 'A': A, 'tau_star': str(tau_star(A, [F(v) for v in X])),
                    'size': len(A)}
        An = [tuple(F(v, D) for v in t) for t in A]; xn = [F(v, D) for v in X]
        st, assign, cells = bad_tuple_milp(An, xn, time_limit=milp_limit)
        if st == 'BAD':
            used = sorted(set(assign))
            S.add_clause([-idx[A[j]] for j in used])
            print(f'  it {it}: |A|={len(A)} bad tuple uses {len(used)} types ({time.time()-t0:.0f}s)', flush=True)
            continue
        res = {'status': 'CANDIDATE' if st == 'NONE' else 'UNKNOWN', 'A': A, 'iterations': it,
               'tau_star': str(tau_star(A, [F(v) for v in X]))}
        return res
    return {'status': 'MAXITER'}

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    D = int(args[0]); X = [int(v) for v in args[1].split(',')]
    T = int(args[2]) if len(args) > 2 else None
    res = run(D, X, T, pairs_only='--pairs-only' in sys.argv)
    print(json.dumps(res, default=str))
