"""Exact independent check of a limitation of every two-type argument.

The 42-function completeness theorem is a separately replayable dependency.
Here every one of its functions is excluded on every pair of the nine types.
Transversals are checked by assigning each type a blocking part, independently
of the discovery code's residual-box enumeration. No solver is imported.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json


LINES=((0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5))


def blocking_optimum(types,caps,integer=False):
    best=sum(caps);witness=None
    choices=[[i for i,a in enumerate(t) if a>0] for t in types]
    for allocation in product(*choices):
        residual=list(caps)
        for t,i in zip(types,allocation):residual[i]=min(residual[i],t[i]-(1 if integer else 0))
        cost=sum(caps)-sum(residual)
        if cost<best:best=cost;witness=residual
    return best,witness


def check(root=None):
    root=Path(root) if root else Path(__file__).parent
    data=json.loads((root/'logs/astra_three_part_two_type_barrier.json').read_text())
    templates=json.loads((root/'logs/astra_two_part_gap_central/templates.json').read_text())
    shapes=[[tuple(map(Q,v)) for v in templates[key]['record']['vertices']] for key in sorted(templates,key=int)]
    assert len(shapes)==42
    r=Q(data['rank']);ts=[tuple(map(Q,t)) for t in data['types']];caps=list(map(Q,data['capacities']))
    assert r==80 and len(ts)==9 and caps==[Q(513,8)]*3
    assert all(sum(t)==r and all(0<=a<=x for a,x in zip(t,caps)) for t in ts)
    margin=min(max(u*a+v*b-x for a,b,x in zip(s,t,caps) for u,v in shape)
               for s,t in product(ts,repeat=2) for shape in shapes)
    assert margin==Q(1,8)>0
    tau,free=blocking_optimum(ts,caps)
    assert tau==Q(data['tau'])==Q(483,8)>3*r/4
    assert all(blocking_optimum(ts[:i]+ts[i+1:],caps)[0]<=3*r/4 for i in range(len(ts)))
    its=[tuple(t) for t in data['integer_types']];icaps=data['integer_capacities']
    assert its==[tuple(8*v for v in t) for t in ts] and icaps==[513]*3
    itau,ifree=blocking_optimum(its,icaps,True)
    assert itau==data['integer_tau']==486
    cells=data['integer_bad_cells'];assert len(cells)==22
    assert all(0<c['mask']<127 and all(isinstance(v,int) and v>=0 for v in c['masses']) for c in cells)
    assert all(a['mask']|b['mask']!=127 for a,b in product(cells,repeat=2))
    loads=[tuple(sum(c['masses'][i] for c in cells if c['mask']>>j&1) for i in range(3)) for j in range(7)]
    assert all(t in its for t in loads)
    assert [its.index(t) for t in loads]==data['integer_bad_row_types']
    assert all(sum(c['masses'][i] for c in cells)<=icaps[i] for i in range(3))
    # A second positive witness uses the hand-proved Fano capacity formula.
    fano=json.loads((root/'logs/astra_three_part_two_type_barrier.json.fano.json').read_text())
    labels=fano['labels'];assert len(labels)==7 and all(0<=j<9 for j in labels)
    costs=[max(max(ts[a][i] for a in labels),
               max(sum(ts[labels[j]][i] for j in line)/2 for line in LINES),
               sum(ts[a][i] for a in labels)/4) for i in range(3)]
    assert costs==list(map(Q,fano['costs'])) and all(v<=x for v,x in zip(costs,caps))
    print('PASS: 3402 exact pair exclusions with margin 1/8; continuous tau=483/8 at rank 80; finite tau=486 at rank 640; explicit bad seven-tuple and independent Fano-capacity witness. Completeness dependency: Theorem 7.69.')


if __name__=='__main__':check()
