"""Bounded numerical arbitrary-code requests after the full-S pivot.

All seven actual rows (the old six and G) are available. No positive-cell
cutoff is imposed. A numerical optimum is not an exact lower certificate.
"""
from collections import defaultdict
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix

ap=argparse.ArgumentParser()
ap.add_argument('--deficits',default='1,1,1,1')
ap.add_argument('--core',default='245G')
ap.add_argument('--requests',type=int,default=2,choices=(1,2,3))
ap.add_argument('--time',type=float,default=60)
ap.add_argument('--residual',type=float,default=110.999)
args=ap.parse_args()
deficits=tuple(float(v)for v in args.deficits.split(','))
assert len(deficits)==4 and sum(deficits)==4 and min(deficits)>=0
mask=lambda label:sum(1<<(int(r)-1)for r in label)
types=[]
for label,d in zip(('235','246','145','136'),deficits):
    if 37-d:types.append((mask(label)|64,37-d))
    if d:types.append((mask(label),d))
for label in ('1234','1256','3456'):
    types.append((mask(label),33))
    for r in label:
        defect=label.replace(r,'')
        types.append((mask(defect)|(64 if defect in('123','124') else 0),1))
assert [sum(w for s,w in types if s&(1<<r))for r in range(7)]==[146]*7
retained=tuple(6 if r=='G'else int(r)-1 for r in args.core)
assert len(retained)==6-args.requests and len(set(retained))==len(retained)
full=(1<<len(retained))-1;nc=1<<args.requests
cells=defaultdict(float)
for support,w in types:
    projected=sum(bool(support&(1<<r))<<j for j,r in enumerate(retained))
    cells[projected]+=w
assert full not in cells,'Core common point requires outside support modelling.'
cw=[(s,w)for s,w in sorted(cells.items())if w and any(s|t==full for t in cells)]
n=len(cw);nq=nc*n;nv=4*nq+1;B=nv-1
x=lambda i,q:nc*i+q
z=lambda i,q:nq+nc*i+q
active=lambda i,q:2*nq+nc*i+q
u=lambda i,q:3*nq+nc*i+q
lb=np.zeros(nv);ub=np.ones(nv);integrality=np.zeros(nv)
integrality[nq:3*nq]=1
for i,(s,w)in enumerate(cw):
    for q in range(nc):ub[x(i,q)]=ub[u(i,q)]=w
ub[B]=sum(w for s,w in cw)
rr=[];cc=[];vv=[];lo=[];hi=[]
def add(co,low=-np.inf,high=np.inf):
    row=len(lo)
    for j,v in co.items():rr.append(row);cc.append(j);vv.append(v)
    lo.append(low);hi.append(high)
for i,(s,w)in enumerate(cw):
    add({x(i,q):1 for q in range(nc)},w,w)
    for q in range(nc):
        add({x(i,q):1,z(i,q):-w},high=0)
        add({u(i,q):1,x(i,q):-1,active(i,q):-w},low=-w)
        for j,(t,v)in enumerate(cw):
            if s|t!=full:continue
            for r in range(nc):
                if q&r==0:add({active(i,q):1,z(j,r):-1},low=0)
for bit in [1<<j for j in range(args.requests)]:
    co={x(i,q):1 for i in range(n)for q in range(nc)if q&bit}
    co[B]=-1;add(co,high=0)
add({u(i,q):1 for i in range(n)for q in range(nc)},high=args.residual)
matrix=coo_matrix((vv,(rr,cc)),shape=(len(lo),nv)).tocsr()
objective=np.zeros(nv);objective[B]=1
res=milp(objective,integrality=integrality,bounds=Bounds(lb,ub),
         constraints=LinearConstraint(matrix,lo,hi),
         options={'time_limit':args.time,'mip_rel_gap':1e-9})
out={'scope':'numerical discovery only','deficits':list(deficits),
     'core':args.core,'requests':args.requests,'endpoint_upper_bound':args.residual,
     'target_budget':109.5,'positive_cell_cutoff':None,
     'status':int(res.status),'message':res.message,
     'best_budget':float(res.fun)if res.x is not None else None,
     'dual_bound':float(res.mip_dual_bound)if getattr(res,'mip_dual_bound',None)is not None else None}
if res.x is not None:
    out['allocation']=[{'mask':s,'mass':w,'q_masses':[float(res.x[x(i,q)])for q in range(nc)]}
                       for i,(s,w)in enumerate(cw)]
slug=args.deficits.replace(',','_')
target=Path(__file__).resolve().parent.parent/'outputs'/f'agent_pivot_arbitrary_{slug}_{args.core}_{args.requests}.json'
target.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
