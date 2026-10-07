#!/usr/bin/env python3
"""wref8 adversarial DISCOVERY search (floats; any hit must be re-checked exactly with wref8_template).
Instance: p parts, all parts boxes or a random subset I (|I|>=3), effective thresholds, tau*>=3/4,
non-homogeneous (theta_i > 4x_i/7 on I). Objective: the WORST ordered triple's template margin
  lam* = max lam s.t. template feasible with all per-part capacities (x_i) replaced by (1-lam) x_i
(box thresholds unchanged). Theorem 8.4 predicts lam* >= 0 everywhere. Hill-climb to minimise lam*."""
import itertools, random, sys
import numpy as np
from scipy.optimize import linprog
LINES = [(0, 1, 3), (1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 0), (5, 6, 1), (6, 0, 2)]
PEN = [l for l in range(7) if 0 in LINES[l]]; QUAD = [l for l in range(7) if 0 not in LINES[l]]

def margin(x, th, box):
    p = len(x); nv = 7 * p + 1; L = 7 * p
    A, b, Aeq, beq = [], [], [], []
    for l in range(7):
        r = np.zeros(nv); r[l * p:(l + 1) * p] = 1; Aeq.append(r); beq.append(1)
        for i in range(p):
            r = np.zeros(nv); r[l * p + i] = 1; r[L] = x[i]; A.append(r); b.append(x[i])
    for i in range(p):
        for q in range(7):
            r = np.zeros(nv)
            for l in range(7):
                if q in LINES[l]: r[l * p + i] = 1
            r[L] = 2 * x[i]; A.append(r); b.append(2 * x[i])
        r = np.zeros(nv)
        for l in range(7): r[l * p + i] = 1
        r[L] = 4 * x[i]; A.append(r); b.append(4 * x[i])
    bounds = []
    for l in range(7):
        for i in range(p): bounds.append((th[i] if box[l] == i else 0, None))
    bounds.append((-5, 1))
    c = np.zeros(nv); c[L] = -1
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=bounds, method='highs')
    return res.x[L] if res.status == 0 else -5

def tmpl(A, B, C):
    box = [None] * 7
    for l in QUAD: box[l] = A
    box[PEN[0]] = B; box[PEN[1]] = B; box[PEN[2]] = C
    return box

def valid(x, th, I):
    p = len(x); X = sum(x)
    if min(x) <= 0: return None
    te = [max(th[i], 1 - X + x[i]) if i in I else 0 for i in range(p)]
    for i in I:
        if not (4 * x[i] / 7 < te[i] <= min(x[i], 1)): return None
    s = sum(te[i] for i in I) + sum(x[j] for j in range(p) if j not in I)
    if s < 1: return None
    ts = sum(x[i] - te[i] for i in I)
    if ts < 0.75: return None
    return te

def worst(x, te, I):
    return min(margin(x, te, tmpl(*t)) for t in itertools.permutations(I, 3))

rng = random.Random(int(sys.argv[1])); runs = int(sys.argv[2]); steps = int(sys.argv[3])
glob = (9, None)
for run in range(runs):
    p = rng.randint(3, 5)
    I = list(range(p)) if rng.random() < 0.6 else sorted(rng.sample(range(p), rng.randint(3, p)))
    while True:
        x = [rng.uniform(0.01, 1.75) for _ in range(p)]
        th = [rng.uniform(4 * xi / 7, min(xi, 1)) if i in I else 0 for i, xi in enumerate(x)]
        te = valid(x, th, I)
        if te: break
    cur = worst(x, te, I)
    for s in range(steps):
        x2 = [max(1e-4, v + rng.gauss(0, 0.05)) for v in x]
        th2 = [v + rng.gauss(0, 0.05) if i in I else 0 for i, v in enumerate(th)]
        te2 = valid(x2, th2, I)
        if not te2: continue
        m = worst(x2, te2, I)
        if m <= cur: x, th, te, cur = x2, th2, te2, m
    tau = sum(x[i] - te[i] for i in I)
    print(f'run {run}: p={p} I={I} min worst-triple margin {cur:.6f} tau*={tau:.5f} x={[round(v,4) for v in x]} th={[round(v,4) for v in te]}', flush=True)
    if cur < glob[0]: glob = (cur, (x, te, I))
print('GLOBAL MIN MARGIN', glob[0], glob[1])
