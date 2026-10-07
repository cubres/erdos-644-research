# random cross-check: lazy mixed-Fano LP value == max(max w, max pencil/2, total/4)
import random, numpy as np
from scipy.optimize import linprog
L=[frozenset(s) for s in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]
rng=random.Random(2); worst=0
for t in range(20000):
    w=[rng.random()**rng.choice([1,3,6]) for _ in range(7)]
    A=[[-(1 if p not in L[l] else 0) for p in range(7)] for l in range(7)]
    res=linprog(np.ones(7),A_ub=A,b_ub=[-v for v in w],bounds=(0,None),method='highs')
    crit=max(max(w),max(sum(w[l] for l in range(7) if q in L[l]) for q in range(7))/2,sum(w)/4)
    worst=max(worst,abs(res.fun-crit))
print('max |LP - criterion| over 20000 random load vectors:',worst)
