# Referee w7 / core#1 BREAK-IT (B2): quantifier of S_min in "tau_f <= 6k/S_min".
# The proof samples four edges i.i.d. (with replacement), so S_min must be the minimum over MULTISETS.
# Question: does tau_f <= 6k/S_min hold with S_min over DISTINCT quadruples?  Hill-climb on small hypergraphs
# maximising ratio = tau_f * S_min_distinct / (6k)  (k = max edge size); >1 is a counterexample to the distinct form.
# tau_f by HiGHS then verified EXACTLY: rational primal cover and dual matching from the basis (Fractions).
import itertools, random, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
def popc(x): return bin(x).count('1')
def S_of(G): return sum(popc(a & b) for a, b in itertools.combinations(G, 2))
def smin(E, distinct):
    it = itertools.combinations(E, 4) if distinct else itertools.combinations_with_replacement(E, 4)
    return min((S_of(G) for G in it), default=None)
def tauf(E, n):
    A = np.array([[(e >> v) & 1 for v in range(n)] for e in E], dtype=float)
    r = linprog(np.ones(n), A_ub=-A, b_ub=-np.ones(len(E)), bounds=[(0, None)] * n, method='highs')
    d = linprog(-np.ones(len(E)), A_ub=A.T, b_ub=np.ones(n), bounds=[(0, None)] * len(E), method='highs')
    return r.fun, r.x, d.x
def exact_certify(E, n, x, y, target):
    # rationalise and check cover >= 1, matching <= 1, and values bracket target
    X = [Fr(v).limit_denominator(1000) for v in x]; Y = [Fr(v).limit_denominator(1000) for v in y]
    cov = all(sum(X[v] for v in range(n) if e >> v & 1) >= 1 for e in E)
    mat = all(sum(Y[i] for i, e in enumerate(E) if e >> v & 1) <= 1 for v in range(n))
    return cov and mat and sum(X) == sum(Y), sum(Y)
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
iters = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
best = (0, None)
for restart in range(40):
    n = rng.randint(5, 9)
    E = list({sum(1 << v for v in rng.sample(range(n), rng.randint(1, n - 1))) for _ in range(rng.randint(4, 8))})
    if len(E) < 4: continue
    def score(E):
        if len(E) < 4: return -1
        k = max(popc(e) for e in E); s = smin(E, True)
        if s == 0: return 0
        return tauf(E, n)[0] * s / (6 * k)
    cur = score(E)
    for _ in range(iters // 40):
        F = list(E)
        op = rng.random()
        if op < 0.4 and F: F[rng.randrange(len(F))] ^= 1 << rng.randrange(n)
        elif op < 0.7: F.append(sum(1 << v for v in rng.sample(range(n), rng.randint(1, n - 1))))
        elif len(F) > 4: F.pop(rng.randrange(len(F)))
        F = [e for e in set(F) if e]
        sc = score(F)
        if sc >= cur: E, cur = F, sc
    if cur > best[0]: best = (cur, (n, sorted(E)))
    if cur > 1 + 1e-9:
        k = max(popc(e) for e in E); tf, x, y = tauf(E, n)
        ok, val = exact_certify(E, n, x, y, tf)
        print('COUNTEREXAMPLE to distinct form: n', n, 'edges', [sorted(v for v in range(n) if e >> v & 1) for e in E],
              'k', k, 'tau_f', val, 'exact-certified', ok, 'S_min distinct', smin(E, True), 'S_min multiset', smin(E, False),
              '6k/S_d', Fr(6 * k, smin(E, True)), '6k/S_multi', Fr(6 * k, smin(E, False)), flush=True)
        break
print('best ratio tau_f*S_d/(6k) =', best[0], best[1])
