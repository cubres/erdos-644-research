#!/usr/bin/env python3
"""Search for (p,2) set systems S (p=6 default) on a small ground set where some positive weighting
w has max edge weight <= 1 but every transversal weight > 1  (LP value z* > 1).
z*(S) = max z s.t. w(J) >= z for all minimal transversals J, w(E) <= 1 for all edges E, w >= 0.
Local search over families (add/remove/replace edges) maximizing z* subject to (p,2)."""
import itertools, random, sys
import numpy as np
from scipy.optimize import linprog

def two_pierceable(edges):
    # edges: list of bitmasks; exists pair (x,y) (x==y allowed) hitting all
    n = max(e.bit_length() for e in edges)
    for x in range(n):
        rest = [e for e in edges if not (e >> x) & 1]
        if not rest: return True
        common = rest[0]
        for e in rest[1:]:
            common &= e
            if not common: break
        if common: return True
    return False

def is_p2(fam, p):
    fam = list(fam)
    m = len(fam)
    for r in range(3, min(p, m) + 1):
        for sub in itertools.combinations(fam, r):
            if not two_pierceable(sub): return False
    return True

def ok_with(fam, new, p):
    # check only subfamilies containing new
    fam = [e for e in fam if e != new]
    for r in range(2, min(p, len(fam) + 1)):
        for sub in itertools.combinations(fam, r):
            if not two_pierceable(list(sub) + [new]): return False
    return True

def min_transversals(fam, n):
    trans = []
    for mask in range(1, 1 << n):
        if all(mask & e for e in fam):
            # minimal?
            if all(not all((mask & ~(1 << b)) & e for e in fam) for b in range(n) if (mask >> b) & 1):
                trans.append(mask)
    return trans

def zstar(fam, n):
    fam = list(fam)
    if not fam: return 0.0, None
    T = min_transversals(fam, n)
    # vars: w_0..w_{n-1}, z ; maximize z
    c = np.zeros(n + 1); c[-1] = -1
    A = []; b = []
    for J in T:
        row = np.zeros(n + 1); row[-1] = 1
        for v in range(n):
            if (J >> v) & 1: row[v] = -1
        A.append(row); b.append(0)
    for E in fam:
        row = np.zeros(n + 1)
        for v in range(n):
            if (E >> v) & 1: row[v] = 1
        A.append(row); b.append(1)
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=[(0, None)] * n + [(None, None)], method='highs')
    return -res.fun, res.x[:n]

def antichain(fam):
    fam = set(fam)
    return {e for e in fam if not any(f != e and (f & e) == f for f in fam)}

def search(n, p, iters, seed):
    rng = random.Random(seed)
    allsets = list(range(1, 1 << n))
    fam = set()
    best = (0, None)
    cur = 0.0
    for it in range(iters):
        f2 = set(fam)
        mv = rng.random()
        if mv < 0.6 or not f2:
            e = rng.choice(allsets)
            if e in f2: continue
            if not ok_with(list(f2), e, p): continue
            f2.add(e)
        elif mv < 0.8:
            f2.remove(rng.choice(sorted(f2)))
        else:
            old = rng.choice(sorted(f2)); f2.remove(old)
            e = old ^ (1 << rng.randrange(n))
            if e == 0 or e in f2 or not ok_with(list(f2), e, p): continue
            f2.add(e)
        f2 = antichain(f2)
        z, w = zstar(f2, n)
        if z >= cur - 0.02 or rng.random() < 0.05:
            fam, cur = f2, z
            if z > best[0] + 1e-9:
                best = (z, sorted(f2), w)
    return best

if __name__ == '__main__':
    n = int(sys.argv[1]); p = int(sys.argv[2]); iters = int(sys.argv[3]); seeds = int(sys.argv[4])
    overall = (0,)
    for s in range(seeds):
        b = search(n, p, iters, s)
        if b[0] > overall[0]: overall = b
        print(f"seed {s}: z*={b[0]:.4f}", flush=True)
    z, fam, w = overall
    print("BEST z*", z)
    print("family", [[v for v in range(n) if (e >> v) & 1] for e in fam])
    print("weights", np.round(w, 4))
