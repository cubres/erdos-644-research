"""Fano-with-requests on note 7.79: which sets of 'actual' lines suffice (others need mass < tau*)?"""
import itertools, numpy as np
from scipy.optimize import linprog
T9 = np.array([[0,54,26],[1,62,17],[8,43,29],[19,0,61],[28,1,51],[31,4,45],[44,32,4],[51,29,0],[58,21,1]], float)/80
x = np.array([513/8]*3)/80; tau = 483/640
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
def solve(assign):  # assign: dict line-> type index; others light; minimise max light mass
    nv = 21 + 1
    A = []; b = []; Aeq = []; beq = []
    for i in range(3):
        r = np.zeros(nv); r[[p*3+i for p in range(7)]] = 1; Aeq.append(r); beq.append(x[i])
    for li, l in enumerate(LINES):
        if li in assign:
            t = T9[assign[li]]
            for i in range(3):
                r = np.zeros(nv); r[[p*3+i for p in l]] = 1; A.append(r); b.append(x[i]-t[i])
        else:
            r = np.zeros(nv); r[[p*3+i for p in l for i in range(3)]] = 1; r[21] = -1; A.append(r); b.append(0)
    c = np.zeros(nv); c[21] = 1
    res = linprog(c, A_ub=np.array(A), b_ub=b, A_eq=np.array(Aeq), b_eq=beq, bounds=[(0,None)]*21+[(None,None)], method='highs')
    return res.fun if res.status == 0 else None
best = {}
for k in range(1, 8):
    for S in itertools.combinations(range(7), k):
        pts = set().union(*[set(LINES[l]) for l in S])
        for types in itertools.product(range(9), repeat=k):
            v = solve(dict(zip(S, types)))
            if v is not None and (k not in best or v < best[k][0]): best[k] = (v, S, types)
    print(k, best.get(k), 'tau*', tau, flush=True)
    if k >= 4: break
