"""Equal capacities x in (3/4, 4/5) (the window not covered by the typeclosed agent's SAT certificates),
cyclically symmetric type sets (k orbit representatives, 3k types).  Maximise tau* subject to NO Fano tuple and
NO two-type bad tuple (FP-free).  tau* > 3/4 => candidate counterexample to FP (then full catalogue)."""
import random, sys, heavylib as h, pairlib as P
seed, iters, k = map(int, sys.argv[1:4]); rng = random.Random(seed)
XLO, XHI = 0.75, 0.80
def orbit(r): return [r, [r[2], r[0], r[1]], [r[1], r[2], r[0]]]
def fam(R): return [t for r in R for t in orbit(r)]
def proj(a, x):
    a = [max(0.0, v) for v in a]; s = sum(a)
    if s <= 0: return None
    a = [v/s for v in a]
    return a if max(a) <= x + 1e-12 else None
def ok(x, R):
    if not (XLO < x < XHI) or any(r is None for r in R): return False
    T = fam(R); X = [x]*3
    return not h.any_fano_np(X, T) and P.pair_margin(X, T) < -1e-9
best = (-1,)
for rs in range(int(sys.argv[4]) if len(sys.argv) > 4 else 6):
    for _ in range(100000):
        x = rng.uniform(XLO, XHI)
        R = [proj([rng.random()**rng.choice([1,2,4]) for _ in range(3)], x) for _ in range(k)]
        if ok(x, R): break
    else:
        continue
    cur = h.tau_star_fast([x]*3, fam(R)); step = 0.03
    for it in range(iters):
        nx = x + (rng.gauss(0, step/3) if rng.random() < 0.2 else 0)
        nR = [list(r) for r in R]
        j = rng.randrange(k); nR[j] = proj([v + rng.gauss(0, step) for v in nR[j]], nx)
        if not ok(nx, nR): continue
        t = h.tau_star_fast([nx]*3, fam(nR))
        if t < cur: continue
        x, R, cur = nx, nR, t
        if it % 5000 == 4999: step *= 0.7
    print("restart %d: FP-free tau* %.4f x %.4f reps %s" % (rs, cur, x, [[round(v,4) for v in r] for r in R]), flush=True)
    if cur > best[0]: best = (cur, x, R)
print("BEST", best, flush=True)
