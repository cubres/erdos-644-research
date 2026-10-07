"""Discovery of covers for types surviving the partner-budget necessary test.

For each actual type b, every certified two-type construction defines an
upper box of possible partners. If deleting down to that box costs <=3/4,
high transversal number forces a partner and a bad tuple. Thus b cannot
occur. Search for one deletion covering all types not excluded in this way.
Fixed-capacity UNSAT outputs need mathematical-input and proof auditing.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import sys
import time
sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3


def system(capacities):
    menu=json.loads(Path('logs/astra_support_capacity_minimal.json').read_text())['minimal_functions']
    p=len(capacities);b=z3.Reals(' '.join('b%d'%i for i in range(p)));s=z3.SolverFor('QF_LRA');s.set(timeout=10000)
    q=lambda v:z3.RealVal(str(v));T=q(F(3,4));minimum=lambda a,c:z3.If(a<=c,a,c)
    for v,x in zip(b,capacities):s.add(v>=0,v<=q(min(x,F(1))))
    s.add(z3.Sum(*b)==1,z3.Or(*[7*v>q(4*x) for v,x in zip(b,capacities)]))
    for item in menu:
        shape=[tuple(map(F,v)) for v in item['vertices']];exceptions=[];residual=[]
        for v,x in zip(b,capacities):
            upper=q(x)
            for u,w in shape:
                if u:upper=minimum(upper,(q(x)-q(w)*v)/q(u))
                else:exceptions.append(q(w)*v>q(x))
            exceptions.append(upper<0);residual.append(upper)
        exceptions.append(q(sum(capacities))-z3.Sum(*residual)>T)
        s.add(z3.Or(*exceptions))
    return s,b


def probe(capacities,mesh=40,limit=3000):
    assert len(capacities)==3
    root=Path('logs/astra_partner_budget_probe');root.mkdir(exist_ok=True)
    key='_'.join(str(v).replace('/','-') for v in capacities);solver,b=system(capacities);started=time.time()
    candidates=[]
    for i in range(3*mesh//4+1):
        for j in range(3*mesh//4-i+1):
            d=[F(i,mesh),F(j,mesh),F(3,4)-F(i+j,mesh)]
            if all(v<=x for v,x in zip(d,capacities)):candidates.append(d)
    # Try balanced and single-part deletions first.
    candidates.sort(key=lambda d:(min(d)>0,max(d)-min(d)))
    counts={'sat':0,'unknown':0};winner=None
    for number,d in enumerate(candidates[:limit]):
        solver.push()
        for v,x,cut in zip(b,capacities,d):solver.add(v<=str(x-cut))
        answer=solver.check()
        if answer==z3.unsat:
            winner=list(map(str,d));(root/(key+'.smt2')).write_text(solver.to_smt2());solver.pop();break
        counts['sat' if answer==z3.sat else 'unknown']+=1;solver.pop()
    report={'capacities':list(map(str,capacities)),'mesh':mesh,'counts':counts,'winner':winner,
            'total_candidates':len(candidates),'elapsed':time.time()-started,'independent_verification':'PENDING'}
    (root/(key+'.json')).write_text(json.dumps(report,indent=2));print(report,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('capacities',nargs=3);parser.add_argument('--mesh',type=int,default=40)
    args=parser.parse_args();probe(list(map(F,args.capacities)),args.mesh)
