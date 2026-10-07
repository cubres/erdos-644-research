#!/usr/bin/env python3
"""Referee templates#0: exact checks of the Gap-Pair Lemma, Theorem 7.75' and one-sided |I|=2.
(A) Gap-Pair: for every choice of one violated facet of Q_b, of Q_a and of V(a,b) (4*4*4 = 64 systems),
    the system {hyps with margin g, three violations with margin g} implies g <= 0. Exact Fourier-Motzkin
    in Fractions (own implementation). Also the variant with (G) strict and (H1),(H2) weak is reported.
(B) Theorem 7.75': random finite C (rational) over two parts; tau* by an independent residual
    enumeration; whenever tau* >= 3/4 check the proof's construction (homogeneous type in H, else gap
    pair a,b around H + first feasible of Q_b, Q_a, V) exactly. Includes equality instances tau* = 3/4.
(C) The H-empty corner: show the written proof needs N >= 7/4 (from tau* <= N-1).
"""
import itertools, random, sys
from fractions import Fraction as F

# ---------------- exact Fourier-Motzkin ----------------
def fm_implies_g_nonpos(rows, nvars, gidx):
    """rows: list of (coef list, rhs) meaning coef.v <= rhs.  Eliminate all vars except g; return the
    tightest bound on g, i.e. True iff the system forces g <= 0 (or is infeasible)."""
    def norm(rs):
        best = {}
        for c, r in rs:
            nz = [i for i in range(nvars) if c[i] != 0]
            if not nz:
                if r < 0: return None
                continue
            m = max(abs(c[i]) for i in nz)
            key = tuple(c[i] / m for i in range(nvars))
            rr = r / m
            if key not in best or rr < best[key]: best[key] = rr
        return [(list(k), v) for k, v in best.items()]
    rs = norm(rows)
    if rs is None: return True
    for v in range(nvars):
        if v == gidx: continue
        pos = [r for r in rs if r[0][v] > 0]; neg = [r for r in rs if r[0][v] < 0]
        new = [r for r in rs if r[0][v] == 0]
        for cp, rp in pos:
            for cn, rn in neg:
                a, b = cp[v], -cn[v]
                new.append(([cp[i] * b + cn[i] * a for i in range(nvars)], rp * b + rn * a))
        rs = norm(new)
        if rs is None: return True
    # remaining rows only in g: c*g <= r
    ub = None
    for c, r in rs:
        if c[gidx] > 0:
            u = r / c[gidx]; ub = u if ub is None else min(ub, u)
    return ub is not None and ub <= 0

# variables x,y,a,b,g  -> indices 0..4
X, Y, A_, B_, G = range(5)
def lin(**kw):
    c = [F(0)] * 5; const = F(0)
    for k, v in kw.items():
        if k == 'c': const = F(v)
        else: c[{'x': X, 'y': Y, 'a': A_, 'b': B_, 'g': G}[k]] = F(v)
    return c, const
def le(expr_c, expr_const, rhs=0):  # expr <= rhs  ->  coef.v <= rhs - const
    return (expr_c, F(rhs) - expr_const)

def hyp_rows(strictG=False, strictH=True):
    R = []
    # x >= g, y >= g  (x,y>0), a >= 0, b >= a, b <= 1
    R.append(le(*lin(x=-1, g=1))); R.append(le(*lin(y=-1, g=1)))
    R.append(le(*lin(a=-1))); R.append(le(*lin(a=1, b=-1))); R.append(le(*lin(b=1), 1))
    hm = 1 if strictH else 0
    # (H1) 4y < 7(1-a):  4y + 7a - 7 + g <= 0
    R.append(le(*lin(y=4, a=7, g=hm, c=-7)))
    # (H2) 4x < 7b:  4x - 7b + g <= 0
    R.append(le(*lin(x=4, b=-7, g=hm)))
    # (G) b - a <= x + y - 7/4
    R.append(le(*lin(b=1, a=-1, x=-1, y=-1, g=(1 if strictG else 0), c=F(7, 4))))
    R.append(le(*lin(g=-1), 0))  # g >= 0 (we test whether g can be > 0)
    return R

# facets as (coef dict over x,y,a,b, const) meaning facet_value - capacity ; violation: >= g
# s = a-load, t = b-load; part1 loads (a,b), part2 loads (1-a,1-b)
def facets_Qb():
    # max(3t/2, s+3t/4) <= cap
    return [lin(b=F(3, 2), x=-1), lin(a=1, b=F(3, 4), x=-1),
            lin(b=F(-3, 2), y=-1, c=F(3, 2)), lin(a=-1, b=F(-3, 4), y=-1, c=F(7, 4))]
def facets_Qa():
    return [lin(a=F(3, 2), x=-1), lin(b=1, a=F(3, 4), x=-1),
            lin(a=F(-3, 2), y=-1, c=F(3, 2)), lin(b=-1, a=F(-3, 4), y=-1, c=F(7, 4))]
def facets_V():
    # max(s+t, 5s/4+t/2)
    return [lin(a=1, b=1, x=-1), lin(a=F(5, 4), b=F(1, 2), x=-1),
            lin(a=-1, b=-1, y=-1, c=2), lin(a=F(-5, 4), b=F(-1, 2), y=-1, c=F(7, 4))]
def viol(fc):  # facet >= g  ->  -facet + g <= 0
    c, const = fc
    c2 = [-v for v in c]; c2[G] += 1
    return (c2, const)  # -coef.v + g <= const  (since -(coef.v+const) + g <= 0)

