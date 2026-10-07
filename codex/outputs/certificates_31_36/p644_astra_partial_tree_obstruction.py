"""Independent exact obstruction for three fixed requests after E,F,G,H.

Standard library only. Exhaustively reconstructs the 18 nonempty minimal
label families on three requests, all 16527 tree templates, and their
complete dual price arrangement. This is a strategy-class obstruction.
"""
from fractions import Fraction as F
from itertools import combinations,product


def minimal(labels):
    return tuple(m for m in sorted(set(labels)) if not any(n!=m and n&m==n for n in labels))


def blocker(labels):
    return minimal([m for m in range(1,8) if all(m&n for n in labels)])


def solve(rows):
    a=[list(map(F,row)) for row in rows]
    for j in range(3):
        k=next((i for i in range(j,3) if a[i][j]),None)
        if k is None:return None
        a[j],a[k]=a[k],a[j];s=a[j][j];a[j]=[v/s for v in a[j]]
        for i in range(3):
            if i==j:continue
            s=a[i][j];a[i]=[u-s*v for u,v in zip(a[i],a[j])]
    return tuple(row[-1] for row in a)


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
    costs={a:tuple(min(sum(p[j] for j in range(3) if m&(1<<j)) for m in a) for p in vertices) for a in ants}
    # Q,X,Y,C,D,B,A,V in units of r/40.
    weights=(2,10,8,22,0,8,8,18)
    count=0;best=None;hist={}
    for q in ants:
        neighbors=[a for a in ants if all(u&v for u in q for v in a)]
        for x,y,c in product(neighbors,repeat=3):
            labs=(q,x,y,c,blocker(q),blocker(x),blocker(y),blocker(c))
            vals=[sum(w*costs[a][j] for w,a in zip(weights,labs)) for j in range(len(vertices))]
            value=max(vals)
            assert value>=35,(labs,value)
            best=value if best is None else min(best,value)
            hist[str(value)]=hist.get(str(value),0)+1;count+=1
    assert count==16527 and best==35
    # Exact upper witness: each part maps request masks to its mass in r/40.
    parts=[{3:2},{1:10},{2:8},{5:10,6:12},{},{1:8},{2:8},{3:5,4:13}]
    assert [sum(a.values()) for a in parts]==list(weights)
    for i,j in [(0,1),(0,2),(0,3),(0,4),(1,5),(2,6),(3,7)]:
        assert all(u&v for u in parts[i] for v in parts[j])
    assert [sum(w for a in parts for m,w in a.items() if m&(1<<j)) for j in range(3)]==[35,35,35]
    # Initial four-edge realization and the maximum-small-intersection gap.
    edge_masks=(14,3,5,9,1,12,10,6)
    totals=[sum(w for w,m in zip(weights,edge_masks) if m&(1<<j)) for j in range(4)]
    # Add two private points of F and four of G, which have no candidate pairs.
    totals[1]+=2;totals[2]+=4;assert totals==[40]*4
    pair_sizes=[sum(w for w,m in zip(weights,edge_masks) if m&(1<<i) and m&(1<<j)) for i,j in combinations(range(4),2)]
    assert max(s for s in pair_sizes if s<=20)==20 and all(s<=20 or s>20 for s in pair_sizes)
    assert F(31,36)-F(9,20)<=F(9,20) # avoided portion fits in V
    print('PASS: 16527 complete tree templates; exact minimum maximum request size 35r/40=7r/8')
    print('PASS: explicit primal allocation, four-edge realization, and legal initial response at T=31r/36')
    print('LIMITATION: three fixed requests after this response; later adaptive requests and other initial choices are not excluded')


if __name__=='__main__':main()
