"""grid scan: margin of the best template when ONE new type c (grid over the class regions) is added to an
adversary's roles; then list boxes u (cost <= tau) all of whose grid types have margin < 0 ("killing requests").
usage: python3 scan2.py adv.json [h=0.02]"""
import sys, os, json, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from scan import best_margin, load_adv

x, tau, R, v = load_adv(sys.argv[1])
h = float(sys.argv[2]) if len(sys.argv) > 2 else 0.02
sig = np.array([v['s0'], v['s1'], v['s2']])
U = {}
for n, c in R.items():
    if not any(np.allclose(c, c2) for c2 in U.values()): U[n] = c
R = U
print('x', x.round(4), 'tau', round(tau, 4), 'sigma', sig.round(4), 'roles', {n: c.round(3).tolist() for n, c in R.items()})
pts = []
for a in np.arange(0, x[0] + 1e-9, h):
    for b in np.arange(0, x[1] + 1e-9, h):
        c = np.array([a, b, 1 - a - b])
        if c[2] < -1e-12 or c[2] > x[2] + 1e-12: continue
        c[2] = max(c[2], 0)
        if not any(c[i] >= sig[i] - 1e-12 for i in range(3)): continue
        R2 = dict(R); R2['T'] = c
        pts.append((c, best_margin(R2, x, tau, fk=5, rk=4)))
print('grid types', len(pts), 'surviving (margin >= 0):', sum(1 for c, m in pts if m[0] >= 0))
for c, m in pts:
    if m[0] >= 0: print('  survivor', c.round(3), round(m[0], 4))
json.dump([[c.tolist(), m[0], m[1]] for c, m in pts], open(sys.argv[1].replace('.json', '_scan2.json'), 'w'))
