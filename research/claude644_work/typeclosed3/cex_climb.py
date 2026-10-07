"""Part B: strong counterexample search over FULL finite families over 3 parts.
Maximise tau*(K) subject to: no Fano tuple (all assignments, margin ETA), no two-type tuple (42 functions, margin ETA),
and (checked on improvement when tau* > GEN_FROM) no general bad tuple (715 supports, float margin).
Random local search with restarts; the best families are dumped to logs/cex_<seed>_<m>.json for exact verification.
Usage: python3 cex_climb.py seed m iters [gen_from]
"""
import sys, json, time
import numpy as np
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3')
from fastlib import tau_star_f, classes_f, pair_margin_f, fano_margin_f, superheavy_margin
from badcheck import load_supports, margin_general

seed, m, iters = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
GEN_FROM = float(sys.argv[4]) if len(sys.argv) > 4 else 0.735
ETA = 1e-4
rng = np.random.default_rng(seed)
SUP = load_supports()


def proj(c, x):
    c = np.maximum(c, 0)
    c = np.minimum(c, x)
    if c.sum() <= 0:
        return None
    for _ in range(30):
        c = c / c.sum()
        if (c <= x + 1e-12).all():
            return c
        c = np.minimum(c, x)
    return None


def constraints(x, K):
    """returns (ok, fano_margin, pair_margin)"""
    if (x < 0.02).any() or (x >= 1.5).any():
        return False, None, None
    fm = fano_margin_f(K, x)
    if fm < ETA:
        return False, fm, None
    pm = pair_margin_f(K, x)
    if pm < ETA:
        return False, fm, pm
    return True, fm, pm


def gen_check(x, K):
    t0 = time.time()
    g = margin_general(K, x, SUP)
    return g[0], g[1], time.time() - t0


best_overall = (-1, None)
for restart in range(1000):
    found = False
    for _ in range(5000):
        x = rng.uniform(0.05, 1.45, 3)
        K = []
        for _k in range(m):
            i = rng.integers(3)
            c = rng.random(3) * 0.3
            c[i] = rng.uniform(0.6, 1.0)
            K.append(proj(c, x))
        if any(c is None for c in K):
            continue
        K = np.array(K)
        ok, fm, pm = constraints(x, K)
        if ok:
            found = True
            break
    if not found:
        continue
    cur = tau_star_f(K, x)
    step = 0.05
    gen_ok_tau = -1     # largest tau* at which the general check passed for this restart
    for it in range(iters):
        nx = x.copy(); nK = K.copy()
        r = rng.random()
        if r < 0.2:
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
        nKl = [proj(c, nx) for c in nK]
        if any(c is None for c in nKl):
            continue
        nK = np.array(nKl)
        ok, fm, pm = constraints(nx, nK)
        if not ok:
            continue
        t = tau_star_f(nK, nx)
        if t >= cur - 1e-4 * rng.random():
            x, K, cur = nx, nK, t
        if it % 3000 == 2999:
            step *= 0.8
    # end of restart: general check if promising
    info = ''
    if cur > GEN_FROM:
        g, wit, dt = gen_check(x, K)
        info = ' GENERAL margin %.4f (%.0fs) wit %s' % (g, dt, wit)
        if g < ETA:
            info += ' -> general bad tuple exists (not a counterexample)'
    if cur > best_overall[0]:
        best_overall = (cur, (x.tolist(), K.tolist()))
    print('restart %d tau* %.4f x %s fm %.4f pm %.4f sh %.4f classes %s%s' % (restart, cur, np.round(x, 4).tolist(),
          fano_margin_f(K, x), pair_margin_f(K, x), superheavy_margin(K, x),
          [list(map(int, s)) for s in classes_f(K, x)], info), flush=True)
    print('   K', np.round(K, 5).tolist(), flush=True)
    json.dump({'tau': cur, 'x': x.tolist(), 'K': K.tolist(), 'general': info},
              open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/logs/cex_%d_%d_r%d.json' % (seed, m, restart), 'w'))
print('BEST', best_overall[0])
