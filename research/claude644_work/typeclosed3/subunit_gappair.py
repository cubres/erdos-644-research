"""SUB-UNIT GAP-PAIR LEMMA (exact check by Farkas certificates).
Setting: two parts with capacities x, y > 0; two rows a = (a1,a2), b = (b1,b2) with 0 <= a, b, a <= (x,y), b <= (x,y),
masses m_a = a1 + a2, m_b = b1 + b2 in (0, 1] (sub-unit allowed, any lower bound),
   (H1) a2 >= 4y/7   (a is 4/7-heavy in part 2),   (H2) b1 >= 4x/7,   (S) b2 <= 4y/7,   (O) a1 <= b1,
   (G)  (x - b1) + (y - a2) >= 3/4                  (the lex box (b1, a2) is free, cost >= tau* >= 3/4).
Claim: one of Q_b = T(a; b,b; b) [4 a-rows off a line, 3 b-rows on it], Q_a = T(b; a,a; a), V(a,b) [5 a, 2 b] is feasible:
   Q_b: 3b/2 <= (x,y) and a + 3b/4 <= (x,y);   Q_a: 3a/2 <= (x,y), b + 3a/4 <= (x,y);   V: a + b <= (x,y), 5a/4 + b/2 <= (x,y).
Method: for every choice of one violated inequality per template (4 x 4 x 4 = 64 cases; violation strict), the LP
{hypotheses, the three strict violations} must be infeasible; we find a Farkas certificate with scipy and re-verify it
exactly with Fractions (nonnegative multipliers, zero combination, negative constant / strictness).
Variables: v = (x, y, a1, a2, b1, b2).  Rows are written as  coef . v >= rhs  (strict flag)."""
from fractions import Fraction as F
import itertools, numpy as np
from scipy.optimize import linprog

VARS = ['x', 'y', 'a1', 'a2', 'b1', 'b2']


def row(d, rhs=0, strict=False):
    return ([F(d.get(v, 0)) for v in VARS], F(rhs), strict)


HYP = [
    row({'a1': 1}), row({'a2': 1}), row({'b1': 1}), row({'b2': 1}),
    row({'x': 1, 'a1': -1}), row({'y': 1, 'a2': -1}), row({'x': 1, 'b1': -1}), row({'y': 1, 'b2': -1}),
    row({'a1': -1, 'a2': -1}, -1), row({'b1': -1, 'b2': -1}, -1),           # masses <= 1
    row({'a2': 1, 'y': F(-4, 7)}), row({'b1': 1, 'x': F(-4, 7)}), row({'b2': -1, 'y': F(4, 7)}), row({'b1': 1, 'a1': -1}),
    row({'x': 1, 'b1': -1, 'y': 1, 'a2': -1}, F(3, 4)),
]
# template feasibility rows (each template feasible iff all its rows hold); failure = one row violated strictly
Qb = [row({'x': 1, 'b1': F(-3, 2)}), row({'y': 1, 'b2': F(-3, 2)}), row({'x': 1, 'a1': -1, 'b1': F(-3, 4)}), row({'y': 1, 'a2': -1, 'b2': F(-3, 4)})]
Qa = [row({'x': 1, 'a1': F(-3, 2)}), row({'y': 1, 'a2': F(-3, 2)}), row({'x': 1, 'b1': -1, 'a1': F(-3, 4)}), row({'y': 1, 'b2': -1, 'a2': F(-3, 4)})]
V = [row({'x': 1, 'a1': -1, 'b1': -1}), row({'y': 1, 'a2': -1, 'b2': -1}), row({'x': 1, 'a1': F(-5, 4), 'b1': F(-1, 2)}), row({'y': 1, 'a2': F(-5, 4), 'b2': F(-1, 2)})]


def neg(r):
    c, rhs, _ = r
    return ([-v for v in c], -rhs, True)          # violation: -(coef.v) > -rhs


