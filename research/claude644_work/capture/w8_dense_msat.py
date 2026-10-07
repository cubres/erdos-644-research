#!/usr/bin/env python3
"""w8_dense_msat.py -- SAT/CEGAR search for a COUNTEREXAMPLE to the multi-part ANCHORED statement:
   integer type set G (up-closed within rank r), anchor (e,0..0) in G, intersecting, continuous tau* >= T,
   and NO six types forming a Fano-labelled bad tuple with the anchor as a line (Lemma 7.63 per part).
Usage: python3 w8_dense_msat.py r e x1 [x2 ...] T
UNSAT (after CEGAR) => no such integer type set at these capacities (exact: clauses are exact, blocking
clauses come from exactly verified configurations).  SAT with no config => candidate counterexample (printed,
re-verified exactly by brute force)."""
import sys, time
from itertools import product
from pysat.solvers import Cadical153
from w8_dense_lib import all_types, minimal, anchored_config, fano_ok, tau_star, intersecting, leq

def main():
    args = list(map(int, sys.argv[1:]))
    r, caps, T = args[0], tuple(args[1:-1]), args[-1]
    e = caps[0]; N = sum(caps); p = len(caps)
    types = all_types(caps, r, amin=1)
    idx = {g: i+1 for i, g in enumerate(types)}
    S = Cadical153()
    ncl = 0
    anchor = (e,) + (0,)*(p-1)
    S.add_clause([idx[anchor]])
    # up-closure
    for g in types:
        for i in range(p):
            h = list(g); h[i] += 1; h = tuple(h)
            if h in idx: S.add_clause([-idx[g], idx[h]]); ncl += 1
    # intersecting: only pairs (g,h) with g+h<=caps; enough to use h maximal, but add all pairs g<=h-lex
    for a, g in enumerate(types):
        comp = tuple(c - x for c, x in zip(caps, g))
        # maximal h <= comp with |h|<=r: if |comp|<=r it is comp; otherwise all h<=comp with |h|=r
        if sum(comp) <= r:
            cands = [comp] if comp in idx else []
        else:
            cands = [h for h in product(*[range(c+1) for c in comp]) if sum(h) == r and h in idx]
        for h in cands:
            S.add_clause([-idx[g], -idx[h]]); ncl += 1
    # covering: every integer w, |w| = N-T+1, contains a type g with (g_i==0 or g_i<w_i) for all i
    target = N - T + 1
    ncov = 0
    for w in product(*[range(c+1) for c in caps]):
        if sum(w) != target: continue
        cl = [idx[g] for g in types if all(gi == 0 or gi < wi for gi, wi in zip(g, w))]
        if not cl:
            print('covering impossible for w', w); print('RESULT UNSAT-trivial'); return
        S.add_clause(cl); ncov += 1
    print(f'r={r} caps={caps} T={T} types={len(types)} clauses~{ncl} cover={ncov}', flush=True)
    it = 0; t0 = time.time()
    while True:
        it += 1
        if not S.solve():
            print(f'RESULT UNSAT after {it-1} cuts ({time.time()-t0:.1f}s)'); return
        model = S.get_model()
        G = [g for g in types if model[idx[g]-1] > 0]
        Gm = minimal(G)
        rows, nodes = anchored_config(Gm, caps, anchor)
        if rows is None:
            ts, w = tau_star(Gm, caps)
            print('RESULT SAT: candidate counterexample', flush=True)
            print(' minimal types:', Gm)
            print(' tau* =', ts, 'witness', w, ' intersecting:', intersecting(Gm, caps), ' dfs nodes', nodes)
            return
        # block the (distinct) minimal types used
        used = sorted(set(rows))
        S.add_clause([-idx[g] for g in used])
        if it % 200 == 0:
            print(f' it {it}: |Gmin|={len(Gm)} cut size {len(used)} ({time.time()-t0:.1f}s)', flush=True)

if __name__ == '__main__':
    main()
