"""Adversarial climb against the menu {P1 (pencil + 1 actual quad line, triangle of light lines), pairs (42 fns)}
in the balanced 3-super-class regime.  Minimise max(P1 margin, pair margin) s.t. tau* >= TGT, all types super-heavy
somewhere, all 3 classes nonempty, e_i+e_j <= 3/4.  usage: climb_p1.py seed iters ntypes start(0 rand,1 h3s,2 779)"""
import sys, random, numpy as np, time
sys.path.insert(0, '.'); sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3')
from frlib import *
import b3lib
seed, iters, n, start = map(int, sys.argv[1:5]); TGT = 0.7505; rng = random.Random(seed)
def ok_regime(x, T):
    r = b3lib.regime(x, T)
    if r is None: return False
    e = r[2]
    return all(e[i] + e[j] <= 0.75 for i in range(3) for j in range(i+1, 3))
def score(x, T):
    ts = b3lib.tau_star(x, T)
    if ts < TGT: return None
    pm = b3lib.pair_margin(x, T)
    p1 = p1_best(x, T, ts)[0]
    return max(pm, p1), pm, p1, ts
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def valid(x, T): return all(0.005 < v <= 1.5 for v in x) and all(a is not None and all(a[i] <= x[i] + 1e-12 for i in range(3)) for a in T)
while True:
    if start == 1:
        x = [0.861, 1.44, 0.741]; T = [[.664, 0, .336], [.019, .981, 0], [.424, 0, .576]]
        T += [proj([v + rng.gauss(0, .03) for v in T[k % 3]]) for k in range(n - 3)]
    elif start == 2:
        V=[(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
        x=[513/640]*3; T=[[v/80 for v in a] for a in V]; T = [T[i] for i in sorted(rng.sample(range(9), n))] if n < 9 else T
    else:
        x = [rng.uniform(0.6, 1.5) for _ in range(3)]
        T = [proj([rng.random()**rng.choice([1,2,4,8]) for _ in range(3)]) for _ in range(n)]
    if valid(x, T) and ok_regime(x, T) and score(x, T) is not None: break
    if start == 2 and n < 9: continue
cur = score(x, T); step = 0.02; t0 = time.time()
print("start", [round(v, 4) for v in cur], flush=True)
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    if rng.random() < 0.25:
        i = rng.randrange(3); nx[i] += rng.gauss(0, step)
    else:
        j = rng.randrange(n); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    if not valid(nx, nT) or not ok_regime(nx, nT): continue
    f = score(nx, nT)
    if f is None or f[0] > cur[0]: continue
    x, T, cur = nx, nT, f
    if it % 300 == 299:
        step *= 0.8
        print(it, [round(v, 4) for v in cur], 'x', [round(v, 4) for v in x], '%.0fs' % (time.time() - t0), flush=True)
    if cur[0] < -1e-9: break
print("END", [round(v, 5) for v in cur], 'fano %.4f' % b3lib.fano_margin(x, T)[0], 'x', x, 'T', T, flush=True)
