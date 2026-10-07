#!/usr/bin/env python3
"""Numerical exploration: c*(1,r) = min over static 5-request covers of the max request,
for anchors of masses 1 and r in [0,1].  Antichains reduced modulo S_5.
Run: python3 two_anchor_envelope.py
"""
from itertools import permutations
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


PERMS = list(permutations(range(N)))


def pm(m, p):
    return sum(1 << p[j] for j in range(N) if m >> j & 1)


def canon(F):
    return min(tuple(sorted(pm(m, p) for m in F)) for p in PERMS)


def primal(F, G, r):
    nv = len(F) + len(G) + 1
    c = np.zeros(nv); c[-1] = 1
    A = []
    for j in range(N):
        row = np.zeros(nv)
        for q, S in enumerate(F):
            if S >> j & 1: row[q] = 1
        for q, T in enumerate(G):
            if T >> j & 1: row[len(F) + q] = 1
        row[-1] = -1
        A.append(row)
    Aeq = np.zeros((2, nv)); Aeq[0, :len(F)] = 1; Aeq[1, len(F):-1] = 1
    res = linprog(c, A_ub=A, b_ub=[0] * N, A_eq=Aeq, b_eq=[1, r],
                  bounds=[(0, None)] * nv, method='highs')
    return res.fun


if __name__ == '__main__':
    reps = {}
    for F in antichains():
        if not F:
            continue
        G = blocker(F)
        if not G:
            continue
        reps.setdefault(canon(F), (F, G))
    print("antichain classes mod S5:", len(reps))
    rs = [i / 120 for i in range(121)]
    env = []
    fm = lambda M: '{' + ' '.join(''.join(str(j) for j in range(N) if m >> j & 1) for m in M) + '}'
    for r in rs:
        best = min((primal(F, G, r), F, G) for F, G in reps.values())
        env.append(best)
    prev = None
    for r, (v, F, G) in zip(rs, env):
        key = fm(F)
        if key != prev:
            print(f"  from r={r:.4f}: value {v:.6f}  F={fm(F)} G={fm(G)}")
            prev = key
    for r, (v, F, G) in zip(rs, env):
        if abs(r * 120 - round(r * 120)) < 1e-9 and round(r * 120) % 6 == 0:
            print(f"  r={r:.3f} c*={v:.6f}  1/5+r={0.2+r:.4f}  1/3+2r/3={1/3+2*r/3:.4f}  5/12+r/2={5/12+r/2:.4f}")
