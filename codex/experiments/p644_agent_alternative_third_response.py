"""Discover a third request against the specific canonical second response.
This is not an adversary-independent third-response strategy.
"""
import sys
from itertools import combinations
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from p644_agent_alternative_two_response_certificate import CELLS


def fixed_cells(M=20,leave='plus'):
 # Second deletion B plus 9M of A: either leaves A+ or a 3M portion of A-.
 cells=[]
 for name,mask,g1,coef,const in CELLS:
  w=coef*M+const
  if name[0]=='A':
   g2=(w if name=='A+' else 0) if leave=='plus' else (3*M if name=='A-' else 0)
  elif name[0]=='B':g2=0
  elif coef:g2=1
  else:g2=0
  if g2:cells.append((name+'2',mask|(64 if g1 else 0)|128,g2))
  if w>g2:cells.append((name+'n',mask|(64 if g1 else 0),w-g2))
 cells.append(('G1fresh',64,M+3))
 cells.append(('G2fresh',128,28*M+3-sum(w for _,mask,w in cells if mask&128)))
 return cells


def profile(cells,rows,target):
 full=rows|64|128
 if any((mask&full)==full for _,mask,_ in cells):return None
 n=len(cells)
 gr=[{j for j,(_,other,_) in enumerate(cells) if i!=j and (mask|other)&full==full}
     for i,(_,mask,_) in enumerate(cells)]
 eligible=[i for i in range(n) if gr[i]]
 total=sum(cells[i][2] for i in eligible)
 # d_i whole-cell deletion, r_i removed endpoint iff closed neighborhood deleted.
 A=[];lo=[];hi=[]
 row=np.zeros(2*n)
 for i in eligible:row[n+i]=cells[i][2]
 A.append(row);lo.append(total-target+1);hi.append(np.inf)
 for i in eligible:
  for j in gr[i]|{i}:
   row=np.zeros(2*n);row[n+i]=1;row[j]=-1
   A.append(row);lo.append(-np.inf);hi.append(0)
 objective=np.r_[[c[2] for c in cells],np.zeros(n)]
 result=milp(objective,integrality=np.ones(2*n),bounds=Bounds(np.zeros(2*n),np.ones(2*n)),
             constraints=LinearConstraint(np.array(A),lo,hi),options={'time_limit':10})
 if result.x is None:return {'status':result.status}
 delete=[i for i in range(n) if result.x[i]>.5]
 removed=[i for i in eligible if gr[i]|{i}<=set(delete)]
 return {'cost':sum(cells[i][2] for i in delete),'endpoint_before':total,
         'endpoint_after_max':total-sum(cells[i][2] for i in removed),
         'delete':[(cells[i][0],cells[i][2]) for i in delete]}

if __name__=='__main__':
 M=int(sys.argv[1]) if len(sys.argv)>1 else 20
 for leave in ['plus','minus']:
  cells=fixed_cells(M,leave)
  for I in combinations(range(6),3):
   out=profile(cells,sum(1<<i for i in I),24*M)
   if out and out.get('cost',1e9)<=21*M+12:print(leave,''.join(str(i+1) for i in I),out,flush=True)
