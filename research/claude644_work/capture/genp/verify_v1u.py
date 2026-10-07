"""Exact random check of LEMMA V1' (corner + V, any number of classes/light parts) and LEMMA U' (minimiser pair V)
from notes_generalp.md (5),(6).  Random rational finite families over p parts (h heavy, L light); every type
super-heavy somewhere; an unbalanced pair e_j+e_k > 3/4 is required.  For V1': a = S_k-minimiser; request u as in the
lemma; if cost(u) < tau* (exact) and a_i <= 2x_i/3 off {j,k}: EVERY witness c <= u must lie in S_j and V(a,c) must be
exactly feasible.  For U': if a_i+b_i <= x_i and 5a_i/4+b_i/2 <= x_i off {j,k}: V(a,b) exactly feasible.
usage: verify_v1u.py seed n h L"""
import sys, os, random, itertools
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'heavy'))
import heavylib as H
seed, n, h, L = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed); p = h + L
def rf(a, b, d=60):
    lo, hi = int(a*d), int(b*d)
    if hi < lo: return None
    return F(rng.randint(lo, hi), d)
def vfeas(x, s, t):
    return all(s[i] + t[i] <= x[i] and F(5,4)*s[i] + t[i]/2 <= x[i] for i in range(p))
stats = {'fam': 0, 'unbal': 0, 'v1_applicable': 0, 'v1_ok': 0, 'v1_FAIL': 0, 'u_applicable': 0, 'u_ok': 0, 'u_FAIL': 0}
for it in range(n):
    x = [rf(0.5, 1.5) for _ in range(h)] + [rf(0.3, 2.0) for _ in range(L)]
    T = []
    for j in range(rng.randint(h, h + 4)):
        k = j % h
        f = rf(float(2*x[k]/3) + 0.02, min(float(x[k]), 1.0))
        if f is None: continue
        rest = [rf(0, 1) for _ in range(p)]; rest[k] = F(0); s = sum(rest)
        if s == 0: continue
        c = [(1 - f) * r / s for r in rest]; c[k] = f
        # scale to fit capacities / lightness; rejection
        if any(c[i] > x[i] for i in range(p)) or any(3*c[i] > 2*x[i] for i in range(h, p)): continue
        T.append(c)
    if len(T) < h: continue
    S = [[j for j in range(len(T)) if 3*T[j][i] > 2*x[i]] for i in range(h)]
    if any(len(S[i]) == 0 for i in range(h)): continue
    stats['fam'] += 1
    sig = [min(T[j][i] for j in S[i]) for i in range(h)]; e = [x[i] - sig[i] for i in range(h)]
    tau = H.tau_star(x, T)
    for j, k in itertools.permutations(range(h), 2):
        if e[j] + e[k] <= F(3, 4): continue
        stats['unbal'] += 1
        a = T[min(S[k], key=lambda q: T[q][k])]
        I = [i for i in range(h) if i not in (j, k)]
        # V1'
        u = list(x); u[k] = sig[k] - F(1, 10**6)
        for i in range(p):
            if i == k: continue
            if i in I and a[i] <= e[i]: u[i] = sig[i] - F(1, 10**6)
            else: u[i] = x[i] - a[i]
        cost = sum(x[i] - u[i] for i in range(p))
        if cost < tau and all(a[i] <= 2*x[i]/3 for i in range(p) if i not in (j, k)):
            stats['v1_applicable'] += 1
            wit = [c for c in T if all(c[i] <= u[i] for i in range(p))]
            ok = len(wit) > 0 and all(3*c[j] > 2*x[j] and vfeas(x, a, c) for c in wit)
            stats['v1_ok' if ok else 'v1_FAIL'] += 1
            if not ok: print("V1 FAIL", x, T, j, k, wit)
        # U'
        b = T[min(S[j], key=lambda q: T[q][j])]
        if all(a[i] + b[i] <= x[i] and F(5,4)*a[i] + b[i]/2 <= x[i] for i in range(p) if i not in (j, k)):
            stats['u_applicable'] += 1
            ok = vfeas(x, a, b)
            stats['u_ok' if ok else 'u_FAIL'] += 1
            if not ok: print("U FAIL", x, a, b, j, k)
print(stats)
