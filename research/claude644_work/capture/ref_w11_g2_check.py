#!/usr/bin/env python3
"""
ref_w11_g2_check.py  (referee w11, architecture#0 = Lemma G2; exact, stdlib only)

Independent checks for the referee report on Lemma G2 (universal rounding shift):

 (1) MILNER n=6 by brute force: the largest family of pairwise-intersecting, pairwise-incomparable
     nonempty subsets of a 6-set has exactly 15 members (= C(6,4)).  Max clique in the 63-vertex graph
     (nonempty subsets; edge iff intersecting and incomparable), Bron-Kerbosch with pivoting.
     Also the elementary bound: max intersecting family on a 6-set = 32 (pairing argument only; and the
     max clique of the "intersecting" graph on 63 vertices is checked to be 32 as an independent confirmation).
 (2) The catalogue: maximal_cells of each orbit form an antichain (so the parent count per window is an
     antichain count, and Milner applies); count orbits attaining 15 parent cells in some window and 32
     downset cells in some window; and confirm the 15-parent windows are exactly the complements
     {all 4-subsets of [7]\\{j}}, i.e. cells = {j} u (2-subset), an extremal Milner family.
 (3) The rounding arithmetic: the claim writes "window >= ceil(v_j) - 14"; with 15 cells of mass 0.99 the
     floored window is 0 while ceil(14.85) - 14 = 1.  The correct statement is window' >= floor(v) - 14
     (>= u - 14 for integer u <= v).  Exhaustive small check with Fractions.
"""
import json, sys
from fractions import Fraction
from itertools import combinations, product
from math import floor, ceil

CAT = "/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_full_support_catalog.json"

def max_clique(n, adj):
    best = [0]
    bestset = [frozenset()]
    def bk(R, P, X):
        if not P and not X:
            if len(R) > best[0]:
                best[0] = len(R); bestset[0] = frozenset(R)
            return
        if len(R) + len(P) <= best[0]:
            return
        u = max(P | X, key=lambda v: len(adj[v] & P))
        for v in list(P - adj[u]):
            bk(R | {v}, P & adj[v], X & adj[v])
            P = P - {v}; X = X | {v}
    bk(set(), set(range(n)), set())
    return best[0], bestset[0]

def check_milner6():
    sets = list(range(1, 64))  # nonempty subsets of a 6-set as bitmasks
    idx = {S: i for i, S in enumerate(sets)}
    # antichain + intersecting graph
    adj = {i: set() for i in range(len(sets))}
    adj_int = {i: set() for i in range(len(sets))}
    for a, b in combinations(sets, 2):
        if a & b:
            adj_int[idx[a]].add(idx[b]); adj_int[idx[b]].add(idx[a])
            if (a & b) != a and (a & b) != b:  # incomparable
                adj[idx[a]].add(idx[b]); adj[idx[b]].add(idx[a])
    m, fam = max_clique(len(sets), adj)
    print(f"[milner n=6] max intersecting antichain on 6 points = {m} (Milner: C(6,4)=15)")
    assert m == 15
    m2, _ = max_clique(len(sets), adj_int)
    print(f"[elementary n=6] max intersecting family on 6 points = {m2} (2^5 = 32)")
    assert m2 == 32

def check_catalogue():
    d = json.load(open(CAT))
    orbits = d["orbits"]
    print("[catalogue] keys of an orbit:", sorted(orbits[0].keys()))
    n15 = 0; n32 = 0; extremal15_all_2sets = 0; windows15 = 0
    for o in orbits:
        M = o["maximal_cells"]
        # antichain check
        for a in M:
            for b in M:
                if a != b:
                    assert (a & b) != a, ("maximal_cells not an antichain", M)
        # downset
        cells = set()
        for mm in M:
            sub = mm
            while True:
                cells.add(sub)
                if sub == 0: break
                sub = (sub - 1) & mm
        hit15 = False; hit32 = False
        for j in range(7):
            par = [mm for mm in M if mm >> j & 1]
            dn = [c for c in cells if c >> j & 1]
            if len(par) == 15:
                hit15 = True; windows15 += 1
                # are these cells exactly {j} u 2-subset of the other six?
                if all(bin(mm).count("1") == 3 for mm in par):
                    extremal15_all_2sets += 1
            if len(dn) == 32:
                hit32 = True
        n15 += hit15; n32 += hit32
    print(f"[catalogue] orbits with a 15-parent window: {n15}; such windows in total: {windows15}, "
          f"of which all parents are 3-sets ({{j}} u pair): {extremal15_all_2sets}; orbits with a 32-cell downset window: {n32}")

def check_rounding():
    # 15 cells of mass 99/100 each: v = 14.85, floored window = 0
    masses = [Fraction(99, 100)] * 15
    v = sum(masses); w = sum(floor(x) for x in masses)
    print(f"[rounding] v = {float(v)}, floored window = {w}, ceil(v)-14 = {ceil(v)-14}, floor(v)-14 = {floor(v)-14}")
    assert w < ceil(v) - 14, "claim's intermediate inequality would hold here -- unexpected"
    assert w >= floor(v) - 14
    # exhaustive: masses in {0, 1/4, 1/2, 3/4, 1, 5/4, 3/2, 7/4} over up to 15 cells is too many; sample the
    # worst case structure instead: for every count c <= 15 and every fractional part f in {0,1/100,...,99/100},
    # c cells of mass q + f: floor-sum >= floor(v) - (c-1) always holds, ceil version fails for some.
    ok_floor = True; fail_ceil = 0
    for c in range(1, 16):
        for k10 in range(100):
            f = Fraction(k10, 100)
            v = c * (1 + f); w = c * 1
            if w < floor(v) - 14: ok_floor = False
            if w < ceil(v) - 14: fail_ceil += 1
    print(f"[rounding] floor-version never violated: {ok_floor}; ceil-version violated in {fail_ceil} configurations")
    assert ok_floor and fail_ceil > 0

if __name__ == "__main__":
    check_milner6()
    check_catalogue()
    check_rounding()
    print("REFEREE CHECKS DONE")
