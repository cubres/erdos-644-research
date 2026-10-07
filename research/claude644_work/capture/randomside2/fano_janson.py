# TYPED-JANSON criterion for STATIC Fano bad 7-tuples in H_rho (no richness, no game):
#   find y on the 64 safe patterns (line sums 1, total n) with  min_{J nonempty subset of lines} exponent_J(y) > 0,
#   exponent_J = n ln n - sum_T m_T ln m_T - |J| psi(x),  m = marginal of y on J.   (Lemma TJ, K_7 constant.)
# Threshold tau_FJ(n) = inf{tau : max_y min_J > 0}.  Compare with 3/4 and with the game threshold.
import numpy as np, itertools, sys, warnings; warnings.filterwarnings("ignore")
from scipy.optimize import minimize
LINES=[frozenset(((i)%7,(i+1)%7,(i+3)%7)) for i in range(7)]
def safe(S):
    u=set()
    for l in S: u|=LINES[l]
    return len(u)<7
SAFE=[S for r in range(5) for S in itertools.combinations(range(7),r) if safe(S)]
Js=[J for r in range(1,8) for J in itertools.combinations(range(7),r)]
def mm(J):
    keys={}
    for c,S in enumerate(SAFE): keys.setdefault(tuple(sorted(set(S)&set(J))),[]).append(c)
    M=np.zeros((len(keys),len(SAFE)))
    for i,cs in enumerate(keys.values()): M[i,cs]=1
    return M
MM=[mm(J) for J in Js]; LEN=np.array([len(J) for J in Js])
def psi(x): return x*np.log(x)-(x-1)*np.log(x-1) if x>1 else 0.0
def xlnx(v): v=np.maximum(v,1e-300); return v*np.log(v)
A=np.array([[1.0 if l in S else 0 for S in SAFE] for l in range(7)])
def allexp(y,n,x): return np.array([n*np.log(n)-np.sum(xlnx(M@y))-L*psi(x) for M,L in zip(MM,LEN)])
def maxmin(n,tau,tries=4,seed=0,sym=False):
    x=n-tau; rng=np.random.default_rng(seed); best=None
    cons=[{'type':'eq','fun':lambda z: A@z[:-1]-1},{'type':'eq','fun':lambda z: np.sum(z[:-1])-n},
          {'type':'ineq','fun':lambda z: allexp(z[:-1],n,x)-z[-1]}]
    for t in range(tries):
        y0=rng.random(len(SAFE))+0.2
        y0=y0/ (A@y0).max(); y0[0]=max(1e-3,n-y0[1:].sum()); z0=np.concatenate([y0,[-1]])
        r=minimize(lambda z:-z[-1],z0,constraints=cons,bounds=[(1e-10,None)]*len(SAFE)+[(None,None)],method='SLSQP',options={'maxiter':800,'ftol':1e-12})
        ok=np.all(np.abs(A@r.x[:-1]-1)<1e-7) and abs(np.sum(r.x[:-1])-n)<1e-7 and np.all(allexp(r.x[:-1],n,x)-r.x[-1]>-1e-7)
        if ok and (best is None or r.x[-1]>best[0]): best=(r.x[-1],r.x[:-1])
    return best
def thresh(n,lo=0.4):
    hi=min(n-1.0005,1.0)
    def pos(t):
        b=maxmin(n,t,tries=3); return b is not None and b[0]>0
    if not pos(hi): return None
    if pos(lo): return lo
    for _ in range(18):
        mid=(lo+hi)/2
        if pos(mid): hi=mid
        else: lo=mid
    return hi
if __name__=="__main__":
    for n in [float(a) for a in sys.argv[1].split(',')]:
        print(f"n={n}: static-Fano typed-Janson threshold tau = {thresh(n)}",flush=True)
