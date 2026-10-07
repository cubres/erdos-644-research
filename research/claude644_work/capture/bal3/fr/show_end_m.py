import sys, numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3')
from frlib import *
import b3lib
exec(open('inspect_end.py').read().split('for fn in sys.argv[1:]:')[0])
names = ['p0','a','a2','b','b2','c','c2']
for fn in sys.argv[1:]:
    r = parse(fn)
    if r is None: continue
    x, T = r; ts = b3lib.tau_star(x, T)
    (bm, basg), allok = p1_best(x, T, ts, True)
    allok.sort(key=lambda z: -z[0])
    for mg, a in allok[:2]:
        v, m = fr_lp(x, T, a, True)
        print(fn, 'x', np.round(x, 3), 'tau*', round(ts, 4), 'margin %.4f' % mg, 'asg', a)
        for li in range(4): print('    line', LINES[li], np.round(T[a[li]], 3))
        for q in range(7): print('    ', names[q], np.round(m[q], 4))
        for li in range(4, 7): print('    light', LINES[li], round(m[list(LINES[li])].sum(), 4))
