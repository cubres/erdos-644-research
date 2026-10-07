"""Relaxation witness (continuum type-closed, rank 1): two parts P,Q of capacity x, two types
a=(s,1-s), b=(1-s,s).  Exact rational checks of the LOCAL rules:
  tau*  = min(x-s, 2x-2+2s)                           (exact via lib tau_star)
  GT*   : every triple with sum <= 2x has U >= 2 tau* (strict)          [exact]
  D4    : no 7-multiset with sum <= 3x                                   [exact]
  nu<=2 : no 3 types with sum <= x (automatic, N<3)                      [exact]
  LemmaC: no three disjoint 'u-blocks' of mass 2tau*/3 whose pairwise unions all contain a type  [exact LP-free:
          conditions are linear; checked by exhaustive case split over which type each union contains, via LP]
  Q     : static dual pencil (min |I6|+|I7| s.t. |I5|<=tau*) >= 2tau*-1   [float LP, discovery]
and the fact that it is NOT (7,2) (two-fixed-type bad tuple, note Thm 7.71; lib pair_bad = exact capacity fns).
Family of witnesses: x in (9/8, 9/7), s < 1-2x/3 close to it: tau* -> 2x/3 -> 6/7."""
from fractions import Fraction as F
import itertools
from w4_typeclosed_lib import tau_star, pair_bad, load_cap42
from w6_core_qcont import qtest
from scipy.optimize import linprog
def check(x, s, verbose=True):
    a = (s, 1-s); b = (1-s, s); A = [a, b]; X = [x, x]
    ts = tau_star(A, X)
    gt = all(sum(max(max(z[i] for z in tr), sum(z[i] for z in tr)/2) for i in range(2)) > 2*ts
             for tr in itertools.combinations_with_replacement(A, 3) if all(sum(z[i] for z in tr) <= 2*x for i in range(2)))
    d4 = not any(all(sum(A[j][i] for j in ms) <= 3*x for i in range(2)) for ms in itertools.combinations_with_replacement(range(2), 7))
    nu = not any(all(sum(z[i] for z in tr) <= x for i in range(2)) for tr in itertools.combinations_with_replacement(A, 3))
    # Lemma C: blocks X,Y,Z (2 coords each) of mass m=2ts/3, disjoint (sum <= x per part); unions contain chosen types
    m = 2*ts/3; lc_viol = False
    for ch in itertools.product(range(2), repeat=3):   # type contained in XuY, XuZ, YuZ
        # vars X1,X2,Y1,Y2,Z1,Z2 >=0 ; X1+X2=m etc ; X1+Y1+Z1<=x ; X2+Y2+Z2<=x ; union >= type coords
        Aeq = [[1,1,0,0,0,0],[0,0,1,1,0,0],[0,0,0,0,1,1]]; beq = [float(m)]*3
        Aub = [[1,0,1,0,1,0],[0,1,0,1,0,1]]; bub = [float(x)]*2
        for (u, v), c in zip([(0, 1), (0, 2), (1, 2)], ch):
            T = A[c]
            for i in range(2):
                row = [0]*6; row[2*u+i] = -1; row[2*v+i] = -1; Aub.append(row); bub.append(-float(T[i]))
        r = linprog([0]*6, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=(0, None), method='highs')
        if r.status == 0: lc_viol = True
    qbest = min(r[0] for quad in itertools.combinations_with_replacement(A, 4)
                for r in [qtest([tuple(float(v) for v in q) for q in quad], [float(x)]*2, float(ts), 1.0)] if r)
    q_ok = qbest >= float(2*ts - 1) - 1e-9
    notseven2 = pair_bad(a, b, X, load_cap42())
    if verbose:
        print(f"x={x} s={s}: tau*={ts}={float(ts):.4f}  GT*:{gt} D4:{d4} nu<=2:{nu} LemmaC-not-violated:{not lc_viol}"
              f" Q-static(min|I6|+|I7|={qbest:.4f} vs {float(2*ts-1):.4f}):{q_ok}  pair-bad (so NOT (7,2)):{notseven2}")
    return ts, gt and d4 and nu and (not lc_viol) and q_ok and notseven2
if __name__ == '__main__':
    check(F(5, 4), F(3, 20))
    check(F(5, 4), F(4, 25))
    check(F(128, 100), F(14, 100))
    check(F(1285, 1000), F(142, 1000))
