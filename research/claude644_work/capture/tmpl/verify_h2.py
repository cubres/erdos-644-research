# EXACT randomized check of THEOREM H2 (templates agent, session 2):
# finite type set C over parts 0,1 (heavy) + light parts 2..p-1; every type heavy (t_i > 4x_i/7) only at 0 or 1
# (or nowhere -> homogeneous Fano).  tau*(C) >= 3/4  =>  the proof's pair works:
#   theta_1 <= 2x_1/3 -> Q_b(a0,b0);  theta_0 <= 2x_0/3 -> Q_a(a0,b0);  else V(a0, b*) with
#   a0 = argmin t_0 over C_0, b* = argmax (x_1 - t_1) over {b in C_1 : b_l + a0_l <= x_l for all light l}.
import random, itertools, sys
from fractions import Fraction as F
rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2])
def tau(x, T):
    p = len(x); best = sum(x) - 1
    cand = [[None] + sorted(set(t[i] for t in T if t[i] > 0)) for i in range(p)]
    for c in itertools.product(*cand):
        if all(any(c[i] is not None and t[i] >= c[i] for i in range(p)) for t in T):
            best = min(best, sum(x[i] - c[i] for i in range(p) if c[i] is not None))
    return best
def rnd(lo, hi, d): return lo + (hi - lo) * F(rng.randint(0, d), d)
def heavy(t, x, i): return 7 * t[i] > 4 * x[i]
Q = lambda s, t: max(F(3, 2) * t, s + F(3, 4) * t)
V = lambda s, t: max(s + t, F(5, 4) * s + t / 2)
stats = {'n': 0, 'H': 0, 'Qb': 0, 'Qa': 0, 'V': 0}; tries = 0
while stats['n'] < NT:
    tries += 1
    p = rng.choice([2, 3, 3, 4]); d = rng.choice([10, 20, 30, 60])
    x = [rnd(F(1, 5), F(8, 5), d) for _ in range(p)]
    T = []
    for k in range(rng.randint(2, 6 if p < 4 else 5)):
        h = k % 2 if k < 2 else rng.randrange(2)
        t = [F(0)] * p
        lo = 4 * x[h] / 7 if rng.random() < 0.3 else 2 * x[h] / 3
        if lo >= min(F(1), x[h]): lo = 4 * x[h] / 7
        t[h] = rnd(lo, min(F(1), x[h]), d)
        rest = 1 - t[h]; ok = True
        others = [i for i in range(p) if i != h]; rng.shuffle(others)
        for i in others:
            cap = min(4 * x[i] / 7, rest)
            v = (rnd(F(0), cap, d) if rng.random() < 0.5 else cap) if i != others[-1] else rest
            if v > 4 * x[i] / 7: ok = False; break
            t[i] = v; rest -= v
        if not ok or rest != 0: continue
        T.append(t)
    if len(T) < 2 or sum(x) < F(7, 4): continue
    if any(heavy(t, x, i) for t in T for i in range(2, p)): continue
    tt = tau(x, T)
    if tt < F(3, 4): continue
    stats['n'] += 1
    if any(all(7 * t[i] <= 4 * x[i] for i in range(p)) for t in T): stats['H'] += 1; continue
    C0 = [t for t in T if heavy(t, x, 0)]; C1 = [t for t in T if heavy(t, x, 1)]
    assert C0 and C1 and not any(heavy(t, x, 0) and heavy(t, x, 1) for t in T)
    a0 = min(C0, key=lambda t: t[0]); b0 = min(C1, key=lambda t: t[1])
    th0, th1 = a0[0], b0[1]; d0, d1 = x[0] - th0, x[1] - th1
    assert d0 + d1 >= F(3, 4) and th0 + th1 > 1
    if 3 * th1 <= 2 * x[1]:
        assert all(Q(a0[i], b0[i]) <= x[i] for i in range(p)), 'Qb'; stats['Qb'] += 1; continue
    if 3 * th0 <= 2 * x[0]:
        assert all(Q(b0[i], a0[i]) <= x[i] for i in range(p)), 'Qa'; stats['Qa'] += 1; continue
    S = [b for b in C1 if all(b[l] + a0[l] <= x[l] for l in range(2, p))]
    assert S, 'survivor set empty'
    bs = max(S, key=lambda b: x[1] - b[1])
    Lam = sum(a0[l] for l in range(2, p))
    assert x[1] - bs[1] >= F(3, 4) - d0 - Lam, 'residual bound'
    assert all(V(a0[i], bs[i]) <= x[i] for i in range(p)), ('V fails', x, T)
    stats['V'] += 1
print('tries', tries, stats, 'ALL CHECKS PASSED')
