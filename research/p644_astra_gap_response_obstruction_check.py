"""Exact fixed-request obstruction compatible with three excluded intervals."""
from fractions import Fraction as F
from itertools import combinations,product
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
    costs={a:tuple(min(sum(p[j] for j in range(3) if m&(1<<j)) for m in a) for p in vertices) for a in ants}
    assert all((12*v).denominator==1 for row in costs.values() for v in row)
    costs={a:tuple(int(12*v) for v in row) for a,row in costs.items()}
    # Q,X,Y,C,D,B,A,V, at rank56000.
    weights=(11017,23016,13489,14000,5495,19783,10263,11495)
    threshold=49896 # (891/1000)*56000
    count=0;best=None
    for q in ants:
        neighbors=[a for a in ants if all(u&v for u in q for v in a)]
        for x,y,c in product(neighbors,repeat=3):
            labs=(q,x,y,c,blocker(q),blocker(x),blocker(y),blocker(c))
            bound=max(sum(w*costs[a][j] for w,a in zip(weights,labs)) for j in range(10))
            assert bound>=12*threshold
            best=bound if best is None else min(best,bound);count+=1
    assert count==16527 and best==12*threshold
    parts=[{3:11017},{5:9632,6:13384},{1:13489},{2:14000},{1:5495},{4:19783},{1:10263},{2:11495}]
    assert [sum(a.values()) for a in parts]==list(weights)
    for i,j in [(0,1),(0,2),(0,3),(0,4),(1,5),(2,6),(3,7)]:
        assert all(u&v for u in parts[i] for v in parts[j])
    loads=[sum(w for a in parts for m,w in a.items() if m&(1<<j)) for j in range(3)]
    assert loads==[49896,49896,42799]
    masks=(14,3,5,9,1,12,10,6)
    totals=[sum(w for w,m in zip(weights,masks) if m&(1<<j)) for j in range(4)]
    totals=[a+b for a,b in zip(totals,[0,209,216,937])];assert totals==[56000]*4
    pair_sizes=[sum(w for w,m in zip(weights,masks) if m&(1<<i) and m&(1<<j)) for i,j in combinations(range(4),2)]
    gaps=[(F(191,1000),F(214,1000)),(F(263,1000),F(357,1000)),(F(429,1000),F(476,1000))]
    assert all(not (a<=F(s,56000)<=b) for s in pair_sizes for a,b in gaps)
    # The initial partial-core request consists exactly of X,Y,V.
    assert weights[1]+weights[2]+weights[7]==48000
    assert F(48000,56000)==F(6,7)<F(threshold,56000)==F(891,1000)
    print('PASS: all16527templates and ten rational price vertices; exact fixed-request optimum891/1000')
    print('PASS: explicit primal allocation, rank56000 realization, three current gap exclusions, and legal6/7 first request')
    print('LIMITATION: this response plus three simultaneous requests; other first requests and later adaptivity remain open')


if __name__=='__main__':main()
