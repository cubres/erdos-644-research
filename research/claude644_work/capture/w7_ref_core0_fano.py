"""Referee w7 core#0: independent check of Lemma Q logic via an explicit PG(2,2) model.
Fano points = nonzero vectors of F_2^3; lines = nonzero functionals. Pick P; the 4 lines missing P become
rows 0..3 (in some bijection), the 3 lines through P become rows 4..6.  We DERIVE the pair<->point and
matching<->P-line correspondences from the geometry (not assumed), then for every membership pattern T
permitted by the construction we find a Fano point on none of the lines in T (the labelling of cases a-d).
Also check: the permitted set equals downward closure of the 7 point-complement types (static support)."""
import itertools
pts=[v for v in itertools.product((0,1),repeat=3) if any(v)]
lines=[frozenset(p for p in pts if sum(a*b for a,b in zip(l,p))%2==0) for l in pts]
P=pts[0]
miss=[L for L in lines if P not in L]; thru=[L for L in lines if P in L]
assert len(miss)==4 and len(thru)==3
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
# point on miss[i] & miss[j]
pairpt={frozenset((i,j)):next(iter(miss[i]&miss[j])) for i,j in itertools.combinations(range(4),2)}
assert len(set(pairpt.values()))==6
# P-line of each matching: must contain both pair points
mline={}
for mi,M in enumerate(MATCH):
    cand=[L for L in thru if all(pairpt[frozenset(e)] in L for e in M)]
    assert len(cand)==1; mline[mi]=cand[0]
ok=0
for order in itertools.permutations(range(3)):
    rows=miss+[mline[order[0]],mline[order[1]],mline[order[2]]]   # row r -> Fano line
    rowof={}
    for j,mi in enumerate(order):
        for e in MATCH[mi]: rowof[frozenset(e)]=4+j
    allowed=[]
    for T in range(128):
        S=[i for i in range(4) if T>>i&1]
        if any(T>>rowof[frozenset(e)]&1 for e in itertools.combinations(S,2)): continue
        if (T>>4&1) and (T>>5&1) and (T>>6&1): continue
        allowed.append(T)
    for T in allowed:
        safe=[p for p in pts if all(p not in rows[r] for r in range(7) if T>>r&1)]
        assert safe, (order,T)
    # Venn: no two allowed types cover [7]
    assert all((a|b)!=127 for a in allowed for b in allowed)
    # static support = downward closure of point types {r : p not in rows[r]}
    ptypes=[sum(1<<r for r in range(7) if p not in rows[r]) for p in pts]
    down={T for T in range(128) if any(T&~pt==0 for pt in ptypes)}
    assert set(allowed)<=down
    extra=down-set(allowed)
    ok+=1
    print("order",order,"allowed",len(allowed),"downclosure",len(down),"down-but-not-forced",len(extra))
print("PASS",ok,"orders")
