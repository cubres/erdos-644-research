"""Discover exactly recovered simultaneous requests for a finite candidate graph.

MILP optimality flags are numerical only; an exact witness is an upper bound.
"""
from fractions import Fraction as F
from itertools import product
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix


def discover(parts,edges=4,requests=3,seconds=30):
    parts={int(m):F(v) for m,v in parts.items() if F(v)>0}
    pairs=[(a,b) for a in parts for b in parts if a<=b and a|b==(1<<edges)-1]
    used={p for ab in pairs for p in ab}
    parts={m:v for m,v in parts.items() if m in used}
    masks=list(parts);idx={m:i for i,m in enumerate(masks)};L=1<<requests;n=len(parts)*L;nv=2*n+1
    rows=[];lo=[];hi=[]
    def add(d,l=-np.inf,u=np.inf):rows.append(d);lo.append(l);hi.append(u)
    for m,i in idx.items():
        add({i*L+j:1 for j in range(L)},float(parts[m]),float(parts[m]))
        for j in range(L):add({i*L+j:1,n+i*L+j:-float(parts[m])},u=0)
    for a,b in pairs:
        for s,t in product(range(L),repeat=2):
            if s&t:continue
            ia=n+idx[a]*L+s;ib=n+idx[b]*L+t
            add({ia:1,ib:1} if ia!=ib else {ia:2},u=1)
    for j in range(requests):add({**{i*L+s:1 for i in range(len(parts)) for s in range(L) if s>>j&1},2*n:-1},u=0)
    A=lil_matrix((len(rows),nv))
    for i,row in enumerate(rows):
        for j,v in row.items():A[i,j]=v
    c=np.zeros(nv);c[-1]=1;lb=np.zeros(nv);ub=np.ones(nv);ub[-1]=edges
    q=milp(c,integrality=np.r_[np.zeros(n),np.ones(n),0],bounds=Bounds(lb,ub),constraints=LinearConstraint(A.tocsr(),lo,hi),options={'time_limit':seconds})
    if q.x is None:return {'status':'UNKNOWN','solver_status':q.status}
    alloc={m:{s:F(float(q.x[i*L+s])).limit_denominator(10**7) for s in range(L) if q.x[i*L+s]>1e-10} for m,i in idx.items()}
    if any(any(v<0 for v in a.values()) or sum(a.values())!=parts[m] for m,a in alloc.items()):return {'status':'UNKNOWN','reason':'mass recovery failed','numeric_budget':q.fun}
    assert all(s&t for a,b in pairs for s in alloc[a] for t in alloc[b])
    loads=[sum(v for a in alloc.values() for s,v in a.items() if s>>j&1) for j in range(requests)]
    return {'status':'EXACT_WITNESS','budget':str(max(loads)),'loads':list(map(str,loads)),'numeric_optimal':q.status==0,'parts':{str(m):{str(s):str(v) for s,v in a.items()} for m,a in alloc.items()}}


if __name__=='__main__':
    from pathlib import Path
    import json
    x,y,z=F(411,1000),F(1927,8000),F(201,500);p=q=F(49,500);a=F(9,50);b=F(161,500);c=F(151,500)
    parts={11:p,14:q,3:x-p,6:z-q,5:y,10:a,12:b,9:c,1:1-x-y-c,4:1-y-z-b}
    out=discover(parts,seconds=60);print(out,flush=True)
    Path('logs/astra_two_triples_first_probe.json').write_text(json.dumps(out,indent=2))
