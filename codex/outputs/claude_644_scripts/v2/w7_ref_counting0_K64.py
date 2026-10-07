#!/usr/bin/env python3
"""w7_ref_counting0_K64.py -- exhaustive (no MILP): all lex (|P7|,|Pi7|)-minimising 7-multisets of K_6^(4);
reports whether ANY minimiser satisfies the corollary hypothesis (d) or the refined 4q<=3d, plus D7 values."""
import itertools
from collections import Counter
import w7_ref_counting0_bf as B
n, k = 6, 4
H = [sum(1 << v for v in S) for S in itertools.combinations(range(n), k)]
best = None; mins = []
for F in itertools.combinations_with_replacement(range(len(H)), 7):
    R = [H[j] for j in F]; Pi = B.pairs_of(R, n)
    assert Pi
    P = set(x for pr in Pi for x in pr); key = (len(P), len(Pi))
    if best is None or key < best: best = key; mins = [R]
    elif key == best: mins.append(R)
t = B.tau(H, n); cnt = Counter()
for R in mins:
    Pi = B.pairs_of(R, n); W = B.quantities(R, n, Pi)
    d = [sum((F >> v) & 1 for F in R) for v in range(n)]
    q = [sum(v in W[i] for i in range(7)) for v in range(n)]
    hyp = all(d[v] >= 4 for v in range(n) if q[v]); hyp2 = all(4 * q[v] <= 3 * d[v] for v in range(n))
    D7 = sum(4 * q[v] - 3 * d[v] for v in range(n))
    cnt[(hyp, hyp2, D7)] += 1
print('K_6^4 t', t, 'lex min', best, 'number of minimising multisets', len(mins))
print('(hyp, refined hyp, D7) -> count:', dict(cnt))
