"""Search for an FP counterexample: type sets (sum 1) with tau* >= TGT, NO pair template (pair_margin<0),
minimising the Fano margin (>=0 iff a Fano tuple exists).  Start: note 7.79 nine-type example (+ random)."""
import random, sys, heavylib as h, pairlib as P
seed, iters = int(sys.argv[1]), int(sys.argv[2]); TGT = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7505
rng = random.Random(seed)
V=[(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
x=[513/640]*3; T=[[v/80 for v in a] for a in V]; p = 3; m = len(T)
def proj(a, x):
    a = [max(0.0, v) for v in a]; s = sum(a)
    if s <= 0: return None
    a = [v/s for v in a]
    return a if all(a[i] <= x[i] + 1e-12 for i in range(p)) else None
def ok(x, T):
    return all(v > 0.02 for v in x) and all(a is not None for a in T) and h.tau_star_fast(x, T) >= TGT and P.pair_margin(x, T) < -1e-9
fm = h.fano_margin(x, T)[0]; step = 0.02
print("start fano margin", fm, flush=True)
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    r = rng.random()
    if r < 0.25:
        i = rng.randrange(p); nx[i] += rng.gauss(0, step)
    elif r < 0.9:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]], nx)
    else:
        nx = [v + rng.gauss(0, step/2) for v in x]; nT = [proj([v + rng.gauss(0, step/3) for v in a], nx) for a in T]
    if not ok(nx, nT): continue
    f = h.fano_margin(nx, nT)[0]
    if f <= fm:
        x, T, fm = nx, nT, f
    if it % 2000 == 1999:
        print(it, "fano margin", round(fm, 5), "tau*", round(h.tau_star_fast(x, T), 4), "x", [round(v, 4) for v in x], flush=True)
        if it % 10000 == 9999: step *= 0.7
    if fm < 0:
        print("FANO-FREE & PAIR-FREE tau*", h.tau_star_fast(x, T), "x", x, "T", T, flush=True); break
print("END fm", fm, "x", x, "T", T, flush=True)
