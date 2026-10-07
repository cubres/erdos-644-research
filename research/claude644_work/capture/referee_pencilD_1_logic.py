#!/usr/bin/env python3
"""Referee check (independent) of the Fano logic behind Lemma D / D'.
(a) builds PG(2,2) from F_2^3, checks the addendum's naming (pencil + m-lines);
(b) exhaustively checks every pair of MAXIMAL membership patterns has a commonly
    missed line (this is exactly the bad-7-tuple conclusion), for Lemma D and D'
    with the stated pairing, and also tests which other pairings work.
"""
import itertools
pts = [v for v in itertools.product([0,1],repeat=3) if any(v)]
lines = []
for a,b in itertools.combinations(pts,2):
    c = tuple((x+y)%2 for x,y in zip(a,b))
    L = frozenset([a,b,c])
    if L not in lines: lines.append(L)
assert len(lines)==7
p0 = (0,0,1)
pencil = [L for L in lines if p0 in L]
mlines = [L for L in lines if p0 not in L]
assert len(pencil)==3 and len(mlines)==4
# name points: l1={p0,a,a'}, etc.
l1,l2,l3 = pencil
a,ap = sorted(l1-{p0}); b,bp = sorted(l2-{p0})
# c is the third point of the m-line through a,b
M1 = [L for L in mlines if a in L and b in L][0]
c = next(iter(M1-{a,b})); cp = next(iter(l3-{p0,c}))
name = {p0:'p0',a:'a',ap:"a'",b:'b',bp:"b'",c:'c',cp:"c'"}
want = [{a,b,c},{ap,bp,c},{ap,b,cp},{a,bp,cp}]
assert sorted(map(sorted,want))==sorted(map(sorted,[set(L) for L in mlines])), "m-line naming"
M1,M2,M3,M4 = [frozenset(s) for s in want]
for x in [a,ap,b,bp,c,cp]:
    assert sum(x in L for L in pencil)==1 and sum(x in L for L in mlines)==2
print("Fano naming OK: m-lines", [sorted(name[p] for p in M) for M in (M1,M2,M3,M4)])

LINES = {'l1':l1,'l2':l2,'l3':l3,'M1':M1,'M2':M2,'M3':M3,'M4':M4}
def safe(S):
    return any(all(p not in LINES[l] for l in S) for p in pts)

def check(avoid_l2, avoid_l3, label='stated'):
    # maximal membership patterns
    pats = []
    for lab in pts:   # U-vertices: in G_l iff label not on l (maximal); E only has labels b,b',c,c'
        S = {l for l,L in LINES.items() if lab not in L}
        if lab in (p0,a,ap): S.discard('l1')      # E contains no R-vertex
        pats.append(('U:'+name[lab],S))
    for in2,in3 in itertools.product([0,1],repeat=2):   # outside vertices (label p0)
        S = {'M1','M2','M3','M4'}
        if in2: S |= {'l2'}; S -= set(avoid_l2)
        if in3: S |= {'l3'}; S -= set(avoid_l3)
        pats.append((f'out:{in2}{in3}',S))
    bad=[]
    for (n1,S1),(n2,S2) in itertools.combinations_with_replacement(pats,2):
        if not any(l not in S1 and l not in S2 for l in LINES): bad.append((n1,n2))
    unsafe=[n for n,S in pats if not safe(S)]
    return bad, unsafe

print("Lemma D (no protrusion):", check(['M1','M2','M3','M4'],['M1','M2','M3','M4']))
print("Lemma D' stated pairing:", check(['M1','M4'],['M2','M3']))
# which pairs of m-lines work for l2 (resp l3) alone
ms=['M1','M2','M3','M4']
ok=[]
for P2 in itertools.combinations(ms,2):
    for P3 in itertools.combinations(ms,2):
        bad,uns=check(list(P2),list(P3))
        if not bad: ok.append((P2,P3))
print("all working pairings (l2-avoiders, l3-avoiders):",len(ok))
for o in ok: print("  ",o)
# can one avoid a single m-line only?
for P2 in ms:
    for P3 in ms:
        bad,_=check([P2],[P3])
        if not bad: print("single-line pairing works:",P2,P3)
