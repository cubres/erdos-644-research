# Among single-heavy 3-type 3-heavy-part families with tau*>=3/4 where no pair (H,Q,V) works:
# which ordering rules for T(argmins) always work?
import random, sys, itertools
from collections import Counter
from h2_lib import *
p = int(sys.argv[1]); NT = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
TF = [(1, .5, .25), (1, 0, .5), (0, 1, .5), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
def T_ok(x, a, b, c): return all(f[0]*a[i] + f[1]*b[i] + f[2]*c[i] <= x[i] + 1e-12 for i in range(len(x)) for f in TF)
def pair_ok(x, T):
    for t in T:
        if all(7 * t[k] <= 4 * x[k] + 1e-12 for k in range(len(x))): return True
    for a in T:
        for b in T:
            if a is not b and (feas(x, a, b, TWO['Qt']) or feas(x, a, b, TWO['V'])): return True
    return False
def sample():
    x = [rng.uniform(0.4, 1.3) for _ in range(p)]
    T = []
    for h in range(3):
        t = [0.0] * p; t[h] = rng.uniform(max(4 * x[h] / 7, 2 * x[h] / 3 * (rng.random() < .7)), min(1, x[h]))
        rest = 1 - t[h]; w = [rng.random() * (rng.random() < .7) for _ in range(p)]; w[h] = 0
        if sum(w) == 0: return None
        t = [t[i] + rest * w[i] / sum(w) for i in range(p)]
        if any(t[i] > x[i] for i in range(p)) or any(7 * t[i] > 4 * x[i] for i in range(p) if i != h): return None
        T.append(t)
    return x, T
C = Counter(); n = 0; fails = Counter()
rules = {
 'A=maxd,C=mind': lambda d: (max(range(3), key=lambda i: d[i]), 3 - max(range(3), key=lambda i: d[i]) - min(range(3), key=lambda i: d[i]), min(range(3), key=lambda i: d[i])),
 'A=mind,C=maxd': lambda d: (min(range(3), key=lambda i: d[i]), 3 - max(range(3), key=lambda i: d[i]) - min(range(3), key=lambda i: d[i]), max(range(3), key=lambda i: d[i])),
 'A=maxd,B=mind': lambda d: (max(range(3), key=lambda i: d[i]), min(range(3), key=lambda i: d[i]), 3 - max(range(3), key=lambda i: d[i]) - min(range(3), key=lambda i: d[i])),
}
while n < NT:
    s = sample()
    if s is None: continue
    x, T = s
    if sum(x) < 1.75: continue
    # short climb to push into pair-free region with tau*>=3/4 is skipped: plain rejection
    tt = tau_rigid2(x, T)
    if tt < 0.75 or pair_ok(x, T): continue
    n += 1
    d = [x[i] - T[i][i] for i in range(3)]
    ok = [tr for tr in itertools.permutations(range(3)) if T_ok(x, *[T[k] for k in tr])]
    C[len(ok)] += 1
    for name, r in rules.items():
        if tuple(r(d)) not in ok: fails[name] += 1
print('n', n, 'num orderings working:', dict(C), 'rule failures:', dict(fails))
