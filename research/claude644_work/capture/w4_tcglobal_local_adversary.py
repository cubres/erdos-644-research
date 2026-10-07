#!/usr/bin/env python3
"""w4_tcglobal_local_adversary.py -- exact simulation of the LOCAL adversarial game against the bounded TC script.
Prover: E0 (k points), balanced quartering; b1 := request avoiding E1uE2 u S1, b2 avoiding E3uE4 u S2, c1 avoiding
E1uE3 u S3, c2 avoiding E2uE4 u S4, with each extra set S of size s = T-ceil(e/2) chosen greedily inside the current
x-union U=(b1ub2)\\E0 (the prover's best static choice: c's avoid the SAME s points of U).
Adversary ('dive'): b's take their allowed half of E0 plus FRESH outside points (so |U| = 2(k-e/2)); c's take their
allowed half plus as many points of U\\S as possible, then fresh points.  Every answered set avoids its request, has
size k, and T = t-1 is the request budget.  Prints |X| and s for t/k in a range: TC fires iff |X| <= s.
Shows the bounded TC script cannot beat t ~ k without global information."""
import sys
k = int(sys.argv[1]) if len(sys.argv) > 1 else 40
for num in range(60, 101, 5):
    t = (num*k)//100; T = t-1; e = k; ce = -(-e//2); s = T - ce
    if s < 0: continue
    E = list(range(e)); q = e//4
    E1, E2, E3, E4 = set(E[:q]), set(E[q:2*q]), set(E[2*q:3*q]), set(E[3*q:])
    fresh = iter(range(1000, 100000))
    b1 = (E3|E4) | {next(fresh) for _ in range(k - len(E3|E4))}
    b2 = (E1|E2) | {next(fresh) for _ in range(k - len(E1|E2))}
    U = (b1|b2) - set(E)
    S = set(sorted(U)[:s])                     # prover: both c's avoid the same s points of U
    def dive(half):
        c = set(half); pool = sorted(U - S)
        for v in pool:
            if len(c) >= k: break
            c.add(v)
        while len(c) < k: c.add(next(fresh))
        return c
    c1 = dive(E2|E4); c2 = dive(E1|E3)
    assert not (c1 & (E1|E3|S)) and not (c2 & (E2|E4|S))
    X = ((b1|b2) & (c1|c2)) - set(E)
    print(f"t/k={t/k:.2f}  s={s}  |X|={len(X)}  TC fires: {len(X) <= s}")
