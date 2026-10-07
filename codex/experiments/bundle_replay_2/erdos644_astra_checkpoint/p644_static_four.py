"""Four static avoidance requests after a good triple.

The six Venn parts X=12,Y=13,Z=23,U=1,V=2,W=3 have a candidate-pair
graph consisting of the triangle XYZ and pendant pairs XW,YV,ZU.
Assign each point a subset of four requests avoiding it. Labels
on adjacent parts must intersect. Numerical MILP only discovers labels;
the rational mass and budget checks are exact. No numerical lower bound
on the optimum is claimed.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix

PAIRS=[(0,1),(0,2),(1,2),(0,5),(1,4),(2,3)]


def discover(x,y,z,seconds=60):
    x,y,z=map(F,(x,y,z));weights=[x,y,z,1-x-y,1-x-z,1-y-z]
    if min(weights)<0:return {'status':'INVALID_TRIPLE'}
    n=96;nv=193;rows=[];lo=[];hi=[]
    def add(d,l=-np.inf,u=np.inf):rows.append(d);lo.append(l);hi.append(u)
    for p in range(6):
        add({p*16+i:1 for i in range(16)},float(weights[p]),float(weights[p]))
        for i in range(16):add({p*16+i:1,n+p*16+i:-float(weights[p])},u=0)
    for a,b in PAIRS:
        for s,t in product(range(16),repeat=2):
            if not s&t:add({n+a*16+s:1,n+b*16+t:1},u=1)
    for j in range(4):add({**{p*16+s:1 for p in range(6) for s in range(16) if s>>j&1},192:-1},u=0)
    A=lil_matrix((len(rows),nv))
    for i,row in enumerate(rows):
        for j,v in row.items():A[i,j]=v
    c=np.zeros(nv);c[-1]=1;lb=np.zeros(nv);ub=np.ones(nv);ub[-1]=3
    integ=np.r_[np.zeros(n),np.ones(n),0]
    q=milp(c,integrality=integ,bounds=Bounds(lb,ub),constraints=LinearConstraint(A.tocsr(),lo,hi),options={'time_limit':seconds})
    if q.x is None:return {'status':'UNKNOWN','solver_status':q.status}
    masses=[[F(float(q.x[p*16+s])).limit_denominator(10**6) for s in range(16)] for p in range(6)]
    if any(min(row)<0 or sum(row)!=w for row,w in zip(masses,weights)):return {'status':'UNKNOWN','reason':'exact mass recovery failed'}
    assert all(s&t for a,b in PAIRS for s,t in product(range(16),repeat=2) if masses[a][s]>0 and masses[b][t]>0)
    budgets=[sum(masses[p][s] for p in range(6) for s in range(16) if s>>j&1) for j in range(4)]
    return {'status':'EXACT_WITNESS','triple':list(map(str,(x,y,z))),'budget':str(max(budgets)),
            'request_budgets':list(map(str,budgets)),
            'parts':[{str(s):str(masses[p][s]) for s in range(16) if masses[p][s]} for p in range(6)],
            'numeric_optimal':q.status==0}


if __name__=='__main__':
    out=[];start=time.monotonic()
    for triple in [('1/2','1/4','1/4'),('1/2','1/4','0'),('1/2','1/10','1/10'),
                   ('9/16','1/16','1/16'),('1/2','3/8','1/8'),('7/16','1/4','1/8')]:
        r=discover(*triple,seconds=45);out.append(r)
        print(triple,r['status'],r.get('budget'),round(time.monotonic()-start,1),flush=True)
        Path('logs/astra_static_four.json').write_text(json.dumps(out,indent=1))
