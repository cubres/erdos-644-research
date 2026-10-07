#!/usr/bin/env python3
"""w6c_seven_check.py -- brute-force sanity check of the SEVEN-ROW joint-minimisation lemma on random small
(7,2) families: for a lex (|P7|,|Pi7|)-minimal 7-multiset of edges, every W_i u {u,v} ({u,v} in Pi7) is a
transversal; and 7 tau <= sum_i (|W_i| + delta_i).  Exhaustive over 7-multisets (small families)."""
import itertools, random, sys
from lib72 import is_72, tau
def pairs_piercing(R, n):
    out = []
    for x in range(n):
        for y in range(x + 1, n):
            m = (1 << x) | (1 << y)
            if all(F & m for F in R): out.append((x, y))
    return out
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
checked = 0; fams = 0
while fams < 60:
    n = random.randint(6, 9); k = random.randint(2, 5); m = random.randint(5, 10)
    H = list(set(sum(1 << v for v in random.sample(range(n), random.randint(2, k))) for _ in range(m)))
    if not is_72(H, n): continue
    t = tau(H, n)
    if t < 2: continue
    fams += 1
    best = None; bestF = None
    for F in itertools.combinations_with_replacement(range(len(H)), 7):
        R = [H[j] for j in F]
        Pi = pairs_piercing(R, n)
        P = set(x for pr in Pi for x in pr)
        key = (len(P), len(Pi))
        if best is None or key < best: best = key; bestF = (R, Pi)
    R, Pi = bestF; Pis = set(Pi)
    tot = 0
    for i in range(7):
        Gi = pairs_piercing(R[:i] + R[i+1:], n)
        Wi = set(x for pr in Gi if pr not in Pis for x in pr)
        for (u, v) in Pi:
            X = Wi | {u, v}
            mask = sum(1 << z for z in X)
            assert all(E & mask for E in H), ('FAIL', H, R, i)
            checked += 1
        tot += len(Wi) + min(len({u, v} - Wi) for (u, v) in Pi)
    assert 7 * t <= tot, ('SUM FAIL', H)
print('families', fams, 'transversal checks', checked, 'ALL PASS')
