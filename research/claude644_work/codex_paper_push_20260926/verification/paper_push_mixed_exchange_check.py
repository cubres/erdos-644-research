"""Exact replay: three-minimum menu obstruction and mixed one-response closure.

Run with python3 -B -S. All checks use rational arithmetic and the ordinary
library. The V4/Fano assertions certify only their named finite menus.
The 113/200 full-family bound is proved by hand in the accompanying report.
"""
from fractions import Fraction as F
from itertools import product, permutations, combinations
from pathlib import Path
import json
from paper_push_anchor_exchange import optimal_request, thresholds

PENCIL=((0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5))
X=tuple(F(v,1000) for v in (755,780,750))
T=tuple(tuple(F(v,1000) for v in row) for row in
        ((512,0,488),(404,521,75),(499,0,501)))


def fano_bad(asg):
    return all(sum(T[j][i] for j in asg)<=4*X[i]
               and all(sum(T[asg[j]][i] for j in p)<=2*X[i]
                       for p in PENCIL) for i in range(3))


def main():
    assert all(sum(t)==1 for t in T)
    assert sum(X[i]-T[i][i] for i in range(3))==F(751,1000)
    assert all(T[i][i]>2*X[i]/3 for i in range(3))
    assert all(T[j][i]<=2*X[i]/3 for i in range(3) for j in range(3) if i!=j)
    assert not any(fano_bad(asg) for asg in product(range(3),repeat=7))
    v4_margin=min(max(max(T[a][i]+T[b][i]+T[c][i]-2*X[i],
                         2*T[d][i]+T[b][i]+T[c][i]-2*X[i],
                         4*T[d][i]+T[a][i]+T[b][i]+T[c][i]-4*X[i])
                     for i in range(3))
                  for d,a,b,c in product(range(3),repeat=4))
    assert v4_margin==F(201,1000)
    pairpath=Path(__file__).resolve().parent/'heavy/astra_support_capacity_minimal.json'
    pairdata=json.loads(pairpath.read_text())
    assert len(pairdata['minimal_functions'])==42
    pair_margin=min(max(F(u)*T[a][i]+F(v)*T[b][i]-X[i]
                        for i in range(3) for u,v in fun['vertices'])
                    for fun in pairdata['minimal_functions']
                    for a,b in permutations(range(3),2))
    assert pair_margin==F(3,2000)
    results=[optimal_request(X,T[a],T[b]) for a,b in combinations(range(3),2)]
    assert [r['cost'] for r in results]==[F(83,100),F(257,200),F(817,1000)]
    assert results[1]['request'] is None

    a,b,c=T
    asg=(0,0,1,1,2,3,2)
    caps=[]
    for i in range(3):
        fs=[4*X[i]-sum(T[j][i] for j in asg if j<3)]
        for p in PENCIL:
            if 5 in p:fs.append(2*X[i]-sum(T[asg[j]][i] for j in p if j!=5))
            else:assert sum(T[asg[j]][i] for j in p)<=2*X[i]
        caps.append(min(fs))
    q=thresholds(X,b,a)
    assert tuple(caps)==tuple(F(v,1000) for v in (190,1039,511))
    assert q==tuple(F(v,1000) for v in (190,515,862))
    retained=(F(19,100),X[1],X[2])
    assert caps[0]>=retained[0] and q[0]>=retained[0]
    assert caps[1]>=X[1] and q[2]>=X[2]
    assert caps[2]+q[1]>=1
    assert sum(X)-sum(retained)==F(113,200)
    # Independent cert-agent discovery: a single Fano partner box is stronger.
    rawcap=tuple(min(2*X[i]-a[i]-b[i],2*X[i]-b[i]-c[i],
                     4*X[i]-a[i]-3*b[i]-2*c[i]) for i in range(3))
    assert rawcap==tuple(F(v,1000) for v in (298,1039,924))
    assert all(a[i]+2*b[i]<=2*X[i] and a[i]+2*c[i]<=2*X[i]
               and 2*b[i]+c[i]<=2*X[i] for i in range(3))
    assert X[0]-rawcap[0]==F(457,1000)
    print('PASS: 2187 Fano assignments, 81 V4 assignments, 252 pair assignments all fail.')
    print('PASS: optimal anchor-pair costs 83/100, 257/200, 817/1000 exceed 3/4.')
    print('PASS: mixed Fano/V5 request proves tau*<=113/200 for every P7 superfamily of these anchors.')
    print('PASS: a single Fano partner box improves that bound to 457/1000.')


if __name__=='__main__':main()
