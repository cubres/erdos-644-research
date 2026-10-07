# First-moment exponents (per k, nats) in H_rho, N=nk, tau=tau_*k, u*=x k with x=n-tau_*, rho ~ 1/C(u*,k).
#  GT : E[# good triples (no common point) with union <= 2 tau k]      exponent gt(n,tau)
#  Q  : E[# 4-tuples violating Lemma Q's hypothesis (some order: |I5|<=t, |I6|+|I7|<=2t-k)]  exponent q(n,tau)
# NUMERICAL (max-entropy via SLSQP; concave programs).
import numpy as np, itertools, sys
from scipy.optimize import minimize
def xlnx(v): v=np.maximum(v,1e-300); return v*np.log(v)
def psi(x): return x*np.log(x)-(x-1)*np.log(x-1) if x>1 else 0.0
def ent(y,n):   # ln multinomial / k  for masses y (incl. empty cell) summing to n
    return xlnx(np.array([n]))[0]-np.sum(xlnx(y))
def gt_exp(n,tau):
    best=-1e9
    for b in np.linspace(max(0,(3-2*tau)/3),0.5,2001):
        a=1-2*b; y0=n-3*a-3*b
        if y0<0: continue
        y=np.array([a,a,a,b,b,b,y0]); best=max(best,ent(y,n))
    return best-3*psi(n-tau)
PAT=[S for r in range(5) for S in itertools.combinations(range(4),r)]
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def inI(S,mu): return any(set(p)<=set(S) for p in mu)
def q_exp(n,tau,tries=6,seed=0):
    rng=np.random.default_rng(seed); best=-1e9
    A=np.array([[1.0 if i in S else 0 for S in PAT] for i in range(4)])
    I=[np.array([1.0 if inI(S,mu) else 0 for S in PAT]) for mu in MATCH]
    cons=[{'type':'eq','fun':lambda y,i=i: A[i]@y-1} for i in range(4)]
    cons+=[{'type':'eq','fun':lambda y: np.sum(y)-n},
           {'type':'ineq','fun':lambda y: tau-I[0]@y},
           {'type':'ineq','fun':lambda y: (2*tau-1)-(I[1]@y+I[2]@y)}]
    for t in range(tries):
        y0=rng.random(len(PAT)); y0=y0/ y0.sum()*n
        r=minimize(lambda y:-ent(y,n),y0,constraints=cons,bounds=[(1e-12,None)]*len(PAT),method='SLSQP',options={'maxiter':500,'ftol':1e-12})
        if r.success and all(abs(c['fun'](r.x))<1e-7 if c['type']=='eq' else c['fun'](r.x)>-1e-7 for c in cons):
            best=max(best,-r.fun)
    return best-4*psi(n-tau)
if __name__=="__main__":
    for tau in [0.76,0.8,0.9,1.0]:
        print("tau",tau)
        for n in [tau+1.02,tau+1.1,tau+1.25,tau+1.5,tau+1.75,tau+2,tau+2.5,tau+3,tau+4,tau+5,tau+6,tau+8]:
            g=gt_exp(n,tau); q=q_exp(n,tau)
            print(f"  n={n:.3f} x={n-tau:.3f}  GT={g:+.4f}  Q={q:+.4f}  {'SURVIVES' if g<0 and q<0 else ''}",flush=True)
