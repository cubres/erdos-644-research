"""Target (3): search continuous type-closed models (grid types) with tau* > 3D/4 that satisfy the
LOCAL conditions only:
  GT*  : every triple of types a,b,c with a+b+c <= 2X has U(a,b,c)=sum_i max(a_i,b_i,c_i,(a_i+b_i+c_i)/2) >= 2 tau*
  D4   : (optional) no 7 types (multiset) with sum <= 3X  (all degrees <= 3 -> bad tuple)
  Q    : (optional) Lemma Q in continuum (checked by LP on 4-multisets)  [only relevant for N > 2.75 D]
CEGAR with pysat.  Types: integer vectors 0<=a<=X with sum a = D (rank D exactly) [or <= D with --le].
tau* (continuum, integer types): N - max_{free v} sum_i min(v_i+1, X_i).
Output: a SAT model (relaxation-counterexample) or UNSAT (no grid type set satisfies GT*(+D4) with tau*>T).
Discovery tool; a SAT witness is re-verified exactly (integers) below.
"""
import itertools, sys, time
from pysat.solvers import Cadical153

def types_of(X, D, le=False):
    p = len(X); out = []
    for a in itertools.product(*[range(x+1) for x in X]):
        s = sum(a)
        if (s == D) or (le and 0 < s <= D):
            out.append(a)
    return out

def tau_star(types, X):
    # exact: N - max over free integer v of sum min(v_i+1, X_i); v free iff no type <= v
    p = len(X); N = sum(X)
    best = -1
    # enumerate candidate v: coordinates v_i in {X_i} or {g-1 : g a type coordinate value >0}
    cand = [sorted(set([X[i]] + [t[i]-1 for t in types if t[i] > 0])) for i in range(p)]
    for v in itertools.product(*cand):
        if any(all(t[i] <= v[i] for i in range(p)) for t in types):
            continue
        val = sum(min(v[i]+1, X[i]) for i in range(p))
        best = max(best, val)
    return N - best

def U3(a, b, c):
    return sum(max(a[i], b[i], c[i], (a[i]+b[i]+c[i])/2) for i in range(len(a)))

def run(X, D, T, use_d4=True, le=False, maxit=2000, verbose=True):
    p = len(X); N = sum(X)
    TY = types_of(X, D, le)
    idx = {a: j+1 for j, a in enumerate(TY)}
    S = Cadical153()
    # covering: every v with sum min(v_i+1,X_i) >= N-T must dominate a type
    need = N - T
    ncov = 0
    for v in itertools.product(*[range(x+1) for x in X]):
        val = sum(min(v[i]+1, X[i]) for i in range(p))
        if val < need: continue
        # minimal only
        minimal = True
        for i in range(p):
            if v[i] > 0:
                w = list(v); w[i] -= 1
                if sum(min(w[j]+1, X[j]) for j in range(p)) >= need:
                    minimal = False; break
        if not minimal: continue
        cl = [idx[a] for a in TY if all(a[i] <= v[i] for i in range(p))]
        if not cl:
            return 'UNSAT-trivial', None
        S.add_clause(cl); ncov += 1
    # static GT* clauses for threshold 2(T+1)
    ngt = 0
    thr = 2*(T+1)
    for x_, y_, z_ in itertools.combinations_with_replacement(range(len(TY)), 3):
        a, b, c = TY[x_], TY[y_], TY[z_]
        if any(a[i]+b[i]+c[i] > 2*X[i] for i in range(p)): continue
        if U3(a, b, c) < thr:
            S.add_clause(sorted(set([-idx[a], -idx[b], -idx[c]]))); ngt += 1
    if verbose: print(f"X={X} D={D} T={T} N/D={N/D:.3f} types={len(TY)} cov={ncov} gt={ngt}", flush=True)
    it = 0
    while it < maxit:
        it += 1
        if not S.solve():
            return 'UNSAT', it
        model = S.get_model()
        A = [a for a in TY if model[idx[a]-1] > 0]
        # minimise A greedily keeping tau* > T (smaller A => fewer violations)
        ts = tau_star(A, X)
        # check GT* with actual tau*
        bad = None
        for a, b, c in itertools.combinations_with_replacement(A, 3):
            if any(a[i]+b[i]+c[i] > 2*X[i] for i in range(p)): continue
            if U3(a, b, c) < 2*ts:
                bad = (a, b, c); break
        if bad:
            S.add_clause(sorted(set(-idx[z] for z in bad))); continue
        if use_d4:
            d4 = find_d4(A, X)
            if d4:
                S.add_clause(sorted(set(-idx[z] for z in d4))); continue
        return 'SAT', (A, ts)
    return 'MAXIT', it

def find_d4(A, X):
    """7 types (multiset) with sum <= 3X coordinatewise.  Small ILP via scipy."""
    import numpy as np
    from scipy.optimize import milp, LinearConstraint, Bounds
    p = len(X); m = len(A)
    Amat = np.array([[a[i] for a in A] for i in range(p)] + [[1]*m])
    lo = [-np.inf]*p + [7]; hi = [3*x for x in X] + [7]
    res = milp(np.zeros(m), constraints=LinearConstraint(Amat, lo, hi), integrality=np.ones(m),
               bounds=Bounds(0, 7))
    if res.status == 0:
        n = [int(round(v)) for v in res.x]
        ms = [A[j] for j in range(m) for _ in range(n[j])]
        assert len(ms) == 7 and all(sum(a[i] for a in ms) <= 3*X[i] for i in range(p))
        return list(set(ms))
    return None

if __name__ == '__main__':
    X = [int(v) for v in sys.argv[1].split(',')]
    D = int(sys.argv[2]); T = (3*D)//4
    d4 = (sys.argv[3] == '1') if len(sys.argv) > 3 else True
    t0 = time.time()
    st, info = run(X, D, T, use_d4=d4)
    print(st, info if st != 'SAT' else '', f"{time.time()-t0:.1f}s")
    if st == 'SAT':
        A, ts = info
        print("tau*=", ts, "ratio", ts/D, "types", len(A))
        for a in A: print("  ", a)
