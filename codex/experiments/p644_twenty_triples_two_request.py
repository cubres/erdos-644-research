"""Bounded discovery for the symmetric twenty-triple witness.

No positive-cell cutoff. Numerical results are not exact lower certificates.
"""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix

cells = [(s, 2 if bin(s).count('1') == 2 else 1) for s in range(1, 15)]
n = 56
x = lambda i, c: 4*i+c
z = lambda i, c: n+4*i+c
r = lambda i, c: 2*n+4*i+c
B = 3*n
nv = B+1
lb = np.zeros(nv)
ub = np.ones(nv)
integ = np.zeros(nv)
integ[n:2*n] = 1
for i, (s, w) in enumerate(cells):
    for c in range(4):
        ub[x(i,c)] = ub[r(i,c)] = w
ub[B] = 20
rr, cc, vv, lo, hi = [], [], [], [], []
def add(co, low=-np.inf, high=np.inf):
    row = len(lo)
    for j, v in co.items():
        rr.append(row); cc.append(j); vv.append(v)
    lo.append(low); hi.append(high)
for i, (s,w) in enumerate(cells):
    add({x(i,c):1 for c in range(4)},w,w)
    for c in range(4):
        add({x(i,c):1,z(i,c):-w},high=0)
        for j,(t,_) in enumerate(cells):
            if s|t != 15:
                continue
            for d in range(4):
                if c&d == 0:
                    add({r(i,c):1,x(i,c):-1,z(j,d):-w},low=-w)
for bit in (1,2):
    co = {x(i,c):1 for i in range(14) for c in range(4) if c&bit}
    co[B]=-1
    add(co,high=0)
co = {r(i,c):1 for i in range(14) for c in range(4)}
co[B]=-1
add(co,high=0)
# Swap requests to place the first no higher than the second.
add({x(i,1):1 for i in range(14)} | {x(i,2):-1 for i in range(14)},high=0)
matrix = coo_matrix((vv,(rr,cc)),shape=(len(lo),nv)).tocsr()
objective=np.zeros(nv);objective[B]=1
res=milp(objective,integrality=integ,bounds=Bounds(lb,ub),
         constraints=LinearConstraint(matrix,lo,hi),
         options={'time_limit':60,'mip_rel_gap':1e-10})
out={'scope':'numerical discovery, not an exact lower proof',
     'positive_cell_cutoff':None,'target':7.5,'status':int(res.status),
     'message':res.message,'objective':None if res.x is None else float(res.fun),
     'dual_bound':float(res.mip_dual_bound) if getattr(res,'mip_dual_bound',None) is not None else None}
if res.x is not None:
    out['allocation']=[{'mask':s,'weight':w,'codes':[float(res.x[x(i,c)]) for c in range(4)]}
                       for i,(s,w) in enumerate(cells)]
path=Path(__file__).resolve().parent.parent/'outputs'/'agent_twenty_triples_two_request_discovery.json'
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
