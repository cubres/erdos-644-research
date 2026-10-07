# Collect single-heavy |H|=3 instances with tau*>=3/4 where the CANONICAL pairs fail; record T(argmin) orderings.
import random, sys, itertools, json
from h2_lib import *
p, nt = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(int(sys.argv[3])); NEED = int(sys.argv[4])
TF = [(1, .5, .25), (1, 0, .5), (0, 1, .5), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
def T_ok(x, a, b, c): return all(f[0]*a[i] + f[1]*b[i] + f[2]*c[i] <= x[i] + 1e-12 for i in range(len(x)) for f in TF)
def argmins(x, T):
    return {h: min([t for t in T if 7 * t[h] > 4 * x[h]], key=lambda t: t[h]) for h in range(3)}
def canpairs(x, T):
    am = argmins(x, T)
    for i in range(3):
        for j in range(3):
            if i == j: continue
            a0 = am[i]
            if feas(x, a0, am[j], TWO['Qt']): return True
            S = [b for b in T if 7 * b[j] > 4 * x[j] and all(b[l] + a0[l] <= x[l] + 1e-12 for l in range(len(x)) if l not in (i, j))]
            if S and feas(x, a0, max(S, key=lambda b: x[j] - b[j]), TWO['V']): return True
    return False
def valid(x, T):
    if sum(x) < 1.75: return False
    hv = set()
    for t in T:
        if abs(sum(t) - 1) > 1e-9 or any(t[i] < 0 or t[i] > x[i] for i in range(p)): return False
        h = [i for i in range(p) if 7 * t[i] > 4 * x[i]]
        if len(h) != 1 or h[0] >= 3: return False
        hv |= set(h)
    return len(hv) == 3
def rand_inst():
    x = [rng.uniform(0.3, 1.5) for _ in range(p)]
    T = []
    for k in range(nt):
        h = k % 3; t = [0.0] * p; t[h] = rng.uniform(4 * x[h] / 7, min(1, x[h]))
        w = [rng.random() * (rng.random() < .6) for _ in range(p)]; w[h] = 0
        if sum(w) == 0: w[(h + 1) % p] = 1
        T.append([t[i] + (1 - t[h]) * w[i] / sum(w) for i in range(p)])
    return x, T
out = []
while len(out) < NEED:
    x, T = rand_inst()
    if not valid(x, T) or canpairs(x, T): continue
    t0 = tau_rigid2(x, T)
    for it in range(3000):
        if t0 >= 0.75: break
        s = rng.choice([0.05, 0.02, 0.005])
        x2 = [max(0.01, v + rng.gauss(0, s)) for v in x]
        T2 = [[max(0, v + rng.gauss(0, s) * (rng.random() < .5)) for v in t] for t in T]
        T2 = [[v / sum(t) for v in t] for t in T2]
        if not valid(x2, T2) or canpairs(x2, T2): continue
        t2 = tau_rigid2(x2, T2)
        if t2 >= t0: x, T, t0 = x2, T2, t2
    if t0 < 0.75: continue
    am = argmins(x, T)
    ords = [tr for tr in itertools.permutations(range(3)) if T_ok(x, *[am[k] for k in tr])]
    th = [am[h][h] for h in range(3)]; d = [x[h] - th[h] for h in range(3)]
    rec = {'tau': t0, 'x': x, 'T': T, 'orders': ords, 'd': d, 'theta': th, 'cross': [[am[h][k] for k in range(p)] for h in range(3)]}
    out.append(rec)
    print(json.dumps({'tau': round(t0, 4), 'd': [round(v, 3) for v in d], 'th': [round(v, 3) for v in th], 'x': [round(v, 3) for v in x],
                      'argmins': [[round(v, 3) for v in am[h]] for h in range(3)], 'orders': ords}), flush=True)
