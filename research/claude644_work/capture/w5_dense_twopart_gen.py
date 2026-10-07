#!/usr/bin/env python3
"""w5_dense_twopart_gen.py -- generator of 2-part staircase type sets with tau* > 3r/4 (by construction, verified
exactly afterwards) that are intersecting; used by w5_dense_twopart_theorem_check2.py"""
import random
from w5_dense_anchor_climb import tau_star, intersecting
def gen(r, extra=0, beyond=False):
    e = random.randint(3*r//4 + 1, r)
    T = random.randint(3*r//4 + 1, e)
    lo = max(1, 3*r//4)
    if beyond: lo = max(lo, (9*r - 6*e)//4 + 1)
    x = random.randint(lo, 2*r)
    c = e + x - T                      # need a + beta(a) < c for all a < e  (strict)
    G = []
    a = random.randint(1, max(1, min(e - T, e)))   # for a' < a: a' + x < c  <=> a' < e - T
    while True:
        bmax = min(x, r - a)
        # strictness: next corner a2 must satisfy a2 - 1 + b < c  -> a2 <= c - b ; and a2 > a
        bmin = 0
        for (aj, bj) in G:
            if a + aj <= e: bmin = max(bmin, x - bj + 1)
        if 2*a <= e: bmin = max(bmin, x//2 + 1)
        if a >= e: G.append((e, 0)); break
        # b must allow a next corner: c - b > a  -> b < c - a
        bmax = min(bmax, c - a - 1)
        if bmax < bmin: return None
        b = random.choice([bmax, random.randint(bmin, bmax)])
        G.append((a, b))
        a2max = min(e, c - b)
        a2 = random.randint(a + 1, a2max) if random.random() < 0.5 else a2max
        a = a2
        if a >= e: G.append((e, 0)); break
    for _ in range(extra):
        aa = random.randint(1, e); bb = random.randint(0, min(x, r - aa)); G.append((aa, bb))
    G = sorted(set(G))
    caps = [e, x]
    if not intersecting([list(g) for g in G], caps): return None
    ts = tau_star([list(g) for g in G], caps)
    if 4*ts <= 3*r: return None
    return e, x, G, ts
