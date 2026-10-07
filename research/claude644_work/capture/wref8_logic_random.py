#!/usr/bin/env python3
"""Referee (Thm 8.4) end-to-end numerical test on UNMERGED families: p parts, boxes I (|I|>=3) plus
non-box parts; thresholds in the non-homogeneous regime 4x/7 < th <= min(x,1); tau* by formula;
also an independent LP check of the 'contains an admissible type' characterisation.
Template T(A,B,C) with roles a random ordered triple of I (the proof claims ANY triple works);
feasibility = Lemma 7.63 criterion in every actual part (no merging), rows sum to 1, box trace >= th."""
import random, sys, itertools
import numpy as np
from scipy.optimize import linprog
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
ROLE = [0,0,1,0,1,2,0]          # line index -> role (0=A quad, 1=B pencil, 2=C pencil), missing point 6

def template_lp(x, th, roles):
    p = len(x); nv = 7*p; vi = lambda l, i: l*p + i
    Aub, bub, Aeq, beq = [], [], [], []
    for i in range(p):
        for q in range(7):
            r = np.zeros(nv)
            for l in range(7):
                if q in LINES[l]: r[vi(l,i)] = 1
            Aub.append(r); bub.append(2*x[i])
        r = np.zeros(nv)
        for l in range(7): r[vi(l,i)] = 1
        Aub.append(r); bub.append(4*x[i])
    for l in range(7):
        r = np.zeros(nv)
        for i in range(p): r[vi(l,i)] = 1
        Aeq.append(r); beq.append(1)
    bounds = []
    for l in range(7):
        for i in range(p):
            lo = th[i] if i == roles[ROLE[l]] else 0
            bounds.append((lo, x[i]))
    res = linprog(np.zeros(nv), A_ub=np.array(Aub), b_ub=np.array(bub), A_eq=np.array(Aeq), b_eq=np.array(beq),
                  bounds=bounds, method='highs')
    return res.status == 0

def contains_admissible_lp(u, x, th, I):
    p = len(u)
    for i in I:
        if th[i] > u[i] + 1e-12: continue
        bounds = [(0, u[j]) for j in range(p)]; bounds[i] = (th[i], u[i])
        res = linprog(np.zeros(p), A_eq=np.ones((1,p)), b_eq=[1], bounds=bounds, method='highs')
        if res.status == 0: return True
    return False

def sample(rng, p, mode):
    while True:
        x = [rng.uniform(0.02, 1.6) for _ in range(p)]
        k = rng.randint(3, p); I = sorted(rng.sample(range(p), k))
        th = [None]*p
        for i in I: th[i] = rng.uniform(4*x[i]/7, min(x[i], 1.0))
        if any(th[i] <= 4*x[i]/7 for i in I): continue
        X = sum(x)
        if X < 1: continue
        for i in I: th[i] = max(th[i], 1 - X + x[i])          # effective threshold
        S = sum(th[i] for i in I) + sum(x[j] for j in range(p) if j not in I)
        tau = (X - 1) if S < 1 else sum(x[i] - th[i] for i in I)
        if S < 1: continue            # complete case handled by homogeneous Fano (X>=7/4)
        if mode == 'near' and not (0.75 <= tau < 0.752): continue
        if mode == 'above' and not (0.75 <= tau < 0.9): continue
        return x, th, I, tau

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    # (a) characterisation of free residuals
    mism = 0
    for _ in range(300):
        p = rng.randint(3, 5); x, th, I, tau = sample(rng, p, 'any')
        u = [rng.uniform(0, xi) for xi in x]
        f = sum(u) >= 1 and any(u[i] >= th[i] for i in I)
        if f != contains_admissible_lp(u, x, th, I): mism += 1
    print('free-residual characterisation mismatches:', mism, '/ 300')
    for mode in ('above', 'near'):
        fails = 0; tot = 0; xL_big = 0
        for s in range(N):
            p = rng.randint(3, 6); x, th, I, tau = sample(rng, p, mode)
            roles = rng.sample(I, 3)
            xL = sum(x) - sum(x[r] for r in roles)
            xL_big += xL >= 7/4
            tot += 1
            if not template_lp(x, th, roles):
                fails += 1
                print('FAIL', mode, [round(v,4) for v in x], [None if t is None else round(t,4) for t in th],
                      'roles', roles, 'tau', round(tau,5), flush=True)
        print(f'mode {mode}: {tot} families, template infeasible {fails}, (xL>=7/4 in {xL_big})')
