"""Numerical minimax discovery for a first deletion in the clean paired state.

Inner solves are local nonlinear optimization, not upper-bound certificates.
All seven-row and endpoint conditions are omitted: a proved strict inner
upper bound would remain sufficient for a Q-minimum argument.
"""
import numpy as np
from itertools import product,combinations
from scipy.optimize import minimize
from p644_agent_alternative_paired_response import MASKS,WEIGHTS,TYPES

W=np.array(WEIGHTS);K=[]
for pair in combinations(range(3),2):
 mask=sum(3<<(2*j) for j in pair)
 K.append(np.array([[int((s|t)&mask==mask) for t in MASKS] for s in MASKS],dtype=float))
K=np.array(K)

def q(z):return np.einsum('i,pij,j->p',z[:6],K,z[6:12])
def qjac(z):
 return np.c_[np.einsum('pij,j->pi',K,z[6:12]),np.einsum('pij,i->pj',K,z[:6]),-np.ones(3)]
LIN=np.r_[np.c_[-np.eye(6),-np.eye(6),np.zeros(6)],
          np.array([[-1]*6+[0]*7,[0]*6+[-1]*6+[0]])]
RHS=np.r_[W,1,1]

def solve(D,starts=8,seed=0):
 rng=np.random.default_rng(seed);best=None
 bounds=[(0,float(w-d)) for w,d in zip(W,D)]+[(0,float(w)) for w in W]+[(0,1)]
 cons=[{'type':'ineq','fun':lambda z:RHS+LIN@z,'jac':lambda z:LIN},
       {'type':'ineq','fun':lambda z:q(z)-z[-1],'jac':qjac}]
 for it in range(starts):
  g=(W-D)*rng.random(6);h=(W-g)*rng.random(6)
  g=g/max(1,sum(g));h=h/max(1,sum(h));z=np.r_[g,h,0]
  r=minimize(lambda z:-z[-1],z,jac=lambda z:np.r_[np.zeros(12),-1],
   bounds=bounds,constraints=cons,method='SLSQP',options={'ftol':1e-11,'maxiter':300})
  if r.success and(best is None or r.fun<best.fun):best=r
 return None if best is None else {'q':float(-best.fun),'g':best.x[:6].tolist(),'h':best.x[6:12].tolist()}

if __name__=='__main__':
 import json,argparse
 p=argparse.ArgumentParser();p.add_argument('--starts',type=int,default=5);p.add_argument('--unit',type=int,default=8);a=p.parse_args()
 best=None;count=0
 for ds in product(*[range(round(w*a.unit)+1) for w in W]):
  if sum(ds)!=round(.75*a.unit):continue
  D=np.array(ds,dtype=float)/a.unit;out=solve(D,a.starts,count);count+=1
  if out is not None and(best is None or out['q']<best['q']):
   best=dict(out,deletion=D.tolist());print(count,json.dumps(best),flush=True)
 print('DONE',count,json.dumps(best),flush=True)
