"""Referee w9, claim typeclosed#0 (Theorem L+). Independent exact library (Fractions only, no LP).

Model (note 7.73/7.76 conventions, r=1): parts i=0..p-1 with capacities x_i; a type is c in [0,x] with sum c = 1
(we also allow sum c <= 1 in stress mode).  A vector u <= x is FREE if no c in C has c <= u.  tau*(C) = inf cost(u)
over free u, cost(u) = sum (x_i - u_i).  For finite C: tau* = min over threshold choices T_i (T_i a positive
coordinate value c_i, or 'none') such that every c has some i with c_i >= T_i, of sum_{i with threshold}(x_i - T_i).

Bad tuple = 7 rows (types) + one family P of cells (subsets of the 7 row labels) with no two cells (equal allowed)
covering all 7 labels + in each part i nonnegative cell masses of total <= x_i whose row loads dominate the rows'
i-coordinates.  We realise it LITERALLY at integer scale: points, 7 actual sets of the prescribed exact profiles
(trim), then check every pair of membership patterns (Venn condition: some row misses both points).
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import lcm

FULL = frozenset(range(7))

def tau_star(C, x):
    p = len(x)
    cands = []
    for i in range(p):
        vals = sorted({c[i] for c in C if c[i] > 0})
        cands.append([None] + vals)
    best = None
    for T in product(*cands):
        cost = sum((x[i] - T[i]) for i in range(p) if T[i] is not None)
        if best is not None and cost >= best:
            continue
        ok = all(any(T[i] is not None and c[i] >= T[i] for i in range(p)) for c in C)
        if ok:
            best = cost
    return best

def is_free(C, u):
    return not any(all(c[i] <= u[i] for i in range(len(u))) for c in C)

# ---------------- explicit templates (hand masses, no LP) ----------------
# V: rows 0,1 = c-rows (load t), rows 2..6 = a-rows (load s); 6 = apex z.
V_CELLS = [frozenset({0, 1})] + [frozenset(S) for S in combinations([2, 3, 4, 5, 6], 4)] + \
          [frozenset(s) for s in ({0, 3, 4, 6}, {0, 2, 5, 6}, {1, 2, 4, 6}, {1, 3, 5, 6})]

def V_masses(s, t):
    """explicit masses on V_CELLS with loads >= (t,t,s,s,s,s,s) and total max(s+t, 5s/4+t/2)."""
    m = {C: F(0) for C in V_CELLS}
    W6 = frozenset({2, 3, 4, 5})
    mixed = V_CELLS[6:]
    if 2 * t >= s:            # alpha=s/4 on mixed, beta=t-s/2 on {0,1}, s/2 on W6
        for C in mixed: m[C] += s / 4
        m[frozenset({0, 1})] += t - s / 2
        m[W6] += s / 2
    else:                     # alpha=t/2, gamma'=(s-2t)/4 on the four 4-sets containing 6, gamma6=s/4+t/2
        for C in mixed: m[C] += t / 2
        for C in V_CELLS[1:6]:
            if C != W6: m[C] += (s - 2 * t) / 4
        m[W6] += s / 4 + t / 2
    return m

# Fano plane on 7 points 0..6; lines; pencil through p0 = 0.
LINES = [frozenset(l) for l in ({0, 1, 2}, {0, 3, 4}, {0, 5, 6}, {1, 3, 5}, {1, 4, 6}, {2, 3, 6}, {2, 4, 5})]
# row index = line index; cell of point q = set of lines NOT through q
FANO_CELLS = [frozenset(li for li, L in enumerate(LINES) if q not in L) for q in range(7)]

def pencil_masses(e, f):
    """rows 0,1,2 = pencil lines through point 0 (load e), rows 3..6 = m-lines (load f)."""
    m = {}
    for q in range(7):
        m[FANO_CELLS[q]] = (e / 4) if q != 0 else max(F(0), f - 3 * e / 4)
    return m

def check_cells_noncovering(cells):
    cells = list(cells)
    for A in cells:
        if A == FULL: return False
    for A, B in combinations(cells, 2):
        if A | B == FULL: return False
    return True

def realise_and_check(rows, x, cellmass_per_part):
    """rows: 7 exact types (lists of Fractions). cellmass_per_part[i]: dict cell->mass (Fractions).
    Build integer realisation at scale D, trim rows to exact profiles, check capacity, profiles, Venn condition.
    Returns (ok, message)."""
    p = len(x)
    dens = [1]
    for i in range(p):
        dens += [v.denominator for v in cellmass_per_part[i].values()]
        dens += [r[i].denominator for r in rows] + [x[i].denominator]
    D = 1
    for d in dens: D = lcm(D, d)
    patterns = set()
    for i in range(p):
        pts = []  # list of cell (membership pattern) per point
        for C, mass in cellmass_per_part[i].items():
            if mass < 0: return False, 'negative mass'
            n = mass * D
            assert n.denominator == 1
            pts += [set(C) for _ in range(int(n))]
        if len(pts) > x[i] * D: return False, f'capacity part {i}: {len(pts)} > {x[i]*D}'
        # trim: row l keeps exactly rows[l][i]*D of the points whose cell contains l
        for l in range(7):
            need = rows[l][i] * D
            have = [idx for idx, P in enumerate(pts) if l in P]
            if len(have) < need: return False, f'load row {l} part {i}: {len(have)} < {need}'
            for idx in have[int(need):]:
                pts[idx].discard(l)
        for l in range(7):
            assert sum(1 for P in pts if l in P) == rows[l][i] * D
        patterns |= {frozenset(P) for P in pts}
    pats = list(patterns)
    for A in pats:
        if A == FULL: return False, 'point in all rows'
    for A, B in combinations(pats, 2):
        if A | B == FULL: return False, f'pair {sorted(A)} {sorted(B)} covers'
    return True, f'D={D}'
