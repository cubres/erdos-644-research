"""[typeclosed#1] referee: exact check of the three template capacity functions used by GGP, with the ACTUAL supports.
Q_b: Fano support, b on the 3 pencil lines through point 0, a on the 4 lines missing 0: claimed max(3t/2, s+3t/4).
Q_a: mirror.  V: 5 a-rows + 2 b-rows on the V support: claimed max(s+t, 5s/4+t/2).
Exact simplex cover values on a rational grid (with optimality certificates) must EQUAL the formulas.
Also: supports are valid (no two cells, possibly equal, cover all 7 rows)."""
from fractions import Fraction as F
from w9_ref_typeclosed1brk_lib import *

assert is_support(FANO_CELLS) and is_support(V_CELLS)
# Fano: every pair of points lies on a line, and a cell = lines missing q; union of cells(q),cells(q') misses line qq'
Qb = lambda s, t: max(3 * t / 2, s + 3 * t / 4)
Qa = lambda s, t: max(3 * s / 2, t + 3 * s / 4)
Vf = lambda s, t: max(s + t, 5 * s / 4 + t / 2)
den = 12
n = 0
for i in range(0, 2 * den + 1):
    for j in range(0, 2 * den + 1):
        s, t = F(i, den), F(j, den)
        assert cover(FANO_CELLS, rows_Qb(s, t))[0] == Qb(s, t), (s, t)
        assert cover(FANO_CELLS, rows_Qa(s, t))[0] == Qa(s, t), (s, t)
        assert cover(V_CELLS, rows_V(s, t))[0] == Vf(s, t), (s, t)
        n += 1
print('capacity formulas Qb, Qa, V equal exact cover values on', n, 'grid points (s,t in [0,2], step 1/12)')
# region vertices, explicit
for name, cells, rf, verts in (('Qb', FANO_CELLS, rows_Qb, [(1, 0), (F(1, 2), F(2, 3)), (0, F(2, 3))]),
                               ('V', V_CELLS, rows_V, [(F(4, 5), 0), (F(2, 3), F(1, 3)), (0, 1)])):
    for s, t in verts:
        v, z = cover(cells, rf(F(s), F(t)))
        print(name, 'vertex', (str(s), str(t)), 'cover value', v, 'masses', [str(q) for q in z if q])
# homogeneous Fano: 7 equal rows c: value 7c/4
assert cover(FANO_CELLS, [F(1)] * 7)[0] == F(7, 4)
print('homogeneous Fano value 7c/4 confirmed')
# mutation control: a wrong support must break the formula
bad_cells = V_CELLS[:-1]
diff = [(s, t) for s in (F(2, 3),) for t in (F(1, 3),) if cover(bad_cells, rows_V(s, t))[0] != Vf(s, t)]
print('mutation control (drop one V cell) detected:', bool(diff))
