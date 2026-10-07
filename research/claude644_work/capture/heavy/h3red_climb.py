"""Adversarial climb for H3-REDUCED: maximise tau*_H over Fano-free type sets on h parts (types sum<=1, each
heavy somewhere, every part hosts a heavy type).  If sup stays < 3/4, supports Conjecture H3 (reduced form,
which implies H3 since light parts never obstruct Fano templates)."""
import random, sys, heavylib as h
hh, m, R, seed = map(int, sys.argv[1:5]); SUM1 = int(sys.argv[5]) if len(sys.argv) > 5 else 0
rng = random.Random(seed)
def valid(x, T):
    if any(v < 0.02 for v in x): return False
    for a in T:
        if any(a[i] < 0 or a[i] > x[i] + 1e-12 for i in range(hh)) or sum(a) > 1 + 1e-12: return False
        if SUM1 and sum(a) < 1 - 1e-9: return False
        if h.is_homog(x, a): return False
    return len(h.heavy_parts(x, T)) == hh
def rtype(x):
    for _ in range(1000):
        s = 1.0 if SUM1 else rng.uniform(0.5, 1.0)
        w = [rng.random()**rng.choice([1,2,4]) for _ in range(hh)]; S = sum(w); a = [s*v/S for v in w]
        if all(a[i] <= x[i] for i in range(hh)): return a
    return None
def proj(a, x):
    a = [max(0.0, min(v, x[i])) for i, v in enumerate(a)]
    s = sum(a)
    if SUM1:
        if s <= 0: return None
        a = [v/s for v in a]
        if any(a[i] > x[i] for i in range(hh)): return None
    elif s > 1: a = [v/s for v in a]
    return a
best = (-1,)
for r in range(R):
    for _ in range(50000):
        x = [rng.uniform(0.3, 1.4) for _ in range(hh)]
        T = [rtype(x) for _ in range(m)]
        if None in T or not valid(x, T): continue
        if not h.any_fano_np(x, T): break
    else:
        print("restart", r, "no start", flush=True); continue
    cur = h.tau_star_fast(x, T); step = 0.08
    for it in range(1500):
        nx = list(x); nT = [list(a) for a in T]
        mv = rng.random()
        if mv < 0.3:
            i = rng.randrange(hh); nx[i] = max(0.02, nx[i] + rng.gauss(0, step))
        elif mv < 0.8:
            j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]], nx)
        else:
            nx = [max(0.02, v + rng.gauss(0, step)) for v in x]
            nT = [proj([v + rng.gauss(0, step/2) for v in a], nx) for a in T]
        if any(a is None for a in nT) or not valid(nx, nT): continue
        t = h.tau_star_fast(nx, nT)
        if t < cur - 1e-9: continue
        if h.any_fano_np(nx, nT): continue
        x, T, cur = nx, nT, t
        if it % 300 == 299: step *= 0.6
    print(f"restart {r}: Fano-free tau*_H {cur:.4f} x={[round(v,4) for v in x]} T={[[round(v,4) for v in a] for a in T]}", flush=True)
    if cur > best[0]: best = (cur, x, T)
print("BEST", round(best[0], 4), best[1], best[2], flush=True)
