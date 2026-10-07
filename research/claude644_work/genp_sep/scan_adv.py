"""scan_adv.py -- numeric diagnosis of an adversary of gen_certp (NOT a proof tool).
For a grid of candidate extra types t (unit, 0 <= t <= x, in exactly one heavy class: t_i >= sigma_i for its class i,
t_j <= 2x_j/3 elsewhere, light parts <= 2x_l/3), test whether some template over (valid roles + t) succeeds with margin
<= -tol.  Prints the surviving candidates (those that do NOT kill the adversary), grouped by class.
usage: python3 scan_adv.py certs/gadvp_<..>.json [step=0.02] [tol=1e-6]"""
import sys, json, itertools
import numpy as np
from fractions import Fraction as F
import gen_certp as GP

adv = json.load(open(sys.argv[1]))
kw = dict(a.split('=') for a in sys.argv[2:])
step = float(kw.get('step', 0.02)); tol = float(kw.get('tol', 1e-6))
spec = adv['spec']; S = GP.StratP(spec, F(adv['pi0']))
v = adv['v']
p, h = S.p, S.h
x = np.array([v['x%d' % i] for i in range(p)]); tau = v['tau']
sig = np.array([v['s%d' % i] for i in range(h)])
R = {n: np.array([v['c%s_%d' % (n, j)] for j in range(p)]) for n in S.names}
E = GP.EngineP(S)
vv = np.array([v[k] for k in S.VARS])
valid = [n for n in S.names if not E.is_void(n, vv)]
print('x', np.round(x, 4), 'tau %.5f' % tau, 'sigma', np.round(sig, 4), 'valid roles', valid)


def best(Rd, names):
    ev = GP.eval_templates(S, Rd, names, x, tau, top_f=1, top_r=1, top_w=1, tol=1.0)
    allm = [(m, nm) for k in ev for m, nm in ev[k][:1]]
    return min(allm) if allm else (9, None)


print('roles alone: best template', best(R, valid))
surv = []; tested = 0
grid = np.arange(0, 1 + 1e-9, step)
for cls in range(h):
    others = [j for j in range(p) if j != cls]
    for ti in grid:
        if ti < sig[cls] - 1e-12 or ti > x[cls] + 1e-12: continue
        rest = 1 - ti
        # distribute rest over the other parts on the grid
        for comb in itertools.product(grid, repeat=len(others) - 1):
            last = rest - sum(comb)
            if last < -1e-9: continue
            t = np.zeros(p); t[cls] = ti
            for j, val in zip(others[:-1], comb): t[j] = val
            t[others[-1]] = max(last, 0)
            ok = all(t[j] <= 2 * x[j] / 3 + 1e-12 for j in others)
            if not ok: continue
            tested += 1
            Rd = dict(R); Rd['T'] = t
            m, nm = best(Rd, valid + ['T'])
            if m > -tol: surv.append((cls, np.round(t, 3).tolist(), round(m, 5), nm))
print('tested %d candidates, %d survive' % (tested, len(surv)))
for s in surv[:60]: print(' ', s)
