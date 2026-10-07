from fractions import Fraction as Fr
import itertools, random
L=[frozenset(s) for s in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]
# co-line incidence: edge for line l = union of classes p not in l
# given class sizes c_p, a_l = sum_{p not in l} c_p ; check inversion formula
rng=random.Random(1)
for _ in range(2000):
    c=[Fr(rng.randint(0,20)) for _ in range(7)]
    a=[sum(c[p] for p in range(7) if p not in l) for l in L]
    for p in range(7):
        rec=(sum(a[i] for i,l in enumerate(L) if p not in l)-sum(a[i] for i,l in enumerate(L) if p in l))/4
        assert rec==c[p]
    assert sum(a)==4*sum(c)
# pairs of distinct points jointly off exactly 2 lines
for p,q in itertools.combinations(range(7),2):
    assert sum(1 for l in L if p not in l and q not in l)==2
print("mixed-Fano inversion formula verified")
