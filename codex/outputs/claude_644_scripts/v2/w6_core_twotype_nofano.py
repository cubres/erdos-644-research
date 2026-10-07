"""Independent check that the two-type witness W(x,s) has NO Fano-labelled (Fano-downset) bad 7-tuple:
for each of the 2^7 assignments of types a/b to the seven Fano lines, and each part, LP: masses y_p>=0 on the
seven parent cells (a vertex labelled by Fano point p may lie in any subset of the 4 lines missing p) with
sum_{p notin l} y_p >= load of row l and sum_p y_p <= x.  Feasible in both parts <=> Fano bad tuple exists.
Exact: infeasibility certified by a rational Farkas vector found by LP and checked in Fractions."""
import itertools
from fractions import Fraction as F
from scipy.optimize import linprog
L=[[0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2]]
def part_feasible_exact(loads, x):
    # primal: min sum y s.t. M y >= loads, y>=0 ; feasible iff optimum <= x. Dual: max w.loads s.t. M^T w <= 1, w>=0.
    M=[[0 if p in L[l] else 1 for p in range(7)] for l in range(7)]
    r=linprog([1]*7, A_ub=[[-v for v in row] for row in M], b_ub=[-float(v) for v in loads], bounds=(0,None), method='highs')
    opt=r.fun
    # exact dual certificate: candidate w from marginals, rationalised
    w=[F(-m).limit_denominator(1000) for m in r.ineqlin.marginals]
    w=[max(v,F(0)) for v in w]
    assert all(sum(w[l]*M[l][p] for l in range(7)) <= 1 for p in range(7))
    dual=sum(w[l]*loads[l] for l in range(7))
    return dual <= x, dual, opt
def check(x, s):
    a=(s,1-s); b=(1-s,s); A=[a,b]; found=0
    for asg in itertools.product(range(2), repeat=7):
        ok=True
        for i in range(2):
            feas, dual, opt = part_feasible_exact([A[asg[l]][i] for l in range(7)], x)
            if dual > x: ok=False; break          # exact certificate of infeasibility in part i
            if opt > float(x) + 1e-9: ok=False; break
        if ok: found+=1
    print(f"x={x} s={s}: Fano-labelled bad 7-tuples found: {found} (0 = none; infeasibility certified by exact duals where dual>x)")
if __name__=='__main__':
    check(F(5,4),F(3,20)); check(F(257,200),F(71,500))
