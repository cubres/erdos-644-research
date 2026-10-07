#!/usr/bin/env python3
"""Exact certificate: for two disjoint anchors of masses 1 >= r >= 0, every static
5-request cover of the cross pairs has a request of mass >= f(r) = min(1/5 + r, 5/12 + r/2).

Run: python3 two_anchor_curve.py
(scipy is used only to FIND candidate dual weights; every inequality is then
checked exactly with Fractions.)

Weak duality used (elementary): for masses mu on A1-types F, nu on A2-types G and any
weights w_j >= 0 with sum 1 on the five requests,
   max_j load_j >= sum_j w_j load_j = sum_S mu_S w(S) + sum_T nu_T w(T)
                 >= 1*min_F w(S) + r*min_G w(T).
f is linear on [0,13/30] and on [13/30,1]; a linear function of r that dominates f at
both ends of a piece dominates it on the piece.  For each antichain F (G = minimal
blocker) we exhibit w1 valid at r=0 and r=13/30 and w2 valid at r=13/30 and r=1.
Also verifies the matching upper-bound configurations at the breakpoints.
"""
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog

N = 5
order = sorted(range(1, 1 << N), key=lambda m: (bin(m).count('1'), m))


def antichains():
    res = []

    def bt(i, chosen):
        if i == len(order):
            res.append(tuple(chosen)); return
        m = order[i]
        bt(i + 1, chosen)
        if all((m & s) != s and (m & s) != m for s in chosen):
            chosen.append(m); bt(i + 1, chosen); chosen.pop()
    bt(0, [])
    return res


def blocker(F):
    hit = [T for T in range(1, 1 << N) if all(T & S for S in F)]
    return [T for T in hit if not any((U & T) == U and U != T for U in hit)]


def ws(w, S):
    return sum(w[j] for j in range(N) if S >> j & 1)


def dual(F, G, r):
    nv = N + 2
    c = np.zeros(nv); c[N] = -1; c[N + 1] = -r
    A, b = [], []
    for S in F:
        row = np.zeros(nv); row[N] = 1
        for j in range(N):
            if S >> j & 1: row[j] = -1
        A.append(row); b.append(0)
    for T in G:
        row = np.zeros(nv); row[N + 1] = 1
        for j in range(N):
            if T >> j & 1: row[j] = -1
        A.append(row); b.append(0)
    Aeq = np.zeros((1, nv)); Aeq[0, :N] = 1
    res = linprog(c, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=[1],
                  bounds=[(0, None)] * N + [(None, None)] * 2, method='highs')
    w = [max(Fr(0), Fr(x).limit_denominator(5000)) for x in res.x[:N]]
    s = sum(w)
    return [x / s for x in w]


def f(r):
    return min(Fr(1, 5) + r, Fr(5, 12) + r / 2)


r0 = Fr(13, 30)
assert Fr(1, 5) + r0 == Fr(5, 12) + r0 / 2
val = lambda w, F, G, r: min(ws(w, S) for S in F) + r * min(ws(w, T) for T in G)
cnt = 0
for F in antichains():
    if not F:
        continue
    G = blocker(F)
    if not G:
        continue
    done1 = done2 = False
    for rr in (0.2, 0.0, 13 / 30, 0.1, 0.3):
        w = dual(F, G, rr)
        if val(w, F, G, Fr(0)) >= f(Fr(0)) and val(w, F, G, r0) >= f(r0):
            done1 = True; break
    for rr in (0.7, 1.0, 13 / 30, 0.5, 0.9):
        w = dual(F, G, rr)
        if val(w, F, G, r0) >= f(r0) and val(w, F, G, Fr(1)) >= f(Fr(1)):
            done2 = True; break
    assert done1 and done2, (F, G)
    cnt += 1
print(f"lower bound f(r)=min(1/5+r,5/12+r/2) certified for all {cnt} antichains, all r in [0,1]")

# matching upper-bound configurations (fractional masses)
def loads(F, G, mu, nu):
    return [sum(m for S, m in zip(F, mu) if S >> j & 1) + sum(n for T, n in zip(G, nu) if T >> j & 1)
            for j in range(N)]

for r in [Fr(0), Fr(1, 5), r0, Fr(1, 2), Fr(3, 4), Fr(1)]:
    # config 1 (7.106 seed): A1 split into 5 singletons, A2 full type
    F1 = [1 << j for j in range(N)]; G1 = [(1 << N) - 1]
    L1 = max(loads(F1, G1, [Fr(1, 5)] * 5, [r]))
    # config 2 (split/grid): A1 on 3x2 grid, A2 on {3,4} (mass p) and {0,1,2} (mass r-p)
    F2 = [(1 << i) | (1 << j) for i in range(3) for j in (3, 4)]
    G2 = [0b11000, 0b00111]
    for S in F2:
        for T in G2:
            assert S & T
    p = (r - Fr(1, 6)) / 2 if r >= Fr(1, 6) else Fr(0)
    L2 = max(loads(F2, G2, [Fr(1, 6)] * 6, [p, r - p]))
    assert min(L1, L2) == f(r), (r, L1, L2, f(r))
print("upper-bound configurations attain f(r) at r = 0, 1/5, 13/30, 1/2, 3/4, 1")
print("ALL CHECKS PASSED")
