import sys, re, json
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture'); sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import numpy as np
from w4_typeclosed_lib import bad_tuple_margin, tau_star
from heavylib import tau_star_fast
def parse(line):
    a=re.findall(r'\[([^\]]*)\]', line)
    p=[float(v) for v in a[-2].split(',')]; t=[float(v) for v in a[-1].split(',')]
    return np.array(p[:3]),np.array(p[3:6]),np.array(t).reshape(-1,3)
lines=[l for l in open(sys.argv[1]) if l.startswith('FAIL')]
for l in lines[:int(sys.argv[2])]:
    x,g,T=parse(l)
    T=np.clip(T,0,None); T=T/T.sum(axis=1,keepdims=True)
    T=np.minimum(T,x)
    ts=tau_star_fast(list(x),[list(t) for t in T])
    lam=bad_tuple_margin([list(t) for t in T],list(x),time_limit=60)
    print('x',np.round(x,3),'e',np.round(x-g,3),'tau*(revealed)',round(ts,4),'allsupport lambda',lam[0] if lam else None, lam[1] if lam else None,flush=True)
