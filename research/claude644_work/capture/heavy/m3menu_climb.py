"""Test the templates agent's CONJECTURE M3-menu: tau*>3/4 => a bad tuple from {H (hom), Q, V, T} with rigid
types.  Minimise the normalised menu margin subject to tau* >= TGT (p=3), from structured starts
(0: H3s-cex, 1: note 7.79, 2: random).  Also report the full FP margin (any Fano + 42 pair fns)."""
import random, sys, itertools, numpy as np, heavylib as h, pairlib as P
seed, iters, start = map(int, sys.argv[1:4]); TGT = 0.7505; rng = random.Random(seed)
def menu_margin(x, T):
    x = np.asarray(x, float); T = np.asarray(T, float); m = len(T)
    # H: 7 copies: 3a<=2x, 7a<=4x  -> normalised slack
    hm = np.minimum((2*x - 3*T)/x, (4*x - 7*T)/x/2).min(axis=1).max()
    S = T[:, None, :]; U = T[None, :, :]           # S = s-type (first), U = t-type
    # Q_s: 3 s-rows on a pencil, 4 t-rows on the quadrilateral: 3s<=2x, 3s+4t<=4x
    qm = np.minimum((2*x - 3*S)/x, (4*x - 3*S - 4*U)/x/2).min(axis=2).max()
    # V(s,t): 5 s-rows, 2 t-rows: s+t<=x, 5s/4+t/2<=x
    vm = np.minimum((x - S - U)/x, (x - 1.25*S - 0.5*U)/x).min(axis=2).max()
    # T: alpha quad x4, beta x2, gamma x1: 2al+be<=2x, 2al+ga<=2x, 2be+ga<=2x, 4al+2be+ga<=4x
    A = T[:, None, None, :]; B = T[None, :, None, :]; G = T[None, None, :, :]
    tm = np.minimum(np.minimum((2*x - 2*A - B)/x, (2*x - 2*A - G)/x), np.minimum((2*x - 2*B - G)/x, (4*x - 4*A - 2*B - G)/x/2)).min(axis=3).max()
    return float(max(hm, qm, vm, tm))
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def valid(x, T): return all(v > 0.005 for v in x) and all(a is not None and all(a[i] <= x[i] + 1e-12 for i in range(3)) for a in T)
if start == 0:
    x = [0.861, 1.44, 0.741]; T = [[.664, 0, .336], [.019, .981, 0], [.424, 0, .576]]
    T += [proj([v + rng.gauss(0, .02) for v in T[k % 3]]) for k in range(3)]
elif start == 1:
    V=[(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
    x=[513/640]*3; T=[[v/80 for v in a] for a in V]
else:
    while True:
        x = [rng.uniform(0.4, 1.5) for _ in range(3)]
        T = [proj([rng.random()**rng.choice([1,2,4,8]) for _ in range(3)]) for _ in range(6)]
        if valid(x, T) and h.tau_star_fast(x, T) >= TGT: break
m = len(T)
assert valid(x, T) and h.tau_star_fast(x, T) >= TGT, h.tau_star_fast(x, T)
cur = menu_margin(x, T); step = 0.02
print("start menu margin", round(cur, 4), flush=True)
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    if rng.random() < 0.25:
        i = rng.randrange(3); nx[i] += rng.gauss(0, step)
    else:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    if not valid(nx, nT): continue
    f = menu_margin(nx, nT)
    if f > cur or h.tau_star_fast(nx, nT) < TGT: continue
    x, T, cur = nx, nT, f
    if it % 10000 == 9999: step *= 0.7
    if cur < -1e-9: break
print("END menu margin %.5f | FP: fano %.5f pair %.5f | tau* %.4f x %s T %s" % (cur, h.fano_margin(x, T)[0], P.pair_margin(x, T), h.tau_star_fast(x, T), [round(v,4) for v in x], [[round(v,4) for v in a] for a in T]), flush=True)
