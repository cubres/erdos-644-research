#!/usr/bin/env python3
"""Randomized check of the PENCIL construction (Lemmas C and D).

Fano plane on points 0..6.  Pick a point p0.  The three lines through p0
form the pencil; the other four lines ("m-lines") all miss p0.
Labeling:  every vertex outside the host U gets label p0.
  Lemma C (no anchor): U is labeled on all 7 points.
  Lemma D (one anchor E in U on pencil line l1): E is labeled on the four
  points off l1; R = U \\ E is labeled on the three points of l1.
Edges:  pencil lines use edges contained in U (host edges) avoiding the
labels on the line (or the anchor E itself for l1); m-lines use ARBITRARY
edges of the family avoiding the U-vertices labeled on the line.
Claim: whenever all seven edges exist, they have no transversal of size <= 2.
This script builds random families (no (7,2) assumption), random hosts and
labelings, runs the construction, and verifies the claim exhaustively.
"""
import itertools, random, sys

LINES = [frozenset(s) for s in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]

def has_small_transversal(edges, V):
    for x in V:
        if all(x in G for G in edges):
            return True
    for x, y in itertools.combinations(V, 2):
        if all((x in G) or (y in G) for G in edges):
            return True
    return False

def run_trial(rng, anchored):
    n = rng.randint(8, 16)
    V = list(range(n))
    nedges = rng.randint(20, 120)
    H = []
    for _ in range(nedges):
        sz = rng.randint(2, max(2, n // 2 + 1))
        H.append(frozenset(rng.sample(V, sz)))
    H = list(set(H))
    p0 = rng.randrange(7)
    pencil = [L for L in LINES if p0 in L]
    mlines = [L for L in LINES if p0 not in L]
    if anchored:
        E = rng.choice(H)
        l1 = pencil[0]
        others = [x for x in V if x not in E]
        R = set(rng.sample(others, rng.randint(0, len(others))))
        U = set(E) | R
        lab = {}
        off_l1 = [p for p in range(7) if p not in l1]
        on_l1 = sorted(l1)
        for x in E:
            lab[x] = rng.choice(off_l1)
        for x in R:
            lab[x] = rng.choice(on_l1)
    else:
        U = set(rng.sample(V, rng.randint(1, n)))
        lab = {x: rng.randrange(7) for x in U}
    for x in V:
        if x not in U:
            lab[x] = p0
    chosen = []
    for L in LINES:
        if anchored and L == pencil[0]:
            chosen.append(E)
            continue
        forbidden = {x for x in U if lab[x] in L}
        if L in pencil:
            cands = [G for G in H if G <= U and not (G & forbidden)]
        else:
            cands = [G for G in H if not (G & forbidden)]
        if not cands:
            return None
        chosen.append(rng.choice(cands))
    # sanity: every vertex x lies only in edges of lines missing lab[x]
    for idx, L in enumerate(LINES):
        for x in chosen[idx]:
            assert lab[x] not in L, (x, lab[x], L)
    return not has_small_transversal(chosen, V)

def main(trials=200000, seed=1):
    rng = random.Random(seed)
    stats = {True: [0, 0], False: [0, 0]}
    for i in range(trials):
        anchored = (i % 2 == 0)
        r = run_trial(rng, anchored)
        if r is None:
            continue
        stats[anchored][0] += 1
        if r:
            stats[anchored][1] += 1
        else:
            print("COUNTEREXAMPLE FOUND", anchored)
            return 1
    print("anchored   : constructions completed %d, all bad 7-tuples: %s" % (stats[True][0], stats[True][0] == stats[True][1]))
    print("unanchored : constructions completed %d, all bad 7-tuples: %s" % (stats[False][0], stats[False][0] == stats[False][1]))
    return 0

if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 200000))
