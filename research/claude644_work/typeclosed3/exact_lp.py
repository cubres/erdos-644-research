"""Small exact LP solver (Fractions, dense tableau, Bland's rule) used to turn a numerical Motzkin certificate
support into an exact certificate.  Solves  max c.x  s.t.  A x = b (b >= 0 after sign flips), x >= 0."""
from fractions import Fraction as F


def simplex_eq(A, b, c, maxit=10000):
    """max c.x s.t. A x = b, x >= 0.  Returns (status, x, value); status 'opt' | 'infeasible' | 'unbounded'."""
    m = len(A); n = len(A[0]) if m else 0
    A = [[F(v) for v in row] for row in A]; b = [F(v) for v in b]; c = [F(v) for v in c]
    for i in range(m):
        if b[i] < 0:
            A[i] = [-v for v in A[i]]; b[i] = -b[i]
    # phase 1: artificials n..n+m-1
    T = [A[i] + [F(1) if j == i else F(0) for j in range(m)] + [b[i]] for i in range(m)]
    basis = [n + i for i in range(m)]
    N = n + m

    def pivot(r, col):
        pv = T[r][col]; T[r] = [v / pv for v in T[r]]
        for i in range(m):
            if i != r and T[i][col] != 0:
                f = T[i][col]; T[i] = [a - f * bb for a, bb in zip(T[i], T[r])]
        basis[r] = col

    def run(obj, allowed):
        for _ in range(maxit):
            # reduced costs: obj_j - sum_i obj_{basis_i} T[i][j]
            cb = [obj[basis[i]] for i in range(m)]
            enter = None
            for j in allowed:
                if j in basis: continue
                rc = obj[j] - sum(cb[i] * T[i][j] for i in range(m))
                if rc > 0: enter = j; break
            if enter is None: return 'opt'
            best = None
            for i in range(m):
                if T[i][enter] > 0:
                    ratio = T[i][-1] / T[i][enter]
                    if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                        best = (ratio, i)
            if best is None: return 'unbounded'
            pivot(best[1], enter)
        return 'maxit'
    obj1 = [F(0)] * n + [F(-1)] * m
    st = run(obj1, list(range(N)))
    if sum(T[i][-1] for i in range(m) if basis[i] >= n) != 0:
        return 'infeasible', None, None
    # drive artificials out of basis where possible
    for i in range(m):
        if basis[i] >= n:
            for j in range(n):
                if T[i][j] != 0:
                    pivot(i, j); break
    obj2 = c + [F(0)] * m
    st = run(obj2, list(range(n)))
    if st != 'opt': return st, None, None
    x = [F(0)] * n
    for i in range(m):
        if basis[i] < n: x[basis[i]] = T[i][-1]
    return 'opt', x, sum(ci * xi for ci, xi in zip(c, x))


def motzkin(rows, VARS):
    """rows: (frozenset((var, F)), rhs F, strict bool) meaning coef.v >= rhs.  Find lam >= 0 with sum lam coef = 0,
    sum lam rhs >= 0, sum lam = 1, maximising sum lam (rhs + strict).  Returns lam (list of F) or None."""
    n = len(rows)
    used = sorted(set(k for co, rhs, s in rows for k, v in co))
    A = []; b = []
    for vname in used:
        A.append([dict(co).get(vname, F(0)) for co, rhs, s in rows] + [F(0)]); b.append(F(0))
    A.append([F(1)] * n + [F(0)]); b.append(F(1))
    A.append([rhs for co, rhs, s in rows] + [F(-1)]); b.append(F(0))     # sum lam rhs - slack = 0, slack >= 0
    c = [rhs + (1 if s else 0) for co, rhs, s in rows] + [F(0)]
    st, x, val = simplex_eq(A, b, c)
    if st != 'opt' or val <= 0: return None
    return x[:n]
