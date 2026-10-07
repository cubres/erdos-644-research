"""[typeclosed#1] referee library: exact cover LP (own Fraction simplex), supports (Fano, V), exact tau* of finite type sets.
All results are re-verified exactly (primal cover checked coordinatewise), so the simplex is only a search tool."""
from fractions import Fraction as F
from itertools import combinations, product

FULL = frozenset(range(7))
# Fano plane on points 0..6; lines indexed 0..6. Pencil at point 0 = lines 0,1,2.
LINES = [frozenset(s) for s in ({0, 1, 2}, {0, 3, 4}, {0, 5, 6}, {1, 3, 5}, {1, 4, 6}, {2, 3, 6}, {2, 4, 5})]
FANO_CELLS = [frozenset(l for l in range(7) if q not in LINES[l]) for q in range(7)]   # rows = lines; cell = lines missing q
PENCIL = [l for l in range(7) if 0 in LINES[l]]
QUAD = [l for l in range(7) if 0 not in LINES[l]]
# V support (templates agent), rows 0,1 = b-rows (t), rows 2..6 = a-rows (s)
V_CELLS = [frozenset({0, 1})] + [frozenset(c) for c in combinations([2, 3, 4, 5, 6], 4)] + \
          [frozenset(c) for c in ({0, 3, 4, 6}, {0, 2, 5, 6}, {1, 2, 4, 6}, {1, 3, 5, 6})]

def is_support(cells):
    cs = list(cells)
    return all((a | b) != FULL for a in cs for b in cs)

def simplex_max(c, A, b):
    """max c.w s.t. A w <= b, w >= 0, b >= 0.  Exact, Bland's rule.  Returns (value, w, y) with y the dual (>=0)."""
    m, n = len(A), len(c)
    T = [list(map(F, A[i])) + [F(1) if k == i else F(0) for k in range(m)] + [F(b[i])] for i in range(m)]
    obj = [-F(v) for v in c] + [F(0)] * m + [F(0)]
    basis = [n + i for i in range(m)]
    while True:
        enter = next((j for j in range(n + m) if obj[j] < 0), None)
        if enter is None: break
        best = None
        for i in range(m):
            if T[i][enter] > 0:
                r = T[i][-1] / T[i][enter]
                if best is None or r < best[0] or (r == best[0] and basis[i] < basis[best[1]]): best = (r, i)
        if best is None: raise ValueError('unbounded')
        _, piv = best
        pv = T[piv][enter]; T[piv] = [v / pv for v in T[piv]]
        for i in range(m):
            if i != piv and T[i][enter] != 0:
                f = T[i][enter]; T[i] = [vi - f * vp for vi, vp in zip(T[i], T[piv])]
        f = obj[enter]; obj = [vo - f * vp for vo, vp in zip(obj, T[piv])]
        basis[piv] = enter
    w = [F(0)] * n
    for i, bi in enumerate(basis):
        if bi < n: w[bi] = T[i][-1]
    y = [obj[n + i] for i in range(m)]
    return obj[-1], w, y

def cover(cells, loads):
    """Exact min total mass on cells covering loads (rows 0..6).  Returns (value, masses) and asserts optimality
    certificate (primal feasible, dual feasible, equal objective)."""
    cells = list(cells)
    A = [[1 if r in c else 0 for r in range(7)] for c in cells]
    val, w, y = simplex_max(loads, A, [1] * len(cells))
    # primal z = y: check z covers loads and sum z = val
    for r in range(7):
        assert sum(y[i] for i, c in enumerate(cells) if r in c) >= F(loads[r]), 'primal infeasible?'
    assert sum(y) == val and all(v >= 0 for v in y)
    for i, c in enumerate(cells):
        assert sum(w[r] for r in c) <= 1
    assert sum(F(loads[r]) * w[r] for r in range(7)) == val
    return val, y

def rows_Qb(a, b):   # b on the pencil at 0, a on the quadrilateral
    return [b if l in PENCIL else a for l in range(7)]

def rows_Qa(a, b):
    return [a if l in PENCIL else b for l in range(7)]

def rows_V(a, b):
    return [b, b, a, a, a, a, a]

def template_ok(name, a, b, x):
    """Exact per-part check with the actual support: every part's cover value <= x_i."""
    cells = V_CELLS if name == 'V' else FANO_CELLS
    rf = {'Qb': rows_Qb, 'Qa': rows_Qa, 'V': rows_V}[name]
    return all(cover(cells, rf(a[i], b[i]))[0] <= x[i] for i in range(len(x)))

def hom_fano_ok(c, x):
    return all(cover(FANO_CELLS, [c[i]] * 7)[0] <= x[i] for i in range(len(x)))

def tau_star(types, x):
    """Exact tau* of a finite type set: min over threshold choices theta_i in {positive a_i values} or None
    (u_i = theta_i - eps, cost x_i - theta_i + eps) such that every type is blocked (a_i >= theta_i for some i)."""
    p = len(x)
    opts = []
    for i in range(p):
        vals = sorted({t[i] for t in types if t[i] > 0})
        opts.append([None] + vals)
    best = None
    for th in product(*opts):
        if all(any(th[i] is not None and t[i] >= th[i] for i in range(p)) for t in types):
            cost = sum(x[i] - th[i] for i in range(p) if th[i] is not None)
            if best is None or cost < best: best = cost
    if best is None:   # no blocking choice: sup sum u = N ... impossible unless some type is 0 -> tau*=... treat as 0
        best = F(0)
    return best
