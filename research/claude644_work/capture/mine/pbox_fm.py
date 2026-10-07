#!/usr/bin/env python3
"""Exact certificate for p one-sided boxes (any p>=3) via 3 template boxes + one merged light part L.
Domain: 4x_i/7<=t_i<=x_i, t_i<=1 (i=A,B,C); 0<=xL<=7/4; sum_{ABC}(x-t) + (3/7)xL >= 3/4;
sum_{ABC} t + xL >= 1.  Vertex check of the FM projection (Fractions)."""
from fractions import Fraction as F
import itertools, sys
V = ['al','be','ga','de','qB','qC','lQ','lB','lC']
P = ['xA','xB','xC','tA','tB','tC','xL']
def C(v, p, c=0): return ({k: F(x) for k, x in v.items() if x}, {k: F(x) for k, x in p.items() if x}, F(c))
cons = [
 C({'al':2,'be':1},{'xA':4,'tA':-4}), C({'al':1},{'xA':2,'tA':-2}), C({'be':1},{'xA':2,'tA':-2}),
 C({'al':2,'be':1},{'xA':2}), C({'al':1},{'xA':1}), C({'be':1},{'xA':1}),
 C({'ga':1},{'xB':2,'tB':-2}), C({'qB':2},{'xB':2,'tB':-1}), C({'qB':2,'ga':1},{'xB':2}),
 C({'qB':4,'ga':1},{'xB':4,'tB':-2}), C({'qB':1},{'xB':1}), C({'ga':1},{'xB':1}),
 C({'de':2},{'xC':2,'tC':-1}), C({'qC':2},{'xC':2,'tC':-1}), C({'de':1,'qC':2},{'xC':2}),
 C({'qC':4,'de':2},{'xC':4,'tC':-1}), C({'qC':1},{'xC':1}), C({'de':1},{'xC':1}),
 # light part L
 C({'lB':2,'lC':1},{'xL':2}), C({'lQ':2,'lB':1},{'xL':2}), C({'lQ':2,'lC':1},{'xL':2}),
 C({'lQ':4,'lB':2,'lC':1},{'xL':4}), C({'lQ':1},{'xL':1}), C({'lB':1},{'xL':1}), C({'lC':1},{'xL':1}),
 # rows
 C({'qB':-1,'qC':-1,'lQ':-1},{'tA':1},-1), C({'al':-1,'de':-1,'lB':-1},{'tB':1},-1), C({'be':-1,'ga':-1,'lC':-1},{'tC':1},-1),
] + [C({v:-1},{}) for v in V]
def combine(c1, c2, var):
    a, b = c1[0][var], c2[0][var]; l1, l2 = -b, a
    v = {k: l1*c1[0].get(k,0)+l2*c2[0].get(k,0) for k in set(c1[0])|set(c2[0])}
    p = {k: l1*c1[1].get(k,0)+l2*c2[1].get(k,0) for k in set(c1[1])|set(c2[1])}
    return ({k:x for k,x in v.items() if x}, {k:x for k,x in p.items() if x}, l1*c1[2]+l2*c2[2])
def key(c):
    v, p, k = c; allc = [abs(x) for x in list(v.values())+list(p.values())+[k] if x]; m = max(allc) if allc else 1
    return (tuple(sorted((a,b/m) for a,b in v.items())), tuple(sorted((a,b/m) for a,b in p.items())), k/m)
# domain vertices (for pruning + final check)
def vec(d, c): return ([F(d.get(p,0)) for p in P], F(c))
dom = []
for s, xs, ts in [('A','xA','tA'),('B','xB','tB'),('C','xC','tC')]:
    dom += [vec({ts:1, xs:F(-4,7)},0), vec({xs:1, ts:-1},0), vec({ts:-1},1)]
dom += [vec({'xL':1},0), vec({'xL':-1},F(7,4)),
        vec({'xA':1,'xB':1,'xC':1,'tA':-1,'tB':-1,'tC':-1,'xL':F(3,7)}, F(-3,4)),
        vec({'tA':1,'tB':1,'tC':1,'xL':1}, -1)]
def solve(rows, n):
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
for S in itertools.combinations(range(len(dom)), 7):
    sol = solve([dom[i] for i in S], 7)
    if sol and all(sum(a*v for a,v in zip(d[0],sol))+d[1] >= 0 for d in dom): verts.add(tuple(sol))
verts = list(verts); print("domain vertices:", len(verts), flush=True)
def holds_on_domain(pc, const):
    a = [F(pc.get(p,0)) for p in P]
    return min(sum(ai*vi for ai,vi in zip(a,v))+const for v in verts)
cur = cons
for var in V:
    pos = [c for c in cur if c[0].get(var,0) > 0]; neg = [c for c in cur if c[0].get(var,0) < 0]
    zero = [c for c in cur if c[0].get(var,0) == 0]
    new = zero + [combine(a,b,var) for a in pos for b in neg]
    seen = {}
    for c in new: seen.setdefault(key(c), c)
    cur = list(seen.values())
    # prune: parameter-only constraints that hold on the whole domain are redundant for the final check
    keep = []
    for c in cur:
        if not c[0]:
            m = holds_on_domain(c[1], c[2])   # constraint: 0 <= sum p*par + const
            if m >= 0: continue
        keep.append(c)
    cur = keep
    print(f"eliminated {var}: {len(cur)} constraints", flush=True)
bad = [c for c in cur if not c[0]]
print("projected inequalities violated somewhere on the domain:", len(bad))
for c in bad[:3]:
    pc = c[1]; m = holds_on_domain(pc, c[2])
    v = min(verts, key=lambda v: sum(F(pc.get(p,0))*vi for p,vi in zip(P,v)) + c[2])
    print("  min", m, "at", dict(zip(P,map(str,v))))
