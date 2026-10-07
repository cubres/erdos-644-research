# TC SEQUENTIAL ENTROPY GAME (analogue of the Fano game, Lemma S, but only 4 richness steps, depth <= 3 or 4).
# Order: E (any edge), quartering Q (free), B1 | (E,Q), B2 | (E,Q,B1), C1 | (E,Q,B1,B2), C2 | (E,Q,B1,B2[,C1]).
# Step entropy e_r = H(roles R u {r}) - H(roles R)   (H = -sum m ln m over marginal cells; E-cells split by quarter).
# Win iff max_y min_r e_r > psi(x) (richness level ln C(u*,k)).  variant 'd3': C2 | (E,Q,B1,B2), X bounded by
# |C1&W|+|C2&W|;  variant 'd4': C2 | (E,Q,B1,B2,C1), exact X.   Threshold tau_game(n) = inf{n-x : win}.
import numpy as np, itertools, sys, warnings; warnings.filterwarnings("ignore")
from scipy.optimize import minimize
from window2 import TCP, quarter, Xrow, r14, r23, psi
def xlnx(v): v=np.maximum(v,1e-300); return v*np.log(v)
def mmat(R):
    keys={}
    for c,(S,q) in enumerate(zip(TCP,quarter)):
        key=(tuple(sorted(set(S)&set(R))), q if 0 in S else 0)
        keys.setdefault(key,[]).append(c)
    M=np.zeros((len(keys),len(TCP)))
    for i,cs in enumerate(keys.values()): M[i,cs]=1
    return M
def H(M,y): return -np.sum(xlnx(M@y))
W=np.array([1.0 if (q==0 and (1 in S or 2 in S)) else 0 for S,q in zip(TCP,quarter)])
C1=np.array([1.0 if 3 in S else 0 for S in TCP]); C2=np.array([1.0 if 4 in S else 0 for S in TCP])
def setup(variant):
    steps=[((0,),1),((0,1),2),((0,1,2),3),((0,1,2) if variant=='d3' else (0,1,2,3),4)]
    return [(mmat(R),mmat(R+(r,))) for R,r in steps]
Aeq=np.array([[1.0 if i in S else 0 for S in TCP] for i in range(5)]+[[1.0]*len(TCP)])
def game_value(n,tau,variant='d4',tries=8,seed=0):
    ST=setup(variant); rng=np.random.default_rng(seed); beq=np.array([1.0]*5+[n])
    Xl=(W*C1+W*C2) if variant=='d3' else np.array(Xrow)
    cons=[{'type':'eq','fun':lambda z: Aeq@z[:-1]-beq},
          {'type':'ineq','fun':lambda z: tau-(Xl+np.array(r14))@z[:-1]},
          {'type':'ineq','fun':lambda z: tau-(Xl+np.array(r23))@z[:-1]}]
    cons+=[{'type':'ineq','fun':lambda z,A=A,B=B: H(B,z[:-1])-H(A,z[:-1])-z[-1]} for A,B in ST]
    best=None
    for t in range(tries):
        y0=rng.random(len(TCP))+0.05; y0=y0*(n/y0.sum()); z0=np.concatenate([y0,[0.0]])
        r=minimize(lambda z:-z[-1],z0,constraints=cons,bounds=[(1e-10,None)]*len(TCP)+[(None,None)],method='SLSQP',options={'maxiter':2000,'ftol':1e-13})
        ok=all((np.all(np.abs(c['fun'](r.x))<1e-7) if c['type']=='eq' else np.all(c['fun'](r.x)>-1e-7)) for c in cons)
        if ok and (best is None or r.x[-1]>best[0]): best=(r.x[-1],r.x[:-1])
    return best
def threshold(n,variant,lo=0.3,hi=None):
    hi=min(n-1.0001,1.0) if hi is None else hi
    def win(t):
        b=game_value(n,t,variant,tries=5); return b is not None and b[0]>psi(n-t)
    if not win(hi): return None
    for _ in range(22):
        mid=(lo+hi)/2
        if win(mid): hi=mid
        else: lo=mid
    return hi
if __name__=="__main__":
    variant=sys.argv[1]
    for n in [float(a) for a in sys.argv[2].split(',')]:
        t=threshold(n,variant)
        print(f"{variant} n={n:.3f}: TC-game threshold tau = {t}",flush=True)
