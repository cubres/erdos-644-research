#!/usr/bin/env python3
"""Referee w9, claim heavyparts#2 (Pair Chain Lemma).  EXACT strict Fourier-Motzkin (Fractions only).

Parts A, B and ONE light part j (more light parts only add nonnegative mass to the sum constraints and
their facet conditions are local, so one light part is the general case; a second-light-part run is
included as a sanity check).  Variables x_i, a_i (=alpha_i), b_i (=beta_i).

For every combination (failed facet of Q_alpha at some part, failed facet of Q_beta at some part,
failed facet of V(beta,alpha) at some part) the hypotheses + the three negations must be INFEASIBLE.

Templates (per part, s = load):
  Q_alpha (3 alpha rows on a pencil, 4 beta rows): 3a <= 2x ,  b + 3a/4 <= x      [also rows a<=x, b<=x,
           other points a+2b <= 2x: all implied, but included as facets anyway]
  Q_beta  mirror.
  V(beta,alpha) (5 beta rows, 2 alpha rows): a + b <= x ,  5b/4 + a/2 <= x.

Variants: G strict / non-strict; Lt included / dropped; light condition 4/7 vs 2/3 (+a+b<=x);
drop probes (H1, H2, G, sum<=1, Lj pair clause, Lj 4/7 clause) must become FEASIBLE for some combo.
"""
from fractions import Fraction as F
import itertools, sys

def fm(cons, nvar):
    """cons: list of (coef list, rhs, strict)  meaning coef.x < rhs (strict) or <= rhs.  Exact FM."""
    def norm(rows):
        best = {}
        for c, r, s in rows:
            nz = [i for i in range(nvar) if c[i] != 0]
            if not nz:
                if r < 0 or (r == 0 and s):
                    return None
                continue
            m = max(abs(c[i]) for i in nz)
            key = tuple(c[i] / m for i in range(nvar))
            rr = r / m
            if key not in best or rr < best[key][1] or (rr == best[key][1] and s and not best[key][2]):
                best[key] = (list(key), rr, s)
        return list(best.values())
    rows = norm(cons)
    if rows is None:
        return False
    for v in range(nvar):
        pos = [r for r in rows if r[0][v] > 0]
        neg = [r for r in rows if r[0][v] < 0]
        new = [r for r in rows if r[0][v] == 0]
        for cp, rp, sp in pos:
            for cn, rn, sn in neg:
                a, b = cp[v], -cn[v]
                c = [cp[i] * b + cn[i] * a for i in range(nvar)]
                c[v] = F(0)
                new.append((c, rp * b + rn * a, sp or sn))
        rows = norm(new)
        if rows is None:
            return False
        if len(rows) > 20000:
            raise RuntimeError('blowup')
    return True

def build(nlight=1, Gstrict=True, Lt=True, light='4/7', drop=()):
    parts = ['A', 'B'] + ['j%d' % t for t in range(nlight)]
    names = []
    for p in parts:
        names += ['x' + p, 'a' + p, 'b' + p]
    idx = {n: i for i, n in enumerate(names)}
    nv = len(names)
    def le(d, rhs=0, strict=False):   # sum d[k]*k <= rhs
        c = [F(0)] * nv
        for k, v in d.items():
            c[idx[k]] += F(v)
        return (c, F(rhs), strict)
    H = []
    for p in parts:
        H += [le({'a' + p: -1}), le({'b' + p: -1}), le({'x' + p: -1}, 0, True)]
    if 'sum' not in drop:
        H.append(le({'a' + p: 1 for p in parts}, 1))
        H.append(le({'b' + p: 1 for p in parts}, 1))
    if 'H2' not in drop:
        H.append(le({'xA': 4, 'aA': -7}, 0, True))          # 7aA > 4xA
    if 'H1' not in drop:
        H.append(le({'xB': 4, 'bB': -7}, 0, True))          # 7bB > 4xB
    if 'G' not in drop:
        H.append(le({'xA': -1, 'aA': 1, 'xB': -1, 'bB': 1}, F(-3, 4), Gstrict))
    if Lt:
        H.append(le({'bA': 7, 'xA': -4}))
        H.append(le({'aB': 7, 'xB': -4}))
    for p in parts[2:]:
        if light == '4/7':
            if 'L47' not in drop:
                H += [le({'a' + p: 7, 'x' + p: -4}), le({'b' + p: 7, 'x' + p: -4})]
        elif light == '2/3':
            H += [le({'a' + p: 3, 'x' + p: -2}), le({'b' + p: 3, 'x' + p: -2})]
        if 'Lpair' not in drop:
            H.append(le({'a' + p: 1, 'b' + p: 1, 'x' + p: -1}))
    # facets as (dict for lhs - x <= 0) ; negation: lhs - x > 0  i.e.  -(lhs-x) < 0
    def facets_Q(s, t, p):   # s = three-row (pencil) type, t = four-row type
        X = 'x' + p
        return [{s + p: 3, X: -2}, {t + p: 1, s + p: F(3, 4), X: -1},
                {s + p: 1, X: -1}, {t + p: 1, X: -1}, {s + p: 1, t + p: 2, X: -2},
                {s + p: 3, t + p: 4, X: -4}]
    def facets_V(s, t, p):   # s = five-row type, t = two-row type
        X = 'x' + p
        return [{s + p: 1, t + p: 1, X: -1}, {s + p: F(5, 4), t + p: F(1, 2), X: -1}]
    Qa = [(p, f) for p in parts for f in facets_Q('a', 'b', p)]
    Qb = [(p, f) for p in parts for f in facets_Q('b', 'a', p)]
    Vba = [(p, f) for p in parts for f in facets_V('b', 'a', p)]
    def neg(f):
        return le({k: -v for k, v in f.items()}, 0, True)
    return H, Qa, Qb, Vba, neg, nv

