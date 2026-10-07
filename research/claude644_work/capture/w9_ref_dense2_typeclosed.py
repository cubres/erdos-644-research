"""Referee w9, dense#2: large type-closed instances (f_pi is 0/1), exact f_2 via hypergeometric pmf (Fractions
for the pmf, float compare).  Checks T3 (proposition) with non-vacuous bounds and measures SHARPNESS:
beta_2(a) := min{b : f_2(a,b) >= 1-eta}  vs  height prediction  X * min{h(g): g gen, a_g<=a}."""
import itertools, random, math, sys
from math import comb
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
fails = 0; checks = 0; nonvac = 0; sharp = []
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 30):
    m = random.choice([2, 3]); ns = [random.randint(15, 40) for _ in range(m)]; X = sum(ns)
    e = random.randint(10, 30)
    gens = []
    for _ in range(random.randint(1, 4)):
        gens.append((random.randint(0, e), tuple(random.randint(0, n) for n in ns)))
    def fpi(a, U):
        return 1 if any(a >= g[0] and all(U[i] >= g[1][i] for i in range(m)) for g in gens) else 0
    def pmf(b):
        out = []
        for U in itertools.product(*[range(n+1) for n in ns]):
            if sum(U) != b: continue
            p = 1
            for u, n in zip(U, ns): p *= comb(n, u)
            out.append((U, p / comb(X, b)))
        return out
    P = {b: pmf(b) for b in range(X+1)}
    def f2(a, b): return sum(p for U, p in P[b] if fpi(a, U))
    for (ga, gu) in gens:
        a = ga
        for eta in [0.0, 0.1]:
            for lam in [2.0, 4.0, 6.0, 8.0]:
                need = max(X*(gu[s]+lam)/ns[s] for s in range(m))
                for b in range(max(1, math.ceil(need)), X+1):
                    bound = 1 - eta - m*math.exp(-2*lam**2/b)
                    checks += 1; nonvac += bound > 0
                    if f2(a, b) < bound - 1e-9: fails += 1
    # sharpness at eta=0.1
    for a in sorted(set(g[0] for g in gens)):
        hs = [max(g[1][s]/ns[s] for s in range(m)) for g in gens if g[0] <= a]
        pred = X*min(hs)
        b2 = next((b for b in range(X+1) if f2(a, b) >= 0.9), None)
        bal = min(sum(g[1]) for g in gens if g[0] <= a)   # fine rank-based (balanced would be = pred)
        sharp.append((round(pred, 1), b2, bal))
print('checks', checks, 'nonvacuous', nonvac, 'fails', fails)
print('sharpness (X*min h, beta_2(a) at eta=.1, min |u|):')
print(sharp[:40])
dev = [b2 - pred for pred, b2, bal in sharp if b2 is not None]
print('beta_2 - X*h : min %.1f max %.1f' % (min(dev), max(dev)))
