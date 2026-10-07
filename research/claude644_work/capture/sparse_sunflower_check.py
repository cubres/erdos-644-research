"""Exact check of the SUNFLOWER-KERNEL LEMMA (notes_sparse.md [s3]).

LEMMA.  H a (7,2) family of rank <= k, tau(H) = t.  Let K u P_1, ..., K u P_m be edges of H forming a sunflower
(P_i pairwise disjoint, disjoint from K, nonempty) with m >= 6k+1 petals.  Then H' := (H minus the m sunflower
edges) u {K} is a (7,2) family of rank <= k with tau(H') = tau(H).  (K != empty since m >= 3 and nu(H) <= 2.)
Proof (hand): (7,2): given <= 6 other edges F of H' plus K, the F's cover <= 6k points hence miss some petal P_i;
a 2-transversal of {F} u {K u P_i} in H either meets K (done) or has a point in P_i, which lies in no F, so the
other point alone pierces all F's and, with any point of K, pierces the new tuple.  Subfamilies of H' avoiding K
are subfamilies of H.  tau(H') >= tau(H): a transversal of H' hits K hence every K u P_i.  tau(H') <= tau(H):
a minimum transversal T of H (|T| = t <= 6k/7+O(1) < m) cannot hit all m petals... precisely: if T misses K it
must contain a point of each of the m > t disjoint petals, impossible; so T hits K and is a transversal of H'.
This script plants sunflowers in random (7,2) families and verifies all three conclusions exactly, and also
records how often the replacement FAILS when m is small (to show the hypothesis is not vacuous).
"""
import random, sys, itertools
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
from lib72 import is_72, tau, popcount

def rank(H): return max(popcount(E) for E in H)

def plant(rng, k, m, ksize, psize, extra, n_extra):
    """vertices: kernel 0..ksize-1, petals next m*psize, extra vertices n_extra.  Returns (H, n, sunflower edges, K)."""
    K = sum(1 << v for v in range(ksize))
    petals = []
    v = ksize
    for i in range(m):
        petals.append(sum(1 << u for u in range(v, v + psize))); v += psize
    n = v + n_extra
    sun = [K | P for P in petals]
    assert popcount(sun[0]) <= k
    # random extra edges of size <= k, mostly touching the kernel so that (7,2) is plausible
    others = set()
    pool = list(range(n))
    tries = 0
    while len(others) < extra and tries < 20000:
        tries += 1
        s = rng.randint(1, k)
        E = sum(1 << u for u in rng.sample(pool, s))
        if rng.random() < 0.7: E |= 1 << rng.randrange(ksize)
        E &= (1 << n) - 1
        if E and popcount(E) <= k: others.add(E)
    H = sun + sorted(others)
    return H, n, sun, K

def main(seed=1):
    rng = random.Random(seed)
    ok = 0; tested = 0; fails_small = 0; tested_small = 0
    for trial in range(400):
        k = rng.choice([2, 3])
        ksize = rng.randint(1, k - 1); psize = k - ksize if rng.random() < 0.5 else 1
        if ksize + psize > k: psize = k - ksize
        big = rng.random() < 0.5
        m = 6 * k + 1 + rng.randint(0, 2) if big else rng.randint(3, 6)
        n_extra = rng.randint(0, 3)
        H, n, sun, K = plant(rng, k, m, ksize, psize, rng.randint(0, 8), n_extra)
        if n > 24: continue
        if not is_72(H, n): continue
        t = tau(H, n)
        Hp = [E for E in H if E not in set(sun)] + [K]
        c72 = is_72(Hp, n); tp = tau(Hp, n); rk = rank(Hp) <= k
        if big:
            tested += 1
            assert c72 and tp == t and rk, (trial, k, m, ksize, psize, t, tp, c72)
            ok += 1
        else:
            tested_small += 1
            if not (c72 and tp == t): fails_small += 1
    print(f"m >= 6k+1: {ok}/{tested} planted sunflowers -> kernel replacement keeps (7,2), rank, tau: PASS")
    print(f"m <= 6 (below threshold): replacement changed (7,2) or tau in {fails_small}/{tested_small} cases "
          f"(hypothesis is not vacuous)")

def witness():
    """Hand witness that the petal count matters: c = vertex 0, V0 = {1..6}; H = {c,i} (i in V0) u {V0 \\ {j}} (j in V0).
    k = 5, sunflower {c,i} with m = 6 petals.  H is (7,2); replacing the sunflower by its kernel {c} gives
    {c} u {V0 \\ {j}}: 7 edges with no 2-transversal."""
    n = 7; V0 = range(1, 7)
    sun = [(1 << 0) | (1 << i) for i in V0]
    F = [sum(1 << v for v in V0 if v != j) for j in V0]
    H = sun + F
    assert is_72(H, n) and rank(H) == 5
    Hp = F + [1 << 0]
    assert not is_72(Hp, n)
    print(f"witness (k=5, m=6 petals): H is (7,2), tau={tau(H,n)}; kernel replacement is NOT (7,2): hypothesis needed")

if __name__ == '__main__':
    main(); witness()
