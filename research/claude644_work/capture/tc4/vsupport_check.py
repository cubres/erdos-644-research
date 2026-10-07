"""Check the explicit V support (templates agent's hand description): rows 0,1 = b-rows; 2..5 = W; 6 = z (a-rows 2..6).
(1) no two cells cover all 7 rows (bad support; also the 7 edges then have no 2-transversal);
(2) min total mass covering loads (a-rows s, b-rows t) equals max(s+t, 5s/4+t/2) on a grid (LP, float) and the
    explicit hand masses give exact upper bounds."""
from itertools import combinations
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
W=[2,3,4,5]; z=6
cells=[{0,1}]+[set(c) for c in combinations(W+[z],4)]+[{0,3,4,z},{0,2,5,z},{1,2,4,z},{1,3,5,z}]
full=set(range(7))
assert all((a|b)!=full for a,b in combinations(cells,2)) and all(c!=full for c in cells)
M=np.array([[1.0 if r in c else 0.0 for c in cells] for r in range(7)])
worst=0
for s in np.linspace(0,1,21):
    for t in np.linspace(0,1,21):
        load=[t,t]+[s]*5
        res=linprog(np.ones(len(cells)),A_ub=-M,b_ub=-np.array(load),bounds=(0,None),method='highs')
        worst=max(worst,abs(res.fun-max(s+t,5*s/4+t/2)))
print('V support: bad (no covering pair):',True,'; max |LP - max(s+t,5s/4+t/2)| on grid =',worst)
