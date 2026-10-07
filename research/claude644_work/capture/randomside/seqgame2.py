# Sequential entropy game, SLSQP with analytic gradients. value V(n,order)=max_y min_j e_j(y).
import numpy as np, itertools, sys
from scipy.optimize import minimize, brentq
from seqgame import SAFE, LINES, A_line, step_data, psi
EPS=1e-12
def xl(z): z=np.maximum(z,0); return np.where(z>0, z*np.log(np.maximum(z,EPS)),0.0)
def ent(y,Z,W):
    z=Z@y; w=W@y; return float(np.sum(xl(z)-xl(w)-xl(z-w)))
def gent(y,Z,W):
    z=Z@y; w=W@y
    lz=np.log(np.maximum(z,EPS)); lw=np.log(np.maximum(w,EPS)); lzw=np.log(np.maximum(z-w,EPS))
    return Z.T@lz - W.T@lw - (Z-W).T@lzw
def solve(n,order,starts=6,seed=0,y0=None):
    data=step_data(order)
    cons=[{'type':'eq','fun':lambda v: A_line@v[:64]-1,'jac':lambda v: np.hstack([A_line,np.zeros((7,1))])},
          {'type':'eq','fun':lambda v: np.array([np.sum(v[:64])-n]),'jac':lambda v: np.hstack([np.ones((1,64)),np.zeros((1,1))])}]
    for (Z,W) in data:
        cons.append({'type':'ineq','fun':(lambda v,Z=Z,W=W: ent(v[:64],Z,W)-v[64]),
                     'jac':(lambda v,Z=Z,W=W: np.concatenate([gent(v[:64],Z,W),[-1.0]]))})
    rng=np.random.default_rng(seed); best=None
    for tr in range(starts):
        if tr==0 and y0 is not None: y=y0.copy()
        else:
            y=rng.random(64)+0.05; y=y/np.sum(y)*n
        v0=np.concatenate([y,[min(ent(y,Z,W) for Z,W in data)]])
        r=minimize(lambda v:-v[64],v0,jac=lambda v: np.concatenate([np.zeros(64),[-1.0]]),method='SLSQP',
                   constraints=cons,bounds=[(0,None)]*64+[(None,None)],options={'maxiter':1000,'ftol':1e-13})
        y=np.maximum(r.x[:64],0)
        feas=max(np.max(np.abs(A_line@y-1)),abs(np.sum(y)-n))
        val=min(ent(y,Z,W) for Z,W in data)
        if feas<1e-7 and (best is None or val>best[0]): best=(val,y)
    return best
if __name__=="__main__":
    order=tuple(int(c) for c in sys.argv[1])
    for n in [1.8,2.0,2.5,3.0,4.0,6.0]:
        b=solve(n,order)
        if b is None: print(n,None); continue
        val=b[0]
        # x* with psi(x*)=val
        xs=brentq(lambda x: psi(x)-val,1+1e-12,1e9) if val>0 else 1.0
        print(f"n={n} V={val:.5f}  x*(V)={xs:.5f}  n-x*={n-xs:.5f}",flush=True)
