#!/usr/bin/env python3
"""Mutation tests for w9_ref_templates0_gap.py's FM engine: dropping a template or a hypothesis must
leave some system open (margin > 0 possible), otherwise the check would be vacuous."""
import itertools, importlib.util, sys
spec = importlib.util.spec_from_file_location('g', '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/w9_ref_templates0_gap.py')
src = open(spec.origin).read().split('# ---------------- (B)')[0]
ns = {}; exec(src.replace("b1 = run_gap", "#").replace("assert not b1", "").replace("b2 = run_gap", "#").replace("print('  (all-weak", "#print("), ns)
fm, hyp, Qb, Qa, V, viol, G = ns['fm_implies_g_nonpos'], ns['hyp_rows'], ns['facets_Qb'], ns['facets_Qa'], ns['facets_V'], ns['viol'], ns['G']
def count_open(templates, drop_hyp=None):
    n_open = 0; n = 0
    for fs in itertools.product(*templates):
        R = hyp(False, True)
        if drop_hyp is not None: R = [r for i, r in enumerate(R) if i != drop_hyp]
        R = R + [viol(f) for f in fs]; n += 1
        if not fm(R, 5, G): n_open += 1
    return n_open, n
print('drop V        :', count_open([Qb(), Qa()]))
print('drop Q_a      :', count_open([Qb(), V()]))
print('drop Q_b      :', count_open([Qa(), V()]))
for i, nm in [(5, 'H1'), (6, 'H2'), (7, 'G')]:
    print('drop hyp', nm, ':', count_open([Qb(), Qa(), V()], i))
