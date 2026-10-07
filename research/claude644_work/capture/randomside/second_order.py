# Second-order analysis near n = 7/4 + d.  y = y0 + d*xi (+ quad corrections), xi>=0 on non-quads,
# sum (4-|S|) xi_S = 4.  At binding step j: e_j = d*(sigma_j ln(1/d) + beta_j) + O(d^2 ln 1/d).
import numpy as np, pickle, sys
from scipy.optimize import minimize, linprog
from seqgame import SAFE
reps=pickle.load(open('order_reps.pkl','rb'))
QUAD=set(i for i,S in enumerate(SAFE) if len(S)==4)
NQ=[i for i in range(64) if i not in QUAD]
def structure(order):
    steps=[]
    for j in range(7):
        prev=set(order[:j]); lj=order[j]
        groups={}
        for i,S in enumerate(SAFE): groups.setdefault(frozenset(set(S)&prev),[]).append(i)
        A=[];B=[];zero=True
        for key,mem in groups.items():
            qs=[i for i in mem if i in QUAD]
            sides=set(lj in SAFE[i] for i in qs)
            if len(sides)>1: zero=False; continue
            if len(sides)==1:
                sd=sides.pop(); A.append([i for i in mem if i not in QUAD and (lj in SAFE[i])!=sd])
            else:
                B.append(([i for i in mem if lj in SAFE[i]],[i for i in mem if lj not in SAFE[i]]))
        if zero: steps.append((j,A,B))
    return steps
def xl(x): return np.where(x>1e-300,x*np.log(np.maximum(x,1e-300)),0.0)
def sig(xi,A): return sum(xi[a].sum() for a in A)
def beta(xi,A,B):
    v=0.0
    for a in A:
        s=xi[a].sum()
        if s>0: v+= s*(1+np.log(1/(4*s)))
    for (i_,o_) in B:
        si=xi[i_].sum(); so=xi[o_].sum()
        v+= xl(np.array(si+so))-xl(np.array(si))-xl(np.array(so))
    return float(v)
wdef=np.array([4-len(S) for S in SAFE],float)
def optimize(order,starts=5,seed=0):
    st=structure(order)
    rng=np.random.default_rng(seed); best=None
    for tr in range(starts):
        x0=np.zeros(64); x0[NQ]=rng.random(len(NQ)); x0[NQ]*=4/np.dot(wdef[NQ],x0[NQ])
        v0=np.concatenate([x0,[0.0]])
        cons=[{'type':'eq','fun':lambda v: np.dot(wdef,v[:64]*np.isin(range(64),NQ))-4}]
        for (j,A,B) in st:
            cons.append({'type':'ineq','fun':lambda v,A=A: sig(v[:64],A)-1})
            cons.append({'type':'ineq','fun':lambda v,A=A,B=B: beta(np.maximum(v[:64],0),A,B)-v[64]})
        bnds=[(0,0) if i in QUAD else (0,None) for i in range(64)]+[(None,None)]
        r=minimize(lambda v:-v[64],v0,method='SLSQP',constraints=cons,bounds=bnds,options={'maxiter':2000,'ftol':1e-12})
        xi=np.maximum(r.x[:64],0)
        ok=abs(np.dot(wdef,xi)-4)<1e-7 and all(sig(xi,A)>=1-1e-7 for (j,A,B) in st)
        val=min(beta(xi,A,B) for (j,A,B) in st)
        if ok and (best is None or val>best[0]): best=(val,xi,st)
    return best
if __name__=="__main__":
    res=[]
    for o in reps:
        b=optimize(o,starts=3)
        res.append((b[0] if b else None,o))
        print(''.join(map(str,o)), b[0] if b else None, flush=True)
