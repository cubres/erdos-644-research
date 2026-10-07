"""Arc-CSP conflict analysis for ONE rigid type per class in the BALANCED regime (3T setting).
Hypotheses H: balanced, tau>3/4, tau<=sum e, pair maps (=> simple types, c_YX <= sigma_X - delta_Y), c<=2x/3.
Pattern XXY fails <=> c_YX > 2e_X  (at X)  or  c_XY > e_Y + sigma_Y/2  (at Y)   [failure at Z impossible: 3*(2x/3)=2x].
For each conflict type and each choice of failure modes, test LP feasibility; print exact certificates."""
import itertools, sys
from fractions import Fraction as F
sys.argv = ['x', '0', '1']
exec(open('three_type_cert.py').read().split('STATS = ')[0])     # V, IX, row, tv, BASE (balanced), DISJ, lp, exact_cert
P = 'ABC'
H = list(BASE)
for Y in range(3):
    for X in range(3):
        if X == Y: continue
        Z = 3 - X - Y
        # pair map: x_X - c_YX + e_Z >= tau  (valid since balanced forces c_YX < sigma_X);  and c_YX <= 2x_X/3
        H.append(row({'tau': 1, 'x' + P[X]: -1, tv(Y, X): 1, 'x' + P[Z]: -1, 's' + P[Z]: 1}, 0))
        H.append(row({tv(Y, X): 1, 'x' + P[X]: F(-2, 3)}, 0))
H.append(row({'tau': 1, 'xA': -1, 'sA': 1, 'xB': -1, 'sB': 1, 'xC': -1, 'sC': 1}, 0))   # id map: tau <= sum e
def fail_at_X(X, Y):   # c_YX > 2 e_X  <=>  2x_X - 2s_X - c_YX < 0
    return row({'x' + P[X]: 2, 's' + P[X]: -2, tv(Y, X): -1}, 0, True)
def fail_at_Y(X, Y):   # c_XY > x_Y - s_Y/2  <=>  x_Y - s_Y/2 - c_XY < 0
    return row({'x' + P[Y]: 1, 's' + P[Y]: F(-1, 2), tv(X, Y): -1}, 0, True)
def pat(X, Y): return [fail_at_X(X, Y), fail_at_Y(X, Y)]
def show(rows, cert):
    out = []
    for k, l in cert:
        c, r, st = rows[k]
        out.append(f"  {l} * [{' + '.join(f'{v}*{n}' for n, v in c.items())} {'<' if st else '<='} {r}]")
    return '\n'.join(out)
A, B, C = 0, 1, 2
CONF = {'cyclic AAB,BBC,CCA': [(A, B), (B, C), (C, A)], 'cyclic AAC,BBA,CCB': [(A, C), (B, A), (C, B)],
        'mutual AB': [(A, B), (B, A)], 'mutual AC': [(A, C), (C, A)], 'mutual BC': [(B, C), (C, B)]}
for name, pats in CONF.items():
    print("==", name)
    for modes in itertools.product(range(2), repeat=len(pats)):
        rows = H + [pat(X, Y)[m] for (X, Y), m in zip(pats, modes)]
        t, z, du = lp(rows)
        lab = ','.join(f"{P[X]}{P[X]}{P[Y]}@{P[X] if m == 0 else P[Y]}" for (X, Y), m in zip(pats, modes))
        if t > 1e-9: print(" ", lab, "FEASIBLE (slack %.4f)" % t)
        else:
            c = exact_cert(rows)
            print(" ", lab, "INFEASIBLE" + ("" if c else " (cert failed)"))
            pass
