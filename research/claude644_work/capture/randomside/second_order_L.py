# L-problem: maximize min_j (sigma_j(xi) L + beta_j(xi)) over xi>=0 (non-quads), sum (4-|S|)xi = 4.
import numpy as np, pickle, sys
from scipy.optimize import minimize
from second_order import structure, sig, beta, NQ, QUAD, wdef
def solveL(order,L,starts=4,seed=1,x0=None):
    st=structure(order)
    rng=np.random.default_rng(seed); best=None
    for tr in range(starts):
        if tr==0 and x0 is not None: x=x0.copy()
        else:
            x=np.zeros(64); x[NQ]=rng.random(len(NQ)); x[NQ]*=4/np.dot(wdef[NQ],x[NQ])
        v0=np.concatenate([x,[0.0]])
        cons=[{'type':'eq','fun':lambda v: np.dot(wdef,v[:64])-4}]
        for (j,A,B) in st:
            cons.append({'type':'ineq','fun':lambda v,A=A,B=B: sig(v[:64],A)*L+beta(np.maximum(v[:64],0),A,B)-v[64]})
        bnds=[(0,0) if i in QUAD else (0,None) for i in range(64)]+[(None,None)]
        r=minimize(lambda v:-v[64],v0,method='SLSQP',constraints=cons,bounds=bnds,options={'maxiter':3000,'ftol':1e-13})
        xi=np.maximum(r.x[:64],0)
        if abs(np.dot(wdef,xi)-4)>1e-7: continue
        val=min(sig(xi,A)*L+beta(xi,A,B) for (j,A,B) in st)
        if best is None or val>best[0]: best=(val,xi)
    return best
if __name__=="__main__":
    order=tuple(int(c) for c in sys.argv[1])
    for L in [5,10,20,50,100,1000]:
        b=solveL(order,L)
        print(L, b[0]-L, flush=True)
