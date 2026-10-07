"""Intersecting RR: parts A,B heavy (every type SUPER-heavy at exactly one of them), light parts; every pair of
types (and each type with itself) overlaps in some part.  MAXIMISE tau*.  If sup <= 3/4 then 'A_tc for |H|=2'
holds (PCL gives Q_alpha/Q_beta outside RR; RR is Fano-free and V needs a disjoint pair)."""
import random, sys, heavylib as h, pairlib as P
seed, iters, nl, m = map(int, sys.argv[1:5]); rng = random.Random(seed); p = 2 + nl; GMIN = 0.76
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def valid(x, T):
    if any(v < 0.005 for v in x): return False
    for a in T:
        if a is None or any(a[i] > x[i] + 1e-12 for i in range(p)): return False
        if any(7*a[i] > 4*x[i] for i in range(2, p)): return False
        sA, sB = 3*a[0] > 2*x[0], 3*a[1] > 2*x[1]
        if sA == sB: return False
        if (not sA and 7*a[0] > 4*x[0]) or (not sB and 7*a[1] > 4*x[1]): return False
    if not all(any(a[i] + b[i] > x[i] + 1e-9 for i in range(p)) for j, a in enumerate(T) for b in T[j:]): return False
    dA = x[0] - min(a[0] for a in T if 3*a[0] > 2*x[0]); dB = x[1] - min(a[1] for a in T if 3*a[1] > 2*x[1])
    return dA + dB >= GMIN
best = -1
for r in range(int(sys.argv[5]) if len(sys.argv) > 5 else 5):
    for _ in range(200000):
        x = [rng.uniform(0.8, 1.5), rng.uniform(0.8, 1.5)] + [rng.uniform(0.05, 1.0) for _ in range(nl)]
        T = []
        for k in range(m):
            j = k % 2; a = [0.0]*p; a[j] = rng.uniform(2*x[j]/3, min(1, x[j]))
            w = [rng.random()**2 if i != j else 0 for i in range(p)]; S = sum(w)
            for i in range(p):
                if i != j: a[i] = (1-a[j])*w[i]/S
            T.append(a)
        if valid(x, T): break
    else:
        continue
    cur = h.tau_star_fast(x, T); step = 0.03
    for it in range(iters):
        nx = list(x); nT = [list(a) for a in T]
        if rng.random() < 0.3:
            i = rng.randrange(p); nx[i] += rng.gauss(0, step)
        else:
            j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
        if not valid(nx, nT): continue
        t = h.tau_star_fast(nx, nT)
        if t < cur: continue
        x, T, cur = nx, nT, t
        if it % 10000 == 9999: step *= 0.7
    print("restart %d tau* %.4f pm %.4f x %s T %s" % (r, cur, P.pair_margin(x, T), [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
    best = max(best, cur)
print("BEST", best)
