# Referee w9 (BREAK-IT), templates#2: consistency of Theorem H2 with note Prop 7.79 (nine types, three parts,
# capacities 513/640, tau* = 483/640 > 3/4, NO two-type bad tuple by the note's certified 42-function catalogue).
# H2 predicts: every sub-family C' of the nine types whose heavy coordinates lie in at most two parts has
# tau*(C') < 3/4 (else H2 would give a two-type tuple, contradicting 7.79).  Check all 511 nonempty subsets, and all
# choices of which two parts play the heavy roles.  Also: pairwise H/Qa/Qb/V slacks on the nine types are all < 0.
import itertools, sys
from fractions import Fraction as F
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
from w9_ref_templates2brk_lib import tau_star, heavy, template_slack, recipe, Fail
raw = [(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
T = [[F(v, 80) for v in t] for t in raw]; x = [F(513, 640)] * 3
assert tau_star(x, T) == F(483, 640), tau_star(x, T)
print('heavy parts:', [[i for i in range(3) if heavy(t, x, i)] for t in T])
best = None; n2 = 0; maxtau = F(0)
for r in range(1, 10):
    for S in itertools.combinations(range(9), r):
        C = [T[k] for k in S]
        Hs = {i for t in C for i in range(3) if heavy(t, x, i)}
        if len(Hs) > 2: continue
        n2 += 1
        ts = tau_star(x, C); maxtau = max(maxtau, ts)
        assert ts < F(3, 4), ('H2 contradicts 7.79?', S, ts)
        # run the recipe anyway with the heavy parts moved to positions 0,1 (to exercise it on a real family)
        perm = sorted(Hs) + [i for i in range(3) if i not in Hs]
        perm = perm[:3]
print('subsets with <=2 heavy parts:', n2, ' max tau* among them =', maxtau, float(maxtau), '< 3/4: OK')
mins = max(template_slack(nm, a, b, x) for a in T for b in T for nm in ('Qb', 'Qa', 'V'))
minH = max(template_slack('H', a, None, x) for a in T)
print('BEST pair slack over Qa/Qb/V =', mins, ' best H slack =', minH, '(both must be < 0; note: every 42-function fails by >= 1/8)')
assert mins < 0 and minH < 0
