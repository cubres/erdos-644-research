#!/usr/bin/env python3
"""Referee w7, claim 'paper': integer-level check of Proposition 4.1 (paper_0865.tex).
For integer r, T with beta*r+3 <= T <= r and every integer triple (m,y,z) with
z<=y<=m, 50m<=23r, 200(m+2y)<=227r, pick the case by the paper's chain on the
normalised values and verify the INTEGER hypotheses of the lemma used directly
(no scaling lemma), with the rounded S1 splits of case (c4).  All exact (Fractions).
usage: w7_ref_paper_int.py rmin rmax [sample_per_r]  (sample 0 = exhaustive)
"""
from fractions import Fraction as F
import math, random, sys

beta = F(173, 200); e = 1 - beta

def ceilF(q): return -((-q.numerator) // q.denominator)

def case_of(m, y, z, r):
    M, Y, Z = F(m, r), F(y, r), F(z, r)
    u, d, S = M+Y, M-Y, M+Y+Z
    if M <= F(119, 400): return 'a'
    if Y <= F(73, 200):
        if Y-Z > M-e: return 'b2'
        if S < F(81, 200): return 'b3'
        return 'b1'
    if Z <= F(319, 200)-2*u: return 'c1'
    if Z < e-d: return 'c2'
    if Z <= (F(146, 200)-Y)/2: return 'c3'
    return 'c4A' if 3*Z >= e+u else 'c4B'

def L26(r, x, y, z, T):
    S = x+y+z
    return T >= S and T >= r-x+z and T >= r-y+z and 2*T >= 2*r-2*x+y and 2*T >= 2*r-2*y+x and 3*T >= r+2*x+2*y+z
def L32(r, x, y, z, T):
    S = x+y+z
    return T <= r and T >= S and 2*T >= r+2*y and 2*T >= r+2*x-y+z and 3*T >= r+2*x+y+3*z
def L31(r, x, y, z, T):
    S = x+y+z
    return (T <= r and T >= x+y and 2*T >= r+2*x and 2*T >= r+2*y and T >= r+x-y-z and T >= r-x+y-z
            and 3*T >= 3*r-S and 5*T >= 3*r+S and 3*T >= r+x+y+2*z and 4*T >= 2*r+3*z)
def S2(r, x, y, z, T):
    P = max(0, r+y-x-z-T); Q = max(0, r+x-y-z-T)
    return x <= T and y <= T and T >= r-x+z+P+Q and T >= y+z+Q and 2*T >= r+y+2*z+P+2*Q
def S1(r, x, y, z, x1, y1, z1, T):
    return (0 <= x1 <= x and 0 <= y1 <= y and 0 <= z1 <= z and x1+y1+z1 <= T and
            y1+z1 >= r+x-T and x1+z1 >= r+y-T and x1+y1 >= r+z-T)
def L18ok(r, m, T):
    B = max(ceilF(F(3*r+m, 4)), ceilF(F(2*r+2*m, 3)))
    return 2*m <= r and B <= T

def check(r, T, m, y, z):
    c = case_of(m, y, z, r)
    if c == 'a': return c, L18ok(r, m, T)
    if c == 'b2': return c, L32(r, m, y, z, T)
    if c == 'b3': return c, L32(r, z, y, m, T)
    if c == 'b1': return c, L31(r, z, y, m, T)
    if c == 'c1': return c, L26(r, m, y, z, T)
    if c == 'c2': return c, S2(r, y, m, z, T)
    if c == 'c3': return c, S2(r, m, y, z, T)
    M, Y, Z = F(m, r), F(y, r), F(z, r)
    if c == 'c4A':
        m1 = (e+Y+Z-M)/2; y1 = (e+M+Z-Y)/2; z1 = (e+M+Y-Z)/2
    else:
        z1 = Z; y1 = e+M-Z; m1 = e+Y-Z
    hm, hy, hz = ceilF(m1*r), ceilF(y1*r), ceilF(z1*r)
    return c, S1(r, m, y, z, hm, hy, hz, T)

def main():
    rmin, rmax = int(sys.argv[1]), int(sys.argv[2])
    samp = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    rnd = random.Random(rmin*7919+rmax)
    tot = 0; bad = []
    from collections import Counter
    cnt = Counter()
    for r in range(rmin, rmax+1):
        Tmin = ceilF(beta*r+3) - int(__import__("os").environ.get("TMUT","0"))
        if Tmin > r: continue
        mmax = (23*r)//50
        for T in sorted({Tmin, r}):
            if samp == 0:
                it = ((m, y, z) for m in range(mmax+1) for y in range(min(m, (227*r//200 - m)//2 if 227*r-200*m >= 0 else -1)+1) for z in range(y+1))
            else:
                def gen():
                    k = 0
                    while k < samp:
                        m = rnd.randint(0, mmax); y = rnd.randint(0, m); z = rnd.randint(0, y)
                        if 200*(m+2*y) <= 227*r:
                            k += 1; yield (m, y, z)
                it = gen()
            for (m, y, z) in it:
                if 200*(m+2*y) > 227*r: continue
                c, ok = check(r, T, m, y, z)
                cnt[c] += 1; tot += 1
                if not ok:
                    bad.append((r, T, m, y, z, c))
    print('checked', tot, dict(cnt), 'failures', len(bad), bad[:10])

if __name__ == '__main__':
    main()
