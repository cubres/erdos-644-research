# |H|=3 rigid sets with tau*>=3/4 where NO pair template (H,Q,V) works: which T(A,B,C) triples work?
import random, sys, itertools
from collections import Counter
from h2_lib import *
p, nt, NT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); rng = random.Random(int(sys.argv[4]))
TF = [(1, .5, .25), (1, 0, .5), (0, 1, .5), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
def T_ok(x, a, b, c): return all(f[0]*a[i] + f[1]*b[i] + f[2]*c[i] <= x[i] + 1e-12 for i in range(len(x)) for f in TF)
def pair_ok(x, T):
    for t in T:
        if all(7 * t[k] <= 4 * x[k] + 1e-12 for k in range(len(x))): return True
    for a in T:
        for b in T:
            if a is not b and (feas(x, a, b, TWO['Qt']) or feas(x, a, b, TWO['V'])): return True
    return False
C = Counter(); n = 0; tries = 0
while n < NT:
    tries += 1
    x = [rng.uniform(0.3, 1.3) for _ in range(p)]
    T = []
    for k in range(nt):
        h = k % 3
        t = [0.0] * p; t[h] = rng.uniform(4 * x[h] / 7, min(1, x[h]))
        rest = 1 - t[h]; w = [rng.random() * (rng.random() < .6) for _ in range(p)]; w[h] = 0
        if sum(w) == 0: w[(h + 1) % p] = 1
        t = [t[i] + rest * w[i] / sum(w) for i in range(p)]
        if any(t[i] > x[i] for i in range(p)) or any(7 * t[i] > 4 * x[i] for i in range(p) if i != h): break
        T.append(t)
    if len(T) < nt or sum(x) < 1.75: continue
    tt = tau_rigid2(x, T)
    if tt < 0.75: continue
    if pair_ok(x, T): C['pair'] += 1; n += 1; continue
    n += 1
    H = [0, 1, 2]
    th = [min(t[i] for t in T if 7 * t[i] > 4 * x[i]) for i in H]
    d = [x[i] - th[i] for i in H]
    ok = [tr for tr in itertools.permutations(range(nt), 3) if T_ok(x, *[T[k] for k in tr])]
    if not ok: C['NONE'] += 1; print('NONE', tt, x, T); continue
    heav = lambda k: [i for i in range(p) if 7 * T[k][i] > 4 * x[i]][0]
    amin = lambda k: abs(T[k][heav(k)] - th[heav(k)]) < 1e-12
    dorder = sorted(H, key=lambda i: -d[i])
    feats = set()
    for tr in ok:
        parts = tuple(heav(k) for k in tr)
        feats.add(('distinct' if len(set(parts)) == 3 else 'rep') + (' argminA' if amin(tr[0]) else '') + (' allargmin' if all(amin(k) for k in tr) else '') + (' A=maxd' if parts[0] == dorder[0] else ''))
    C['T'] += 1
    for f in feats: C[f] += 1
print(p, nt, 'tries', tries, dict(C))
