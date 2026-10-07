"""Float vertex enumeration of P_D = {w>=0 : w(C)<=1 for maximal cells C} for the 715 bad-support orbits
(astra_full_support_catalog.json, read-only copy of logs).  Discovery; exact verification separate."""
import json, numpy as np, itertools, time
from scipy.spatial import HalfspaceIntersection
from fractions import Fraction as F
D = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_full_support_catalog.json'))
out = []
t0 = time.time()
for oi, orb in enumerate(D['orbits']):
    cells = orb['maximal_cells']
    H = []
    for C in cells:
        a = [1.0 if C >> j & 1 else 0.0 for j in range(7)]; H.append(a + [-1.0])
    for j in range(7):
        a = [0.0]*7; a[j] = -1.0; H.append(a + [0.0])
    H = np.array(H)
    hs = HalfspaceIntersection(H, np.full(7, 1/20))
    V = np.unique(np.round(hs.intersections, 9), axis=0)
    # rationalise
    VR = [[str(F(v).limit_denominator(1000)) for v in row] for row in V]
    out.append({'orbit': oi, 'cells': cells, 'vertices': VR})
    if oi % 100 == 0: print(oi, len(cells), len(V), round(time.time()-t0, 1), flush=True)
json.dump(out, open('supp_vertices_float.json', 'w'))
print('done', sum(len(o['vertices']) for o in out))
