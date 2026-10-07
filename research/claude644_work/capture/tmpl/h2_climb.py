# |H|=2 rigid type sets over p parts (parts 0,1 heavy, others light): maximise tau* s.t. no pair template (+H).
import random, sys
from h2_lib import *
MODE = sys.argv[5] if len(sys.argv) > 5 else 'pair'
def argmin_ok(x, T):
    C1 = [u for u in T if 7 * u[0] > 4 * x[0]]; C2 = [u for u in T if 7 * u[1] > 4 * x[1]]
    a = min(C1, key=lambda u: u[0]); b = min(C2, key=lambda u: u[1])
    return any(feas(x, aa, bb, fs) for fs, aa, bb in [(TWO['Qt'], a, b), (TWO['Qt'], b, a), (TWO['V'], a, b), (TWO['V'], b, a)])
def overlap_case(x, T):
    C1 = [u for u in T if 7 * u[0] > 4 * x[0]]; C2 = [u for u in T if 7 * u[1] > 4 * x[1]]
    a = min(C1, key=lambda u: u[0]); b = min(C2, key=lambda u: u[1])
    if feas(x, a, b, TWO['Qt']) or feas(x, b, a, TWO['Qt']): return False
    return any(a[i] + b[i] > x[i] for i in range(2, len(x)))
def nocompat(x, T):
    C1 = [u for u in T if 7 * u[0] > 4 * x[0]]; C2 = [u for u in T if 7 * u[1] > 4 * x[1]]
    if min(u[0] for u in C1) <= 2 * x[0] / 3 or min(u[1] for u in C2) <= 2 * x[1] / 3: return False
    for a in C1:
        for b in C2:
            if (x[0] - a[0]) + (x[1] - b[1]) >= 0.75 and all(a[i] + b[i] <= x[i] for i in range(2, len(x))): return False
    return True
def blockedf(x, T):
    if MODE == 'nocompat': return nocompat(x, T)
    if MODE == 'overlap': return overlap_case(x, T)
    return (not argmin_ok(x, T)) if MODE == 'argmin' else (pair_menu(x, T) is None)
p, nt = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(int(sys.argv[3])); iters = int(sys.argv[4])
def valid(x, T):
    if sum(x) < 1.75: return False
    for t in T:
        if abs(sum(t) - 1) > 1e-9 or any(t[i] < 0 or t[i] > x[i] for i in range(p)): return False
        h0 = 7 * t[0] > 4 * x[0]; h1 = 7 * t[1] > 4 * x[1]
        if not (h0 or h1): return False
        if any(7 * t[i] > 4 * x[i] for i in range(2, p)): return False
    if not any(7 * t[0] > 4 * x[0] for t in T) or not any(7 * t[1] > 4 * x[1] for t in T): return False
    return True
def rand_type(x):
    for _ in range(100):
        h = rng.randrange(2)
        t = [0.0] * p
        t[h] = rng.uniform(4 * x[h] / 7, min(1, x[h]))
        rest = 1 - t[h]
        w = [rng.random() * (rng.random() < .7) for _ in range(p)]; w[h] = 0
        if sum(w) == 0: w[1 - h] = 1
        s = sum(w); t2 = [t[i] + rest * w[i] / s for i in range(p)]
        if all(t2[i] <= x[i] for i in range(p)): return t2
    return None
def normalize(t, x):
    s = sum(t); return [v / s for v in t]
best = None; cur = None
for it in range(iters):
    if best is None or rng.random() < 0.01:
        x = [rng.uniform(0.3, 1.6) for _ in range(p)]
        T = [rand_type(x) for _ in range(nt)]
        if None in T or not valid(x, T) or not blockedf(x, T): continue
        c = (tau_rigid2(x, T), x, T)
        if best is None or c[0] > best[0]: best = c
        cur = c; continue
    t0, x0, T0 = best if rng.random() < 0.6 else cur
    s = rng.choice([0.1, 0.03, 0.01, 0.003, 0.001])
    x = [max(0.01, v + rng.gauss(0, s) * (rng.random() < .7)) for v in x0]
    T = [normalize([max(0, v + rng.gauss(0, s) * (rng.random() < 0.4)) for v in t], x) for t in T0]
    if not valid(x, T): continue
    tt = tau_rigid2(x, T)
    if tt < t0 - 1e-12: continue
    if not blockedf(x, T): continue
    cur = (tt, x, T)
    if tt > best[0]:
        best = cur
        print(it, round(tt, 5), [round(v, 4) for v in x], [[round(v, 4) for v in t] for t in T], flush=True)
print('FINAL', best[0], best[1], best[2])
