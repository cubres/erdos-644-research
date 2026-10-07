#!/usr/bin/env python3
"""Exact combinatorial checks for the pencil / two-anchor arguments.

Run:  python3 fano_pencil_check.py
Pure standard library; all checks are exhaustive over finitely many cases.

1. Fano plane facts (safe line sets).
2. Lemma P (pencil lemma with protrusion, ambient anchor): for every vertex
   class and every membership pattern the construction permits, the union
   of the lines of sigma(x) misses some Fano point.
3. Two disjoint anchors: grid (quadrant) cover and C5 cover kill every
   cross pair; loads as claimed.
"""
from itertools import combinations, product

# Fano plane on F_2^3 \ {0}; points encoded as ints 1..7 (bit vectors)
P0 = 0b001
a, b = 0b010, 0b100
ap, bp = a ^ P0, b ^ P0
c, cp = a ^ b, a ^ b ^ P0
POINTS = [1, 2, 3, 4, 5, 6, 7]
LINES = sorted({frozenset([x, y, x ^ y]) for x in POINTS for y in POINTS if x != y},
               key=lambda s: sorted(s))
assert len(LINES) == 7
l1, l2, l3 = frozenset([P0, a, ap]), frozenset([P0, b, bp]), frozenset([P0, c, cp])
M1, M2, M3, M4 = (frozenset([a, b, c]), frozenset([ap, bp, c]),
                  frozenset([ap, b, cp]), frozenset([a, bp, cp]))
for L in (l1, l2, l3, M1, M2, M3, M4):
    assert L in LINES, L
assert len({l1, l2, l3, M1, M2, M3, M4}) == 7


def safe(lines):
    cov = set()
    for L in lines:
        cov |= L
    return len(cov) < 7


# 1. safe-set facts
for r in range(0, 8):
    for S in combinations(LINES, r):
        s = safe(S)
        if r <= 2:
            assert s
        elif r == 3:
            conc = len(S[0] & S[1] & S[2]) == 1
            assert s == (not conc)
        elif r == 4:
            missing_pt = any(all(p not in L for L in S) for p in POINTS)
            assert s == missing_pt
        else:
            assert not s
print("[1] Fano safe-set facts: OK")

# 2. Lemma P.  Edges: G_l1 = E (fixed); G_l2, G_l3 host rows; m-lines global.
# Avoidance prescribed by the construction:
#   G_l1 = E : contains exactly E-classes (Eb,Eb',Ec,Ec'); nothing else.
#   G_l2 avoids Rp, Eb, Eb' ; its outside part is O2 (may be anything else)
#   G_l3 avoids Rp, Ec, Ec' ; outside part O3
#   M1 avoids Ra, Eb, Ec, O2 ; M4 avoids Ra, Eb', Ec', O2
#   M2 avoids Ra', Eb', Ec, O3 ; M3 avoids Ra', Eb, Ec', O3
# A vertex class may lie in an edge unless forbidden.  Outside vertices are
# split by (in O2?, in O3?); vertices outside U not in O2 u O3 lie in no host row.
edges = {'l1': l1, 'l2': l2, 'l3': l3, 'M1': M1, 'M2': M2, 'M3': M3, 'M4': M4}
forbid = {
    'M1': {'Ra', 'Eb', 'Ec', 'O2'}, 'M4': {'Ra', 'Ebp', 'Ecp', 'O2'},
    'M2': {'Rap', 'Ebp', 'Ec', 'O3'}, 'M3': {'Rap', 'Eb', 'Ecp', 'O3'},
}
classes = ['Eb', 'Ebp', 'Ec', 'Ecp', 'Ra', 'Rap', 'Rp', 'out00', 'out10', 'out01', 'out11']


def possible_edges(cls):
    """Edges that may contain a vertex of this class (worst case: all allowed)."""
    res = []
    inE = cls.startswith('E')
    if inE:
        res.append('l1')
    # host rows l2,l3
    if cls in ('Ec', 'Ecp', 'Ra', 'Rap', 'out10', 'out11'):
        res.append('l2')  # l2 row avoids Rp,Eb,Ebp; outside only if in O2
    if cls in ('Eb', 'Ebp', 'Ra', 'Rap', 'out01', 'out11'):
        res.append('l3')
    # global m-lines: may contain anything not forbidden; O2/O3 membership
    tags = {cls}
    if cls in ('out10', 'out11'):
        tags.add('O2')
    if cls in ('out01', 'out11'):
        tags.add('O3')
    for mname, fb in forbid.items():
        if not (tags & fb):
            res.append(mname)
    return res


for cls in classes:
    pe = possible_edges(cls)
    lines = [edges[n] for n in pe]
    assert safe(lines), (cls, pe)
    free = [p for p in POINTS if all(p not in L for L in lines)]
    print(f"    class {cls:6s} may lie in {pe}; free points {free}")
print("[2] Lemma P free-point check: OK (every class keeps a free Fano point)")

# 3. Two disjoint anchors.
# (a) grid: A1 halves X,X' ; A2 halves Y,Y'; four requests X u Y, X u Y', X' u Y, X' u Y'.
types_A1 = {'X': {0, 1}, "X'": {2, 3}}          # request indices avoiding the point
types_A2 = {'Y': {0, 2}, "Y'": {1, 3}}
for s, t in product(types_A1.values(), types_A2.values()):
    assert s & t
print("[3a] grid: every cross pair lies in a common request: OK")
# (b) C5 cover: A1 types = edges of the 5-cycle, A2 types = rotations of {0,2,4}
C5_edges = [frozenset({i, (i + 1) % 5}) for i in range(5)]
covers = [frozenset({i % 5, (i + 2) % 5, (i + 4) % 5}) for i in range(5)]
for s in C5_edges:
    for t in covers:
        assert s & t, (s, t)
load_A1 = [sum(1 for s in C5_edges if j in s) for j in range(5)]
load_A2 = [sum(1 for t in covers if j in t) for j in range(5)]
assert load_A1 == [2] * 5 and load_A2 == [3] * 5
print("[3b] C5 cover: cross-intersecting, each request gets 2 A1-classes and 3 A2-classes: OK")
print("ALL CHECKS PASSED")
