"""Closed-neighborhood third-profile discovery allowing partial cells."""
from itertools import combinations
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from p644_agent_alternative_third_scan import cells_for


def partial_profile(cells,rows,target,seconds=15):
 full=rows|64|128
 if any(mask&full==full for _,mask,_ in cells):return None
 n=len(cells); weights=np.array([w for _,_,w in cells])
 graph=[{j for j,(_,other,_) in enumerate(cells) if i!=j and (mask|other)&full==full}
     for i,(_,mask,_) in enumerate(cells)]
 eligible=[i for i in range(n) if graph[i]]
 total=sum(weights[i] for i in eligible)
 # d deletion masses, s removed endpoint masses, b support of s.
 A=[];lo=[];hi=[]
 def add(terms,L=-np.inf,U=np.inf):
  row=np.zeros(3*n)
  for i,w in terms.items():row[i]=w
  A.append(row);lo.append(L);hi.append(U)
 add({n+i:1 for i in eligible},L=total-target+1)
 for i in range(n):
  add({i:1,n+i:-1},L=0)
  add({n+i:1,2*n+i:-weights[i]},U=0)
  if not graph[i]:add({n+i:1},U=0)
  for j in graph[i]:add({j:1,2*n+i:-weights[j]},L=0)
 objective=np.r_[np.ones(n),np.zeros(2*n)]
 ints=np.zeros(3*n);ints[2*n:]=1
 res=milp(objective,integrality=ints,bounds=Bounds(np.zeros(3*n),np.r_[weights,weights,np.ones(n)]),
          constraints=LinearConstraint(np.array(A),lo,hi),options={'time_limit':seconds,'mip_rel_gap':0})
 if res.x is None:return {'status':int(res.status)}
 return {'status':int(res.status),'cost':res.fun,'endpoint_before':int(total),
         'delete':[(cells[i][0],round(res.x[i],8)) for i in range(n) if res.x[i]>1e-6],
         'remove':[(cells[i][0],round(res.x[n+i],8)) for i in range(n) if res.x[n+i]>1e-6]}

if __name__=='__main__':
 g=dict(zip(['A+','C-','D+','D-','E-','F+','F-'],[60,120,60,0,120,60,0]));h=20
 cells=cells_for(g,20,h)
 best=None
 for I in combinations(range(6),3):
  out=partial_profile(cells,sum(1<<i for i in I),480)
  if out and (best is None or out.get('cost',1e9)<best['cost']):
   best=dict(out,rows=''.join(str(i+1) for i in I));print(best,flush=True)
