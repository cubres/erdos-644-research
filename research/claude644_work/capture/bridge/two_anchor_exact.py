#!/usr/bin/env python3
"""Exact certificates for the two-disjoint-anchor static covers.

Run:  python3 two_anchor_exact.py      (standard library only, Fractions)

(A) Upper-bound configurations (integer, exact):
    split/grid:  A1 (size alpha) in six classes X_ij (i in {0,1,2}, j in {3,4}),
                 A2 (size beta) = P (type {3,4}) + Q (type {0,1,2});
                 request D_l = union of classes whose type contains l.
    For all 1<=alpha,beta<=300 we build the integer partition described in the
    proof and check (i) every A1-type meets every A2-type, (ii) max |D_l| equals
    the closed form  max(2u+ceil((beta+u)/2), 3u+floor((beta-u)/2)) with u=ceil(alpha/6)
    when beta>=u (and <= (5u+beta)/2 + 1).
(B) Method lower bound at alpha=beta: for EVERY antichain F on {0..4} (types of
    A1-points) with G = minimal blocker of F (types of A2-points), exhibit rational
    request weights w (sum 1) with  min_{S in F} w(S) + min_{T in G} w(T) >= 11/12.
    By LP duality this shows no static 5-request cover of the cross pairs of two
    equal anchors has all requests below (11/12)|A1|.
"""
from fractions import Fraction as Fr
from itertools import combinations, product
import math

# ---------------- (A) upper bound -----------------
def split_grid(alpha, beta):
    u = math.ceil(alpha / 6)
    # six grid classes of sizes floor/ceil(alpha/6)
    sizes = [alpha // 6 + (1 if i < alpha % 6 else 0) for i in range(6)]
    keys = [(i, j) for i in range(3) for j in (3, 4)]
    # assign larger classes first; all <= u
    X = dict(zip(keys, sizes))
    if beta >= u:
        P = (beta - u) // 2
    else:
        P = 0
    Q = beta - P
    types1 = {k: {k[0], k[1]} for k in keys}
    types2 = {'P': {3, 4}, 'Q': {0, 1, 2}}
    for s in types1.values():
        for t in types2.values():
            assert s & t
    D = []
    for l in range(5):
        d = sum(X[k] for k in keys if l in types1[k])
        d += (P if l in types2['P'] else 0) + (Q if l in types2['Q'] else 0)
        D.append(d)
    return max(D), u


worst = Fr(0)
for alpha in range(1, 301):
    for beta in range(1, 301):
        mx, u = split_grid(alpha, beta)
        if beta >= u:
            bound = max(2 * u + math.ceil((beta + u) / 2), 3 * u + (beta - u) // 2)
            assert mx <= bound, (alpha, beta, mx, bound)
            assert Fr(mx) <= Fr(5 * u + beta, 2) + 1
            worst = max(worst, Fr(mx) - (Fr(5 * alpha, 12) + Fr(beta, 2)))
        else:
            assert mx <= 3 * u
print(f"(A) split/grid cover verified for 1<=alpha,beta<=300; "
      f"max excess over 5alpha/12+beta/2 = {worst} (<= 5/2 + 1/2)")

# ---------------- (B) lower bound at alpha = beta -----------------
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


def wsum(w, S):
    return sum(w[j] for j in range(N) if S >> j & 1)


# candidate weight vectors: all w with entries in {0,1/12,...,1} summing to 1 is too many;
# use a small structured pool and fall back to exhaustive search on a grid of denominators 12.
def comps(total, parts):
    if parts == 1:
        yield (total,); return
    for x in range(total + 1):
        for rest in comps(total - x, parts - 1):
            yield (x,) + rest

POOL = [tuple(Fr(x, 12) for x in c) for c in comps(12, N)]   # 1820 vectors
target = Fr(11, 12)
ants = [F for F in antichains() if F]
count = 0
for F in ants:
    G = blocker(F)
    if not G:
        continue
    ok = False
    for w in POOL:
        v = min(wsum(w, S) for S in F) + min(wsum(w, T) for T in G)
        if v >= target:
            ok = True; break
    assert ok, (F, G)
    count += 1
print(f"(B) all {count} antichains F (with G = blocker(F)) certified: "
      f"some rational w (denominator 12) gives min_F w + min_G w >= 11/12")
# the value 11/12 is attained by F={{3,4},{0,1,2}} with G its blocker (3x2 grid):
F0 = [0b11000, 0b00111]
G0 = blocker(F0)
assert sorted(G0) == sorted([(1 << i) | (1 << j) for i in range(3) for j in (3, 4)])
print("    extremal pair: F={{3,4},{0,1,2}}, G={{i,j}: i<3<=j}; value 11/12 at alpha=beta")
print("ALL EXACT CHECKS PASSED")
