"""Referee w9 (typeclosed#1): independent EXACT strict Fourier-Motzkin certificate for GGP and GGP-mass.

Variables (parts j,k only): aj, ak, bj, bk, xj, xk.
Base:  all >= 0;  unit-mass version: aj+ak <= 1, bj+bk <= 1 (rest of the mass sits in other parts);
       mass version: no mass bound, gap measured against m_a = aj+ak and m_b = bj+bk.
Hyp:   H1: 4xk < 7ak;  H2: 4xj < 7bj;  G: (xj-bj)+(xk-ak) > 3/4  (or >= / mass variants).
Negation of the conclusion restricted to parts j,k: some facet of Q_b fails in j or k, AND some facet of
Q_a fails, AND some facet of V fails.  (Other parts are handled by condition L, checked separately below.)
Q_b(s,t)=max(3t/2, s+3t/4) [s=a-load, t=b-load]; Q_a(s,t)=max(3s/2, t+3s/4); V(s,t)=max(s+t, 5s/4+t/2).
Each of the 4*4*4 = 64 combinations is a system of linear (strict/non-strict) inequalities; we show each is
infeasible by exact FM elimination with strictness tracking.  Also mutation tests (drop / weaken a hypothesis)
to show the certificate is sensitive.
"""
from fractions import Fraction as F
from itertools import product

V_ = ['aj', 'ak', 'bj', 'bk', 'xj', 'xk']


def lin(**kw):
    return {k: F(v) for k, v in kw.items()}


def le(coef, rhs, strict=False):
    """sum coef*v (<|<=) rhs"""
    return (dict(coef), F(rhs), strict)


def ge(coef, rhs, strict=False):
    return ({k: -v for k, v in coef.items()}, -F(rhs), strict)


def fm_feasible(rows, vars_=V_):
    rows = list(rows)
    for s in vars_:
        pos = [r for r in rows if r[0].get(s, 0) > 0]
        neg = [r for r in rows if r[0].get(s, 0) < 0]
        new = [r for r in rows if r[0].get(s, 0) == 0]
        for (cp, rp, sp_) in pos:
            for (cn, rn, sn) in neg:
                a, b = cp[s], -cn[s]
                coef = {k: cp.get(k, 0) * b + cn.get(k, 0) * a for k in set(cp) | set(cn)}
                coef.pop(s, None)
                coef = {k: v for k, v in coef.items() if v != 0}
                new.append((coef, rp * b + rn * a, sp_ or sn))
        # dedupe: keep tightest per normalised direction
        best = {}
        for coef, rhs, st in new:
            if not coef:
                if rhs < 0 or (rhs == 0 and st):
                    return False
                continue
            m = max(abs(v) for v in coef.values())
            key = tuple(sorted((k, v / m) for k, v in coef.items()))
            r = rhs / m
            if key not in best or r < best[key][1] or (r == best[key][1] and st):
                best[key] = ({k: v / m for k, v in coef.items()}, r, st)
        rows = list(best.values())
    for coef, rhs, st in rows:
        if rhs < 0 or (rhs == 0 and st):
            return False
    return True


def base(unit_mass=True):
    R = [ge(lin(**{v: 1}), 0) for v in V_]
    if unit_mass:
        R += [le(lin(aj=1, ak=1), 1), le(lin(bj=1, bk=1), 1)]
    return R


H1 = ge(lin(ak=7, xk=-4), 0, True)          # 7ak - 4xk > 0
H2 = ge(lin(bj=7, xj=-4), 0, True)


def G(c=F(3, 4), strict=True):              # xj-bj+xk-ak > c
    return ge(lin(xj=1, bj=-1, xk=1, ak=-1), c, strict)


