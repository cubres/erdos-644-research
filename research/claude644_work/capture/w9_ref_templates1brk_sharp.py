# [templates#1] BREAK-IT referee (w9): sharpness of the 3/4 hypothesis for the CANONICAL recipe of 2UB.
# Takes the role-reduced MILP optimum at threshold 0.74 (w9_ref_templates1brk_milp.py), adds one "rest" part with
# capacity 2 carrying g_rest,h_rest (all hypotheses involving it hold automatically), rationalises, and verifies
# EXACTLY (independent brute tau*) that tau* >= 37/50 while the canonical pair fails Q_b, Q_a and V.
import sys
from fractions import Fraction as F
sys.argv = ['x', '0.74']
src = open('w9_ref_templates1brk_milp.py').read().split('best = -9')[0]
exec(src)
import w9_ref_templates1brk_edge_lib as E
found = 0
for pat in set_partitions(['I', 'J', 'K', 'L', 'M']):
    val, st, sol = solve(pat, 'tmpl')
    if val is None or val < 1e-4: continue
    q = len(pat); roles = {r: bi for bi, blk in enumerate(pat) for r in blk}
    R = lambda v: F(v).limit_denominator(2000)
    x = [R(sol[f'x{i}']) for i in range(q)] + [F(2)]
    g = [R(sol[f'g{i}']) for i in range(q)] + [R(sol['grest'])]
    h = [R(sol[f'h{i}']) for i in range(q)] + [R(sol['hrest'])]
    if sum(g) > 1 or sum(h) > 1 or any(a > b for a, b in zip(g, x)) or any(a > b for a, b in zip(h, x)): continue
    t = E.tau_star(x, g, h)
    I, J = roles['I'], roles['J']
    if not (7 * g[I] > 4 * x[I] and 7 * h[J] > 4 * x[J]): continue
    a = list(g); a[J] += 1 - sum(g); b = list(h); b[I] += 1 - sum(h)
    adm = all(a[i] <= x[i] and b[i] <= x[i] for i in range(len(x)))
    fe = {k: all(E.formula(k, a[i], b[i]) <= x[i] for i in range(len(x))) for k in ['Qb', 'Qa', 'V']}
    if t >= F(37, 50) and adm and not any(fe.values()):
        found += 1
        print('pattern', pat, 'tau* =', t, float(t))
        print('  x =', [str(v) for v in x]); print('  g =', [str(v) for v in g]); print('  h =', [str(v) for v in h])
        print('  (I,J) =', (I, J), ' a =', [str(v) for v in a], ' b =', [str(v) for v in b], ' Qb/Qa/V feasible:', fe)
        if found >= 3: break
print('exact sharpness witnesses found:', found)
