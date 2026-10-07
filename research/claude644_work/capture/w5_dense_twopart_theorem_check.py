#!/usr/bin/env python3
"""w5_dense_twopart_theorem_check.py -- EXACT integer check of the ANCHORED TWO-PART THEOREM (continuous model).
Model: part 0 = E0 (capacity e), part 1 = O (capacity x); finite type set G of pairs (a,b), a+b <= r (rank),
containing the anchor (e,0) (e <= r); intersecting (no two types with a+a' <= e and b+b' <= x); continuous
tau* > 3r/4 (tau_star from w5_dense_anchor_climb, exact integers).
Proof construction being checked:
  g* = type attaining beta(e/2) (min b over types with a <= e/2; smallest such a on ties irrelevant);
  Case 1: 3 b* <= 2x  -> template {E0 on L, g* on all six}.
  Case 2: else let a'' = min{a : beta(a) < b*}, g'' = (a'', beta(a'')) -> template {E0, g* on a star, g'' on the
  opposite triangle}.  Claims A (a*+a''<=e), B (3a''<=2e), C (3b''<=2x and 2b*+b''<=2x) are checked, and the
  template is verified against note Lemma 7.63 via anchorable() restricted to the 3 types.
  Also checks independently that anchorable(full type set) succeeds.
Usage: seed trials r maxtypes"""
import sys, random
from w5_dense_anchor_climb import anchorable, tau_star, intersecting
seed, trials, r, maxt = (int(v) for v in sys.argv[1:5]); random.seed(seed)
stats = dict(tested=0, case1=0, case2=0, fail_template=0, fail_claims=0, fail_full=0)
for _ in range(trials):
    e = random.randint(r//2, r); x = random.randint(1, 3*r)
    nt = random.randint(1, maxt)
    G = set()
    for _ in range(nt):
        a = random.randint(1, e); b = random.randint(0, min(x, r - a)); G.add((a, b))
    G.add((e, 0)); G = sorted(G)
    caps = [e, x]
    if not intersecting([list(g) for g in G], caps): continue
    ts = tau_star([list(g) for g in G], caps)
    if 4*ts <= 3*r: continue
    stats['tested'] += 1
    small = [g for g in G if 2*g[0] <= e]
    if not small:
        print("no type with a<=e/2 ?!", e, x, G); stats['fail_claims'] += 1; continue
    bstar = min(g[1] for g in small); gstar = min(g for g in small if g[1] == bstar)
    if 3*bstar <= 2*x:
        stats['case1'] += 1; T = [[e,0], list(gstar)]
    else:
        stats['case2'] += 1
        cand = [g for g in G if g[1] < bstar]
        app = min(g[0] for g in cand)
        bpp = min(g[1] for g in G if g[0] <= app)
        gpp = (app, bpp)
        A = gstar[0] + app <= e; B = 3*app <= 2*e; C = (3*bpp <= 2*x) and (2*bstar + bpp <= 2*x)
        if not (A and B and C):
            stats['fail_claims'] += 1; print("CLAIM FAIL", e, x, r, G, gstar, gpp, A, B, C, flush=True)
        T = [[e,0], list(gstar), list(gpp)]
    if anchorable(T, caps, 0) is None:
        stats['fail_template'] += 1; print("TEMPLATE FAIL", e, x, r, G, T, flush=True)
    if anchorable([list(g) for g in G], caps, G.index((e,0))) is None:
        stats['fail_full'] += 1; print("FULL FAIL", e, x, r, G, flush=True)
print(stats)
