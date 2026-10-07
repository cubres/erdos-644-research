"""Adversarial climb, |H|=2 + light parts: maximise tau* over type sets (sum 1) with parts 0,1 heavy, parts>=2
light for all types, and NO Fano tuple and NO two-type bad tuple (42-function catalogue).  tau*>3/4 found =>
counterexample to 'Fano-or-pair' (FP) in the |H|=2 regime (then run full catalogue)."""
import random, sys, heavylib as h, pairlib as P
nl, m, R, seed = map(int, sys.argv[1:5]); rng = random.Random(seed); p = 2 + nl
START = [([1.2,1.2,0.33],[[.82,0,.18],[0,.82,.18],[.89,.11,0],[.11,.89,0]])]
def valid(x, T):
    if any(v < 0.02 for v in x): return False
    for a in T:
        if abs(sum(a) - 1) > 1e-9 or any(a[i] < -1e-12 or a[i] > x[i] + 1e-12 for i in range(p)): return False
        if any(7*a[i] > 4*x[i] for i in range(2, p)): return False
        if not (7*a[0] > 4*x[0] or 7*a[1] > 4*x[1]): return False
    return any(7*a[0] > 4*x[0] for a in T) and any(7*a[1] > 4*x[1] for a in T)
def bad(x, T):
    return P.any_pair(x, T) is not None or h.any_fano_np(x, T)
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a]
def rstart():
    for _ in range(100000):
        x = [rng.uniform(0.8, 1.5), rng.uniform(0.8, 1.5)] + [rng.uniform(0.05, 0.8) for _ in range(nl)]
        T = []
        for j in range(m):
            w = [rng.random()**rng.choice([1,2,4]) for _ in range(p)]; T.append(proj(w))
        if valid(x, T) and not bad(x, T): return x, T
    return None
best = (-1,)
for r in range(R):
    if r == 0 and nl == 1 and m >= 4:
        x, T = START[0]; T = T + [proj([rng.random() for _ in range(p)]) for _ in range(m-4)]
        x = [v - 0.0 for v in x]; x[2] = 0.325
        if not valid(x, T) or bad(x, T):
            st = rstart()
            if st is None: continue
            x, T = st
    else:
        st = rstart()
        if st is None: print("no start"); continue
        x, T = st
    cur = h.tau_star_fast(x, T); step = 0.05
    for it in range(3000):
        nx = list(x); nT = [list(a) for a in T]
        mv = rng.random()
        if mv < 0.3:
            i = rng.randrange(p); nx[i] = max(0.02, nx[i] + rng.gauss(0, step))
        elif mv < 0.85:
            j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
        else:
            nx = [max(0.02, v + rng.gauss(0, step/2)) for v in x]
            nT = [proj([v + rng.gauss(0, step/3) for v in a]) for a in T]
        if not valid(nx, nT): continue
        t = h.tau_star_fast(nx, nT)
        if t < cur - 1e-12: continue
        if bad(nx, nT): continue
        x, T, cur = nx, nT, t
        if it % 500 == 499: step *= 0.6
    print(f"restart {r}: FP-free tau* {cur:.4f} x={[round(v,4) for v in x]} T={[[round(v,4) for v in a] for a in T]}", flush=True)
    if cur > best[0]: best = (cur, x, T)
print("BEST", best, flush=True)
