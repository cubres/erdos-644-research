# Is T(argmins) (some ordering) forced by: 3 single-heavy types a^h (heavy only at h), sum_h d_h >= 3/4,
# [optionally d_i+d_j < 3/4], [optionally theta_h > 2x_h/3]?  Random + climb for counterexamples.  NUMERICAL
import random, sys, itertools
rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); p = int(sys.argv[3]); PAIRS = sys.argv[4] == '1'; NOQ = sys.argv[5] == '1'
TF = [(1, .5, .25), (1, 0, .5), (0, 1, .5), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
def T_ok(x, a, b, c): return all(f[0]*a[i] + f[1]*b[i] + f[2]*c[i] <= x[i] + 1e-12 for i in range(len(x)) for f in TF)
def gen():
    x = [rng.uniform(0.3, 1.5) for _ in range(p)]
    A = []
    for h in range(3):
        lo = 2 * x[h] / 3 if NOQ else 4 * x[h] / 7
        if lo >= min(1, x[h]): return None
        t = [0.0] * p; t[h] = rng.uniform(lo, min(1, x[h]))
        rest = 1 - t[h]
        w = [rng.random() ** 3 * (rng.random() < .7) for _ in range(p)]; w[h] = 0
        if sum(w) == 0: return None
        t = [t[i] + rest * w[i] / sum(w) for i in range(p)]
        if any(7 * t[i] > 4 * x[i] for i in range(p) if i != h): return None
        A.append(t)
    d = [x[h] - A[h][h] for h in range(3)]
    if sum(d) < 0.75: return None
    if PAIRS and any(d[i] + d[j] >= 0.75 for i, j in [(0, 1), (0, 2), (1, 2)]): return None
    return x, A, d
n = 0; bad = 0
while n < NT:
    g = gen()
    if g is None: continue
    x, A, d = g; n += 1
    if not any(T_ok(x, *[A[k] for k in tr]) for tr in itertools.permutations(range(3))):
        bad += 1
        if bad <= 3: print('T fails:', [round(v, 3) for v in x], [[round(v, 3) for v in t] for t in A], [round(v, 3) for v in d])
print('p', p, 'pairs<3/4', PAIRS, 'noQ', NOQ, 'n', n, 'T fails', bad)
