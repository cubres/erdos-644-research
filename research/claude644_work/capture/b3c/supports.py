"""General bad supports: a support is a family of cells (subsets of the 7 rows, bitmasks) no two of which
(possibly equal) cover all 7 rows.  Capacity: loads l (7-vector) fit in a part of capacity x iff
w.l <= x for every vertex w of P_D = {w >= 0 : w(C) <= 1 for every cell C} (LP duality).
Exact vertex enumeration: brute force over 7-subsets of tight constraints (standard library + Fraction)."""
from fractions import Fraction as F
import itertools
FULL = 127
def is_bad(cells):
    cs = list(cells)
    return all((a | b) != FULL for a in cs for b in cs)
def maximal_extension(cells):
    fam = set()
    for C in cells:                      # downset closure not needed for maximal cells; keep given
        fam.add(C)
    assert is_bad(fam)
    for S in sorted(range(FULL), key=lambda s: -bin(s).count('1')):
        if S in fam: continue
        if (S | S) == FULL: continue
        if all((S | C) != FULL for C in fam): fam.add(S)
    # maximal cells
    mx = [S for S in fam if not any(S != T and (S & T) == S for T in fam)]
    return tuple(sorted(mx))
def solve_exact(A, b):
    """solve square system A w = b exactly; None if singular"""
    n = len(A); M = [list(map(F, A[i])) + [F(b[i])] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return None
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]; M[c] = [v / pv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [a - f*bb for a, bb in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]
def constraints_of(maxcells):
    rows = []
    for C in maxcells: rows.append(([1 if C >> j & 1 else 0 for j in range(7)], 1))
    for j in range(7): rows.append(([-1 if i == j else 0 for i in range(7)], 0))
    return rows
def vertices_exact(maxcells):
    rows = constraints_of(maxcells)
    V = set()
    for S in itertools.combinations(range(len(rows)), 7):
        w = solve_exact([rows[r][0] for r in S], [rows[r][1] for r in S])
        if w is None: continue
        if all(sum(a*v for a, v in zip(rows[r][0], w)) <= rows[r][1] for r in range(len(rows))):
            V.add(tuple(w))
    return sorted(V)
def vertices_check_candidates(maxcells, cand):
    """cheap exact check that each candidate is a vertex (7 lin. indep. tight constraints, feasible)"""
    rows = constraints_of(maxcells); ok = []
    for w in cand:
        if not all(sum(a*v for a, v in zip(r[0], w)) <= r[1] for r in rows): return False
        tight = [r[0] for r in rows if sum(a*v for a, v in zip(r[0], w)) == r[1]]
        if rank(tight) < 7: return False
    return True
def rank(Ms):
    M = [list(map(F, r)) for r in Ms]; rk = 0; ncol = 7
    for c in range(ncol):
        p = next((r for r in range(rk, len(M)) if M[r][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for r in range(len(M)):
            if r != rk and M[r][c] != 0:
                f = M[r][c] / M[rk][c]; M[r] = [a - f*b for a, b in zip(M[r], M[rk])]
        rk += 1
    return rk
