"""[typeclosed#1] referee (BREAK-IT lens): exact strict Fourier-Motzkin verification of GGP / GGP-mass on parts j,k.

Variables: xj,xk,aj,ak,bj,bk (>=0) and M (mass bound).  Constraint = (coef dict, rhs, strict): sum coef*v (<|<=) rhs.
For each of the 4x4x4 = 64 ways to pick one violated per-part constraint of Q_b, Q_a, V (in part j or k), the system
  hypotheses + (the three violations)
must be infeasible.  Also: step (0) claims, and necessity probes (drop one hypothesis -> feasible violation).
Q_b (b on pencil, a on quad): per part 3b/2 <= x, a+3b/4 <= x.   Q_a mirror.   V: a+b <= x, 5a/4+b/2 <= x.
Independent code (no import from attacker scripts)."""
from fractions import Fraction as F
from itertools import product

VARS = ['xj', 'xk', 'aj', 'ak', 'bj', 'bk', 'M']

def C(d, rhs, strict=False):
    return ({k: F(v) for k, v in d.items() if F(v) != 0}, F(rhs), strict)

def ge(d, rhs, strict=False):  # sum d >= rhs  ->  -sum d <= -rhs
    return C({k: -F(v) for k, v in d.items()}, -F(rhs), strict)

def fm_feasible(cons, vars_=VARS):
    rows = list(cons)
    for v in vars_:
        pos = [r for r in rows if r[0].get(v, 0) > 0]
        neg = [r for r in rows if r[0].get(v, 0) < 0]
        new = [r for r in rows if r[0].get(v, 0) == 0]
        for cp, rp, sp in pos:
            for cn, rn, sn in neg:
                a, b = cp[v], -cn[v]
                coef = {}
                for kk in set(cp) | set(cn):
                    val = cp.get(kk, 0) * b + cn.get(kk, 0) * a
                    if kk != v and val != 0: coef[kk] = val
                new.append((coef, rp * b + rn * a, sp or sn))
        best = {}
        for coef, rhs, st in new:
            if not coef:
                if rhs < 0 or (rhs == 0 and st): return False
                continue
            m = max(abs(x) for x in coef.values())
            key = tuple(sorted((kk, x / m) for kk, x in coef.items()))
            r = rhs / m
            if key not in best or r < best[key][1] or (r == best[key][1] and st and not best[key][2]):
                best[key] = ({kk: x / m for kk, x in coef.items()}, r, st)
        rows = list(best.values())
    return all(not (rhs < 0 or (rhs == 0 and st)) for coef, rhs, st in rows)

def base(mass_version, drop=(), Gstrict=True):
    H = [ge({v: 1}, 0) for v in ['xj', 'xk', 'aj', 'ak', 'bj', 'bk']]
    if mass_version:
        H += [C({'aj': 1, 'ak': 1, 'M': -1}, 0), C({'bj': 1, 'bk': 1, 'M': -1}, 0)]
        if 'G' not in drop: H.append(ge({'xj': 1, 'bj': -1, 'xk': 1, 'ak': -1, 'M': F(-3, 4)}, 0, Gstrict))
    else:
        if 'mass' not in drop: H += [C({'aj': 1, 'ak': 1}, 1), C({'bj': 1, 'bk': 1}, 1)]
        H += [C({'M': 1}, 0), ge({'M': 1}, 0)]
        if 'G' not in drop: H.append(ge({'xj': 1, 'bj': -1, 'xk': 1, 'ak': -1}, F(3, 4), Gstrict))
    if 'H1' not in drop: H.append(C({'xk': 4, 'ak': -7}, 0, True))   # 4xk < 7ak
    if 'H2' not in drop: H.append(C({'xj': 4, 'bj': -7}, 0, True))   # 4xj < 7bj
    return H

def viol(d_x, lin):  # lin > x
    coef = {d_x: F(1)}
    for k, v in lin.items(): coef[k] = coef.get(k, 0) - F(v)
    return C(coef, 0, True)

def fails(template):
    out = []
    for part in 'jk':
        x, a, b = 'x' + part, 'a' + part, 'b' + part
        if template == 'Qb':
            out += [(part + ':3b/2', viol(x, {b: F(3, 2)})), (part + ':a+3b/4', viol(x, {a: 1, b: F(3, 4)}))]
        elif template == 'Qa':
            out += [(part + ':3a/2', viol(x, {a: F(3, 2)})), (part + ':b+3a/4', viol(x, {b: 1, a: F(3, 4)}))]
        else:
            out += [(part + ':a+b', viol(x, {a: 1, b: 1})), (part + ':5a/4+b/2', viol(x, {a: F(5, 4), b: F(1, 2)}))]
    return out

def failing(H):
    return [(n1, n2, n3) for (n1, c1), (n2, c2), (n3, c3) in product(fails('Qb'), fails('Qa'), fails('V'))
            if fm_feasible(H + [c1, c2, c3])]

if __name__ == '__main__':
    assert fm_feasible([C({'xj': 1}, 1, True), ge({'xj': 1}, 1)]) is False
    assert fm_feasible([C({'xj': 1}, 1), ge({'xj': 1}, 1)]) is True
    assert fm_feasible([C({'xj': 1, 'xk': 1}, 1), ge({'xj': 1}, F(1, 2), True), ge({'xk': 1}, F(1, 2))]) is False
    for mv in (False, True):
        for gs in (True, False):
            H = base(mv, Gstrict=gs)
            assert fm_feasible(H)
            bad = failing(H)
            print('GGP' + ('-mass' if mv else '') + (' (G strict)' if gs else ' (G non-strict)'),
                  ': all 64 failure combinations infeasible:', not bad, bad[:3])
            assert not bad
    H = base(True)
    for name, c in [('bj+ak>M', C({'bj': 1, 'ak': 1, 'M': -1}, 0)),
                    ('aj<bj', ge({'aj': 1, 'bj': -1}, 0)), ('bk<ak', ge({'bk': 1, 'ak': -1}, 0))]:
        print('step(0)', name, 'holds (mass version):', not fm_feasible(H + [c]))
    for tmpl, only in (('Qb', 'j:3b/2'), ('Qa', 'k:3a/2')):
        others = [n for n, c in fails(tmpl) if n != only and fm_feasible(H + [c])]
        print(tmpl, 'can fail only through', only, ':', others == [], others)
    for mv in (False, True):
        for d in (['G', 'H1', 'H2'] + ([] if mv else ['mass'])):
            print('drop', d, '(mass version)' if mv else '(mass-1 version)', ': failing combos', len(failing(base(mv, drop=(d,)))))
    for c in (F(3, 4) - F(1, 1000), F(3, 4) - F(1, 100)):
        H = base(False, drop=('G',)) + [ge({'xj': 1, 'bj': -1, 'xk': 1, 'ak': -1}, c, True)]
        print('G with constant', c, ': failing combos', len(failing(H)))
    print('DONE')
