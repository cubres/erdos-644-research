"""Direct bad-tuple discovery: one fixed anchor and six core rows.

Complement types on C1 must be pairwise intersecting and intersect every
complement type on C2. Both exclude the empty type because the anchor's
private part can be paired with a point common to all six core rows.
"""
import argparse,json,time
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import coo_matrix

def run(q,epsilon,limit,intervals=None,presolve=True):
    if intervals is None:
        intervals=[(1-q,1-2*q/3-epsilon),(q/2+epsilon,1-q/2-epsilon),(2*q/3+epsilon,q)]
    nc=63; nb=len(intervals);nv=4*nc+6*nb
    low=np.zeros(nv);high=np.full(nv,np.inf);high[2*nc:]=1
    integrality=np.zeros(nv);integrality[2*nc:]=1
    rr=[];cc=[];vv=[];lbs=[];ubs=[]
    def add(d,lo=-np.inf,hi=np.inf):
        r=len(lbs);lbs.append(lo);ubs.append(hi)
        for j,v in d.items():rr.append(r);cc.append(j);vv.append(v)
    for i in range(2):
        add({i*nc+m-1:1 for m in range(1,64)},q,q)
        for m in range(1,64):add({i*nc+m-1:1,2*nc+i*nc+m-1:-q},hi=0)
    for m in range(1,64):
        for n in range(1,64):
            if m&n==0:
                add({2*nc+m-1:1,3*nc+n-1:1},hi=1)
                if m<n:add({2*nc+m-1:1,2*nc+n-1:1},hi=1)
    deg=[]
    for j in range(6):
        ds=[{i*nc+m-1:1 for m in range(1,64)if m>>j&1}for i in range(2)]
        deg.append(ds[0]);add(dict(list(ds[0].items())+list(ds[1].items())),2*q-1,2*q-1)
        bs=[4*nc+j*nb+b for b in range(nb)];add({v:1 for v in bs},1,1)
        for b,(lo,hi)in enumerate(intervals):
            d=dict(ds[0]);d[bs[b]]=-2;add(d,lo=q-hi-2)
            d=dict(ds[0]);d[bs[b]]=2;add(d,hi=q-lo+2)
    for j in range(5):
        d=dict(deg[j])
        for i,v in deg[j+1].items():d[i]=d.get(i,0)-v
        add(d,lo=0)
    A=coo_matrix((vv,(rr,cc)),shape=(len(lbs),nv)).tocsc()
    start=time.time();res=milp(np.zeros(nv),integrality=integrality,bounds=Bounds(low,high),
        constraints=LinearConstraint(A,lbs,ubs),options={'time_limit':limit,'presolve':presolve})
    out={'q':q,'epsilon':epsilon,'intervals':intervals,'status':int(res.status),'message':res.message,'elapsed_seconds':time.time()-start}
    if res.x is not None:
        out['complement_cells']=[{'mask':m,'mass':[float(res.x[i*nc+m-1])for i in range(2)]}
                                for m in range(1,64)if any(res.x[i*nc+m-1]>1e-8 for i in range(2))]
        out['first_traces']=[q-sum(res.x[i]*v for i,v in d.items())for d in deg]
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--q',type=float,default=.87)
    p.add_argument('--epsilon',type=float,default=.001);p.add_argument('--limit',type=float,default=60)
    p.add_argument('--intervals')
    p.add_argument('--no-presolve',action='store_true')
    a=p.parse_args();print(json.dumps(run(a.q,a.epsilon,a.limit,json.loads(a.intervals)if a.intervals else None,not a.no_presolve),indent=2))
