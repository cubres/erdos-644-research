#!/usr/bin/env python3
"""Three-box type-closed families over 3 parts: capacities x, thresholds theta (4x_i/7 < theta_i <= x_i),
types = {a <= x : sum a = 1, a_i >= theta_i for some i}; tau* = sum(x - theta) when sum theta >= 1.
Test: is there a Fano PARENT construction (class masses c[i][p], windows >= row traces) with each
line's row of box type b(l)?  Exact LP per box assignment (orbit reps under PSL(2,7))."""
import itertools, random, sys
import numpy as np
from scipy.optimize import linprog

LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
PTS = range(7)

def fano_autos():
    L = [frozenset(l) for l in LINES]; Ls = set(L)
    autos = []
    for perm in itertools.permutations(range(7)):
        if all(frozenset(perm[p] for p in l) in Ls for l in L):
            autos.append(perm)
    return autos, L

AUT, LSET = fano_autos()
LIDX = {l: i for i, l in enumerate(LSET)}
def line_perm(pp):
    return [LIDX[frozenset(pp[p] for p in l)] for l in LSET]
LPERMS = [line_perm(pp) for pp in AUT]

def assignment_reps():
    seen = set(); reps = []
    for b in itertools.product(range(3), repeat=7):
        if b in seen: continue
        reps.append(b)
        for lp in LPERMS:
            nb = [None]*7
            for i in range(7): nb[lp[i]] = b[i]
            seen.add(tuple(nb))
    return reps
REPS = assignment_reps()

def fano_lp(x, th, b):
    # vars: a[l][i] (21), c[i][p] (21)
    nA = 21; nv = 42
    A_ub, b_ub = [], []
    def ai(l, i): return l*3 + i
    def ci(i, p): return nA + i*7 + p
    for i in range(3):
        r = np.zeros(nv); 
        for p in PTS: r[ci(i,p)] = 1
        A_ub.append(r); b_ub.append(x[i])
    for l, line in enumerate(LSET):
        for i in range(3):
            r = np.zeros(nv); r[ai(l,i)] = 1
            for p in PTS:
                if p not in line: r[ci(i,p)] = -1
            A_ub.append(r); b_ub.append(0)
        r = np.zeros(nv)
        for i in range(3): r[ai(l,i)] = -1
        A_ub.append(r); b_ub.append(-1)
    bounds = []
    for l in range(7):
        for i in range(3):
            lo = th[i] if b[l] == i else 0
            bounds.append((lo, x[i]))
    bounds += [(0, None)]*21
    res = linprog(np.zeros(nv), A_ub=np.array(A_ub), b_ub=np.array(b_ub), bounds=bounds, method='highs')
    return res.status == 0

def sample(rng):
    while True:
        x = [rng.uniform(0.3, 1.2) for _ in range(3)]
        th = [rng.uniform(4*xi/7, xi) for xi in x]
        if sum(th) < 1 or any(t > 1 for t in th): continue
        d = sum(xi - ti for xi, ti in zip(x, th))
        if d > 0.75: return x, th, d

if __name__ == '__main__':
    N = int(sys.argv[1]); seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    rng = random.Random(seed)
    print(f"{len(AUT)} automorphisms, {len(REPS)} assignment reps", flush=True)
    fails = []
    for s in range(N):
        x, th, d = sample(rng)
        ok = any(fano_lp(x, th, b) for b in REPS)
        if not ok:
            fails.append((x, th, d)); print("NO FANO:", [round(v,4) for v in x], [round(v,4) for v in th], "tau*", round(d,4), flush=True)
    print(f"samples {N}, no-Fano {len(fails)}")