def Gmass(strict=True, c=F(3, 4)):          # gap > c*m_a and gap > c*m_b
    return [ge({'xj': F(1), 'bj': F(-1) - c, 'xk': F(1), 'ak': F(-1)}, 0, strict) if False else
            ge({'xj': F(1), 'bj': F(-1), 'xk': F(1), 'ak': F(-1) - c, 'aj': -c}, 0, strict),
            ge({'xj': F(1), 'bj': F(-1) - c, 'xk': F(1), 'ak': F(-1), 'bk': -c}, 0, strict)]


def fail(s_coef, t_coef, part):
    """facet  s_coef*a_part + t_coef*b_part > x_part"""
    return ge({'a' + part: F(s_coef), 'b' + part: F(t_coef), 'x' + part: F(-1)}, 0, True)


QB = [(0, F(3, 2)), (1, F(3, 4))]           # (s,t) coefficient pairs of facets
QA = [(F(3, 2), 0), (F(3, 4), 1)]
VV = [(1, 1), (F(5, 4), F(1, 2))]


def neg_systems():
    fb = [fail(s, t, p) for p in 'jk' for (s, t) in QB]
    fa = [fail(s, t, p) for p in 'jk' for (s, t) in QA]
    fv = [fail(s, t, p) for p in 'jk' for (s, t) in VV]
    return list(product(fb, fa, fv))


def run(hyps, unit_mass=True):
    feas = 0
    for combo in neg_systems():
        if fm_feasible(base(unit_mass) + hyps + list(combo)):
            feas += 1
    return feas


def light_part_check():
    """Part i with L: 3a/2<=x, 3b/2<=x, a+b<=x, a,b>=0: every facet of Q_b,Q_a,V holds."""
    vs = ['a', 'b', 'x']
    L = [ge({'a': F(1)}, 0), ge({'b': F(1)}, 0),
         le({'a': F(3, 2), 'x': F(-1)}, 0), le({'b': F(3, 2), 'x': F(-1)}, 0), le({'a': F(1), 'b': F(1), 'x': F(-1)}, 0)]
    bad = 0
    for (s, t) in QB + QA + VV:
        if fm_feasible(L + [ge({'a': F(s), 'b': F(t), 'x': F(-1)}, 0, True)], vs):
            bad += 1
    return bad


if __name__ == '__main__':
    # sanity of the FM routine
    assert fm_feasible([ge({'aj': F(1)}, 0, True), le({'aj': F(1)}, 0)], ['aj']) is False
    assert fm_feasible([ge({'aj': F(1)}, 0), le({'aj': F(1)}, 0)], ['aj']) is True
    print('GGP (unit mass, G strict): feasible negation systems =', run([H1, H2, G()]))
    print('GGP (unit mass, G NON-strict >= 3/4): feasible =', run([H1, H2, G(strict=False)]))
    print('GGP-mass (G > (3/4)max(m_a,m_b), no mass bound): feasible =', run([H1, H2] + Gmass(), unit_mass=False))
    print('GGP-mass (non-strict): feasible =', run([H1, H2] + Gmass(strict=False), unit_mass=False))
    print('light part L => all 6 facets: failures =', light_part_check())
    # mutations (should give feasible negation systems, i.e. certificate is sensitive)
    print('MUT drop H1:', run([H2, G()]))
    print('MUT drop H2:', run([H1, G()]))
    print('MUT G > 3/4 - 1/1000:', run([H1, H2, G(F(3, 4) - F(1, 1000))]))
    print('MUT mass: G > (3/4 - 1/1000) max m:', run([H1, H2] + Gmass(c=F(3, 4) - F(1, 1000)), unit_mass=False))
    print('MUT mass: G > (3/4) min(m) only [only m_a term]:', run([H1, H2] + Gmass()[:1], unit_mass=False),
          '[only m_b term]:', run([H1, H2] + Gmass()[1:], unit_mass=False))
    print('MUT H1 weakened to 4xk < (7+1/100)ak:', run([ge(lin(ak=F(7) + F(1, 100), xk=-4), 0, True), H2, G()]))
