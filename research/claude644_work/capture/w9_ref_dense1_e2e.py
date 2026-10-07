#!/usr/bin/env python3
"""w9_ref_dense1_e2e.py -- referee w9, claim dense#1 (Corollary Q), TYPE-CLOSED special case end to end.

H_S = all sets of V = E0 u O (|E0|=e, |O|=x) whose 2-part profile lies in S u {(e,0)}; S intersecting
(a+a'>e or b+b'>x for all pairs incl. equal), every type has a>=1 and e<=a+b<=k (so E0 is a smallest edge).
Exact: alpha = max{|w| : w<=n integer, no type <= w};  tau = N - alpha.
Proof chain of Corollary Q with D=3 (s=3):
  A = {u<=n : (u-3)^+ >= some type}  (type-closed => f in {0,1}),  r=k+6,  T = A^{<=r} u {e0}.
  (i)  tau*(T) >= tau - 8                                   [lower bound half]
  (ii) if tau*(T) > 3r/4: the anchored two-part template (g* from beta(e/2); Case 1 all g*, Case 2 g'' on the pencil
       at an off-L point, g* on the other three non-L lines) is Lemma-7.63-feasible; class masses (LP), rounding,
       integer windows >= load-3; every window contains an edge of H_S; the explicit 7 edges are brute-force checked
       to have NO 2-transversal.
  (iii) whenever tau > (3k+50)/4 the chain (ii) must fire (the Corollary's contrapositive).
Also records max(tau - 3k/4) among instances where NO bad tuple is produced (sanity) and the floor-rounding issue.
Usage: python3 w9_ref_dense1_e2e.py SEED NINST
"""
import sys, random
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog

LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]   # line 0 = L (anchor)
OFFL = [3,4,5,6]

def alpha_of(types, n):
    e, x = n
    best = -1
    for w0 in range(e + 1):
        # max w1 with no type <= (w0,w1)
        bmin = min([b for (a, b) in types if a <= w0], default=None)
        w1 = x if bmin is None else min(x, bmin - 1)
        if w1 >= 0: best = max(best, w0 + w1)
    return best

def taustar(T, n):
    e, x = n
    best = -1
    for w0 in range(e + 1):
        # closed-free: every g has (g0>0 and w0<=g0) or (g1>0 and w1<=g1)
        need = [g[1] for g in T if not (g[0] > 0 and w0 <= g[0])]
        if any(b == 0 for b in need): continue
        w1 = min([x] + need)
        best = max(best, w0 + w1)
    return e + x - best

