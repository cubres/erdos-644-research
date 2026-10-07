"""Conjecture H3s test: SIMPLE-heavy type sets (each type heavy at exactly one part), >=3 parts hosting heavy
types, tau* >= TGT.  Minimise the Fano margin (>=0 iff a Fano tuple exists).  Negative => H3s counterexample."""
import random, sys, heavylib as h, pairlib as P
seed, iters, start, m, p = map(int, sys.argv[1:6]); TGT = 0.7505
rng = random.Random(seed)
def hs(x, a): return [i for i in range(len(x)) if 7*a[i] > 4*x[i]]
def valid(x, T):
    if any(v < 0.005 for v in x): return False
    for a in T:
        if a is None or any(v < -1e-12 for v in a) or abs(sum(a)-1) > 1e-9 or any(a[i] > x[i]+1e-12 for i in range(len(x))): return False
        if len(hs(x, a)) != 1: return False
    return len(set(hs(x, a)[0] for a in T)) >= 3
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
if start == 0:
    V=[(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
    x=[513/640]*3; T=[[v/80 for v in a] for a in V]; p = 3
else:
    while True:
        x = [rng.uniform(0.2, 1.5) for _ in range(p)]
        T = [proj([rng.random()**rng.choice([1,2,4,8]) for _ in range(p)]) for _ in range(m)]
        if valid(x, T) and h.tau_star_fast(x, T) >= TGT: break
m = len(T)
fm = h.fano_margin(x, T)[0]; step = 0.03
print("start fm", fm, "tau*", h.tau_star_fast(x, T), flush=True)
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
    f = h.fano_margin(nx, nT)[0]
    if f > fm: continue
    if h.tau_star_fast(nx, nT) < TGT: continue
    x, T, fm = nx, nT, f
    if it % 3000 == 2999:
        print(it, "fm", round(fm, 5), "tau*", round(h.tau_star_fast(x, T), 4), "x", [round(v, 4) for v in x], flush=True)
        if it % 15000 == 14999: step *= 0.7
    if fm < -1e-9:
        print("H3s-CEX tau*", h.tau_star_fast(x, T), "x", x, "T", T, "pair margin", P.pair_margin(x, T), flush=True); break
print("END fm", fm, "tau*", h.tau_star_fast(x, T), "x", x, "T", T, flush=True)
