"""Minimum-badness search restricted to case (B) of Theorem A1: K = S_0 u S_1 (every type super-heavy at part 0 or
part 1), S_2 nonempty, x_2 < 3/4, the class-0 and class-1 minimisers super-heavy at part 2; tau* >= TGT.
badness = min(fano, pair) during the climb; general margin at the end of each restart.
Usage: python3 caseB_minbad.py seed m iters [TGT]"""
import sys, json
import numpy as np
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3')
from fastlib import tau_star_f, classes_f, pair_margin_f, fano_margin_f, superheavy_margin, general_margin_vec
from badcheck import load_supports

seed, m, iters = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
TGT = float(sys.argv[4]) if len(sys.argv) > 4 else 0.7505
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


def caseB(x, K):
    K = np.asarray(K)
    if not ((x >= 0.02).all() and (x < 1.5).all() and x[2] < 0.75):
        return False
    sh = (K - 2 * x / 3) / x
    if (sh.max(1) < 1e-3).any():                       # every type strictly super-heavy somewhere
        return False
    if not ((sh[:, 0] >= 1e-3) | (sh[:, 1] >= 1e-3)).all():   # covered by classes 0,1
        return False
    if not (sh[:, 2] >= 1e-3).any():                   # S_2 nonempty
        return False
    for i in (0, 1):
        Si = np.where(sh[:, i] >= 1e-3)[0]
        if len(Si) == 0:
            return False
        mins = Si[K[Si, i] <= K[Si, i].min() + 1e-9]
        if not (sh[mins, 2] >= 1e-3).all():            # minimisers super-heavy at 2
            return False
    return True


def badness(x, K):
    return min(fano_margin_f(K, x), pair_margin_f(K, x))


best_overall = (-np.inf, None)
for restart in range(10 ** 6):
    for _ in range(50000):
        x = np.array([rng.uniform(1.15, 1.45), rng.uniform(1.15, 1.45), rng.uniform(0.02, 0.15)])
        K = []
        okstart = True
        for i in (0, 1):
            lo, hi = 2 * x[i] / 3 + 0.01, min(1.0, x[i]) - 2 * x[2] / 3 - 0.01
            if hi <= lo:
                okstart = False; break
            sig = rng.uniform(lo, hi)
            z = rng.uniform(2 * x[2] / 3 + 0.002, min(x[2], 1 - sig))
            c = np.zeros(3); c[i] = sig; c[2] = z; c[1 - i] = 1 - sig - z
            K.append(proj(c, x))
        if not okstart:
            continue
        for _k in range(m - 2):
            # two-cloud construction: a type near (1,0,.) or (0,1,.) with gamma >= sigma_i, third coordinate z
            i = rng.integers(2); sig_i = K[i][i]
            gam = rng.uniform(sig_i, min(1.0, x[i]))
            z = 0.0 if rng.random() < 0.5 else rng.uniform(0, min(x[2], 1 - gam))
            c = np.zeros(3); c[i] = gam; c[2] = z; c[1 - i] = 1 - gam - z
            K.append(proj(c, x))
        if any(c is None for c in K):
            continue
        if caseB(x, K) and tau_star_f(np.array(K), x) >= TGT:
            break
    else:
        print('no valid start'); continue
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
        if any(c is None for c in nKl) or not caseB(nx, nKl) or tau_star_f(np.array(nKl), nx) < TGT:
            continue
        nK = np.array(nKl)
        b = badness(nx, nK)
        if b >= cur - 1e-4 * rng.random():
            x, K, cur = nx, nK, b
        if it % 3000 == 2999:
            step *= 0.8
    g = general_margin_vec(K, x, SUP) if SUP is not None else None
    print('restart %d badness %.4f (fano %.4f pair %.4f general %s) tau* %.4f x %s classes %s' % (
        restart, cur, fano_margin_f(K, x), pair_margin_f(K, x), None if g is None else round(float(g), 4),
        tau_star_f(K, x), np.round(x, 4).tolist(), [list(map(int, s)) for s in classes_f(K, x)]), flush=True)
    print('   K', np.round(K, 5).tolist(), flush=True)
    tot = cur if g is None else min(cur, g)
    if tot > best_overall[0]:
        best_overall = (tot, (x.tolist(), K.tolist()))
        json.dump({'badness': float(tot), 'x': x.tolist(), 'K': K.tolist(), 'tau': float(tau_star_f(K, x))},
                  open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/logs/caseB_%d_%d.json' % (seed, m), 'w'))
