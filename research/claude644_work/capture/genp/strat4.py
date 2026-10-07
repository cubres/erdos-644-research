"""generalp: adversarial climb against RESTRICTED menus in the super-heavy regime with h heavy parts.
Regime: parts 0..h-1 host super-heavy types (>2x/3); parts h..p-1 light (all traces <= 2x/3); every type
super-heavy somewhere.  Menus (witness-robust where requests are involved):
  min  : Fano colourings on the h class minimisers (row = minimiser of its class) + V pairs of minimisers
  minc : min + corner witnesses: for each class X with minimiser a, request u=(x-a off X, sigma_X-eps at X)
         (cost 1-a_X+e_X, must be < tau*); adversary picks the witness (any type <= u); we need for EVERY
         witness choice some Fano colouring (rows from minimisers + that witness) or V pair to work.
  all  : Fano over all types + V over all pairs (reference).
Mode: minimise menu margin s.t. tau* >= TGT.  usage: python3 strat4.py seed iters m p h menu [TGT]
"""
import random, sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'heavy'))
import heavylib as H
seed, iters, m, p, h, menu = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
TGT = float(sys.argv[7]) if len(sys.argv) > 7 else 0.7505
rng = random.Random(seed)

def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def regime_ok(x, T):
    if any(v < 0.05 or v > 1.5 for v in x[:h]) or any(v < 0.05 or v > 3.0 for v in x[h:]): return False
    for a in T:
        if a is None or any(a[i] > x[i] + 1e-12 for i in range(p)): return False
        if not any(3*a[i] > 2*x[i] + 1e-9 for i in range(h)): return False
        if any(3*a[i] > 2*x[i] + 1e-12 for i in range(h, p)): return False
    for i in range(h):
        if not any(3*a[i] > 2*x[i] + 1e-9 for a in T): return False
    return True
def v_margin_rows(x, R, pairs=None):
    x = np.asarray(x, float); R = np.asarray(R, float)
    S = R[:, None, :]; U = R[None, :, :]
    mm = np.minimum((x - S - U)/x, (x - 1.25*S - 0.5*U)/x).min(axis=2)
    if pairs is not None:
        best = -1e9
        for (i, j) in pairs: best = max(best, mm[i, j])
        return best
    return float(mm.max())
def fano_rows_margin(x, R):
    return H.fano_margin(x, R)[0]
def classes(x, T):
    return [[j for j in range(len(T)) if 3*T[j][i] > 2*x[i]] for i in range(h)]
def minimisers(x, T):
    S = classes(x, T)
    return [min(S[i], key=lambda j: T[j][i]) for i in range(h)]
def menu_margin(x, T):
    if menu == 'all':
        return max(fano_rows_margin(x, T), v_margin_rows(x, T))
    mins = minimisers(x, T); R = [T[j] for j in mins]
    base = max(fano_rows_margin(x, R), v_margin_rows(x, R))
    if menu == 'min': return base
    # corners
    tau = H.tau_star_fast(x, T)
    worst = 1e9
    for X in range(h):
        a = R[X]; sig = a[X]; e = x[X] - sig
        cost = 1 - a[X] + e
        if cost >= tau - 1e-9: continue          # request not affordable: skip
        u = [x[i] - a[i] for i in range(p)]; u[X] = sig
        wit = [j for j in range(len(T)) if all(T[j][i] <= u[i] + 1e-12 for i in range(p)) and T[j][X] < sig - 1e-12]
        if not wit: continue                      # cannot happen if tau* correct (u costs < tau*), but be safe
        wm = 1e9
        for j in wit:
            R2 = R + [T[j]]
            wm = min(wm, max(fano_rows_margin(x, R2), v_margin_rows(x, R2)))
        # this corner strategy gives margin wm (adversary picks witness); strategy may choose the best corner
        worst = min(worst, -wm)   # placeholder, replaced below
    # strategy chooses the corner X maximising its guaranteed margin
    bestc = base
    for X in range(h):
        a = R[X]; sig = a[X]; e = x[X] - sig
        cost = 1 - a[X] + e
        if cost >= tau - 1e-9: continue
        u = [x[i] - a[i] for i in range(p)]; u[X] = sig
        wit = [j for j in range(len(T)) if all(T[j][i] <= u[i] + 1e-12 for i in range(p)) and T[j][X] < sig - 1e-12]
        if not wit: continue
        wm = 1e9
        for j in wit:
            R2 = R + [T[j]]
            wm = min(wm, max(fano_rows_margin(x, R2), v_margin_rows(x, R2)))
        bestc = max(bestc, wm)
    return bestc
def rand_start():
    while True:
        x = [rng.uniform(0.5, 1.5) for _ in range(h)] + [rng.uniform(0.3, 2.0) for _ in range(p - h)]
        T = []
        for j in range(m):
            i = j % h
            a = [rng.random()**rng.choice([1, 2, 4]) for _ in range(p)]
            a[i] = 0.0; s = sum(a); f = rng.uniform(2*x[i]/3 + 0.01, min(x[i], 1.0))
            a = [v/s*(1-f) for v in a]; a[i] = f
            T.append(a)
        if regime_ok(x, T) and H.tau_star_fast(x, T) >= TGT: return x, T
x, T = rand_start()
tau = H.tau_star_fast(x, T); cur = menu_margin(x, T); step = 0.03
print("start tau*", round(tau, 5), "margin", round(cur, 5), flush=True)
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    r = rng.random()
    if r < 0.25:
        i = rng.randrange(p); nx[i] += rng.gauss(0, step)
    elif r < 0.9:
        j = rng.randrange(m); nT[j] = proj([v + rng.gauss(0, step) for v in nT[j]])
    else:
        nx = [v + rng.gauss(0, step/2) for v in x]; nT = [proj([v + rng.gauss(0, step/3) for v in a]) for a in T]
    if not regime_ok(nx, nT): continue
    nt = H.tau_star_fast(nx, nT)
    if nt < TGT: continue
    b = menu_margin(nx, nT)
    if b > cur: continue
    x, T, tau, cur = nx, nT, nt, b
    if it % 1000 == 999:
        print(it, "tau*", round(tau, 5), "margin", round(cur, 5), "x", [round(v, 4) for v in x], flush=True)
        if it % 5000 == 4999: step *= 0.7
print("END tau*", tau, "margin", cur, "x", x, "T", T, flush=True)
