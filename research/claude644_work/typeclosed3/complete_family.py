"""Family completion experiment: start from an adversary configuration (its valid roles as SEED types, fixed) and add m
free types; local search maximising  badness(K) = min over templates (F <= 3 distinct types, V, TT, K4) of the max
normalised violation, subject to tau*(K) >= tau_target (penalised).  If every completion has badness < 0 (some template
works), report which types are used and how they relate to the seeds (which request would produce them).
usage: python3 complete_family.py adv.json [m] [restarts] [seed]"""
import sys, json, itertools
import numpy as np
from roles3 import LINES, PATS, load_tt

TT = load_tt()


def tau_star_f(K, x):
    """float tau* by threshold enumeration (types blocked iff c_i >= t_i)."""
    p = 3; K = np.asarray(K)
    cands = [sorted(set(K[:, i][K[:, i] > 1e-12])) + [None] for i in range(p)]
    best = np.inf
    for t0 in cands[0]:
        for t1 in cands[1]:
            unb = np.ones(len(K), bool)
            if t0 is not None: unb &= K[:, 0] < t0 - 1e-12
            if t1 is not None: unb &= K[:, 1] < t1 - 1e-12
            if not unb.any():
                t2 = None
            else:
                m = K[unb, 2].min()
                if m <= 1e-12: continue
                t2 = m
            cost = sum(x[i] - t for i, t in enumerate((t0, t1, t2)) if t is not None)
            best = min(best, cost)
    return best


def badness(K, x, menu=('F', 'V', 'TT', 'K4'), maxk=3):
    K = np.asarray(K); n = len(K); best = np.inf; arg = None
    if 'F' in menu:
        for k in range(1, maxk + 1):
            for combo in itertools.combinations(range(n), k):
                for pat in PATS[k]:
                    pts = [combo[p] for p in pat]
                    z = K[pts]
                    w = np.max((z.sum(0) - 4 * x) / x)
                    for l in LINES:
                        w = max(w, np.max((z[l[0]] + z[l[1]] + z[l[2]] - 2 * x) / x))
                    if w < best: best, arg = w, ('F',) + tuple(pts)
    for a in range(n):
        for b in range(n):
            if a == b: continue
            if 'V' in menu:
                v = np.max(np.maximum(K[a] + K[b], 1.25 * K[a] + 0.5 * K[b]) / x - 1)
                if v < best: best, arg = v, ('V', a, b)
            if 'TT' in menu:
                for fn, vs in enumerate(TT):
                    v = max(np.max((u * K[a] + w * K[b]) / x - 1) for u, w in vs)
                    if v < best: best, arg = v, ('TT', a, b, fn)
    if 'K4' in menu:
        for g in range(n):
            for a, b, c in itertools.combinations([j for j in range(n) if j != g], 3):
                A_, B_, C_ = K[a], K[b], K[c]
                v = max(np.max((A_ - B_ - C_) / x), np.max((B_ - A_ - C_) / x), np.max((C_ - A_ - B_) / x),
                        np.max((K[g] + 0.5 * (A_ + B_ + C_)) / x - 1))
                if v < best: best, arg = v, ('K4', g, a, b, c)
    return best, arg


def project(c, x):
    """project onto the simplex {0 <= c <= x, |c| = 1} (approximate: clip then renormalise a few times)"""
    c = np.clip(c, 0, x)
    for _ in range(20):
        s = c.sum()
        if abs(s - 1) < 1e-12: break
        free = (c > 1e-12) if s > 1 else (c < x - 1e-12)
        if not free.any(): break
        c[free] += (1 - s) / free.sum()
        c = np.clip(c, 0, x)
    return c


def climb(seeds, x, m, tau_t, rng, iters=3000, verbose=False):
    seeds = np.asarray(seeds); x = np.asarray(x)
    F = np.array([project(rng.uniform(0, x), x) for _ in range(m)])

    def obj(F):
        K = np.vstack([seeds, F])
        b, arg = badness(K, x)
        ts = tau_star_f(K, x)
        return b - 50 * max(0.0, tau_t - ts), b, ts, arg
    cur, b, ts, arg = obj(F); step = 0.1
    for it in range(iters):
        G = F.copy(); j = rng.integers(m)
        G[j] = project(G[j] + rng.normal(0, step, 3), x)
        if rng.random() < 0.1:
            G[j] = project(rng.uniform(0, x), x)
        val, b2, ts2, arg2 = obj(G)
        if val >= cur:
            F, cur, b, ts, arg = G, val, b2, ts2, arg2
        if it % 500 == 499:
            step *= 0.7
            if verbose: print('  it', it, 'obj %.4f badness %.4f tau* %.4f' % (cur, b, ts), arg, flush=True)
    return F, cur, b, ts, arg


if __name__ == '__main__':
    sol = json.load(open(sys.argv[1]))
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    x = np.array(sol['x']); tau_t = sol['tau']
    valid = [q is None or q == 1 for q in sol['Q']]
    seeds = [sol['roles'][j] for j in range(len(sol['roles'])) if valid[j]]
    print('x', x, 'tau target', tau_t, 'seeds', len(seeds), 'badness(seeds) %.4f tau*(seeds) %.4f' % (badness(seeds, x)[0], tau_star_f(seeds, x)))
    rng = np.random.default_rng(seed)
    best = None
    for r in range(restarts):
        F, cur, b, ts, arg = climb(seeds, x, m, tau_t, rng, verbose=True)
        print('restart', r, 'obj %.4f badness %.4f tau* %.4f' % (cur, b, ts), arg, flush=True)
        if best is None or cur > best[1]:
            best = (F, cur, b, ts, arg)
    F, cur, b, ts, arg = best
    K = np.vstack([seeds, F])
    print('BEST badness %.4f tau* %.4f template %s' % (b, ts, arg))
    for j, c in enumerate(K):
        print(' type', j, np.round(c, 4), 'seed' if j < len(seeds) else 'free', 'superheavy at', [i for i in range(3) if c[i] > 2 * x[i] / 3])
    json.dump({'x': x.tolist(), 'K': K.tolist(), 'nseeds': len(seeds), 'badness': float(b), 'tau': float(ts), 'arg': [str(a) for a in arg]},
              open(sys.argv[1].replace('.json', '_completed.json'), 'w'))
