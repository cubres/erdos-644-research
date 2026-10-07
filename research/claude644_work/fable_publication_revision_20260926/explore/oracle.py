"""Discovery oracle for closing good triples (normalized k=1).

Static cover: given cells (sizes) and a candidate-pair adjacency between cells,
find labels (subsets of the r final requests) so that adjacent cells get
cross-intersecting label sets, minimizing the maximum request load.
This is exact for the continuous (normalized) relaxation of a static cover.
Used for DISCOVERY only; no proof depends on it.
"""
import itertools, functools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

FULL3 = frozenset({0, 1, 2})
FULL4 = frozenset({0, 1, 2, 3})


def static_cover(sizes, adj, r, eps=1e-12, want_solution=False):
    """sizes: list of floats; adj: list of (i,j) i<j cell pairs that are candidate pairs.
    r: number of requests. returns min max load (float) [and solution]."""
    n = len(sizes)
    act = [i for i in range(n) if sizes[i] > eps]
    nbrs = {i: set() for i in act}
    for (i, j) in adj:
        if sizes[i] > eps and sizes[j] > eps:
            nbrs[i].add(j); nbrs[j].add(i)
    # cells with neighbours need a label; others can be empty (load 0)
    cells = [i for i in act if nbrs[i]]
    if not cells:
        return (0.0, {}) if want_solution else 0.0
    labels = [frozenset(s) for m in range(1, r + 1) for s in itertools.combinations(range(r), m)]
    L = len(labels)
    idx = {}
    nv = 0
    for c in cells:
        for li in range(L):
            idx[('w', c, li)] = nv; nv += 1
    for c in cells:
        for li in range(L):
            idx[('s', c, li)] = nv; nv += 1
    tau = nv; nv += 1
    rows = []  # (coeff dict, lb, ub)
    for c in cells:
        rows.append(({idx[('w', c, li)]: 1.0 for li in range(L)}, sizes[c], sizes[c]))
        for li in range(L):
            rows.append(({idx[('w', c, li)]: 1.0, idx[('s', c, li)]: -sizes[c]}, -np.inf, 0.0))
    done = set()
    for c in cells:
        for d in nbrs[c]:
            if (d, c) in done:
                continue
            done.add((c, d))
            for li in range(L):
                for lj in range(L):
                    if not (labels[li] & labels[lj]):
                        rows.append(({idx[('s', c, li)]: 1.0, idx[('s', d, lj)]: 1.0}, -np.inf, 1.0))
    for j in range(r):
        coef = {tau: -1.0}
        for c in cells:
            for li in range(L):
                if j in labels[li]:
                    coef[idx[('w', c, li)]] = 1.0
        rows.append((coef, -np.inf, 0.0))
    A = lil_matrix((len(rows), nv))
    lb = np.empty(len(rows)); ub = np.empty(len(rows))
    for k, (cd, l, u) in enumerate(rows):
        for v, a in cd.items():
            A[k, v] = a
        lb[k] = l; ub[k] = u
    cvec = np.zeros(nv); cvec[tau] = 1.0
    integ = np.zeros(nv)
    for c in cells:
        for li in range(L):
            integ[idx[('s', c, li)]] = 1
    lo = np.zeros(nv); hi = np.full(nv, np.inf)
    for c in cells:
        for li in range(L):
            hi[idx[('s', c, li)]] = 1.0
    res = milp(c=cvec, constraints=LinearConstraint(A.tocsr(), lb, ub), integrality=integ,
               bounds=Bounds(lo, hi), options={'disp': False})
    if res.x is None:
        raise RuntimeError(res.message)
    val = res.x[tau]
    if want_solution:
        sol = {}
        for c in cells:
            for li in range(L):
                w = res.x[idx[('w', c, li)]]
                if w > 1e-9:
                    sol.setdefault(c, []).append((tuple(sorted(labels[li])), w))
        return val, sol
    return val


# ---------- good triple geometry ----------
TRIPLE_CELLS = [frozenset({0, 1}), frozenset({0, 2}), frozenset({1, 2}),
                frozenset({0}), frozenset({1}), frozenset({2})]
NAMES = ['X', 'Y', 'Z', 'PE', 'PF', 'PG']


def triple_sizes(x, y, z):
    return [x, y, z, 1 - x - y, 1 - x - z, 1 - y - z]


def triple_static(x, y, z, r=4, want_solution=False):
    sizes = triple_sizes(x, y, z)
    adj = [(i, j) for i in range(6) for j in range(i + 1, 6)
           if TRIPLE_CELLS[i] | TRIPLE_CELLS[j] == FULL3]
    return static_cover(sizes, adj, r, want_solution=want_solution)


# sub-cells after a 4th edge H: index 2*c + b, b=1 means in H
SUB_LABELS = [TRIPLE_CELLS[c] | ({3} if b else set()) for c in range(6) for b in (0, 1)]
SUB_ADJ = [(i, j) for i in range(12) for j in range(i + 1, 12)
           if frozenset(SUB_LABELS[i]) | frozenset(SUB_LABELS[j]) == FULL4]
SUB_NAMES = [NAMES[c] + ('1' if b else '0') for c in range(6) for b in (0, 1)]


def after_response(x, y, z, h, want_solution=False):
    """h: list of 6 amounts of H in each triple cell. returns min max load of 3 final requests."""
    s = triple_sizes(x, y, z)
    sizes = []
    for c in range(6):
        sizes += [s[c] - h[c], h[c]]
    return static_cover(sizes, SUB_ADJ, 3, want_solution=want_solution)


if __name__ == '__main__':
    import sys
    print(triple_static(0.25, 0.25, 0.25))
    print(triple_static(3/7, 3/7, 0.0, want_solution=True))
    print(triple_static(0.5, 9/28, 9/28, want_solution=True))
