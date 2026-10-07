"""Exact Fourier-Motzkin with strictness flags over the rationals.
Constraint: (coef dict var->Fraction, rhs Fraction, strict bool) meaning sum coef*v (< or <=) rhs."""
from fractions import Fraction as F
def _norm(rows):
    best = {}
    for coef, rhs, st in rows:
        nz = {k: v for k, v in coef.items() if v != 0}
        if not nz:
            if rhs < 0 or (rhs == 0 and st): return None      # 0 < 0 or 0 <= negative
            continue
        m = max(abs(v) for v in nz.values())
        key = tuple(sorted((k, v / m) for k, v in nz.items()))
        r = rhs / m
        if key not in best or r < best[key][1] or (r == best[key][1] and st and not best[key][2]):
            best[key] = ({k: v / m for k, v in nz.items()}, r, st)
    return list(best.values())
def feasible(rows, variables, maxrows=200000):
    rows = _norm([(dict(c), F(r), s) for c, r, s in rows])
    if rows is None: return False
    for v in variables:
        pos = [r for r in rows if r[0].get(v, 0) > 0]; neg = [r for r in rows if r[0].get(v, 0) < 0]
        new = [r for r in rows if r[0].get(v, 0) == 0]
        for cp, rp, sp in pos:
            for cn, rn, sn in neg:
                a, b = cp[v], -cn[v]
                coef = {k: cp.get(k, 0) * b + cn.get(k, 0) * a for k in set(cp) | set(cn)}
                coef.pop(v, None)
                new.append((coef, rp * b + rn * a, sp or sn))
        rows = _norm(new)
        if rows is None: return False
        if len(rows) > maxrows: raise RuntimeError("blowup")
    return True
