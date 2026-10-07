#!/usr/bin/env python3
"""w4_tcglobal_k4_logic.py -- exact finite checks (Claude, 23 Sep 2026):
 (1) TC Fano plane: points p0,p1,q,r1..r4; lines L={p0,p1,q}, B1={p0,r1,r2}, B2={p0,r3,r4}, C1={p1,r1,r3},
     C2={p1,r2,r4}, g1={q,r1,r4}, g2={q,r2,r3} form a Fano plane.
 (2) K4 dictionary: non-L line {x,r_a,r_b} <-> K4 edge ab; the two lines through an L-point <-> a perfect matching.
     For EVERY subset sigma of the six non-L lines: sigma is safe (some Fano point on no line of sigma)
     iff sigma contains no triangle of K4 (i.e. no three lines {ab,bc,ca}).
 (3) Among all 2^7 sets of Fano lines, unsafe <=> contains three concurrent lines.
 (4) TC* labelling: for the refined labels (x in B_i n C_j only -> r-point off B_i u C_j; >=3 -> q) every
     vertex type is safe given g1 avoids X_11 u X_22 u X_q and g2 avoids X_12 u X_21 u X_q.
Exit 0 iff all pass. Pure finite enumeration."""
import itertools, sys
P = ['p0','p1','q','r1','r2','r3','r4']
LN = {'L':{'p0','p1','q'},'B1':{'p0','r1','r2'},'B2':{'p0','r3','r4'},'C1':{'p1','r1','r3'},
      'C2':{'p1','r2','r4'},'g1':{'q','r1','r4'},'g2':{'q','r2','r3'}}
ok = True
def chk(c, m):
    global ok
    if not c: ok = False; print("FAIL", m)
pairs = set()
for l in LN.values():
    for a,b in itertools.combinations(sorted(l),2): pairs.add((a,b))
chk(len(pairs)==21 and all(len(l)==3 for l in LN.values()), "Fano")
def safe(sig): return any(all(p not in LN[l] for l in sig) for p in P)
six = ['B1','B2','C1','C2','g1','g2']
edge = {l: frozenset(int(x[1]) for x in LN[l] if x.startswith('r')) for l in six}
tri = [frozenset(frozenset(e) for e in itertools.combinations(T,2)) for T in itertools.combinations([1,2,3,4],3)]
for r in range(7):
    for sig in itertools.combinations(six, r):
        es = frozenset(edge[l] for l in sig)
        has_tri = any(T <= es for T in tri)
        chk(safe(sig) == (not has_tri), ("K4", sig))
# matchings
for x in ['p0','p1','q']:
    ls = [l for l in six if x in LN[l]]
    chk(len(ls)==2 and not (edge[ls[0]] & edge[ls[1]]), ("matching", x))
# (3)
allL = list(LN)
conc = [frozenset(l for l in allL if p in LN[l]) for p in P]
for r in range(8):
    for sig in itertools.combinations(allL, r):
        s = frozenset(sig)
        chk((not safe(sig)) == any(c <= s for c in conc), ("concurrent", sig))
# (4) refined TC labels: vertex outside E with membership pattern among B1,B2,C1,C2 (+ g's per rule)
off = {('B1','C1'):'r4',('B1','C2'):'r3',('B2','C1'):'r2',('B2','C2'):'r1'}
for r in range(5):
    for pat in itertools.combinations(['B1','B2','C1','C2'], r):
        nb = sum(1 for x in pat if x[0]=='B'); nc = len(pat)-nb
        if nb >= 1 and nc >= 1:
            if len(pat) == 2:
                lab = off[pat]
                gs = ['g1'] if lab in ('r4','r1') else ['g2']   # g avoiding it
                # vertex may lie in the other g
                others = [g for g in ('g1','g2') if g not in gs]
                sig = list(pat) + others
                chk(all(lab not in LN[l] for l in sig), ("refined", pat))
            else:
                sig = list(pat); chk(all('q' not in LN[l] for l in sig), ("q", pat))
        elif nb >= 1:   # only B's -> p1 ; may lie in g's
            chk(all('p1' not in LN[l] for l in list(pat)+['g1','g2']), ("p1", pat))
        else:           # only C's or none -> p0
            chk(all('p0' not in LN[l] for l in list(pat)+['g1','g2']), ("p0", pat))
print("ALL PASS" if ok else "SOME FAIL"); sys.exit(0 if ok else 1)
