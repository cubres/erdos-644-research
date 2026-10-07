"""Case (B) of Theorem A1: is the parameter region nonempty?  (wave typeclosed3, structure agent)

Parameters of a hypothetical counterexample in case (B) (K = S_1 u S_2, part 3 the small part):
  x1, x2, x3 capacities;  s1 = sigma_1, s2 = sigma_2 (class minima);  eta = tau* - 3/4 > 0;
  class-2 minimiser m^2 = (a1, s2, a3), class-1 minimiser m^1 = (s1, b2, b3).
Proved constraints (notes_structure.md, A1(B), L4, L6, and the V-push):
  (C1) 3/4 <= x1, x2 <= 3/2, 0 <= x3, x1 + x2 >= 9/4;
  (C2) s_i >= 2x_i/3;  e1 + e2 = x1 + x2 - s1 - s2 >= 3/4 + eta   (the class box is free);
  (C3) a1 + s2 + a3 = 1, a1 >= 0, 4x3/5 <= a3 <= x3;  s1 + b2 + b3 = 1, b2 >= 0, 4x3/5 <= b3 <= x3;   [A1(B)]
  (C4) V-push: every d in K_0 cap S_1 has d_1 > u1 := min(x1 - a1, 4(x1 - a1/2)/5), i.e. d_1 > x1 - A with
       A := max(a1, (x1 + 2a1)/5); symmetrically K_0 cap S_2 subset {c_2 > x2 - B}, B := max(b2, (x2 + 2b2)/5);
  (C5) L6: x3 >= delta + eta with delta > 3/4 - A - B (two-sided), or x3 > 3/4 + eta - A (one-sided), so in all
       cases  x3 >= 3/4 + eta - A - B.
Feasibility of {(C1)-(C5), eta >= 0} is an OR over the 4 branches of the two max's (each branch an LP: replace A by
one of its two arguments — valid since A >= each argument, so the branch LPs are RELAXATIONS: if all four are
infeasible, case (B) is impossible).  We maximise eta in each branch.
"""
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as Fr

# variables: x1 x2 x3 s1 s2 a1 a3 b2 b3 eta   (index 0..9)
names = ['x1', 'x2', 'x3', 's1', 's2', 'a1', 'a3', 'b2', 'b3', 'eta']


def solve(branchA, branchB, extra=None):
    A_ub = []; b_ub = []; A_eq = []; b_eq = []
    def le(coefs, rhs):        # sum coefs[i]*v_i <= rhs
        row = [0.0] * 10
        for k, v in coefs.items():
            row[names.index(k)] += v
        A_ub.append(row); b_ub.append(rhs)
    def eq(coefs, rhs):
        row = [0.0] * 10
        for k, v in coefs.items():
            row[names.index(k)] += v
        A_eq.append(row); b_eq.append(rhs)
    # (C1)
    le({'x1': -1, 'x2': -1}, -9 / 4)
    # (C2)
    le({'x1': 2 / 3, 's1': -1}, 0); le({'x2': 2 / 3, 's2': -1}, 0)
    le({'x1': -1, 'x2': -1, 's1': 1, 's2': 1, 'eta': 1}, -3 / 4)
    # (C3)
    eq({'a1': 1, 's2': 1, 'a3': 1}, 1); eq({'s1': 1, 'b2': 1, 'b3': 1}, 1)
    le({'x3': 4 / 5, 'a3': -1}, 0); le({'a3': 1, 'x3': -1}, 0)
    le({'x3': 4 / 5, 'b3': -1}, 0); le({'b3': 1, 'x3': -1}, 0)
    # (C5) with the branch choice: x3 >= 3/4 + eta - A - B  <=>  -x3 + eta - A - B <= -3/4
    Aco = {'a1': 1} if branchA == 0 else {'x1': 1 / 5, 'a1': 2 / 5}
    Bco = {'b2': 1} if branchB == 0 else {'x2': 1 / 5, 'b2': 2 / 5}
    row = {'x3': -1, 'eta': 1}
    for k, v in Aco.items():
        row[k] = row.get(k, 0) - v
    for k, v in Bco.items():
        row[k] = row.get(k, 0) - v
    le(row, -3 / 4)
    if extra:
        for coefs, rhs in extra:
            le(coefs, rhs)
    bounds = [(3 / 4, 3 / 2), (3 / 4, 3 / 2), (0, 3 / 8), (0, 3 / 2), (0, 3 / 2), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 1)]
    c = [0.0] * 10; c[9] = -1.0          # maximise eta
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    return res


