#!/usr/bin/env python3
"""w7_ref_denseTwoPart_nonint3.py -- is INTERSECTING needed?  Random integer 3-type sets {anchor, g1, g2}
(plus optional 4th type), NOT required intersecting, rank R; tau* exact (sup_free); if 4tau*>3R, test ALL
assignments of G-types to the 6 non-anchor lines against Lemma 7.63 (explicit Fano pencils)."""
import sys, random, itertools
from w7_ref_denseTwoPart_lib import *
seed, R, trials = map(int, sys.argv[1:4]); random.seed(seed)
found = 0; qual = 0; qual_int = 0
for _ in range(trials):
    e = random.randint(3*R//4+1, R); x = random.randint(R//2, 2*R)
    G = [(e, 0)]
    for j in range(random.choice([2, 3])):
        a = random.randint(1, e); b = random.randint(0, min(x, R-a)); G.append((a, b))
    G = list(dict.fromkeys(G))
    ts = tau_star(G, e, x)
    if 4*ts <= 3*R: continue
    qual += 1; isint = intersecting(G, e, x); qual_int += isint
    ok = False
    for ass in itertools.product(G, repeat=6):
        rows = [(e, 0)] + list(ass)
        if fano_ok(rows, (e, x)): ok = True; break
    if not ok:
        found += 1
        if found <= 10: print('NO ANCHORED TUPLE: R', R, 'e', e, 'x', x, 'G', G, 'tau*', ts, 'intersecting', isint, flush=True)
        if isint: print('!!! INTERSECTING COUNTEREXAMPLE', flush=True)
print('R', R, 'qualifying', qual, 'of which intersecting', qual_int, 'no-anchored-tuple', found)
