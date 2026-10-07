#!/usr/bin/env python3
"""
referee_lemmaZ_converse.py (referee w12, claim generalp#1).  Exact check of the key inequality behind
   Th_Z'(p)  ==>  Th_Z(p)   (so the two statements are EQUIVALENT, not 'formally weaker'):
Given integer Gen (0 <= g <= n, |g| <= r) let U_M := { integer v : |v| = Mr, Mg <= v <= Mn for some g }  (the integer
unit points of M G_r).  Claim:  sup free(U_M) <= max( sup free(M Gen), Mr + p - 1 ),  i.e.
   tau*(U_M) >= min( M tau*(Gen), M(N - r) - p + 1 ).
Proof: w free for U_M, |floor w| >= Mr and Mg <= w => Mg <= floor w, raise Mg inside floor w to mass Mr: a point of U_M
below w, contradiction; so either |floor w| <= Mr - 1 (|w| < Mr - 1 + p) or w is free for M Gen.
Since tau*(Gen) > 3r/4 and N - r > 3r/4 in the Th_Z hypothesis, tau*(U_M) > 3Mr/4 for large M; Th_Z' on U_M (rows unit,
rank Mr) gives a bad tuple with rows in U_M subset M G_r.
We verify the inequality exactly with the corner enumerator for random small integer instances and M = 1,2,3.
"""
from fractions import Fraction as Fr
from itertools import product
import random, sys
sys.path.insert(0, __file__.rsplit('/',1)[0])
from ref2_lemmaZ_check import sup_free_exact

def unit_points(Gen, n, R):
    pts = set()
    p = len(n)
    rngs = [range(0, n[i]+1) for i in range(p)]
    for v in product(*rngs):
        if sum(v) != R: continue
        if any(all(g[i] <= v[i] for i in range(p)) for g in Gen):
            pts.add(tuple(Fr(c) for c in v))
    return list(pts)

def main(seed=3, trials=150):
    random.seed(seed)
    fails = 0; done = 0; tight = 0
    for t in range(trials):
        p = random.choice([2,3])
        n = [random.randint(0, 4) for _ in range(p)]
        r = random.randint(1, max(1, sum(n)))
        Gen = []
        for _ in range(random.randint(1,3)):
            g = [random.randint(0, n[i]) for i in range(p)]
            while sum(g) > r:
                i = random.randrange(p)
                if g[i] > 0: g[i] -= 1
            Gen.append(tuple(Fr(c) for c in g))
        nF = [Fr(c) for c in n]
        for M in (1,2,3):
            if M*sum(n) > 14: continue
            GM = [tuple(M*c for c in g) for g in Gen]
            nM = [M*c for c in nF]
            U = unit_points([tuple(int(c) for c in g) for g in GM], [M*c for c in n], M*r)
            if not U: continue
            lhs = sup_free_exact(U, nM)
            rhs = max(sup_free_exact(GM, nM), Fr(M*r + p - 1))
            done += 1
            if lhs > rhs:
                fails += 1; print("FAIL", n, r, Gen, M, lhs, rhs)
            if lhs == rhs: tight += 1
    print("checked", done, "failures", fails, "equality cases", tight)
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
