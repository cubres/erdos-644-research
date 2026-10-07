#!/usr/bin/env python3
"""Referee w9 [templates#0]: exact end-to-end test of Theorem 7.75' (closed two-part type sets) following the
written proof, plus an independent brute-force tau* for finite C.
Model: parts x,y; type c = first-part size, admissible iff max(0,1-y) <= c <= min(1,x).
tau* (finite C): infimum cost of residual (r1,r2) leaving no type: brute force over cut levels
  r1 in {x} u {c-} , r2 in {y} u {(1-c)-}  plus the 'total < 1' residual (cost N-1).
Proof steps checked: H=[1-4y/7,4x/7]; if C meets H -> homogeneous Fano (7c/4<=x,7(1-c)/4<=y);
else a=max(C below H), b=min(C above H), check (H1),(H2),(G) and that Q_b, Q_a or V(a,b) is feasible.
Usage: python3 w9_ref_templates0_closed2.py n seed den
"""
import random, sys
from fractions import Fraction as F
def tau_formula(C, x, y):
    C = sorted(C); N = x + y
    v = [N - 1]
    if C[0] > 0: v.append(x - C[0])
    if C[-1] < 1: v.append(y - 1 + C[-1])
    for u, w in zip(C, C[1:]):
        v.append(N - 1 - (w - u))
    return min(v)
def tau_brute(C, x, y):
    N = x + y; best = N - 1
    R1 = [(x, False)] + [(c, True) for c in C]           # (level, strict-cut)
    R2 = [(y, False)] + [(1 - c, True) for c in C]
    for r1, s1 in R1:
        for r2, s2 in R2:
            if r1 > x or r2 > y or (s1 and r1 <= 0) or (s2 and r2 <= 0): continue
            surv = [c for c in C if (c < r1 if s1 else c <= r1) and ((1 - c) < r2 if s2 else (1 - c) <= r2)]
            if not surv:
                best = min(best, (x - r1) + (y - r2))
    return best
def Qb(s, t): return max(F(3, 2) * t, s + F(3, 4) * t)
def Qa(s, t): return Qb(t, s)
def Vf(s, t): return max(s + t, F(5, 4) * s + t / 2)
def feas(M, a, b, x, y):  # a = five/"s" type, b = "t" type
    return M(a, b) <= x and M(1 - a, 1 - b) <= y
def check(C, x, y, stats):
    t = tau_formula(C, x, y)
    tb = tau_brute(C, x, y)
    assert t == tb, (C, x, y, t, tb)
    if t < F(3, 4):
        stats['low'] += 1; return
    stats['hi'] += 1
    lo, hi = 1 - F(4, 7) * y, F(4, 7) * x
    assert lo <= hi, ("H empty with tau*>=3/4", C, x, y)   # the proof's unstated step: N>=7/4
    inH = [c for c in C if lo <= c <= hi]
    if inH:
        c = inH[0]; assert F(7, 4) * c <= x and F(7, 4) * (1 - c) <= y
        stats['H'] += 1; return
    below = [c for c in C if c < lo]; above = [c for c in C if c > hi]
    assert below and above, ("one-sided", C, x, y, t)
    a, b = max(below), min(above)
    assert 4 * y < 7 * (1 - a) and 4 * x < 7 * b and b - a <= x + y - F(7, 4)
    if feas(Qb, a, b, x, y): stats['Qb'] += 1
    elif feas(Qa, a, b, x, y): stats['Qa'] += 1
    elif feas(Vf, a, b, x, y): stats['V'] += 1
    else:
        raise AssertionError(("GAP-PAIR FAILS", C, x, y, a, b))
    if t == F(3, 4): stats['eq'] += 1
def main():
    n, seed, den = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    stats = dict(low=0, hi=0, H=0, Qb=0, Qa=0, V=0, eq=0)
    for it in range(n):
        x = F(rng.randint(den // 2, 2 * den), den); y = F(rng.randint(den // 2, 2 * den), den)
        lo, hi = max(F(0), 1 - y), min(F(1), x)
        if lo > hi: continue
        mode = rng.random()
        pts = set()
        m = rng.randint(1, 6)
        Hlo, Hhi = 1 - F(4, 7) * y, F(4, 7) * x
        for _ in range(m):
            c = F(rng.randint(0, 4 * den), 4 * den)
            if lo <= c <= hi:
                if mode < 0.7 and Hlo <= c <= Hhi:
                    continue       # avoid the hole most of the time (the interesting case)
                pts.add(c)
        if mode < 0.5:  # plant a tight gap pair around H
            a = Hlo - F(rng.randint(1, den), 8 * den); b = Hhi + F(rng.randint(1, den), 8 * den)
            for c in (a, b):
                if lo <= c <= hi: pts.add(c)
        if not pts: continue
        check(sorted(pts), x, y, stats)
    print("seed", seed, "den", den, stats)
main()
