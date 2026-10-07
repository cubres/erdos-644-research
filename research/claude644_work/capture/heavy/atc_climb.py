"""Conjecture A_tc test: INTERSECTING type sets (every two types, incl. a type with itself, overlap in some part:
a_i+b_i>x_i) with tau*>=TGT; minimise the normalised Fano margin.  Negative => A_tc counterexample."""
import random, sys, heavylib as h, pairlib as P
seed, iters, m, p = map(int, sys.argv[1:5]); TGT = 0.7505; rng = random.Random(seed)
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def inter(x, T): return all(any(a[i] + b[i] > x[i] + 1e-9 for i in range(p)) for j, a in enumerate(T) for b in T[j:])
def valid(x, T): return all(v > 0.005 for v in x) and all(a is not None and all(a[i] <= x[i] + 1e-12 for i in range(p)) for a in T) and inter(x, T)
tries = 0
while True:
    tries += 1
    x = [rng.uniform(0.3, 1.3) for _ in range(p)]
    T = [proj([rng.random()**rng.choice([1,2,4]) for _ in range(p)]) for _ in range(m)]
    if valid(x, T) and h.tau_star_fast(x, T) >= TGT: break
cur = h.fano_margin(x, T)[0]; step = 0.03
print("start fm", round(cur, 4), "tries", tries, flush=True)
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    if rng.random() < 0.3:
        i = rng.randrange(p); nx[i] += rng.gauss(0, step)
    else:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    if not valid(nx, nT): continue
    f = h.fano_margin(nx, nT)[0]
    if f > cur or h.tau_star_fast(nx, nT) < TGT: continue
    x, T, cur = nx, nT, f
    if it % 10000 == 9999: step *= 0.7
    if cur < -1e-9: break
print("END fm %.5f tau* %.4f pm %.4f x %s T %s" % (cur, h.tau_star_fast(x, T), P.pair_margin(x, T), [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
