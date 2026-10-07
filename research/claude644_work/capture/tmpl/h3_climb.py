# |H|>=3 rigid finite type sets: maximise tau* s.t. NO template from the menu works.
# menus: 'QVT' = H, Q_a/Q_b, V (all ordered pairs), T(A,B,C) (all ordered triples of types, equal rows per class)
#        'QVTF' = plus every Fano colouring by types (orbit reps)
import random, sys, itertools
from h2_lib import *
from hub_lib import fano_colourings
p, nt = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(int(sys.argv[3])); iters = int(sys.argv[4]); MENU = sys.argv[5]
NH = int(sys.argv[6]) if len(sys.argv) > 6 else 3
SINGLE = len(sys.argv) > 7 and sys.argv[7] == 'single'   # number of heavy parts (parts 0..NH-1)
FC = fano_colourings(nt) if 'F' in MENU else []
TF = [(1, .5, .25), (1, 0, .5), (0, 1, .5), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
def T_ok(x, a, b, c):
    return all(f[0] * a[i] + f[1] * b[i] + f[2] * c[i] <= x[i] + 1e-12 for i in range(len(x)) for f in TF)
def argmins(x, T):
    am = {}
    for h in range(NH):
        Ch = [t for t in T if 7 * t[h] > 4 * x[h]]
        am[h] = min(Ch, key=lambda t: t[h])
    return am
def canon(x, T):
    am = argmins(x, T)
    for i in range(NH):
        for j in range(NH):
            if i == j: continue
            a0 = am[i]
            if feas(x, a0, am[j], TWO['Qt']): return 'Qcan'
            S = [b for b in T if 7 * b[j] > 4 * x[j] and all(b[l] + a0[l] <= x[l] + 1e-12 for l in range(len(x)) if l not in (i, j))]
            if S:
                bs = max(S, key=lambda b: x[j] - b[j])
                if feas(x, a0, bs, TWO['V']): return 'Vcan'
    for tr in itertools.permutations(range(NH), 3):
        if T_ok(x, *[am[k] for k in tr]): return 'Tmin'
    return None
def works(x, T):
    for t in T:
        if all(7 * t[k] <= 4 * x[k] + 1e-12 for k in range(len(x))): return 'H'
    if MENU == 'CAN': return canon(x, T)
    for i, a in enumerate(T):
        for j, b in enumerate(T):
            if i == j: continue
            if feas(x, a, b, TWO['Qt']): return 'Q'
            if feas(x, a, b, TWO['V']): return 'V'
    if MENU == 'QV': return None
    if MENU == 'QVTmin':
        am = argmins(x, T)
        for tr in itertools.permutations(range(NH), 3):
            if T_ok(x, *[am[k] for k in tr]): return 'Tmin'
        return None
    for tr in itertools.permutations(range(len(T)), 3):
        if T_ok(x, T[tr[0]], T[tr[1]], T[tr[2]]): return 'T'
    for col in FC:
        if fano_rigid(x, T, col): return 'F'
    return None
def valid(x, T):
    if sum(x) < 1.75: return False
    hv = set()
    for t in T:
        if abs(sum(t) - 1) > 1e-9 or any(t[i] < 0 or t[i] > x[i] for i in range(p)): return False
        h = [i for i in range(p) if 7 * t[i] > 4 * x[i]]
        if not h or any(i >= NH for i in h): return False
        if SINGLE and len(h) > 1: return False
        hv |= set(h)
    return len(hv) == NH
def rand_type(x):
    for _ in range(100):
        h = rng.randrange(NH)
        t = [0.0] * p
        t[h] = rng.uniform(4 * x[h] / 7, min(1, x[h]))
        rest = 1 - t[h]
        w = [rng.random() * (rng.random() < .6) for _ in range(p)]; w[h] = 0
        if sum(w) == 0: w[(h + 1) % p] = 1
        s = sum(w); t2 = [t[i] + rest * w[i] / s for i in range(p)]
        if all(t2[i] <= x[i] for i in range(p)): return t2
    return None
best = None; cur = None
for it in range(iters):
    if best is None or rng.random() < 0.01:
        x = [rng.uniform(0.3, 1.6) for _ in range(p)]
        T = [rand_type(x) for _ in range(nt)]
        if None in T or not valid(x, T) or works(x, T): continue
        c = (tau_rigid2(x, T), x, T)
        if best is None or c[0] > best[0]: best = c
        cur = c; continue
    t0, x0, T0 = best if rng.random() < 0.6 else cur
    s = rng.choice([0.1, 0.03, 0.01, 0.003, 0.001])
    x = [max(0.01, v + rng.gauss(0, s) * (rng.random() < .7)) for v in x0]
    T = [[max(0, v + rng.gauss(0, s) * (rng.random() < 0.4)) for v in t] for t in T0]
    T = [[v / sum(t) for v in t] for t in T]
    if not valid(x, T): continue
    tt = tau_rigid2(x, T)
    if tt < t0 - 1e-12: continue
    if works(x, T): continue
    cur = (tt, x, T)
    if tt > best[0]:
        best = cur
        print(it, round(tt, 5), [round(v, 4) for v in x], [[round(v, 4) for v in t] for t in T], flush=True)
print('FINAL', best[0], best[1], best[2])
