#!/usr/bin/env python3
"""Exact certificate: every projected inequality of the three-box template holds on the closed domain
D = {4x_i/7 <= theta_i <= x_i, theta_i <= 1, sum theta >= 1, sum(x - theta) >= T0}. Vertex enumeration
with Fractions (a linear function attains its minimum over a polytope at a vertex)."""
from fractions import Fraction as F
import itertools, pickle, sys
P = ['xA','xB','xC','tA','tB','tC']
T0 = F(sys.argv[1]) if len(sys.argv) > 1 else F(3,4)
def vec(d, c): return ([F(d.get(p,0)) for p in P], F(c))
X = {'A':'xA','B':'xB','C':'xC'}; Tn = {'A':'tA','B':'tB','C':'tC'}
dom = []
for s in 'ABC':
    dom.append(vec({Tn[s]:1, X[s]:F(-4,7)}, 0))   # t - 4x/7 >= 0
    dom.append(vec({X[s]:1, Tn[s]:-1}, 0))         # x - t >= 0
    dom.append(vec({Tn[s]:-1}, 1))                 # 1 - t >= 0
dom.append(vec({'tA':1,'tB':1,'tC':1}, -1))        # sum t - 1 >= 0
dom.append(vec({'xA':1,'xB':1,'xC':1,'tA':-1,'tB':-1,'tC':-1}, -T0))
def solve(rows):
    # rows: list of (a, c) meaning a.p + c = 0 ; gaussian elimination
    M = [a[:] + [-c] for a, c in rows]; n = 6
    r = 0; piv = []
    for col in range(n):
        pr = next((i for i in range(r, len(M)) if M[i][col] != 0), None)
        if pr is None: return None
        M[r], M[pr] = M[pr], M[r]
        pv = M[r][col]; M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col] != 0:
                f = M[i][col]; M[i] = [a - f*b for a, b in zip(M[i], M[r])]
        piv.append(col); r += 1
    return [M[i][n] for i in range(n)]
verts = set()
for S in itertools.combinations(range(len(dom)), 6):
    sol = solve([dom[i] for i in S])
    if sol is None: continue
    if all(sum(a*v for a, v in zip(d[0], sol)) + d[1] >= 0 for d in dom):
        verts.add(tuple(sol))
verts = list(verts)
print("domain vertices:", len(verts))
proj = pickle.load(open('threebox_proj.pkl','rb'))
worst = None; bad = 0
for pcoef, const in proj:
    a = [F(pcoef.get(p,0)) for p in P]
    m = min(sum(ai*vi for ai, vi in zip(a, v)) + const for v in verts)
    if worst is None or m < worst[0]: worst = (m, pcoef, const)
    if m < 0: bad += 1
print(f"T0={T0}: violated projected inequalities: {bad}; worst min value {worst[0]} ({float(worst[0]):.5f})")
if bad:
    m, pc, c = worst
    v = min(verts, key=lambda v: sum(F(pc.get(p,0))*vi for p, vi in zip(P, v)) + c)
    print("worst vertex:", dict(zip(P, map(str, v))), "ineq:", {k: str(x) for k, x in pc.items()}, "const", c)
