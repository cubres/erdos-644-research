"""Discovery MILP for two static avoidance requests on a four-row graph.
Feasible solutions are checked as explicit rational allocations; numerical
infeasibility is only exploratory. No lower positive-occupancy cutoff.
"""
from collections import defaultdict
from itertools import combinations
import json
import argparse
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix


def cells(rows):
    lines=[frozenset(t) for t in combinations(range(7),3)
           if (t[0]+1)^(t[1]+1)^(t[2]+1)==0]
    c=defaultdict(int)
    for l in lines:
        c[sum(1<<j for j,r in enumerate(rows) if r not in l)]+=33
        for h in set(range(7))-l:
            c[sum(1<<j for j,r in enumerate(rows) if r not in l|{h})]+=1
    full=(1<<len(rows))-1
    assert full not in c
    return [(s,w) for s,w in sorted(c.items()) if any(s|t==full for t in c)]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--endpoint',type=float,default=110.99)
    ap.add_argument('--time',type=float,default=50)
    ap.add_argument('--budget',type=float,default=None)
    ap.add_argument('--requests',type=int,default=2,choices=[2,3])
    args=ap.parse_args()
    rows=[2,4,5,6] if args.requests==2 else [1,3,5]
    full=(1<<len(rows))-1
    nc=1<<args.requests
    cw=cells(rows); n=len(cw); nq=nc*n
    # x=mass; z=supported; a=activated endpoint category; u=endpoint mass.
    x=lambda i,q:nc*i+q
    z=lambda i,q:nq+nc*i+q
    a=lambda i,q:2*nq+nc*i+q
    u=lambda i,q:3*nq+nc*i+q
    B=4*nq; nv=B+1
    lb=np.zeros(nv); ub=np.ones(nv); integ=np.zeros(nv)
    integ[nq:3*nq]=1
    for i,(s,w) in enumerate(cw):
        for q in range(nc): ub[x(i,q)]=ub[u(i,q)]=w
    ub[B]=args.budget if args.budget is not None else 222
    rr=[];cc=[];vv=[];lo=[];hi=[]
    def add(co,l=-np.inf,h=np.inf):
        row=len(lo)
        for j,v in co.items():rr.append(row);cc.append(j);vv.append(v)
        lo.append(l);hi.append(h)
    for i,(s,w) in enumerate(cw):
        add({x(i,q):1 for q in range(nc)},w,w)
        for q in range(nc):
            add({x(i,q):1,z(i,q):-w},h=0)
            add({u(i,q):1,x(i,q):-1,a(i,q):-w},l=-w)
            # u>=x if a=1; u>=0 already if a=0.
            for j,(t,ww) in enumerate(cw):
                if s|t!=full:continue
                for r in range(nc):
                    if q&r==0: add({a(i,q):1,z(j,r):-1},l=0)
    for d in [1<<j for j in range(args.requests)]:
        co={x(i,q):1 for i in range(n) for q in range(nc) if q&d}
        co[B]=-1;add(co,h=0)
    add({u(i,q):1 for i in range(n) for q in range(nc)},h=args.endpoint)
    obj=np.zeros(nv)
    if args.budget is None:obj[B]=1
    else:
        for i in range(n):
            for q in range(nc):obj[u(i,q)]=1
    mat=coo_matrix((vv,(rr,cc)),shape=(len(lo),nv)).tocsr()
    res=milp(obj,integrality=integ,bounds=Bounds(lb,ub),constraints=LinearConstraint(mat,lo,hi),options={'time_limit':args.time,'mip_rel_gap':1e-9})
    result={'status':int(res.status),'message':res.message,'endpoint_target':args.endpoint,'budget_cap':args.budget,'requests':args.requests,'rows':rows,'objective':float(res.fun) if res.fun is not None else None,'dual_bound':float(res.mip_dual_bound) if getattr(res,'mip_dual_bound',None) is not None else None}
    if res.x is not None:
        result['allocation']=[{'mask':format(s,'0%db'%len(rows)),'mass':w,'D_categories':[float(res.x[x(i,q)]) for q in range(nc)]} for i,(s,w) in enumerate(cw)]
    path='outputs/root_near_fano_requests_'+str(args.requests)+'_'+str(args.endpoint)+'_'+str(args.budget)+'.json'
    open(path,'w').write(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
