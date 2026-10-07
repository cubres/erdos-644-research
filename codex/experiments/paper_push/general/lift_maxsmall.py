"""Substitute the initial globally largest small intersection x for m."""
from fractions import Fraction as F

def lift(fn,*args):
 a=fn(*args,F(0));b=fn(*args,F(1))
 assert len(a)==len(b)
 out=[]
 for aa,bb in zip(a,b):
  assert len(aa)==len(bb)
  rr=[]
  for u,v in zip(aa,bb):
   assert u[1:]==v[1:],(u,v)
   rr.append((u[0],u[1]+v[0]-u[0],u[2],u[3]))
  out.append(rr)
 return out
