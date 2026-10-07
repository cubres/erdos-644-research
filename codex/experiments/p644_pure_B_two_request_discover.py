"""Bounded discovery only: two arbitrary requests on four pure-B witness rows.

No minimum positive-cell mass is imposed. Reported numerical optima or
infeasibility are not exact impossibility certificates.
"""
from collections import defaultdict
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix

ap = argparse.ArgumentParser()
ap.add_argument('--scale', type=int, default=1000)
ap.add_argument('--time', type=float, default=60)
ap.add_argument('--old', type=str, default='2356')
args = ap.parse_args()
eps = 1/args.scale
typ = [('1234',37), ('1256',37), ('3456',37), ('135',30+2*eps),
       ('35',2-eps), ('15',2-eps), ('13',2-eps), ('146',32),
       ('16',2), ('14',2), ('236',34), ('36',2), ('245',36)]
retained = tuple(int(r)-1 for r in args.old)
assert len(retained) == 4 and len(set(retained)) == 4
full = 15
cells = defaultdict(float)
for label, w in typ:
    mask = sum(1 << (int(r)-1) for r in label)
    projected = sum(bool(mask & (1 << r)) << j for j, r in enumerate(retained))
    cells[projected] += w
assert full not in cells, 'Retained rows have a common point; outside partners are unbounded.'
cw = [(s,w) for s,w in sorted(cells.items())
      if w and any(s | t == full for t in cells)]
n = len(cw); nq = 4*n; nv = 4*nq+1; B = nv-1
x = lambda i,q: 4*i+q
z = lambda i,q: nq+4*i+q
act = lambda i,q: 2*nq+4*i+q
u = lambda i,q: 3*nq+4*i+q
lb=np.zeros(nv); ub=np.ones(nv); integ=np.zeros(nv)
integ[nq:3*nq]=1
for i,(s,w) in enumerate(cw):
    for q in range(4): ub[x(i,q)]=ub[u(i,q)]=w
ub[B] = sum(w for s,w in cw)
rr=[];cc=[];vv=[];lo=[];hi=[]
def add(co, low=-np.inf, high=np.inf):
    row = len(lo)
    for j,v in co.items(): rr.append(row);cc.append(j);vv.append(v)
    lo.append(low);hi.append(high)
for i,(s,w) in enumerate(cw):
    add({x(i,q):1 for q in range(4)},w,w)
    for q in range(4):
        add({x(i,q):1,z(i,q):-w},high=0)
        add({u(i,q):1,x(i,q):-1,act(i,q):-w},low=-w)
        for j,(t,v) in enumerate(cw):
            if s | t != full: continue
            for r in range(4):
                if q & r == 0:
                    add({act(i,q):1,z(j,r):-1},low=0)
for bit in [1,2]:
    co={x(i,q):1 for i in range(n) for q in range(4) if q & bit}
    co[B]=-1;add(co,high=0)
add({u(i,q):1 for i in range(n) for q in range(4)},high=111-eps)
mat=coo_matrix((vv,(rr,cc)),shape=(len(lo),nv)).tocsr()
obj=np.zeros(nv);obj[B]=1
res=milp(obj,integrality=integ,bounds=Bounds(lb,ub),
         constraints=LinearConstraint(mat,lo,hi),
         options={'time_limit':args.time,'mip_rel_gap':1e-9})
out={'scope':'numerical discovery only', 'scale':args.scale,
     'retained':[r+1 for r in retained], 'requests':2,
     'rank_bound':144+eps,'target':108+.75*eps,
     'endpoint_bound':111-eps,'positive_cell_cutoff':None,
     'status':int(res.status),'message':res.message,
     'cost':float(res.fun) if res.x is not None else None,
     'dual_bound':float(res.mip_dual_bound) if getattr(res,'mip_dual_bound',None) is not None else None}
if res.x is not None:
    out['allocation']=[{'mask':s,'weight':w,
                        'q_masses':[float(res.x[x(i,q)]) for q in range(4)]}
                       for i,(s,w) in enumerate(cw)]
path=Path(__file__).resolve().parent.parent/'outputs'/f'agent_pure_B_two_request_{args.old}_{args.scale}.json'
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
