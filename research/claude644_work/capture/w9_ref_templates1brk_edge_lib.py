# functions of w9_ref_templates1brk_edge.py (auto-extracted)
# [templates#1] BREAK-IT referee (w9): EXACT edge-case end-to-end test of Theorem 2UB.
# Independent code: tau* by brute force over cut patterns (u_i = c^- for c in {x_i, g_i, h_i}, plus the sum<1
# blocker N-1), pushed DOWN onto tau*=3/4 exactly; canonical pair for EVERY heavy pair (I,J); a bad seven-tuple
# realised with EXPLICIT exact cell masses (Fano line-complement support for H/Q_b/Q_a, ten-cell support for V),
# brute-force row loads, capacity, and pairwise non-covering of the support.
# Generators focus on edge cases: g_I = 1, |g| = 1, g_i = x_i (generator at capacity), coordinates exactly at
# 4x_i/7 (non-heavy boundary), several heavy parts per generator, many small tail coordinates, p up to 9,
# the narrow K != J window (g_I > 9/10), and nested/overlapping generators (g <= h).
import random, itertools, sys
from fractions import Fraction as F
Q34 = F(3, 4)

def tau_star(x, g, h):
    p = len(x); best = sum(x) - 1
    cand = [sorted({x[i], g[i], h[i]} - {F(0)}) for i in range(p)]
    # u_i = c^- blocks a type iff a_i >= c; uncut part: c = +inf
    for pat in itertools.product(*[[None] + c for c in cand]):
        cost = sum(x[i] - c for i, c in enumerate(pat) if c is not None)
        if cost >= best: continue
        def blocked(gen):
            # every type a in U(gen) (gen <= a <= x, sum 1) has a_i >= c_i for some cut i, or no type fits
            # a type fits under u iff gen_i < c_i for all cut i and sum_i min(x_i, c_i^-) >= 1 (c^- -> sup)
            if any(c is not None and gen[i] >= c for i, c in enumerate(pat)): return True
            cap = sum((x[i] if c is None else c) for i, c in enumerate(pat))
            ncut = sum(c is not None for c in pat)
            return cap < 1 or (cap == 1 and ncut > 0)
        if blocked(g) and blocked(h): best = cost
    return best

# ---------- explicit supports ----------
LINES = [frozenset(s) for s in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
FANO_CELLS = [frozenset(range(7)) - l for l in LINES]
assert all(len(c1 | c2) < 7 for c1 in FANO_CELLS for c2 in FANO_CELLS)
# V support on rows 0..6: b0=0,b1=1,w1..w4=2..5,z=6
b0, b1, w1, w2, w3, w4, z = range(7)
A5 = [w1, w2, w3, w4, z]
V_CELLS = [frozenset({b0, b1})] + [frozenset(A5) - {r} for r in A5] + \
          [frozenset({b0, w3, w4, z}), frozenset({b0, w1, w2, z}), frozenset({b1, w2, w4, z}), frozenset({b1, w1, w3, z})]
assert all(len(c1 | c2) < 7 for c1 in V_CELLS for c2 in V_CELLS)

def fano_masses(rowload):
    # rowload: dict row(point)->load; find masses on line complements by the explicit formulas below
    raise NotImplementedError

def realise(kind, s, t):
    """return (cells, masses, rows_a, rows_b) realising loads >= s on a-rows, >= t on b-rows in one part"""
    if kind == 'Ha':
        return FANO_CELLS, [s / 4] * 7, list(range(7)), []
    if kind == 'Hb':
        return FANO_CELLS, [t / 4] * 7, [], list(range(7))
    if kind in ('Qb', 'Qa'):
        L = LINES[0]
        brows = sorted(L); arows = sorted(set(range(7)) - L)
        ss, tt = (s, t) if kind == 'Qb' else (t, s)     # ss: load of the 4 off-L rows, tt: of the 3 L rows
        u = max(F(0), ss - 3 * tt / 4); v = tt / 4
        masses = [u if l == L else v for l in LINES]
        if kind == 'Qb': return FANO_CELLS, masses, arows, brows
        return FANO_CELLS, masses, brows, arows
    if kind == 'V':
        m = [F(0)] * 10
        def addcomb(lam, which):
            if which == '10':
                for k in range(1, 6): m[k] += lam / 4
            elif which == '01':
                m[0] += lam
            else:  # (2,1): 1 on W={w1..w4} (= cell A5 minus z, index of z is 5 -> k=5), 1/2 on mixed cells
                m[1 + A5.index(z)] += lam
                for k in range(6, 10): m[k] += lam / 2
        if t <= s / 2:
            addcomb(t, '21'); addcomb(s - 2 * t, '10')
        else:
            addcomb(s / 2, '21'); addcomb(t - s / 2, '01')
        return V_CELLS, m, A5, [b0, b1]
    raise ValueError

def check_tuple(kind, a, b, x):
    for i in range(len(x)):
        cells, masses, ra, rb = realise(kind, a[i], b[i])
        assert all(mm >= 0 for mm in masses)
        if sum(masses) > x[i]: return False
        load = [sum(mm for c, mm in zip(cells, masses) if r in c) for r in range(7)]
        if any(load[r] < a[i] for r in ra) or any(load[r] < b[i] for r in rb):
            raise AssertionError('realisation bug')
    return True

def formula(kind, s, t):
    return {'Ha': 7 * s / 4, 'Hb': 7 * t / 4, 'Qb': max(3 * t / 2, s + 3 * t / 4),
            'Qa': max(3 * s / 2, t + 3 * s / 4), 'V': max(s + t, 5 * s / 4 + t / 2)}[kind]

