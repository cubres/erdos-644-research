"""SAT-CEGAR search for counterexamples to CONJECTURE FP ('tau*>3/4 => Fano bad tuple or two-type bad tuple')
restricted to GRID type sets: types a with a_i in (1/N)Z, sum a = 1, a <= x (p parts).
Variables y_a (type selected).  Clauses: (i) no pair template (42 fns, incl. a=b) [static, binary];
(ii) lazily: every free residual u with sum u >= X - T (T = 3/4 + eta) must contain a selected type;
(iii) lazily: no Fano tuple among selected types (found by MILP).
Output: UNSAT (no FP-counterexample on this grid with tau* >= T) or an explicit FP-free set (then verified)."""
import sys, itertools, time, json
import numpy as np
from fractions import Fraction as Fr
from scipy.optimize import milp, LinearConstraint, Bounds
from pysat.solvers import Solver
import heavylib as h, pairlib as P

def grid_types(x, N):
    p = len(x); out = []
    for c in itertools.product(range(N+1), repeat=p-1):
        s = sum(c)
        if s > N: continue
        v = list(c) + [N - s]
        a = [Fr(k, N) for k in v]
        if all(a[i] <= x[i] for i in range(p)): out.append(a)
    return out

def max_free(x, T):
    """return (sup free sum, caps, strict-flags) via B&B over blocking maps"""
    p = len(x)
    order = sorted(range(len(T)), key=lambda j: -max(T[j][i]/x[i] for i in range(p)))
    best = [None, None, None]
    def blocked(a, caps, st):
        return any(a[i] > 0 and (caps[i] < a[i] or (caps[i] == a[i] and st[i])) for i in range(p))
    def rec(k, caps, st):
        s = sum(caps)
        if best[0] is not None and s <= best[0]: return
        while k < len(order) and blocked(T[order[k]], caps, st): k += 1
        if k == len(order):
            best[0] = s; best[1] = list(caps); best[2] = list(st); return
        a = T[order[k]]
        for i in sorted(range(p), key=lambda i: a[i]-caps[i]):
            if a[i] > 0 and a[i] <= caps[i]:
                c2 = list(caps); c2[i] = a[i]; s2 = list(st); s2[i] = True
                rec(k+1, c2, s2)
    rec(0, list(x), [False]*p)
    return best

def fits(a, caps, st):
    return all(a[i] < caps[i] or (a[i] == caps[i] and not st[i]) for i in range(len(caps)))

def fano_find(x, T):
    """MILP: choose a type for each line, per-part Lemma 7.63 inequalities. returns list of type indices or None"""
    m = len(T); p = len(x)
    if m == 0: return None
    nv = 7*m
    A = []; lo = []; hi = []
    for l in range(7):
        r = np.zeros(nv); r[l*m:(l+1)*m] = 1; A.append(r); lo.append(1); hi.append(1)
    Tf = np.array([[float(v) for v in a] for a in T])
    for i in range(p):
        for q in range(7):
            r = np.zeros(nv)
            for l in h.PENCIL[q]: r[l*m:(l+1)*m] = Tf[:, i]
            A.append(r); lo.append(-np.inf); hi.append(2*float(x[i]) + 1e-9)
        r = np.zeros(nv)
        for l in range(7): r[l*m:(l+1)*m] = Tf[:, i]
        A.append(r); lo.append(-np.inf); hi.append(4*float(x[i]) + 1e-9)
    res = milp(np.zeros(nv), constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.ones(nv),
               bounds=Bounds(0, 1), options={'time_limit': 60})
    if res.status != 0 or res.x is None: return None
    z = res.x.reshape(7, m)
    asg = [int(np.argmax(z[l])) for l in range(7)]
    rows = [T[j] for j in asg]
    if not h.fano_rows_ok(x, rows, tol=0): return None   # exact recheck
    return asg

def run(x, N, eta, maxit=100000, log=print):
    p = len(x); X = sum(x); Tgt = Fr(3, 4) + eta
    G = grid_types(x, N); n = len(G)
    idx = {tuple(a): k+1 for k, a in enumerate(G)}
    S = Solver(name='cd15')
    Gf = [[float(v) for v in a] for a in G]
    npair = 0
    for j in range(n):
        if P.pair_ok([float(v) for v in x], Gf[j], Gf[j], tol=-1e-12) is not None:
            S.add_clause([-(j+1)]); npair += 1
    for j in range(n):
        for l in range(j+1, n):
            if P.pair_ok([float(v) for v in x], Gf[j], Gf[l], tol=-1e-12) is not None or \
               P.pair_ok([float(v) for v in x], Gf[l], Gf[j], tol=-1e-12) is not None:
                S.add_clause([-(j+1), -(l+1)]); npair += 1
    log(f"x={[str(v) for v in x]} N={N} types={n} pair/single clauses={npair}")
    ncov = nfano = 0; t0 = time.time()
    for it in range(maxit):
        if not S.solve():
            log(f"UNSAT after {it} iters (cov cuts {ncov}, fano cuts {nfano}), {time.time()-t0:.0f}s"); return None
        model = set(v for v in S.get_model() if v > 0)
        sel = [G[k] for k in range(n) if (k+1) in model]
        # covering
        best, caps, st = max_free(x, sel) if sel else (X, list(x), [False]*p)
        if best is None: best, caps, st = X, list(x), [False]*p
        if X - best < Tgt:
            cl = [k+1 for k in range(n) if fits(G[k], caps, st)]
            S.add_clause(cl); ncov += 1
            continue
        asg = fano_find(x, sel)
        if asg is not None:
            used = sorted(set(idx[tuple(sel[j])] for j in asg))
            S.add_clause([-v for v in used]); nfano += 1
            continue
        log(f"FOUND FP-free grid set: tau*={X-best} ({float(X-best):.4f}), {len(sel)} types, iters {it}")
        return sel
    log("maxit reached"); return 'maxit'

if __name__ == '__main__':
    xs = [Fr(s) for s in sys.argv[1].split(',')]; N = int(sys.argv[2]); eta = Fr(sys.argv[3])
    sel = run(xs, N, eta)
    if isinstance(sel, list):
        print("types:", [[str(v) for v in a] for a in sel])
        print("exact tau*:", h.tau_star_fast(xs, sel), " any pair:", P.any_pair([float(v) for v in xs], [[float(v) for v in a] for a in sel]))
