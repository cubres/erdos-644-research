"""Four-dimensional complementary-core transition and minimax discovery.

Any actual three cuts on 2k points have opposite masses (v_i+s,v_i),
sum(v)+2s=1 after normalization. A new cut is g in [u,w], sum(g)=1,
and its actual complement is w-g. All seven-row supports are inspected.
Inner SLSQP solves are LOCAL discovery, never certified upper bounds.
"""
from itertools import product,combinations
import json
import numpy as np
from scipy.optimize import minimize

TYPES=list(product([0,1],repeat=3));EVEN=[i for i,t in enumerate(TYPES) if sum(t)%2==0]
PAIRS=list(combinations(range(3),2))
MASKS=[sum(1<<(2*j+b) for j,b in enumerate(t)) for t in TYPES]
L=np.array([[int(t[i]==t[j]) for t in TYPES] for i,j in PAIRS],dtype=float)
K=[]
for pair in PAIRS:
 mask=sum(3<<(2*j) for j in pair)
 K.append(np.array([[int((u|v)&mask==mask) for v in MASKS] for u in MASKS],dtype=float))
K=np.array(K)

def masses(v,s):
 w=np.zeros(8)
 for i,x in zip(EVEN,v):w[i]=x+s;w[7-i]=x
 return w

def requests(w,T):
 out=set()
 for bits in product([0,1],repeat=8):
  base=np.array(bits)*w
  for j in range(8):
   u=base.copy();u[j]=T-sum(u[i] for i in range(8) if i!=j)
   if -1e-9<=u[j]<=w[j]+1e-9:out.add(tuple(np.round(np.maximum(0,np.minimum(w,u)),12)))
 return sorted(out)

def seven_check(w,g,tol=1e-8):
 atoms=[]
 for i,(ww,gg) in enumerate(zip(w,g)):
  if gg>tol:atoms.append(MASKS[i]|64)
  if ww-gg>tol:atoms.append(MASKS[i]|128)
 bad=[]
 for omitted in range(8):
  full=255^(1<<omitted)
  if not any((x|y)&full==full for x,y in combinations(atoms,2)):bad.append(omitted)
 return bad

class State:
 def __init__(self,v,s):
  self.v=np.array(v);self.s=s;self.w=w=masses(v,s)
  assert abs(sum(w)-2)<1e-7
  self.q=float(sum(self.v*(self.v+s)))
  self.a=np.array([sum(w[z] for z,t in enumerate(TYPES) if t[i]==t[j]==0) for i,j in PAIRS])

 def transitions(self,g):
  q=np.einsum('i,pij,j->p',g,K,self.w-g);signed=L@g-self.a
  states=[]
  for pair in PAIRS:
   weights=np.zeros(8)
   for i,t in enumerate(TYPES):
    j=4*t[pair[0]]+2*t[pair[1]]
    weights[j]+=g[i];weights[j+1]+=self.w[i]-g[i]
   ss=abs(weights[0]-weights[7]);vv=sorted(min(weights[i],weights[7-i]) for i in EVEN)
   states.append({'s':float(ss),'v':list(map(float,vv))})
  return {'q':q.tolist(),'s':abs(signed).tolist(),'states':states}

 def solve(self,u,lam=0,starts=8,seed=0):
  u=np.array(u);w=self.w;T=sum(u);old=self.q+lam*self.s**2
  generic=u+(1-T)/(2-T)*(w-u)
  impossible=seven_check(w,generic)
  if impossible:return {'margin':float('-inf'),'bad_generic_sevens':impossible,'request':u.tolist()}
  def phi(g):return np.einsum('i,pij,j->p',g,K,w-g)+lam*(L@g-self.a)**2-old
  def jac(g):return np.einsum('pij,j->pi',K,w-2*g)+2*lam*(L@g-self.a)[:,None]*L
  bounds=list(zip(u,w))+[(-2,2)]
  cons=[{'type':'eq','fun':lambda z:sum(z[:8])-1,'jac':lambda z:np.r_[np.ones(8),0]},
        {'type':'ineq','fun':lambda z:phi(z[:8])-z[8],'jac':lambda z:np.c_[jac(z[:8]),-np.ones(3)]}]
  rng=np.random.default_rng(seed);best=None
  for it in range(starts):
   # Convex combinations with generic preserve all lower bounds and rank.
   if it==0:g=generic.copy()
   else:
    order=rng.permutation(8);g=u.copy();remaining=1-T
    for i in order:
     add=min(remaining,w[i]-g[i]);g[i]+=add;remaining-=add
    g=.02*generic+.98*g
   z=np.r_[g,min(phi(g))]
   r=minimize(lambda z:-z[-1],z,jac=lambda z:np.r_[np.zeros(8),-1],bounds=bounds,constraints=cons,method='SLSQP',options={'ftol':1e-11,'maxiter':500})
   if r.success and(best is None or r.fun<best.fun):best=r
  if best is None:return {'margin':None,'request':u.tolist()}
  g=best.x[:8]
  return {'margin':float(-best.fun),'request':u.tolist(),'g':g.tolist(),
          'boundary_bad_sevens':seven_check(w,g),'transition':self.transitions(g)}

 def scan(self,T=.75,lam=0,starts=6):
  best=None;uu=requests(self.w,T)
  for seed,u in enumerate(uu):
   out=self.solve(u,lam,starts,seed)
   if out['margin'] is not None and(best is None or out['margin']<best['margin']):best=out
  return {'v':self.v.tolist(),'s':self.s,'q':self.q,'lambda':lam,'T':T,'requests':len(uu),'best':best}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--starts',type=int,default=8);p.add_argument('--T',type=float,default=.7501);a=p.parse_args()
 states=[State([.125,.125,0,0],.375),State([.0625]*4,.375),State([.01,.01,0,0],.49),State([.125]*4,.25)]
 for state in states:
  for lam in [0,.5,.9]:print(json.dumps(state.scan(a.T,lam,a.starts)),flush=True)
