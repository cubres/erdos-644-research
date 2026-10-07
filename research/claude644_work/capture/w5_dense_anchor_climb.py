#!/usr/bin/env python3
"""w5_dense_anchor_climb.py -- EXPLORATORY search (exact integer arithmetic) for a counterexample to the
ANCHORED statement in type-closed models: an intersecting type-closed family (parts with capacities x,
finite set of admissible integer types of common size r) with tau*/r > 3/4 in which a designated type a0 is
NOT a line of any Fano-labelled bad tuple (note Lemma 7.63 conditions, necessary and sufficient).
Hill-climbs tau* over (caps, types) keeping a0 unanchorable and the family intersecting.
Usage: seed ntypes nparts r iters restarts"""
import sys, random, itertools
import numpy as np
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
# row index j = line index; row 0 = anchor on line (0,1,2).  point pencils: for each point q the 3 lines through q
PENC = [[j for j,l in enumerate(LINES) if q in l] for q in range(7)]
def anchorable(types, caps, a0=0):
    T = np.array(types); X = np.array(caps); nt = len(types)
    assigns = np.array(list(itertools.product(range(nt), repeat=6)))  # rows 1..6
    rows = np.concatenate([np.full((len(assigns),1), a0), assigns], axis=1)  # (A,7)
    L = T[rows]  # (A,7,p)
    ok = np.all(L <= X, axis=(1,2))
    ok &= np.all(L.sum(axis=1) <= 4*X, axis=1)
    for pen in PENC:
        ok &= np.all(L[:, pen, :].sum(axis=1) <= 2*X, axis=1)
    idx = np.nonzero(ok)[0]
    return (rows[idx[0]].tolist() if len(idx) else None)
def tau_star(types, caps):
    p = len(caps); nt = len(types); best = None
    choices = [[i for i in range(p) if types[a][i] > 0] for a in range(nt)]
    for m in itertools.product(*choices):
        cost = 0
        for i in range(p):
            need = [caps[i]-types[a][i] for a in range(nt) if m[a] == i]
            if need: cost += max(need)
        if best is None or cost < best: best = cost
    return best  # continuous-model tau* (sup not attained; cost = mass removed)
def intersecting(types, caps):
    p = len(caps)
    return all(any(types[a][i]+types[b][i] > caps[i] for i in range(p)) for a in range(len(types)) for b in range(a, len(types)))
def rand_type(r, caps):
    p = len(caps)
    for _ in range(1000):
        cut = sorted(random.randint(0, r) for _ in range(p-1))
        v = [b-a for a,b in zip([0]+cut, cut+[r])]
        if all(v[i] <= caps[i] for i in range(p)): return v
    return None
def mutate(types, caps, r):
    types = [list(t) for t in types]; caps = list(caps); p = len(caps)
    k = random.random()
    if k < 0.3:
        i = random.randrange(p); caps[i] = max(1, caps[i] + random.choice([-2,-1,1,2]))
    elif k < 0.9:
        a = random.randrange(len(types)); i, j = random.sample(range(p), 2); d = random.randint(1, 3)
        if types[a][i] >= d: types[a][i] -= d; types[a][j] += d
    else:
        a = random.randrange(len(types)); t = rand_type(r, caps)
        if t: types[a] = t
    if any(types[a][i] > caps[i] for a in range(len(types)) for i in range(p)): return None
    return types, caps
def score(types, caps, r):
    if not intersecting(types, caps): return None
    if anchorable(types, caps, 0) is not None: return None
    return tau_star(types, caps) / r
if __name__ == '__main__':
    seed, nt, p, r, iters, restarts = (int(x) for x in sys.argv[1:7]); random.seed(seed)
    overall = 0
    for rs in range(restarts):
        while True:
            caps = [random.randint(r//3, 2*r) for _ in range(p)]
            types = [rand_type(r, caps) for _ in range(nt)]
            if None in types: continue
            sc = score(types, caps, r)
            if sc is not None: break
        cur = sc
        for it in range(iters):
            m = mutate(types, caps, r)
            if m is None: continue
            s2 = score(m[0], m[1], r)
            if s2 is not None and s2 >= cur - (0.002 if random.random() < 0.1 else 0):
                types, caps = m; cur = s2
        overall = max(overall, cur)
        print(f"restart {rs}: best tau*/r with unanchorable a0 = {cur:.4f} caps={caps} types={types}", flush=True)
    print("overall", overall)
