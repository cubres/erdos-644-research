"""Standard-library-only exact replay of the intersecting two-type theorem.

The mathematical reduction and the two constructive Fano-downset templates
are stated in note_644.md. This checks every one of the 87 resulting LP cases.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def constraints(i,j,facet,states):
    n=len(states);N=3*n+1;g=N-1;A=[];b=[]
    def row(d,rhs):
        v=[F(0)]*N
        for k,w in d.items():v[k]+=F(w)
        A.append(v);b.append(F(rhs))
    a=lambda k:3*k;t=lambda k:3*k+1;x=lambda k:3*k+2
    row({a(k):1 for k in range(n)},1);row({t(k):1 for k in range(n)},1);row({g:1},1)
    for k,s in enumerate(states):
        row({a(k):1,x(k):-1},0);row({t(k):1,x(k):-1},0);row({x(k):1},2)
        if s=='A':row({t(k):1},0);row({g:1,a(k):-1},0)
        elif s=='B':row({a(k):1},0);row({g:1,t(k):-1},0)
        else:
            row({g:1,a(k):-1},0);row({g:1,t(k):-1},0)
            if s=='ab':row({t(k):1,a(k):-1},0);m=t(k)
            else:row({a(k):1,t(k):-1},0);m=a(k)
            row({m:1,x(k):-1,g:1},-F(3,4))
    for k in range(n):
        for l in range(n):
            if k!=l and states[k]!='B' and states[l]!='A':
                row({x(k):-1,a(k):1,x(l):-1,t(l):1,g:1},-F(3,4))
    row({x(0):1,a(0):-1,t(0):-1,g:1},0)
    row({x(i):1,a(i):-F(1,4),t(i):-F(3,2),g:1},0)
    row({x(j):1,a(j):-facet[0],t(j):-facet[1],g:1},0)
    return A,b,g


def main():
    data=json.loads((Path(__file__).parent/'logs/astra_two_type_dichotomy.json').read_text())
    expected={(i,j,facet,('ab',)+states)
              for i,j in [(0,0),(0,1),(1,0),(1,1),(1,2)]
              for facet in [(F(3,2),F(0)),(F(5,4),F(1,2)),(F(1,2),F(1))]
              for states in product(['A','B','ab','ba'],repeat=max(i,j))}
    found=set();nzero=0;nempty=0
    for C in data:
        key=(C['i'],C['j'],tuple(map(F,C['facet'])),tuple(C['states']))
        assert key in expected and key not in found;found.add(key)
        A,b,g=constraints(*key);y=list(map(F,C['dual']))
        assert len(A)==len(y) and all(v<=0 for v in y)
        dual_value=sum(v*w for v,w in zip(y,b))
        reduced=[sum(y[l]*A[l][k] for l in range(len(A))) for k in range(len(A[0]))]
        if C['status']=='EXACT_ZERO_DUAL':
            assert dual_value>=0 and all(v<=(-1 if k==g else 0) for k,v in enumerate(reduced));nzero+=1
        else:
            assert C['status']=='EXACT_INFEASIBLE_DUAL'
            assert dual_value>0 and all(v<=0 for v in reduced);nempty+=1
    assert found==expected and len(found)==87
    print(f'PASS: all 87 coordinate/support/order cases; {nzero} exact nonpositive-margin duals; {nempty} exact infeasibility duals')


if __name__=='__main__':main()
