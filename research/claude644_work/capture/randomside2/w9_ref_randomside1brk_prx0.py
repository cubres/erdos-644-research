# BREAK-IT referee, Lemma TJ: EXACT Pr[X=0] (enumerating all subfamilies of K_N^(k)) vs the lemma's bound
# exp(-min_J mu_J/(2K_j)), and vs the raw Janson bound exp(-mu^2/(2 Dbar)) (sanity), for every exact type
# (optionally with a chosen subset Q of A_0 as extra data). Also two MUTATIONS that must break:
#  M1 refined marginals (J-part carries Q) -- j=1, config (G,Q), Q subset G, |Q|=s.
#  M2 FIXED global extra data (a fixed set Z; role must meet Z in a points) with the marginal forgetting Z.
import itertools, math, sys
import numpy as np
from collections import Counter, defaultdict
from fractions import Fraction as F

def venn(sets, N):
    c = Counter()
    for x in range(N):
        c[tuple(i for i, s in enumerate(sets) if x in s)] += 1
    return tuple(sorted(c.items()))
def Ksum(j): return sum(math.comb(j, s) * math.perm(j, s) for s in range(1, j + 1))

def prx0_poly(gammas, m):
    arr = np.arange(1 << m, dtype=np.int64)
    bad = np.zeros(1 << m, dtype=bool)
    for g in gammas: bad |= (arr & g) == g
    pc = np.array([bin(i).count('1') for i in range(1 << m)]) if m <= 16 else None
    good_sizes = np.bincount(pc[~bad], minlength=m + 1)
    return good_sizes  # Pr[X=0] = sum_s good[s] rho^s (1-rho)^(m-s)

def evalp(good, m, rho): return sum(int(good[s]) * rho ** s * (1 - rho) ** (m - s) for s in range(m + 1))

def run(N, k, j, qsize=None):
    ks = [frozenset(c) for c in itertools.combinations(range(N), k)]; m = len(ks); ix = {s: i for i, s in enumerate(ks)}
    types = defaultdict(list)
    for tup in itertools.permutations(ks, j):
        if qsize is None: types[venn(tup, N)].append((tup, None))
        else:
            for Q in itertools.combinations(sorted(tup[0]), qsize):
                types[venn(tup + (frozenset(Q),), N)].append((tup, frozenset(Q)))
    Kj = Ksum(j); viol = 0; viol_janson = 0; tightest = None; nt = 0
    for Y, confs in types.items():
        nt += 1
        subsets = [J for r in range(1, j + 1) for J in itertools.combinations(range(j), r)]
        P = {J: len({tuple(t[i] for i in J) for t, _ in confs}) for J in subsets}
        gam = {sum(1 << ix[s] for s in t) for t, _ in confs}
        good = prx0_poly(sorted(gam), m)
        # Dbar polynomial
        union = Counter(); C = len(confs)
        for tA, _ in confs:
            for tB, _ in confs:
                sh = len(set(tA) & set(tB))
                if sh: union[2 * j - sh] += 1
        for rho in [0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99]:
            p0 = evalp(good, m, rho)
            lemma = math.exp(-min(P[J] * rho ** len(J) for J in subsets) / (2 * Kj))
            mu = C * rho ** j; Db = sum(v * rho ** u for u, v in union.items())
            jan = math.exp(-mu * mu / (2 * Db))
            if p0 > lemma * (1 + 1e-12): viol += 1
            if p0 > jan * (1 + 1e-12): viol_janson += 1
            r = p0 / lemma
            if tightest is None or r > tightest[0]: tightest = (r, rho, Y)
    return nt, viol, viol_janson, tightest

def mutation_M1(N, k, s, rho):
    M = math.comb(N, k); true = (1 - rho) ** M
    refined = math.exp(-M * math.comb(k, s) * rho / 2)   # refined mu_{1} = #(G,Q) rho, K_1 = 1
    unref = math.exp(-M * rho / 2)
    return true, refined, unref

def mutation_M2(N, k, z, a, rho):
    Mtrue = math.comb(z, a) * math.comb(N - z, k - a); true = (1 - rho) ** Mtrue
    forget = math.exp(-math.comb(N, k) * rho / 2)
    orbit = math.exp(-Mtrue * rho / 2)   # correct marginal = orbit under Stab(Z)
    return true, forget, orbit

if __name__ == "__main__":
    for (N, k, j, q) in [(4,2,2,None),(5,2,2,None),(5,2,3,None),(5,3,2,None),(6,2,2,None),(6,2,3,None),(5,2,2,1),(5,3,2,1),(6,2,2,1),(5,3,3,None),(5,2,4,None)]:
        nt, v, vj, t = run(N, k, j, q)
        print(f"N={N} k={k} j={j} Q={q}: types={nt} lemma violations={v} janson violations={vj}  max Pr[X=0]/lemma = {t[0]:.4g} (rho={t[1]})", flush=True)
    print("M1 refined marginals, j=1, (G,Q), N=5,k=4,|Q|=2, rho=0.1: true, refined-bound, unrefined-bound =", mutation_M1(5, 4, 2, 0.1))
    print("M1 N=20,k=4,s=2, rho=1e-3:", mutation_M1(20, 4, 2, 1e-3))
    print("M2 fixed Z, N=6,k=3,|Z|=3,a=3, rho=0.5: true, forget-Z bound, orbit bound =", mutation_M2(6, 3, 3, 3, 0.5))
    print("M2 N=12,k=4,|Z|=4,a=4 rho=0.05:", mutation_M2(12, 4, 4, 4, 0.05))
