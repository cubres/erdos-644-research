"""General FP test: minimise BAD = max(pair_margin, fano_margin) over type sets (sum 1) on p parts with
tau* >= TGT.  BAD < 0 => counterexample to Conjecture FP (then check full 715-support catalogue)."""
import random, sys, heavylib as h, pairlib as P
seed, iters, start, m, p = map(int, sys.argv[1:6]); TGT = 0.7505; rng = random.Random(seed)
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def valid(x, T):
    return all(v > 0.005 for v in x) and all(a is not None and all(a[i] <= x[i] + 1e-12 for i in range(len(x))) for a in T)
def bad(x, T): return max(P.pair_margin(x, T), h.fano_margin(x, T)[0])
if start == 0:
    V=[(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
    x=[513/640]*3; T=[[v/80 for v in a] for a in V]
elif start == 2:   # W + third part + helpers
    x = [1.25, 1.25, 0.3]; T = [[.15,.85,0],[.85,.15,0]] + [proj([rng.random() for _ in range(3)]) for _ in range(m-2)]
    while not (valid(x, T) and h.tau_star_fast(x, T) >= TGT):
        T = [[.15,.85,0],[.85,.15,0]] + [proj([rng.random()**3 for _ in range(3)]) for _ in range(m-2)]
else:
    while True:
        x = [rng.uniform(0.2, 1.5) for _ in range(p)]
        T = [proj([rng.random()**rng.choice([1,2,4,8]) for _ in range(p)]) for _ in range(m)]
        if valid(x, T) and h.tau_star_fast(x, T) >= TGT: break
p = len(x); m = len(T)
cur = bad(x, T); step = 0.03
print("start BAD", cur, "tau*", h.tau_star_fast(x, T), flush=True)
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    r = rng.random()
    if r < 0.25:
        i = rng.randrange(p); nx[i] += rng.gauss(0, step)
    elif r < 0.9:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    else:
        nx = [v + rng.gauss(0, step/2) for v in x]; nT = [proj([v + rng.gauss(0, step/3) for v in a]) for a in T]
    if not valid(nx, nT): continue
    b = bad(nx, nT)
    if b > cur: continue
    if h.tau_star_fast(nx, nT) < TGT: continue
    x, T, cur = nx, nT, b
    if it % 3000 == 2999:
        print(it, "BAD", round(cur, 5), "tau*", round(h.tau_star_fast(x, T), 4), "x", [round(v, 4) for v in x], flush=True)
        if it % 15000 == 14999: step *= 0.7
    if cur < -1e-9:
        print("FP-CEX tau*", h.tau_star_fast(x, T), "x", x, "T", T, flush=True); break
print("END BAD", cur, "tau*", h.tau_star_fast(x, T), "x", x, "T", T, flush=True)
