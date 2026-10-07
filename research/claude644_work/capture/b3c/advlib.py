"""Adversarial numerics for request strategies in the 3-super-class regime (float, discovery only)."""
import sys; sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import numpy as np
from heavylib import reparr, _PM
from pairlib import _FV
def fano_marg(x,T,R=None):
    T=np.asarray(T); 
    if R is None: R=reparr(len(T))
    rows=T[R]; pen=np.einsum('ql,nlp->nqp',_PM,rows)
    s1=(2*x-pen).min(axis=1); s2=(4*x-rows.sum(axis=1))/2
    m=np.minimum(s1,s2).min(axis=1); k=int(m.argmax())
    return m[k], R[k]
def pair_marg(x,T):
    T=np.asarray(T); best=-9; arg=None
    for f,V in enumerate(_FV):
        Mx=(V[:,0][:,None,None,None]*T[None,:,None,:]+V[:,1][:,None,None,None]*T[None,None,:,:]).max(axis=0)
        mm=(x[None,None,:]-Mx).min(axis=2)
        j,l=np.unravel_index(mm.argmax(),mm.shape)
        if mm[j,l]>best: best=mm[j,l]; arg=(f,j,l)
    return best,arg
def class_pen(t,x,sg,need=True):
    p=0; anyin=False
    for l in range(3):
        if t[l]>=sg[l]-1e-12: anyin=True
        elif t[l]>2*x[l]/3: p+=min(t[l]-2*x[l]/3, sg[l]-t[l])
    if need and not anyin:
        p+=min(max(0,sg[l]-t[l]) for l in range(3))
    return p
def base_decode(z):
    x=np.clip(z[:3],1e-4,1.5); sg=2*x/3+np.clip(z[3:6],0,1)*(np.minimum(x,1)-2*x/3)
    return x,sg
def type_from(v,x):
    v=np.abs(v); v=v/v.sum() if v.sum()>0 else np.ones(3)/3
    return v
def base_pen(x,sg,balanced=True):
    e=x-sg; p=max(0,0.75-e.sum())
    if balanced: p+=sum(max(0,e[a]+e[b]-0.75) for a,b in ((0,1),(0,2),(1,2)))
    p+=np.maximum(0,2*x/3-np.minimum(x,1)).sum()
    return p
