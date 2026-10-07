"""INTERSECTING families, >=3 heavy parts: minimise the margin of the MINIMISER MENU = {homogeneous(any type),
T(A,B,C) with minimiser rows (all ordered triples of heavy parts), Q_{a^i}(a^j) (3 a^i-rows on a pencil, 4 a^j
quad)} subject to tau*>=TGT.  Negative => the minimiser menu fails for an intersecting family."""
import random, sys, itertools, numpy as np, heavylib as h
seed, iters, m, p = map(int, sys.argv[1:5]); TGT = 0.7505; rng = random.Random(seed)
TPL = (1,1,2,0,0,0,0)
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def inter(x, T): return all(any(a[i] + b[i] > x[i] + 1e-9 for i in range(p)) for j, a in enumerate(T) for b in T[j:])
def mins(x, T):
    out = {}
    for i in range(p):
        hv = [a for a in T if 7*a[i] > 4*x[i]]
        if hv: out[i] = min(hv, key=lambda a: a[i])
    return out
def rowmargin(x, rows):
    x = np.asarray(x); R = np.asarray(rows)
    pen = h._PM @ R
    return float(min(((2*x - pen)/x).min(), ((4*x - R.sum(axis=0))/x/2).min()))
def menu_margin(x, T):
    best = -9
    for a in T: best = max(best, rowmargin(x, [a]*7))
    M = mins(x, T)
    for A, B, C in itertools.permutations(sorted(M), 3):
        best = max(best, rowmargin(x, [[M[A], M[B], M[C]][k] for k in TPL]))
    for A, B in itertools.permutations(sorted(M), 2):
        best = max(best, rowmargin(x, [M[A]]*3 + [M[B]]*4))   # lines 0,1,2 = pencil at point 0
    return best
def valid(x, T):
    return all(v > 0.005 for v in x) and all(a is not None and all(a[i] <= x[i] + 1e-12 for i in range(p)) for a in T) and inter(x, T) and len(mins(x, T)) >= 3
tries = 0
while True:
    tries += 1
    x = [rng.uniform(0.3, 1.3) for _ in range(p)]
    T = [proj([rng.random()**rng.choice([1,2,4]) for _ in range(p)]) for _ in range(m)]
    if valid(x, T) and h.tau_star_fast(x, T) >= TGT: break
cur = menu_margin(x, T); step = 0.03
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    if rng.random() < 0.3:
        i = rng.randrange(p); nx[i] += rng.gauss(0, step)
    else:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    if not valid(nx, nT): continue
    f = menu_margin(nx, nT)
    if f > cur or h.tau_star_fast(nx, nT) < TGT: continue
    x, T, cur = nx, nT, f
    if it % 10000 == 9999: step *= 0.7
    if cur < -1e-9: break
print("END menu margin %.5f fano margin %.5f tau* %.4f x %s T %s" % (cur, h.fano_margin(x, T)[0], h.tau_star_fast(x, T), [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
