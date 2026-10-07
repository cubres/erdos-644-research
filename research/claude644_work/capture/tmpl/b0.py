from lib2 import *
Q=F(3,4)
# class alpha=0, 0<beta<1 ; vars (x,y,al,be) with al fixed 0 via two inequalities
cons=[([0,0,1,0],0),([0,0,-1,0],0),([0,0,0,1],0),([0,0,0,-1],1),
      ([0,1,0,1],-1-Q),        # y-1+be>=3/4
      ([1,1,0,-1],-1-Q),       # N-1-be>=3/4
      ([1,0,0,-1],0),([0,1,0,0],-1)]
V=vertices(cons,4)
for v in V: print([str(c) for c in v],[k+1 for k in range(42) if feasible(k,*v)])
