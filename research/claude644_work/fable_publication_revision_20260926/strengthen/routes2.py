"""Generalisation of routes.py: trace constraints are a list of forbidden intervals
(lo,hi] (a trace of the response on E, F or G may not lie in any of them).
The finisher dichotomy is forbidden=[(M,1/2)]; Stage 2 uses [(A,B)]; Stage 3 uses
[(A,B),(L,C)]; Stage 1 uses [] (no information).
Also allows a subset of routes and an arbitrary first request d.
"""
import numpy as np, random, time
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
from cells import cover, cellname, triple_config
from routes import position, CELLS6, fmt, BIG, X, Y, Z, PE, PF, PG

EPSH = 1e-5


def trace_ok(h, forbidden):
    if sum(h.values()) > 1 + 1e-9:
        return False
    for bit in (1, 2, 4):
        tr = sum(v for c, v in h.items() if c & bit)
        for lo, hi in forbidden:
            if lo + 1e-9 < tr < hi + EPSH:
                return False
    return True


def repair(h, cells, forbidden):
    for bit in (1, 2, 4):
        tr = sum(h[c] for c in cells if c & bit)
        for lo, hi in forbidden:
            if lo < tr < hi + EPSH:
                f = lo / tr if tr > 0 else 0.0
                for c in cells:
                    if c & bit:
                        h[c] *= f
    return h


def solve_multi2(config, d, t, forbidden, routes=('alpha', 'betaE', 'betaF', 'betaG'), iters=80,
                 tol=2e-5, verbose=False, init=None, stop_below=None, stop_above=None):
    cells = [c for c in CELLS6 if config[c] - d.get(c, 0.0) > 1e-12]
    avail = {c: config[c] - d.get(c, 0.0) for c in cells}
    n = len(cells); ci = {c: i for i, c in enumerate(cells)}
    pool = []
    best = (-1.0, None, None)
    pts = [] if init is None else [dict(p) for p in init]
    pts.append({c: min(avail[c], 1.0 / max(1, n)) for c in cells})
    for c in cells:
        hh = {c2: 0.0 for c2 in cells}; hh[c] = min(avail[c], 0.999); pts.append(hh)
    for hh in pts:
        hh = {c: hh.get(c, 0.0) for c in cells}
        if not trace_ok(hh, forbidden):
            continue
        v, vals, cols = position(config, d, hh, routes)
        for r, col in cols.items():
            pool.append(col)
        if v > best[0]:
            best = (v, hh, vals)
    lam = None
    nf = len(forbidden)
    for it in range(iters):
        nq = [len(col) for col in pool]; nu = sum(nq)
        nb = 3 * nf
        nv = n + nb + nu + 1
        LAM = nv - 1
        rows, cols_, vals_, lb, ub = [], [], [], [], []
        k = [0]
        def add(coefs, lo, hi):
            for v, a in coefs:
                rows.append(k[0]); cols_.append(v); vals_.append(a)
            lb.append(lo); ub.append(hi); k[0] += 1
        add([(i, 1.0) for i in range(n)], -np.inf, 1.0)
        for e, bit in enumerate((1, 2, 4)):
            coefs = [(ci[c], 1.0) for c in cells if c & bit]
            if not coefs:
                continue
            for fi, (lo, hi) in enumerate(forbidden):
                b = n + e * nf + fi
                add(coefs + [(b, -BIG)], -np.inf, lo)
                add(coefs + [(b, -BIG)], hi + EPSH - BIG, np.inf)
        off = n + nb
        for j, col in enumerate(pool):
            us = []
            for q, (const, coefs) in enumerate(col):
                u = off; off += 1; us.append(u)
                add([(LAM, 1.0)] + [(ci[c], -a) for c, a in coefs.items() if c in ci] + [(u, BIG)],
                    -np.inf, const + BIG)
            add([(u, 1.0) for u in us], 1.0, np.inf)
        A = coo_matrix((vals_, (rows, cols_)), shape=(k[0], nv)).tocsr()
        cvec = np.zeros(nv); cvec[LAM] = -1.0
        integ = np.zeros(nv); integ[n:nv - 1] = 1
        lo_ = np.zeros(nv); hi_ = np.ones(nv)
        for c in cells:
            hi_[ci[c]] = avail[c]
        hi_[LAM] = BIG
        res = milp(c=cvec, constraints=LinearConstraint(A, np.array(lb), np.array(ub)),
                   integrality=integ, bounds=Bounds(lo_, hi_), options={'disp': False})
        if res.x is None or res.status != 0:
            raise RuntimeError(res.message)
        lam = float(res.x[LAM])
        hstar = {c: float(min(max(res.x[ci[c]], 0.0), avail[c])) for c in cells}
        if not trace_ok(hstar, forbidden):
            hstar = repair(hstar, cells, forbidden)
        v, vals, cols = position(config, d, hstar, routes)
        if v > best[0]:
            best = (v, hstar, vals)
        if verbose:
            print('  it %d lam=%.5f pos(h*)=%.5f %s best=%.5f' % (
                it, lam, v, {r: round(x, 4) for r, x in vals.items()}, best[0]), flush=True)
        if v >= lam - tol:
            break
        if stop_below is not None and lam <= stop_below:
            break
        if stop_above is not None and best[0] >= stop_above:
            break
        for r, col in cols.items():
            pool.append(col)
    return {'ub': lam, 'lb': best[0], 'h': best[1], 'routes': best[2]}


def verdict(r, t):
    if r['ub'] <= t + 1e-6:
        return 'CLOSES'
    if r['lb'] > t + 1e-6:
        return 'FAILS'
    return 'open'


if __name__ == '__main__':
    import sys
    x, y, z, t = 0.4275, 0.357, 0.14, 0.855
    cfg = triple_config(x, y, z)
    d = {Y: y, Z: z, X: t - y - z}
    t0 = time.time()
    r = solve_multi2(cfg, d, t, [(x, 0.5)])
    print('dichotomy only : lb=%.5f ub=%.5f h=%s routes=%s (%.0fs)' % (r['lb'], r['ub'], fmt(r['h']),
          {k: round(v, 4) for k, v in r['routes'].items()}, time.time() - t0), flush=True)
    A = 3 - 3 * t; B = (4 * t - 2) / 3; C = t - 0.5; D = 2 - t - 2 * B; L = D - 1e-4
    t0 = time.time()
    r = solve_multi2(cfg, d, t, [(x, 0.5), (L, C)])
    print('with stage-2 gap (L,C]=(%.4f,%.4f]: lb=%.5f ub=%.5f h=%s routes=%s (%.0fs)' % (L, C, r['lb'], r['ub'], fmt(r['h']),
          {k: round(v, 4) for k, v in r['routes'].items()}, time.time() - t0), flush=True)
