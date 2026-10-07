"""Exact sharp obstruction for the fixed three-request matching stage.

All 5832 antichain templates on three complementary pairs are reconstructed.
The independent dual-price enumeration uses only the standard library.
"""
from fractions import Fraction as F
from itertools import combinations,product
from p644_astra_partial_tree_obstruction import minimal,blocker,solve


def main():
    ants=[]
    for k in range(1,8):
        for L in combinations(range(1,8),k):
            if minimal(L)==L:ants.append(L)
    assert len(ants)==18
    planes={tuple(int(i==j) for i in range(3)) for j in range(3)}
    for L in ants:
        for a,b in combinations(L,2):
            d=tuple(((a>>j)&1)-((b>>j)&1) for j in range(3))
            if next(x for x in d if x)<0:d=tuple(-x for x in d)
            planes.add(d)
    vs=set()
    for a,b in combinations(sorted(planes),2):
        p=solve([(1,1,1,1),a+(0,),b+(0,)])
        if p is not None and min(p)>=0:vs.add(p)
    vs=sorted(vs);assert len(vs)==10
    costs={L:[min(sum(p[j] for j in range(3) if m&(1<<j)) for m in L) for p in vs] for L in ants}
    weights=(20,26,5,5,5,5);best=None;count=0
    for t in product(ants,repeat=3):
        labs=tuple(v for L in t for v in (L,blocker(L)))
        vals=[sum(w*costs[L][j] for w,L in zip(weights,labs)) for j in range(len(vs))]
        value=max(vals);assert value>=33
        best=value if best is None else min(best,value);count+=1
    assert count==5832 and best==33
    parts=[{5:20},{1:13,6:13},{2:5},{2:5},{2:5},{2:5}]
    assert [sum(p.values()) for p in parts]==list(weights)
    for i in (0,2,4):assert all(a&b for a in parts[i] for b in parts[i+1])
    loads=[sum(w for p in parts for m,w in p.items() if m&(1<<j)) for j in range(3)]
    assert loads==[33]*3
    beta=F(11,13);ell=F(7,26);m0=F(5,39)
    assert max((3+ell)/4,(2+2*ell)/3)==beta
    assert m0==(2-beta)/9
    assert F(7,4)-F(9,8)*beta+F(3,8)*m0==beta
    assert 2-F(5,4)*beta-F(3,4)*m0==beta
    assert 1-beta/2+F(3,2)*(1-beta)==F(21,26)<beta
    assert 4*(1-beta)<beta
    print('PASS: 5832 templates; ten exact price vertices; matching weights (20,26,5,5,5,5) have optimum33')
    print('PASS: explicit equality witness and all 11/13 gap-theorem constants')
    print('LIMITATION: fixed post-response requests only; not a lower bound on f(k,7)')


if __name__=='__main__':main()
