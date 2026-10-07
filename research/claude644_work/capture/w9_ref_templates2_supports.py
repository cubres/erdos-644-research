# Referee w9, claim templates#2 (Theorem H2): INDEPENDENT exact check of the three templates' per-part
# minimum-mass functions, computed from the SUPPORTS themselves (not from Lemma 7.63's formula):
#   * enumerate all vertices of the dual polytope {w >= 0, sum_{j in c} w_j <= 1 for every maximal cell c}
#     by exact Gaussian elimination over all 7-subsets of constraints;
#   * min mass for loads z is max_w z.w (LP duality); for a two-colouring (rows of class a get s, class b get t)
#     this is max over vertices of A*s + B*t with A = sum_{a-rows} w, B = sum_{b-rows} w;
#   * compare with the claimed formulas exactly at every breakpoint on s+t=1 (both sides piecewise linear).
# Also checks the support property: no two cells (maximal cells; any two, incl. a cell with itself) cover [7].
import itertools
from fractions import Fraction as F

def solve(A, b):
    n = len(A); M = [row[:] + [bb] for row, bb in zip(A, b)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None: return None
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [M[r][k] - f * M[c][k] for k in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]

def dual_vertices(cells):
    cons = []  # (coef, rhs) meaning coef.w <= rhs
    for c in cells: cons.append(([F(1) if j in c else F(0) for j in range(7)], F(1)))
    for j in range(7): cons.append(([F(-1) if k == j else F(0) for k in range(7)], F(0)))
    verts = set()
    for S in itertools.combinations(range(len(cons)), 7):
        w = solve([cons[i][0] for i in S], [cons[i][1] for i in S])
        if w is None: continue
        if all(sum(a * b for a, b in zip(co, w)) <= r for co, r in cons): verts.add(tuple(w))
    return verts

def no_cover(cells):
    full = frozenset(range(7))
    return all(frozenset(c1) | frozenset(c2) != full for c1 in cells for c2 in cells)

def maximal(cells):
    cells = [frozenset(c) for c in cells]
    return [c for c in cells if not any(c < d for d in cells)]

def compare(verts, arows, brows, formula, name):
    lin = set((sum(w[j] for j in arows), sum(w[j] for j in brows)) for w in verts)
    pts = {F(0), F(1)}
    cand = list(lin) + formula
    for (A1, B1), (A2, B2) in itertools.combinations(cand, 2):
        # A1 s + B1 (1-s) = A2 s + B2 (1-s)
        den = (A1 - B1) - (A2 - B2)
        if den != 0:
            s = (B2 - B1) / den
            if 0 <= s <= 1: pts.add(s)
    for s in pts:
        t = 1 - s
        m1 = max(A * s + B * t for A, B in lin)
        m2 = max(u * s + v * t for u, v in formula)
        assert m1 == m2, (name, s, m1, m2)
    print(name, ': support ok, #dual vertices', len(verts), ', min-mass function == claimed formula at',
          len(pts), 'breakpoints')

LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
fano_cells = [frozenset(range(7)) - frozenset(L) for L in LINES]
assert no_cover(fano_cells)
fv = dual_vertices(fano_cells)
# H: all rows a
compare(fv, range(7), [], [(F(7, 4), F(0))], 'H (homogeneous Fano), 7s/4')
# Q_b: b-rows = line (0,1,2), a-rows = the other four
compare(fv, [3, 4, 5, 6], [0, 1, 2], [(F(0), F(3, 2)), (F(1), F(3, 4))], 'Q_b = max(3t/2, s+3t/4)')
# V support: rows 0=b0, 1=b1, 2..5 = w1..w4, 6 = z
b0, b1, w1, w2, w3, w4, z = range(7)
W = [w1, w2, w3, w4]
Vcells = [frozenset({b0, b1})] + [frozenset(c) for c in itertools.combinations(W + [z], 4)] + \
    [frozenset({b0, w3, w4, z}), frozenset({b0, w1, w2, z}), frozenset({b1, w2, w4, z}), frozenset({b1, w1, w3, z})]
assert no_cover(Vcells), 'V support has a covering pair'
vv = dual_vertices(Vcells)
compare(vv, W + [z], [b0, b1], [(F(1), F(1)), (F(5, 4), F(1, 2))], 'V = max(s+t, 5s/4+t/2)')
print('ALL SUPPORT CHECKS PASSED')
