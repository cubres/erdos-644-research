from lib2 import *
Q = F(3,4)
# vars (x,y,al,be)
cons = [
 ([0,0,1,0], 0),            # al>=0
 ([0,0,-1,1], 0),           # be>=al
 ([0,0,0,-1], 1),           # be<=1
 ([1,0,-1,0], -Q),          # T1 x-al>=3/4
 ([0,1,0,1], -1-Q),         # T2 y-1+be>=3/4
 ([1,1,1,-1], -1-Q),        # T3 x+y-1-(be-al)>=3/4
 ([1,0,0,-1], 0),           # fit x>=be
 ([0,1,1,0], -1),           # fit y>=1-al
]
V = vertices(cons, 4)
print(len(V), 'vertices')
for v in V:
    fs = [k+1 for k in range(42) if feasible(k,*v)]
    print([str(c) for c in v], fs)
