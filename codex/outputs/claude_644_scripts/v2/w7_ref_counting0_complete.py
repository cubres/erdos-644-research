#!/usr/bin/env python3
"""w7_ref_counting0_complete.py -- referee counting#0: for the complete family K_n^(k) (rows = k-sets,
complement blocks C_j of size b=n-k, repetitions allowed), MILP (HiGHS) for
  phase 1: lex-min (|P7|,|Pi7|) over 7-tuples;
  phase 2: among lex-minimisers, is there one satisfying the corollary hypothesis
           (every v in some W_j has d(v)>=4, i.e. v lies in <=3 blocks)?  and the refined 4q<=3d?
Then extracts the witness and RE-VERIFIES it exactly in pure python (P, Pi, W_j, d, q, hypothesis).
Pair semantics: uv in Pi7 iff no block contains both; uv in A_j iff C_j contains both and no other block does.
Usage: n k [refined]"""
import sys, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def solve(n, k, phase2=None, refined=False, time_limit=500):
    b = n - k
    V = range(n); J = range(7)
    prs = list(itertools.combinations(V, 2))
    idx = {}
    def var(name):
        idx[name] = len(idx); return idx[name]
    for v in V:
        for j in J: var(('x', v, j))
    for (u, v) in prs:
        for j in J: var(('c', u, v, j))
        var(('y', u, v))
    for v in V: var(('z', v))
    if phase2 is not None:
        for (u, v) in prs:
            for j in J: var(('a', u, v, j))
        for v in V:
            for j in J: var(('w', v, j))
        if refined:
            for v in V: var(('q', v))
    N = len(idx)
    rows = []; lo = []; hi = []
    def add(coefs, l, h):
        r = np.zeros(N)
        for name, c in coefs: r[idx[name]] += c
        rows.append(r); lo.append(l); hi.append(h)
    for j in J: add([(('x', v, j), 1) for v in V], b, b)
    for (u, v) in prs:
        for j in J:
            add([(('c', u, v, j), 1), (('x', u, j), -1)], -np.inf, 0)
            add([(('c', u, v, j), 1), (('x', v, j), -1)], -np.inf, 0)
            add([(('c', u, v, j), 1), (('x', u, j), -1), (('x', v, j), -1)], -1, np.inf)
            add([(('y', u, v), 1), (('c', u, v, j), 1)], -np.inf, 1)       # y <= 1 - c_j
        add([(('y', u, v), 1)] + [(('c', u, v, j), 1) for j in J], 1, np.inf)  # y >= 1 - sum c
        add([(('z', u), 1), (('y', u, v), -1)], 0, np.inf)
        add([(('z', v), 1), (('y', u, v), -1)], 0, np.inf)
    # z_v <= sum of y's at v (exact P)
    for v in V:
        add([(('z', v), 1)] + [(('y', *sorted((u, v))), -1) for u in V if u != v], -np.inf, 0)
    M = len(prs) + 1
    c = np.zeros(N)
    if phase2 is None:
        for v in V: c[idx[('z', v)]] = M
        for (u, v) in prs: c[idx[('y', u, v)]] = 1
    else:
        p, pi = phase2
        add([(('z', v), 1) for v in V], p, p)
        add([(('y', u, v), 1) for (u, v) in prs], pi, pi)
        for (u, v) in prs:
            for j in J:
                add([(('a', u, v, j), 1), (('c', u, v, j), -1)] + [(('c', u, v, l), 1) for l in J if l != j], 0, np.inf)
                add([(('w', u, j), 1), (('a', u, v, j), -1)], 0, np.inf)
                add([(('w', v, j), 1), (('a', u, v, j), -1)], 0, np.inf)
        for v in V:
            if not refined:
                for j in J:  # w_vj=1 -> sum_l x_vl <= 3
                    add([(('x', v, l), 1) for l in J] + [(('w', v, j), 4)], -np.inf, 7)
            else:  # 4q <= 3d = 3(7 - #blocks)
                add([(('q', v), 1)] + [(('w', v, j), -1) for j in J], 0, np.inf)
                add([(('q', v), 4)] + [(('x', v, l), 3) for l in J], -np.inf, 21)
    integ = np.ones(N)
    A = np.array(rows)
    res = milp(c, constraints=LinearConstraint(A, lo, hi), integrality=integ, bounds=Bounds(0, [7 if (isinstance(key, tuple) and key[0] == 'q') else 1 for key in idx]),
               options={'time_limit': time_limit, 'disp': False})
    return res, idx

def exact_check(n, k, blocks):
    V = range(n)
    prs = list(itertools.combinations(V, 2))
    inb = lambda u, v, C: u in C and v in C
    Pi = [(u, v) for (u, v) in prs if not any(inb(u, v, C) for C in blocks)]
    P = set(x for pr in Pi for x in pr)
    W = []
    for j in range(7):
        A = [(u, v) for (u, v) in prs if inb(u, v, blocks[j]) and not any(inb(u, v, blocks[l]) for l in range(7) if l != j)]
        W.append(set(x for pr in A for x in pr))
    d = [7 - sum(v in C for C in blocks) for v in V]
    q = [sum(v in W[j] for j in range(7)) for v in V]
    hyp = all(d[v] >= 4 for v in V if q[v] > 0)
    hyp2 = all(4 * q[v] <= 3 * d[v] for v in V)
    delta = [min(len({u, v} - W[j]) for (u, v) in Pi) for j in range(7)]
    t = n - k + 1
    bound7 = sum(len(W[j]) + delta[j] for j in range(7))
    return dict(P=len(P), Pi=len(Pi), d=d, q=q, hyp=hyp, hyp2=hyp2, Wsizes=[len(w) for w in W], delta=delta,
                t=t, sum_bound_over7=bound7 / 7, D7=sum(4 * q[v] - 3 * d[v] for v in V))

if __name__ == '__main__':
    n, k = int(sys.argv[1]), int(sys.argv[2]); refined = len(sys.argv) > 3
    res, idx = solve(n, k)
    print('phase1 status', res.status, res.message, 'obj', res.fun)
    xs = res.x
    blocks = [set(v for v in range(n) if xs[idx[('x', v, j)]] > .5) for j in range(7)]
    info = exact_check(n, k, blocks)
    print('phase1 witness blocks', [sorted(C) for C in blocks]); print(' exact:', info)
    p, pi = info['P'], info['Pi']
    for ref in ([False, True] if not refined else [True]):
        res2, idx2 = solve(n, k, phase2=(p, pi), refined=ref)
        print('phase2 refined=%s status' % ref, res2.status, res2.message)
        if res2.status == 0:
            blocks = [set(v for v in range(n) if res2.x[idx2[('x', v, j)]] > .5) for j in range(7)]
            info2 = exact_check(n, k, blocks)
            print(' witness blocks', [sorted(C) for C in blocks]); print(' exact:', info2)
