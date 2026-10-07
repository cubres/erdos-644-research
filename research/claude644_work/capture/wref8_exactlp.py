#!/usr/bin/env python3
"""wref8: independent exact rational feasibility LP (two-phase simplex, Bland's rule, Fractions only).
feasible(nv, ub_rows, eq_rows, lb, ubv) with rows given as (dict{var:coef}, rhs):
   ub rows:  sum coef*v <= rhs ;  eq rows: sum coef*v == rhs ; lb[v] <= v (<= ubv[v] if not None).
Returns ('FEAS', point) with the point re-verified exactly, or ('INFEAS', y) with a verified Farkas vector.
No floats anywhere."""
from fractions import Fraction as F

def feasible(nv, ub_rows, eq_rows, lb=None, ubv=None):
    lb = lb or [F(0)] * nv
    ubv = ubv or [None] * nv
    rows = []  # (coef dict over shifted vars z = v - lb, rhs, kind)
    allub = list(ub_rows) + [({j: F(1)}, ubv[j]) for j in range(nv) if ubv[j] is not None]
    for coef, rhs in allub:
        r = F(rhs) - sum(F(c) * lb[j] for j, c in coef.items())
        rows.append(({j: F(c) for j, c in coef.items()}, r, 'ub'))
    for coef, rhs in eq_rows:
        r = F(rhs) - sum(F(c) * lb[j] for j, c in coef.items())
        rows.append(({j: F(c) for j, c in coef.items()}, r, 'eq'))
    m = len(rows)
    nslack = sum(1 for r in rows if r[2] == 'ub')
    ncol = nv + nslack + m
    T = []
    si = 0
    for i, (coef, r, kind) in enumerate(rows):
        row = [F(0)] * (ncol + 1)
        for j, c in coef.items(): row[j] = c
        if kind == 'ub':
            row[nv + si] = F(1); si += 1
        row[ncol] = r
        if r < 0: row = [-v for v in row]
        row[nv + nslack + i] = F(1)
        T.append(row)
    basis = [nv + nslack + i for i in range(m)]
    cost = [F(0)] * (nv + nslack) + [F(1)] * m
    # objective row: reduced costs  c_j - c_B B^-1 A_j
    obj = [cost[j] - sum(T[i][j] for i in range(m)) for j in range(ncol)] + [-sum(T[i][ncol] for i in range(m))]
    while True:
        ent = next((j for j in range(ncol) if obj[j] < 0), None)
        if ent is None: break
        best = None
        for i in range(m):
            if T[i][ent] > 0:
                ratio = T[i][ncol] / T[i][ent]
                if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        if best is None: raise RuntimeError('unbounded phase 1 (impossible)')
        i = best[1]; pv = T[i][ent]
        T[i] = [v / pv for v in T[i]]
        for k in range(m):
            if k != i and T[k][ent] != 0:
                f = T[k][ent]; T[k] = [a - f * b for a, b in zip(T[k], T[i])]
        if obj[ent] != 0:
            f = obj[ent]; obj = [a - f * b for a, b in zip(obj, T[i])]
        basis[i] = ent
    val = -obj[ncol]
    if val == 0:
        z = [F(0)] * ncol
        for i, b in enumerate(basis): z[b] = T[i][ncol]
        pt = [z[j] + lb[j] for j in range(nv)]
        assert check_point(pt, ub_rows, eq_rows, lb, ubv), 'witness failed exact recheck'
        return 'FEAS', pt
    # Farkas: y_i = c_B B^-1 e_i ; artificial column i of final tableau is B^-1 e_i (sign-flipped rows handled)
    y = []
    for i in range(m):
        col = nv + nslack + i
        y.append(sum(cost[basis[r]] * T[r][col] for r in range(m)))
    # verify: for sign-normalised system M z (+slack) = b', z>=0: y^T M <= 0 on z and slack cols, y^T b' > 0
    sgn = [(-1 if rows[i][1] < 0 else 1) for i in range(m)]
    for j in range(nv + nslack):
        s = F(0); si = 0
        for i, (coef, r, kind) in enumerate(rows):
            if j < nv: a = coef.get(j, F(0))
            else:
                a = F(0)
            s += y[i] * sgn[i] * a
        if j >= nv:  # slack column
            k = j - nv; cnt = -1
            for i, (coef, r, kind) in enumerate(rows):
                if kind == 'ub':
                    cnt += 1
                    if cnt == k: s = y[i] * sgn[i]
        assert s <= 0, 'Farkas column check failed'
    assert sum(y[i] * sgn[i] * rows[i][1] for i in range(m)) > 0, 'Farkas rhs check failed'
    return 'INFEAS', y

def check_point(pt, ub_rows, eq_rows, lb, ubv):
    for j, v in enumerate(pt):
        if v < lb[j]: return False
        if ubv[j] is not None and v > ubv[j]: return False
    for coef, rhs in ub_rows:
        if sum(F(c) * pt[j] for j, c in coef.items()) > rhs: return False
    for coef, rhs in eq_rows:
        if sum(F(c) * pt[j] for j, c in coef.items()) != rhs: return False
    return True

if __name__ == '__main__':
    # self tests
    print(feasible(2, [({0: 1, 1: 1}, F(1))], [], [F(0), F(0)])[0])            # FEAS
    print(feasible(2, [({0: 1, 1: 1}, F(1))], [({0: 1}, F(2))])[0])            # INFEAS
    print(feasible(2, [({0: -1, 1: -1}, F(-3))], [], None, [F(1), F(1)])[0])   # INFEAS
    print(feasible(2, [({0: -1, 1: -1}, F(-3))], [], None, [F(2), F(1)])[0])   # FEAS
