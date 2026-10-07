"""Referee w9, claim typeclosed#0 (Theorem L+).  Independent EXACT checks of the algebra:
 (1) the two part-k identities (sympy, exact);
 (2) the V support: 10 cells, pairwise non-covering [7]; primal masses (explicit formulas, both regimes) meet the loads
     exactly with total max(s+t,5s/4+t/2); dual weights prove the lower bound (so the capacity function is exact);
 (3) the pencil tuple (e,e,e | d,d,d,d) with d=x-3e/4 satisfies Lemma 7.63's inequalities iff e<=2x/3 (0<=e<=x):
     checked by enumerating the row-Fano lines, symbolically.
"""
import sympy as sp
from itertools import combinations

# (1) identities
xj, xk, sj, sk = sp.symbols('xj xk sj sk', real=True)
ej, ek = xj - sj, xk - sk
lhs1 = xk - sk - (1 - sj)
rhs1 = (ej + ek - sp.Rational(3, 4)) + 2 * (sj - 2 * xj / 3) + (xj - sp.Rational(3, 4)) / 3
lhs2 = xk - 5 * sk / 4 - (1 - sj) / 2
rhs2 = (ej + ek - sp.Rational(3, 4)) + (1 - sk) / 4 + sp.Rational(3, 2) * (sj - 2 * xj / 3)
assert sp.expand(lhs1 - rhs1) == 0 and sp.expand(lhs2 - rhs2) == 0
print('identities K1,K2: exact OK')

# (2) V support
W = [2, 3, 4, 5]; z = 6; full = set(range(7))
cells = [frozenset({0, 1})] + [frozenset(c) for c in combinations(W + [z], 4)] + \
        [frozenset(c) for c in ({0, 3, 4, z}, {0, 2, 5, z}, {1, 2, 4, z}, {1, 3, 5, z})]
assert len(set(cells)) == 10
for a in cells:
    for b in cells:  # includes a==b
        assert (a | b) != full
print('V support: 10 cells, no pair (incl. equal) covers [7]: OK')
s, t = sp.symbols('s t', nonnegative=True)
mixed = cells[6:]
fours = cells[1:6]

def cover4(dem):  # demands on rows 2..6 by the five 4-subsets: mass m_r on the cell omitting r
    # classical: with total T=max(maxd, sum/4), mass on cell omitting row r = T - d_r
    return None

def primal(regime):
    m = {c: sp.Integer(0) for c in cells}
    if regime == 'lo':  # t <= s/2
        for c in mixed: m[c] = t / 2
        dem = {2: s - t, 3: s - t, 4: s - t, 5: s - t, 6: s - 2 * t}
        T = sum(dem.values()) / 4  # = 5s/4-3t/2 >= s-t when t<=s/2
    else:  # t >= s/2
        for c in mixed: m[c] = s / 4
        m[frozenset({0, 1})] = t - s / 2
        dem = {2: s / 2, 3: s / 2, 4: s / 2, 5: s / 2, 6: sp.Integer(0)}
        T = s / 2
    for c in fours:
        omit = (set(W + [z]) - c).pop()
        m[c] += T - dem[omit]
    return m, T

for regime, cond in (('lo', sp.Le(t, s / 2)), ('hi', sp.Ge(t, s / 2))):
    m, T = primal(regime)
    loads = [sp.simplify(sum(m[c] for c in cells if r in c)) for r in range(7)]
    need = [t, t] + [s] * 5
    tot = sp.simplify(sum(m.values()))
    target = 5 * s / 4 + t / 2 if regime == 'lo' else s + t
    assert sp.simplify(tot - target) == 0, (regime, tot)
    for r in range(7):
        assert sp.simplify(loads[r] - need[r]) == 0, (regime, r, loads[r])
    # nonnegativity of masses on the regime: check at vertices of the regime cone {(s,t)>=0, cond} via rays
    rays = [(1, 0), (2, 1)] if regime == 'lo' else [(0, 1), (2, 1)]
    for c in cells:
        for (a, b) in rays:
            v = m[c].subs({s: a, t: b})
            assert v >= 0, (regime, sorted(c), v)
print('V primal: loads exact, masses >=0 on both regimes (linear in (s,t), checked on extreme rays), totals = 5s/4+t/2 | s+t')
for w in ({0: sp.Rational(1, 2), 1: sp.Rational(1, 2), 2: sp.Rational(1, 4), 3: sp.Rational(1, 4), 4: sp.Rational(1, 4), 5: sp.Rational(1, 4), 6: 0},
          {r: sp.Rational(1, 4) for r in range(7)}):
    for c in cells:
        assert sum(w[r] for r in c) <= 1
    print('dual weights feasible; objective =', sp.simplify(sum(w[r] * ([t, t] + [s] * 5)[r] for r in range(7))))

# (3) pencil tuple against Lemma 7.63: row-Fano on points 0..6, lines = {i,i+1,i+3} mod 7; put e on line {0,1,3}
lines = [frozenset({i % 7, (i + 1) % 7, (i + 3) % 7}) for i in range(7)]
L0 = lines[0]
x, e = sp.symbols('x e', positive=True)
d = x - 3 * e / 4
row = {r: (e if r in L0 else d) for r in range(7)}
conds = set()
for L in lines:
    conds.add(sp.simplify(2 * x - sum(row[r] for r in L)))
conds.add(sp.simplify(4 * x - sum(row.values())))
print('pencil Lemma-7.63 slacks (must be >=0):', conds, '; rows: x-e, x-d =', sp.simplify(x - d))
# slacks: 2x-3e (>=0 iff e<=2x/3), e/2, 0 ;  x-d = 3e/4 >= 0 ; d>=0 iff e<=4x/3.
