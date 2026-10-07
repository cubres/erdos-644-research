#!/usr/bin/env python3
"""w4_tcglobal_convex_anchor.py -- EXPLORATORY (floating LP): convex admissible sets Adm = conv(V) cap {sum=r}
(V random vertices with sum r) over p parts; tau* via tau* = min_{lam in simplex} [sum x - knapsack(lam)] on a grid
(upper bound on tau*, so 'tau*>3/4' is conservative-ish); for each vertex a0 of Adm test
 (H) homogeneous anchored template: exists b in Adm with 6b + a0 <= 4x;
 (G) general anchored Fano-downset: rows 2..7 in Adm with note Lemma 7.63 constraints (LP).
Usage: seed samples p nverts"""
import random, sys, itertools
import numpy as np
from scipy.optimize import linprog
seed, S, p, nv = (int(x) for x in sys.argv[1:5]); random.seed(seed)
r = 1.0
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
def knap(lam, x, mu):
    # max sum u, 0<=u<=x, lam.u <= mu  (fractional knapsack: cheapest first)
    order = sorted(range(len(x)), key=lambda i: lam[i]); tot = 0.0; budget = mu
    for i in order:
        if lam[i] <= 1e-15: tot += x[i]; continue
        take = min(x[i], budget/lam[i]); tot += take; budget -= take*lam[i]
        if budget <= 1e-15: break
    return tot
def tau_star(V, x, grid=60):
    best = None
    for comb in itertools.product(range(grid+1), repeat=len(x)-1):
        if sum(comb) > grid: continue
        lam = [c/grid for c in comb] + [1 - sum(comb)/grid]
        mu = min(sum(l*a for l,a in zip(lam, v)) for v in V)
        val = sum(x) - knap(lam, x, mu)
        best = val if best is None else min(best, val)
    return best
def hom_anchor(V, x, a0):
    # b = sum w_j V_j, w>=0, sum w=1 ; 6b <= 4x - a0
    A = [[6*v[i] for v in V] for i in range(len(x))]; b = [4*x[i]-a0[i] for i in range(len(x))]
    res = linprog(np.zeros(len(V)), A_ub=A, b_ub=b, A_eq=[[1]*len(V)], b_eq=[1], bounds=(0,None), method='highs')
    return res.status == 0
def gen_anchor(V, x, a0):
    # rows 1..6 (Fano points 1..6; point 0 = anchor) each a convex combo of V: vars w[row][j]
    nV = len(V); nvar = 6*nV; A_ub, b_ub, A_eq, b_eq = [], [], [], []
    for rr in range(6):
        row = [0]*nvar
        for j in range(nV): row[rr*nV+j] = 1
        A_eq.append(row); b_eq.append(1)
    for i in range(len(x)):
        def load_row(rows, const):
            row = [0]*nvar
            for rr in rows:
                for j in range(nV): row[(rr-1)*nV+j] += V[j][i]
            return row
        for L in LINES:
            rows = [q for q in L if q != 0]; const = a0[i] if 0 in L else 0
            A_ub.append(load_row(rows, const)); b_ub.append(2*x[i]-const)
        A_ub.append(load_row(range(1,7), a0[i])); b_ub.append(4*x[i]-a0[i])
    res = linprog(np.zeros(nvar), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0,None), method='highs')
    return res.status == 0
tested = hfail = gfail = 0
for _ in range(S):
    x = [random.uniform(0.2, 1.5) for _ in range(p)]
    V = []
    for _ in range(nv):
        for _t in range(100):
            w = [random.random() for _ in range(p)]; s = sum(w); v = [r*wi/s for wi in w]
            if all(v[i] <= x[i] for i in range(p)): V.append(v); break
    if len(V) < nv: continue
    ts = tau_star(V, x)
    if ts <= 0.76: continue
    tested += 1
    for a0 in V:
        h = hom_anchor(V, x, a0)
        if not h:
            hfail += 1
            g = gen_anchor(V, x, a0)
            if not g:
                gfail += 1; print("GENERAL ANCHOR FAILS: x", [round(t,3) for t in x], "V", [[round(t,3) for t in v] for v in V], "a0", [round(t,3) for t in a0], "tau*~", round(ts,3), flush=True)
print(f"convex families tested (tau*>0.76): {tested}; homogeneous-anchor failures: {hfail}; general-anchor failures: {gfail}")
