"""Referee w9 heavyparts#2: sup of G-gap (x_A-a_A)+(x_B-b_B) over PCL hypotheses (minus G) with ALL of
Q_alpha, Q_beta, V(beta,alpha) infeasible, per failure combo (LP, closed relaxation), and an exact rational witness."""
import itertools
from fractions import Fraction as F
from scipy.optimize import linprog
import numpy as np
import importlib.util
spec = importlib.util.spec_from_file_location('fm', '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/w9_ref_heavyparts2brk_fm.py')
fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
H = fm.hyps(drop=('G',))
best = (-1, None, None)
for ch in itertools.product(fm.QA.items(), fm.QB.items(), fm.VV.items()):
    cons = H + [c for _, c in ch]
    # coef.v + const (>=) 0 ; strict ones get margin eps=1e-6 ; maximise gap = xA-aA+xB-bB
    A = []; b = []
    for co, cc, st in cons:
        A.append([-float(a) for a in co]); b.append(float(cc) - (1e-6 if st else 0))
    c = -np.array([1, 1, -1, 0, 0, -1.0])
    r = linprog(c, A_ub=A, b_ub=b, bounds=[(0, 5)]*6, method='highs')
    if r.status == 0 and -r.fun > best[0]: best = (-r.fun, [k for k, _ in ch], r.x)
print('sup gap with all three templates failing ~', best[0], best[1])
print('point', best[2])
# exact one-parameter witness: gap = 3/4 - d, all three templates fail (d small positive)
import importlib.util as iu
s2 = iu.spec_from_file_location('e2e', '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/w9_ref_heavyparts2brk_e2e.py')
e2e = iu.module_from_spec(s2); s2.loader.exec_module(e2e)
for d in [F(1, 100), F(1, 1000), F(1, 10**6)]:
    xA, aA, bA = F(3, 2) - d, F(1), F(2, 3) - d
    xB, aB, bB = F(7, 12) + d, F(0), F(1, 3) + d
    assert 7*aA > 4*xA and 7*bB > 4*xB and 7*bA <= 4*xA and 7*aB <= 4*xB and aA + aB <= 1 and bA + bB <= 1
    P = [(xA, aA, bA), (xB, aB, bB)]
    print('d=%s gap=%s  QA %s QB %s V %s | LP: %s %s %s' % (d, (xA-aA)+(xB-bB), e2e.feas_exact(P, 'QA'), e2e.feas_exact(P, 'QB'),
          e2e.feas_exact(P, 'V'), e2e.feas_lp(P, 'QA'), e2e.feas_lp(P, 'QB'), e2e.feas_lp(P, 'V')))
