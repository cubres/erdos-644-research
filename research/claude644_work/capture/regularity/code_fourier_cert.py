# FOURIER-JANSON CERTIFICATE for random linear-code (syndrome) families  H_{c,a} = {k-sets E : sum_{x in E} c(x) = a},
# c: [N] -> F_2^r uniform, 2^{-r} = 1/C(xk,k) (so r ln2 = k psi(x)), N = nk.
# Lemma (notes_regularity [r5]): for a Venn type tau on cells (safe Fano sets) with masses y, nondegenerate over F_2,
#   P_c[no 7-tuple of type tau in H] <= 2^49 * sum_{U != 0} exp(-k E_U + O(ln k)),
#   E_U(y,n,x) = n ln n - sum_v m_v ln m_v - dim(U) psi(x),   m_v = mass of the cells S with (mu(S))_{mu in basis(U)} = v.
# Coordinate subspaces U = <e_j : j in J> give exactly the typed-Janson marginal exponents E_J of randomside2.
# Symmetric types y_S = a_{|S|}; empty cell a0 = n - (7a1+21a2+28a3+7a4) >= 0; line sums a1+6a2+12a3+4a4 = 1.
# Staircase exactly as randomside2/cert_fano_staircase.py: E_U increases with empty mass (dE/dd = ln((n+d)/(m0+d)) >= 0)
# and decreases in x, so certifying (n_i = x_{i-1}+3/4, x_i) covers {x in [x_{i-1},x_i], n >= x+3/4}.
import numpy as np, itertools, sys, os, time
from fractions import Fraction as F
from mpmath import iv
from scipy.optimize import minimize
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'randomside2'))
from fano_janson_sym import SAFE, SZ
iv.dps = 30
CELLS = [sum(1 << l for l in S) for S in SAFE]          # bitmask over the 7 lines; () -> 0 = empty cell
SIZES = [len(S) for S in SAFE]
assert len(SAFE) == 64 and 0 in CELLS
# ---- all subspaces of F_2^7 (as frozensets of ints), by BFS over spans
def span(vs):
    s = {0}
    for v in vs:
        s |= {w ^ v for w in s}
    return frozenset(s)
subspaces = {frozenset([0]): []}
frontier = [frozenset([0])]
while frontier:
    nxt = []
    for S in frontier:
        for v in range(1, 128):
            if v not in S:
                T = span(list(subspaces[S]) + [v])
                if T not in subspaces:
                    subspaces[T] = subspaces[S] + [v]; nxt.append(T)
    frontier = nxt
assert len(subspaces) == 29212, len(subspaces)
# ---- coarsening signatures: for each nonzero U, classes of cells by (parity of |mu & S|)_{mu in basis}
def popc(x): return bin(x).count('1')
SIG = {}
for U, basis in subspaces.items():
    d = len(basis)
    if d == 0: continue
    cls = {}
    for c, m in zip(CELLS, SIZES):
        v = tuple(popc(b & c) & 1 for b in basis)
        cls.setdefault(v, [0]*5)[m] += 1
    sig = tuple(sorted(tuple(x) for x in cls.values()))
    SIG.setdefault((d, sig), 0); SIG[(d, sig)] += 1
KEYS = sorted(SIG)
print(f"{len(subspaces)} subspaces, {len(KEYS)} distinct (dim, signature) pairs", flush=True)
# matrix form for fast evaluation: rows = classes, cols = a0..a4 ; owner = key index ; DIM per key
rows = []; owner = []; DIM = []
for i, (d, sig) in enumerate(KEYS):
    DIM.append(d)
    for cv in sig:
        rows.append(cv); owner.append(i)
ROWS = np.array(rows, float); OWNER = np.array(owner); DIM = np.array(DIM, float)
# sanity: coordinate subspaces reproduce the Janson marginals (E_J) -- checked in notes by hand; here structural check:
coord_sigs = set()
for r_ in range(1, 8):
    for J in itertools.combinations(range(7), r_):
        cls = {}
        for c, m in zip(CELLS, SIZES):
            key = tuple(sorted(l for l in J if c >> l & 1))
            cls.setdefault(key, [0]*5)[m] += 1
        coord_sigs.add((r_, tuple(sorted(tuple(x) for x in cls.values()))))
assert coord_sigs <= set(KEYS), "coordinate subspaces missing"
def psi(x): return x*np.log(x) - (x-1)*np.log(x-1) if x > 1 else 0.0
def avec(a, n):
    a1, a2, a3, a4 = a
    return np.array([n - (7*a1 + 21*a2 + 28*a3 + 7*a4), a1, a2, a3, a4])
