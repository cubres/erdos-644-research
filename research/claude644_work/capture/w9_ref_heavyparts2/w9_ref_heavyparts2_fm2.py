"""heavyparts#2: follow-ups to the FM audit: (a) drop BOTH Lt hypotheses; (b) sub-claims with Lt dropped;
(c) explicit rational witnesses (HiGHS max-slack LP, then exact re-check) for every drop probe that FM says fails."""
import itertools, sys
sys.argv = ['x']
exec(open('w9_ref_heavyparts2_fm.py').read().split("out = []")[0])
from scipy.optimize import linprog
import numpy as np
def witness(rows):
    # maximise eps s.t. f + eps*[strict] <= c
    n = len(V); A = []; b = []
    for coef, rhs, st in rows:
        A.append([float(coef.get(v, 0)) for v in V] + [1.0 if st else 0.0]); b.append(float(rhs))
    r = linprog(c=[0]*n + [-1], A_ub=A, b_ub=b, bounds=[(0, 5)]*n + [(0, 1)], method='highs')
    if r.status != 0 or r.x[-1] <= 1e-9: return None
    pt = {v: F(r.x[i]).limit_denominator(2000) for i, v in enumerate(V)}
    ok = all((sum(c.get(v, 0)*pt[v] for v in V) < rhs) if st else (sum(c.get(v, 0)*pt[v] for v in V) <= rhs) for c, rhs, st in rows)
    return pt, ok
print('(a) drop LtA and LtB:', main_claim(drop=('LtA', 'LtB'))[:6])
print('(b) Q_alpha failing facets w/o Lt:', [k for k in QA if fm(hyps(drop=('LtA','LtB')) + [neg(*QA[k])])])
print('    Q_beta failing facets w/o Lt:', [k for k in QB if fm(hyps(drop=('LtA','LtB')) + [neg(*QB[k])])])
for d in ['H2', 'H1', 'suma', 'sumb', 'G', ('LtA', 'LtB')]:
    dd = d if isinstance(d, tuple) else (d,)
    for combo in main_claim(drop=dd)[:1]:
        rows = hyps(drop=dd) + [neg(*QA[combo[0]]), neg(*QB[combo[1]]), neg(*VB[combo[2]])]
        w = witness(rows)
        print('   drop', dd, combo, '->', None if w is None else ({k: str(v) for k, v in w[0].items()}, 'exact ok' if w[1] else 'rounding broke it'))
