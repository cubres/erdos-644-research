"""Exact-dual discovery for the nonintersecting two-fixed-type branch.

Assume a+b<=x, high transversal coefficient, and failure of homogeneous
Fano and six-versus-one disjoint constructions. At most four witness
coordinates are needed. A SAT model is a method gap, not a counterexample.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog


def cases():
    for p in (2,3,4):
        for k,l in product(range(p),repeat=2):
            if {0,1,k,l}!=set(range(p)):continue
            for states in product(('A','B','ab','ba'),repeat=p):
                if states[0] not in ('A','ab') or states[1] not in ('B','ba'):continue
                if states[k]=='B' or states[l]=='A':continue
                yield p,k,l,states


def constraints(p,k,l,states,fano=False):
    n=3*p+1;g=n-1;A=[];b=[]
    ai=lambda i:3*i;bi=lambda i:3*i+1;xi=lambda i:3*i+2
    def row(d,rhs):
        v=[F(0)]*n
        for j,q in d.items():v[j]+=F(q)
        A.append(v);b.append(F(rhs))
    row({ai(i):1 for i in range(p)},1);row({bi(i):1 for i in range(p)},1);row({g:1},1)
    for i,state in enumerate(states):
        row({ai(i):1,bi(i):1,xi(i):-1},0)
        if state=='A':row({bi(i):1},0);row({g:1,ai(i):-1},0)
        elif state=='B':row({ai(i):1},0);row({g:1,bi(i):-1},0)
        else:
            row({g:1,ai(i):-1},0);row({g:1,bi(i):-1},0)
            larger,smaller=(ai(i),bi(i)) if state=='ab' else (bi(i),ai(i))
            row({smaller:1,larger:-1},0)
            row({xi(i):-1,smaller:1,g:1},-F(3,4))
    for i in range(p):
        for j in range(p):
            if i!=j and states[i]!='B' and states[j]!='A':
                row({xi(i):-1,ai(i):1,xi(j):-1,bi(j):1,g:1},-F(3,4))
    if fano:
        row({xi(0):1,ai(0):-F(3,2),bi(0):-F(1,4),g:1},0)
        row({xi(1):1,ai(1):-F(1,4),bi(1):-F(3,2),g:1},0)
    else:
        row({xi(0):1,ai(0):-F(7,4),g:1},0)
        row({xi(1):1,bi(1):-F(7,4),g:1},0)
    row({xi(k):1,ai(k):-F(6,5),bi(k):-1,g:1},0)
    row({xi(l):1,ai(l):-1,bi(l):-F(6,5),g:1},0)
    return A,b,g


def run(fano=False):
    out=[];models=[]
    for p,k,l,states in cases():
        A,b,g=constraints(p,k,l,states,fano);objective=[0]*len(A[0]);objective[g]=-1
        res=linprog(objective,A_ub=np.array(A,dtype=float),b_ub=list(map(float,b)),bounds=(0,None),method='highs')
        key={'parts':p,'k':k,'l':l,'states':states}
        if res.status==2:
            phase=linprog([0]*len(objective)+[1],A_ub=np.column_stack([np.array(A,dtype=float),-np.ones(len(A))]),b_ub=list(map(float,b)),bounds=(0,None),method='highs')
            assert phase.status==0 and phase.fun>0
            dual=[F(float(v)).limit_denominator(1000000) for v in phase.ineqlin.marginals]
            assert all(v<=0 for v in dual) and sum(v*w for v,w in zip(dual,b))>0
            assert all(sum(dual[i]*A[i][j] for i in range(len(A)))<=0 for j in range(len(objective)))
            key.update(dual=list(map(str,dual)),kind='infeasible');out.append(key);continue
        assert res.status==0
        if res.fun < -1e-8:
            point=[F(float(v)).limit_denominator(1000000) for v in res.x]
            assert point[g]>0 and all(sum(v*w for v,w in zip(row,point))<=rhs for row,rhs in zip(A,b))
            key['point']=list(map(str,point));models.append(key)
        else:
            dual=[F(float(v)).limit_denominator(1000000) for v in res.ineqlin.marginals]
            assert all(v<=0 for v in dual)
            assert sum(v*w for v,w in zip(dual,b))>=0
            assert all(sum(dual[i]*A[i][j] for i in range(len(A)))<=objective[j] for j in range(len(objective)))
            key.update(dual=list(map(str,dual)),kind='nonpositive');out.append(key)
    report={'fano_failure':fano,'exact_nonpositive_cases':out,'exact_positive_models':models}
    Path('logs/astra_disjoint_two_types%s.json'%('_fano' if fano else '')).write_text(json.dumps(report,indent=2))
    print('Cases',len(out)+len(models),'nonpositive',len(out),'positive',len(models),flush=True)
    if models:print('First method gap:',models[0],flush=True)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--fano',action='store_true');args=parser.parse_args();run(args.fano)
