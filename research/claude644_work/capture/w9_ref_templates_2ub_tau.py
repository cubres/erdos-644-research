# Referee w9, templates#1: cross-check of the 2UB tau* formula (min(N-1, K1', K2')) against note Lemma 7.56
# (blocker pairs over all subsets, upper bounds h=x) and against a brute-force residual search on a grid.
import random, itertools, sys
from fractions import Fraction as F
from w9_ref_templates_2ub import tau_756, sample
def tau_2ub(x, g, h):
    p = len(x); best = sum(x) - 1
    for i in range(p):
        if g[i] > 0 and h[i] > 0: best = min(best, x[i] - min(g[i], h[i]))
        for j in range(p):
            if i != j and g[i] > 0 and h[j] > 0: best = min(best, x[i] - g[i] + x[j] - h[j])
    return best
def tau_brute(x, g, h, D):
    # residual r on grid (multiples of 1/D, plus values just below generator coords); cost N-|r|;
    # r must block both: exists i r_i<g_i or |r|<1.  Brute force over candidate r_i values.
    p = len(x); N = sum(x); best = None
    cands = []
    for i in range(p):
        c = {x[i], F(0)} | {v - F(1, 10**6) for v in (g[i], h[i]) if v > 0}
        cands.append(sorted(v for v in c if 0 <= v <= x[i]))
    for r in itertools.product(*cands):
        s = sum(r)
        def blocked(gen): return s < 1 or any(r[i] < gen[i] for i in range(p))
        if blocked(g) and blocked(h):
            # also allow shrinking |r| to just below 1 is covered by candidate 0/x; take cost
            c = N - s; best = c if best is None or c < best else best
    # the |r|<1 blocker: cost -> N-1 (infimum)
    return min(best, N - 1)
rng = random.Random(int(sys.argv[1])); bad = 0; n = 0; nb = 0
for it in range(int(sys.argv[2])):
    x, g, h = sample(rng, it % 3)
    if sum(g) > 1 or sum(h) > 1: continue
    n += 1
    t1, t2 = tau_756(x, [g, h]), tau_2ub(x, g, h)
    if t1 != t2: bad += 1; print('MISMATCH 756', x, g, h, t1, t2)
    if len(x) <= 4:
        nb += 1; t3 = tau_brute(x, g, h, 0)
        if abs(t3 - t2) > F(1, 10**4): bad += 1; print('MISMATCH brute', [str(v) for v in x], g, h, t2, t3)
print('instances', n, 'brute-checked', nb, 'mismatches', bad)
