#!/usr/bin/env python3
"""Referee w7, claim 'paper', Section 7 of paper_0865.tex:
(1) K_9^(5) has property (7,2)?  (Remark after Theorem 7.2)  exact MILP: min number of
    4-subsets of [9] covering all 36 pairs (complements of 7 edges must cover all pairs).
(2) Theorem 7.2 (GT) construction: random good triples with N<=2t-3, parity splits as in
    the proof, worst-case (full complement) requested edges; check request sizes <= t-1
    and brute-force badness.
(3) Theorem 7.3 (TC): random instances, g1,g2 = random subsets avoiding T_A,T_B
    (including full complements); brute-force badness.
(4) Theorem 7.4 (K4 criterion): random instances satisfying hypotheses; badness.
"""
import random, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def no2(edges, pts):
    types = set()
    for p in pts:
        t = 0
        for i, E in enumerate(edges):
            if p in E: t |= 1 << i
        types.add(t)
    full = (1 << len(edges))-1
    return not any((a | b) == full for a in types for b in types)

# (1)
subs = list(itertools.combinations(range(9), 4))
pairs = list(itertools.combinations(range(9), 2))
A = np.array([[1 if (p[0] in s and p[1] in s) else 0 for s in subs] for p in pairs])
res = milp(c=np.ones(len(subs)), constraints=[LinearConstraint(A, lb=np.ones(len(pairs)))],
           integrality=np.ones(len(subs)), bounds=Bounds(0, 1))
print('(1) min #4-subsets of [9] covering all pairs =', round(res.fun), '-> K_9^(5) has (7,2):', round(res.fun) > 7)

rnd = random.Random(2026)
# (2) GT
bad_cnt = 0; n2 = 0
for it in range(20000):
    t = rnd.randint(3, 9)
    N = rnd.randint(3, 2*t-3)
    U = list(range(N)); out = list(range(N, N+6))
    # random good triple covering U exactly
    G = [set(), set(), set()]
    for v in U:
        typ = rnd.choice([(0,), (1,), (2,), (0, 1), (0, 2), (1, 2)])
        for i in typ: G[i].add(v)
    if any(not g for g in G): continue
    A_ = [v for v in U if v not in G[0]]; B_ = [v for v in G[0] if v not in G[1]]; C_ = [v for v in G[0] if v in G[1]]
    # choose parity splits as in the proof
    def split(L, eps):
        k = (len(L)+eps)//2
        return L[:k], L[k:]
    best = None
    for eA in ([0] if len(A_) % 2 == 0 else [1, -1]):
        for eB in ([0] if len(B_) % 2 == 0 else [1, -1]):
            for eC in ([0] if len(C_) % 2 == 0 else [1, -1]):
                Aa, Aa2 = split(A_, eA); Bb, Bb2 = split(B_, eB); Cc, Cc2 = split(C_, eC)
                lines = [Aa+Bb+Cc, Aa2+Bb2+Cc, Aa2+Bb+Cc2, Aa+Bb2+Cc2]
                mx = max(len(l) for l in lines)
                if best is None or mx < best[0]: best = (mx, lines)
    mx, lines = best
    n2 += 1
    if mx > t-1:
        bad_cnt += 1; print('GT size fail', N, t, mx); continue
    pts = set(U) | set(out)
    edges = G + [pts - set(l) for l in lines]
    if not no2(edges, pts):
        bad_cnt += 1; print('GT not bad', N, t)
print('(2) GT instances', n2, 'failures', bad_cnt)

# (3) TC
fails = 0; n3 = 0
for it in range(30000):
    nE = rnd.randint(1, 10); nO = rnd.randint(0, 10)
    E0 = list(range(nE)); O = list(range(nE, nE+nO)); pts = set(E0) | set(O)
    b1, b2, c1, c2 = set(), set(), set(), set()
    for v in E0:
        bb = rnd.choice([(), (1,), (2,)]); cc = rnd.choice([(), (1,), (2,)])
        if 1 in bb: b1.add(v)
        if 2 in bb: b2.add(v)
        if 1 in cc: c1.add(v)
        if 2 in cc: c2.add(v)
    for v in O:
        for s in (b1, b2, c1, c2):
            if rnd.random() < 0.5: s.add(v)
    DA, DB = set(), set()
    for v in E0:
        inA = (v in b1 and v in c1) or (v in b2 and v in c2)
        inB = (v in b1 and v in c2) or (v in b2 and v in c1)
        if inA: DA.add(v)
        elif inB: DB.add(v)
        else: (DA if rnd.random() < 0.5 else DB).add(v)
    TA = DA | (b1 & c1) | (b2 & c2); TB = DB | (b1 & c2) | (b2 & c1)
    for mode in range(2):
        g1 = pts - TA; g2 = pts - TB
        if mode:
            g1 = {v for v in g1 if rnd.random() < 0.7}; g2 = {v for v in g2 if rnd.random() < 0.7}
        edges = [set(E0), b1, b2, c1, c2, g1, g2]
        n3 += 1
        if not no2(edges, pts):
            fails += 1
            if fails < 5: print('TC fail', E0, b1, b2, c1, c2, DA, DB)
print('(3) TC instances', n3, 'failures', fails)

# (4) K4 criterion
fails = 0; n4 = 0
pairs4 = list(itertools.combinations(range(4), 2))
tris = [set(itertools.combinations(tr, 2)) for tr in itertools.combinations(range(4), 3)]
for it in range(30000):
    parts = [list(range(10*i, 10*i+rnd.randint(0, 3))) for i in range(4)]
    E0 = set(sum(parts, [])); O = list(range(100, 100+rnd.randint(0, 8)))
    Gs = {}
    for (a, b) in pairs4:
        Gs[(a, b)] = {v for v in parts[a]+parts[b] if rnd.random() < 0.7}
    for v in O:
        while True:
            sig = {p for p in pairs4 if rnd.random() < 0.5}
            if not any(tr <= sig for tr in tris): break
        for p in sig: Gs[p].add(v)
    pts = E0 | set(O)
    if not pts: continue
    edges = [E0] + [Gs[p] for p in pairs4]
    n4 += 1
    if not no2(edges, pts):
        fails += 1
        if fails < 5: print('K4 fail')
print('(4) K4 instances', n4, 'failures', fails)
