"""generalp: adversarial climb over finite type sets on p parts in the SUPER-HEAVY regime.
Regime: every type super-heavy (>2x/3) at some part; parts 0..h-1 each host a super-heavy type; parts h..p-1 are
LIGHT (all types <= 2x/3 there).  Menu: all Fano assignments (Lemma 7.63) + 42 two-type functions.
Mode A (maxtau): maximise tau* subject to BAD = max(fano_margin, pair_margin) < 0.
Mode B (minbad): minimise BAD subject to tau* >= TGT.
usage: python3 climb_h.py seed iters m p h mode [TGT]
"""
import random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'heavy'))
import heavylib as H, pairlib as P
seed, iters, m, p, h, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
TGT = float(sys.argv[7]) if len(sys.argv) > 7 else 0.7505
rng = random.Random(seed)
def proj(a):
    a = [max(0.0, v) for v in a]; s = sum(a); return [v/s for v in a] if s > 0 else None
def regime_ok(x, T):
    if any(v < 0.05 or v > 1.5 for v in x[:h]) or any(v < 0.05 or v > 3.0 for v in x[h:]): return False
    for a in T:
        if a is None or any(a[i] > x[i] + 1e-12 for i in range(p)): return False
        if not any(3*a[i] > 2*x[i] + 1e-9 for i in range(h)): return False      # super-heavy somewhere (heavy parts)
        if any(3*a[i] > 2*x[i] + 1e-12 for i in range(h, p)): return False      # light parts stay light
    for i in range(h):
        if not any(3*a[i] > 2*x[i] + 1e-9 for a in T): return False           # every heavy part hosts a class
    return True
def bad(x, T): return max(P.pair_margin(x, T), H.fano_margin(x, T)[0])
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
        if regime_ok(x, T): return x, T
x, T = rand_start()
if mode == 'minbad':
    while H.tau_star_fast(x, T) < TGT: x, T = rand_start()
else:
    while bad(x, T) >= -1e-9: x, T = rand_start()
tau = H.tau_star_fast(x, T); cur = bad(x, T); step = 0.03
print("start tau*", round(tau, 5), "BAD", round(cur, 5), flush=True)
best_report = None
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
    if mode == 'maxtau':
        b = bad(nx, nT)
        if b >= -1e-9: continue
        nt = H.tau_star_fast(nx, nT)
        if nt < tau: continue
        x, T, tau, cur = nx, nT, nt, b
    else:
        b = bad(nx, nT)
        if b > cur: continue
        nt = H.tau_star_fast(nx, nT)
        if nt < TGT: continue
        x, T, tau, cur = nx, nT, nt, b
    if it % 2000 == 1999:
        print(it, "tau*", round(tau, 5), "BAD", round(cur, 5), "x", [round(v, 4) for v in x], flush=True)
        if it % 10000 == 9999: step *= 0.7
print("END tau*", tau, "BAD", cur, "x", x, "T", T, flush=True)
