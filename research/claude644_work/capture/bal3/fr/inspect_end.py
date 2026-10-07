import sys, json, re, numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3')
from frlib import *
import b3lib
def parse(fn):
    s = open(fn).read(); i = s.rfind('END')
    if i < 0: return None
    xs = s[i:]; x = eval(xs[xs.index('x [')+2: xs.index('] T')+1]); T = eval(xs[xs.index('T [')+2:].strip())
    return x, T
for fn in sys.argv[1:]:
    r = parse(fn)
    if r is None: continue
    x, T = r; ts = b3lib.tau_star(x, T); S, sig, e = b3lib.regime(x, T)
    cls = lambda j: ''.join('ABC'[i] for i in range(3) if j in S[i])
    print(fn, 'x', np.round(x, 3), 'tau*', round(ts, 4), 'sigma', np.round(sig, 3), 'e', np.round(e, 3))
    for j, t in enumerate(T):
        tags = [f'min{"ABC"[i]}' for i in range(3) if j in S[i] and abs(t[i]-sig[i]) < 1e-9]
        for Y in range(3):
            for X in range(3):
                if X != Y and j in S[Y] and abs(t[X] - min(T[k][X] for k in S[Y])) < 1e-9: tags.append(f'd{"ABC"[Y]}{"ABC"[X]}')
        print('   type', j, cls(j), np.round(t, 4), tags)
    (bm, basg), allok = p1_best(x, T, ts, True)
    allok.sort(key=lambda z: -z[0])
    for mg, a in allok[:8]:
        print('   P1 margin %.4f' % mg, 'pencil', a[:3], [cls(j) for j in a[:3]], 'q1', a[3], cls(a[3]))
    print('   pair', round(b3lib.pair_margin(x, T), 4), 'V', b3lib.v_margin(x, T))
