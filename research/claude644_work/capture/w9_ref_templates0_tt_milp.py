#!/usr/bin/env python3
"""Referee w9 [templates#0]: NUMERICAL global counterexample search for Theorem TT by MILP (HiGHS).
Retention argument: a counterexample has <=5 witness parts (failing parts of Ha,Hb,Qb,Qa,V); restricting to
them keeps all failures, keeps K1/K2 among them, and gives type sums <= 1.  So the MILP with p=5 parts and
sums <= 1 is a complete relaxation.  Strictness (failures, positivity) is modelled by a common margin gamma,
maximised.  gamma* <= ~1e-9 means: no counterexample (numerically).
Sanity (non-vacuity): dropping V (or Q_b) must give gamma* > 0.
Usage: python3 w9_ref_templates0_tt_milp.py p [drop]"""
import sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
p = int(sys.argv[1]); drop = sys.argv[2] if len(sys.argv) > 2 else None
sums_eq = (len(sys.argv) > 3 and sys.argv[3] == 'eq')
names = []
def var(n):
    names.append(n); return len(names) - 1
a = [var(f'a{i}') for i in range(p)]; b = [var(f'b{i}') for i in range(p)]; x = [var(f'x{i}') for i in range(p)]
pa = [var(f'pa{i}') for i in range(p)]; pb = [var(f'pb{i}') for i in range(p)]; w = [var(f'w{i}') for i in range(p)]
g = var('gamma')
# templates: list of facets (ca, cb) meaning ca*s + cb*t  (s=a-load, t=b-load)
T = {'Ha': [(7/4, 0)], 'Hb': [(0, 7/4)], 'Qb': [(0, 3/2), (1, 3/4)], 'Qa': [(3/2, 0), (3/4, 1)],
     'V': [(1, 1), (5/4, 1/2)]}
if drop: del T[drop]
f = {}
for tn, facets in T.items():
    for i in range(p):
        for k in range(len(facets)):
            f[(tn, i, k)] = var(f'f_{tn}_{i}_{k}')
nv = len(names)
rows = []; lo = []; hi = []
def add(coefs, l, h):
    r = np.zeros(nv)
    for j, c in coefs: r[j] += c
    rows.append(r); lo.append(l); hi.append(h)
M = 10.0
for i in range(p):
    add([(a[i], 1), (pa[i], -1)], -np.inf, 0)              # a_i <= pa_i
    add([(b[i], 1), (pb[i], -1)], -np.inf, 0)
    add([(a[i], 1), (g, -1), (pa[i], -1)], -1, np.inf)     # a_i >= gamma - (1-pa_i)
    add([(b[i], 1), (g, -1), (pb[i], -1)], -1, np.inf)
    add([(x[i], 1), (a[i], -1)], 0, np.inf); add([(x[i], 1), (b[i], -1)], 0, np.inf)
    # K1: pa&pb => (x-a>=3/4) or (x-b>=3/4)
    add([(x[i], 1), (a[i], -1), (pa[i], -M), (pb[i], -M), (w[i], M)], 0.75 - 2 * M, np.inf)
    add([(x[i], 1), (b[i], -1), (pa[i], -M), (pb[i], -M), (w[i], -M)], 0.75 - 3 * M, np.inf)
    for j in range(p):
        if j != i:
            add([(x[i], 1), (a[i], -1), (x[j], 1), (b[j], -1), (pa[i], -M), (pb[j], -M)], 0.75 - 2 * M, np.inf)
add([(ai, 1) for ai in a], -np.inf if not sums_eq else 1, 1)
add([(bi, 1) for bi in b], -np.inf if not sums_eq else 1, 1)
for tn, facets in T.items():
    add([(f[(tn, i, k)], 1) for i in range(p) for k in range(len(facets))], 1, 1)
    for i in range(p):
        for k, (ca, cb) in enumerate(facets):
            # ca a_i + cb b_i - x_i >= gamma - M(1-f)
            add([(a[i], ca), (b[i], cb), (x[i], -1), (g, -1), (f[(tn, i, k)], -M)], -M, np.inf)
A = np.array(rows)
lb = np.zeros(nv); ub = np.ones(nv)
for i in range(p): ub[x[i]] = 3.0
integrality = np.zeros(nv)
for j, n in enumerate(names):
    if n.startswith(('pa', 'pb', 'w', 'f_')): integrality[j] = 1
c = np.zeros(nv); c[g] = -1
res = milp(c, constraints=LinearConstraint(A, lo, hi), integrality=integrality, bounds=Bounds(lb, ub),
           options={'disp': False, 'time_limit': 500})
print(f"p={p} drop={drop} sums_eq={sums_eq} status={res.status} msg={res.message}")
if res.x is not None:
    gam = res.x[g]
    print("gamma* =", gam)
    if gam > 1e-7:
        print(" a =", np.round(res.x[a], 5)); print(" b =", np.round(res.x[b], 5)); print(" x =", np.round(res.x[x], 5))
