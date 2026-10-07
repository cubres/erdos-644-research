#!/usr/bin/env python3
"""Referee independent check of K4 criterion (both directions) purely at the level of Venn types.
Rows: 'L' and the six halves ab. Forward: allowed vertex types are
  inside E_i: {L} u S, S subset of halves containing i;  outside: any triangle-free subset of halves.
Tuple is bad iff no two allowed types (same allowed) have union = all 7 rows.
Converse: for every Fano labelling class p and every choice of line L, the maximal types (lines missing p)
translate to allowed K4 types."""
import itertools
H=[frozenset(c) for c in itertools.combinations(range(1,5),2)]
rows=['L']+H
tri=[frozenset(frozenset(e) for e in itertools.combinations(T,2)) for T in itertools.combinations(range(1,5),3)]
def sub(s):
    s=list(s); return [frozenset(c) for r in range(len(s)+1) for c in itertools.combinations(s,r)]
types=[]
for i in range(1,5):
    for S in sub([h for h in H if i in h]): types.append(S|{'L'})
for S in sub(H):
    if not any(T<=S for T in tri): types.append(S)
full=frozenset(rows)
bad=all((a|b)!=full for a in types for b in types)
print("forward: allowed types",len(types),"tuple bad:",bad)
# Converse via explicit Fano plane, all choices of L and labelings of the off-L points
P=range(7); import itertools as it
lines=[frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
ok=True
for L in lines:
    off=[p for p in P if p not in L]
    for perm in it.permutations(range(1,5)):
        lab=dict(zip(off,perm))
        def row(l):
            if l==L: return 'L'
            cd={lab[p] for p in l if p in lab}; return frozenset(set(range(1,5))-cd)
        tset=set(types)
        for p in P:
            T=frozenset(row(l) for l in lines if p not in l)
            # maximal type of a point labelled p must be allowed (downward closed sets)
            if p in lab: ok &= (T in tset and 'L' in T)
            else: ok &= (T in tset and 'L' not in T)
print("converse (all 7 L x 24 labelings):",ok)