def farkas(rows):
    """rows: coef.v >= rhs (strict flag). Find lambda >= 0 with sum lambda_i coef_i = 0 and sum lambda_i rhs_i > 0
    (or >= 0 with some strict row weighted) => infeasible.  Returns exact multipliers or None."""
    n = len(rows); d = len(VARS)
    A = np.array([[float(v) for v in r[0]] for r in rows])          # n x d
    rhs = np.array([float(r[1]) for r in rows]); st = np.array([r[2] for r in rows], dtype=float)
    # maximize sum lambda*rhs + sum_{strict} lambda  subject to A^T lambda = 0, lambda >= 0, sum lambda <= 1
    c = -(rhs + 0.5 * st)
    res = linprog(c, A_eq=A.T, b_eq=np.zeros(d), A_ub=np.ones((1, n)), b_ub=[1], bounds=[(0, None)] * n, method='highs')
    if res.status != 0 or -res.fun <= 1e-9:
        return None
    lam = [F(v).limit_denominator(10 ** 6) for v in res.x]
    # exact repair: solve A^T lam = 0 exactly on the support via fractions (least squares not exact) -> instead verify
    return lam


def verify(rows, lam):
    comb = [sum(l * r[0][j] for l, r in zip(lam, rows)) for j in range(len(VARS))]
    if any(v != 0 for v in comb):
        return False
    val = sum(l * r[1] for l, r in zip(lam, rows))
    strict = any(l > 0 and r[2] for l, r in zip(lam, rows))
    return val > 0 or (val == 0 and strict)


def exact_farkas(rows):
    """EXACT rational Farkas multipliers via sympy's simplex: maximise sum lam_i rhs_i + sum_{strict} lam_i subject to
    sum lam_i coef_i = 0, lam >= 0, sum lam <= 1.  Optimum > 0 <=> the strict system is infeasible (certificate)."""
    import sympy
    from sympy.solvers.simplex import lpmax
    n = len(rows); lam = sympy.symbols('l0:%d' % n)
    cons = []
    for j in range(len(VARS)):
        cons.append(sympy.Eq(sum(sympy.Rational(rows[i][0][j]) * lam[i] for i in range(n)), 0))
    cons += [l >= 0 for l in lam]
    cons.append(sum(lam) <= 1)
    cons.append(sum(sympy.Rational(rows[i][1]) * lam[i] for i in range(n)) >= 0)      # value >= 0 (needed for a certificate)
    obj = sum((sympy.Rational(rows[i][1]) + (1 if rows[i][2] else 0)) * lam[i] for i in range(n))
    val, sol = lpmax(obj, cons)
    if val <= 0:
        return None
    lam_v = [F(str(sympy.Rational(sol[l]))) for l in lam]
    assert verify(rows, lam_v)
    return lam_v


def exact_feasible_margin(rows):
    """max eps such that all rows hold with the strict ones satisfied by >= eps (exact)."""
    import sympy
    from sympy.solvers.simplex import lpmax
    v = sympy.symbols('v0:%d' % len(VARS)); eps = sympy.Symbol('eps')
    cons = [vv >= 0 for vv in v] + [vv <= 3 for vv in v] + [eps <= 1]
    for c, rhs, st in rows:
        cons.append(sum(sympy.Rational(c[j]) * v[j] for j in range(len(VARS))) - (eps if st else 0) >= sympy.Rational(rhs))
    try:
        val, sol = lpmax(eps, cons)
    except Exception as e:
        return None, str(e)
    return val, {VARS[j]: sol[v[j]] for j in range(len(VARS))}


if __name__ == '__main__':
    bad = 0; n = 0
    for i, j, k in itertools.product(range(4), repeat=3):
        rows = HYP + [neg(Qb[i]), neg(Qa[j]), neg(V[k])]
        lam = exact_farkas(rows); n += 1
        if lam is None:
            bad += 1; print('NO CERTIFICATE for failure choice', (i, j, k))
            print('   exact max strict margin and point:', exact_feasible_margin(rows))
    print('cases', n, 'without certificate', bad)
    print('SUB-UNIT GAP-PAIR:', 'PROVED (exact Farkas certificates for all 64 failure combinations)' if bad == 0 else 'FAILS')
