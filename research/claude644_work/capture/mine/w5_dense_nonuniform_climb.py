#!/usr/bin/env python3
"""w5_dense_nonuniform_climb.py -- EXPLORATORY (exact integers).  Non-uniform type-closed models with an anchor
E0 that is a UNION OF PARTS (E0 = parts 0..p0-1 in full) and is a SMALLEST edge (all types have size >= e),
rank <= k.  Other parts form O.  Search (hill-climb) for: intersecting family, tau*/k large, and E0 NOT a line of
any Fano-labelled bad tuple (note Lemma 7.63 conditions, exact).  A hit with tau*/k > 3/4 would refute
Conjecture A (anchored at a smallest edge) in the type-closed model.
Usage: seed ntypes p0 p1 k iters restarts"""
import sys, random, itertools
import numpy as np
from w5_dense_anchor_climb import anchorable, tau_star, intersecting
def rand_type(caps, p0, e, k):
    p = len(caps)
    for _ in range(2000):
        size = random.randint(e, k)
        v = [random.randint(0, c) for c in caps]
        tot = sum(v)
        if tot == 0: continue
        v = [min(caps[i], round(v[i]*size/tot)) for i in range(p)]
        if e <= sum(v) <= k and sum(v[:p0]) >= 1 and v != list(caps[:p0])+[0]*(p-p0): return v
    return None
def ok(types, caps, p0, e, k):
    p = len(caps)
    for t in types:
        if any(t[i] > caps[i] or t[i] < 0 for i in range(p)): return False
        if not (e <= sum(t) <= k): return False
    return True
def score(types, caps, p0, e, k):
    a0 = list(caps[:p0]) + [0]*(len(caps)-p0)
    allt = [a0] + [list(t) for t in types]
    if not intersecting(allt, caps): return None
    if anchorable(allt, caps, 0) is not None: return None
    return tau_star(allt, caps) / k
if __name__ == '__main__':
    seed, nt, p0, p1, k, iters, restarts = (int(x) for x in sys.argv[1:8]); random.seed(seed)
    overall = (0, None)
    for rs in range(restarts):
        tries = 0
        while True:
            tries += 1
            e = random.randint(k//2, k)
            ecaps = [e//p0 + (1 if i < e % p0 else 0) for i in range(p0)]
            caps = ecaps + [random.randint(k//6, k) for _ in range(p1)]
            types = [rand_type(caps, p0, e, k) for _ in range(nt)]
            if None in types: continue
            sc = score(types, caps, p0, e, k)
            if sc is not None: break
        cur = sc
        for it in range(iters):
            T = [list(t) for t in types]; C = list(caps); E = e
            r = random.random(); p = len(C)
            if r < 0.15:
                i = random.randrange(p0, p); C[i] = max(1, C[i] + random.choice([-2,-1,1,2]))
            elif r < 0.25 and p0 >= 1:
                i = random.randrange(p0); d = random.choice([-1,1]); C[i] = max(1, C[i]+d); E = sum(C[:p0])
            elif r < 0.9:
                a = random.randrange(nt); i = random.randrange(p); d = random.choice([-2,-1,1,2]); T[a][i] += d
            else:
                a = random.randrange(nt); tt = rand_type(C, p0, E, k)
                if tt: T[a] = tt
            if not ok(T, C, p0, E, k): continue
            s2 = score(T, C, p0, E, k)
            if s2 is not None and s2 >= cur - (0.003 if random.random() < 0.1 else 0):
                types, caps, e, cur = T, C, E, s2
        if cur > overall[0]: overall = (cur, (caps, e, types))
        print(f"restart {rs}: tau*/k={cur:.4f} e={e} caps={caps} types={types}", flush=True)
    print("overall", overall)
