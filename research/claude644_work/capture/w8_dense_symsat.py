#!/usr/bin/env python3
"""w8_dense_symsat.py -- anchored multi-part SAT/CEGAR restricted to type sets INVARIANT under a group of
permutations of the (equal-capacity) outside parts.  Finds the max continuous tau* of an intersecting,
up-closed, symmetric integer type set containing the anchor with NO anchored Fano configuration.
Usage: python3 w8_dense_symsat.py r e x m group   (group: 'cyc' or 'sym'; m outside parts of cap x each)
Soundness: every type set found is re-verified exactly (tau*, intersecting, no config by exhaustive DFS)."""
import sys, time
from itertools import product, permutations
from pysat.solvers import Cadical153
from w8_dense_lib import all_types, minimal, anchored_config, tau_star, intersecting

def main():
    r, e, x, m = map(int, sys.argv[1:5]); grp = sys.argv[5]
    caps = (e,) + (x,)*m; N = sum(caps); p = m + 1
    if grp == 'cyc': perms = [tuple((i + s) % m for i in range(m)) for s in range(m)]
    else: perms = list(permutations(range(m)))
    def act(g, pi): return (g[0],) + tuple(g[1 + pi[i]] for i in range(m))
    types = all_types(caps, r, amin=1)
    orb = {}; reps = []
    for g in types:
        if g in orb: continue
        o = {act(g, pi) for pi in perms}
        v = len(reps) + 1; reps.append(sorted(o))
        for h in o: orb[h] = v
    base = []
    anchor = (e,) + (0,)*m
    base.append([orb[anchor]])
    for g in types:
        for i in range(p):
            h = list(g); h[i] += 1; h = tuple(h)
            if h in orb and orb[h] != orb[g]: base.append([-orb[g], orb[h]])
    seen = set()
    for g in types:
        comp = tuple(c - v for c, v in zip(caps, g))
        if sum(comp) <= r: cands = [comp] if comp in orb else []
        else: cands = [h for h in product(*[range(c+1) for c in comp]) if sum(h) == r and h in orb]
        for h in cands:
            key = tuple(sorted((orb[g], orb[h])))
            if key in seen: continue
            seen.add(key); base.append([-orb[g], -orb[h]] if orb[g] != orb[h] else [-orb[g]])
    print(f'r={r} caps={caps} group={grp} orbits={len(reps)} base={len(base)}', flush=True)
    cuts = []; best = None; T = int(3*r/4) - p
    t0 = time.time()
    while True:
        S = Cadical153(bootstrap_with=base + cuts)
        target = N - T + 1; ok = True
        for w in product(*[range(c+1) for c in caps]):
            if sum(w) != target: continue
            if w != max(act(w, pi) for pi in perms): continue   # orbit representative
            cl = sorted({orb[g] for g in types if all(gi == 0 or gi < wi for gi, wi in zip(g, w))})
            if not cl: ok = False; break
            S.add_clause(cl)
        found = None
        while ok:
            if not S.solve(): break
            mdl = S.get_model()
            G = [g for g in types if mdl[orb[g]-1] > 0]
            Gm = minimal(G)
            rows, _ = anchored_config(Gm, caps, anchor)
            if rows is None: found = Gm; break
            cl = sorted({-orb[g] for g in rows}); cuts.append(cl); S.add_clause(cl)
        if found is None:
            print(f'  T={T}: UNSAT (cuts {len(cuts)}, {time.time()-t0:.0f}s)', flush=True); break
        ts, wit = tau_star(found, caps)
        print(f'  T={T}: SAT tau*={ts} (3r/4={3*r/4}) intersecting={intersecting(found, caps)} '
              f'|Gmin|={len(found)} ({time.time()-t0:.0f}s)', flush=True)
        if ts > 3*r/4: print('  !!! tau* > 3r/4 with no anchored config:', found, flush=True)
        best = (ts, found); T = ts + 1
    if best: print('BEST', best[0], best[0]/r, best[1])

if __name__ == '__main__':
    main()
