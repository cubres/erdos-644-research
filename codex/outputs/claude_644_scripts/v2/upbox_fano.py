#!/usr/bin/env python3
"""Up-box unions: generators c^j (|c^j|<=1) over p parts, types = {a <= x : a >= c^j some j, sum a = 1}.
tau* = X - max(1, max over blocking maps pi: j -> part with c^j_pi(j) > 0 of sum_i min(x_i, min_{pi(j)=i} c^j_i)).
Search for instances with tau* > 3/4 admitting NO Fano parent construction (rows = up-box types)."""
import itertools, random, sys
import numpy as np
from scipy.optimize import linprog
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
def tau_star(x, gens):
    p = len(x); X = sum(x); best = 1.0
    choices = [[i for i in range(p) if c[i] > 0] for c in gens]
    for pi in itertools.product(*choices):
        caps = list(x)
        for j, i in enumerate(pi): caps[i] = min(caps[i], gens[j][i])
        best = max(best, sum(caps))
    return X - best
def fano(x, gens, assign):
    p = len(x); nA = 7*p; nv = nA + 7*p
    ai = lambda l,i: l*p+i; ci = lambda i,q: nA+i*7+q
    A=[];b=[]
    for i in range(p):
        r=np.zeros(nv)
        for q in range(7): r[ci(i,q)]=1
        A.append(r); b.append(x[i])
    for l,line in enumerate(LINES):
        for i in range(p):
            r=np.zeros(nv); r[ai(l,i)]=1
            for q in range(7):
                if q not in line: r[ci(i,q)]=-1
            A.append(r); b.append(0)
    Aeq=[];beq=[]
    for l in range(7):
        r=np.zeros(nv)
        for i in range(p): r[ai(l,i)]=1
        Aeq.append(r); beq.append(1)
    bounds=[(gens[assign[l]][i], x[i]) for l in range(7) for i in range(p)]+[(0,None)]*(7*p)
    if any(hi is not None and lo > hi + 1e-12 for lo, hi in bounds): return False
    return linprog(np.zeros(nv),A_ub=np.array(A),b_ub=np.array(b),A_eq=np.array(Aeq),b_eq=np.array(beq),bounds=bounds,method='highs').status==0
def any_fano(x, gens):
    m = len(gens)
    seen=set()
    for assign in itertools.product(range(m), repeat=7):
        if fano(x, gens, assign): return assign
    return None
if __name__ == '__main__':
    p, m, N, seed = map(int, sys.argv[1:5]); rng = random.Random(seed)
    found = 0; tested = 0
    while tested < N:
        x = [rng.uniform(0.3, 1.2) for _ in range(p)]
        gens = []
        for j in range(m):
            supp = rng.sample(range(p), rng.randint(1, min(2, p)))
            c = [0.0]*p
            for i in supp: c[i] = rng.uniform(0.1, 1.0) * x[i]
            s = sum(c)
            if s > 1: c = [v/s for v in c]
            gens.append(c)
        # generator must be realisable: exists a >= c, a <= x, sum a = 1
        if any(sum(c) > 1 or sum(x) < 1 for c in gens): continue
        t = tau_star(x, gens)
        if t <= 0.75: continue
        tested += 1
        a = any_fano(x, gens)
        if a is None:
            found += 1
            print("FANO-FREE tau*=%.4f x=%s gens=%s" % (t, [round(v,3) for v in x], [[round(v,3) for v in c] for c in gens]), flush=True)
    print(f"p={p} m={m}: tested {tested} instances with tau*>3/4, Fano-free {found}")
