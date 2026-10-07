# Referee w9, templates#1: MUTATION tests (checker sensitivity + necessity of each ingredient of Theorem 2UB).
# Uses the explicit-construction checker of w9_ref_templates_2ub.py.  Each mutation should produce failures.
import random, sys
from fractions import Fraction as F
from w9_ref_templates_2ub import check_tuple, tau_756, in_upbox, sample
rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2])
fails = {'M1_thr_0.70': 0, 'M2_fill_own_part': 0, 'M3_no_V': 0, 'M4_no_Qa': 0, 'M5_no_Qb': 0}
ex = {}
n = {'M1': 0, 'main': 0}
tries = 0
while n['main'] < NT:
    tries += 1
    x, g, h = sample(rng, tries % 3)
    p = len(x)
    if sum(g) > 1 or sum(h) > 1: continue
    Is = [i for i in range(p) if 7 * g[i] > 4 * x[i]]; Js = [j for j in range(p) if 7 * h[j] > 4 * x[j]]
    if not Is or not Js: continue
    t = tau_756(x, [g, h])
    if t < F(7, 10): continue
    main = t >= F(3, 4)
    if main: n['main'] += 1
    else: n['M1'] += 1
    for I in Is:
        for J in Js:
            if I == J: continue
            a = list(g); a[J] += 1 - sum(g); b = list(h); b[I] += 1 - sum(h)
            adm = in_upbox(a, g, x) and in_upbox(b, h, x)
            res = {k: adm and check_tuple(k, x, a, b) for k in ('Qb', 'Qa', 'V')}
            if not main:
                if not any(res.values()): fails['M1_thr_0.70'] += 1; ex.setdefault('M1', (x, g, h, I, J, t))
                continue
            if not (res['Qb'] or res['Qa']): fails['M3_no_V'] += 1; ex.setdefault('M3', (x, g, h, I, J))
            if not (res['Qb'] or res['V']): fails['M4_no_Qa'] += 1
            if not (res['Qa'] or res['V']): fails['M5_no_Qb'] += 1
            # M2: fill the free mass at the generator's own heavy part instead (a' = g+(1-|g|)e_I, b' = h+(1-|h|)e_J)
            a2 = list(g); a2[I] += 1 - sum(g); b2 = list(h); b2[J] += 1 - sum(h)
            ok2 = in_upbox(a2, g, x) and in_upbox(b2, h, x) and any(check_tuple(k, x, a2, b2) for k in ('Qb', 'Qa', 'V'))
            if not ok2: fails['M2_fill_own_part'] += 1; ex.setdefault('M2', (x, g, h, I, J))
print('tries', tries, n, fails)
for k, v in ex.items(): print(k, [[str(z) for z in q] if isinstance(q, list) else str(q) for q in v])
