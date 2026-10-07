import sys; sys.path.insert(0,'.')
import numpy as np, itertools
from suppmilp import support_milp
x = np.array([0.75,0.75,0.75]); th = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
step = 1/20
types = []
for a in np.arange(0, 0.75+1e-9, step):
    for b in np.arange(0, 0.75+1e-9, step):
        c = 1 - a - b
        if c < -1e-9 or c > 0.75+1e-9: continue
        t = np.array([a,b,max(c,0)])
        if t.max() >= th - 1e-9: types.append(t)
types = np.array(types); print(len(types))
r = support_milp(types, x, time_limit=200)
print('lambda', r[0] if r else None, r[1] if r else None, [types[i].round(3).tolist() for i in set(r[1])] if r else None)
