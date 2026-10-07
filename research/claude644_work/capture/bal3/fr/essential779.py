"""Exact tau* of note 7.79 and of all single-deletion / pair-deletion subfamilies (blocking-map enumeration).
tau*(C) = min over maps pi (type -> part, c_{pi(c)}>0) of sum_{i in image} (x_i - min_{pi(c)=i} c_i)."""
import itertools
from fractions import Fraction as F
T9 = [[0,54,26],[1,62,17],[8,43,29],[19,0,61],[28,1,51],[31,4,45],[44,32,4],[51,29,0],[58,21,1]]
T9 = [[F(v, 80) for v in t] for t in T9]
x = [F(513, 640)] * 3
def taustar(C):
    best = None
    for pi in itertools.product(range(3), repeat=len(C)):
        if any(C[k][pi[k]] == 0 for k in range(len(C))): continue
        cost = F(0)
        for i in range(3):
            m = [C[k][i] for k in range(len(C)) if pi[k] == i]
            if m: cost += x[i] - min(m)
        if best is None or cost < best: best = cost
    return best
full = taustar(T9); print('tau*(C) =', full, float(full))
sig = [min(t[i] for t in T9 if t[i] > 2*x[i]/3) for i in range(3)]
print('sigma', sig, 'e', [x[i]-sig[i] for i in range(3)], 'classes', [[k for k,t in enumerate(T9) if t[i] >= sig[i]] for i in range(3)])
for k in range(9):
    C = [t for j, t in enumerate(T9) if j != k]
    v = taustar(C); print('drop', k, T9[k], 'tau* =', v, float(v), 'ESSENTIAL' if v <= F(3,4) else 'inessential')
print('3-subsets with tau*>3/4:', [S for S in itertools.combinations(range(9), 3) if taustar([T9[k] for k in S]) > F(3,4)])
best = max(((taustar([T9[k] for k in S]), S) for S in itertools.combinations(range(9), 3)))
print('best triple', best, float(best[0]))
b4 = max(((taustar([T9[k] for k in S]), S) for S in itertools.combinations(range(9), 4))); print('best 4-subset', b4, float(b4[0]))
