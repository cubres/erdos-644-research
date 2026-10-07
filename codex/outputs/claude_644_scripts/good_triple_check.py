#!/usr/bin/env python3
"""Exact check of the static good-triple union bound (GT) used for Theorem G.

GT: if G1,G2,G3 are edges with empty common intersection and
    |G1 u G2 u G3| <= 2t - 4,
then G1,G2,G3 together with four edges avoiding sets of size <= t-1
(the four 'm-line' requests) form a family with no transversal of size <= 2.

The script (a) enumerates ALL membership-count vectors of a good triple
(sizes of the six nonempty Venn cells over three sets with empty triple
cell), with union u <= 2t-4, for t up to T, and checks that the balanced
parity split gives four m-line requests of size <= t-1; (b) on random
explicit instances builds the seven edges (m-line edges chosen as the
complements of the requests inside a big universe, i.e. worst case where
the responses use every allowed vertex) and verifies exhaustively that no
<=2-point transversal exists.
"""
import itertools, random, sys

def split_bal(n):
    return (n + 1) // 2, n // 2

def check_counts(T=40):
    worst = 0
    for t in range(3, T + 1):
        for u in range(0, 2 * t - 3):
            # classes A (in G2&G3 or G2-only/G3-only assigned), B, C sizes with A+B+C=u
            # the labelling may place private vertices in either allowed pair; the
            # worst case for our fixed rule is any split (A,B,C) with A+B+C=u
            for A in range(u + 1):
                for B in range(u - A + 1):
                    C = u - A - B
                    a, ap = split_bal(A)
                    # choose which of b/b', c/c' carries the ceiling to minimise the max m-line
                    best = None
                    for (b, bp) in (split_bal(B), split_bal(B)[::-1]):
                        for (c, cp) in (split_bal(C), split_bal(C)[::-1]):
                            m = max(a + b + c, ap + bp + c, ap + b + cp, a + bp + cp)
                            best = m if best is None else min(best, m)
                    if best > t - 1:
                        print("FAIL", t, u, A, B, C, best)
                        return False
                    worst = max(worst, best - (u / 2))
    print("counts OK up to t=%d; max m-line minus u/2 = %.1f" % (T, worst))
    return True

L1, L2, L3 = {0, 1, 3}, {0, 4, 5}, {0, 2, 6}     # pencil at p0 = 0
M = [{1, 2, 4}, {2, 3, 5}, {3, 4, 6}, {5, 6, 1}]  # m-lines: (a,b,c),(a',b',c),(a',b,c'),(a,b',c')
PA, PB, PC = (1, 3), (4, 5), (2, 6)               # a,a' / b,b' / c,c'

def no_small_cover(edges, V):
    for x in V:
        if all(x in G for G in edges):
            return False
    for x, y in itertools.combinations(V, 2):
        if all(x in G or y in G for G in edges):
            return False
    return True

def random_instance(rng, t):
    # build a good triple with union <= 2t-4 inside a universe of size n
    u = rng.randint(3, 2 * t - 4)
    n = u + rng.randint(0, 6)
    V = list(range(n))
    W = V[:u]
    # random Venn cells with empty triple cell
    cells = {}
    for x in W:
        cells[x] = rng.choice(['12', '13', '23', '1', '2', '3'])
    G1 = {x for x in W if '1' in cells[x]}
    G2 = {x for x in W if '2' in cells[x]}
    G3 = {x for x in W if '3' in cells[x]}
    if not (G1 and G2 and G3):
        return None
    # labelling: G1 on line L1 must avoid {0,1,3} -> G1 cells in b/c pairs, etc.
    A = [x for x in W if cells[x] == '23'] + [x for x in W if cells[x] in ('2', '3') and rng.random() < 0.5]
    rest = [x for x in W if x not in A]
    B = [x for x in rest if cells[x] in ('13', '3', '1') and (cells[x] != '1' or rng.random() < 0.5)]
    C = [x for x in rest if x not in B]
    # check allowed: A vertices must avoid G1 ; B vertices avoid G2 ; C vertices avoid G3
    if any(x in G1 for x in A) or any(x in G2 for x in B) or any(x in G3 for x in C):
        return None
    lab = {}
    for cls, pair in ((A, PA), (B, PB), (C, PC)):
        h = (len(cls) + 1) // 2
        for i, x in enumerate(cls):
            lab[x] = pair[0] if i < h else pair[1]
    for x in V:
        if x not in lab:
            lab[x] = 0
    edges = [G1, G2, G3]
    for Mk in M:
        forb = {x for x in V if lab[x] in Mk}
        if len(forb) > t - 1:
            return 'toolarge'
        edges.append(set(V) - forb)   # worst case: response uses all allowed vertices
    return no_small_cover(edges, V)

def main():
    ok = check_counts(40)
    rng = random.Random(3)
    stats = {}
    for _ in range(20000):
        t = rng.randint(5, 9)
        r = random_instance(rng, t)
        stats[r] = stats.get(r, 0) + 1
    print(stats)
    return 0 if ok and stats.get(False, 0) == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
