"""Finite exact graph search for high-transversal three-part type sets.

Every selected pair must evade all 42 certified bad-tuple constructions.
Critical residual boxes impose the exact continuous transversal threshold
on the integer type grid. A SAT model is a limitation of two-type methods,
not a counterexample to (7,2); a general seven-type check must follow.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd
from pathlib import Path
import argparse
import json
import time
import numpy as np
from pysat.solvers import Glucose3


def run(rank,caps,threshold=None):
    assert rank%4==0 and len(caps)==3
    custom=threshold is not None
    threshold=3*rank//4 if threshold is None else threshold;started=time.time();root=Path('logs/astra_three_part_type_graph');root.mkdir(exist_ok=True)
    key='%d_%s'%(rank,'_'.join(map(str,caps)))+('_T%d'%threshold if custom else '')
    types=[(a,b,rank-a-b) for a in range(min(rank,caps[0])+1) for b in range(min(rank-a,caps[1])+1)
           if 0<=rank-a-b<=caps[2]]
    types=[a for a in types if any(7*q>4*x for q,x in zip(a,caps))]
    menu=json.loads(Path('logs/astra_two_part_gap_central/templates.json').read_text())
    table=np.asarray(types,dtype=np.int64).reshape((-1,3));n=len(types);bad=np.zeros((n,n),dtype=bool)
    shapes=[]
    for item in menu.values():
        shape=[tuple(map(F,q)) for q in item['record']['vertices']];shapes.append(shape)
        fits=np.ones((n,n),dtype=bool)
        for u,v in shape:
            den=u.denominator*v.denominator//gcd(u.denominator,v.denominator);a,b=int(u*den),int(v*den)
            for i,cap in enumerate(caps):fits &= a*table[:,i,None]+b*table[None,:,i]<=den*cap
        bad |= fits
    bad |= bad.T
    clauses=[];target=sum(caps)-threshold;boxes=[]
    for a in range(caps[0]+1):
        for b in range(caps[1]+1):
            c=target-a-b
            if 0<=c<=caps[2]:boxes.append((a,b,c))
    for box in boxes:
        clauses.append([i+1 for i,t in enumerate(types) if all(v<u if u else v==0 for v,u in zip(t,box))])
    for i in range(n):
        for j in range(i,n):
            if bad[i,j]:clauses.append([-i-1,-j-1])
    print('START',key,'types',n,'residual boxes',len(boxes),'clauses',len(clauses),flush=True)
    with Glucose3(bootstrap_with=clauses) as solver:
        answer=solver.solve();selected=[types[i-1] for i in solver.get_model() if i>0] if answer else []
    report={'rank':rank,'capacities':caps,'threshold':threshold,'types_considered':n,'critical_boxes':len(boxes),'sat':answer,
            'selected':selected,'elapsed':time.time()-started,'scope':'FINITE_TYPE_GRID_ONLY'}
    if answer:
        for a,b in product(selected,repeat=2):
            assert not any(all(max(u*s+v*t for u,v in shape)<=cap for s,t,cap in zip(a,b,caps)) for shape in shapes)
        maximum=0
        for box in product(*[range(cap+1) for cap in caps]):
            if not any(all(v<u if u else v==0 for v,u in zip(t,box)) for t in selected):maximum=max(maximum,sum(box))
        tau=sum(caps)-maximum;assert tau>threshold
        report.update(exact_tau=tau,exact_tau_ratio=str(F(tau,rank)),exact_pair_checks=True,
                      status='NEEDS_MULTI_TYPE_BAD_TUPLE_CHECK_NOT_ERDOS_COUNTEREXAMPLE')
    (root/(key+'.json')).write_text(json.dumps(report,indent=2));print('FINISHED',report,flush=True)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('rank',type=int);parser.add_argument('capacities',nargs=3,type=int)
    parser.add_argument('--threshold',type=int)
    args=parser.parse_args();run(args.rank,args.capacities,args.threshold)
