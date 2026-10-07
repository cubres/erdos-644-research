# EXACT randomized check of the TWO UP-BOX THEOREM (templates agent, session 2):
# C = U(g) u U(h) over p parts, tau*(C) >= 3/4, both generators heavy somewhere (else homogeneous Fano).
# Canonical types a = g + (1-|g|) e_J, b = h + (1-|h|) e_I (I heavy for g, J heavy for h) are admissible and
# one of Q_b, Q_a, V(a,b) is feasible; also checks the intermediate claims of the hand proof.
import random, itertools, sys
from fractions import Fraction as F
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
NT = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
def tau(x, gens):
    p = len(x); best = sum(x) - 1
    ch = [[i for i in range(p) if g[i] > 0] for g in gens]
    for phi in itertools.product(*ch):
        u = {}
        for j, i in enumerate(phi): u[i] = min(u.get(i, F(10)), gens[j][i])
        best = min(best, sum(x[i] - u[i] for i in u))
    return best
def rnd(lo, hi, d): return lo + (hi - lo) * F(rng.randint(0, d), d)
stats = {'n': 0, 'Qb': 0, 'Qa': 0, 'V': 0}
tries = 0
while stats['n'] < NT:
    tries += 1
    p = rng.choice([2, 3, 3, 4, 5]); d = rng.choice([8, 12, 20, 40, 60])
    x = [rnd(F(1, 5), F(8, 5), d) for _ in range(p)]
    gens = []
    for j in range(2):
        g = [F(0)] * p; H = rng.randrange(p)
        g[H] = rnd(4 * x[H] / 7, min(F(1), x[H]), d)
        for i in range(p):
            if i != H and rng.random() < 0.6: g[i] = rnd(F(0), x[i] * rng.choice([F(1, 5), F(1, 2), F(4, 5), F(1)]), d)
        gens.append(g)
    g, h = gens
    if sum(g) > 1 or sum(h) > 1: continue
    t = tau(x, gens)
    if t < F(3, 4): continue
    stats['n'] += 1
    Is = [i for i in range(p) if 7 * g[i] > 4 * x[i]]; Js = [i for i in range(p) if 7 * h[i] > 4 * x[i]]
    for I in Is:
        for J in Js:
            assert I != J
            a = list(g); a[J] += 1 - sum(g); b = list(h); b[I] += 1 - sum(h)
            assert a[J] <= x[J] and b[I] <= x[I], 'admissibility'
            assert g[I] + h[J] > 1
            Qb = all(max(F(3, 2) * b[i], a[i] + F(3, 4) * b[i]) <= x[i] for i in range(p))
            Qa = all(max(F(3, 2) * a[i], b[i] + F(3, 4) * a[i]) <= x[i] for i in range(p))
            V = all(max(a[i] + b[i], F(5, 4) * a[i] + b[i] / 2) <= x[i] for i in range(p))
            # intermediate claims
            assert all(a[i] + F(3, 4) * b[i] <= x[i] for i in range(p)), 'Qb facet'
            assert all(b[i] + F(3, 4) * a[i] <= x[i] for i in range(p)), 'Qa facet'
            if not Qb and not Qa:
                Ks = [i for i in range(p) if 2 * x[i] < 3 * b[i]]; Ls = [i for i in range(p) if 2 * x[i] < 3 * a[i]]
                assert I not in Ks and J not in Ls and not set(Ks) & set(Ls)
                assert V, ('V fails', x, g, h, I, J)
            assert Qb or Qa or V
            if (I, J) == (Is[0], Js[0]):
                stats['Qb' if Qb else 'Qa' if Qa else 'V'] += 1
print('tries', tries, stats, 'ALL CHECKS PASSED')
