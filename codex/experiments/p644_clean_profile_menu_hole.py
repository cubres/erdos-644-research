"""Discovery only: search outside all automorphic two-request regions.

Any returned profile is subsequently checked with exact rational arithmetic.
Failure of this fixed menu is not a hypergraph counterexample.
"""
from itertools import permutations
from pathlib import Path
import json
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix

C=[sum(1<<(int(i)-1) for i in s) for s in ('235','145','136','246')]
bases=[15,51,60]
B=bases+[base^(1<<i) for base in bases for i in range(6)if base>>i&1]
types=C+B
autos=[]
for perm in permutations(range(6)):
    image=lambda s:sum(1<<perm[i]for i in range(6)if s>>i&1)
    if set(map(image,C))==set(C) and set(map(image,bases))==set(bases):autos.append(perm)
assert len(autos)==24
menus=[]
for perm in autos:
    rows=[perm[i]for i in (1,3,4,5)]
    traces=[sum(bool(s>>r&1)<<j for j,r in enumerate(rows))for s in types]
    m=lambda ss:np.array([int(s in ss)for s in traces],dtype=float)
    d1=m((1,2,3,10,12,13,14));d2=m((6,9,11,13))
    r0=m((5,9,10,11,12,14));p=np.array([0]*4+[1]*15)
    m9=m((9,));m12=m((12,))
    # Each inequality is coefficient*x <= rhs.
    ineq=[(d1,.75),(d2,.75),(r0-p-m9-m12,0),
          (r0-p-m9+d2,.75),(r0-p+d1-m12,.75),
          (r0-p+d1+d2,1.5)]
    menus.append((rows,ineq))
n=19;nb=24*6;nv=n+nb+1;delta=nv-1
lb=np.zeros(nv);ub=np.ones(nv);lb[:n]=.001
integ=np.zeros(nv);integ[n:n+nb]=1
rows=[];lo=[];hi=[]
for row in range(6):
    v=np.zeros(nv);v[:n]=[bool(s>>row&1)for s in types]
    rows.append(v);lo.append(-np.inf);hi.append(1)
v=np.zeros(nv);v[4:19]=1
rows.append(v);lo.append(.75);hi.append(np.inf)
M=6
for j,(_,ineq)in enumerate(menus):
    v=np.zeros(nv);v[n+6*j:n+6*(j+1)]=1
    rows.append(v);lo.append(1);hi.append(np.inf)
    for q,(coeff,rhs)in enumerate(ineq):
        v=np.zeros(nv);v[:n]=coeff;v[delta]=-1;v[n+6*j+q]=-M
        rows.append(v);lo.append(rhs-M);hi.append(np.inf)
objective=np.zeros(nv);objective[delta]=-1
res=milp(objective,integrality=integ,bounds=Bounds(lb,ub),
         constraints=LinearConstraint(np.array(rows),lo,hi),
         options={'time_limit':50,'mip_rel_gap':1e-8})
out={'status':int(res.status),'message':res.message,
     'margin':float(res.x[delta])if res.x is not None else None}
if res.x is not None:
    out['weights']={''.join(str(i+1)for i in range(6)if s>>i&1):float(v)
                    for s,v in zip(types,res.x[:n])}
    out['rows']=[sum(res.x[j]for j,s in enumerate(types)if s>>i&1)for i in range(6)]
    out['menu_max_violations']=[float(max(coeff@res.x[:n]-rhs for coeff,rhs in menu))
                               for _,menu in menus]
Path('outputs/agent_clean_profile_menu_hole_discovery.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
