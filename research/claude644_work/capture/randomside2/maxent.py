# Max-entropy via the convex DUAL:  max_{y>=0} -sum y ln y  s.t. Aeq y = beq, Aub y <= bub
#   <=  g(nu) = sum_S exp(-1 - a_S . nu) + b . nu   for ANY nu=(mu free, lam>=0)   (weak duality; RIGOROUS upper bound)
# minimise g by L-BFGS-B; also return the primal point y(nu) for diagnostics.
import numpy as np
from scipy.optimize import minimize
def maxent_dual(Aeq,beq,Aub=None,bub=None,x0=None):
    A=Aeq if Aub is None else np.vstack([Aeq,Aub]); b=beq if Aub is None else np.concatenate([beq,bub])
    ne=len(beq); m=A.shape[0]
    def g(nu):
        z=-1-A.T@nu; z=np.minimum(z,700); e=np.exp(z)
        return e.sum()+b@nu, -A@e+b
    bounds=[(None,None)]*ne+[(0,None)]*(m-ne)
    x0=np.zeros(m) if x0 is None else x0
    r=minimize(g,x0,jac=True,method='L-BFGS-B',bounds=bounds,options={'maxiter':20000,'ftol':1e-15,'gtol':1e-11})
    nu=r.x; y=np.exp(np.minimum(-1-A.T@nu,700))
    viol=np.concatenate([np.abs(Aeq@y-beq), np.maximum(0,(Aub@y-bub) if Aub is not None else np.zeros(0))])
    return r.fun, y, viol.max(), nu
def ent_primal(y): y=y[y>0]; return -np.sum(y*np.log(y))
