#!/usr/bin/env python3
"""w4_tcglobal_convex2_exact.py -- exact rational grid check, TWO parts: Adm = {(s,1-s): s in [al,be]} (any convex
Adm in 2 parts is such an interval), capacities x1,x2.  tau* = min(x1-al, x2-1+be, x1+x2-1) (exact formula, derived
in notes).  Anchor a0 = (s0,1-s0), s0 in [al,be].  Homogeneous anchored template: exists s in [al,be] with
6(s,1-s) + a0 <= 4x.  Reports any case with tau* > 3/4 where the template fails for some anchor.  Pure Fractions."""
from fractions import Fraction as F
import itertools, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 24
grid = [F(i, N) for i in range(0, 2*N+1)]
bad = 0; tested = 0
for x1 in grid:
    for x2 in grid:
        if x1 + x2 <= F(7,4): continue
        for al in grid:
            if al > 1: break
            for be in grid:
                if be < al or be > 1: continue
                if be > x1 or 1-al > x2: continue       # all of Adm must fit (a <= x)
                tau = min(x1-al, x2-1+be, x1+x2-1)
                if tau <= F(3,4): continue
                tested += 1
                for s0 in (al, be, (al+be)/2):
                    lo = max(al, (7 - s0 - 4*x2)/6 + 0)   # 6(1-s)+(1-s0) <= 4x2  <=> s >= (7-s0-4x2)/6
                    hi = min(be, (4*x1 - s0)/6)
                    if lo > hi:
                        bad += 1
                        if bad <= 10: print("FAIL x", x1, x2, "Adm s in", [al, be], "anchor s0", s0, "tau*", tau)
print("tested", tested, "failures", bad)
