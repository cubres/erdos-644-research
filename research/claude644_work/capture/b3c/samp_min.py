import sys; sys.path.insert(0,'heavy')
import numpy as np
from heavylib import fano_mask, reparr
from pairlib import pair_margin, FUNCS
rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)
R3=reparr(3)
def sample():
    while True:
        x=rng.uniform(0,1.5,3)
        if x.sum()<=2.25: continue
        sig=np.array([rng.uniform(2*xi/3, min(xi,1)) if 2*xi/3<min(xi,1) else None for xi in x],dtype=object)
        if any(s is None for s in sig): continue
        sig=sig.astype(float); e=x-sig
        if e.sum()<0.75: continue
        if max(e[0]+e[1],e[0]+e[2],e[1]+e[2])>0.75: continue
        M=[]
        ok=True
        for i in range(3):
            j,k=[t for t in range(3) if t!=i]
            rest=1-sig[i]
            lo=max(0,rest-x[k]); hi=min(x[j],rest)
            if lo>hi: ok=False;break
            mj=rng.uniform(lo,hi); mk=rest-mj
            m=np.zeros(3); m[i]=sig[i]; m[j]=mj; m[k]=mk
            # class constraint
            for t in (j,k):
                if 2*x[t]/3 < m[t] < sig[t]: ok=False
            M.append(m)
        if ok: return x,sig,np.array(M)
def menu(x,M):
    f=fano_mask(x,M,1e-12,R3).any()
    pm=pair_margin(x,M)
    return f, pm>=-1e-12
n=int(sys.argv[2]) if len(sys.argv)>2 else 2000
cnt=[0,0,0,0]; fails=[]
for it in range(n):
    x,sig,M=sample()
    f,p=menu(x,M)
    cnt[2*f+p]+=1
    if not f and not p: fails.append((x,sig,M))
print('none,paironly,fanoonly,both',cnt)
for x,sig,M in fails[:10]:
    print(np.round(x,3),np.round(x-sig,3),np.round(M,3).tolist())
