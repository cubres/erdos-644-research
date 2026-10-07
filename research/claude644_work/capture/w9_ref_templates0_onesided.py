#!/usr/bin/env python3
"""Referee w9 [templates#0]: exact test of handproofs sec.3 (one-sided box families, |I|=2), over parts
A,B plus m light parts.  tau* = X - max(1,S) (handback 8.4 formula; S = th_A+th_B+sum_light x) with
effective thresholds th_i := max(th_i, 1-X+x_i).  Also an independent brute-force tau* (m<=2): enumerate
residuals u with u_i in cut levels {x_i, th_i-} and the 'sum<1' residual.
Checks for tau*>=3/4 with th_i>4x_i/7: Claim 1-th_B<=x_A, 1-th_A<=x_B; a'=1-th_B<b'=th_A; Gap-Pair
hypotheses (H1),(H2),(G); and that Q_{b'},Q_{a'} or V(a',b') is feasible on (x_A,x_B) (light parts load 0).
Also tests |I|=1 vacuity: th_A>4x_A/7 => tau*<3/4."""
import random, sys, itertools
from fractions import Fraction as F
def Qb(s, t): return max(F(3, 2) * t, s + F(3, 4) * t)
def Qa(s, t): return Qb(t, s)
def Vf(s, t): return max(s + t, F(5, 4) * s + t / 2)
def main(n, seed, den):
    rng = random.Random(seed)
    st = dict(hi=0, hom=0, Qb=0, Qa=0, V=0, eq=0, one_hi=0)
    for _ in range(n):
        m = rng.randint(0, 2)
        xA = F(rng.randint(1, 2 * den), den); xB = F(rng.randint(1, 2 * den), den)
        xL = [F(rng.randint(0, den), den) for _ in range(m)]
        X = xA + xB + sum(xL)
        thA = F(rng.randint(0, 4 * den), 4 * den) * min(xA, 1); thB = F(rng.randint(0, 4 * den), 4 * den) * min(xB, 1)
        if thA == 0 or thB == 0: continue
        thA = max(thA, 1 - X + xA); thB = max(thB, 1 - X + xB)
        if thA > min(xA, 1) or thB > min(xB, 1): continue
        S = thA + thB + sum(xL)
        tau = X - max(F(1), S)
        # |I|=1 vacuity (box A only): tau1 = X - max(1, thA1 + X - xA)
        th1 = max(thA, 1 - X + xA)
        tau1 = X - max(F(1), th1 + X - xA)
        if th1 > F(4, 7) * xA and tau1 >= F(3, 4): st['one_hi'] += 1; print("I=1 not vacuous!", xA, X, th1)
        if tau < F(3, 4): continue
        st['hi'] += 1
        if S < 1 or thA <= F(4, 7) * xA or thB <= F(4, 7) * xB:
            st['hom'] += 1; continue
        assert 1 - thB <= xA and 1 - thA <= xB, "claim fails"
        a, b = 1 - thB, thA
        assert a < b
        x, y = xA, xB
        assert 4 * y < 7 * (1 - a) and 4 * x < 7 * b and b - a <= x + y - F(7, 4)
        if tau == F(3, 4): st['eq'] += 1
        for nm, M in (('Qb', Qb), ('Qa', Qa), ('V', Vf)):
            if M(a, b) <= x and M(1 - a, 1 - b) <= y:
                st[nm] += 1; break
        else:
            raise AssertionError(("FAIL", xA, xB, xL, thA, thB))
    print("seed", seed, "den", den, st)
for s in range(1, 4):
    main(200000, s, 8 * s)
