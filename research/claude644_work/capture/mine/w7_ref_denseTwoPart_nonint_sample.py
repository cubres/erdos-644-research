#!/usr/bin/env python3
"""w7_ref_denseTwoPart_nonint_sample.py -- sampled version of the Claim-B regime (3a''>2e, 3b*>2x), rank R=100,
types {anchor, g*, g''} (+ optional random extras), NOT intersecting; exact tau*; all assignments via Lemma 7.63."""
import sys, random, itertools
from w7_ref_denseTwoPart_lib import *
seed, R, trials = map(int, sys.argv[1:4]); random.seed(seed)
cnt = bad = 0
for _ in range(trials):
    e = random.randint(3*R//4+1, R); x = random.randint(R, 3*R//2)
    a1 = random.randint(1, e//4); b1 = random.randint(2*x//3+1, max(2*x//3+1, min(x, R-a1)))
    if b1 > min(x, R-a1): continue
    a2 = random.randint(2*e//3+1, e-1); b2 = random.randint(0, min(b1-1, R-a2))
    G = [(e,0),(a1,b1),(a2,b2)]
    for _ in range(random.choice([0,0,1,2])):
        a = random.randint(1, e); G.append((a, random.randint(0, min(x, R-a))))
    G = list(dict.fromkeys(G))
    ts = tau_star_fixed(G, e, x)
    if ts is None or 4*ts <= 3*R: continue
    ts = tau_star(G, e, x)
    if 4*ts <= 3*R: continue
    cnt += 1
    if not any(fano_ok([(e,0)]+list(ass), (e,x)) for ass in itertools.product(G, repeat=6)):
        bad += 1
        if bad <= 10: print('NO ANCHORED TUPLE', 'R',R,'e',e,'x',x,'G',G,'tau*',ts,'int',intersecting(G,e,x), flush=True)
print('R', R, 'qualifying', cnt, 'no anchored tuple', bad)
