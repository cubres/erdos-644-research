"""Discovery: can many two-part types evade every two-type bad tuple?

The exact 42-function list determines the forbidden-pair graph. A SAT path
across the type line, with short gaps and adequate endpoint cover costs,
would yield a high-transversal family requiring three or more distinct
types in every bad tuple. Finite-grid UNSAT is not a continuous theorem.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import time
import numpy as np
from pysat.solvers import Glucose3


def search(x,y,mesh,menu):
    threshold=F(3,4);delta=x+y-1-threshold
    if delta<=0:return None
    values=[F(j,mesh) for j in range(mesh+1) if F(j,mesh)<=x and 1-F(j,mesh)<=y]
    # Homogeneous Fano tuples rule out the closed central interval.
    values=[q for q in values if 7*q>4*x or 7*(1-q)>4*y]
    if not values:return None
    v=np.array(list(map(float,values)));a=v[:,None];b=v[None,:]
    bad=np.zeros((len(v),len(v)),dtype=bool)
    for shape in menu:
        fits=np.ones_like(bad)
        for u,w in shape:
            fits &= float(u)*a+float(w)*b<=float(x)+1e-11
            fits &= float(u)*(1-a)+float(w)*(1-b)<=float(y)+1e-11
        bad |= fits
    bad |= bad.T
    clauses=[]
    start=[i+1 for i,q in enumerate(values) if q==0 or x-q>threshold]
    if not start:return None
    clauses.append(start)
    for i,q in enumerate(values):
        if q!=1 and y-1+q<=threshold:
            clauses.append([-i-1]+[j+1 for j,t in enumerate(values) if q<t<q+delta])
        for j in range(i,len(values)):
            if bad[i,j]:clauses.append([-i-1,-j-1])
    with Glucose3(bootstrap_with=clauses) as solver:
        if not solver.solve():return None
        chosen={i-1 for i in solver.get_model() if i>0}
    selected=sorted(values[i] for i in chosen)
    # All claims for a discovered positive model are recomputed rationally.
    for s in selected:
        for t in selected:
            assert not any(all(u*s+w*t<=x and u*(1-s)+w*(1-t)<=y for u,w in shape) for shape in menu)
    costs=[x+y-1]
    if selected[0]>0:costs.append(x-selected[0])
    if selected[-1]<1:costs.append(y-1+selected[-1])
    costs += [x+y-1-(t-s) for s,t in zip(selected,selected[1:])]
    assert min(costs)>threshold
    return {'capacities':list(map(str,[x,y])),'types':list(map(str,selected)),
            'tau':str(min(costs)),'exact_pair_checks':True,
            'status':'METHOD_OBSTRUCTION_NOT_COUNTEREXAMPLE_TO_ERDOS_644'}


def run(mesh=100,capmesh=20):
    raw=json.loads(Path('logs/astra_support_capacity_minimal.json').read_text())['minimal_functions']
    menu=[[tuple(map(F,v)) for v in row['vertices']] for row in raw]
    tested=0;found=[];started=time.time()
    for i in range(1,(7*capmesh)//4):
        for j in range(i,(7*capmesh)//4):
            x,y=F(i,capmesh),F(j,capmesh)
            if x+y<=F(7,4):continue
            tested+=1;result=search(x,y,mesh,menu)
            if result:
                found.append(result);print('FOUND',result,flush=True)
                break
        if found:break
        if i%5==0:print('tested',tested,'seconds',round(time.time()-started,2),flush=True)
    report={'mesh':mesh,'capacity_mesh':capmesh,'tested':tested,'found':found,
            'elapsed':time.time()-started,'negative_status':'FINITE_GRIDS_ONLY_NO_CONTINUOUS_CONCLUSION'}
    Path('logs/astra_two_part_type_graph_%d_%d.json'%(mesh,capmesh)).write_text(json.dumps(report,indent=2))
    print('FINISHED',tested,'found',len(found),'seconds',round(report['elapsed'],2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--mesh',type=int,default=100);parser.add_argument('--capmesh',type=int,default=20)
    args=parser.parse_args();run(args.mesh,args.capmesh)
