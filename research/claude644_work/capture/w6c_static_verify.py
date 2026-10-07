#!/usr/bin/env python3
"""w6c_static_verify.py -- independent VERTEX-LEVEL exact check of the static calibration on the a=0 near-Fano
support (28 classes S u {h} of size b, seven Fano coordinates, six rows = coordinates 1..6).
Computes from scratch: rows, Pi, P, A_i, W_i, delta_i, part-2 sets {x} u N(x) u Q_i, and for row 0 the
Lemma 7.93 bound min |N_Gamma[Y]| over |Y| >= |P5|-p+1 restricted to Y = union of whole classes
(exhaustive over class subsets)."""
import itertools, sys
b = int(sys.argv[1]) if len(sys.argv) > 1 else 2
lines = [frozenset(s) for s in ([0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5])]
V = []   # (class id, vertex id); comp type over 7 coords
comp = []
cls = []
for S in lines:
    for h in range(7):
        if h in S: continue
        cls.append(S | {h})
for ci, C in enumerate(cls):
    for j in range(b):
        V.append(ci); comp.append(C)
n = len(V)
rowsc = [c for c in range(1, 7)]
rows = [set(v for v in range(n) if c not in comp[v]) for c in rowsc]
def pierce(pair, R):
    return all(pair[0] in F or pair[1] in F for F in R)
pairs = list(itertools.combinations(range(n), 2))
Pi = [pr for pr in pairs if pierce(pr, rows)]
P = set(x for pr in Pi for x in pr)
print('b', b, 'n', n, 'rows', [len(F) for F in rows], '|Pi|', len(Pi), 'p', len(P))
W = []; delta = []; T2 = []
Pis = set(Pi)
Gam = []
for i in range(6):
    R = rows[:i] + rows[i+1:]
    G = [pr for pr in pairs if pierce(pr, R)]
    Ai = [pr for pr in G if pr not in Pis]
    Wi = set(x for pr in Ai for x in pr)
    W.append(len(Wi)); Gam.append(G)
    delta.append(min(len(set(pr) - Wi) for pr in Pi))
    Qi = set(x for pr in Ai if (pr[0] not in P or pr[1] not in P) for x in pr)
    best = None
    for x in P & rows[i]:
        N = set(y for pr in Pi if x in pr for y in pr if y != x)
        val = len({x} | N | Qi)
        best = val if best is None else min(best, val)
    T2.append(best)
print('W', W, 'delta', delta, 'T2', T2)
# Lemma 7.93 for row 0, class-level Y
G = Gam[0]
nb = {v: set() for v in range(n)}
for (u, w) in G: nb[u].add(w); nb[w].add(u)
P5 = set(v for v in range(n) if nb[v])
need = len(P5) - len(P) + 1
clsP5 = sorted(set(V[v] for v in P5))
best = None
for m in range(1, len(clsP5) + 1):
    for sub in itertools.combinations(clsP5, m):
        Y = set(v for v in P5 if V[v] in sub)
        if len(Y) < need: continue
        NY = set(Y)
        for y in Y: NY |= nb[y]
        if best is None or len(NY) < best[0]: best = (len(NY), sub)
print('|P5|', len(P5), 'need', need, 'class-level min|N[Y]|', best[0], ' k', max(len(F) for F in rows))
# partial-class search: whole classes + a partial class (exhaustive over subsets and the partial one)
best2 = None
for m in range(0, len(clsP5) + 1):
    for sub in itertools.combinations(clsP5, m):
        Yw = set(v for v in P5 if V[v] in sub)
        base = set(Yw)
        for y in Yw: base |= nb[y]
        if len(Yw) >= need:
            if best2 is None or len(base) < best2[0]: best2 = (len(base), sub, None)
            continue
        for c2 in clsP5:
            if c2 in sub: continue
            members = [v for v in P5 if V[v] == c2]
            j = need - len(Yw)
            if j > len(members): continue
            Y = Yw | set(members[:j])
            NY = set(Y)
            for y in Y: NY |= nb[y]
            if best2 is None or len(NY) < best2[0]: best2 = (len(NY), sub, (c2, j))
print('whole+one partial class: min|N[Y]|', best2[0], best2[1:], ' |Y|>=', need)
