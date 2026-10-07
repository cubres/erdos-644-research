# Referee w9, randomside#1: MUTATION tests (show the exact checker has power) + asymptotic exponent check.
# M1: drop the marginals (use mu itself instead of min_J mu_J): expect Dbar <= mu^2 K_j/mu to FAIL somewhere,
#     and exp(-mu/(2K_j)) to be violated by the exact Pr[X=0].
# M2: K_j with the |J|=j terms only (sigma a permutation):  expect FAIL.
# A : ln P_J - |J| ln C(xk,k)  vs  k*E_J  (E_J = n ln n - sum m ln m - |J| psi(x)) : difference = O(ln k).
import itertools, math
from fractions import Fraction as F
from mpmath import mp, mpf, exp, log, loggamma
import numpy as np
from w9_ref_randomside1_exact import venn, marginal, multinom, Kj
mp.dps = 40
Q = lambda q: mpf(q.numerator) / q.denominator

def pairs(tups):
    sets = [frozenset(t) for t in tups]; cont = {}; cnt = {}
    for a, s in enumerate(sets):
        for g in s: cont.setdefault(g, []).append(a)
    for a, s in enumerate(sets):
        seen = set()
        for g in s:
            for b in cont[g]:
                if b not in seen: seen.add(b); sh = len(s & sets[b]); cnt[sh] = cnt.get(sh, 0) + 1
    return sets, cnt

def mutation(N, k, j):
    ksets = [frozenset(c) for c in itertools.combinations(range(N), k)]
    idx = {s: i for i, s in enumerate(ksets)}; G = len(ksets)
    types = {}
    for tup in itertools.permutations(ksets, j):
        types.setdefault(frozenset(venn(tup, N).items()), []).append(tup)
    f1 = f2 = f3 = 0
    for key, tups in types.items():
        Y = dict(key); T = len(tups); sets, cnt = pairs(tups)
        masks = sorted(set(sum(1 << idx[g] for g in s) for s in sets))
        allm = np.arange(1 << G, dtype=np.int64); bad = np.zeros(1 << G, dtype=bool)
        for a in masks: bad |= (allm & a) == a
        good = allm[~bad]; pc = np.zeros(good.shape, dtype=np.int64); t = good.copy()
        while t.any(): pc += t & 1; t >>= 1
        fm = np.bincount(pc, minlength=G + 1)
        for rho in [F(1, 100), F(1, 10), F(1, 3), F(1, 2), F(9, 10)]:
            mu = T * rho ** j; Dbar = sum(c * rho ** (2 * j - s) for s, c in cnt.items())
            if Dbar > mu * Kj(j): f1 += 1
            Kperm = math.factorial(j)
            mn = min(multinom(N, marginal(Y, frozenset(J))) * rho ** len(J) for r in range(1, j + 1) for J in itertools.combinations(range(j), r))
            if Dbar > mu * mu * Kperm / mn: f2 += 1
            p0 = sum(int(fm[m]) * rho ** m * (1 - rho) ** (G - m) for m in range(G + 1))
            if mpf(p0.numerator) / p0.denominator > exp(-mpf(mu.numerator) / mu.denominator / (2 * Kj(j))): f3 += 1
    return f1, f2, f3

def asym():
    # a 3-role type (fractions of k): cells over subsets of {0,1,2}; each role has size 1
    y = {(): F(3, 5), (0,): F(2, 5), (1,): F(2, 5), (2,): F(2, 5), (0, 1): F(1, 5), (0, 2): F(1, 5), (1, 2): F(1, 5), (0, 1, 2): F(1, 5)}
    for r in range(3): assert sum(v for S, v in y.items() if r in S) == 1
    n = sum(y.values()); x = F(3, 2)
    psi = lambda x: x * log(x) - (x - 1) * log(x - 1)
    print("A: type n =", n, " x =", x)
    for k in [50, 100, 200, 400, 800, 1600, 3200]:
        worst = 0
        for r in range(1, 4):
            for J in itertools.combinations(range(3), r):
                m = {}
                for S, v in y.items():
                    T = tuple(sorted(set(S) & set(J))); m[T] = m.get(T, 0) + v
                EJ = Q(n) * log(Q(n)) - sum(Q(v) * log(Q(v)) for v in m.values() if v) - len(J) * psi(Q(x))
                N = int(n * k)
                lnP = loggamma(N + 1) - sum(loggamma(int(v * k) + 1) for v in m.values())
                lnrho = -(loggamma(int(x * k) + 1) - loggamma(k + 1) - loggamma(int((x - 1) * k) + 1))
                d = (lnP + len(J) * lnrho - k * EJ) / log(k)
                worst = max(worst, abs(d))
        print(f"  k={k}: max_J |ln mu_J - k E_J| / ln k = {float(worst):.3f}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1: asym(); sys.exit()
    for (N, k, j) in [(4, 2, 2), (4, 2, 3), (5, 2, 3), (6, 2, 3), (6, 3, 2)]:
        f1, f2, f3 = mutation(N, k, j)
        print(f"N={N} k={k} j={j}: M1 (no marginals) Dbar-bound violations {f1}, Pr-bound violations {f3};"
              f" M2 (K_j=j! only) violations {f2}", flush=True)
    asym()
