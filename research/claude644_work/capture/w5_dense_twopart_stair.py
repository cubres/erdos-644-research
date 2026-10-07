#!/usr/bin/env python3
"""w5_dense_twopart_stair.py -- EXPLORATORY, exact integers.  Two-part anchored model: part 0 = E0 (cap e), part 1 = O
(cap x), rank k.  Generators = staircase corners (a_i, b_i) (a_i = trace size, b_i = outside size), a_i+b_i <= k,
built randomly so that the continuous tau* >= T (T > 3k/4) and the family is intersecting.  Tests whether E0
(type (e,0)) is a line of some Fano-labelled tuple (note Lemma 7.63, all 6-slot assignments).  Reports any
non-anchorable instance (would be a 2-part counterexample to the anchored statement).
Usage: seed trials k"""
import sys, random
from w5_dense_anchor_climb import anchorable, tau_star, intersecting
seed, trials, k = (int(v) for v in sys.argv[1:4]); random.seed(seed)
found = 0; tested = 0; beyond = 0
for _ in range(trials):
    e = random.randint(3*k//4 + 1, k)
    T = random.randint(3*k//4 + 1, e)          # target tau*
    x = random.randint(max(1, T - e//2), 2*k)   # need x big enough for tau* >= T
    c = e + x - T                               # free boxes must have a + b < c  (continuous: <= c)
    # build corners left to right
    gens = []; a = random.randint(0, max(0, e - T)); ok = True
    while True:
        # beta must satisfy a' + beta(a'') ... choose b with a+b<=k, and next corner a2 <= c - b
        bmax = min(k - a, x)
        # intersecting with previous corners and with itself
        bmin = 0
        for (aj, bj) in gens + [(a, None)]:
            if aj is None: continue
            if a + aj <= e:
                other = bj if bj is not None else None
                if other is None: bmin = max(bmin, x//2 + 1)
                else: bmin = max(bmin, x - other + 1)
        if bmax < bmin: ok = False; break
        b = random.randint(bmin, bmax) if random.random() < 0.5 else bmax
        gens.append((a, b))
        if a >= e: break
        a2max = c - b          # next corner must come no later than c - b (so that a + b <= c on the flat part)
        if a2max <= a: ok = False; break
        a2 = random.randint(a+1, min(a2max, e))
        if a2 >= e: gens.append((e, 0)); break
        a = a2
    if not ok: continue
    types = [list(g) for g in gens]
    if [e, 0] not in types: types.append([e, 0])
    caps = [e, x]
    if not intersecting(types, caps): continue
    ts = tau_star(types, caps)
    if 4*ts <= 3*k: continue
    tested += 1
    if 3*(ts) >= 0 and x > (9*k - 6*e)//4: beyond += 1
    a0 = types.index([e, 0])
    if anchorable(types, caps, a0) is None:
        found += 1
        print("NON-ANCHORABLE:", "e", e, "x", x, "k", k, "tau*", ts, "gens", types, flush=True)
print(f"tested {tested} (beyond static range: {beyond}); non-anchorable: {found}")
