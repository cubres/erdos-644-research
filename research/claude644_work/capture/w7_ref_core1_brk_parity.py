# Referee w7 / core#1 BREAK-IT (B3): the FKW parity family P_m (|A|=4m, |B|=3m+1, edges = 4m-sets with
# |E&A| odd; k=4m, t=3m+1 = 3k/4+1) is the only known family in the claim's regime t>=3k/4+1.
# Exact: (i) S_min over four edges (repeats allowed; also distinct) by a Venn MILP (HiGHS, integer data,
#     objective re-evaluated exactly on the integer solution; optimality certified by the LP-free lower bound
#     below when they coincide);  (ii) tau_f exactly (Fractions) via the Sym(A)xSym(B)-symmetric 2-variable LP
#     (symmetrisation is exact: averaging an optimal cover over the group keeps feasibility and value);
#     (iii) min-norm marginal ||p*||^2 exactly over symmetric distributions (edge-type mixture), check >= S_min/6;
#     (iv) compare with the claim: S_min >= t, tau_f <= 6k/S_min <= 6k/t < 8.
# Also K_n^k (n = t+k-1 < 7k/4): S_min closed form vs stated bound.
import itertools, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from math import comb

PATS = [P for r in range(0, 5) for P in itertools.combinations(range(4), r)]  # includes empty
W = [len(P) * (len(P) - 1) // 2 for P in PATS]

def smin_parity(m, distinct=False):
    nP = len(PATS)
    # vars: xA_P (nP), xB_P (nP), y_j (4)   with sum_{P ni j} xA_P = 2y_j+1
    nv = 2 * nP + 4
    c = np.array(W + W + [0] * 4, dtype=float)
    rows, lo, hi = [], [], []
    def add(r, l, h): rows.append(r); lo.append(l); hi.append(h)
    r = [0] * nv
    for i in range(nP): r[i] = 1
    add(r, 4 * m, 4 * m)
    r = [0] * nv
    for i in range(nP): r[nP + i] = 1
    add(r, 3 * m + 1, 3 * m + 1)
    for j in range(4):
        r = [0] * nv
        for i, P in enumerate(PATS):
            if j in P: r[i] = 1; r[nP + i] = 1
        add(r, 4 * m, 4 * m)
        r = [0] * nv
        for i, P in enumerate(PATS):
            if j in P: r[i] = 1
        r[2 * nP + j] = -2
        add(r, 1, 1)
    cons = [LinearConstraint(np.array(rows, dtype=float), lo, hi)]
    res = milp(c, constraints=cons, integrality=np.ones(nv), bounds=Bounds(0, 8 * m))
    x = [int(round(v)) for v in res.x]
    val = sum(W[i] * (x[i] + x[nP + i]) for i in range(nP))
    # exact recheck of constraints
    xa, xb = x[:nP], x[nP:2 * nP]
    assert sum(xa) == 4 * m and sum(xb) == 3 * m + 1
    for j in range(4):
        sa = sum(xa[i] for i, P in enumerate(PATS) if j in P)
        sb = sum(xb[i] for i, P in enumerate(PATS) if j in P)
        assert sa + sb == 4 * m and sa % 2 == 1
    return val, {PATS[i]: (xa[i], xb[i]) for i in range(nP) if xa[i] or xb[i]}

def smin_lower(n, k):
    # balanced degree bound: sum_v C(d_v,2) with sum d_v = 4k over n points (any 4 k-sets)
    q, r = divmod(4 * k, n)
    return (n - r) * comb(q, 2) + r * comb(q + 1, 2)

def tauf_parity(m):
    # symmetric cover: alpha on A, beta on B; edge with a A-points (a odd, max(1,m-1)<=a<=4m, 4m-a<=3m+1)
    k = 4 * m; nB = 3 * m + 1
    As = [a for a in range(1, 4 * m + 1, 2) if 4 * m - a <= nB]
    cons = [(Fr(a), Fr(k - a)) for a in As] + [(Fr(1), Fr(0)), (Fr(0), Fr(1))]  # alpha,beta>=0 as rows (>=0)
    best = None
    # vertices: intersections of pairs of lines among a*al+(k-a)*be=1, al=0, be=0
    lines = [(Fr(a), Fr(k - a), Fr(1)) for a in As] + [(Fr(1), Fr(0), Fr(0)), (Fr(0), Fr(1), Fr(0))]
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(lines, 2):
        det = a1 * b2 - a2 * b1
        if det == 0: continue
        al = (c1 * b2 - c2 * b1) / det; be = (a1 * c2 - a2 * c1) / det
        if al < 0 or be < 0: continue
        if all(a * al + (k - a) * be >= 1 for a in As):
            v = 4 * m * al + nB * be
            if best is None or v < best[0]: best = (v, al, be)
    return best

def minnorm_parity(m):
    # symmetric distributions: mixture over edge types a (A-count); marginals pA = sum q_a a/(4m), pB = sum q_a (4m-a)/(3m+1)
    # ||p||^2 = 4m pA^2 + (3m+1) pB^2, convex in (pA,pB) on the segment hull -> minimise over the 2D hull exactly
    k = 4 * m; nB = 3 * m + 1
    As = [a for a in range(1, 4 * m + 1, 2) if 4 * m - a <= nB]
    pts = [(Fr(a, 4 * m), Fr(k - a, nB)) for a in As]
    # all points lie on the line 4m pA + nB pB = k; minimise f on the segment between extreme pts
    f = lambda pa, pb: 4 * m * pa * pa + nB * pb * pb
    # unconstrained min on the line: pA = pB = k/(7m+1)
    lo_a = min(p[0] for p in pts); hi_a = max(p[0] for p in pts)
    pa = Fr(k, 7 * m + 1)
    pa = min(max(pa, lo_a), hi_a)
    pb = (k - 4 * m * pa) / nB
    return f(pa, pb), pa, pb

if __name__ == '__main__':
    print('FKW parity family P_m: k=4m, t=3m+1')
    for m in range(1, int(sys.argv[1]) if len(sys.argv) > 1 else 13):
        k = 4 * m; t = 3 * m + 1; n = 7 * m + 1
        S, venn = smin_parity(m)
        lb = smin_lower(n, k)
        tf = tauf_parity(m)
        nn, pa, pb = minnorm_parity(m)
        stated = min(t, (3 * (2 * t - k - 2)) // 2 + 1)
        print(f' m={m:2d} k={k:2d} t={t:2d}: S_min={S:3d} (balanced lower bd {lb}) stated bound={stated}  S_min/t={S/t:.3f}'
              f' | tau_f={tf[0]} ({float(tf[0]):.4f}) 6k/S_min={Fr(6*k,S)} ({6*k/S:.3f}) 6k/t={6*k/t:.3f}'
              f' | ||p*||^2={nn} >= S_min/6={Fr(S,6)}: {nn >= Fr(S,6)}', flush=True)
        assert S >= stated and tf[0] <= Fr(6 * k, S) and nn >= Fr(S, 6)
    print('K_n^k with n=t+k-1 < 7k/4 (property (7,2) iff n<=ceil(7k/4)-1): S_min vs stated bound')
    worst = None
    for k in range(4, 81):
        for n in range(k + 1, -(-7 * k // 4)):
            t = n - k + 1
            S = smin_lower(n, k)
            stated = min(t, (3 * (2 * t - k - 2)) // 2 + 1)
            assert S >= stated
            r = S / t
            if worst is None or r < worst[0]: worst = (r, k, n, t, S)
    print(' all K_n^k (k<=80) consistent; min S_min/t =', worst)
