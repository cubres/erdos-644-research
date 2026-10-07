"""Part B, 'maximum margin' search (MAXIMISE the minimum template margin; > 0 = no bad tuple): families K (m types, 3 parts) with tau*(K) >= TGT; minimise
badness = min(fano_margin, pair_margin[, general_margin over all 715 supports]) (normalised violations; > 0 = no bad
tuple of that kind).  Negative badness with tau* >= TGT would be a counterexample candidate (then exact check).
Random local search with restarts; general margin included every GEN_EVERY accepted steps when m <= 6.
Usage: python3 minbad.py seed m iters [TGT] [use_general 0/1]
"""
import sys, json, time
import numpy as np
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3')
from fastlib import tau_star_f, classes_f, pair_margin_f, fano_margin_f, superheavy_margin, general_margin_vec
from badcheck import load_supports

seed, m, iters = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
TGT = float(sys.argv[4]) if len(sys.argv) > 4 else 0.7505
USEG = int(sys.argv[5]) if len(sys.argv) > 5 else 0
rng = np.random.default_rng(seed)
SUP = load_supports() if USEG else None


def proj(c, x):
    c = np.maximum(c, 0); c = np.minimum(c, x)
    if c.sum() <= 0:
        return None
    for _ in range(30):
        c = c / c.sum()
        if (c <= x + 1e-12).all():
            return c
        c = np.minimum(c, x)
    return None


def badness(x, K, gen=False):
    b = min(fano_margin_f(K, x), pair_margin_f(K, x))
    if gen and SUP is not None:
        b = min(b, general_margin_vec(K, x, SUP))
    return b


def valid(x, K):
    return (x >= 0.02).all() and (x < 1.5).all() and all(c is not None for c in K)


best_overall = (-np.inf, None)
for restart in range(10 ** 6):
    for _ in range(20000):
        x = rng.uniform(0.05, 1.45, 3)
        K = []
        for _k in range(m):
            i = rng.integers(3); c = rng.random(3) * 0.4; c[i] = rng.uniform(0.55, 1.0); K.append(proj(c, x))
        if valid(x, K) and tau_star_f(np.array(K), x) >= TGT:
            break
    else:
        continue
    K = np.array(K)
    cur = badness(x, K)
    step = 0.05
    for it in range(iters):
        nx = x.copy(); nK = K.copy()
        r = rng.random()
        if r < 0.2:
            i = rng.integers(3); nx[i] += rng.normal(0, step)
        elif r < 0.92:
            j = rng.integers(m); c = proj(nK[j] + rng.normal(0, step, 3), nx)
            if c is None:
                continue
            nK[j] = c
        else:
            j = rng.integers(m); i = rng.integers(3); c = rng.random(3) * 0.4; c[i] = rng.uniform(0.55, 1.0)
            nK[j] = proj(c, nx)
        nKl = [proj(c, nx) for c in nK]
        if not valid(nx, nKl) or tau_star_f(np.array(nKl), nx) < TGT:
            continue
        nK = np.array(nKl)
        b = badness(nx, nK)
        if b >= cur - 1e-4 * rng.random():
            x, K, cur = nx, nK, b
        if it % 3000 == 2999:
            step *= 0.8
    g = general_margin_vec(K, x, SUP) if SUP is not None else None
    print('restart %d badness %.4f (fano %.4f pair %.4f general %s) tau* %.4f x %s sh %.4f classes %s' % (
        restart, cur, fano_margin_f(K, x), pair_margin_f(K, x), None if g is None else round(float(g), 4),
        tau_star_f(K, x), np.round(x, 4).tolist(), superheavy_margin(K, x), [list(map(int, s)) for s in classes_f(K, x)]), flush=True)
    print('   K', np.round(K, 5).tolist(), flush=True)
    tot = cur if g is None else min(cur, g)
    if tot > best_overall[0]:
        best_overall = (tot, (x.tolist(), K.tolist()))
        json.dump({'badness': float(tot), 'x': x.tolist(), 'K': K.tolist(), 'tau': float(tau_star_f(K, x))},
                  open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/logs/minbad_%d_%d_g%d.json' % (seed, m, USEG), 'w'))
