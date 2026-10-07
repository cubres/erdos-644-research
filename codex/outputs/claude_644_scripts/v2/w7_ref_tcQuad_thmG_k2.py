"""Referee (w7, tcQuad): Theorem G, k>=2 regime stress test (x <= 1/(2 theta)), p up to 8.
Checks: supports (7,2) => tau(S) <= k (EFKT, rank<=k, k>=2) and tau* <= k x (1-theta) <= 3/4;
and the k=1 violations of the original step all have |S|=2 singleton supports."""
import random, sys
from fractions import Fraction as F
from w7_ref_tcQuad_thmG import gen_type, tau_star, is72, tau_set, partB
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
cnt = {}; bad = []
for tr in range(int(sys.argv[2]) if len(sys.argv) > 2 else 3000):
    p = rng.randint(3, 8)
    theta = F(4, 7) + F(rng.randint(0, 10), 70) if rng.random() < 0.5 else F(4, 7)
    xmax = 1 / (2 * theta)
    x = F(rng.randint(20, 100), 100) * xmax
    k = int(1 / (theta * x))
    A = set()
    for _ in range(rng.randint(2, 7)):
        a = gen_type(p, x, theta, rng.randint(1, min(k, p)), rng)
        if a is not None: A.add(a)
    if not A: continue
    A = sorted(A)
    if k ** len(A) > 200000: continue
    ts = tau_star(A, p, x)
    S = [frozenset(i for i in range(p) if a[i] > 0) for a in A]
    ok, _ = is72(S, p)
    key = (min(k, 5), ok, ts > F(3, 4))
    cnt[key] = cnt.get(key, 0) + 1
    if ok:
        tS = tau_set(set(S), p)
        if tS > k or ts > k * x * (1 - theta) or ts > F(3, 4):
            bad.append((p, x, theta, k, A, ts, tS))
print('counts (k, S is (7,2), tau*>3/4):', sorted(cnt.items()))
print('k>=2 violations:', len(bad)); [print(b) for b in bad[:5]]
# k=1 violations in partB: confirm all are 2 singleton supports
st, vo, vc = partB(4000, 11)
shapes = set((v[3], tuple(sorted(tuple(i for i in range(v[0]) if a[i] > 0) for a in v[4]))) and (v[3], len(v[4]), v[6]) for v in vo)
print('partB original-step violations: (k, #types, tau(S)) shapes:', shapes, ' corrected violations:', len(vc))
