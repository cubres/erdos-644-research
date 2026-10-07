#!/usr/bin/env python3
"""w4_tcglobal_fano_exact.py -- exact-integer Fano-downset (= Fano-LABELLED) tuple test for type-closed families,
using note Lemma 7.63: seven types a^(1..7) on the Fano lines are realizable in capacities x iff for every part i:
  a_i^(j) <= x_i,  sum_{j in L} a_i^(j) <= 2 x_i (every Fano line L of ROW labels),  sum_j a_i^(j) <= 4 x_i.
(Rows are indexed by Fano POINTS in 7.63; by duality rows<->lines is the same structure.)  Also exact tau*.
Cross-checked against the LP in w4_tcglobal_fanofree_search.py by test_crosscheck()."""
import itertools
from fractions import Fraction
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
AUTOS = []
for perm in itertools.permutations(range(7)):
    if all(tuple(sorted(perm[x] for x in l)) in LINES for l in LINES): AUTOS.append(perm)
assert len(AUTOS) == 168
def canon(assign):
    return min(tuple(assign[p[j]] for j in range(7)) for p in AUTOS)
_orb = {}
def orbit_reps(nt):
    if nt not in _orb: _orb[nt] = sorted(set(canon(a) for a in itertools.product(range(nt), repeat=7)))
    return _orb[nt]
def part_ok(loads, cap):
    if max(loads) > cap: return False
    if sum(loads) > 4*cap: return False
    return all(sum(loads[j] for j in L) <= 2*cap for L in LINES)
def fano_tuple(types, caps):
    for assign in orbit_reps(len(types)):
        if all(part_ok([types[assign[j]][i] for j in range(7)], caps[i]) for i in range(len(caps))):
            return assign
    return None
def tau_star(types, caps):
    n = len(caps); best = None
    for m in itertools.product(range(n), repeat=len(types)):
        cost = 0
        for i in range(n):
            need = [caps[i]-types[a][i] for a in range(len(types)) if m[a] == i]
            if need: cost += max(0, max(need))
        best = cost if best is None else min(best, cost)
    return best
def intersecting(types, caps):
    return all(any(types[a][i]+types[b][i] > caps[i] for i in range(len(caps)))
               for a in range(len(types)) for b in range(a, len(types)))
def test_crosscheck(trials=300, seed=5):
    import random
    from w4_tcglobal_fanofree_search import fano_exists
    random.seed(seed); bad = 0
    for _ in range(trials):
        caps = [random.randint(3,20) for _ in range(3)]
        types = [tuple(random.randint(0,c) for c in caps) for _ in range(2)]
        if (fano_tuple(types, caps) is None) != (fano_exists(types, caps) is None): bad += 1
    return bad
if __name__ == '__main__':
    print("crosscheck mismatches (closed form vs LP):", test_crosscheck())
    t = [(22,1),(5,18)]; c = (32,26)
    print("non-intersecting example caps", c, "types", t, "tau*", tau_star(t,c), "k", 23,
          "fano tuple:", fano_tuple(t,c), "intersecting:", intersecting(t,c))
