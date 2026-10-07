"""generalp: adversarial climb for Th_Z'(p) (Lemma Z in notes_generalp.md): FINITE SUB-UNIT generator sets.
Variables: capacities x (p parts, x_i >= XMIN), m generators g with 0 <= g <= x, |g| in [SMIN, 1].
Objective tauZ := min(tau*(Gen), N - 1) (= tau*(G_1), Lemma U).  Menu: all Fano assignments lines -> generators
(Lemma 7.63; includes the homogeneous Fano g <= 4x/7 and the pencil of Lemma Z(c)) + the 42 two-type functions (pairlib).
Regime: at least HMIN parts host super-heavy unit completions (min(x_i, g_i + 1 - |g|) > 2x_i/3 for some g).
Mode maxtau: maximise tauZ subject to BAD < 0.   Mode minbad: minimise BAD subject to tauZ >= TGT.
usage: python3 climb_sub.py seed iters m p mode [TGT] [HMIN] [XMIN] [SMIN]"""
import random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'heavy'))
import heavylib as H, pairlib as P
seed, iters, m, p, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
TGT = float(sys.argv[6]) if len(sys.argv) > 6 else 0.7505
HMIN = int(sys.argv[7]) if len(sys.argv) > 7 else 3
XMIN = float(sys.argv[8]) if len(sys.argv) > 8 else 0.005
SMIN = float(sys.argv[9]) if len(sys.argv) > 9 else 0.4
rng = random.Random(seed)
def hosts(x, T):
    return [i for i in range(p) if any(min(x[i], g[i] + 1 - sum(g)) > 2*x[i]/3 + 1e-9 for g in T)]
def regime_ok(x, T):
    if any(v < XMIN or v > 3.0 for v in x): return False
    for g in T:
        if g is None or any(v < 0 for v in g) or any(g[i] > x[i] + 1e-12 for i in range(p)): return False
        s = sum(g)
        if s > 1 + 1e-12 or s < SMIN: return False
    return len(hosts(x, T)) >= HMIN
def tauZ(x, T): return min(H.tau_star_fast(x, T), sum(x) - 1)
def bad(x, T): return max(P.pair_margin(x, T), H.fano_margin(x, T)[0])
def rand_start():
    while True:
        x = [rng.uniform(0.3, 1.5) for _ in range(p)]
        T = []
        for j in range(m):
            i = j % p
            a = [rng.random()**rng.choice([1, 2, 4]) for _ in range(p)]
            a[i] = 0.0; s = sum(a); f = rng.uniform(2*x[i]/3 + 0.01, min(x[i], 1.0))
            a = [v/s*(1-f) for v in a]; a[i] = f
            sc = rng.uniform(max(SMIN, 0.6), 1.0)
            T.append([v*sc for v in a])
        if regime_ok(x, T): return x, T
x, T = rand_start()
if mode == 'minbad':
    while tauZ(x, T) < TGT: x, T = rand_start()
else:
    while bad(x, T) >= -1e-9: x, T = rand_start()
tau = tauZ(x, T); cur = bad(x, T); step = 0.03
print("start tauZ", round(tau, 5), "BAD", round(cur, 5), "hosts", hosts(x, T), flush=True)
for it in range(iters):
    nx = list(x); nT = [list(a) for a in T]
    r = rng.random()
    if r < 0.25:
        i = rng.randrange(p); nx[i] += rng.gauss(0, step)
    elif r < 0.85:
        j = rng.randrange(m); nT[j] = [max(0.0, v + rng.gauss(0, step)) for v in nT[j]]
        s = sum(nT[j])
        if s > 1: nT[j] = [v/s for v in nT[j]]
    elif r < 0.93:
        j = rng.randrange(m); sc = rng.uniform(0.9, 1.1); nT[j] = [v*sc for v in nT[j]]
        s = sum(nT[j])
        if s > 1: nT[j] = [v/s for v in nT[j]]
    else:
        nx = [v + rng.gauss(0, step/2) for v in x]; nT = [[max(0.0, v + rng.gauss(0, step/3)) for v in a] for a in T]
        nT = [[v/max(1.0, sum(a)) for v in a] for a in nT]
    if not regime_ok(nx, nT): continue
    if mode == 'maxtau':
        b = bad(nx, nT)
        if b >= -1e-9: continue
        nt = tauZ(nx, nT)
        if nt < tau: continue
        x, T, tau, cur = nx, nT, nt, b
    else:
        b = bad(nx, nT)
        if b > cur: continue
        nt = tauZ(nx, nT)
        if nt < TGT: continue
        x, T, tau, cur = nx, nT, nt, b
    if it % 2000 == 1999:
        print(it, "tauZ", round(tau, 5), "BAD", round(cur, 5), "x", [round(v, 4) for v in x], "|g|", [round(sum(g), 3) for g in T], flush=True)
        if it % 10000 == 9999: step *= 0.7
print("END tauZ", tau, "BAD", cur, "hosts", hosts(x, T), "x", x, "T", T, flush=True)
