"""Sanity certificate for THEOREM SC (notes_sparse.md [s1]) on explicit (7,2) families.

For each family H (rank <= k, tau = t) it checks, exactly where possible:
  (Q)  every 4-tuple of edges (repeats allowed) has S = sum_{i<j}|G_i & G_j| >= m_Q := min(t, floor(3(2t-k-2)/2)+1)
       (Lemma Q corollary; exhaustive over 4-multisets, or sampled for large families);
  (F)  a rational fractional transversal w (rounded up from the HiGHS LP optimum) with w(E) >= 1 for every edge
       and total mass <= 6k/m_Q  (i.e. tau* <= 6k/m_Q, exact rational verification of the certificate w);
  (G)  the greedy star cover has size <= mass(w) ln|H| + 1 and >= tau (so tau <= tau* ln|H| + 1);
  (E)  |H| >= exp((t-1) m_Q/(6k)).
The theorem is a hand proof; this script only exercises every inequality of the chain on real families.
"""
import itertools, math, random, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
from lib72 import is_72, tau as tau_exact, complete, popcount

def frac_transversal(H, n):
    """LP: min sum w_x s.t. sum_{x in E} w_x >= 1, w >= 0.  Returns rational w rounded up (feasible)."""
    A = np.zeros((len(H), n))
    for i, E in enumerate(H):
        for x in range(n):
            if E >> x & 1: A[i, x] = -1.0
    res = linprog(np.ones(n), A_ub=A, b_ub=-np.ones(len(H)), bounds=[(0, None)] * n, method='highs')
    assert res.status == 0
    w = [Fr(max(0.0, v) * (1 + 1e-7)).limit_denominator(10**9) + Fr(1, 10**9) for v in res.x]
    for E in H:
        assert sum(w[x] for x in range(n) if E >> x & 1) >= 1, "rounded w infeasible"
    return w, sum(w)

def greedy_cover(H, n):
    rem = list(H); cnt = 0
    while rem:
        deg = [sum(1 for E in rem if E >> x & 1) for x in range(n)]
        x = max(range(n), key=lambda v: deg[v]); cnt += 1
        rem = [E for E in rem if not (E >> x & 1)]
    return cnt

def S_of(G):
    return sum(popcount(G[i] & G[j]) for i in range(4) for j in range(i + 1, 4))

def check_family(name, H, n, k, exhaustive_limit=60, samples=200000, seed=1):
    H = sorted(set(H))
    t = tau_exact(H, n)
    mQ = min(t, (3 * (2 * t - k - 2)) // 2 + 1)
    rng = random.Random(seed)
    if mQ < 1:
        print(f"{name}: n={n} k={k} |H|={len(H)} tau={t} m_Q={mQ} <= 0: statement vacuous, skipped"); return
    if len(H) <= exhaustive_limit:
        Smin = min(S_of(G) for G in itertools.combinations_with_replacement(H, 4))
        mode = 'exhaustive'
    else:
        Smin = min(S_of([rng.choice(H) for _ in range(4)]) for _ in range(samples))
        mode = 'sampled'
    assert Smin >= mQ, (name, Smin, mQ)
    w, mass = frac_transversal(H, n)
    assert mass <= Fr(6 * k, mQ) + Fr(1, 10**6), (name, mass, Fr(6 * k, mQ))
    g = greedy_cover(H, n)
    assert t <= g <= float(mass) * math.log(len(H)) + 1 + 1e-9, (name, t, g, mass)
    assert len(H) >= math.exp((t - 1) * mQ / (6 * k)) - 1e-9, (name, len(H), (t - 1) * mQ / (6 * k))
    print(f"{name}: n={n} k={k} |H|={len(H)} tau={t} m_Q={mQ} minS({mode})={Smin} tau*<={float(mass):.4f} "
          f"(bound {6*k/mQ:.3f}) greedy={g} ln|H|={math.log(len(H)):.3f} >= {(t-1)*mQ/(6*k):.3f}  PASS")

def padded_complete(m, g, seed=0):
    """all (4m-1)-subsets of [7m-2], each padded by a group point p_j, j = random group in [g]."""
    n0 = 7 * m - 2; rng = random.Random(seed); H = []
    for c in itertools.combinations(range(n0), 4 * m - 1):
        E = sum(1 << v for v in c) | (1 << (n0 + rng.randrange(g)))
        H.append(E)
    return H, n0 + g

def random_72(n, k, m, rng):
    while True:
        H = list({sum(1 << v for v in rng.sample(range(n), rng.randint(1, k))) for _ in range(m)})
        if is_72(H, n): return H

if __name__ == '__main__':
    check_family('K_9^5', complete(9, 5), 9, 5)
    check_family('K_10^6', complete(10, 6), 10, 6)
    check_family('K_12^7', complete(12, 7), 12, 7)
    check_family('K_8^5', complete(8, 5), 8, 5)
    H, n = padded_complete(2, 5); check_family('padded K_12^7 (g=5)', H, n, 8)
    rng = random.Random(7)
    for (nn, kk) in [(9, 5), (10, 6), (12, 7), (8, 5), (7, 4)]:
        full = complete(nn, kk)
        for i in range(4):
            sub = [E for E in full if rng.random() < 0.5 + 0.12 * i]
            check_family(f'random subfamily of K_{nn}^{kk} #{i}', sub, nn, kk)
    for i in range(20):
        n = rng.randint(6, 9); k = rng.randint(3, n - 1); m = rng.randint(4, 20)
        H = random_72(n, k, m, rng)
        check_family(f'random#{i}', H, n, k)
    print("ALL PASS")
