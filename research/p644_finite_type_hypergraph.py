"""Finite type-grid search with positive witnesses involving several types.

This is discovery, not a continuous upper-bound certificate. SAT candidates
need the full (7,2) test. Every learned multi-type exclusion carries exact
parent masses or exact Fano inequalities, so it can be audited separately.
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
from p644_fano_type_assignment import solve as fano_solve
from p644_parent_type_assignment import solve as parent_solve


def compositions(total,bounds):
    if len(bounds)==1:
        if 0<=total<=bounds[0]:yield (total,)
        return
    for a in range(max(0,total-sum(bounds[1:])),min(total,bounds[0])+1):
        for rest in compositions(total-a,bounds[1:]):yield (a,)+rest


def run(rank,caps,threshold=None,limit=2000):
    started=time.time();T=F(3*rank,4) if threshold is None else F(threshold)
    assert T.denominator==1;T=int(T);p=len(caps)
    root=Path('logs/astra_finite_type_hypergraph');root.mkdir(exist_ok=True)
    key='%d_%s_T%d'%(rank,'_'.join(map(str,caps)),T)
    types=[t for t in compositions(rank,caps) if any(7*a>4*x for a,x in zip(t,caps))]
    n=len(types);table=np.asarray(types,dtype=np.int64).reshape((-1,p));bad=np.zeros((n,n),dtype=bool)
    menu=json.loads(Path('logs/astra_two_part_gap_central/templates.json').read_text())
    shapes=[[tuple(map(F,v)) for v in item['record']['vertices']] for item in menu.values()]
    for shape in shapes:
        fits=np.ones((n,n),dtype=bool)
        for u,v in shape:
            den=u.denominator*v.denominator//gcd(u.denominator,v.denominator);ai,bi=int(u*den),int(v*den)
            for i,x in enumerate(caps):fits &= ai*table[:,i,None]+bi*table[None,:,i]<=den*x
        bad |= fits
    bad |= bad.T;clauses=[];boxes=list(compositions(sum(caps)-T,caps))
    for box in boxes:
        clauses.append([j+1 for j,t in enumerate(types) if all(a<b if b else a==0 for a,b in zip(t,box))])
    for i in range(n):clauses.extend([[-i-1,-int(j)-1] for j in np.nonzero(bad[i,i:])[0]+i])
    print('START',key,'types',n,'queries',len(boxes),'clauses',len(clauses),flush=True)
    witnesses=[];status='ITERATION_LIMIT';selected=[]
    with Glucose3(bootstrap_with=clauses) as solver:
        for step in range(limit):
            if not solver.solve():status='FINITE_GRID_UNSAT_UNAUDITED';break
            indices=[v-1 for v in solver.get_model() if 0<v<=n];selected=[types[i] for i in indices]
            result=fano_solve(selected,caps,seconds=10)
            if result['status']!='EXACT_POSITIVE':result=parent_solve(selected,caps,seconds=3)
            if result['status']!='EXACT_POSITIVE':status='NEEDS_FULL_BAD_TUPLE_TEST';break
            global_labels=[indices[j] for j in result['labels']];result['global_labels']=global_labels
            witnesses.append(result);clause=[-i-1 for i in sorted(set(global_labels))]
            solver.add_clause(clause);clauses.append(clause)
            if step%20==0:print('EXCLUSIONS',len(witnesses),'selected',len(selected),'seconds',round(time.time()-started,2),flush=True)
    report={'rank':rank,'capacities':caps,'threshold':T,'types':types,'selected':selected,'status':status,
            'witnesses':witnesses,'elapsed':time.time()-started}
    if status=='NEEDS_FULL_BAD_TUPLE_TEST':
        maximum=-1;best=None
        for box in product(*[range(x+1) for x in caps]):
            if sum(box)>maximum and not any(all(a<b if b else a==0 for a,b in zip(t,box)) for t in selected):maximum=sum(box);best=box
        tau=sum(caps)-maximum;assert tau>T
        assert all(not any(all(max(u*a+v*b for u,v in shape)<=x for a,b,x in zip(s,t,caps)) for shape in shapes) for s,t in product(selected,repeat=2))
        report.update(exact_tau=tau,free_box=best)
    (root/(key+'.json')).write_text(json.dumps(report,indent=2));print('FINISHED',status,'seconds',round(time.time()-started,2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('rank',type=int);parser.add_argument('capacities',nargs='+',type=int)
    parser.add_argument('--threshold');parser.add_argument('--limit',type=int,default=2000);args=parser.parse_args()
    run(args.rank,args.capacities,args.threshold,args.limit)
