#!/usr/bin/env python3
"""w8_dense_maxT.py -- for a list of capacity vectors, find the largest T such that the anchored multi-part
SAT/CEGAR (w8_dense_msat logic) is SAT, i.e. the max continuous tau* of an intersecting, up-closed integer type
set containing the anchor (e,0..0) with NO anchored Fano configuration.  Prints T_max/r and the grid-adjusted
excess  T_max - (3r/4 - p + 1)  (the complete type set loses p-1 to the integer grid).
Usage: python3 w8_dense_maxT.py r e "x1,x2;x1,x2,x3;..." """
import sys, time
from itertools import product
from pysat.solvers import Cadical153
from w8_dense_lib import all_types, minimal, anchored_config, tau_star, intersecting

def build(r, caps):
    e = caps[0]; p = len(caps)
    types = all_types(caps, r, amin=1)
    idx = {g: i+1 for i, g in enumerate(types)}
    base = []
    anchor = (e,) + (0,)*(p-1)
    base.append([idx[anchor]])
    for g in types:
        for i in range(p):
            h = list(g); h[i] += 1; h = tuple(h)
            if h in idx: base.append([-idx[g], idx[h]])
    for g in types:
        comp = tuple(c - x for c, x in zip(caps, g))
        if sum(comp) <= r:
            cands = [comp] if comp in idx else []
        else:
            cands = [h for h in product(*[range(c+1) for c in comp]) if sum(h) == r and h in idx]
        for h in cands: base.append([-idx[g], -idx[h]])
    return types, idx, anchor, base

def solve(r, caps, T, types, idx, anchor, base, cuts):
    N = sum(caps)
    S = Cadical153(bootstrap_with=base)
    for c in cuts: S.add_clause(c)
    target = N - T + 1
    for w in product(*[range(c+1) for c in caps]):
        if sum(w) != target: continue
        cl = [idx[g] for g in types if all(gi == 0 or gi < wi for gi, wi in zip(g, w))]
        if not cl: return None
        S.add_clause(cl)
    while True:
        if not S.solve(): return None
        model = S.get_model()
        Gm = minimal([g for g in types if model[idx[g]-1] > 0])
        rows, _ = anchored_config(Gm, caps, anchor)
        if rows is None: return Gm
        cl = [-idx[g] for g in sorted(set(rows))]
        cuts.append(cl); S.add_clause(cl)

def main():
    r = int(sys.argv[1]); e = int(sys.argv[2])
    for spec in sys.argv[3].split(';'):
        xs = tuple(int(v) for v in spec.split(','))
        caps = (e,) + xs; p = len(caps)
        t0 = time.time()
        types, idx, anchor, base = build(r, caps)
        cuts = []
        best = None; bestG = None
        T = 1
        while True:
            G = solve(r, caps, T, types, idx, anchor, base, cuts)
            if G is None: break
            ts, _ = tau_star(G, caps) if len(types) < 3000 else (None, None)
            best = T if ts is None else ts; bestG = G
            T = best + 1
        adj = None if best is None else best - (3*r/4 - p + 1)
        print(f'r={r} caps={caps} Tmax={best} ratio={None if best is None else round(best/r,3)} '
              f'excess_vs_grid_complete={adj} cuts={len(cuts)} ({time.time()-t0:.1f}s)', flush=True)
        if bestG is not None and adj is not None and adj > 0:
            print('   EXCESS example minimal types:', bestG, ' intersecting', intersecting(bestG, caps), flush=True)

if __name__ == '__main__':
    main()
