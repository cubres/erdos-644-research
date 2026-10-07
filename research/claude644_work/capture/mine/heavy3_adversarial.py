"""ADVERSARIAL test of the |H|>=3 minimiser-template claim: hill-climb rigid type sets (p parts, m types) to
MAXIMISE tau* subject to: no homogeneous type (every type heavy somewhere), |H| >= 3, and the minimiser template
T(A,B,C) FAILS for every ordered triple of heavy parts.  If sup < 3/4 the claim survives."""
import random, sys, itertools
from upbox_fano import tau_star, fano
p, m, R, seed = map(int, sys.argv[1:5]); rng = random.Random(seed)
def heavy_ok(x, T):
    if any(all(a[i] <= 4*x[i]/7 for i in range(p)) for a in T): return None
    mins = {}
    for i in range(p):
        hv = [a for a in T if a[i] > 4*x[i]/7]
        if hv: mins[i] = min(hv, key=lambda a: a[i])
    return mins if len(mins) >= 3 else None
def template_works(x, mins):
    return any(fano(x, [mins[A], mins[B], mins[C]], (0,0,1,0,1,2,0)) for A, B, C in itertools.permutations(sorted(mins), 3))
def valid(x, T):
    return all(v > 0.02 for v in x) and all(abs(sum(a)-1) < 1e-9 and all(0 <= a[i] <= x[i] for i in range(p)) for a in T)
def rtype(x):
    for _ in range(1000):
        w = [rng.random()**rng.choice([1,2,4]) for _ in range(p)]; s = sum(w); a = [v/s for v in w]
        if all(a[i] <= x[i] for i in range(p)): return a
    return None
best = (-1,)
for r in range(R):
    for _ in range(20000):
        x = [rng.uniform(0.3, 1.4) for _ in range(p)]
        T = [rtype(x) for _ in range(m)]
        if None in T: continue
        mins = heavy_ok(x, T)
        if mins and not template_works(x, mins): break
    else:
        print("restart", r, "no failing start"); continue
    cur = tau_star(x, T); step = 0.05
    for it in range(300):
        nx = [max(0.02, v + rng.gauss(0, step)) for v in x]
        nT = []
        for a in T:
            b = [max(0.0, v + rng.gauss(0, step)) for v in a]; s = sum(b); nT.append([v/s for v in b])
        if not valid(nx, nT): continue
        mins = heavy_ok(nx, nT)
        if not mins or template_works(nx, mins): continue
        t = tau_star(nx, nT)
        if t > cur: x, T, cur = nx, nT, t
        if it % 100 == 99: step *= 0.6
    print(f"restart {r}: template-failing tau* {cur:.4f}", flush=True)
    if cur > best[0]: best = (cur, x, T)
print("BEST", round(best[0], 4), [round(v, 3) for v in best[1]], [[round(v, 3) for v in a] for a in best[2]])
