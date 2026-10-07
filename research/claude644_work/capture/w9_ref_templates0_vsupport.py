#!/usr/bin/env python3
"""Referee w9 [templates#0]: independent exact checks of the three constructions H, Q_b, V.
(1) V support: no two cells (incl. a cell with itself) cover all 7 rows; the three mass vectors give the
    stated loads and masses; the combination gives mass V(s,t) with loads >= (s,t) on a rational grid.
(2) Exact minimum mass of V support vs V(s,t) (LP via scipy, only informational) -- the claim needs only the
    upper bound.
(3) Q_b: minimum Fano-downset mass per Lemma 7.63 formula computed directly from the Fano lines, compared
    with max(3t/2, s+3t/4) exactly on a grid; homogeneous = 7s/4.
(4) Q_b explicit realisation (note Lemma 7.57 masses) checked: loads and no covering pair.
"""
from fractions import Fraction as F
import itertools
# rows: 0=b0 1=b1 2..5 = w1..w4, 6 = z
B0, B1, W1, W2, W3, W4, Z = range(7)
cells = [frozenset({B0, B1})]
A = [W1, W2, W3, W4, Z]
for c in itertools.combinations(A, 4):
    cells.append(frozenset(c))
mixed = [frozenset({B0, W3, W4, Z}), frozenset({B0, W1, W2, Z}), frozenset({B1, W2, W4, Z}), frozenset({B1, W1, W3, Z})]
cells += mixed
assert len(set(cells)) == 10
full = frozenset(range(7))
bad = [(c, d) for c in cells for d in cells if c | d == full]
print("V support: covering pairs:", len(bad))
assert not bad
# also: all subsets (downward closure) -- trivially fine since union monotone
def loads(mass):
    L = [F(0)] * 7
    for c, m in mass.items():
        for r in c:
            L[r] += m
    return L
m10 = {c: F(1, 4) for c in cells if c <= frozenset(A)}
m01 = {frozenset({B0, B1}): F(1)}
m21 = {frozenset({W1, W2, W3, W4}): F(1)}
for c in mixed:
    m21[c] = F(1, 2)
for m, (s, t), tot in [(m10, (1, 0), F(5, 4)), (m01, (0, 1), F(1)), (m21, (2, 1), F(3))]:
    L = loads(m)
    assert all(L[r] == s for r in A), (L, s)
    assert L[B0] == t and L[B1] == t, L
    assert sum(m.values()) == tot
print("V mass vectors (1,0):5/4, (0,1):1, (2,1):3 exact OK")
def V(s, t):
    return max(s + t, F(5, 4) * s + t / 2)
cnt = 0
for sn in range(0, 25):
    for tn in range(0, 25):
        s, t = F(sn, 8), F(tn, 8)
        if t <= s / 2:
            comb = [(m21, t), (m10, s - 2 * t)]
        else:
            comb = [(m21, s / 2), (m01, t - s / 2)]
        tot = {}
        for m, lam in comb:
            assert lam >= 0
            for c, v in m.items():
                tot[c] = tot.get(c, F(0)) + lam * v
        L = loads(tot)
        assert all(L[r] >= s for r in A) and L[B0] >= t and L[B1] >= t
        assert sum(tot.values()) == V(s, t), (s, t, sum(tot.values()), V(s, t))
        cnt += 1
print("V combination mass == V(s,t) and loads dominate on", cnt, "grid points: OK")

# Fano plane
lines = [frozenset(l) for l in [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]]
for l1, l2 in itertools.combinations(lines, 2):
    assert len(l1 & l2) == 1
def fano_mass(z):
    return max(max(z), max(sum(z[j] for j in L) for L in lines) / 2, sum(z) / 4)
L0 = lines[0]
def Qb(s, t):
    return max(F(3, 2) * t, s + F(3, 4) * t)
for sn in range(0, 25):
    for tn in range(0, 25):
        s, t = F(sn, 8), F(tn, 8)
        z = [t if j in L0 else s for j in range(7)]
        assert fano_mass(z) == Qb(s, t)
        assert fano_mass([s] * 7) == F(7, 4) * s
print("Q_b == Lemma 7.63 mass (b-rows on a line) and homogeneous == 7s/4 on grid: OK")
# explicit Q_b realisation (note Lemma 7.57): v=3t/2 on the six line complements other than compl(L0), u=max(0,s-3t/4) on compl(L0)
comps = [full - L for L in lines]
for sn in range(0, 17):
    for tn in range(0, 17):
        s, t = F(sn, 8), F(tn, 8)
        mass = {}
        for L, c in zip(lines, comps):
            mass[c] = (max(F(0), s - F(3, 4) * t) if L == L0 else F(3, 2) * t / 6)
        Ld = loads(mass)
        assert all(Ld[j] >= (t if j in L0 else s) for j in range(7))
        assert sum(mass.values()) == Qb(s, t)
assert not [(c, d) for c in comps for d in comps if c | d == full]
print("Q_b explicit realisation OK; Fano complements have no covering pair")
# informational: exact min mass of V support
try:
    from scipy.optimize import linprog
    import numpy as np
    worst = 0
    for sn in range(0, 9):
        for tn in range(0, 9):
            s, t = sn / 4, tn / 4
            Amat = np.zeros((7, 10)); b = np.zeros(7)
            for k, c in enumerate(cells):
                for r in c:
                    Amat[r, k] = 1
            b[:] = [t, t, s, s, s, s, s]
            res = linprog(np.ones(10), A_ub=-Amat, b_ub=-b, bounds=[(0, None)] * 10, method="highs")
            worst = max(worst, abs(res.fun - float(V(F(sn, 4), F(tn, 4)))))
    print("informational: LP min mass of V support vs V(s,t): max |diff| =", worst)
except Exception as e:
    print("scipy check skipped", e)
print("ALL OK")
