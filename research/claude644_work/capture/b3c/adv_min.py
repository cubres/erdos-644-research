import sys; sys.path.insert(0,'heavy')
import numpy as np
from heavylib import reparr, _PM
from pairlib import _FV
rng=np.random.default_rng(int(sys.argv[1]))
R3=reparr(3)
def fano_marg(x,M):
    rows=M[R3]; pen=np.einsum('ql,nlp->nqp',_PM,rows)
    s1=(2*x-pen).min(axis=1); s2=(4*x-rows.sum(axis=1))/2
    return np.minimum(s1,s2).min(axis=1).max()
def pair_marg(x,M):
    best=-9
    for V in _FV:
        Mx=(V[:,0][:,None,None,None]*M[None,:,None,:]+V[:,1][:,None,None,None]*M[None,None,:,:]).max(axis=0)
        best=max(best,(x[None,None,:]-Mx).min(axis=2).max())
    return best
def decode(z):
    # z: x(3), s-frac(3), split(3)
    x=z[:3]; sig=2*x/3+z[3:6]*(np.minimum(x,1)-2*x/3)
    M=np.zeros((3,3))
    for i in range(3):
        j,k=[t for t in range(3) if t!=i]
        rest=1-sig[i]; lo=max(0,rest-x[k]); hi=min(x[j],rest)
        mj=lo+z[6+i]*(hi-lo); M[i,i]=sig[i]; M[i,j]=mj; M[i,k]=rest-mj
    return x,sig,M
def penalty(z):
    if (z[3:]<0).any() or (z[3:]>1).any() or (z[:3]<=0.001).any() or (z[:3]>1.5).any(): return 9
    x,sig,M=decode(z)
    if (np.minimum(x,1)<2*x/3).any(): return 9
    e=x-sig; pen=0
    pen+=max(0,0.75-e.sum())
    pen+=max(0,e[0]+e[1]-0.75)+max(0,e[0]+e[2]-0.75)+max(0,e[1]+e[2]-0.75)
    for i in range(3):
        for t in range(3):
            if t!=i and 2*x[t]/3<M[i,t]<sig[t]: pen+=min(M[i,t]-2*x[t]/3, sig[t]-M[i,t])
        j,k=[t for t in range(3) if t!=i]
        if max(0,1-sig[i]-x[k])>min(x[j],1-sig[i]): pen+=1
    return pen
def score(z):
    p=penalty(z)
    if p>0: return 10+p
    x,sig,M=decode(z)
    return max(fano_marg(x,M),pair_marg(x,M))
best=None
for rs in range(int(sys.argv[2])):
    while True:
        z=np.concatenate([rng.uniform(0,1.5,3),rng.uniform(0,1,6)])
        if penalty(z)==0: break
    s=score(z); step=0.2
    for it in range(3000):
        z2=z+rng.normal(0,step,9)*(rng.random(9)<0.4)
        s2=score(z2)
        if s2<=s: z,s=z2,s2
        if it%500==499: step*=0.6
    x,sig,M=decode(z)
    print(rs, round(s,4), np.round(x,3), 'e',np.round(x-sig,3), np.round(M,3).tolist(), flush=True)
