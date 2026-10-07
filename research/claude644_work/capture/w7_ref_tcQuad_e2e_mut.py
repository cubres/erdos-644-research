"""Mutation test for w7_ref_tcQuad_e2e.py: weaken the third request bound to r3 <= c (dropping
2c - r1 - r2) or the second to r2 <= c; the end-to-end checker must then find failures."""
import random, sys
from fractions import Fraction as F
import w7_ref_tcQuad_e2e as M
def run(mode, seed=5, trials=3000):
    rng = random.Random(seed); fails = 0; tot = 0
    for tr in range(trials):
        p = rng.randint(1, 3); R = rng.choice([4, 8, 12])
        X = [rng.randint(1, 2 * R) for _ in range(p)]
        e = M.rand_below(X, rng, R)
        if e is None: continue
        c = [min(xi, 2*xi - 2*ei) for xi, ei in zip(X, e)]
        r1 = M.rand_below(c, rng, R)
        if r1 is None: continue
        B2 = c if mode == 'r2' else [int(F(ci) - F(a, 2)) for ci, a in zip(c, r1)]
        r2 = M.rand_below(B2, rng, R)
        if r2 is None: continue
        B3 = c if mode == 'r3' else [min(ci, 2*ci - a - b) for ci, a, b in zip(c, r1, r2)]
        r3 = M.rand_below(B3, rng, R)
        if r3 is None: continue
        rows = {l: e for l in M.QUAD}; rows[M.PENC[0]] = r1; rows[M.PENC[1]] = r2; rows[M.PENC[2]] = r3
        res, s = M.build_and_check(X, R, rows); tot += 1
        fo = all(M.formula_ok([rows[l][i] for l in range(7)], X[i]) for i in range(p))
        if res != 'BAD_OK': fails += 1
        assert (res == 'BAD_OK') == fo or res == 'NO_INTEGER_REALISATION' and not fo, (res, fo)
    print('mutation', mode, ': failures', fails, 'of', tot, '(formula and MILP agree)')
run('r3'); run('r2')
