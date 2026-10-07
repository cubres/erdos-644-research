#!/usr/bin/env python3
"""p one-sided boxes over p parts: types = {a<=x, sum a = 1, a_i >= theta_i for some i}.
tau* = sum(x-theta) if sum theta >= 1.  Test the universal Fano template with boxes (A,B,C) chosen among
the p parts (all ordered triples), rows' non-box mass in ANY part; exact LP with explicit class masses."""
import itertools, random, sys
import numpy as np
from scipy.optimize import linprog
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
def lp(x, th, box):
    p = len(x); nA = 7*p; nv = nA + 7*p
    ai = lambda l, i: l*p + i; ci = lambda i, q: nA + i*7 + q
    A, b = [], []
    for i in range(p):
        r = np.zeros(nv)
        for q in range(7): r[ci(i,q)] = 1
        A.append(r); b.append(x[i])
    for l, line in enumerate(LINES):
        for i in range(p):
            r = np.zeros(nv); r[ai(l,i)] = 1
            for q in range(7):
                if q not in line: r[ci(i,q)] = -1
            A.append(r); b.append(0)
        r = np.zeros(nv)
        for i in range(p): r[ai(l,i)] = -1
        A.append(r); b.append(-1)
    bounds = [((th[i] if box[l] == i else 0), x[i]) for l in range(7) for i in range(p)] + [(0, None)]*(7*p)
    return linprog(np.zeros(nv), A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method='highs').status == 0
def template(A, B, C): return (A, A, B, A, B, C, A)
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 3)
p = int(sys.argv[1]); N = int(sys.argv[3]) if len(sys.argv) > 3 else 150
fails = 0; tmpl_all = 0
for s in range(N):
    while True:
        x = [rng.uniform(0.05, 1.2) for _ in range(p)]
        th = [xi - rng.uniform(0, 3*xi/7) for xi in x]
        if sum(th) < 1 or any(t > 1 for t in th): continue
        d = sum(xi - ti for xi, ti in zip(x, th))
        if 0.75 < d < 0.8: break
    oks = [lp(x, th, template(*t)) for t in itertools.permutations(range(p), 3)]
    if not any(oks):
        fails += 1; print("TEMPLATE FAILS for all triples:", [round(v,3) for v in x], [round(v,3) for v in th], round(d,4), flush=True)
    if all(oks): tmpl_all += 1
print(f"p={p}: samples {N}, no template triple works: {fails}; all triples work: {tmpl_all}")
