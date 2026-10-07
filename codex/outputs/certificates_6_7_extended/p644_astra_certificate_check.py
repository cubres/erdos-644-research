"""Replay the two-type upper-bound certificate using only Python's stdlib.

Usage: python3 p644_astra_certificate_check.py
No LP/MILP solver, numerical tolerance, or inherited verifier is used.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys


def area(P):
    return abs(sum((a[0]*b[1]-a[1]*b[0] for a,b in zip(P,P[1:]+P[:1])),F(0)))/2


def halfplane(a,b):
    return a[1]-b[1],b[0]-a[0],a[0]*b[1]-a[1]*b[0]


def clip(P,L):
    a,b,c=L;out=[]
    for X,Y in zip(P,P[1:]+P[:1]):
        x=a*X[0]+b*X[1]+c;y=a*Y[0]+b*Y[1]+c
        if x>=0:out.append(X)
        if (x<0<y) or (y<0<x):
            t=x/(x-y);out.append((X[0]+t*(Y[0]-X[0]),X[1]+t*(Y[1]-X[1])))
    return list(dict.fromkeys(out))


def subtract(P,Q):
    out=[]
    for X,Y in zip(Q,Q[1:]+Q[:1]):
        L=halfplane(X,Y);outside=clip(P,tuple(-v for v in L))
        if area(outside):out.append(outside)
        P=clip(P,L)
        if not area(P):break
    return out


def check(path):
    data=json.loads(Path(path).read_text());full=frozenset(range(7));polys=[];nv=0
    assert F(data['gap'])==F(1,20)
    for T in data['templates']:
        assert len(T['types'])==7
        P=[];union_support=set()
        for V in T['vertices']:
            d,c=F(V['d']),F(V['c']);P.append((d,c));nv+=1
            targets={'A1':(1,0),'A2':(0,1),'s':(d,1-d),'t':(c,1-c)}
            cells=[(int(s),frozenset(v),F(m)) for s,v,m in V['cells']]
            assert all(s in (1,2) and v and v<full and m>0 for s,v,m in cells)
            union_support.update(v for s,v,m in cells)
            for side in (1,2):
                assert sum(m for s,v,m in cells if s==side)<=1
                for j in range(7):
                    assert sum(m for s,v,m in cells if s==side and j in v)==targets[T['types'][j]][side-1]
        # Supports must be compatible ACROSS different vertices too, since
        # convex interpolation combines them.
        assert all(a|b!=full for a,b in product(union_support,repeat=2))
        assert area(P)>0
        assert all(a*x+b*y+c>=0 for a,b,c in [halfplane(U,V) for U,V in zip(P,P[1:]+P[:1])] for x,y in P)
        polys.append(P)
    remaining=[[(F(1,20),F(1,2)),(F(1,2),F(1,2)),(F(1,2),F(19,20))]]
    for Q in polys:
        remaining=[R for P in remaining for R in subtract(P,Q)]
    assert not remaining, 'Positive-area uncovered region'
    print('PASS: 20-template bound' if len(polys)==20 else 'PASS: template bound',
          f'; {len(polys)} polygons; {nv} exact vertex witnesses; entire closed triangle covered')


if __name__=='__main__':
    check(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'logs/astra_cover_zero_certificate.json')
