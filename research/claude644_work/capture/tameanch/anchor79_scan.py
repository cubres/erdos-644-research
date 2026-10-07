# Does an ANCHORED rule (K4 / Fano-labelled tuple with E0 as a line; TC at E0) kill the sparsified note-7.9 family
# H_c (intersecting, tau_c/k ~ 0.79 > 3/4 for c <= 0.25, NON-TAME for every partition by Theorem R+)?
# Typed-Janson maximin exponent (janson3.Config): > 0  =>  the configuration exists in H_c whp (Lemma TJ of
# notes_randomside).  Family: parts X,Y,Z caps (0.40,1.39,0.99) per k, types a=(0.2,0,0.8), b=(0,0.8,0.2), k-uniform.
# Usage: python3 anchor79_scan.py fano|tc  [c values...]
import sys, itertools, time
import numpy as np
sys.path.insert(0, '.')
from janson3 import fano_anchored, tc_anchored
CAPS = {0: 0.40, 1: 1.39, 2: 0.99}
TYPES = {'a': {0: 0.2, 1: 0.0, 2: 0.8}, 'b': {0: 0.0, 1: 0.8, 2: 0.2}}
mode = sys.argv[1]
cs = [float(x) for x in sys.argv[2:]] or [0.0, 0.05, 0.1, 0.2, 0.25]
TAUP = 0.78   # tau_c/k - margin (fam79.log: 0.79 for c<=0.25)
for anchor in ('a', 'b'):
    e_prof = TYPES[anchor]
    if mode == 'fano':
        rows = [l for l in range(7) if l != 0]
        assigns = list(itertools.product('ab', repeat=6))
        build = lambda asg: fano_anchored(CAPS, e_prof, {rows[i]: TYPES[asg[i]] for i in range(6)}, L0=0)
    else:
        assigns = list(itertools.product('ab', repeat=4))
        build = lambda asg: tc_anchored(CAPS, e_prof, {R: TYPES[asg[i]] for i, R in enumerate(['B1', 'B2', 'C1', 'C2'])}, TAUP)
    # stage 1: c = cs[0], all assignments, cheap solve; keep the best 4
    t0 = time.time(); res = []
    for asg in assigns:
        cfg = build(asg)
        b = cfg.solve(cs[0], tries=2, maxiter=600)
        val = b[0] if b is not None else -np.inf
        res.append((val, asg))
    res.sort(reverse=True)
    print(f'[{mode}] anchor={anchor} c={cs[0]}: {len(assigns)} assignments in {time.time()-t0:.0f}s; top: ' +
          ', '.join(f"{''.join(a)}:{v:+.3f}" for v, a in res[:6]), flush=True)
    top = [a for v, a in res[:4] if v > -np.inf]
    for c in cs[1:]:
        line = []
        for asg in top:
            cfg = build(asg); b = cfg.solve(c, tries=4, maxiter=1500)
            val = b[0] if b is not None else -np.inf
            wj = cfg.worstJ(b[1], c) if b is not None else None
            line.append(f"{''.join(asg)}:{val:+.4f}(J={wj})")
        print(f'[{mode}] anchor={anchor} c={c}: ' + '  '.join(line), flush=True)
