"""Adversarial climb in the BALANCED 3-super-class regime: rigid finite type sets over 3 parts, every type
super-heavy (>2x/3) somewhere, all three classes nonempty, e_i+e_j<=3/4 (pairs), tau*>=TGT.
Objective (minimised): menu margin = max(V margin, T margin) [mode 'vt'] or full FP margin
max(Fano margin over all assignments, 42-fn pair margin) [mode 'fp'].
usage: climb_bal.py seed iters m mode"""
import random, sys, json, numpy as np, b3lib as B
seed, iters, m, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
TGT = 0.7505; rng = random.Random(seed)
def obj(x, T):
    if mode == 'vt': return max(B.v_margin(x, T)[0], B.t_margin(x, T)[0])
    return max(B.fano_margin(x, T)[0], B.pair_margin(x, T))
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def valid(x, T):
    if not all(v > 0.005 for v in x): return False
    if not all(a is not None and all(a[i] <= x[i] + 1e-12 for i in range(3)) for a in T): return False
    r = B.regime(x, T)
    if r is None: return False
    S, sig, e = r
    return all(e[i]+e[j] <= 0.75 for i in range(3) for j in range(i+1, 3))
def rand_start():
    while True:
        x = [rng.uniform(0.5, 1.5) for _ in range(3)]
        T = []
        for j in range(m):
            i = j % 3; a = [0, 0, 0]; a[i] = rng.uniform(2*x[i]/3, min(1, x[i]))
            r = 1 - a[i]; o = [k for k in range(3) if k != i]; w = rng.random()
            a[o[0]] = r*w; a[o[1]] = r*(1-w)
            T.append(a)
        if valid(x, T) and B.tau_star(x, T) >= TGT: return x, T
x, T = rand_start(); cur = obj(x, T); step = 0.03
print("start", round(cur, 4), flush=True)
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    if rng.random() < 0.25:
        i = rng.randrange(3); nx[i] += rng.gauss(0, step)
    else:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    if not valid(nx, nT): continue
    f = obj(nx, nT)
    if f > cur or B.tau_star(nx, nT) < TGT: continue
    x, T, cur = nx, nT, f
    if it % 3000 == 2999: step *= 0.7
    if cur < -1e-9: break
r = B.regime(x, T)
print("END %s obj %.5f tau* %.5f e %s" % (mode, cur, B.tau_star(x, T), [round(v, 4) for v in r[2]]), flush=True)
print(json.dumps({'x': x, 'T': T, 'obj': cur, 'mode': mode}), flush=True)
