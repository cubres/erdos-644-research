"""Fixed-x climb: families K of m types with tau*(K) >= TGT, maximise min(Fano margin, 42-fn pair margin)
(> 0 = no Fano / two-type tuple).  usage: python3 climb_x.py x0 x1 x2 m iters seed [TGT=0.75]"""
import sys, numpy as np, json
sys.path.insert(0, '..')
from fastlib import tau_star_f, pair_margin_f, fano_margin_f
x = np.array([float(eval(a)) for a in sys.argv[1:4]]); m = int(sys.argv[4]); iters = int(sys.argv[5]); seed = int(sys.argv[6])
TGT = float(sys.argv[7]) if len(sys.argv) > 7 else 0.75
rng = np.random.default_rng(seed)
def proj(c):
    c = np.clip(c, 0, x)
    for _ in range(40):
        s = c.sum()
        if s <= 0: return None
        c = c / s
        if (c <= x + 1e-12).all(): return c
        c = np.minimum(c, x)
    return None
def score(K):
    t = tau_star_f(K, x)
    if t < TGT: return -10 + t, t
    return min(fano_margin_f(K, x), pair_margin_f(K, x)), t
best = (-np.inf, None, None)
for restart in range(1000):
    K = []
    while len(K) < m:
        i = rng.integers(3); c = rng.random(3) * 0.5; c[i] = rng.uniform(2 * x[i] / 3, x[i]); c = proj(c)
        if c is not None: K.append(c)
    K = np.array(K); sc, t = score(K); step = 0.05
    for it in range(iters):
        nK = K.copy(); j = rng.integers(m); c = proj(nK[j] + rng.normal(0, step, 3))
        if c is None: continue
        nK[j] = c; s2, t2 = score(nK)
        if s2 >= sc: K, sc, t = nK, s2, t2
        if it % 300 == 299: step = max(step * 0.7, 0.002)
    if sc > best[0]:
        best = (sc, K.tolist(), t)
        print('restart %d best margin %.4f tau* %.4f' % (restart, sc, t), flush=True)
        json.dump({'x': x.tolist(), 'margin': sc, 'tau': t, 'K': K.tolist()}, open('climb_x_%d.json' % seed, 'w'))
