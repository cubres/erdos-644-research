import random, itertools
from collections import Counter
random.seed(5)
T={'Ha':lambda s,t:7*s/4,'Hb':lambda s,t:7*t/4,'Qb':lambda s,t:max(3*t/2,s+3*t/4),
   'Qa':lambda s,t:max(3*s/2,3*s/4+t),'V':lambda s,t:max(s+t,5*s/4+t/2),"V'":lambda s,t:max(t+s,5*t/4+s/2),
   'K4':lambda s,t:max(2*s/3+t,4*s/3+t/2),"K4'":lambda s,t:max(2*t/3+s,4*t/3+s/2),
   'F61':lambda s,t:max(t,3*s/2+t/4),'F16':lambda s,t:max(s,3*t/2+s/4)}
def canon(x,th,box,mode):
    o=[i for i in range(3) if i!=box]; L=2
    v=[0.0]*3
    if mode=='minL':   # threshold in box, fill L first then the other box part
        v[box]=th; r=1-th; other=[i for i in o if i!=L][0] if box!=L else o[0]
        v[L]=min(x[L],r); r-=v[L]; v[other]=r
    elif mode=='minO': # threshold, fill other box part first
        v[box]=th; r=1-th; other=[i for i in o if i!=L][0]
        v[other]=min(x[other],r); r-=v[other]; v[L]=r
    elif mode=='max':  # as much as possible in box, then L, then other
        v[box]=min(x[box],1); r=1-v[box]; other=[i for i in o if i!=L][0]
        v[L]=min(x[L],r); r-=v[L]; v[other]=r
    if any(v[i]>x[i]+1e-12 or v[i]<-1e-12 for i in range(3)) or v[box]<th-1e-12: return None
    return v
C=Counter(); n=0; fails=Counter()
modes=['minL','minO','max']
for it in range(20000):
    xA=random.uniform(0.6,1.75); xB=random.uniform(0.6,1.75); xL=random.choice([0,random.uniform(0,1.75)])
    x=[xA,xB,xL]
    lo=max(4*xA/7,1-xB-xL); hi=min(xA,1)
    lo2=max(4*xB/7,1-xA-xL); hi2=min(xB,1)
    if lo>hi or lo2>hi2: continue
    thA=random.uniform(lo,hi); thB=random.uniform(lo2,hi2)
    if thA+thB+xL<1: continue
    tau=min(xA-thA+xB-thB, sum(x)-1)
    if tau<=0.75: continue
    n+=1
    for ma in modes:
        for mb in modes:
            a=canon(x,thA,0,ma); b=canon(x,thB,1,mb)
            if a is None or b is None: fails[(ma,mb)]+=1; continue
            w=[k for k,M in T.items() if all(M(a[i],b[i])<=x[i]+1e-12 for i in range(3))]
            if not w: fails[(ma,mb)]+=1
print('n',n)
for ma in modes:
    for mb in modes: print(ma,mb,'fail',fails[(ma,mb)])
