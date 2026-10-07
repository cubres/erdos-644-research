"""Referee heavyparts#2: EXACT cover functions of the two supports used by PCL.
Cover LP in one part: min sum_C w_C s.t. sum_{C ni r} w_C >= z_r (r=0..6), w>=0, over the MAXIMAL cells of a
downset support.  Dual: max z.y s.t. sum_{r in C} y_r <= 1 (all C), y>=0.  We enumerate ALL dual vertices exactly
(Fractions, 7 tight constraints out of cells+nonnegativity), so cover(z) = max_vertex z.y is exact.
Supports: (i) Fano support (cells inside complements of Fano lines) -> compare with Lemma 7.63 dual criterion
(rows<=x, pencils<=2x, total<=4x); (ii) V support = catalogue fn38 witness (msb-first bit order, rows 0,1 = type b).
"""
import itertools, json, pickle, os
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))

def solve(A, b):
    n = len(A); M = [list(map(F, A[i])) + [F(b[i])] for i in range(n)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None: return None
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]; M[r] = [M[r][k] - f*M[c][k] for k in range(n+1)]
    return [M[i][n] / M[i][i] for i in range(n)]

def dual_vertices(cells):
    cons = [[1 if r in C else 0 for r in range(7)] for C in cells]   # <= 1
    nonneg = [[1 if r == k else 0 for r in range(7)] for k in range(7)]  # y_k >= 0 as equality 0
    allc = [(c, 1) for c in cons] + [(c, 0) for c in nonneg]
    verts = set()
    for S in itertools.combinations(range(len(allc)), 7):
        y = solve([allc[i][0] for i in S], [allc[i][1] for i in S])
        if y is None: continue
        if any(v < 0 for v in y): continue
        if any(sum(c[r]*y[r] for r in range(7)) > 1 for c in cons): continue
        verts.add(tuple(y))
    # keep only non-dominated (z>=0 so dominated vertices never matter)
    V = [v for v in verts if not any(w != v and all(w[i] >= v[i] for i in range(7)) for w in verts)]
    return V

LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
fano_cells = [tuple(r for r in range(7) if r not in L) for L in LINES]
d = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy/astra_support_capacity_minimal.json'))
w = d['minimal_functions'][38]['witness']; n = int(w[0], 16)
S = [k for k in range(128) if (n >> (127-k)) & 1]
assert all((c & ~(1 << r)) in S for c in S for r in range(7) if c >> r & 1), 'not a downset'
assert all((a | b) != 127 for a in S for b in S), 'two cells cover'
mx = [c for c in S if not any(e != c and e & c == c for e in S)]
V_cells = [tuple(r for r in range(7) if c >> r & 1) for c in mx]
print('V support maximal cells:', V_cells, ' assignment', d['minimal_functions'][38]['witness'][1])
# Fano support sanity: non-covering
assert all(set(a) | set(b) != set(range(7)) for a in fano_cells for b in fano_cells)

FV = dual_vertices(fano_cells); VV = dual_vertices(V_cells)
print('Fano dual vertices (non-dominated):', len(FV)); print('V dual vertices:', len(VV))
# (i) compare Fano cover with Lemma 7.63 criterion: cover(z) <= x  <=>  rows, pencils, totals.
# criterion in dual form: the set of functionals {e_r}, {pencil/2}, {all/4}; check the two polytopes coincide:
PEN = [[l for l, L in enumerate(LINES) if q in L] for q in range(7)]
crit = [tuple(F(1) if r == k else F(0) for r in range(7)) for k in range(7)]
crit += [tuple(F(1,2) if r in PEN[q] else F(0) for r in range(7)) for q in range(7)] + [tuple([F(1,4)]*7)]
# NOTE: z_r here are indexed by LINES? No: the Fano support cells are complements of lines, rows are POINTS 0..6.
# Rows sit on points; row r is avoided by cells complementary to lines through r.  Lemma 7.63 in heavylib indexes
# rows by LINES and pencils by points (dual plane) -- equivalent by duality.  Check with the point-indexed version:
PENP = [[q for q in range(7) if q in L] for L in LINES]  # 3 rows (points) on a line
critP = [tuple(F(1) if r == k else F(0) for r in range(7)) for k in range(7)]
critP += [tuple(F(1,2) if r in PENP[l] else F(0) for r in range(7)) for l in range(7)] + [tuple([F(1,4)]*7)]
def cover_le(V, z): return max(sum(a*b for a, b in zip(v, z)) for v in V)
# polytope equality: every FV vertex is a convex-dominated combo? Check support functions agree on many z.
import random
random.seed(1)
bad = 0
for _ in range(3000):
    z = [F(random.randint(0, 20), 20) for _ in range(7)]
    if cover_le(FV, z) != max(cover_le(critP, z), 0): bad += 1
print('Fano cover == max(row, line/2, total/4) [point-indexed rows] mismatches in 3000:', bad)
print('FV vertices:', sorted(set(tuple(sorted(v)) for v in FV)))
# (ii) V cover as function of (s = load on 5 a-rows 2..6, t = load on b-rows 0,1)
coef = sorted(set((sum(v[2:]), sum(v[:2])) for v in VV))
nd = [c for c in coef if not any(e != c and e[0] >= c[0] and e[1] >= c[1] for e in coef)]
print('V cover = max over (u,v) of u*s+v*t, (u,v) in', nd)
# Q_alpha in Fano: 3 alpha rows through a point.  In point-indexed form: rows = points; 'three rows concurrent'
# dualises to 'three points on a line'.  Q: alpha on the 3 points of line 0, beta on the other 4 (a quadrilateral's
# dual = the complement of a line, which is an affine plane / 4 points no three collinear).
QV = set()
for v in FV:
    QV.add((sum(v[r] for r in LINES[0]), sum(v[r] for r in range(7) if r not in LINES[0])))
Qnd = [c for c in QV if not any(e != c and e[0] >= c[0] and e[1] >= c[1] for e in QV)]
print('Q cover (alpha on a line of 3 rows, beta on 4) = max of u*al+v*be over', sorted(Qnd))
pickle.dump({'FV': FV, 'VV': VV, 'V_cells': V_cells}, open(os.path.join(HERE, 'w9_ref_heavyparts2_supports.pkl'), 'wb'))
