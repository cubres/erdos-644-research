#!/usr/bin/env python3
"""Two disjoint fixed anchors A1 (mass 1) and A2 (mass r), five further edges.

(a) Fano placements: A1 on a nonempty set of lines L1, A2 on L2 (disjoint);
    labels of A_i-points off all lines of L_i; free lines get loads.
    Minimise the max free-line load (fractional LP).  Expect (1+r)/2.
(b) General 5-biclique covers: A1-points get types S (subsets of the 5 free
    requests), A2-points types T, S cap T nonempty for all used S,T.
    Enumerate maximal cross-intersecting pairs (F upset, G its blocker upset),
    solve LP.  Reports c*(1,r).
Floating LP (scipy HiGHS) = exploration; the upper-bound configurations found
are re-verified exactly (fractions) in two_anchor_exact.py.
"""
import sys
from itertools import combinations
import numpy as np
from scipy.optimize import linprog

POINTS = list(range(1, 8))
LINES = sorted({frozenset([x, y, x ^ y]) for x in POINTS for y in POINTS if x != y},
               key=lambda s: sorted(s))


def fano_lp(r):
    best = None
    for n1 in range(1, 7):
        for L1 in combinations(range(7), n1):
            rest = [i for i in range(7) if i not in L1]
            for n2 in range(1, len(rest) + 1):
                for L2 in combinations(rest, n2):
                    free = [i for i in range(7) if i not in L1 and i not in L2]
                    if not free:
                        continue
                    lab1 = [p for p in POINTS if all(p not in LINES[i] for i in L1)]
                    lab2 = [p for p in POINTS if all(p not in LINES[i] for i in L2)]
                    if not lab1 or not lab2:
                        continue
                    # vars: x_p (p in lab1), y_p (p in lab2), z
                    nv = len(lab1) + len(lab2) + 1
                    cobj = np.zeros(nv); cobj[-1] = 1
                    A_ub, b_ub = [], []
                    for i in free:
                        row = np.zeros(nv)
                        for j, p in enumerate(lab1):
                            if p in LINES[i]:
                                row[j] = 1
                        for j, p in enumerate(lab2):
                            if p in LINES[i]:
                                row[len(lab1) + j] = 1
                        row[-1] = -1
                        A_ub.append(row); b_ub.append(0)
                    A_eq = np.zeros((2, nv)); A_eq[0, :len(lab1)] = 1
                    A_eq[1, len(lab1):-1] = 1
                    res = linprog(cobj, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1, r],
                                  bounds=[(0, None)] * nv, method='highs')
                    if res.status == 0:
                        v = res.fun
                        if best is None or v < best[0] - 1e-12:
                            best = (v, L1, L2)
    return best


def upsets(n):
    """All upsets (monotone increasing families) of subsets of [n], as frozensets of bitmasks."""
    N = 1 << n
    # generate antichains recursively via minimal elements: simple approach for n=5
    masks = list(range(N))
    # enumerate antichains by backtracking over masks sorted by popcount
    order = sorted(masks, key=lambda m: (bin(m).count('1'), m))
    res = []

    def bt(i, chosen):
        if i == len(order):
            res.append(tuple(chosen)); return
        m = order[i]
        bt(i + 1, chosen)
        if all((m & s) != s and (m & s) != m for s in chosen):  # incomparable
            chosen.append(m); bt(i + 1, chosen); chosen.pop()
    bt(0, [])
    return res  # antichains (minimal elements of upsets)


def blocker_min(F, n):
    """Minimal sets meeting every member of antichain F (as bitmasks)."""
    N = 1 << n
    hit = [T for T in range(1, N) if all(T & S for S in F)]
    return [T for T in hit if not any((U & T) == U and U != T for U in hit)]


def biclique_lp(r, n=5, verbose=False):
    best = None
    ants = upsets(n)
    for F in ants:
        if not F or 0 in F:
            continue
        G = blocker_min(F, n)
        if not G:
            continue
        nv = len(F) + len(G) + 1
        cobj = np.zeros(nv); cobj[-1] = 1
        A_ub = []
        for j in range(n):
            row = np.zeros(nv)
            for q, S in enumerate(F):
                if S >> j & 1:
                    row[q] = 1
            for q, T in enumerate(G):
                if T >> j & 1:
                    row[len(F) + q] = 1
            row[-1] = -1
            A_ub.append(row)
        A_eq = np.zeros((2, nv)); A_eq[0, :len(F)] = 1; A_eq[1, len(F):-1] = 1
        res = linprog(cobj, A_ub=A_ub, b_ub=[0] * n, A_eq=A_eq, b_eq=[1, r],
                      bounds=[(0, None)] * nv, method='highs')
        if res.status == 0 and (best is None or res.fun < best[0] - 1e-12):
            best = (res.fun, F, G, res.x)
    return best


if __name__ == '__main__':
    print("(a) Fano placements, min max free-line load vs (1+r)/2")
    for r in [0.0, 0.25, 0.5, 0.75, 1.0]:
        v, L1, L2 = fano_lp(r)
        print(f"  r={r:.2f}: LP={v:.6f}  (1+r)/2={(1+r)/2:.6f}  lines A1={L1} A2={L2}")
    print("(b) general 5-biclique covers c*(1,r); compare grid (1+r)/2, C5 (2+3r)/5, count 2sqrt(r/5)")
    for r in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        v, F, G, x = biclique_lp(r)
        fm = lambda M: ['{' + ','.join(str(j) for j in range(5) if m >> j & 1) + '}' for m in M]
        print(f"  r={r:.2f}: c*={v:.6f} grid={(1+r)/2:.4f} C5={(2+3*r)/5:.4f} count={2*np.sqrt(r/5):.4f}  F={fm(F)} G={fm(G)}")
