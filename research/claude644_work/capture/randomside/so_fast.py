# Fast second-order L-problem with analytic gradients.
import numpy as np, pickle, sys
from scipy.optimize import minimize
from second_order import structure, QUAD, NQ, wdef
E=1e-14
def build(order):
    st=structure(order); out=[]
    for (j,A,B) in st:
        Am=np.zeros((len(A),64))
        for g,a in enumerate(A): Am[g,a]=1
        Bi=np.zeros((len(B),64)); Bo=np.zeros((len(B),64))
        for g,(i_,o_) in enumerate(B): Bi[g,i_]=1; Bo[g,o_]=1
        out.append((j,Am,Bi,Bo))
    return out
def xl(x): return np.where(x>E, x*np.log(np.maximum(x,E)),0.0)
def f_j(x,Am,Bi,Bo,L):
    s=Am@x; si=Bi@x; so=Bo@x
    return L*s.sum() + np.sum(s - xl(4*s)/4*4/4 if False else s - s*np.log(np.maximum(4*s,E))) + np.sum(xl(si+so)-xl(si)-xl(so))
def g_j(x,Am,Bi,Bo,L):
    s=Am@x; si=Bi@x; so=Bo@x
    gs=L - np.log(np.maximum(4*s,E))
    gi=np.log(np.maximum(si+so,E))-np.log(np.maximum(si,E))
    go=np.log(np.maximum(si+so,E))-np.log(np.maximum(so,E))
    return Am.T@gs + Bi.T@gi + Bo.T@go
def solveL(order,L,starts=6,seed=1,x0=None,data=None):
    data=data or build(order)
    rng=np.random.default_rng(seed); best=None
    mask=np.zeros(64); mask[NQ]=1
    for tr in range(starts):
        if tr==0 and x0 is not None: x=x0.copy()
        else:
            x=np.zeros(64); x[NQ]=rng.random(len(NQ))+0.01; x*=4/np.dot(wdef,x)
        v0=np.concatenate([x,[min(f_j(x,A,B,C,L) for (_,A,B,C) in data)]])
        cons=[{'type':'eq','fun':lambda v: np.dot(wdef,v[:64])-4,'jac':lambda v: np.concatenate([wdef,[0]])}]
        for (j,A,B,C) in data:
            cons.append({'type':'ineq','fun':lambda v,A=A,B=B,C=C: f_j(np.maximum(v[:64],0),A,B,C,L)-v[64],
                         'jac':lambda v,A=A,B=B,C=C: np.concatenate([g_j(np.maximum(v[:64],0),A,B,C,L),[-1]])})
        bnds=[(0,0) if i in QUAD else (0,None) for i in range(64)]+[(None,None)]
        r=minimize(lambda v:-v[64],v0,jac=lambda v: np.concatenate([np.zeros(64),[-1.0]]),method='SLSQP',
                   constraints=cons,bounds=bnds,options={'maxiter':3000,'ftol':1e-14})
        xi=np.maximum(r.x[:64],0)
        if abs(np.dot(wdef,xi)-4)>1e-7: continue
        val=min(f_j(xi,A,B,C,L) for (_,A,B,C) in data)
        if best is None or val>best[0]: best=(val,xi)
    return best
if __name__=="__main__":
    order=tuple(int(c) for c in sys.argv[1])
    for L in [5,10,20,50,100,1000,10000]:
        b=solveL(order,L)
        print(L, round(b[0]-L,6), flush=True)