def exps(a, n, x):
    m = ROWS @ avec(a, n)
    t = np.where(m > 0, m*np.log(np.maximum(m, 1e-300)), 0.0)
    s = np.bincount(OWNER, weights=t, minlength=len(KEYS))
    return n*np.log(n) - s - DIM*psi(x)
def best_a(n, x):
    cons = [{'type': 'eq', 'fun': lambda z: z[0] + 6*z[1] + 12*z[2] + 4*z[3] - 1},
            {'type': 'ineq', 'fun': lambda z: n - (7*z[0] + 21*z[1] + 28*z[2] + 7*z[3])},
            {'type': 'ineq', 'fun': lambda z: exps(z[:4], n, x) - z[4]}]
    best = None
    for a0 in [(0.1, 0.05, 0.03, 0.05), (0.02, 0.02, 0.02, 0.15), (0.2, 0.05, 0.02, 0.02), (0.001, 0.001, 0.02, 0.18), (0.001, 0.001, 0.001, 0.247), (0.05, 0.01, 0.04, 0.1)]:
        a0 = np.array(a0); a0 = a0/(a0[0] + 6*a0[1] + 12*a0[2] + 4*a0[3])
        if 7*a0[0] + 21*a0[1] + 28*a0[2] + 7*a0[3] > n: a0 = np.array([0.0, 0.0, (n - 1.75)/7*0.9, 0.25 - 3*(n - 1.75)/7*0.9])
        z0 = np.concatenate([a0, [exps(np.maximum(a0, 1e-12), n, x).min()]])
        r = minimize(lambda z: -z[4], z0, constraints=cons, bounds=[(0, None)]*4 + [(None, None)], method='SLSQP', options={'maxiter': 600, 'ftol': 1e-13})
        if best is None or r.x[4] > best[4]: best = r.x
    return best[:4]
def I(q): return iv.mpf(q.numerator)/iv.mpf(q.denominator)
def xlnx(v): return iv.mpf(0) if v.b <= 0 else v*iv.log(v)
def certify_point(nq, xq, a):
    a2, a3, a4 = [F(float(max(v, 0))).limit_denominator(10**9) for v in a[1:4]]
    a1 = 1 - 6*a2 - 12*a3 - 4*a4
    if a1 < 0: return None
    a0 = nq - (7*a1 + 21*a2 + 28*a3 + 7*a4)
    if a0 < 0: return None
    A = [a0, a1, a2, a3, a4]
    if a1 == 0 and a3 == 0: return None            # degenerate over F_2 (no odd cell): all-ones dependency
    AI = [I(v) for v in A]
    nI = I(nq); xI = I(xq); ps = xI*iv.log(xI) - (xI-1)*iv.log(xI-1) if xq > 1 else iv.mpf(0)
    worst = None; wk = None
    for i, (d, sig) in enumerate(KEYS):
        s = iv.mpf(0)
        for cv in sig:
            m = sum(cv[t]*AI[t] for t in range(5) if cv[t]); s += xlnx(m)
        e = nI*iv.log(nI) - s - d*ps
        if worst is None or e.a < worst: worst = e.a; wk = (d, sig)
    return worst, wk, A
if __name__ == "__main__":
    XMAX = F(sys.argv[1]) if len(sys.argv) > 1 else F(9, 2)
    THR = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-4
    xprev = F(1); h = F(1, 20); cells = 0; minmarg = None; t0 = time.time()
    while xprev < XMAX:
        while True:
            xi = min(xprev + h, XMAX); ni = xprev + F(3, 4)
            a = best_a(float(ni), float(xi))
            res = certify_point(ni, xi, a)
            if res is not None and res[0] > THR: break
            h = h*F(4, 5)
            if h < F(1, 10**6):
                print("FAIL at x=", float(xprev), "last result", None if res is None else float(res[0])); sys.exit(1)
        w, wk, A = res
        cells += 1; minmarg = w if minmarg is None else min(minmarg, w)
        print(f"cell x in [{float(xprev):.5f},{float(xi):.5f}], n>=x+3/4: certified at (n={float(ni):.5f},x={float(xi):.5f}) min_U E_U >= {float(w):.5f} (binding dim {wk[0]}; a1..a4 = {[float(v) for v in A[1:]]}) [{time.time()-t0:.0f}s]", flush=True)
        xprev = xi; h = min(h*2, F(7, 10))
    print(f"CERTIFIED (Fourier-Janson, all 29212 subspaces) region x in [1,{float(XMAX)}], n-x>=3/4: {cells} cells, min margin {float(minmarg):.5f}")
