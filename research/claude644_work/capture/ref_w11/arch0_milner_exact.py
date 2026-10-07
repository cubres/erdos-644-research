#!/usr/bin/env python3
"""
arch0_milner_exact.py  (wave-11 referee of architecture#0 / Lemma G2; exact, pysat + stdlib)

Self-contained exact certificates for the three counting bounds used by Lemma G2, WITHOUT the Astra catalogue and
WITHOUT quoting Milner's theorem:

  (B32)  the cells (subsets of [7], none equal to [7]) that contain a fixed row j and pairwise do not cover [7]
         number at most 32;
  (B15)  if moreover the cells form an ANTICHAIN (the maximal used cells after Lemma 7.63's reassignment), they number
         at most 15  (= Milner's bound C(6,4) for intersecting Sperner families on a 6-set);
  (B64/B35) the total number of cells is at most 64, and of antichain cells at most 35 (= C(7,4), Milner on [7]).

Method: each bound is a maximum-clique question on an explicit compatibility graph; we ask a SAT solver whether a
clique of size (bound + 1) exists (UNSAT = certificate) and exhibit a clique of size (bound) (attained).
The catalogue check of arch/window_bound_check.py inspects only the maximal cells of the 715 maximal intersecting
families, which is NOT the same family of objects as the maximal used cells of an arbitrary bad tuple; this script
closes that gap.
"""
import sys
from itertools import combinations
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

FULL = 127

def max_clique_certificate(vertices, compatible, bound, name):
    """Prove: every pairwise-compatible subfamily of `vertices` has <= bound members, and bound is attained."""
    n = len(vertices)
    idx = {v: i + 1 for i, v in enumerate(vertices)}
    # (a) UNSAT for bound+1
    for target, expect in ((bound + 1, False), (bound, True)):
        clauses = []
        for a, b in combinations(vertices, 2):
            if not compatible(a, b):
                clauses.append([-idx[a], -idx[b]])
        card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=target, top_id=n, encoding=EncType.seqcounter)
        with Solver(name="cadical153", bootstrap_with=clauses + card.clauses) as s:
            sat = s.solve()
            assert sat == expect, (name, target, sat)
            if sat:
                model = set(l for l in s.get_model() if 0 < l <= n)
                chosen = [v for v in vertices if idx[v] in model]
                assert len(chosen) >= bound
                assert all(compatible(a, b) for a, b in combinations(chosen, 2))
                witness = chosen
    print(f"[{name}] max compatible family = {bound} (UNSAT at {bound+1}, witness of size {bound}: "
          f"{sorted(bin(c).count('1') for c in witness)[:40]})")
    return witness

def noncover(a, b):
    return (a | b) != FULL

def antichain_noncover(a, b):
    return (a | b) != FULL and (a & b) != a and (a & b) != b

def main():
    cells = [c for c in range(1, FULL) if c != FULL]          # nonempty proper subsets of [7] (empty cell irrelevant)
    win0 = [c for c in cells if c & 1]                         # cells containing row 0
    # B32: cells in the window of row 0, pairwise non-covering
    max_clique_certificate(win0, noncover, 32, "B32 window, any cells")
    # B15: antichain cells in the window of row 0, pairwise non-covering  (Milner n=6)
    max_clique_certificate(win0, antichain_noncover, 15, "B15 window, antichain cells")
    # B64: all cells pairwise non-covering (complements intersecting on [7]); the empty cell adds one -> 64 with it
    max_clique_certificate(cells, noncover, 63, "B63 nonempty cells, any")
    # B35: antichain of cells pairwise non-covering (Milner n=7)
    max_clique_certificate(cells, antichain_noncover, 35, "B35 all cells, antichain")
    # Milner on small n by the same method (sanity of the encoding): n=5 -> C(5,3)=10, n=4 -> C(4,3)=4
    for n, expect in ((4, 4), (5, 10), (6, 15)):
        U = (1 << n) - 1
        subs = [S for S in range(1, U + 1)]
        def inter_anti(a, b):
            return (a & b) != 0 and (a & b) != a and (a & b) != b
        max_clique_certificate(subs, inter_anti, expect, f"Milner n={n}")
    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    main()
