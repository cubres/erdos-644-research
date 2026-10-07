# Referee w9 templates#2 (LOGIC lens, resume): independent exact check of the survivor-step example and of the
# H2 recipe on it.  tau* = min over assignments type->part of sum_i (x_i - min_{t assigned to i} t_i).
from fractions import Fraction as F
from itertools import product
def tau_star(x, T):
    best = None
    for asg in product(range(len(x)), repeat=len(T)):
        u = list(x)
        if any(t[i] == 0 for t, i in zip(T, asg)): continue   # cannot cut below 0
        for t, i in zip(T, asg): u[i] = min(u[i], t[i])
        c = sum(x[i] - u[i] for i in range(len(x)))
        best = c if best is None or c < best else best
    return best
V = lambda s, t: max(s + t, F(5, 4) * s + t / 2)
Qb = lambda s, t: max(F(3, 2) * t, s + F(3, 4) * t)
x = [F(32, 25), F(32, 25), F(9, 100)]
a0 = [F(9, 10), F(1, 20), F(1, 20)]; a1 = [F(91, 100), F(9, 100), F(0)]
b0 = [F(1, 20), F(9, 10), F(1, 20)]; b1 = [F(2, 25), F(23, 25), F(0)]
T = [a0, a1, b0, b1]
ts = tau_star(x, T); print('tau* =', ts, ts >= F(3, 4))
th1, th2 = min(t[0] for t in (a0, a1)), min(t[1] for t in (b0, b1))
print('theta', th1, th2, 'case C', th1 > 2 * x[0] / 3 and th2 > 2 * x[1] / 3)
S = [b for b in (b0, b1) if b[2] + a0[2] <= x[2]]
bs = max(S, key=lambda b: x[1] - b[1]); print('b* =', bs, 'b0 in S', b0 in S)
d1 = x[0] - th1; Lam0 = a0[2]
print('(2):', x[1] - bs[1], '>=', F(3, 4) - d1 - Lam0, x[1] - bs[1] >= F(3, 4) - d1 - Lam0)
print('V(a0,b*) slacks', [x[i] - V(a0[i], bs[i]) for i in range(3)])
print('V(a0,b0) slacks', [x[i] - V(a0[i], b0[i]) for i in range(3)], '(b0 fails at the light part)')
print('Qb(a0,b*) slacks', [x[i] - Qb(a0[i], bs[i]) for i in range(3)])
print('Qa(a0,b*) slacks', [x[i] - Qb(bs[i], a0[i]) for i in range(3)])

# ---- random end-to-end of the literal recipe with the brute tau* above (finite C is closed) ----
import random, sys
H = lambda s: F(7, 4) * s
def recipe(x, T):
    p = len(x); heavy = lambda t, i: 7 * t[i] > 4 * x[i]
    assert all(not heavy(t, l) for t in T for l in range(2, p))
    for t in T:
        if not heavy(t, 0) and not heavy(t, 1):
            return 'H', all(H(t[i]) <= x[i] for i in range(p))
    C1 = [t for t in T if heavy(t, 0)]; C2 = [t for t in T if heavy(t, 1)]
    assert C1 and C2 and not any(heavy(t, 0) and heavy(t, 1) for t in T)
    th1 = min(t[0] for t in C1); th2 = min(t[1] for t in C2)
    a0 = min(C1, key=lambda t: t[0]); b0 = min(C2, key=lambda t: t[1])
    assert x[0] - th1 + x[1] - th2 >= F(3, 4) and th1 + th2 > 1          # (1), F1
    if 3 * th2 <= 2 * x[1]: return 'Qb', all(Qb(a0[i], b0[i]) <= x[i] for i in range(p))
    if 3 * th1 <= 2 * x[0]: return 'Qa', all(Qb(b0[i], a0[i]) <= x[i] for i in range(p))
    S = [b for b in C2 if all(b[l] + a0[l] <= x[l] for l in range(2, p))]
    assert S
    bs = max(S, key=lambda b: x[1] - b[1])
    assert x[1] - bs[1] >= F(3, 4) - (x[0] - th1) - sum(a0[2:])            # (2)
    return ('V*' if bs is not b0 else 'V'), all(V(a0[i], bs[i]) <= x[i] for i in range(p))
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
def rf(lo, hi, d=60): return lo + (hi - lo) * F(rng.randint(0, d), d)
cnt = {}; tested = 0
for it in range(int(sys.argv[2]) if len(sys.argv) > 2 else 3000):
    p = rng.choice([2, 3, 3, 4]); x = [rf(F(3, 4), F(3, 2)), rf(F(3, 4), F(3, 2))] + [rf(F(1, 20), F(1, 2)) for _ in range(p - 2)]
    T = []
    for _ in range(rng.randint(2, 5)):
        h = rng.randint(0, 1); o = 1 - h
        t = [F(0)] * p; rest = F(1)
        for l in range(2, p):
            v = min(rest, 4 * x[l] / 7 * rf(0, 1, 7)); t[l] = v; rest -= v
        v = rf(F(1, 2), 1, 20) * rest; t[h] = v; t[o] = rest - v
        if all(t[i] <= x[i] for i in range(p)) and not any(7 * t[l] > 4 * x[l] for l in range(2, p)): T.append(t)
    if len(T) < 2 or tau_star(x, T) < F(3, 4): continue
    tested += 1; k, ok = recipe(x, T); cnt[k] = cnt.get(k, 0) + 1
    assert ok, (x, T, k)
print('random: tested', tested, cnt, 'ALL PASS')