def run_gap(strictG, strictH, label):
    bad = []
    n = 0
    for f1, f2, f3 in itertools.product(facets_Qb(), facets_Qa(), facets_V()):
        R = hyp_rows(strictG, strictH) + [viol(f1), viol(f2), viol(f3)]
        n += 1
        if not fm_implies_g_nonpos(R, 5, G): bad.append((f1, f2, f3))
    print(f'Gap-Pair [{label}]: {n} systems, {n - len(bad)} force margin <= 0, {len(bad)} NOT')
    return bad

b1 = run_gap(False, True, '(H1),(H2) strict, (G) weak -- as stated')
assert not b1
b2 = run_gap(False, False, 'all weak (H1),(H2),(G): sensitivity')
print('  (all-weak variant: systems not closed =', len(b2), ') -- expected >0 only if strictness matters')

# ---------------- (B) Theorem 7.75' end-to-end ----------------
def tau_star_two_part(C, x, y):
    """independent: inf over residuals (u,v), 0<=u<=x, 0<=v<=y, 'just below' semantics, of x+y-u-v,
    such that no c in C has c <= u and 1-c <= v (strictly: residual u- means c<u fails iff c>=u).
    Enumerate candidate u in {x} U {c in C: c>0} (u just below c), v in {y} U {1-c : c<1}."""
    N = x + y
    best = N - 1  # sum of residual just below 1
    us = [(x, False)] + [(c, True) for c in C if 0 < c <= x]
    vs = [(y, False)] + [(1 - c, True) for c in C if 0 < 1 - c <= y]
    for u, us_ in us:
        for v, vs_ in vs:
            ok = True
            for c in C:
                fits1 = (c < u) if us_ else (c <= u)
                fits2 = ((1 - c) < v) if vs_ else ((1 - c) <= v)
                if fits1 and fits2: ok = False; break
            if ok: best = min(best, N - u - v)
    return best

def Qb(s, t): return max(F(3, 2) * t, s + F(3, 4) * t)
def Qa(s, t): return Qb(t, s)
def Vf(s, t): return max(s + t, F(5, 4) * s + t / 2)
def feasible(M, c1, c2, x, y):  # c1,c2 first-part sizes of the (s-type, t-type)
    return M(c1, c2) <= x and M(1 - c1, 1 - c2) <= y

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
stats = {'hom': 0, 'Qb': 0, 'Qa': 0, 'V': 0, 'eq': 0, 'low': 0}
fails = []
def check_instance(C, x, y):
    C = sorted(set(C))
    ts = tau_star_two_part(C, x, y)
    if ts < F(3, 4): stats['low'] += 1; return
    if ts == F(3, 4): stats['eq'] += 1
    N = x + y
    assert N >= F(7, 4)
    lo, hi = 1 - F(4, 7) * y, F(4, 7) * x
    for c in C:
        if lo <= c <= hi:
            assert F(7, 4) * c <= x and F(7, 4) * (1 - c) <= y
            stats['hom'] += 1; return
    below = [c for c in C if c < lo]; above = [c for c in C if c > hi]
    assert below and above, ('one-sided C with tau*>=3/4??', C, x, y, ts)
    a, b = max(below), min(above)
    assert a < b
    assert 4 * y < 7 * (1 - a) and 4 * x < 7 * b and b - a <= N - F(7, 4)
    for name, M, c1, c2 in [('Qb', Qb, a, b), ('Qa', Qa, a, b), ('V', Vf, a, b)]:
        if feasible(M, c1, c2, x, y): stats[name] += 1; return
    fails.append((C, x, y, ts))

def rnd(den): return F(random.randint(0, den), den)
for it in range(20000):
    den = random.choice([8, 12, 20, 24, 40, 60])
    x = F(random.randint(den // 2, 2 * den), den); y = F(random.randint(den // 2, 2 * den), den)
    k = random.randint(1, 5)
    C = [c for c in (rnd(den) for _ in range(k)) if c <= x and 1 - c <= y]
    if not C: continue
    check_instance(C, x, y)
# equality-focused: choose a,b and set x,y so that constraints are tight
for it in range(20000):
    den = random.choice([12, 24, 60, 120])
    a = rnd(den); b = rnd(den)
    if a > b: a, b = b, a
    # pick x just above 4b/7*(something) ... sample x in (b, 7b/4), y in (1-a, 7(1-a)/4)
    if b == 0 or a == 1: continue
    x = b + (F(3, 4) * b) * F(random.randint(0, 100), 100)
    y = (1 - a) + (F(3, 4) * (1 - a)) * F(random.randint(0, 100), 100)
    extra = [rnd(den) for _ in range(random.randint(0, 3))]
    C = [c for c in [a, b] + extra if c <= x and 1 - c <= y]
    if not C: continue
    check_instance(C, x, y)
print('7.75\' end-to-end:', stats, 'failures:', len(fails))
for f in fails[:5]: print('  FAIL', f)
assert not fails

# ---------------- (C) H-empty corner ----------------
# If N < 7/4 then tau* <= N-1 < 3/4, so the theorem's hypothesis excludes it; the written proof never
# says so. Illustrate: x=y=3/4 (N=3/2), C={1/2}: 1/2 is both 'above H' (>4x/7=3/7) and 'below H' (<1-4y/7=4/7).
x = y = F(3, 4); C = [F(1, 2)]
print('H-empty corner: lo,hi =', 1 - F(4, 7) * y, F(4, 7) * x, ' tau* =', tau_star_two_part(C, x, y),
      '(<3/4, so excluded only via tau*<=N-1, which the written proof does not state)')
print('DONE')
