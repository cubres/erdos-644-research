"""Exact 6/7 boundary for the final simultaneous allocation with two triple cells."""
from fractions import Fraction as F
from itertools import combinations,product,combinations_with_replacement
from p644_astra_partial_tree_obstruction import minimal,blocker,solve


def main():
    ants=[]
    for k in range(1,8):
        for a in combinations(range(1,8),k):
            if minimal(a)==a:ants.append(a)
    assert len(ants)==18
    planes={tuple(int(i==j) for i in range(3)) for j in range(3)}
    for a in ants:
        for u,v in combinations(a,2):
            d=tuple(((u>>j)&1)-((v>>j)&1) for j in range(3))
            if next(x for x in d if x)<0:d=tuple(-x for x in d)
            planes.add(d)
    vertices=set()
    for a,b in combinations(sorted(planes),2):
        p=solve([(1,1,1,1),a+(0,),b+(0,)])
        if p is not None and min(p)>=0:vertices.add(p)
    vertices=sorted(vertices);assert len(vertices)==10
    cost=[]
    for a in ants:
        row=[min(sum(p[j] for j in range(3) if m&(1<<j)) for m in a) for p in vertices]
        assert all((12*v).denominator==1 for v in row);cost.append(tuple(int(12*v) for v in row))
    idx={a:i for i,a in enumerate(ants)};blocks=[idx[blocker(a)] for a in ants]
    comp=[{j for j,M in enumerate(ants) if all(a&b for a in L for b in M)} for L in ants]
    raw=0;checked=0;minimum=None
    for p in range(18):
        for q in comp[p]:
            # The two length-three P-to-Q arms have equal endpoint weights9.
            arms=[tuple(9*(cost[x][j]+cost[b][j]) for j in range(10)) for x in comp[q] for b in comp[p]&comp[x]]
            ys=comp[p]&comp[q];raw+=len(ys)*len(arms)**2
            unique=sorted(set(arms))
            sums={tuple(a+b for a,b in zip(u,v)) for u,v in combinations_with_replacement(unique,2)}
            for y in ys:
                fixed=[3*(cost[p][j]+cost[q][j])+6*cost[y][j]+4*cost[blocks[y]][j]+cost[blocks[p]][j]+cost[blocks[q]][j] for j in range(10)]
                for arm_sum in sums:
                    value=max(a+b for a,b in zip(fixed,arm_sum))
                    assert value>=24*12
                    minimum=value if minimum is None else min(minimum,value);checked+=1
    assert raw==6194025 and minimum==24*12
    # Parts P,Q,X',Z',Y,A,B,C,D,W at rank28; masks refer to E,F,G,H.
    masks=(11,14,3,6,5,10,12,9,1,4);weights=(3,3,9,9,6,4,9,9,1,1)
    assert [sum(w for w,m in zip(weights,masks) if m>>j&1) for j in range(4)]==[28]*4
    labels=(7,7,2,4,1,1,2,4,1,1)
    assert all(labels[i]&labels[j] for i in range(10) for j in range(i,10) if masks[i]|masks[j]==15)
    loads=[sum(w for w,m in zip(weights,labels) if m>>j&1) for j in range(3)]
    assert loads==[18,24,24]
    assert weights[4]+weights[2]+weights[3]==24 # Y+X'+Z', avoided by H
    # Strict perturbation: decrease P,Q by e, increase A by2e and D,W by e.
    slopes=(-1,-1,0,0,0,2,0,0,1,1)
    assert [sum(w for w,m in zip(slopes,masks) if m>>j&1) for j in range(4)]==[0]*4
    assert [sum(w for w,m in zip(slopes,labels) if m>>j&1) for j in range(3)]==[2,-2,-2]
    pair_base=[sum(w for w,m in zip(weights,masks) if m>>i&1 and m>>j&1) for i,j in combinations(range(4),2)]
    pair_slope=[sum(w for w,m in zip(slopes,masks) if m>>i&1 and m>>j&1) for i,j in combinations(range(4),2)]
    assert pair_base==[12,6,12,12,10,12] and pair_slope==[-1,0,-1,-1,0,-1]
    assert all(0<=v<=12 for row in cost for v in row)
    # Each old lower dual falls by at most2e: only P,Q have negative slopes.
    # Upper loads are18+2e,24-2e,24-2e, so equality holds for0<=e<=1.
    assert 18+2<=24-2
    print('PASS:',raw,'complete templates;',checked,'distinct arm-sum cases; exact allocation optimum6/7')
    print('PASS: rank28 realization, legal first request, and primal loads18,24,24')
    print('PASS: strict-gap perturbations have exact optimum(24-2e)/28 for0<e<=1, tendingto6/7')
    print('LIMITATION: three fixed final requests for this response; not a bound on f(k,7) or an obstruction to later adaptivity')


if __name__=='__main__':main()
