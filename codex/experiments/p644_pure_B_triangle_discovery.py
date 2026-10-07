"""Discovery of alternate allocations for a symmetric clean-star profile."""
from collections import defaultdict
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix

ap=argparse.ArgumentParser();ap.add_argument('--c',type=float,default=37)
ap.add_argument('--a',type=float,default=33);ap.add_argument('--b',type=float,default=1)
ap.add_argument('--time',type=float,default=40)
ap.add_argument('--requests',type=int,choices=(2,3,4),default=2)
ap.add_argument('--old',type=str,default=None,help='one-based retained old rows, e.g. 2456')
ap.add_argument('--endpoint-bound',type=float,default=None);args=ap.parse_args()
b=args.b
a=37*b
args.a=a
args.c=0
args.requests=3
args.old='235'
typ=[('1234',a),('1256',a),('3456',a),('135',30*b+2),('35',2*b-1),('15',2*b-1),('13',2*b-1),('146',32*b),('16',2*b),('14',2*b),('236',34*b),('36',2*b),('245',36*b)]
types=[(sum(1<<(int(i)-1) for i in s),w) for s,w in typ]
cells=defaultdict(float);retained=tuple(int(c)-1 for c in args.old) if args.old else ((1,3,4,5)if args.requests==2 else(0,2,4))
full=(1<<len(retained))-1;nc=1<<args.requests
for s,w in types:
    mask=sum(bool(s>>r&1)<<j for j,r in enumerate(retained))
    cells[mask]+=w
cw=[(s,w)for s,w in sorted(cells.items())if w and any(s|t==full for t in cells)]
n=len(cw);nq=nc*n;nv=4*nq+1;B=nv-1
x=lambda i,q:nc*i+q
z=lambda i,q:nq+nc*i+q
act=lambda i,q:2*nq+nc*i+q
u=lambda i,q:3*nq+nc*i+q
lb=np.zeros(nv);ub=np.ones(nv);integ=np.zeros(nv);integ[nq:3*nq]=1
for i,(s,w)in enumerate(cw):
 for q in range(nc):ub[x(i,q)]=ub[u(i,q)]=w
ub[B]=sum(w for s,w in cw)
rr=[];cc=[];vv=[];lo=[];hi=[]
def add(co,l=-np.inf,h=np.inf):
 r=len(lo)
 for j,v in co.items():rr.append(r);cc.append(j);vv.append(v)
 lo.append(l);hi.append(h)
for i,(s,w)in enumerate(cw):
 add({x(i,q):1 for q in range(nc)},w,w)
 for q in range(nc):
  add({x(i,q):1,z(i,q):-w},h=0)
  add({u(i,q):1,x(i,q):-1,act(i,q):-w},l=-w)
  for j,(t,v)in enumerate(cw):
   if s|t!=full:continue
   for r in range(nc):
    if q&r==0:add({act(i,q):1,z(j,r):-1},l=0)
for bit in[1<<j for j in range(args.requests)]:
 co={x(i,q):1 for i in range(n)for q in range(nc)if q&bit};co[B]=-1;add(co,h=0)
p=3*args.a;k=144*b+1
add({u(i,q):1 for i in range(n)for q in range(nc)},h=p-.001 if args.endpoint_bound is None else args.endpoint_bound)
mat=coo_matrix((vv,(rr,cc)),shape=(len(lo),nv)).tocsr();obj=np.zeros(nv);obj[B]=1
res=milp(obj,integrality=integ,bounds=Bounds(lb,ub),constraints=LinearConstraint(mat,lo,hi),options={'time_limit':args.time,'mip_rel_gap':1e-8})
out={'a':args.a,'b':args.b,'c':args.c,'p':p,'k':k,'target':.75*k,'status':int(res.status),'message':res.message,'cost':float(res.fun)if res.x is not None else None}
out['requests']=args.requests;out['retained']=[r+1 for r in retained];out['endpoint_bound']=args.endpoint_bound
if res.x is not None:out['allocation']=[{'mask':format(s,f'0{len(retained)}b'),'weight':w,'q_masses':[float(res.x[x(i,q)])for q in range(nc)]}for i,(s,w)in enumerate(cw)]
suffix='' if args.old is None and args.endpoint_bound is None else f'_old{args.old}_ep{args.endpoint_bound}'
path=Path('outputs')/f'agent_pure_B_triangle_discovery_{b}.json';path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
