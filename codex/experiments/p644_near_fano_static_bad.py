"""Discover static requests covering all pairs of a retained old-row graph.
Numerical optimality is exploratory only; rational feasible witnesses can
be independently checked. No minimum positive mass restriction.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from p644_near_fano_two_requests import cells
import argparse,json
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--time',type=float,default=50);ap.add_argument('--requests',type=int,default=4,choices=[2,3,4]);args=ap.parse_args()
 nr=args.requests; rows={2:[2,3,4,5,6],3:[2,4,5,6],4:[1,3,5]}[nr]
 cw=cells(rows); nc=(1<<nr)-1;n=len(cw); nq=nc*n;B=2*nq;nv=B+1;full=(1<<len(rows))-1
 x=lambda i,q:nc*i+(q-1);z=lambda i,q:nq+nc*i+(q-1)
 lb=np.zeros(nv);ub=np.ones(nv);integ=np.zeros(nv);integ[nq:B]=1
 for i,(s,w) in enumerate(cw):
  for q in range(1,nc+1):ub[x(i,q)]=w
 ub[B]=sum(w for _,w in cw)
 rr=[];cc=[];vv=[];lo=[];hi=[]
 def add(co,l=-np.inf,h=np.inf):
  row=len(lo)
  for j,v in co.items():rr.append(row);cc.append(j);vv.append(v)
  lo.append(l);hi.append(h)
 for i,(s,w) in enumerate(cw):
  add({x(i,q):1 for q in range(1,nc+1)},w,w)
  for q in range(1,nc+1):add({x(i,q):1,z(i,q):-w},h=0)
  for j,(t,ww) in enumerate(cw):
   if i>=j or s|t!=full:continue
   for q in range(1,nc+1):
    for r in range(1,nc+1):
     if q&r==0:add({z(i,q):1,z(j,r):1},h=1)
 for d in [1<<j for j in range(nr)]:
  co={x(i,q):1 for i in range(n) for q in range(1,nc+1) if q&d};co[B]=-1;add(co,h=0)
 obj=np.zeros(nv);obj[B]=1
 mat=coo_matrix((vv,(rr,cc)),shape=(len(lo),nv)).tocsr()
 res=milp(obj,integrality=integ,bounds=Bounds(lb,ub),constraints=LinearConstraint(mat,lo,hi),options={'time_limit':args.time,'mip_rel_gap':1e-9})
 result={'status':int(res.status),'message':res.message,'requests':nr,'rows':rows,'objective':float(res.fun) if res.fun is not None else None,'dual_bound':float(res.mip_dual_bound) if getattr(res,'mip_dual_bound',None) is not None else None}
 if res.x is not None:result['allocation']=[{'mask':format(s,'0%db'%len(rows)),'mass':w,'request_categories':{str(q):float(res.x[x(i,q)]) for q in range(1,nc+1) if res.x[x(i,q)]>1e-8}} for i,(s,w) in enumerate(cw)]
 Path('outputs/root_near_fano_static_bad_'+str(nr)+'.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
