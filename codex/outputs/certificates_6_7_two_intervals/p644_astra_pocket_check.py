"""Exact, standard-library-only replay of the pocket interval certificate.

This certifies (7,2) for d=1/4-e, c=7/10+e, 0<e<=1/1000.
Together with p644_astra_certificate_check.py it gives sigma_2=11/20.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path
import json
import sys

FULL=127
EPS=F(1,1000)


def enumerate_maximal():
    triples=[sum(1<<j for j in t) for t in combinations(range(7),3)]
    neighbours=[sum(1<<j for j,b in enumerate(triples) if a!=b and a&b) for a in triples]
    result=set()
    def visit(R,P,X):
        if not P and not X:
            result.add(tuple(sorted(triples[j] for j in range(35) if R>>j&1)));return
        pivot=((P|X)&-(P|X)).bit_length()-1
        todo=P&~neighbours[pivot]
        while todo:
            vbit=todo&-todo;v=vbit.bit_length()-1;todo^=vbit
            visit(R|vbit,P&neighbours[v],X&neighbours[v]);P^=vbit;X|=vbit
    visit(0,(1<<35)-1,0)
    assert len(result)==6127
    for T in result:
        assert all(a&b for a,b in combinations(T,2))
        assert all(any(not a&b for b in T) for a in triples if a not in T)
    return result


def columns(types):
    # In a bad tuple no point can lie in >=5 edges: the omitted two
    # intersect unless they are A1,A2, and no point misses both anchors.
    cols=[]
    for side in (0,1):
        for mask in range(127):
            if bin(mask).count('1')>4:continue
            valid=True
            for j,t in enumerate(types):
                if t=='A1' and bool(mask>>j&1)!=(side==0):valid=False
                if t=='A2' and bool(mask>>j&1)!=(side==1):valid=False
            if valid:cols.append((mask,[side*8]+[side*8+1+j for j in range(7) if mask>>j&1]))
    return cols


def rhs(types,e):
    val={'A1':(F(1),F(0)),'A2':(F(0),F(1)),
         's':(F(1,4)-e,F(3,4)+e),'t':(F(7,10)+e,F(3,10)-e)}
    return [v for side in (0,1) for v in [F(1)]+[val[t][side] for t in types]]


def check(path):
    data=json.loads(Path(path).read_text());assert F(data['epsilon'])==EPS
    expected={tuple(['A1']*a+['A2']*b+['s']*s+['t']*(7-a-b-s))
              for a,b in product((0,1),repeat=2) for s in range(8-a-b)}
    assert len(expected)==28
    cases={tuple(C['types']):C for C in data['cases']};assert set(cases)==expected
    assert len(data['cases'])==28
    maximal=None;total_duals=0;total_nodes=0
    for types,C in cases.items():
        assert C['status']=='EXACT_INTERVAL_CERTIFICATE'
        cols=columns(types);b0=rhs(types,F(0));b1=rhs(types,EPS)
        nodes=C['nodes'];negative={};memo=set();total_nodes+=len(nodes)
        for i,N in enumerate(nodes):
            if 'dual' not in N:continue
            y=list(map(F,N['dual']));assert len(y)==16
            assert sum(a*b for a,b in zip(y,b0))<=0
            assert sum(a*b for a,b in zip(y,b1))<0
            negative[i]=sum(1<<m for m in {m for m,rows in cols if sum(y[j] for j in rows)<0})
            total_duals+=1
        def visit(i,banned):
            if (i,banned) in memo:return
            memo.add((i,banned));N=nodes[i]
            if i in negative:
                assert not negative[i]&~banned;return
            a,b=N['pair'];assert 0<=a<127 and 0<=b<127 and a|b==127
            l,r=N['children'];assert 0<=l<i and 0<=r<i
            visit(l,banned|1<<a);visit(r,banned|1<<b)
        if 'maximal_roots' in C:
            if maximal is None:maximal=enumerate_maximal()
            groups=[[j for j,t in enumerate(types) if t==name] for name in dict.fromkeys(types)]
            maps=[]
            for images in product(*(list(permutations(g)) for g in groups)):
                p=list(range(7))
                for g,im in zip(groups,images):
                    for a,b in zip(g,im):p[a]=b
                maps.append([sum(1<<p[j] for j in range(7) if m>>j&1) for m in range(128)])
            covered=set()
            for R in C['maximal_roots']:
                T=tuple(sorted(R['triples']));assert T in maximal
                for p in maps:covered.add(tuple(sorted(p[m] for m in T)))
                banned=sum(1<<m for m in range(128) if bin(m).count('1')==4 and (FULL^m) not in T)
                visit(R['root'],banned)
            assert covered==maximal
        else:visit(C['root'],0)
    print(f'PASS: all 28 type multisets; {total_nodes} proof nodes; {total_duals} exact interval duals; 6127 maximal triple families covered')
    print('CERTIFIED: F(1/4-e,7/10+e) has (7,2) for every rational 0<e<=1/1000 and every integral scale.')


if __name__=='__main__':
    check(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'logs/astra_pocket_compact_certificate.json')
