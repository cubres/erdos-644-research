#!/usr/bin/env python3
"""End-to-end test of Lemma D' (anchored pencil bound with protruding host edges).

Claim: H with tau(H)=t, E in H, R disjoint from E, U = E u R, m >= 0 with
2*ceil(e/4) + m <= t-1.  If
     q_m := tau(H^(m)_U) > max(2*ceil(e/4), |R| + 6*ceil(e/4) + 2m - 2t + 2)
then H is not (7,2).  Construction: labels as in Lemma D; host edges for l2,l3
come from H^(m)_U (edges with <= m points outside U); m-lines M1={1,2,4} and
M4={5,6,1} additionally avoid the outside part of the l2 edge, M2={2,3,5} and
M3={3,4,6} avoid the outside part of the l3 edge.  We verify on random families
that the resulting 7 edges have no transversal of size <= 2.
"""
import itertools, random, sys
from collections import Counter

L1, L2, L3 = {0, 1, 3}, {0, 4, 5}, {0, 2, 6}
M1, M2, M3, M4 = {1, 2, 4}, {2, 3, 5}, {3, 4, 6}, {5, 6, 1}

def tau(edges, V):
    edges = [set(G) for G in edges]
    if not edges:
        return 0
    for s in range(0, len(V) + 1):
        for T in itertools.combinations(V, s):
            Ts = set(T)
            if all(G & Ts for G in edges):
                return s

def no_small_cover(edges, V):
    for x in V:
        if all(x in G for G in edges):
            return False
    for x, y in itertools.combinations(V, 2):
        if all(x in G or y in G for G in edges):
            return False
    return True

def trial(rng):
    n = rng.randint(8, 12)
    V = list(range(n))
    H = list({frozenset(rng.sample(V, rng.randint(2, 5))) for _ in range(rng.randint(10, 45))})
    t = tau(H, V)
    E = rng.choice(H)
    e = len(E)
    c4 = -(-e // 4)
    m = rng.randint(0, 2)
    if 2 * c4 + m > t - 1:
        return 'skip'
    rest = [x for x in V if x not in E]
    R = set(rng.sample(rest, rng.randint(0, len(rest))))
    U = set(E) | R
    Hm = [G for G in H if len(G - U) <= m]
    qm = tau(Hm, V)
    bound = max(2 * c4, len(R) + 6 * c4 + 2 * m - 2 * t + 2)
    if qm <= bound:
        return 'nobad'
    lab = {}
    order = [4, 5, 2, 6]
    for i, x in enumerate(sorted(E)):
        lab[x] = order[i % 4]
    rho = t - 1 - 2 * c4 - m
    Rl = sorted(R)
    if len(Rl) <= 2 * rho:
        ra, rap = (len(Rl) + 1) // 2, len(Rl) // 2
    else:
        ra = rap = rho
    for i, x in enumerate(Rl):
        lab[x] = 1 if i < ra else (3 if i < ra + rap else 0)
    chosen = [E]
    host = []
    for Lk in (L2, L3):
        forb = {x for x in U if lab[x] in Lk}
        assert len(forb) <= qm - 1
        cands = [G for G in Hm if not (G & forb)]
        assert cands
        G = rng.choice(cands)
        host.append(G)
        chosen.append(G)
    O2 = set(host[0]) - U
    O3 = set(host[1]) - U
    for Mk, extra in ((M1, O2), (M4, O2), (M2, O3), (M3, O3)):
        forb = {x for x in U if lab[x] in Mk} | extra
        assert len(forb) <= t - 1, (len(forb), t)
        cands = [G for G in H if not (G & forb)]
        assert cands
        chosen.append(rng.choice(cands))
    assert no_small_cover(chosen, V), "FAILED"
    return 'bad-built'

def main(N=30000, seed=11):
    rng = random.Random(seed)
    print(dict(Counter(trial(rng) for _ in range(N))))

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 30000)
