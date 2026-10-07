"""Cofinal-containment LP against a globally bounded triple imbalance.

Numerical discovery only. All extreme points of the containment box
simplex are tested, which suffices for its convex projection inclusion.
No seven-row property is included: this isolates the max-imbalance route.
"""
from itertools import product,combinations
import numpy as np
from scipy.optimize import linprog

TYPES=list(product([0,1],repeat=3))
PAIRS=list(combinations(range(3),2))
EVEN=[i for i,t in enumerate(TYPES) if sum(t)%2==0]
L=np.array([[int(t[i]==t[j]) for t in TYPES] for i,j in PAIRS])

def check(v,s,T=.75,gap=False):
 w=np.zeros(8)
 for i,x in zip(EVEN,v):w[i]=x+s;w[7-i]=x
 a=np.array([sum(w[z] for z,t in enumerate(TYPES) if t[i]==t[j]==0) for i,j in PAIRS])
 A=np.r_[L,-L];b=np.r_[a+s,s-a];count=0
 for bits in product([0,1],repeat=8):
  u=np.array(bits)*w
  for j in range(8):
   d=u.copy();d[j]=T-sum(d[i] for i in range(8) if i!=j)
   if d[j]<-1e-8 or d[j]>w[j]+1e-8:continue
   d=np.maximum(0,np.minimum(w,d));count+=1
   if gap:
    good=False
    rows=np.array([[t[j] for t in TYPES] for j in range(3)])
    for modes in product(range(3),repeat=3):
     lo=np.array([0 if m==0 else T-s if m==1 else 1-s for m in modes])
     hi=np.array([s if m==0 else 1-T+s if m==1 else 1 for m in modes])
     if any(lo>hi+1e-9):continue
     r=linprog(np.zeros(8),A_ub=np.r_[A,rows,-rows],b_ub=np.r_[b,hi,-lo],A_eq=[np.ones(8)],b_eq=[1],bounds=list(zip(d,w)),method='highs')
     if r.success:good=True;break
   else:
    r=linprog(np.zeros(8),A_ub=A,b_ub=b,A_eq=[np.ones(8)],b_eq=[1],bounds=list(zip(d,w)),method='highs');good=r.success
   if not good:return {'s':s,'v':list(v),'count':count,'bad':d.tolist()}
 return {'s':s,'v':list(v),'count':count,'bad':None}

if __name__=='__main__':
 import json
 rng=np.random.default_rng(45)
 for run in range(12):
  s=.25+run*.015;v=rng.dirichlet(np.ones(4))*(1-2*s)
  print(json.dumps(check(v,s)),flush=True)
