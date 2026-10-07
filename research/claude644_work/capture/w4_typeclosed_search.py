"""CEGAR search for a finite GRID type set A (integer types summing to D, capacities X) with
tau*(A) > T (default 3D/4) and NO bad seven-tuple.  Discovery tool.

SAT vars: one per grid type.  Clauses:
  * covering: every residual box u with blocking cost <= T contains a chosen type;
  * single exclusions (homogeneous Fano), pair exclusions (42 certified two-type functions);
  * learned: for every bad tuple found by the MILP, not all of its distinct types.
Model is greedily minimised (drop types while covering holds) before the MILP check.
A returned 'CANDIDATE' is a finite type set on which the MILP found no bad tuple: it still needs
exact verification.  'UNSAT' means: no grid type set (this D, X) is a counterexample (modulo the
numerical MILP used to learn exclusions: exclusions are only learned from MILP-feasible tuples,
which should be re-verified exactly if the UNSAT is to be used)."""
import sys, time, itertools, json
from fractions import Fraction as F
from pysat.solvers import Solver
from w4_typeclosed_lib import *

def grid_types(D, X):
    p = len(X)
    out = []
    def rec(i, rem, cur):
        if i == p - 1:
            if rem <= X[i]: out.append(tuple(cur + [rem]))
            return
        for v in range(0, min(rem, X[i]) + 1):
            rec(i + 1, rem - v, cur + [v])
    rec(0, D, [])
    return out

def residual_boxes(X, T):
    """minimal u (u_i in [0,X_i]) with cost(u)=sum_{u_i<X_i}(X_i-1-u_i) <= T."""
    p = len(X)
    def cost(u): return sum(X[i]-1-u[i] for i in range(p) if u[i] < X[i])
    boxes = []
    for u in itertools.product(*[range(X[i]+1) for i in range(p)]):
        c = cost(u)
        if c > T: continue
        minimal = True
        for i in range(p):
            if u[i] > 0:
                v = list(u); v[i] -= 1
                if cost(v) <= T: minimal = False; break
        if minimal: boxes.append(u)
    return boxes

def run(D, X, T=None, max_iter=100000, milp_limit=60, log=None, seed_clauses=None):
    p = len(X)
    if T is None: T = (3*D)//4 if (3*D) % 4 else 3*D//4   # tau* > 3D/4  <=> every cost <= 3D/4 covered
    types = [t for t in grid_types(D, X) if not all(7*t[i] <= 4*X[i] for i in range(p))]
    idx = {t: k+1 for k, t in enumerate(types)}
    boxes = residual_boxes(X, T)
    cap = load_cap42()
    S = Solver(name='cadical153')
    cov = []
    for u in boxes:
        cl = [idx[t] for t in types if all(t[i] <= u[i] for i in range(p))]
        if not cl:
            return {'status': 'UNSAT-trivial', 'box': u}
        cov.append(cl); S.add_clause(cl)
    Xf = [F(v) for v in X]
    npair = 0
    for a, b in itertools.combinations(types, 2):
        if pair_bad(a, b, Xf, cap):
            S.add_clause([-idx[a], -idx[b]]); npair += 1
    for a in types:
        if pair_bad(a, a, Xf, cap):
            S.add_clause([-idx[a]]); npair += 1
    print(f'D={D} X={X} T={T}: {len(types)} types, {len(boxes)} boxes, {npair} pair exclusions', flush=True)
    it = 0; t0 = time.time()
    while it < max_iter:
        it += 1
        if not S.solve():
            return {'status': 'UNSAT', 'iterations': it, 'seconds': time.time()-t0}
        model = set(v for v in S.get_model() if v > 0)
        chosen = [t for t in types if idx[t] in model]
        # greedy minimisation w.r.t. covering
        chosen_set = set(idx[t] for t in chosen)
        for t in sorted(chosen, key=lambda t: -max(t)):
            k = idx[t]
            chosen_set.discard(k)
            if not all(any(c in chosen_set for c in cl) for cl in cov):
                chosen_set.add(k)
        A = [t for t in types if idx[t] in chosen_set]
        An = [tuple(F(v, D) for v in t) for t in A]
        xn = [F(v, D) for v in X]
        st, assign, cells = bad_tuple_milp(An, xn, time_limit=milp_limit)
        if st == 'BAD':
            used = sorted(set(assign))
            S.add_clause([-idx[A[j]] for j in used])
            if it % 20 == 0:
                print(f'  it {it}: |A|={len(A)} bad tuple types {len(used)} ({time.time()-t0:.0f}s)', flush=True)
            continue
        return {'status': 'CANDIDATE' if st == 'NONE' else 'UNKNOWN', 'A': A, 'iterations': it,
                'tau_star': str(tau_star(A, [F(v) for v in X]))}
    return {'status': 'MAXITER'}

if __name__ == '__main__':
    D = int(sys.argv[1]); X = [int(v) for v in sys.argv[2].split(',')]
    T = int(sys.argv[3]) if len(sys.argv) > 3 else None
    res = run(D, X, T)
    print(json.dumps(res, default=str))
