"""Three-type FP: C={a,b,c} on p parts (sum 1), minimise BAD=max(pair margin, Fano margin) s.t. tau*>=TGT."""
import random, sys, heavylib as h, pairlib as P
seed, iters, p = map(int, sys.argv[1:4]); TGT = 0.7505; rng = random.Random(seed); m = 3
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def valid(x, T): return all(v > 0.005 for v in x) and all(a is not None and all(a[i] <= x[i] + 1e-12 for i in range(p)) for a in T)
def bad(x, T): return max(P.pair_margin(x, T), h.fano_margin(x, T)[0])
while True:
    x = [rng.uniform(0.2, 1.5) for _ in range(p)]
    T = [proj([rng.random()**rng.choice([1,2,4,8]) for _ in range(p)]) for _ in range(m)]
    if valid(x, T) and h.tau_star(x, T) >= TGT: break
cur = bad(x, T); step = 0.03
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    if rng.random() < 0.3:
        i = rng.randrange(p); nx[i] += rng.gauss(0, step)
    else:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    if not valid(nx, nT): continue
    b = bad(nx, nT)
    if b > cur or h.tau_star(nx, nT) < TGT: continue
    x, T, cur = nx, nT, b
    if it % 15000 == 14999: step *= 0.6
    if cur < -1e-9: break
print("END BAD %.5f tau* %.4f x %s T %s" % (cur, h.tau_star(x, T), [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
