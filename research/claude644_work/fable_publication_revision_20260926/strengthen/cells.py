"""Mask-based cell machinery for adaptive closure games (normalized k=1).

Edges are indexed 0..ne-1 (0=E,1=F,2=G,3=H,4=I). A cell is the set of points whose
edge-membership is exactly a bitmask. A configuration is a dict mask -> mass.
Candidate pairs (2-point transversals of the current edge set) are pairs of cells
(c,c') with c|c' == full. Points in no cell of positive mass adjacency are irrelevant.

cover(config, full, r): exact minimum max-load of r static requests covering all
candidate pairs (continuous relaxation; MILP with label indicators). Discovery only.
"""
import itertools, functools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix

E, F, G, H, I = 1, 2, 4, 8, 16
NAME = {1: 'PE', 2: 'PF', 4: 'PG', 3: 'X', 5: 'Y', 6: 'Z'}


def cellname(m):
    s = ''.join(n for b, n in [(1, 'E'), (2, 'F'), (4, 'G'), (8, 'H'), (16, 'I')] if m & b)
    return s or 'out'


def triple_config(x, y, z):
    return {3: x, 5: y, 6: z, 1: 1 - x - y, 2: 1 - x - z, 4: 1 - y - z}


def relevant(config, full, eps=1e-12):
    cells = [c for c, m in config.items() if m > eps]
    nb = {c: [d for d in cells if (c | d) == full and d != c] for c in cells}
    return [c for c in cells if nb[c]], nb


@functools.lru_cache(maxsize=200000)
def _cover_cached(items, full, r):
    return _cover(dict(items), full, r, False)[0]


def cover(config, full, r, want_solution=False, eps=1e-12, digits=9):
    if not want_solution:
        items = tuple(sorted((c, round(m, digits)) for c, m in config.items() if m > eps))
        return _cover_cached(items, full, r)
    return _cover(config, full, r, True)


STRUCT = 1e-4   # cells with mass <= STRUCT are structural: need a label, carry no load


def _cover(config, full, r, want_solution, eps=1e-12):
    cells, nb = relevant(config, full, eps)
    if not cells:
        return (0.0, {}) if want_solution else (0.0, None)
    labels = [frozenset(s) for m in range(1, r + 1) for s in itertools.combinations(range(r), m)]
    L = len(labels)
    n = len(cells)
    ci = {c: i for i, c in enumerate(cells)}
    heavy = [c for c in cells if config[c] > STRUCT]
    # variables: w[i,l] (n*L, only meaningful for heavy), s[i,l] (n*L), tau
    nv = 2 * n * L + 1
    W = lambda i, l: i * L + l
    S = lambda i, l: n * L + i * L + l
    tau = 2 * n * L
    rows, cols, vals, lb, ub = [], [], [], [], []
    k = 0
    def add(coefs, lo, hi):
        nonlocal k
        for v, a in coefs:
            rows.append(k); cols.append(v); vals.append(a)
        lb.append(lo); ub.append(hi); k += 1
    for c in cells:
        i = ci[c]; m = config[c]
        if c in heavy:
            add([(W(i, l), 1.0) for l in range(L)], m, m)
            for l in range(L):
                add([(W(i, l), 1.0), (S(i, l), -m)], -np.inf, 0.0)
        else:
            add([(S(i, l), 1.0) for l in range(L)], 1.0, np.inf)
    done = set()
    for c in cells:
        for d in nb[c]:
            if (d, c) in done:
                continue
            done.add((c, d))
            i, j = ci[c], ci[d]
            for l in range(L):
                for l2 in range(L):
                    if not (labels[l] & labels[l2]):
                        add([(S(i, l), 1.0), (S(j, l2), 1.0)], -np.inf, 1.0)
    for q in range(r):
        coefs = [(tau, -1.0)]
        for c in heavy:
            i = ci[c]
            for l in range(L):
                if q in labels[l]:
                    coefs.append((W(i, l), 1.0))
        add(coefs, -np.inf, 0.0)
    A = coo_matrix((vals, (rows, cols)), shape=(k, nv)).tocsr()
    cvec = np.zeros(nv); cvec[tau] = 1.0
    integ = np.zeros(nv); integ[n * L:2 * n * L] = 1
    lo = np.zeros(nv); hi = np.full(nv, np.inf); hi[n * L:2 * n * L] = 1.0
    for c in cells:
        if c not in heavy:
            for l in range(L):
                hi[W(ci[c], l)] = 0.0
    res = milp(c=cvec, constraints=LinearConstraint(A, np.array(lb), np.array(ub)),
               integrality=integ, bounds=Bounds(lo, hi), options={'disp': False, 'mip_rel_gap': 1e-7})
    if res.x is None or res.status != 0:
        raise RuntimeError('milp status %s: %s' % (res.status, res.message))
    val = float(res.x[tau])
    if not want_solution:
        return val, None
    sol = {}
    for c in cells:
        i = ci[c]
        m = config[c]
        if c in heavy:
            ws = [max(0.0, float(res.x[W(i, l)])) for l in range(L)]
        else:
            allowed = [l for l in range(L) if res.x[S(i, l)] > 0.5]
            ws = [m / len(allowed) if l in allowed else 0.0 for l in range(L)]
        for l in range(L):
            if ws[l] > 0:
                sol.setdefault(cellname(c), []).append((tuple(sorted(labels[l])), ws[l]))
    return val, sol


def traces(config, ne):
    """trace of the last edge (bit ne-1) on each earlier edge."""
    last = 1 << (ne - 1)
    out = []
    for e in range(ne - 1):
        b = 1 << e
        out.append(sum(m for c, m in config.items() if (c & last) and (c & b)))
    return out


def respond(config, avail_mask_bit, amounts):
    """split config by a new edge: amounts dict cell->mass taken by new edge."""
    new = {}
    for c, m in config.items():
        a = amounts.get(c, 0.0)
        if m - a > 1e-12:
            new[c] = m - a
        if a > 1e-12:
            new[c | avail_mask_bit] = a
    priv = amounts.get(0, 0.0)
    if priv > 1e-12:
        new[avail_mask_bit] = new.get(avail_mask_bit, 0.0) + priv
    return new


if __name__ == '__main__':
    import sys, time
    cfg = triple_config(0.425, 0.36, 0.144)
    t0 = time.time()
    print('static4', cover(cfg, 7, 4), time.time() - t0)
    # NC hand response
    h = {3: 0.074, 1: 0.215, 2: 0.431}
    c4 = respond(cfg, H, h)
    t0 = time.time()
    print('after NC response, 3-cover', cover(c4, 15, 3, want_solution=True), time.time() - t0)
    t0 = time.time()
    print('after NC response, 2-cover', cover(c4, 15, 2, want_solution=True), time.time() - t0)
