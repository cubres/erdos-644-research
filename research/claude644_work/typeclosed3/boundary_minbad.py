"""Maximum-margin search with a FORCED boundary type: type 0 is super-heavy only at part 0 with
c_0 in [2x_0/3 + 1e-3, 2x_0/3 + BND] and light (<= 2x/3 - 1e-3) elsewhere, tau* >= TGT, all types strictly super-heavy
somewhere.  Tests whether mechanism (b) (boundary types) lowers the best achievable margin.
Usage: python3 boundary_minbad.py seed m iters [TGT] [BND]"""
import sys, json
import numpy as np
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3')
from fastlib import tau_star_f, classes_f, pair_margin_f, fano_margin_f, superheavy_margin, general_margin_vec
from badcheck import load_supports

seed, m, iters = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
TGT = float(sys.argv[4]) if len(sys.argv) > 4 else 0.7505
BND = float(sys.argv[5]) if len(sys.argv) > 5 else 0.01
rng = np.random.default_rng(seed)
SUP = load_supports() if m <= 6 else None


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


def ok(x, K):
    K = np.asarray(K)
    if not ((x >= 0.02).all() and (x < 1.5).all()):
        return False
    if superheavy_margin(K, x) < 1e-3:
        return False
    g = K[0]
    if not (2 * x[0] / 3 + 1e-3 <= g[0] <= 2 * x[0] / 3 + BND):
        return False
    if not (g[1] <= 2 * x[1] / 3 - 1e-3 and g[2] <= 2 * x[2] / 3 - 1e-3):
        return False
    return True


def badness(x, K):
    return min(fano_margin_f(K, x), pair_margin_f(K, x))


best_overall = (-np.inf, None)
for restart in range(10 ** 6):
    for _ in range(50000):
        x = rng.uniform(0.05, 1.45, 3)
        K = []
        c = rng.random(3) * 0.4; c[0] = 2 * x[0] / 3 + rng.uniform(1e-3, BND)
        K.append(proj(c, x))
        for _k in range(m - 1):
            i = rng.integers(3); c = rng.random(3) * 0.4; c[i] = rng.uniform(0.55, 1.0); K.append(proj(c, x))
        if any(c is None for c in K):
            continue
        if ok(x, K) and tau_star_f(np.array(K), x) >= TGT:
            break
    else:
        print('no valid start', flush=True); continue
    K = np.array(K)
    cur = badness(x, K)
    step = 0.05
    for it in range(iters):
        nx = x.copy(); nK = K.copy()
        r = rng.random()
        if r < 0.2:
            i = rng.integers(3); nx[i] += rng.normal(0, step)
        else:
            j = rng.integers(m); c = proj(nK[j] + rng.normal(0, step, 3), nx)
            if c is None:
                continue
            nK[j] = c
        nKl = [proj(c, nx) for c in nK]
        if any(c is None for c in nKl) or not ok(nx, nKl) or tau_star_f(np.array(nKl), nx) < TGT:
            continue
        nK = np.array(nKl)
        b = badness(nx, nK)
        if b >= cur - 1e-4 * rng.random():
            x, K, cur = nx, nK, b
        if it % 3000 == 2999:
            step *= 0.8
    g = general_margin_vec(K, x, SUP) if SUP is not None else None
    print('restart %d badness %.4f (fano %.4f pair %.4f general %s) tau* %.4f x %s classes %s g0-2x0/3 %.4f' % (
        restart, cur, fano_margin_f(K, x), pair_margin_f(K, x), None if g is None else round(float(g), 4),
        tau_star_f(K, x), np.round(x, 4).tolist(), [list(map(int, s)) for s in classes_f(K, x)], K[0][0] - 2 * x[0] / 3), flush=True)
    print('   K', np.round(K, 5).tolist(), flush=True)
    tot = cur if g is None else min(cur, g)
    if tot > best_overall[0]:
        best_overall = (tot, (x.tolist(), K.tolist()))
        json.dump({'badness': float(tot), 'x': x.tolist(), 'K': K.tolist(), 'tau': float(tau_star_f(K, x))},
                  open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/logs/boundary_%d_%d.json' % (seed, m), 'w'))
