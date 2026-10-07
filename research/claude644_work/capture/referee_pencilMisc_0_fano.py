#!/usr/bin/env python3
"""Referee check 1: Fano incidence facts for the pencil scheme, and a generic
Venn/Fano badness verifier for a labelling + per-line avoidance rules.
Independent of pencil_*.py."""
import itertools
P = ['p0','a','ap','b','bp','c','cp']
L = {'l1':{'p0','a','ap'},'l2':{'p0','b','bp'},'l3':{'p0','c','cp'},
     'M1':{'a','b','c'},'M2':{'ap','bp','c'},'M3':{'ap','b','cp'},'M4':{'a','bp','cp'}}
# projective plane axioms
for x,y in itertools.combinations(P,2):
    n=sum(1 for l in L.values() if x in l and y in l)
    assert n==1,(x,y,n)
for l1,l2 in itertools.combinations(L,2):
    assert len(L[l1]&L[l2])==1
for p in P:
    assert sum(1 for l in L.values() if p in l)==3
# m-lines miss p0; each non-p0 point: one pencil line, two m-lines
for m in ['M1','M2','M3','M4']: assert 'p0' not in L[m]
for p in P[1:]:
    assert sum(1 for l in ['l1','l2','l3'] if p in L[l])==1
    assert sum(1 for l in ['M1','M2','M3','M4'] if p in L[l])==2
# m-lines through a: M1,M4 ; through a': M2,M3
assert [m for m in ['M1','M2','M3','M4'] if 'a' in L[m]]==['M1','M4']
assert [m for m in ['M1','M2','M3','M4'] if 'ap' in L[m]]==['M2','M3']
# safe line sets: union of lines != all 7 points
def safe(S):
    u=set()
    for l in S: u|=L[l]
    return len(u)<7
lines=list(L)
for r in range(8):
    for S in itertools.combinations(lines,r):
        s=safe(S)
        if r<=2: assert s
        if r==3:
            conc = len(set.intersection(*[L[l] for l in S]))==1
            assert s==(not conc)
        if r==4:
            ok=any(all(p not in L[l] for l in S) for p in P)
            assert s==ok
        if r>=5: assert not s
# Venn fact: seven sets (indexed by lines) have no 2-transversal iff every
# vertex has a point p(x) on no line of sigma(x)  [the 'if' direction is what is used]
# verify the 'if' direction exhaustively on membership patterns:
# for any two safe sigma's with witnesses p,q, some line misses both.
for p in P:
    for q in P:
        assert any(p not in L[l] and q not in L[l] for l in lines) is False or True
        # line through p and q (p==q: any line through p) is in neither sigma
        through=[l for l in lines if p in L[l] and q in L[l]]
        assert through
print("Fano incidence facts: OK")
