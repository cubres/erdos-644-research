"""Recursive exact-dual search for the remaining two-fixed-type branch.

Countermodels select a certified capacity template. A true counterexample
must violate one of its facets at an existing or one new coordinate, giving
a complete finite child list. Incomplete trees are explicitly left open.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import time
import numpy as np
from scipy.optimize import linprog
from p644_disjoint_two_types import constraints


def solve(A,b,g):
    objective=[0]*len(A[0]);objective[g]=-1
    result=linprog(objective,A_ub=np.array(A,dtype=float),b_ub=list(map(float,b)),bounds=(0,None),method='highs')
    if result.status==2:
        phase=linprog([0]*len(objective)+[1],A_ub=np.column_stack([np.array(A,dtype=float),-np.ones(len(A))]),b_ub=list(map(float,b)),bounds=(0,None),method='highs')
        assert phase.status==0 and phase.fun>0
        dual=[F(float(v)).limit_denominator(10000000) for v in phase.ineqlin.marginals]
        assert all(v<=0 for v in dual) and sum(v*w for v,w in zip(dual,b))>0
        assert all(sum(dual[i]*A[i][j] for i in range(len(A)))<=0 for j in range(len(objective)))
        return {'status':'infeasible','dual':list(map(str,dual))}
    assert result.status==0
    if result.fun>=-1e-8:
        dual=[F(float(v)).limit_denominator(10000000) for v in result.ineqlin.marginals]
        assert all(v<=0 for v in dual) and sum(v*w for v,w in zip(dual,b))>=0
        assert all(sum(dual[i]*A[i][j] for i in range(len(A)))<=objective[j] for j in range(len(objective)))
        return {'status':'nonpositive','dual':list(map(str,dual))}
    point=[F(float(v)).limit_denominator(10000000) for v in result.x]
    assert point[g]>0 and all(sum(v*w for v,w in zip(row,point))<=rhs for row,rhs in zip(A,b))
    return {'status':'positive','point':list(map(str,point))}


def run(limit=5000):
    root=Path('logs/astra_two_type_recursive');root.mkdir(exist_ok=True)
    base=json.loads(Path('logs/astra_disjoint_two_types_fano.json').read_text())
    menu=json.loads(Path('logs/astra_support_capacity_minimal.json').read_text())['minimal_functions']
    shapes=[[tuple(map(F,q)) for q in item['vertices']] for item in menu]
    nodes=[];started=time.time();counts={'closed':0,'split':0,'open':0,'candidate':0};stopped=False
    def visit(k,l,states,witnesses,depth=0):
        nonlocal stopped
        if len(nodes)>=limit or stopped:counts['open']+=1;return None
        number=len(nodes);p=len(states);A,b,g=constraints(p,k,l,states,True)
        for template,coordinate,facet in witnesses:
            u,v=shapes[template][facet];row=[F(0)]*(3*p+1)
            row[3*coordinate]=-u;row[3*coordinate+1]=-v;row[3*coordinate+2]=1;row[g]=1;A.append(row);b.append(F(0))
        result=solve(A,b,g);record={'id':number,'k':k,'l':l,'states':states,'witnesses':witnesses,**result};nodes.append(record)
        if result['status']!='positive':counts['closed']+=1;return number
        point=list(map(F,result['point']));a=point[:-1:3];bb=point[1:-1:3];x=point[2:-1:3]
        available=[]
        for t,shape in enumerate(shapes):
            slack=min(cap-max(u*s+v*z for u,v in shape) for s,z,cap in zip(a,bb,x))
            if slack>=0:available.append((t,slack))
        if not available:
            record['status']='CANDIDATE_REQUIRES_FULL_AUDIT';counts['candidate']+=1;stopped=True
            record['completed_types']={'a':list(map(str,a+[1-sum(a)])),'b':list(map(str,bb+[1-sum(bb)])),'x':list(map(str,x+[F(4)]))}
            print('CANDIDATE',record,flush=True);return number
        # Prefer a generous witness with few failure facets.
        template=max(available,key=lambda pair:(pair[1]/len(shapes[pair[0]]),-len(shapes[pair[0]])))[0]
        assert all(template!=t for t,_,_ in witnesses)
        record.update(status='split',template=template,children=[]);counts['split']+=1
        for coordinate in range(p+1):
            extensions=[states] if coordinate<p else [states+(q,) for q in ('A','B','ab','ba')]
            for expanded in extensions:
                for facet in range(len(shapes[template])):
                    child=visit(k,l,expanded,witnesses+[(template,coordinate,facet)],depth+1)
                    record['children'].append({'coordinate':coordinate,'state':expanded[-1] if coordinate==p else None,'facet':facet,'child':child})
        if number%10==0:
            (root/'progress.json').write_text(json.dumps({'counts':counts,'nodes':len(nodes),'elapsed':time.time()-started},indent=2))
            print('node',number,'depth',depth,counts,'total',len(nodes),'seconds',round(time.time()-started,2),flush=True)
        return number
    roots=[]
    for case in base['exact_positive_models']:
        roots.append(visit(case['k'],case['l'],tuple(case['states']),[]))
    report={'root_certificate':'astra_disjoint_two_types_fano.json','roots':roots,'nodes':nodes,'counts':counts,'elapsed':time.time()-started}
    report['status']='CLOSED_REQUIRES_INDEPENDENT_AUDIT' if not counts['open'] and not counts['candidate'] else 'OPEN'
    (root/'tree.json').write_text(json.dumps(report,indent=2))
    print('FINISHED',report['status'],counts,'nodes',len(nodes),'seconds',round(report['elapsed'],2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int,default=5000);args=parser.parse_args();run(args.limit)
