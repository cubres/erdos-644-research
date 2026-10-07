#!/usr/bin/env python3
"""EXACT certificate (convexity argument): the template-feasible parameter set is the projection of a
polyhedron, hence convex; so the domain polytope D is covered iff every vertex of D is feasible.
Each vertex: exact rational LP feasibility via sympy.solvers.simplex.lpmin (Rational arithmetic),
and the returned rational point is re-checked against every constraint with Fractions.
Modes: '3box' (parts A,B,C), 'pbox' (A,B,C + merged light part L), '2box' (template with C:=B)."""
import itertools, sys
from fractions import Fraction as F
import sympy as sp
from sympy.solvers.simplex import lpmin
mode = sys.argv[1]
al,be,ga,de,qB,qC,lQ,lB,lC = sp.symbols('al be ga de qB qC lQ lB lC')
def cons_for(xA,xB,xC,tA,tB,tC,xL):
    c = [2*al+be <= 4*(xA-tA), al <= 2*(xA-tA), be <= 2*(xA-tA), 2*al+be <= 2*xA, al <= xA, be <= xA]
    if mode == '2box':
        # parts A,B only; pencil lines L2,L4,L5 all box B: point 6 in B: 3 tB <= 2 xB ; rows P: al + tB + gB >= 1
        c += [3*tB <= 2*xB, qB*2 + tB <= 2*xB, 4*qB + 3*tB <= 4*xB, qB <= xB,
              -qB <= tA - 1, -al <= tB - 1, -be <= tB - 1]
        return c
    c += [ga <= 2*(xB-tB), 2*qB <= 2*xB-tB, 2*qB+ga <= 2*xB, 4*qB+ga <= 4*xB-2*tB, qB <= xB, ga <= xB,
          2*de <= 2*xC-tC, 2*qC <= 2*xC-tC, de+2*qC <= 2*xC, 4*qC+2*de <= 4*xC-tC, qC <= xC, de <= xC]
    if mode == 'pbox':
        c += [2*lB+lC <= 2*xL, 2*lQ+lB <= 2*xL, 2*lQ+lC <= 2*xL, 4*lQ+2*lB+lC <= 4*xL, lQ <= xL, lB <= xL, lC <= xL,
              -qB-qC-lQ <= tA-1, -al-de-lB <= tB-1, -be-ga-lC <= tC-1]
    else:
        c += [-qB-qC <= tA-1, -al-de <= tB-1, -be-ga <= tC-1]
    return c
VARS = {'2box': [al,be,qB], '3box': [al,be,ga,de,qB,qC], 'pbox': [al,be,ga,de,qB,qC,lQ,lB,lC]}[mode]
# ---- domain vertices
names = {'2box': ['xA','xB','tA','tB'], '3box': ['xA','xB','xC','tA','tB','tC'], 'pbox': ['xA','xB','xC','tA','tB','tC','xL']}[mode]
n = len(names); idx = {s:i for i,s in enumerate(names)}
def row(d, c):
    a = [F(0)]*n
    for k, v in d.items(): a[idx[k]] = F(v)
    return (a, F(c))
dom = []
parts = [('xA','tA'),('xB','tB')] + ([('xC','tC')] if mode != '2box' else [])
for xs, ts in parts:
    dom += [row({ts:1, xs:F(-4,7)},0), row({xs:1, ts:-1},0), row({ts:-1},1)]
tsum = {ts:1 for _,ts in parts}; dsum = {}
for xs, ts in parts: dsum[xs] = 1; dsum[ts] = -1
if mode == 'pbox':
    dom += [row({'xL':1},0), row({'xL':-1},F(7,4))]
    tsum['xL'] = 1; dsum['xL'] = F(3,7)
dom += [row(tsum, -1), row(dsum, F(-3,4))]
def solve(rows):
    M = [a[:]+[-c] for a,c in rows]; r = 0
    for col in range(n):
        pr = next((i for i in range(r,len(M)) if M[i][col] != 0), None)
        if pr is None: return None
        M[r], M[pr] = M[pr], M[r]; pv = M[r][col]; M[r] = [v/pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col] != 0:
                f = M[i][col]; M[i] = [a-f*b for a,b in zip(M[i],M[r])]
        r += 1
    return [M[i][n] for i in range(n)]
verts = set()
for S in itertools.combinations(range(len(dom)), n):
    sol = solve([dom[i] for i in S])
    if sol and all(sum(a*v for a,v in zip(d[0],sol))+d[1] >= 0 for d in dom): verts.add(tuple(sol))
verts = sorted(verts)
print(f"mode {mode}: {len(verts)} domain vertices", flush=True)
allok = True
for v in verts:
    P = dict(zip(names, [sp.Rational(x.numerator, x.denominator) for x in v]))
    args = [P.get(k, sp.Integer(0)) for k in ['xA','xB','xC','tA','tB','tC','xL']]
    cons = cons_for(*args) + [s >= 0 for s in VARS]
    try:
        val, sol = lpmin(sp.Integer(0), cons)
        ok = all(bool(c.subs(sol)) for c in cons)
    except Exception as e:
        ok = False; sol = str(e)
    if not ok:
        allok = False; print("  INFEASIBLE at vertex", {k: str(x) for k, x in zip(names, v)}, flush=True)
print(f"mode {mode}: ALL VERTICES FEASIBLE = {allok}")
