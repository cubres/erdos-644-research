#!/usr/bin/env python3
"""w4_tcglobal_anchor_search.py -- EXPLORATORY: intersecting two-type type-closed families with tau*/k > 3/4 in which
the SMALLER type never occurs in a Fano-downset tuple (so anchoring TC at a smallest edge must fail).
Exact integer tests (note Lemma 7.63 closed form). Usage: seed restarts steps nparts"""
import random, sys, itertools
from fractions import Fraction
from w4_tcglobal_fano_exact import part_ok, tau_star, intersecting
seed, R, steps, npart = (int(x) for x in sys.argv[1:5])
random.seed(seed)
def assignments_using(types, caps, must):
    for assign in itertools.product(range(len(types)), repeat=7):
        if must not in assign: continue
        if all(part_ok([types[assign[j]][i] for j in range(7)], caps[i]) for i in range(len(caps))):
            return assign
    return None
def valid(types, caps):
    if any(x < 0 or x > caps[i] for t in types for i, x in enumerate(t)): return False
    if sum(types[0]) > sum(types[1]): return False
    return intersecting(types, caps) and assignments_using(types, caps, 0) is None
def score(types, caps):
    return Fraction(tau_star(types, caps), max(sum(t) for t in types))
best = Fraction(0)
for r in range(R):
    caps = [random.randint(10, 60) for _ in range(npart)]
    types = [[random.randint(0, c) for c in caps] for _ in range(2)]
    if not valid(types, caps): continue
    cur = score(types, caps)
    for st in range(steps):
        t2 = [list(t) for t in types]; c2 = list(caps)
        for _ in range(random.randint(1,3)):
            if random.random() < 0.35:
                i = random.randrange(npart); c2[i] += random.choice([-2,-1,1,2])
            else:
                a = random.randrange(2); i = random.randrange(npart); t2[a][i] += random.choice([-2,-1,1,2])
        if not valid(t2, c2): continue
        sc = score(t2, c2)
        if sc < cur: continue
        types, caps, cur = t2, c2, sc
    if cur > best:
        best = cur; print("best", cur, float(cur), "caps", caps, "types", types, flush=True)
print("done", float(best))
