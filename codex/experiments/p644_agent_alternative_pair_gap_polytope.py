"""Finite polytope discovery for all containment requests on one old pair.

For each allowed pair-overlap mode, enumerate the vertices of its response
polytope, take the convex hull of the coordinate boxes below those vertices,
and obtain the exact downward projection in request space. A MILP searches
for a request outside every projection, minimizing its total size.

The geometric construction is exact as a mathematical reduction. This
implementation uses floating ConvexHull/MILP and is discovery, not an exact
rational certificate. No claim about a whole hypergraph follows from one
old pair's response projection.
"""
from itertools import combinations, product
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import milp, Bounds, LinearConstraint
import json

ROWS=np.array([[0,0,1,1],[0,1,0,1]],float)
DIAG=np.array([1,0,0,1],float)


def response_vertices(a,M,modes,T=.75):
    w=np.array([a,1-a,1-a,a])
    bands=[(0,M),(T-M,1-T+M),(1-M,1)]
    lo=np.array([bands[j][0] for j in modes])
    hi=np.array([bands[j][1] for j in modes])
    A=np.r_[np.eye(4),-np.eye(4),ROWS,-ROWS,[DIAG],[-DIAG]]
    b=np.r_[w,np.zeros(4),hi,-lo,a+M,M-a]
    # eliminate g3 using sum(g)=1
    A3=A[:,:3]-A[:,3,None];b3=b-A[:,3]
    seen={}
    for active in combinations(range(len(b)),3):
        mat=A3[list(active)]
        if abs(np.linalg.det(mat))<1e-9:continue
        q=np.linalg.solve(mat,b3[list(active)])
        if np.max(A3@q-b3)>1e-8:continue
        g=np.r_[q,1-sum(q)];g=np.clip(g,0,w)
        seen[tuple(np.round(g,10))]=g
    return list(seen.values())


def down_facets(vs):
    if not vs:return []
    corners=np.array(list({tuple(np.round(v*bits,10)) for v in vs
                           for bits in product((0,1),repeat=4)}))
    hull=ConvexHull(corners)
    seen={}
    for eq in hull.equations:
        n,c=eq[:-1],-eq[-1]
        if c<1e-9:continue # coordinate nonnegativity
        if min(n)<-1e-7:raise ValueError(('negative upper normal',eq))
        n=np.maximum(n,0)/c
        key=tuple(np.round(n,9))
        seen[key]=n
    return list(seen.values())


def check(a,M,T=.75,eps=1e-4):
    groups=[];meta=[]
    for mode in product(range(3),repeat=2):
        vs=response_vertices(a,M,mode,T)
        fs=down_facets(vs)
        if fs:groups.append(fs);meta.append({'mode':mode,'vertices':len(vs),'facets':len(fs)})
    nz=sum(map(len,groups));n=4+nz
    obj=np.r_[np.ones(4),np.zeros(nz)]
    lower=np.zeros(n);upper=np.r_[[a,1-a,1-a,a],np.ones(nz)]
    integ=np.r_[np.zeros(4),np.ones(nz)]
    rows=[];lbs=[];ubs=[];z=4
    for fs in groups:
        chosen=np.zeros(n)
        for normal in fs:
            row=np.zeros(n);row[:4]=normal;row[z]=-(1+eps)
            rows.append(row);lbs.append(0);ubs.append(np.inf)
            chosen[z]=1;z+=1
        rows.append(chosen);lbs.append(1);ubs.append(np.inf)
    r=milp(obj,integrality=integ,bounds=Bounds(lower,upper),
           constraints=LinearConstraint(np.array(rows),lbs,ubs),
           options={'time_limit':60,'mip_rel_gap':1e-9})
    return {'a':a,'M':M,'T':T,'eps':eps,'modes':meta,'status':r.status,
            'message':r.message,'min_free':r.fun if r.x is not None else None,
            'u':r.x[:4].tolist() if r.x is not None else None,
            'dual_bound':getattr(r,'mip_dual_bound',None)}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--M',type=float,default=.32)
    p.add_argument('--a',type=float,default=.5);args=p.parse_args()
    print(json.dumps(check(args.a,args.M)),flush=True)