def run(label, expect_infeasible=True, V=None, **kw):
    H, Qa, Qb, Vba, neg, nv = build(**kw)
    if V is not None:
        Vba = V(kw)
    feas = []
    n = 0
    for (pa, fa), (pb, fb), (pv, fv) in itertools.product(Qa, Qb, Vba):
        n += 1
        if fm(H + [neg(fa), neg(fb), neg(fv)], nv):
            feas.append((pa, fa, pb, fb, pv, fv))
    ok = (len(feas) == 0) == expect_infeasible
    print('%-62s combos=%4d feasible=%4d  -> %s' % (label, n, len(feas), 'PASS' if ok else 'UNEXPECTED'))
    if feas and not expect_infeasible:
        print('     e.g.', feas[0])
    sys.stdout.flush()
    return ok

if __name__ == '__main__':
    allok = True
    allok &= run('PCL as stated (G strict, Lt, 4/7 & a+b<=x), 1 light part')
    allok &= run('PCL, G NON-strict')
    allok &= run('PCL WITHOUT Lt (Lt redundant?)', Lt=False)
    allok &= run('PCL without Lt, G non-strict', Lt=False, Gstrict=False)
    allok &= run('PCL, 2 light parts', nlight=2)
    allok &= run('light 2/3 & a+b<=x (GGP-L form), no Lt', Lt=False, light='2/3')
    allok &= run('light: only a+b<=x (no 4/7 clause) -> expect feasible', expect_infeasible=False, Lt=True, drop=('L47',))
    allok &= run('light: only 4/7 (no pair clause) -> expect feasible', expect_infeasible=False, drop=('Lpair',))
    allok &= run('drop H1 -> expect feasible', expect_infeasible=False, drop=('H1',))
    allok &= run('drop H2 -> expect feasible', expect_infeasible=False, drop=('H2',))
    allok &= run('drop G -> expect feasible', expect_infeasible=False, drop=('G',))
    allok &= run('drop sum<=1 -> expect feasible', expect_infeasible=False, drop=('sum',))
    allok &= run('drop H1 AND Lt -> expect feasible', expect_infeasible=False, drop=('H1',), Lt=False)
    # V orientation: V(alpha,beta) instead of V(beta,alpha)
    def Vab(kw):
        H, Qa, Qb, Vba, neg, nv = build(**kw)
        parts = sorted(set(p for p, _ in Vba), key=lambda p: (p not in ('A', 'B'), p))
        out = []
        for p in parts:
            X = 'x' + p
            out += [(p, {'a' + p: 1, 'b' + p: 1, X: -1}), (p, {'a' + p: F(5, 4), 'b' + p: F(1, 2), X: -1})]
        return out
    allok &= run('conclusion with V(alpha,beta) instead', V=Vab)
    print('ALL AS EXPECTED' if allok else 'SOME UNEXPECTED RESULT')
