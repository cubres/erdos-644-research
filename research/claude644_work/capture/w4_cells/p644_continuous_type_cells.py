"""Rigorous outer discretization of arbitrary three-part admissible sets.

A node is an entire closed triangle, not a sampled type. Pair exclusions use
coordinate maxima and therefore hold for every choice of types in the cells.
Positive clauses overapproximate the cells meeting a residual box. UNSAT needs
an independent input and proof check before being reported as a theorem.
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


def expand_fano_regions(labels,nodes,caps):
    from p644_fano_type_assignment import LINES
    unique=sorted(set(labels));mapping={v:i for i,v in enumerate(unique)}
    assignment=[mapping[v] for v in labels];q=len(unique)
    inequalities=[([int(i==j) for i in range(q)],1) for j in range(q)]
    inequalities += [([sum(assignment[j]==i for j in line) for i in range(q)],2) for line in LINES]
    inequalities += [([assignment.count(i) for i in range(q)],4)]
    initial=[[F(v) for v in nodes[j][1]] for j in unique]
    import random
    rng=random.Random(tuple(labels).__repr__());best=None
    for trial in range(12):
        bounds=[row[:] for row in initial]
        for part,cap in enumerate(caps):
            order=list(range(q));rng.shuffle(order)
            for j in order:
                limit=min((mult*cap-sum(coef[k]*bounds[k][part] for k in range(q) if k!=j))/coef[j]
                          for coef,mult in inequalities if coef[j])
                assert limit>=bounds[j][part];bounds[j][part]=limit
        regions=[[i for i,node in enumerate(nodes) if all(v<=b for v,b in zip(node[1],bound))] for bound in bounds]
        size=1
        for region in regions:size*=len(region)
        if best is None or size>best[0]:best=(size,bounds,regions)
    _,bounds,regions=best
    for part,cap in enumerate(caps):
        assert all(sum(v*bounds[j][part] for j,v in enumerate(coef))<=mult*cap for coef,mult in inequalities)
    return {'assignment':assignment,'bounds':[[str(v) for v in row] for row in bounds],'regions':regions}


def cells(rank, caps):
    result=[]
    # [l,l+1]^3 intersect sum(a)=rank is a triangle when sum(l)=rank-1 or rank-2.
    for deficit in (1,2):
        for a in range(min(rank,caps[0])):
            for b in range(min(rank-a,caps[1])):
                c=rank-deficit-a-b
                if 0<=c<caps[2]:
                    lo=(a,b,c);hi=tuple(v+1 for v in lo)
                    if any(7*v>4*x for v,x in zip(hi,caps)):
                        result.append((lo,hi))
    return result


def run(rank,caps,threshold=None,lazy=False,fano=False,regions=False,parents=False):
    T=F(3*rank,4) if threshold is None else F(threshold)
    assert len(caps)==3 and all(v>0 for v in caps) and T.denominator==1
    root=Path('logs/astra_continuous_type_cells');root.mkdir(exist_ok=True)
    key='%d_%s_T%s'%(rank,'_'.join(map(str,caps)),T)+('_lazy' if lazy else '')+('_fano' if fano else '')+('_regions' if regions else '')+('_parents' if parents else '')
    started=time.time();nodes=cells(rank,caps);n=len(nodes)
    lower=np.asarray([a for a,b in nodes],dtype=np.int64).reshape((-1,3))
    upper=np.asarray([b for a,b in nodes],dtype=np.int64).reshape((-1,3))
    menu=json.loads(Path('logs/astra_two_part_gap_central/templates.json').read_text())
    shapes=[[tuple(map(F,v)) for v in item['record']['vertices']] for item in menu.values()]
    target=sum(caps)-int(T);boxes=[];clauses=[]
    for a in range(caps[0]+1):
        for b in range(caps[1]+1):
            c=target-a-b
            if 0<=c<=caps[2]:
                box=(a,b,c);boxes.append(box)
                possible=np.all(lower<=box,axis=1)&(np.minimum(upper,box).sum(axis=1)>=rank)
                clauses.append(list(map(int,np.nonzero(possible)[0]+1)))
    print('START',key,'cells',n,'boxes',len(boxes),flush=True)
    bad=np.zeros((n,n),dtype=bool)
    for shape in shapes:
        fits=np.ones((n,n),dtype=bool)
        for u,v in shape:
            den=u.denominator*v.denominator//gcd(u.denominator,v.denominator)
            ai,bi=int(u*den),int(v*den)
            for i,cap in enumerate(caps):
                fits &= ai*upper[:,i,None]+bi*upper[None,:,i]<=den*cap
        bad |= fits
    bad |= bad.T
    print('MATRIX',int(bad.sum()),'seconds',round(time.time()-started,2),flush=True)
    if not lazy:
        for i in range(n):
            clauses.extend([[-i-1,-int(j)-1] for j in np.nonzero(bad[i,i:])[0]+i])
    rounds=0;learned=set();fano_clauses=[];oracle_status=None;numvars=n;region_variables={}
    if fano:
        from p644_fano_type_assignment import solve as fano_solve
    if parents:
        from p644_parent_type_assignment import solve as parent_solve,expand_regions as parent_expand
    with Glucose3(bootstrap_with=clauses,with_proof=True) as solver:
        while True:
            answer=solver.solve()
            if not answer:break
            selected=[i-1 for i in solver.get_model() if 0<i<=n]
            additions=[(i,j) for i in selected for j in selected if i<=j and bad[i,j]]
            if not additions:
                if not fano:break
                witness=fano_solve([nodes[i][1] for i in selected],caps,seconds=10)
                if witness['status']!='EXACT_POSITIVE' and parents:
                    witness=parent_solve([nodes[i][1] for i in selected],caps,seconds=3)
                oracle_status=witness['status']
                if oracle_status!='EXACT_POSITIVE':break
                labels=[selected[j] for j in witness['labels']]
                record={'labels':labels,'kind':'parents' if 'parents' in witness else 'fano'}
                if 'parents' in witness:record.update(parents=witness['parents'],weights=witness['weights'])
                else:record['costs']=witness['costs']
                if regions:
                    expanded=(parent_expand(witness,nodes,caps,labels) if 'parents' in witness else expand_fano_regions(labels,nodes,caps))
                    if expanded is None:raise RuntimeError('Exact region expansion failed; retain the original positive witness.')
                    record.update(expanded);rvars=[]
                    for region in expanded['regions']:
                        regionkey=tuple(region)
                        if regionkey not in region_variables:
                            numvars+=1;region_variables[regionkey]=numvars
                            for cell in region:
                                implication=[-cell-1,numvars];clauses.append(implication);solver.add_clause(implication)
                        rvars.append(region_variables[regionkey])
                    record['region_variables']=rvars;clause=[-v for v in rvars]
                else:clause=[-i-1 for i in sorted(set(labels))]
                fano_clauses.append(record);clauses.append(clause);solver.add_clause(clause)
                if len(fano_clauses)%10==0:
                    print('FANO',len(fano_clauses),'seconds',round(time.time()-started,2),flush=True)
                if len(fano_clauses)%100==0:
                    (root/(key+'_progress.json')).write_text(json.dumps({'rank':rank,'capacities':caps,'threshold':str(T),
                        'cells':nodes,'boxes':boxes,'fano_clauses':fano_clauses,'elapsed':time.time()-started},indent=2))
                continue
            assert lazy
            for i,j in additions:
                assert (i,j) not in learned;learned.add((i,j))
                clause=[-i-1,-j-1];clauses.append(clause);solver.add_clause(clause)
            rounds+=1
            if rounds%100==0:print('LAZY',rounds,'clauses',len(clauses),'seconds',round(time.time()-started,2),flush=True)
        if not answer:
            proof=solver.get_proof()
            (root/(key+'.drat')).write_text('\n'.join(proof)+'\n')
            with (root/(key+'.cnf')).open('w') as out:
                out.write('p cnf %d %d\n'%(numvars,len(clauses)))
                for clause in clauses:out.write(' '.join(map(str,clause))+' 0\n')
    report={'rank':rank,'capacities':caps,'threshold':str(T),'cells':nodes,'boxes':boxes,
            'sat':answer,'selected':[nodes[i] for i in selected] if answer else [],
            'lazy':lazy,'learned_pairs':sorted(learned),'fano_clauses':fano_clauses,
            'oracle_status':oracle_status,'elapsed':time.time()-started,
            'verification':'INDEPENDENT_INPUT_AND_PROOF_AUDIT_PENDING'}
    (root/(key+'.json')).write_text(json.dumps(report,indent=2))
    print('FINISHED','SAT_RELAXATION' if answer else 'UNSAT_AUDIT_PENDING','rounds',rounds,
          'seconds',round(report['elapsed'],2),flush=True)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('rank',type=int)
    parser.add_argument('capacities',nargs=3,type=int);parser.add_argument('--threshold')
    parser.add_argument('--lazy',action='store_true');parser.add_argument('--fano',action='store_true')
    parser.add_argument('--regions',action='store_true');parser.add_argument('--parents',action='store_true');args=parser.parse_args()
    assert not args.regions or args.fano
    assert not args.parents or args.fano
    run(args.rank,args.capacities,args.threshold,args.lazy,args.fano,args.regions,args.parents)
