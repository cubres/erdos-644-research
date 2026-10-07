#!/usr/bin/env python3
"""w4_tcglobal_spread_pg.py -- exact end-to-end demonstration of the SPREAD LEMMA mechanism on PG(2,q), q prime.
E0 = a line, balanced quartering; b1,b2 fixed lines with the trace conditions; c1,c2 drawn uniformly from the lines
through points of E1uE3 resp. E2uE4 (the uniform distribution has outside marginals 2/(q+1) < spread threshold).
Whenever |X| <= s (s = t-1-ceil(e/2), t = q+1), pick g1,g2 avoiding X u E1 u E4, X u E2 u E3 and verify that the
7 lines have NO 2-point transversal (exact).  Also prints the expected |X| bound |U|(p+q) vs s+1.
Usage: python3 w4_tcglobal_spread_pg.py q trials seed"""
import sys, random, itertools
q, trials, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); random.seed(seed)
pts = []
for x in range(q):
    for y in range(q):
        for z in range(q):
            v = (x,y,z)
            if v == (0,0,0): continue
            i = next(i for i in range(3) if v[i]); inv = pow(v[i], q-2, q)
            if tuple(c*inv % q for c in v) == v: pts.append(v)
idx = {p:i for i,p in enumerate(pts)}
lines = []
for l in pts:
    lines.append(frozenset(idx[p] for p in pts if (l[0]*p[0]+l[1]*p[1]+l[2]*p[2]) % q == 0))
t = q+1; e = q+1
def two_pierce(E):
    V = set().union(*E)
    for x in V:
        rest = [L for L in E if x not in L]
        if not rest: return True
        common = frozenset.intersection(*rest)
        if common: return True
    return False
E0 = lines[0]; ev = sorted(E0); random.shuffle(ev)
j, r = divmod(e, 4); sizes = [j+1]*r + [j]*(4-r)
# arrange so that |E1uE4|,|E2uE3| <= ceil(e/2): sizes sorted desc -> E1,E2,E3,E4 = s0,s2,s3,s1 pattern
s_sorted = sorted(sizes, reverse=True)
order = s_sorted
Q, pos = [], 0
for sz in order: Q.append(frozenset(ev[pos:pos+sz])); pos += sz
E1,E2,E3,E4 = Q
ce = -(-e//2)
assert len(E1|E4) <= ce and len(E2|E3) <= ce
s = t-1-max(len(E1|E4), len(E2|E3))
def inside(L, half): return (L & E0) <= half
O = lambda half: [L for L in lines if L != E0 and inside(L, half)]
b1 = random.choice(O(E3|E4)); b2 = random.choice(O(E1|E2))
U = (b1|b2) - E0
O13, O24 = O(E1|E3), O(E2|E4)
# exact outside marginals of the uniform distributions
from fractions import Fraction
def maxmarg(F):
    cnt = {}
    for L in F:
        for v in L - E0: cnt[v] = cnt.get(v,0)+1
    return Fraction(max(cnt.values()), len(F))
p13, p24 = maxmarg(O13), maxmarg(O24)
print("q",q,"t",t,"s",s,"|U|",len(U),"p13",p13,"p24",p24,"bound |U|(p+q) =",float(len(U)*(p13+p24)),"vs s+1 =",s+1)
wins = fails = 0
for _ in range(trials):
    c2 = random.choice(O13); c1 = random.choice(O24)
    X = ((b1|b2) & (c1|c2)) - E0
    if len(X) > s: continue
    g1 = next((L for L in lines if not (L & (X|E1|E4))), None)
    g2 = next((L for L in lines if not (L & (X|E2|E3))), None)
    assert g1 is not None and g2 is not None
    wins += 1
    if two_pierce([E0,b1,b2,c1,c2,g1,g2]): fails += 1
print("draws with |X|<=s:", wins, "of", trials, " bad-tuple verification failures:", fails)
sys.exit(1 if fails else 0)
