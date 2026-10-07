"""Continuous type-response synthesis retaining actual pair compatibility.

At fixed capacities, tau*>T supplies an admissible type strictly below each
positive coordinate of any residual box of deletion cost <=T. Responses
must be pairwise incompatible with every certified bad-tuple construction.
A rational minimum cover of the current finite responses supplies the next
query. A solver contradiction needs independent auditing; limits are UNKNOWN.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json
import sys
import time
sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3


def critical_free_box(types,caps):
    menus=[sorted({F(0),cap}|{t[i] for t in types},reverse=True) for i,cap in enumerate(caps)]
    best=None;total=-1
    for u in product(*menus):
        if sum(u)<=total:continue
        if not any(all(v<w if w else v==0 for v,w in zip(t,u)) for t in types):best=u;total=sum(u)
    assert best is not None
    return best,sum(caps)-total


def run(caps,limit=30,seconds=120,rounded=False,lazy=False):
    root=Path('logs/astra_type_request_cegis');root.mkdir(exist_ok=True)
    key='_'.join(str(v).replace('/','-') for v in caps)+('_rounded' if rounded else '')+('_lazy' if lazy else '');T=F(3,4)
    shapes=[[tuple(map(F,v)) for v in q['record']['vertices']] for q in json.loads(Path('logs/astra_two_part_gap_central/templates.json').read_text()).values()]
    q=lambda v:z3.RealVal(str(v));z3.set_param(proof=True);solver=z3.SolverFor('QF_LRA');solver.set(timeout=int(seconds*1000))
    responses=[];requests=[];steps=[];start=time.time();learned=set();lazy_rounds=0
    def add_request(u):
        assert sum(caps)-sum(u)<=T and all(0<=a<=b for a,b in zip(u,caps))
        index=len(responses);a=z3.Reals(' '.join('a%d_%d'%(index,i) for i in range(len(caps))))
        for v,upper in zip(a,u):solver.add(v>=0,v<q(upper) if upper else v==0)
        solver.add(z3.Sum(*a)==1,z3.Or(*[7*v>q(4*x) for v,x in zip(a,caps)]))
        if not lazy:
            for b in responses:
                for shape in shapes:
                    solver.add(z3.Or(*[q(u)*s+q(v)*t>q(cap) for s,t,cap in zip(a,b,caps) for u,v in shape]))
        responses.append(a);requests.append(u)
    for i in range(len(caps)):
        u=caps[:];u[i]=max(F(0),u[i]-T);add_request(u)
    status='ITERATION_LIMIT'
    for step in range(limit):
        begin=time.time()
        while True:
            answer=solver.check()
            if answer!=z3.sat or not lazy:break
            model=solver.model();types=[[F(str(model.eval(v,model_completion=True))) for v in row] for row in responses]
            additions=[]
            for i,a in enumerate(types):
                for j,b in enumerate(types):
                    if i==j:continue
                    for k,shape in enumerate(shapes):
                        if all(max(u*s+v*t for u,v in shape)<=cap for s,t,cap in zip(a,b,caps)):
                            assert (i,j,k) not in learned;additions.append((i,j,k))
            if not additions:break
            for i,j,k in additions:
                learned.add((i,j,k));solver.add(z3.Or(*[q(u)*s+q(v)*t>q(cap) for s,t,cap in zip(responses[i],responses[j],caps) for u,v in shapes[k]]))
            lazy_rounds+=1
            if lazy_rounds%10==0:print('lazy rounds',lazy_rounds,'constraints',len(learned),'seconds',round(time.time()-start,2),flush=True)
        if answer!=z3.sat:
            status='UNSAT_REQUIRES_INDEPENDENT_AUDIT' if answer==z3.unsat else 'SOLVER_UNKNOWN'
            (root/(key+'.smt2')).write_text(solver.to_smt2())
            if answer==z3.unsat:(root/(key+'.proof')).write_text(solver.proof().sexpr())
            break
        model=solver.model();types=[[F(str(model.eval(v,model_completion=True))) for v in row] for row in responses]
        for a,u in zip(types,requests):
            assert sum(a)==1 and min(a)>=0 and all(v<w if w else v==0 for v,w in zip(a,u))
        for a,b in product(types,repeat=2):
            assert not any(all(max(u*s+v*t for u,v in shape)<=cap for s,t,cap in zip(a,b,caps)) for shape in shapes)
        u,tau=critical_free_box(types,caps)
        record={'types':[list(map(str,t)) for t in types],'critical_free_box':list(map(str,u)),
                'tau':str(tau),'solver_seconds':time.time()-begin};steps.append(record)
        print('step',step,'responses',len(responses),'tau',str(tau),'seconds',round(time.time()-start,2),flush=True)
        if tau>T:status='TWO_TYPE_METHOD_CANDIDATE';break
        if rounded:
            for power in range(2,25):
                mesh=1<<power
                simpler=[F((v*mesh).numerator//(v*mesh).denominator,mesh) for v in u]
                if sum(caps)-sum(simpler)<=T:u=tuple(simpler);break
        assert tuple(u) not in set(map(tuple,requests));add_request(list(u))
        (root/(key+'_progress.json')).write_text(json.dumps({'requests':[list(map(str,u)) for u in requests],'steps':steps},indent=2))
    report={'capacities':list(map(str,caps)),'budget':str(T),'status':status,'requests':[list(map(str,u)) for u in requests],
            'lazy_constraints':sorted(learned),'lazy_rounds':lazy_rounds,
            'steps':steps,'elapsed':time.time()-start,'independent_verification':'PENDING'}
    (root/(key+'.json')).write_text(json.dumps(report,indent=2));print('FINISHED',status,'requests',len(requests),'seconds',round(report['elapsed'],2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('capacities',nargs='+');parser.add_argument('--limit',type=int,default=30);parser.add_argument('--seconds',type=float,default=120)
    parser.add_argument('--rounded',action='store_true')
    parser.add_argument('--lazy',action='store_true')
    args=parser.parse_args();run(list(map(F,args.capacities)),args.limit,args.seconds,args.rounded,args.lazy)
