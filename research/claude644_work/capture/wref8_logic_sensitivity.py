#!/usr/bin/env python3
"""Referee: non-vacuity of wref8_logic_random -- below tau*=3/4 the same template must sometimes fail;
and adversarial points near product vertices of D (unmerged, with L split into 1-3 parts)."""
import random
from wref8_logic_random import template_lp
rng = random.Random(5)
fails = tot = 0
while tot < 400:
    p = rng.randint(3, 5); x = [rng.uniform(0.02, 1.6) for _ in range(p)]
    I = list(range(p)); th = [rng.uniform(4*xi/7, min(xi,1)) for xi in x]
    X = sum(x)
    if X < 1: continue
    th = [max(t, 1-X+xi) for t, xi in zip(th, x)]
    if sum(th) < 1: continue
    tau = sum(xi-t for xi, t in zip(x, th))
    if not (0.6 <= tau < 0.74): continue
    tot += 1; fails += not template_lp(x, th, rng.sample(I, 3))
print('tau* in [0.6,0.74): template infeasible in', fails, 'of', tot)
# adversarial: perturb product vertices of D inward, split L into pieces (non-box parts)
TRI = [(0,0),(1,1),(1.75,1)]
bad = tot = 0
for _ in range(4000):
    pts = [rng.choice(TRI) for _ in range(3)]; xL = rng.choice([0, 1.75])
    # move slightly toward random interior point of the triangle, keeping 4x/7<th<=min(x,1)
    par = []
    for (x0, t0) in pts:
        lam = rng.uniform(0, 0.15); a, b = rng.random(), rng.random()
        if a + b > 1: a, b = 1-a, 1-b
        xi = (1-a-b)*x0 + a*1 + b*1.75; ti = (1-a-b)*t0 + a*1 + b*1
        par.append(((1-lam)*x0+lam*xi, (1-lam)*t0+lam*ti))
    xL = min(1.75, max(0, xL + rng.uniform(-0.2, 0.2)))
    if any(t <= 4*x/7 + 1e-9 for x, t in par): continue
    d = sum(x - t for x, t in par) + 3*xL/7
    if sum(t for _, t in par) + xL < 1 or d < 0.75: continue
    k = rng.randint(1, 3); cuts = sorted(rng.random() for _ in range(k-1)); ws = [b-a for a, b in zip([0]+cuts, cuts+[1])]
    # L pieces: as non-box parts (theta None) -- tau* of L then 0, so the real family has tau* = sum d < 3/4
    # unless xL counted as boxes; we test template feasibility over the D-parameters regardless (as the proof does)
    x = [p[0] for p in par] + [w*xL for w in ws]; th = [p[1] for p in par] + [None]*k
    tot += 1
    if not template_lp(x, th, [0,1,2]):
        bad += 1; print('FAIL', [round(v,4) for v in x], [None if t is None else round(t,4) for t in th])
print('near-vertex D points (unmerged L):', tot, 'infeasible', bad)
