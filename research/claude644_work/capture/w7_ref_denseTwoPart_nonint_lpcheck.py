#!/usr/bin/env python3
"""Cross-check (floating LP, HiGHS) of the non-intersecting instance e=100,x=140,G={(100,0),(5,94),(70,25)}:
for every assignment of types to the 6 non-anchor lines, LP feasibility of point masses (E0 all off L, sum=e;
O sum<=x; loads >= types).  Independent of Lemma 7.63's closed form."""
import itertools, numpy as np
from scipy.optimize import linprog
from w7_ref_denseTwoPart_lib import LINES, L, OFF, tau_star, intersecting
e, x = 100, 140; G = [(100,0),(5,94),(70,25)]
print('tau*', tau_star(G, e, x), 'intersecting', intersecting(G, e, x))
nonL = [i for i in range(7) if i != L]; feas = 0
for ass in itertools.product(G, repeat=6):
    A = []; b = []
    for k, i in enumerate(nonL):
        r = np.zeros(11)
        for j, p in enumerate(OFF):
            if p not in LINES[i]: r[j] = -1
        A.append(r); b.append(-ass[k][0])
        r = np.zeros(11)
        for p in range(7):
            if p not in LINES[i]: r[4+p] = -1
        A.append(r); b.append(-ass[k][1])
    r = np.zeros(11); r[4:] = 1; A.append(r); b.append(x)
    Aeq = [np.r_[np.ones(4), np.zeros(7)]]
    res = linprog(np.zeros(11), A_ub=np.array(A), b_ub=b, A_eq=np.array(Aeq), b_eq=[e], bounds=[(0,None)]*11, method='highs')
    feas += (res.status == 0)
print('feasible assignments:', feas, 'of', 3**6)
