#!/usr/bin/env python3
"""End-to-end test of Lemma D (anchored pencil host bound).

For random small families H (NOT assumed (7,2)) we compute t = tau(H) exactly,
pick an edge E and a set R disjoint from E, compute q = tau(H[E u R]).
Lemma D (hand version) says: if 2*ceil(e/4) <= t-1 and
      q > max(2*ceil(e/4), |R| + 6*ceil(e/4) - 2t + 2)
then H is not (7,2).  We verify this by EXPLICITLY building the seven edges
with the split used in the hand proof and checking they have no <=2 cover.
"""
import itertools, random, sys

# Fano plane with pencil point p0=0: l1={0,1,3} (a=1,a'=3), l2={0,4,5} (b=4,b'=5),
# l3={0,2,6} (c=2,c'=6); m-lines {1,2,4},{2,3,5},{3,4,6},{5,6,1}.
L1, L2, L3 = {0, 1, 3}, {0, 4, 5}, {0, 2, 6}
M = [{1, 2, 4}, {2, 3, 5}, {3, 4, 6}, {5, 6, 1}]
LINES = [L1, L2, L3] + M

def tau(edges, V):
    edges = [set(G) for G in edges]
    if not edges:
        return 0
    for s in range(0, len(V) + 1):
        for T in itertools.combinations(V, s):
            Ts = set(T)
            if all(G & Ts for G in edges):
                return s
    return None

def no_small_cover(edges, V):
    for x in V:
        if all(x in G for G in edges):
            return False
    for x, y in itertools.combinations(V, 2):
        if all(x in G or y in G for G in edges):
            return False
    return True

def ceil4(e):
    return -(-e // 4)

def trial(rng):
    n = rng.randint(7, 11)
    V = list(range(n))
    H = list({frozenset(rng.sample(V, rng.randint(2, 5))) for _ in range(rng.randint(8, 40))})
    t = tau(H, V)
    E = rng.choice(H)
    e = len(E)
    c4 = ceil4(e)
    if 2 * c4 > t - 1:
        return 'skip'
    rest = [x for x in V if x not in E]
    R = set(rng.sample(rest, rng.randint(0, len(rest))))
    U = set(E) | R
    HU = [G for G in H if G <= U]
    q = tau(HU, V)
    bound = max(2 * c4, len(R) + 6 * c4 - 2 * t + 2)
    if q <= bound:
        return 'nobad'
    # build labels exactly as in the hand proof
    El = sorted(E)
    lab = {}
    classes = {4: [], 5: [], 2: [], 6: []}   # b,b',c,c'
    order = [4, 5, 2, 6]
    for i, x in enumerate(El):
        lab[x] = order[i % 4]
    rho = t - 1 - 2 * c4
    Rl = sorted(R)
    if len(Rl) <= 2 * rho:
        ra = (len(Rl) + 1) // 2
        rap = len(Rl) // 2
        w = 0
    else:
        ra = rap = rho
        w = len(Rl) - 2 * rho
    for i, x in enumerate(Rl):
        if i < ra:
            lab[x] = 1
        elif i < ra + rap:
            lab[x] = 3
        else:
            lab[x] = 0
    for x in V:
        if x not in U:
            lab[x] = 0
    chosen = [E]
    for Lk in (L2, L3):
        forb = {x for x in U if lab[x] in Lk}
        cands = [G for G in HU if not (G & forb)]
        assert len(forb) <= q - 1, (len(forb), q)
        assert cands, "host edge must exist since |forb| < q"
        chosen.append(cands[0])
    for Lk in M:
        forb = {x for x in V if lab[x] in Lk}
        assert len(forb) <= t - 1, (len(forb), t)
        cands = [G for G in H if not (G & forb)]
        assert cands, "global edge must exist since |forb| < t"
        chosen.append(cands[0])
    assert no_small_cover(chosen, V), "construction failed to be bad!"
    return 'bad-built'

def main(N=20000, seed=7):
    rng = random.Random(seed)
    from collections import Counter
    c = Counter(trial(rng) for _ in range(N))
    print(dict(c))

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20000)
