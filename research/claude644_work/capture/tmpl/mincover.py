import itertools,sys
from cover import *
Q=F(3,4)
BASE = [([0,0,1,0], 0), ([0,0,-1,1], 0), ([0,0,0,-1], 1),([1,0,-1,0], -Q), ([0,1,0,1], -1-Q), ([1,1,1,-1], -1-Q),([1,0,0,-1], 0), ([0,1,1,0], -1)]
B0=[([0,0,1,0],0),([0,0,-1,0],0),([0,0,0,1],0),([0,0,0,-1],1),([0,1,0,1],-1-Q),([1,1,0,-1],-1-Q),([1,0,0,-1],0),([0,1,0,0],-1)]
pool=[int(a) for a in sys.argv[1].split(',')]
dom = BASE if sys.argv[2]=='int' else B0
for r in range(1,len(pool)+1):
    found=False
    for S in itertools.combinations(pool,r):
        ok,_=covered(dom,S)
        if ok: print('COVER',S); found=True
    if found: break
    print('none of size',r)