def gen(rng):
    k = rng.randint(40, 120)
    mode = rng.random()
    if mode < 0.4:
        # 'complete' mode: N = e + x < 2e => all profiles with e <= a+b <= k are pairwise intersecting
        e = rng.randint((3 * k) // 4, k)
        x = rng.randint(max(1, e // 3), e - 1) if rng.random() < 0.3 else rng.randint(min(e - 1, (3 * k) // 4 - 3), e - 1)
        p = rng.choice([1.0, 0.5, 0.1, 0.02])
        S = [(a, b) for a in range(1, e + 1) for b in range(0, x + 1) if e <= a + b <= k and rng.random() < p]
        return k, e, x, S
    if mode < 0.7:
        # 'twoblock' mode aimed at Case 2 of the anchored theorem (beta(e/2) > 2x/3)
        e = rng.randint((3 * k) // 4, k)
        x = rng.randint(e // 2, 2 * k)
        b0 = rng.randint(x // 2 + 1, x)
        S1 = []
        for a in range(1, e // 2 + 1):
            b = max(b0 + rng.randint(0, 3) * rng.randint(0, 1), e - a)
            if b <= x and a + b <= k: S1.append((a, b))
        if rng.random() < 0.5 and S1: S1 = rng.sample(S1, max(1, len(S1) // rng.randint(1, 8)))
        S2 = []
        for a in range(e // 2 + 1, e + 1):
            for b in sorted({max(0, e - a), max(0, e - a) + rng.randint(0, x)}):
                if b <= x and e <= a + b <= k and all(a + a1 > e or b + b1 > x for (a1, b1) in S1):
                    S2.append((a, b))
        return k, e, x, S1 + S2
    e = rng.randint((3 * k) // 4 - 5, k)
    x = rng.randint(1, 2 * k)
    cand = [(a, b) for a in range(1, e + 1) for b in range(0, x + 1) if e <= a + b <= k]
    if mode < 0.8:
        cand.sort(key=lambda g: g[0] + g[1] + rng.uniform(0, rng.choice([1, 5, 20])))
        lim = 300
    else:
        rng.shuffle(cand); lim = rng.choice([2, 3, 5, 10, 40])
    S = []
    for (a, b) in cand:
        if len(S) >= lim: break
        if (2 * a > e or 2 * b > x) and all(a + a2 > e or b + b2 > x for (a2, b2) in S):
            S.append((a, b))
    return k, e, x, S

def lp_masses(loads, cap, anchored):
    """class masses c_p>=0 (7 points), sum=cap, window(l)=sum_{p notin l} c_p >= loads[l]; anchored: c_p=0 on L."""
    A_ub = []; b_ub = []
    for j, l in enumerate(LINES):
        A_ub.append([-1.0 if p not in l else 0.0 for p in range(7)]); b_ub.append(-loads[j])
    bounds = [(0, 0) if (anchored and p in LINES[0]) else (0, None) for p in range(7)]
    res = linprog(np.zeros(7), A_ub=A_ub, b_ub=b_ub, A_eq=[[1.0] * 7], b_eq=[cap], bounds=bounds, method='highs')
    return res.x if res.status == 0 else None

def criterion(loads, cap):
    if max(loads) > cap or sum(loads) > 4 * cap: return False
    for q in range(7):
        if sum(loads[j] for j, l in enumerate(LINES) if q in l) > 2 * cap: return False
    return True

def round_masses(c, cap):
    c = [0.0 if abs(v) < 1e-9 else v for v in c]
    c = [round(v) if abs(v - round(v)) < 1e-9 else v for v in c]
    fl = [int(np.floor(v)) for v in c]
    rem = cap - sum(fl)
    order = sorted(range(7), key=lambda p: -(c[p] - fl[p]))
    for p in order[:rem]:
        assert c[p] - fl[p] > 0
        fl[p] += 1
    assert sum(fl) == cap
    return fl

def covers(g, types):
    return next((t for t in types if t[0] <= g[0] and t[1] <= g[1]), None)

def check(k, e, x, S, st):
    n = (e, x); N = e + x
    info = {}
    types = S + [(e, 0)]
    assert all(a + a2 > e or b + b2 > x for (a, b) in types for (a2, b2) in types), 'not intersecting'
    assert all(e <= a + b <= k and a >= 1 and b <= x for (a, b) in types)
    alpha = alpha_of(types, n); tau = N - alpha
    st['inst'] += 1
    r = k + 6
    INF = 10**9
    beta = [min([b for (a2, b) in types if a2 <= a], default=INF) for a in range(e + 1)]
    A = []   # minimal elements of A^{<=r}: for each a the least b
    for a in range(e + 1):
        b0 = beta[max(0, a - 3)]
        if b0 >= INF: continue
        b = b0 + 3 if b0 > 0 else 0
        if b <= x and a + b <= r: A.append((a, b))
    T = A + [(e, 0)]
    ts = taustar(T, n)
    info['gap'] = ts - Fr(3 * r, 4)
    cs = [g for g in A if 2 * g[0] <= e]
    info['case2'] = bool(cs) and 3 * min(g[1] for g in cs) > 2 * x
    if ts < tau - 8:
        st['lowfail'] += 1; print('LOWFAIL', k, e, x, S, tau, ts)
    must = 4 * tau > 3 * k + 50
    if must: st['mustfire'] += 1
    if 4 * ts <= 3 * r:
        if must: st['mustfire_fail'] += 1; print('MUSTFIRE-FAIL', k, e, x, S, tau, ts)
        st['maxgap_nofire'] = max(st['maxgap_nofire'], float(tau - Fr(3 * k, 4)))
        return info
    st['big'] += 1
    # anchored template (proof of the anchored two-part theorem, with the tau* formula over T)
    half = Fr(e, 2)
    cands = [g for g in A if g[0] <= half]
    gstar = min(cands, key=lambda g: (g[1], g[0]))
    a1, b1 = gstar
    if 3 * b1 <= 2 * x:
        st['case1'] += 1
        rows = [(e, 0)] + [gstar] * 6
    else:
        st['case2'] += 1
        lower = [g for g in A if g[1] < b1]
        a2 = min(g[0] for g in lower)
        g2 = min([g for g in lower if g[0] == a2], key=lambda g: g[1])
        # pencil at off-L point 6: lines containing 6 except L
        rows = [(e, 0)] + [g2 if 6 in LINES[j] else gstar for j in range(1, 7)]
    ok = True
    for i, cap in enumerate(n):
        loads = [rw[i] for rw in rows]
        if not criterion(loads, cap):
            st['critfail'] += 1; ok = False; print('CRITFAIL', k, e, x, S, rows, i); break
    if not ok: st['tmplfail'] += 1; return info
    masses = []
    for i, cap in enumerate(n):
        c = lp_masses([rw[i] for rw in rows], cap, anchored=(i == 0))
        if c is None: st['tmplfail'] += 1; ok = False; print('LPFAIL', rows, i); break
        masses.append(round_masses(list(c), cap))
    if not ok: return info
    # integer windows
    chosen = []
    for j, l in enumerate(LINES):
        win = tuple(sum(masses[i][p] for p in range(7) if p not in l) for i in range(2))
        if j == 0:
            if win[0] != e: ok = False; st['roundfail'] += 1; print('ANCHORFAIL', rows); break
            chosen.append((e, 0)); continue
        if any(win[i] < rows[j][i] - 3 for i in range(2)):
            ok = False; st['roundfail'] += 1; print('ROUNDFAIL', rows, masses); break
        t = covers(win, types)
        if t is None: ok = False; st['roundfail'] += 1; print('NOEDGE', rows, win); break
        chosen.append(t)
    if not ok: return info
    # explicit vertices: part i, cell p -> masses[i][p] vertices labelled p
    verts = []  # (part, label)
    for i in range(2):
        for p in range(7):
            verts += [(i, p)] * masses[i][p]
    edges = []
    for j, l in enumerate(LINES):
        need = list(chosen[j]); G = set()
        for v, (i, p) in enumerate(verts):
            if p not in l and need[i] > 0: G.add(v); need[i] -= 1
        assert need == [0, 0]
        edges.append(G)
    # E0 = all part-0 vertices must be edges[0]
    assert edges[0] == {v for v, (i, p) in enumerate(verts) if i == 0}
    # brute force: no pair (v,w) meets all 7
    inc = [frozenset(j for j in range(7) if v in edges[j]) for v in range(len(verts))]
    sets = set(inc)
    bad = all(len(s | t) < 7 for s in sets for t in sets)
    if not bad: st['bffail'] += 1; print('BFFAIL', k, e, x, S); return info
    st['fired'] += 1
    return info

def run(seed, ninst):
    rng = random.Random(seed)
    st = dict(inst=0, lowfail=0, big=0, fired=0, tmplfail=0, critfail=0, roundfail=0, bffail=0,
              mustfire=0, mustfire_fail=0, case1=0, case2=0, maxgap_nofire=-99)
    for it in range(ninst):
        k, e, x, S = gen(rng)
        check(k, e, x, S, st)
    return st

def intersecting_with(t, S, e, x):
    return all(t[0] + a > e or t[1] + b > x for (a, b) in S + [t])

def climb(seed, restarts, steps):
    """hill-climb over intersecting S aiming at Case 2 (3 beta(e/2)+9 > 2x) with tau*(T) > 3r/4."""
    rng = random.Random(seed)
    st = dict(inst=0, lowfail=0, big=0, fired=0, tmplfail=0, critfail=0, roundfail=0, bffail=0,
              mustfire=0, mustfire_fail=0, case1=0, case2=0, maxgap_nofire=-99)
    for rs in range(restarts):
        k = rng.randint(40, 100); e = rng.randint((3 * k) // 4, k); x = rng.randint(e // 2, 2 * k)
        S = []
        def score(S):
            info = check(k, e, x, S, st)
            g = info.get('gap', -99)
            return float(g) + (0 if info.get('case2') else -8)
        cur = score(S)
        for _ in range(steps):
            S2 = list(S)
            if S2 and rng.random() < 0.3:
                S2.pop(rng.randrange(len(S2)))
            else:
                a = rng.randint(1, e); lo = max(0, e - a); hi = min(x, k - a)
                if lo > hi: continue
                b = rng.choice([lo, hi, rng.randint(lo, hi)])
                t = (a, b)
                if t in S2 or not intersecting_with(t, S2, e, x) or not (2 * a > e or 2 * b > x): continue
                S2.append(t)
            sc = score(S2)
            if sc >= cur or rng.random() < 0.02: S, cur = S2, sc
    return st

def explicit(seed, ninst):
    """Case-2 shaped families: types ~ k*(a*,1-a*), k*(a2,1-a2), k*(a3,1-a3) (rank k), e ~ .93k, x ~ 1.2k
    (continuous tau* ~ .76-.77 > 3/4; hand-designed from the proof of the anchored theorem)."""
    rng = random.Random(seed)
    st = dict(inst=0, lowfail=0, big=0, fired=0, tmplfail=0, critfail=0, roundfail=0, bffail=0,
              mustfire=0, mustfire_fail=0, case1=0, case2=0, maxgap_nofire=-99)
    for it in range(ninst):
        k = rng.randint(500, 1500)
        e = int(k * rng.uniform(0.92, 0.95)); x = int(k * rng.uniform(1.15, 1.25))
        a1 = int(k * rng.uniform(0.10, 0.15)); a2 = e // 2 + rng.randint(1, max(1, k // 30)); a3 = int(k * rng.uniform(0.82, 0.88))
        S = [(a, k - a) for a in (a1, a2, a3) if k - a <= x and a <= e]
        types = S + [(e, 0)]
        if not all(a + a_ > e or b + b_ > x for (a, b) in types for (a_, b_) in types): continue
        check(k, e, x, S, st)
    return st

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    if len(sys.argv) > 3 and sys.argv[3] == 'explicit':
        print(seed, 'explicit', explicit(seed, n))
    elif len(sys.argv) > 3 and sys.argv[3] == 'climb':
        print(seed, 'climb', climb(seed, n, int(sys.argv[4])))
    else:
        print(seed, run(seed, n))
