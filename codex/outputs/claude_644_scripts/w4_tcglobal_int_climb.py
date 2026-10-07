#!/usr/bin/env python3
"""w4_tcglobal_int_climb.py -- EXPLORATORY hill climb (exact integer tests): maximize tau*/k over INTERSECTING
type-closed families (nt types, np parts) with NO Fano-labelled bad tuple.  Usage: seed restarts nt np steps"""
import random, sys
from fractions import Fraction
from w4_tcglobal_fano_exact import fano_tuple, tau_star, intersecting
seed, R, nt, npart, steps = (int(x) for x in sys.argv[1:6])
random.seed(seed)
def valid(types, caps):
    if min(caps) < 0 or any(x < 0 or x > caps[i] for t in types for i, x in enumerate(t)): return False
    return intersecting(types, caps) and fano_tuple(types, caps) is None
def score(types, caps):
    k = max(sum(t) for t in types)
    return Fraction(tau_star(types, caps), k) if k else Fraction(-1)
best = Fraction(0)
for r in range(R):
    S = random.randint(10, 40)
    caps = [random.randint(S//2, 2*S) for _ in range(npart)]
    types = [[random.randint(0, c) for c in caps] for _ in range(nt)]
    ok = False
    for _ in range(200):
        if valid(types, caps): ok = True; break
        i = random.randrange(npart)
        if random.random() < 0.5: caps[i] = max(max(t[i] for t in types), caps[i]-1)
        else:
            a = random.randrange(nt); types[a][i] = min(caps[i], types[a][i]+1)
    if not ok: continue
    cur = score(types, caps)
    for st in range(steps):
        t2 = [list(t) for t in types]; c2 = list(caps)
        for _ in range(random.randint(1,3)):
            if random.random() < 0.35:
                i = random.randrange(npart); c2[i] += random.choice([-2,-1,1,2])
            else:
                a = random.randrange(nt); i = random.randrange(npart); t2[a][i] += random.choice([-2,-1,1,2])
        if not valid(t2, c2): continue
        sc = score(t2, c2)
        if sc < cur: continue
        types, caps, cur = t2, c2, sc
    if cur > best:
        best = cur
        print("restart", r, "best", cur, float(cur), "caps", caps, "types", types, flush=True)
print("done", best, float(best))
