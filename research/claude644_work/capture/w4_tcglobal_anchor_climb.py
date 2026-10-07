#!/usr/bin/env python3
"""w4_tcglobal_anchor_climb.py -- EXPLORATORY: random-walk/hill-climb over INTERSECTING type-closed families
(nt types, np parts, integer masses, rank k = max type size) pushing tau*/k up; every visited state with
tau*/k > 3/4 is tested (exactly, note Lemma 7.63) for (i) existence of a Fano-downset tuple, (ii) whether EVERY type
occurs as a row of one (anchor participation), (iii) whether a SMALLEST type occurs.  Usage: seed restarts steps nt np"""
import random, sys, itertools
from fractions import Fraction
from w4_tcglobal_fano_exact import part_ok, tau_star, intersecting
seed, R, steps, nt, npart = (int(x) for x in sys.argv[1:6]); random.seed(seed)
def rows_used(types, caps):
    used = set()
    for assign in itertools.product(range(len(types)), repeat=7):
        if set(assign) <= used: continue
        if all(part_ok([types[assign[j]][i] for j in range(7)], caps[i]) for i in range(npart)):
            used |= set(assign)
            if len(used) == len(types): break
    return used
def ok(types, caps):
    return min(caps) >= 0 and all(0 <= x <= caps[i] for t in types for i,x in enumerate(t)) and min(sum(t) for t in types) > 0 and intersecting(types, caps)
def score(types, caps): return Fraction(tau_star(types, caps), max(sum(t) for t in types))
tested = 0; bad = 0; best = 0
for rr in range(R):
    caps = [random.randint(8, 30) for _ in range(npart)]
    types = [[random.randint(0, c) for c in caps] for _ in range(nt)]
    if not ok(types, caps): continue
    cur = score(types, caps)
    for st in range(steps):
        t2 = [list(t) for t in types]; c2 = list(caps)
        for _ in range(random.randint(1,3)):
            if random.random() < 0.3:
                i = random.randrange(npart); c2[i] += random.choice([-1,1])
            else:
                a = random.randrange(nt); i = random.randrange(npart); t2[a][i] += random.choice([-1,1])
        if not ok(t2, c2): continue
        sc = score(t2, c2)
        if sc < cur and random.random() > 0.05: continue
        types, caps, cur = t2, c2, sc
        best = max(best, cur)
        if 4*cur > 3:
            tested += 1
            u = rows_used(types, caps)
            sizes = [sum(t) for t in types]; smallest = [i for i in range(nt) if sizes[i] == min(sizes)]
            if not u or len(u) < nt:
                bad += 1
                print("tau*/k", cur, float(cur), "caps", caps, "types", types, "rows used", sorted(u),
                      "smallest used:", any(i in u for i in smallest), flush=True)
print("best tau*/k", float(best), "states tested (tau*/k>3/4):", tested, " with missing Fano / anchor-free type:", bad)
