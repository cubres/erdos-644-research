#!/usr/bin/env python3
"""w7_ref_denseTwoPart_nonint_grid.py -- targeted: G={(e,0), g*, g''} in the regime where the proof's Claim B needs
intersecting (Case 2, 3a''>2e); intersecting NOT imposed.  Exhaustive grid at rank R; tau* exact; if 4tau*>3R test
all 3^6 assignments (Lemma 7.63, explicit Fano).  Prints any instance with no anchored Fano tuple."""
import sys, itertools
from w7_ref_denseTwoPart_lib import *
R = int(sys.argv[1]); cnt = 0; bad = 0; nint = 0
for e in range(3*R//4+1, R+1):
    for x in range(R//2, 2*R+1):
        for a1 in range(1, e//2+1):
            for b1 in range(2*x//3+1, min(x, R-a1)+1):
                for a2 in range(2*e//3+1, e):
                    for b2 in range(0, min(b1, R-a2+1)):
                        G = [(e,0),(a1,b1),(a2,b2)]
                        # only states where g* and g'' are what the proof picks: beta(e/2)=b1 etc. (automatic here)
                        ts = tau_star(G, e, x)
                        if 4*ts <= 3*R: continue
                        cnt += 1; isint = intersecting(G, e, x); nint += isint
                        if not any(fano_ok([(e,0)]+list(ass), (e,x)) for ass in itertools.product(G, repeat=6)):
                            bad += 1
                            if bad <= 15: print('NO ANCHORED TUPLE', 'R',R,'e',e,'x',x,'G',G,'tau*',ts,'int',isint, flush=True)
print('R', R, 'qualifying', cnt, 'intersecting', nint, 'no anchored tuple', bad)
