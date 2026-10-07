import itertools,sys
from coverf import *
from fractions import Fraction as F
Q=F(3,4)
BASE = [([0,0,1,0], 0), ([0,0,-1,1], 0), ([0,0,0,-1], 1),([1,0,-1,0], -Q), ([0,1,0,1], -1-Q), ([1,1,1,-1], -1-Q),([1,0,0,-1], 0), ([0,1,1,0], -1)]
B0=[([0,0,1,0],0),([0,0,-1,0],0),([0,0,0,1],0),([0,0,0,-1],1),([0,1,0,1],-1-Q),([1,1,0,-1],-1-Q),([1,0,0,-1],0),([0,1,0,0],-1)]
pool=[int(a) for a in sys.argv[1].split(',')]
dom = BASE if sys.argv[2]=='int' else B0
maxr=int(sys.argv[3]) if len(sys.argv)>3 else len(pool)
for r in range(1,maxr+1):
    found=False
    for S in itertools.combinations(pool,r):
        ok,_=covered_f(dom,S)
        if ok: print('COVER',S,flush=True); found=True
    if found: break
    print('none of size',r,flush=True)
