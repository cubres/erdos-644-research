"""Maximise tau* over one-type-per-class super-heavy 3-part families with a CYCLIC (not mutual) conflict."""
import random, sys, heavylib as h, pairlib as P
rng = random.Random(int(sys.argv[1])); iters = int(sys.argv[2]); MODE = sys.argv[3] if len(sys.argv) > 3 else 'cyc'
def forb(x, a, b): return any(2*a[i] + b[i] > 2*x[i] + 1e-12 for i in range(3))
def ok(x, T):
    if any(a is None for a in T) or any(v < 0.01 for v in x): return False
    if any(a[i] > x[i] + 1e-12 for a in T for i in range(3)): return False
    if [[i for i in range(3) if 3*a[i] > 2*x[i]] for a in T] != [[0],[1],[2]]: return False
    A, B, C = T
    mutual = (forb(x,A,B) and forb(x,B,A)) or (forb(x,A,C) and forb(x,C,A)) or (forb(x,B,C) and forb(x,C,B))
    cyc = (forb(x,A,B) and forb(x,B,C) and forb(x,C,A)) or (forb(x,A,C) and forb(x,B,A) and forb(x,C,B))
    return (cyc and not mutual) if MODE == 'cyc' else (mutual and P.pair_margin(x, T) < 0)
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
best = -1
for r in range(5):
    while True:
        x = [rng.uniform(0.6, 1.5) for _ in range(3)]
        T = []
        for j in range(3):
            a = [0.0]*3; a[j] = rng.uniform(2*x[j]/3, min(1, x[j])); u = rng.random(); o = [i for i in range(3) if i != j]
            a[o[0]] = (1-a[j])*u; a[o[1]] = (1-a[j])*(1-u); T.append(a)
        if ok(x, T): break
    cur = h.tau_star(x, T); step = 0.03
    for it in range(iters):
        nx = list(x); nT = [list(a) for a in T]
        if rng.random() < 0.3:
            i = rng.randrange(3); nx[i] += rng.gauss(0, step)
        else:
            j = rng.randrange(3); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
        if not ok(nx, nT): continue
        t = h.tau_star(nx, nT)
        if t < cur: continue
        x, T, cur = nx, nT, t
        if it % 5000 == 4999: step *= 0.7
    print("%s restart %d: tau* %.4f fano %s pair margin %.4f x %s T %s" % (MODE, r, cur, h.any_fano_np(x, T), P.pair_margin(x, T), [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
    best = max(best, cur)
print("BEST", MODE, best)
