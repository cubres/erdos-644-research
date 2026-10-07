#!/usr/bin/env python3
"""w4_tcglobal_fanofree_search.py -- EXPLORATORY random search (floating LP) for type-closed families with
high tau/k and NO Fano-labelled (downset) bad tuple.  Such a family would obstruct every proof that only
produces Fano-labelled tuples (TC, K4 form, pencil lemmas...).  Usage: python3 w4_tcglobal_fanofree_search.py seed iters ntypes nparts"""
import itertools, random, sys
import numpy as np
from scipy.optimize import linprog
lines = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
safe = set()
for p in range(7):
    miss = [i for i,l in enumerate(lines) if p not in l]
    for r in range(1,5):
        for c in itertools.combinations(miss, r): safe.add(frozenset(c))
safe = sorted(safe, key=lambda s:(len(s),sorted(s)))
A_eq = np.array([[1.0 if l in s else 0.0 for s in safe] for l in range(7)])
A_ub = np.ones((1,len(safe)))
# automorphisms of Fano acting on lines
autos = []
for perm in itertools.permutations(range(7)):
    img = [tuple(sorted(perm[x] for x in l)) for l in lines]
    if all(i in lines for i in img):
        autos.append([lines.index(i) for i in img])
assert len(autos) == 168
def canon(assign):
    best = None
    for a in autos:
        b = [None]*7
        for l in range(7): b[a[l]] = assign[l]
        b = tuple(b)
        if best is None or b < best: best = b
    return best
orbit_cache = {}
def orbit_reps(nt):
    if nt not in orbit_cache:
        reps = set(canon(a) for a in itertools.product(range(nt), repeat=7))
        orbit_cache[nt] = sorted(reps)
    return orbit_cache[nt]
def part_feasible(loads, cap):
    r = linprog(np.zeros(len(safe)), A_ub=A_ub, b_ub=[cap], A_eq=A_eq, b_eq=loads, bounds=(0,None), method='highs')
    return r.status == 0
def fano_exists(types, caps):
    for assign in orbit_reps(len(types)):
        if all(part_feasible([types[assign[l]][P] for l in range(7)], caps[P]) for P in range(len(caps))):
            return assign
    return None
def tau_cont(types, caps):
    n = len(caps); best = None
    for m in itertools.product(range(n), repeat=len(types)):
        cost = 0.0
        for i in range(n):
            need = [caps[i]-types[a][i] for a in range(len(types)) if m[a]==i]
            if need: cost += max(0.0, max(need))
        if best is None or cost < best: best = cost
    return best
if __name__ == '__main__':
    seed, iters, nt, npart = (int(x) for x in sys.argv[1:5])
    random.seed(seed)
    best = 0
    for it in range(iters):
        caps = [random.randint(1,40) for _ in range(npart)]
        types = [tuple(random.randint(0,c) for c in caps) for _ in range(nt)]
        k = max(sum(a) for a in types)
        if k == 0: continue
        tau = tau_cont(types, caps)
        if tau/k <= max(best, 0.70): continue
        if fano_exists(types, caps) is None:
            best = tau/k
            print("NEW fano-free", round(best,4), "caps", caps, "types", types, "tau", tau, "k", k, flush=True)
    print("done best", best)
