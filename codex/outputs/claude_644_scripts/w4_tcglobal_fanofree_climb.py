#!/usr/bin/env python3
"""w4_tcglobal_fanofree_climb.py -- EXPLORATORY hill climb: maximize tau/k over type-closed families
(ntypes types, nparts parts, integer masses) subject to: NO Fano-labelled (downset) bad tuple.
Floating LP; any hit must be re-certified exactly.  Usage: seed iters ntypes nparts"""
import random, sys
from w4_tcglobal_fanofree_search import fano_exists, tau_cont
seed, iters, nt, npart = (int(x) for x in sys.argv[1:5])
random.seed(seed)
def score(types, caps):
    k = max(sum(a) for a in types)
    if k == 0: return -1
    return tau_cont(types, caps)/k
def feasible(types, caps):
    return all(0 <= types[a][i] <= caps[i] for a in range(nt) for i in range(npart)) and fano_exists(types, caps) is None
bestall = 0
for restart in range(iters):
    caps = [random.randint(5,30) for _ in range(npart)]
    types = [[random.randint(0,c) for c in caps] for _ in range(nt)]
    # start from something fano-free: shrink caps until fano-free
    tries = 0
    while fano_exists(types, caps) is not None and tries < 50:
        i = random.randrange(npart)
        caps[i] = max(max(t[i] for t in types), caps[i]-1); tries += 1
        if tries % 10 == 0:
            a = random.randrange(nt); i = random.randrange(npart); types[a][i] = min(caps[i], types[a][i]+1)
    if fano_exists(types, caps) is not None: continue
    cur = score(types, caps)
    for step in range(300):
        nt2 = [list(t) for t in types]; c2 = list(caps)
        r = random.random()
        if r < 0.4:
            i = random.randrange(npart); c2[i] += random.choice([-1,1])
        else:
            a = random.randrange(nt); i = random.randrange(npart); nt2[a][i] += random.choice([-1,1])
        if min(c2) < 0 or any(x < 0 for t in nt2 for x in t): continue
        if not all(nt2[a][i] <= c2[i] for a in range(nt) for i in range(npart)): continue
        sc = score(nt2, c2)
        if sc + 1e-12 < cur: continue
        if fano_exists(nt2, c2) is not None: continue
        types, caps, cur = nt2, c2, sc
    if cur > bestall:
        bestall = cur
        print("restart", restart, "best", round(cur,4), "caps", caps, "types", types, flush=True)
print("done", bestall)
