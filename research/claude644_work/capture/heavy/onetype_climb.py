"""Adversarial: p parts, p types, type j heavy EXACTLY at part j (sum<=1 or =1). maximise tau* subject to
no T(A,B,C) (any ordered triple, rows = the part-types), optionally also no pair template / no Fano."""
import random, sys, itertools, heavylib as h, pairlib as P
p, R, seed, SUM1, MODE = map(int, sys.argv[1:6]); rng = random.Random(seed)
TPL = (1,1,2,0,0,0,0)
def tfeas(x, T):
    return any(h.fano_rows_ok(x, [T[(A,B,C)[k]] for k in TPL]) for A, B, C in itertools.permutations(range(p), 3))
def valid(x, T):
    if any(v < 0.01 for v in x): return False
    for j, a in enumerate(T):
        if any(v < 0 for v in a) or sum(a) > 1 + 1e-12 or (SUM1 and sum(a) < 1 - 1e-12): return False
        if any(a[i] > x[i] + 1e-12 for i in range(p)): return False
        if [i for i in range(p) if 7*a[i] > 4*x[i]] != [j]: return False
    return True
def bad(x, T):
    if tfeas(x, T): return True
    if MODE >= 1 and P.pair_margin(x, T) >= 0: return True
    if MODE >= 2 and h.any_fano_np(x, T): return True
    return False
def rstart():
    for _ in range(100000):
        x = [rng.uniform(0.05, 1.5) for _ in range(p)]
        T = []
        for j in range(p):
            a = [0.0]*p; a[j] = rng.uniform(4*x[j]/7, min(1, x[j]))
            rest = (1 - a[j]) if SUM1 else rng.uniform(0, 1 - a[j])
            w = [rng.random()**3 if i != j else 0 for i in range(p)]; S = sum(w)
            for i in range(p):
                if i != j: a[i] = rest*w[i]/S
            T.append(a)
        if valid(x, T) and not bad(x, T): return x, T
best = (-1,)
for r in range(R):
    st = rstart()
    if st is None: continue
    x, T = st; cur = h.tau_star_fast(x, T); step = 0.05
    for it in range(4000):
        nx = list(x); nT = [list(a) for a in T]
        if rng.random() < 0.3:
            i = rng.randrange(p); nx[i] += rng.gauss(0, step)
        else:
            j = rng.randrange(p); nT[j] = [max(0, v + rng.gauss(0, step)) for v in nT[j]]
            s = sum(nT[j])
            if SUM1 or s > 1: nT[j] = [v/s for v in nT[j]]
        if not valid(nx, nT): continue
        t = h.tau_star_fast(nx, nT)
        if t < cur: continue
        if bad(nx, nT): continue
        x, T, cur = nx, nT, t
        if it % 800 == 799: step *= 0.6
    print(f"restart {r}: tau* {cur:.4f} x={[round(v,4) for v in x]} T={[[round(v,4) for v in a] for a in T]}", flush=True)
    if cur > best[0]: best = (cur, x, T)
print("BEST", best, flush=True)