if __name__ == '__main__':
    print('Case (B) relaxation LPs (maximise eta); case (B) is impossible iff every branch has max eta < 0:')
    for bA in (0, 1):
        for bB in (0, 1):
            r = solve(bA, bB)
            if r.status == 0:
                v = dict(zip(names, np.round(r.x, 5)))
                print('  branch A=%s B=%s : max eta = %.6f  at %s' % (['a1', '(x1+2a1)/5'][bA], ['b2', '(x2+2b2)/5'][bB], -r.fun, v))
            else:
                print('  branch', bA, bB, 'status', r.status, r.message)


def solve2(branchA, branchB, branchC, strictC3=0.0):
    """(C5') replaces (C5): the box W = (u1, u2, x3 - max(a3,b3)) is free (every type inside is V-killed), so
    cost(W) = A + B + max(a3, b3) >= 3/4 + eta.  Exact decomposition into 8 branches."""
    A_ub = []; b_ub = []; A_eq = []; b_eq = []
    def le(coefs, rhs):
        row = [0.0] * 10
        for k, v in coefs.items():
            row[names.index(k)] += v
        A_ub.append(row); b_ub.append(rhs)
    def eq(coefs, rhs):
        row = [0.0] * 10
        for k, v in coefs.items():
            row[names.index(k)] += v
        A_eq.append(row); b_eq.append(rhs)
    le({'x1': -1, 'x2': -1}, -9 / 4)
    le({'x1': 2 / 3, 's1': -1}, 0); le({'x2': 2 / 3, 's2': -1}, 0)
    le({'x1': -1, 'x2': -1, 's1': 1, 's2': 1, 'eta': 1}, -3 / 4)
    eq({'a1': 1, 's2': 1, 'a3': 1}, 1); eq({'s1': 1, 'b2': 1, 'b3': 1}, 1)
    le({'x3': 4 / 5, 'a3': -1}, -strictC3); le({'a3': 1, 'x3': -1}, 0)
    le({'x3': 4 / 5, 'b3': -1}, -strictC3); le({'b3': 1, 'x3': -1}, 0)
    Aco = {'a1': 1} if branchA == 0 else {'x1': 1 / 5, 'a1': 2 / 5}
    Bco = {'b2': 1} if branchB == 0 else {'x2': 1 / 5, 'b2': 2 / 5}
    Cco = {'a3': 1} if branchC == 0 else {'b3': 1}
    row = {'eta': 1}
    for co in (Aco, Bco, Cco):
        for k, v in co.items():
            row[k] = row.get(k, 0) - v
    le(row, -3 / 4)                     # eta - A - B - C <= -3/4
    bounds = [(3 / 4, 3 / 2), (3 / 4, 3 / 2), (0, 3 / 8), (0, 3 / 2), (0, 3 / 2), (0, 1), (0, 1), (0, 1), (0, 1), (-1, 1)]
    c = [0.0] * 10; c[9] = -1.0
    return linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')


if __name__ == '__main__':
    print('\nWith the free box W (C5\'): 8 branches, maximise eta:')
    worst = -np.inf
    for bA in (0, 1):
        for bB in (0, 1):
            for bC in (0, 1):
                r = solve2(bA, bB, bC)
                if r.status == 0:
                    worst = max(worst, -r.fun)
                    print('  A=%d B=%d C=%d : max eta = %.6f  x=%s s=%s a1,a3=%s b2,b3=%s' % (bA, bB, bC, -r.fun, np.round(r.x[:3], 4), np.round(r.x[3:5], 4), np.round(r.x[5:7], 4), np.round(r.x[7:9], 4)))
                else:
                    print('  A=%d B=%d C=%d : infeasible (%s)' % (bA, bB, bC, r.message[:40]))
    print('max eta over branches:', worst, '-> case (B) impossible' if worst < 0 else '-> NOT closed')
