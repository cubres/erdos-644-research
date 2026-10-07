# Commitment-at-first-sight LP: fresh mass (budget b_i per step) at step i is committed to a dual line L not containing i,
# and then avoided at every later step of L.  cost_j = sum_{i<j} sum_{L: j in L, i not in L} w[i][L].
import sys, itertools
sys.path.insert(0, '.')
from fano import *
import numpy as np
from scipy.optimize import linprog

def commit_lp(tlines, budgets):
    n = 7
    var = []  # (i, Lidx)
    for i in range(n):
        if budgets[i] == 0: continue
        for li, L in enumerate(tlines):
            if i not in L:
                var.append((i, li))
    nv = len(var) + 1  # last = c
    # minimize c
    cobj = np.zeros(nv); cobj[-1] = 1
    A_ub = []; b_ub = []
    for j in range(n):
        row = np.zeros(nv)
        for k, (i, li) in enumerate(var):
            if i < j and j in tlines[li]:
                row[k] = 1
        row[-1] = -1
        A_ub.append(row); b_ub.append(0)
    A_eq = []; b_eq = []
    for i in range(n):
        if budgets[i] == 0: continue
        row = np.zeros(nv)
        for k, (ii, li) in enumerate(var):
            if ii == i: row[k] = 1
        A_eq.append(row); b_eq.append(budgets[i])
    res = linprog(cobj, A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq), b_eq=b_eq, bounds=[(0, None)] * nv, method='highs')
    return res.fun, {var[k]: res.x[k] for k in range(len(var)) if res.x[k] > 1e-9}

if __name__ == '__main__':
    # unanchored
    best = None
    res_all = []
    for order in itertools.permutations(range(7)):
        pass
    reps = canonical_orders()
    vals = []
    for tl, order in reps.items():
        tlines = [frozenset(L) for L in tl]
        v, sol = commit_lp(tlines, [1] * 7)
        comp = [sum(1 for L in tlines if max(L) == j) for j in range(7)]
        vals.append((v, comp, tl))
    vals.sort()
    print("UNANCHORED commitment LP values by order class:")
    for v, comp, tl in vals[:10]:
        print(round(v, 6), comp, tl)
    print('max', vals[-1][0])
    # anchored: anchor = time 0 with budget 0
    vals = []
    seen = set()
    for order in itertools.permutations(range(7)):
        tl = tuple(sorted(tuple(sorted(L)) for L in relabel(LINES, order)))
        if tl in seen: continue
        seen.add(tl)
    # canonical under collineations fixing nothing: but we need anchor at time 0; all time-labelled systems are in 'seen' (5040/168*?)
    reps2 = {}
    for order in itertools.permutations(range(7)):
        tl = tuple(sorted(tuple(sorted(L)) for L in relabel(LINES, order)))
        reps2.setdefault(tl, order)
    for tl in reps2:
        tlines = [frozenset(L) for L in tl]
        v, sol = commit_lp(tlines, [0] + [1] * 6)
        vals.append((v, tl))
    vals.sort()
    print("ANCHORED (anchor at time 0) commitment LP values:")
    for v, tl in vals[:10]:
        print(round(v, 6), tl)
