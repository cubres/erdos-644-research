"""[typeclosed#2] referee library (independent of the attacker's code). Exact rationals throughout.
Model: p parts, capacities x (Fractions), finite closed type set C = list of tuples (c_i >= 0, c_i <= x_i, sum c <= 1).
tau*(C) = inf{ sum_i (x_i - u_i) : 0 <= u <= x, no c in C with c <= u }.
For finite C: tau* = min over threshold vectors t (t_i in {c_i : c in C, c_i > 0} or INF) such that every type c
has some i with c_i >= t_i, of sum_i (x_i - t_i) over finite t_i (u_i -> t_i from below)."""
from fractions import Fraction as F
from itertools import product

INF = None

def tau_star(C, x):
    p = len(x)
    if not C:
        return F(0), None
    cand = []
    for i in range(p):
        vals = sorted(set(c[i] for c in C if c[i] > 0))
        cand.append([INF] + vals)
    best = None; arg = None
    for t in product(*cand):
        ok = True
        for c in C:
            if not any(t[i] is not INF and c[i] >= t[i] for i in range(p)):
                ok = False; break
        if not ok:
            continue
        cost = sum((x[i] - t[i]) for i in range(p) if t[i] is not INF)
        if best is None or cost < best:
            best = cost; arg = t
    return best, arg

# Fano plane: points 0..6, lines
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]

def fano_ok(rows, x):
    """rows[l] = type placed on line l (l = 0..6). Lemma 7.63 criterion, exact. Rows are indexed by LINES; the
    'point' constraints of Lemma 7.63 are over triples of rows forming a line of the DUAL plane, i.e. the three
    lines through a common point."""
    p = len(x)
    pencils = [[l for l in range(7) if q in LINES[l]] for q in range(7)]
    for i in range(p):
        if any(r[i] > x[i] for r in rows):
            return False
        for pen in pencils:
            if sum(rows[l][i] for l in pen) > 2 * x[i]:
                return False
        if sum(r[i] for r in rows) > 4 * x[i]:
            return False
    return True

def _scale(C, x):
    from math import lcm
    L = 1
    for v in list(x) + [v for c in C for v in c]:
        L = lcm(L, F(v).denominator)
    return [tuple(int(v * L) for v in c) for c in C], [int(v * L) for v in x]

def fano_search(C, x, limit=None):
    """Exhaustive search over row assignments (backtracking, exact integer arithmetic after scaling by the common
    denominator). Returns an assignment (list of types from C, one per line) or None."""
    p = len(x)
    Ci, xi = _scale(C, x)
    idx = {}
    pencils = [[l for l in range(7) if q in LINES[l]] for q in range(7)]
    # pencils completed exactly when their max line index is m-1
    done_at = {m: [pen for pen in pencils if max(pen) == m - 1] for m in range(1, 8)}
    Cf = [c for c in Ci if all(c[i] <= xi[i] for i in range(p))]
    rows = [None] * 7
    tot = [0] * p
    def rec(m):
        if m == 7:
            return True
        for c in Cf:
            if any(tot[i] + c[i] > 4 * xi[i] for i in range(p)):
                continue
            rows[m] = c
            if all(sum(rows[l][i] for l in pen) <= 2 * xi[i] for pen in done_at[m + 1] for i in range(p)):
                for i in range(p): tot[i] += c[i]
                r = rec(m + 1)
                for i in range(p): tot[i] -= c[i]
                if r: return True
        rows[m] = None
        return False
    if not rec(0):
        return None
    back = {ci: c for ci, c in zip(Ci, C)}
    res = [back[r] for r in rows]
    assert fano_ok(res, x)
    return res

def V_ok(s, t, x):
    """two-type template V: 5 rows s, 2 rows t; per part max(s+t, 5s/4+t/2) <= x (note fn 38/39)."""
    return all(max(s[i] + t[i], F(5, 4) * s[i] + t[i] / 2) <= x[i] for i in range(len(x)))

def pencil_type(c, x):
    return all(3 * c[i] <= 2 * x[i] for i in range(len(x)))

def hom_fano(c, x):
    return all(7 * c[i] <= 4 * x[i] for i in range(len(x)))

def super_classes(C, x):
    p = len(x)
    S = [[c for c in C if 3 * c[i] > 2 * x[i]] for i in range(p)]
    sigma = [min(c[i] for c in S[i]) if S[i] else None for i in range(p)]
    e = [x[i] - sigma[i] if sigma[i] is not None else None for i in range(p)]
    return S, sigma, e

def restrict(C, x, I):
    """C^(I) = {c : c_i <= 2x_i/3 for i in I}"""
    return [c for c in C if all(3 * c[i] <= 2 * x[i] for i in I)]
