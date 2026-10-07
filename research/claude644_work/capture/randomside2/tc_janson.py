# TYPED JANSON criterion for the Two-Colour Lemma (TC) in H_rho.
# For a typed configuration (E + quartering, B1,B2,C1,C2) with cell masses y (32 cells), Janson gives
#   Pr[no TC configuration] <= exp(-min_J mu_J / (2*1545)),  mu_J = E[# J-sub-tuples of the merged marginal type].
# exponent_J(y) = n ln n - sum_T m_T ln m_T - |J| psi(x),  m = marginal of y on roles J (quarters merged).
# We maximise  s  s.t. exponent_J(y) >= s for all 31 nonempty J, TC linear constraints.  s>0 => TC violated whp.
import numpy as np, itertools, sys, warnings; warnings.filterwarnings("ignore")
from scipy.optimize import minimize
from window2 import TCP, quarter, Xrow, r14, r23, psi
roles=range(5)
Js=[J for r in range(1,6) for J in itertools.combinations(roles,r)]
def marg_matrix(J):
    keys={}; rows=[]
    for c,S in enumerate(TCP):
        key=tuple(sorted(set(S)&set(J)))
        keys.setdefault(key,[]).append(c)
    M=np.zeros((len(keys),len(TCP)))
    for i,(key,cs) in enumerate(keys.items()): M[i,cs]=1
    return M
MM={J:marg_matrix(J) for J in Js}
def xlnx(v): v=np.maximum(v,1e-300); return v*np.log(v)
def expJ(y,J,n,x): m=MM[J]@y; return n*np.log(n)-np.sum(xlnx(m))-len(J)*psi(x)
Aeq=np.array([[1.0 if i in S else 0 for S in TCP] for i in roles]+[[1.0]*len(TCP)])
def solve(n,tau,tries=6,seed=1):
    x=n-tau; rng=np.random.default_rng(seed); best=None
    beq=np.array([1.0]*5+[n])
    cons=[{'type':'eq','fun':lambda z: Aeq@z[:-1]-beq},
          {'type':'ineq','fun':lambda z: tau-(np.array(Xrow)+np.array(r14))@z[:-1]},
          {'type':'ineq','fun':lambda z: tau-(np.array(Xrow)+np.array(r23))@z[:-1]}]
    cons+=[{'type':'ineq','fun':lambda z,J=J: expJ(z[:-1],J,n,x)-z[-1]} for J in Js]
    for t in range(tries):
        y0=rng.random(len(TCP))+0.1; 
        # crude feasible-ish start: scale
        y0=y0/ (Aeq[:5]@y0).max(); z0=np.concatenate([y0,[-1.0]])
        r=minimize(lambda z:-z[-1],z0,constraints=cons,bounds=[(1e-9,None)]*len(TCP)+[(None,None)],method='SLSQP',options={'maxiter':1000,'ftol':1e-12})
        ok=all((np.all(np.abs(c['fun'](r.x))<1e-6) if c['type']=='eq' else np.all(c['fun'](r.x)>-1e-6)) for c in cons)
        if ok and (best is None or r.x[-1]>best[0]): best=(r.x[-1],r.x[:-1])
    return best
if __name__=="__main__":
    for tau in [float(a) for a in sys.argv[1].split(',')]:
        for n in [float(a) for a in sys.argv[2].split(',')]:
            if n-tau<=1: continue
            b=solve(n,tau)
            if b is None: print(f"tau={tau} n={n}: no feasible solution found",flush=True); continue
            s,y=b; worst=min(Js,key=lambda J: expJ(y,J,n,n-tau))
            print(f"tau={tau} n={n:.3f} x={n-tau:.3f}: max_y min_J exponent = {s:+.4f}  (binding J={worst})",flush=True)
