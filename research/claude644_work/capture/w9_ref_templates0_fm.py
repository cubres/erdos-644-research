"""Referee w9 [templates#0]: tiny exact Fourier-Motzkin with strict inequalities (Fractions).
A constraint is (coef dict var->Fraction, rhs Fraction, strict bool) meaning sum coef*v <= rhs (or < if strict).
fm_feasible(cons, vars) -> True/False exactly (real feasibility)."""
from fractions import Fraction as F

def _norm(c):
    coef, rhs, st = c
    coef = {k: F(v) for k, v in coef.items() if v != 0}
    return (coef, F(rhs), st)

def fm_feasible(cons, vars_):
    cons = [_norm(c) for c in cons]
    for v in vars_:
        pos, neg, zero = [], [], []
        for c in cons:
            a = c[0].get(v, F(0))
            (pos if a > 0 else neg if a < 0 else zero).append(c)
        new = list(zero)
        for (cp, rp, sp) in pos:
            ap = cp[v]
            for (cn, rn, sn) in neg:
                an = -cn[v]
                coef = {}
                for k, val in cp.items():
                    coef[k] = coef.get(k, F(0)) + val / ap
                for k, val in cn.items():
                    coef[k] = coef.get(k, F(0)) + val / an
                coef.pop(v, None)
                coef = {k: val for k, val in coef.items() if val != 0}
                new.append((coef, rp / ap + rn / an, sp or sn))
        # dedupe: keep tightest per coefficient vector
        best = {}
        for coef, rhs, st in new:
            key = tuple(sorted(coef.items()))
            if key not in best:
                best[key] = (coef, rhs, st)
            else:
                _, r0, s0 = best[key]
                if rhs < r0 or (rhs == r0 and st and not s0):
                    best[key] = (coef, rhs, st)
        cons = list(best.values())
        for coef, rhs, st in cons:
            if not coef and (rhs < 0 or (rhs == 0 and st)):
                return False
    for coef, rhs, st in cons:
        assert not coef
        if rhs < 0 or (rhs == 0 and st):
            return False
    return True

def le(coef, rhs):
    return (coef, F(rhs), False)

def lt(coef, rhs):
    return (coef, F(rhs), True)

def lin(**kw):
    return {k: F(v) for k, v in kw.items()}

if __name__ == "__main__":
    # sanity
    assert fm_feasible([lt({'x': 1}, 0), lt({'x': -1}, 0)], ['x']) is False
    assert fm_feasible([le({'x': 1}, 0), le({'x': -1}, 0)], ['x']) is True
    assert fm_feasible([lt({'x': 1, 'y': 1}, 1), le({'x': -1}, 0), le({'y': -1}, -1)], ['x', 'y']) is False
    assert fm_feasible([le({'x': 1, 'y': 1}, 1), le({'x': -1}, 0), le({'y': -1}, -1)], ['x', 'y']) is True
    print("fm sanity ok")
