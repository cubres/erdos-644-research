# one-sided two-box families over parts A,B,L: does some PAIR of admissible types admit a bad tuple (42 functions)?
import random, itertools
import numpy as np
from lib2 import FUNCS
random.seed(3)
FV=[np.array([[float(u),float(v)] for u,v in f]) for f in FUNCS]
def pair_ok(x,a,b):
    for V in FV:
        if all((V@np.array([a[i],b[i]])).max()<=x[i]+1e-12 for i in range(3)): return True
    return False
def box_types(x,th,box,g=12):
    # types with coordinate box >= th[box], sum 1, <= x ; grid over the free coordinates
    out=[]
    others=[i for i in range(3) if i!=box]
    for s in np.linspace(th[box],min(x[box],1),g):
        rest=1-s
        for t in np.linspace(0,1,g):
            v=[0,0,0]; v[box]=s; v[others[0]]=rest*t; v[others[1]]=rest*(1-t)
            if all(v[i]<=x[i]+1e-12 for i in range(3)): out.append(v)
    return out
bad=0; n=0
for it in range(3000):
    xA=random.uniform(0.6,1.75); xB=random.uniform(0.6,1.75); xL=random.uniform(0,1.75)
    x=[xA,xB,xL]
    thA=random.uniform(max(4*xA/7,1-xB-xL),min(xA,1)); thB=random.uniform(max(4*xB/7,1-xA-xL),min(xB,1))
    if thA>min(xA,1) or thB>min(xB,1): continue
    if thA+thB+xL<1: continue
    tau=min(xA-thA+xB-thB, sum(x)-1)
    if tau<=0.75: continue
    n+=1
    TA=box_types(x,[thA,thB],0); TB=box_types(x,[thA,thB],1)
    found=False
    for a in TA:
        for b in TB:
            if pair_ok(x,a,b): found=True; break
        if found: break
    if not found:
        # also same-box pairs
        for P in (TA,TB):
            for a,b in itertools.combinations(P,2):
                if pair_ok(x,a,b): found=True; break
            if found: break
    if not found:
        bad+=1; print('NO PAIR', [round(v,4) for v in x], round(thA,4), round(thB,4), 'tau',round(tau,4))
print('instances',n,'no-pair',bad)
