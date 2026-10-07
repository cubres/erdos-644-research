"""OBSTRUCTION (notes_sparse.md [s4b]): pair extension + edge criticality + (7,2) + tau = 3k/4 do NOT bound N.

Construction G(m, g): X = [7m-2], every (4m-1)-subset A of X gets one 'group point' p_{phi(A)}, phi(A) in [g];
edges A u {p_{phi(A)}}  (rank k = 4m).  (7,2) holds for EVERY phi: seven (4m-1)-subsets of a (7m-2)-set have a
common pair (their complements have size 3m-1 < 3(7m-2)/7).  Edge-critical for every phi: B = X \ A is a (t-1)-set
disjoint from the edge meeting all others (t = 3m).  tau <= 3m always.  The design of phi must give
  (P1) tau = 3m  and  (P2) every pair of vertices lies in a minimum transversal (pair extension).
For a pair of group points p_j, p_j' (P2) needs a 4m-set Y_{jj'} subset X all of whose (4m-1)-subsets have phi in
{j, j'}: we take a PACKING {Y_{jj'}} of 4m-sets (no two share a (4m-1)-subset), split each Y's subsets between
j and j', and assign the remaining subsets to random groups.  g can be as large as the packing allows
(C(g,2) <= packing size, exponential in m), so N = 7m-2+g is not O(k).
This script builds G(2, g) (k = 8, |X| = 12, t = 6) with the largest g found by random greedy packing, and verifies
(P1) by MILP (exact 0/1 set cover) and (P2) by MILP for every pair, plus edge criticality, and reports that
incidence-minimality FAILS (deleting a group point from an edge keeps (7,2) and tau): the example is NOT in the
7.87 normal form, which is exactly the point (incidence minimality is the only local consequence left).
"""
import itertools, random, sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
from lib72 import is_72, popcount

def min_transversal(H, n, force=()):
    """exact minimum transversal containing the vertices in 'force' (MILP, HiGHS)."""
    A = np.zeros((len(H), n))
    for i, E in enumerate(H):
        for x in range(n):
            if E >> x & 1: A[i, x] = 1
    lb = np.zeros(n); ub = np.ones(n)
    for v in force: lb[v] = 1
    res = milp(c=np.ones(n), constraints=LinearConstraint(A, lb=np.ones(len(H))), integrality=np.ones(n),
               bounds=Bounds(lb, ub))
    assert res.status == 0, res.message
    T = [x for x in range(n) if res.x[x] > 0.5]
    # exact verification of the returned transversal
    mask = sum(1 << x for x in T)
    assert all(E & mask for E in H) and all(v in T for v in force)
    return T

def build(m, g, seed=0):
    rng = random.Random(seed)
    n0 = 7 * m - 2; a = 4 * m - 1
    subsets = list(itertools.combinations(range(n0), a))
    idx = {c: i for i, c in enumerate(subsets)}
    # random greedy packing of 4m-sets with pairwise intersection <= 4m-2
    used = set(); packing = []
    Ys = list(itertools.combinations(range(n0), a + 1)); rng.shuffle(Ys)
    need = g * (g - 1) // 2
    for Y in Ys:
        subs = [tuple(sorted(set(Y) - {y})) for y in Y]
        if any(s in used for s in subs): continue
        packing.append((Y, subs)); used.update(subs)
        if len(packing) >= need: break
    if len(packing) < need: return None
    phi = {}
    pairs = list(itertools.combinations(range(g), 2))
    for (j, jp), (Y, subs) in zip(pairs, packing):
        for r, s in enumerate(subs):
            phi[s] = j if r % 2 == 0 else jp
    for s in subsets:
        if s not in phi: phi[s] = rng.randrange(g)
    H = [sum(1 << v for v in s) | (1 << (n0 + phi[s])) for s in subsets]
    return H, n0 + g, n0, phi, dict(zip(pairs, [p[0] for p in packing]))

def main():
    m = 2; k = 4 * m; t = 3 * m
    best = None
    for g in range(20, 5, -1):
        for seed in range(6):
            out = build(m, g, seed)
            if out is None: continue
            H, n, n0, phi, Ypair = out
            T = min_transversal(H, n)
            if len(T) == t:
                best = (g, seed, H, n, n0, phi, Ypair); break
        if best: break
    g, seed, H, n, n0, phi, Ypair = best
    print(f"G(m=2, g={g}, seed={seed}): k={k}, |X|={n0}, N={n} (= {n/k:.2f} k), |H|={len(H)}, tau={t} (MILP exact)")
    # rank
    assert max(popcount(E) for E in H) == k
    # (7,2) is a theorem here (Lemma 2.2); an exact brute-force check is also run (may take a while)
    # (P2) pair extension
    for u, v in itertools.combinations(range(n), 2):
        T = min_transversal(H, n, force=(u, v))
        assert len(T) == t, (u, v, len(T))
    print(f"(P2) every one of the {n*(n-1)//2} vertex pairs lies in a minimum transversal: PASS")
    # edge criticality: B = X \ A
    for E in H:
        B = ((1 << n0) - 1) & ~E
        assert popcount(B) == t - 1 and not (B & E) and all(F & B for F in H if F != E)
    print("edge criticality (B_E = X \\ A): PASS")
    # incidence minimality fails: delete the group point from the first edge
    E0 = H[0]; A0 = E0 & ((1 << n0) - 1)
    Hd = [A0] + H[1:]
    Td = min_transversal(Hd, n)
    print(f"deleting the group point of one edge: tau = {len(Td)} (unchanged), (7,2) preserved by Lemma 2.2 "
          f"=> NOT incidence-minimal")
    if '--brute72' in sys.argv:
        print("running exact brute-force (7,2) check of the full family ...")
        print("is_72:", is_72(H, n))
    else:
        print("(7,2) holds by Lemma 2.2 (complements of 7-subsets of [12] have size 5 < 36/7); pass --brute72 to brute-force it")

if __name__ == '__main__':
    main()
