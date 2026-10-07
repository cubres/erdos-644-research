import sys, re
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture'); sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
import numpy as np
from w4_typeclosed_lib import bad_tuple_milp
from inspect_fail import parse
lines=[l for l in open(sys.argv[1]) if l.startswith('FAIL')]
for l in lines[:int(sys.argv[2])]:
    x,g,T=parse(l); T=np.clip(T,0,None); T=T/T.sum(axis=1,keepdims=True); T=np.minimum(T,x)
    st,asg,cells=bad_tuple_milp([list(t) for t in T],list(x*0.95),time_limit=60)
    print(st,asg)
    if cells:
        for (i,S),m in sorted(cells.items()): print('  part',i,format(S,'07b')[::-1],round(m,4))
