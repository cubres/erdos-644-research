#!/usr/bin/env python3
"""w4_tcglobal_single_anchor.py -- EXPLORATORY: intersecting type-closed families with a distinguished part P0 of
capacity e which is itself an edge E0 (type a0 = (e,0,..,0)), other types arbitrary; maximize tau*/k subject to:
NO Fano-downset tuple in which E0 is a row (i.e. no K4/TC configuration anchored at E0), while tuples not using
E0 may exist.  Exact integer tests (note Lemma 7.63).  Usage: seed restarts steps ntypes nparts"""
import random, sys, itertools
from fractions import Fraction
from w4_tcglobal_fano_exact import part_ok, tau_star, intersecting
seed, R, steps, nt, npart = (int(x) for x in sys.argv[1:6])
random.seed(seed)
def uses_anchor(types, caps):
    for assign in itertools.product(range(len(types)), repeat=7):
        if assign[0] != 0: continue          # row 0 (a fixed line) is E0 (by transitivity WLOG)
        if all(part_ok([types[assign[j]][i] for j in range(7)], caps[i]) for i in range(len(caps))):
            return assign
    return None
def full(types, caps):
    return [tuple([caps[0]] + [0]*(npart-1))] + [tuple(t) for t in types]
def valid(types, caps):
    if min(caps) < 1 or any(x < 0 or x > caps[i] for t in types for i, x in enumerate(t)): return False
    T = full(types, caps)
    return intersecting(T, caps) and uses_anchor(T, caps) is None
def score(types, caps):
    T = full(types, caps)
    return Fraction(tau_star(T, caps), max(sum(t) for t in T))
best = Fraction(0)
for r in range(R):
    caps = [random.randint(10, 40) for _ in range(npart)]
    types = [[random.randint(0, c) for c in caps] for _ in range(nt)]
    if not valid(types, caps): continue
    cur = score(types, caps)
    for st in range(steps):
        t2 = [list(t) for t in types]; c2 = list(caps)
        for _ in range(random.randint(1,3)):
            if random.random() < 0.3:
                i = random.randrange(npart); c2[i] += random.choice([-2,-1,1,2])
            else:
                a = random.randrange(nt); i = random.randrange(npart); t2[a][i] += random.choice([-2,-1,1,2])
        if not valid(t2, c2): continue
        sc = score(t2, c2)
        if sc < cur: continue
        types, caps, cur = t2, c2, sc
    if cur > best:
        best = cur; print("best", cur, float(cur), "caps", caps, "types", full(types, caps), flush=True)
print("done", float(best))
