#!/usr/bin/env python3
"""w7_ref_denseTwoPart_integer.py -- INTEGER (finite) version, needed for the TRANSFER statement.
Referee's integer construction (hand proof in notes_referee_w7.md [denseTwoPart] entry 2):
 T = tau*(G) >= 3R/4 + 3  (i.e. 4T >= 3R + 12), G intersecting integer, anchor (e,0):
  g* = argmin{b : a <= e/2 - 1};  Case 1': 3b* <= 2x-3 : E0 split into 4 near-equal integers on 3,4,5,6;
                                    O: ceil(b*/2) on 0,1,2; six rows g*.
  Case 2': a'' = min{a : b < b*}, b'' = beta(a''); E0: (ceil(a''/2), ceil(a''/2), floor(a''/2)) on 3,4,5,
           remainder on 6;  O: v=ceil(b''/2) on 0,1,2 and max(0,b*-2v) on 6;  g'' on lines through 6.
 Checked exactly (integers) and by brute force on the actual 7 sets.
Part (b): for every qualifying state with 4T > 3R, decide by MILP (HiGHS; feasible solutions re-verified exactly;
infeasibility is NUMERICAL) whether ANY integer anchored Fano realisation exists; report the largest 4T-3R among
states with none (shows how much slack integrality needs).
Usage: seed R steps restarts"""
import sys, random
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from w7_ref_denseTwoPart_lib import *

seed, R, steps, restarts = map(int, sys.argv[1:5]); random.seed(seed)

