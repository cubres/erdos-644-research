"""Referee w9, claim typeclosed#0: Theorem L+ on specific extremal / literature families (exact).
Reuses the literal proof runner of w9_ref_typeclosed0_e2e.py (definitions only).
 (a) heavyparts H3-cex  x=(5/4,5/4,3/200): tiny part is EXACTLY 2/3-light (1/100 = 2(3/200)/3) -> L+ applies.
 (b) heavyparts H3*-cex x=(2449/2000,2449/2000,3/200), tau*=0.754.
 (c) note Prop 7.79 (nine types, rank 80, capacities 513/8): pair-free (no 2-type bad tuple) with tau*>3/4.
     L+ always outputs a 2-type tuple, so 7.79 MUST violate the hypothesis for every choice of {j,k}: check.
 (d) note W-family of 7.78 (types a,b over 3 parts, x=4/5 each) -- just classify.
 (e) complete family boundary: 1 part x=7/4 (tau*=3/4 exactly; theorem not applicable, but tuple exists).
"""
import sys, itertools
from fractions import Fraction as F
src = open(__file__.replace('_special.py', '_e2e.py')).read().split('# ---- generator')[0]
sys.argv = ['x', '0', '0']
exec(src)

def perm_run(X, C, R, label):
    p = len(X)
    tR = tau_R(X, C)
    print(f'--- {label}: X={X} R={R} tau*={F(tR, R)} (>3/4: {4*tR > 3*R})')
    ok_pairs = []
    for j, k in itertools.permutations(range(p), 2):
        rest = [i for i in range(p) if i not in (j, k)]
        if all(3 * c[i] <= 2 * X[i] for c in C for i in rest):
            ok_pairs.append((j, k))
    print('   hypothesis holds for (j,k) in', ok_pairs)
    for (j, k) in ok_pairs[:2]:
        order = [j, k] + [i for i in range(p) if i not in (j, k)]
        Xp = [X[i] for i in order]; Cp = [tuple(c[i] for i in order) for c in C]
        if 4 * tR > 3 * R:
            before = dict(stats)
            run_proof(Xp, Cp, R)
            print('   proof run OK with (j,k)=', (j, k), 'branch counts delta:',
                  {kk: stats[kk] - before[kk] for kk in stats})

perm_run([250, 250, 3], [(30, 170, 0), (170, 30, 0), (168, 30, 2)], 200, 'H3-cex')
perm_run([2449, 2449, 30], [(300, 1700, 0), (1700, 300, 0), (1680, 300, 20)], 2000, 'H3*-cex')
T79 = [(0, 54, 26), (1, 62, 17), (8, 43, 29), (19, 0, 61), (28, 1, 51), (31, 4, 45), (44, 32, 4), (51, 29, 0), (58, 21, 1)]
perm_run([513, 513, 513], [tuple(8 * v for v in c) for c in T79], 640, 'note 7.79 (rank 640)')
perm_run([80, 80, 80], [(54, 23, 23), (23, 54, 23)], 100, 'note 7.78 W pair (x=4/5)')
perm_run([7], [(4,)], 4, 'complete x=7/4')
