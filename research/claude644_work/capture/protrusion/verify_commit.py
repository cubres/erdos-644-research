# Commit-at-first-sight strategies: exact values for every line order (anchored and unanchored).
# A fresh outside vertex first seen at step i is committed to a dual line L not containing i and is avoided at every
# later step of L. Against such strategies re-use is useless to the adversary, so the adversary plays all-fresh and the
# value is the LP  min c  s.t.  cost_j = sum_{i<j} sum_{L: j in L, i notin L} w_i(L) <= c,  sum_L w_i(L) = 1.
# Exact certificates: rational primal w (upper bound) and rational dual weights y on steps (lower bound):
#   c >= sum_i min_{L not containing i} y(L cap (i,6])  for any y >= 0 with sum y = 1.
import itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
BASE = [frozenset(((0+i)%7, (1+i)%7, (3+i)%7)) for i in range(7)]
def relabel(order):
    pos = {p: t for t, p in enumerate(order)}
    return [frozenset(pos[p] for p in L) for L in BASE]
def classes():
    seen = {}
    for order in itertools.permutations(range(7)):
        lines = relabel(order); key = tuple(sorted(tuple(sorted(L)) for L in lines))
        seen.setdefault(key, lines)
    return seen
def lp(lines, budgets):
    var = [(i, li) for i in range(7) if budgets[i] for li, L in enumerate(lines) if i not in L]
    nv = len(var) + 1
    A_ub = []; b_ub = []
    for j in range(7):
        row = np.zeros(nv)
        for k, (i, li) in enumerate(var):
            if i < j and j in lines[li]: row[k] = 1
        row[-1] = -1; A_ub.append(row); b_ub.append(0)
    A_eq = []; b_eq = []
    for i in range(7):
        if not budgets[i]: continue
        row = np.zeros(nv)
        for k, (ii, li) in enumerate(var):
            if ii == i: row[k] = 1
        A_eq.append(row); b_eq.append(1)
    c = np.zeros(nv); c[-1] = 1
    res = linprog(c, A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq), b_eq=b_eq, bounds=[(0, None)] * nv, method='highs')
    y = [-v for v in res.ineqlin.marginals]
    return res.fun, var, res.x, y
def exact_upper(lines, budgets, var, x):
    w = {v: Fr(xx).limit_denominator(1000) for v, xx in zip(var, x)}
    # renormalise each step's weights to sum exactly 1 (put the rounding residue on the largest entry)
    for i in range(7):
        if not budgets[i]: continue
        ks = [v for v in var if v[0] == i]; s = sum(w[v] for v in ks)
        big = max(ks, key=lambda v: w[v]); w[big] += 1 - s
        assert all(w[v] >= 0 for v in ks)
    return max(sum(w[(i, li)] for (i, li) in var if i < j and j in lines[li]) for j in range(7))
def exact_lower(lines, budgets, y):
    y = [max(Fr(v).limit_denominator(1000), Fr(0)) for v in y]; s = sum(y); y = [v / s for v in y]
    tot = Fr(0)
    for i in range(7):
        if not budgets[i]: continue
        tot += min(sum(y[j] for j in L if j > i) for L in lines if i not in L)
    return tot
for name, budgets in [('unanchored', [1]*7), ('anchored', [0]+[1]*6)]:
    vals = []
    for key, lines in classes().items():
        f, var, x, y = lp(lines, budgets)
        up = exact_upper(lines, budgets, var, x); lo = exact_lower(lines, budgets, y)
        assert lo <= up
        vals.append((lo, up, key))
    best_up = min(v[1] for v in vals); worst_lo = min(v[0] for v in vals)
    print(name, ': exact commitment value range over the 30 order classes: every class has value >=', worst_lo,
          '; best class achieves', best_up, '; classes with lo==up:', sum(1 for v in vals if v[0] == v[1]))