def ceil2(v): return -((-v) // 2)

def integer_construction(G, e, x):
    small = [g for g in G if 2 * g[0] <= e - 2]
    if not small: return None, 'no g*'
    bstar = min(g[1] for g in small); gstar = min(g for g in small if g[1] == bstar)
    rows = [None] * 7; rows[L] = (e, 0)
    if 3 * bstar <= 2 * x - 3:
        q, r = divmod(e, 4); parts = [q + 1] * r + [q] * (4 - r)
        m0 = dict(zip(OFF, parts)); v = ceil2(bstar); m1 = {0: v, 1: v, 2: v}
        for i in range(7):
            if i != L: rows[i] = gstar
        case = 1
    else:
        app = min(g[0] for g in G if g[1] < bstar); bpp = beta(G, app); gpp = (app, bpp)
        if gpp not in G: return None, 'gpp not type'
        c = ceil2(app); f = app // 2
        m0 = {3: c, 4: c, 5: f, 6: e - 2 * c - f}
        v = ceil2(bpp); m1 = {0: v, 1: v, 2: v, 6: max(0, bstar - 2 * v)}
        for i, l in enumerate(LINES):
            if i != L: rows[i] = gpp if 6 in l else gstar
        case = 2
    return (rows, m0, m1, case), None

def milp_any(G, e, x):
    G = list(G); nG = len(G); nonL = [i for i in range(7) if i != L]
    # vars: m3..m6 (4), n0..n6 (7), y[i][g] (6*nG)
    nv = 4 + 7 + 6 * nG
    def yidx(k, g): return 11 + k * nG + g
    A = []; lo = []; hi = []
    row = np.zeros(nv); row[0:4] = 1; A.append(row); lo.append(e); hi.append(e)
    row = np.zeros(nv); row[4:11] = 1; A.append(row); lo.append(0); hi.append(x)
    for k, i in enumerate(nonL):
        row = np.zeros(nv)
        for g in range(nG): row[yidx(k, g)] = 1
        A.append(row); lo.append(1); hi.append(1)
        row = np.zeros(nv)
        for j, p in enumerate(OFF):
            if p not in LINES[i]: row[j] = 1
        for g in range(nG): row[yidx(k, g)] = -G[g][0]
        A.append(row); lo.append(0); hi.append(np.inf)
        row = np.zeros(nv)
        for p in range(7):
            if p not in LINES[i]: row[4 + p] = 1
        for g in range(nG): row[yidx(k, g)] = -G[g][1]
        A.append(row); lo.append(0); hi.append(np.inf)
    ub = np.array([e] * 4 + [x] * 7 + [1] * (6 * nG), dtype=float)
    res = milp(np.zeros(nv), constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.ones(nv),
               bounds=Bounds(np.zeros(nv), ub))
    if res.status != 0: return None
    sol = np.round(res.x).astype(int)
    m0 = {OFF[j]: int(sol[j]) for j in range(4)}; m1 = {p: int(sol[4 + p]) for p in range(7)}
    rows = [None] * 7; rows[L] = (e, 0)
    for k, i in enumerate(nonL):
        gs = [g for g in range(nG) if sol[yidx(k, g)] == 1]; rows[i] = G[gs[0]]
    f = verify_realisation(rows, m0, m1, e, x)
    if f: raise RuntimeError('MILP solution fails exact verification %s' % f)
    return rows, m0, m1

stats = dict(qual=0, big=0, constr_fail=0, brute=0, brute_fail=0, milp_none=0, milp_yes=0)
worst = None; seen = set()

def handle(G, e, x):
    global worst
    key = (e, x, tuple(sorted(G)))
    if key in seen: return
    seen.add(key)
    if not intersecting(G, e, x): return
    T = tau_star(G, e, x)
    if 4 * T <= 3 * R: return
    stats['qual'] += 1
    if 4 * T >= 3 * R + 12:
        stats['big'] += 1
        out, why = integer_construction(G, e, x)
        if out is None:
            stats['constr_fail'] += 1; print('CONSTRUCTION FAIL', why, e, x, sorted(G), T, flush=True); return
        rows, m0, m1, case = out
        stats['case%d' % case] = stats.get('case%d' % case, 0) + 1
        f = verify_realisation(rows, m0, m1, e, x)
        if f or any(r not in G for r in rows):
            stats['constr_fail'] += 1; print('CONSTRUCTION FAIL', case, f, e, x, sorted(G), T, flush=True); return
        if stats['brute'] < 300 and random.random() < 0.3:
            from fractions import Fraction as Fr
            verts, sets = integerise([(Fr(a), Fr(b)) for a, b in rows], {p: Fr(v) for p, v in m0.items()},
                                     {p: Fr(v) for p, v in m1.items()}, 1)
            stats['brute'] += 1
            if not brute_bad(verts, sets): stats['brute_fail'] += 1; print('BRUTE FAIL', e, x, sorted(G), flush=True)
    else:
        r = milp_any(G, e, x)
        if r is None:
            stats['milp_none'] += 1
            gap = 4 * T - 3 * R
            if worst is None or gap > worst[0]:
                worst = (gap, e, x, sorted(G), T); print('NO INTEGER ANCHORED TUPLE (MILP):', worst, flush=True)
        else:
            stats['milp_yes'] += 1

for rs in range(restarts):
    e = random.randint((3 * R) // 4 + 1, R); x = random.randint(R // 2, 2 * R)
    G = {(e, 0)}; cur = tau_star_fixed(G, e, x) or -1
    for st in range(steps):
        H = set(G); mv = random.random()
        if mv < 0.55 or len(H) == 1:
            a = random.randint(1, e); bmax = min(x, R - a)
            if bmax < 0: continue
            H.add((a, bmax if random.random() < 0.6 else random.randint(0, bmax)))
        elif mv < 0.85:
            H.discard(random.choice([g for g in H if g != (e, 0)]))
        else:
            g = random.choice([g for g in H if g != (e, 0)]); H.discard(g); a, b = g
            a2 = min(e, max(1, a + random.randint(-2, 2))); b2 = min(x, R - a2, max(0, b + random.randint(-2, 2)))
            H.add((a2, b2))
        if not intersecting(H, e, x): continue
        new = tau_star_fixed(H, e, x); new = -1 if new is None else new
        if new >= cur or random.random() < 0.05:
            G, cur = H, new
            if 4 * cur > 3 * R: handle(G, e, x)
print('R', R, stats, 'worst no-integer-tuple (4T-3R, e, x, G, T):', worst, flush=True)
