"""Part A numerics: can a family with tau* > 3/4 (all types super-heavy somewhere, all classes nonempty) have NO
triple window?  Lemma A0 says this forces an INF facet (S_k subset S_i u S_j, x_k + x_i < 3/2).  Random local search:
maximise tau*(K) subject to  triple_window_value >= ETA  and  superheavy_margin >= ETAS  and classes nonempty.
Usage: python3 notriple_climb.py seed m iters
"""
import sys, json, random
import numpy as np
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3')
from fastlib import tau_star_f, classes_f, superheavy_margin, triple_window_value

seed, m, iters = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
ETA, ETAS = 1e-3, 1e-3
rng = np.random.default_rng(seed)


def proj(c, x):
    c = np.maximum(c, 0)
    c = np.minimum(c, x)
    s = c.sum()
    if s <= 0:
        return None
    # scale to unit mass, re-clip (few rounds)
    for _ in range(20):
        c = c / c.sum()
        if (c <= x + 1e-12).all():
            return c
        c = np.minimum(c, x)
    return None


def valid(x, K):
    if (x < 0.02).any() or (x >= 1.5).any():
        return False
    if any(c is None for c in K):
        return False
    K = np.asarray(K)
    if superheavy_margin(K, x) < ETAS:
        return False
    S = classes_f(K, x)
    if any(len(s) == 0 for s in S):
        return False
    return triple_window_value(K, x) >= ETA


best_overall = (-1, None)
for restart in range(200):
    # random start
    for _ in range(2000):
        x = rng.uniform(0.05, 1.45, 3)
        K = [proj(rng.random(3) ** rng.choice([1, 2, 4]), x) for _ in range(m)]
        if valid(x, K):
            break
    else:
        continue
    K = np.array(K)
    cur = tau_star_f(K, x)
    step = 0.05
    for it in range(iters):
        nx = x.copy(); nK = K.copy()
        r = rng.random()
        if r < 0.25:
            i = rng.integers(3); nx[i] += rng.normal(0, step)
        elif r < 0.9:
            j = rng.integers(m); c = proj(nK[j] + rng.normal(0, step, 3), nx)
            if c is None:
                continue
            nK[j] = c
        else:
            j = rng.integers(m); c = proj(rng.random(3) ** rng.choice([1, 2, 4]), nx)
            if c is None:
                continue
            nK[j] = c
        # re-project all types to the new capacities
        nKl = [proj(c, nx) for c in nK]
        if not valid(nx, nKl):
            continue
        nK = np.array(nKl)
        t = tau_star_f(nK, nx)
        if t >= cur - 1e-4 * rng.random():
            x, K, cur = nx, nK, t
        if it % 3000 == 2999:
            step *= 0.8
    if cur > best_overall[0]:
        best_overall = (cur, (x.tolist(), K.tolist()))
        S = classes_f(K, x)
        print('restart %d tau* %.4f x %s classes %s tw %.4f' % (restart, cur, np.round(x, 4).tolist(),
              [list(map(int, s)) for s in S], triple_window_value(K, x)), flush=True)
        print('   K', np.round(K, 4).tolist(), flush=True)
print('BEST', best_overall[0])
json.dump({'tau': best_overall[0], 'x': best_overall[1][0], 'K': best_overall[1][1]},
          open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/logs/notriple_%d_%d.json' % (seed, m), 'w'))
