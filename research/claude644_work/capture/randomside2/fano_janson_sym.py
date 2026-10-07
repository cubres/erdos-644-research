# Static Fano typed-Janson with PSL(2,7)-SYMMETRIC types (exact reduction: concave maxmin, invariant constraints =>
# a symmetric optimiser exists).  y_S = a_{|S|} for safe S (|S|=0..4; the 28 triples and 7 quads form single orbits).
# Line sums: a1 + 6 a2 + 12 a3 + 4 a4 = 1; total a0 + 7a1 + 21a2 + 28a3 + 7a4 = n.
# Marginal exponents for all 127 J (orbit duplicates harmless).  threshold tau_FJ(n).
import numpy as np, itertools, sys
from scipy.optimize import minimize
LINES=[frozenset(((i)%7,(i+1)%7,(i+3)%7)) for i in range(7)]
def safe(S):
    u=set()
    for l in S: u|=LINES[l]
    return len(u)<7
SAFE=[S for r in range(5) for S in itertools.combinations(range(7),r) if safe(S)]
SZ=np.array([len(S) for S in SAFE])
Js=[J for r in range(1,8) for J in itertools.combinations(range(7),r)]
rows=[];owner=[]
for j,J in enumerate(Js):
    keys={}
    for c,S in enumerate(SAFE): keys.setdefault(tuple(sorted(set(S)&set(J))),[]).append(c)
    for cs in keys.values():
        r=np.zeros(len(SAFE)); r[cs]=1; rows.append(r); owner.append(j)
BIG=np.array(rows); owner=np.array(owner); LEN=np.array([len(J) for J in Js])
# symmetric param a=(a1,a2,a3,a4) -> y ; a0 = n - (7a1+21a2+28a3+7a4)
def y_of(a,n):
    a1,a2,a3,a4=a; y=np.array([[0,a1,a2,a3,a4][s] for s in SZ],float)
    y[SZ==0]=n-(7*a1+21*a2+28*a3+7*a4); return y
def psi(x): return x*np.log(x)-(x-1)*np.log(x-1) if x>1 else 0.0
def exps(a,n,x):
    y=y_of(a,n); m=BIG@y
    t=np.where(m>0,m*np.log(np.maximum(m,1e-300)),0.0)
    s=np.bincount(owner,weights=t,minlength=len(Js))
    return n*np.log(n)-s-LEN*psi(x)
def maxmin(n,x):
    best=-1e9
    cons=[{'type':'eq','fun':lambda z: z[0]+6*z[1]+12*z[2]+4*z[3]-1},
          {'type':'ineq','fun':lambda z: n-(7*z[0]+21*z[1]+28*z[2]+7*z[3])},
          {'type':'ineq','fun':lambda z: exps(z[:4],n,x)-z[4]}]
    for a0 in [(0.1,0.05,0.03,0.05),(0.02,0.02,0.02,0.15),(0.2,0.05,0.02,0.02),(0.01,0.01,0.01,0.2)]:
        a0=np.array(a0); a0=a0/(a0[0]+6*a0[1]+12*a0[2]+4*a0[3])
        if 7*a0[0]+21*a0[1]+28*a0[2]+7*a0[3]>n: a0=np.array([0,0,0,0.25])
        z0=np.concatenate([a0,[exps(np.maximum(a0,1e-9),n,x).min()]])
        r=minimize(lambda z:-z[4],z0,constraints=cons,bounds=[(1e-12,None)]*4+[(None,None)],method='SLSQP',options={'maxiter':1000,'ftol':1e-14})
        z=r.x
        if abs(z[0]+6*z[1]+12*z[2]+4*z[3]-1)<1e-8 and n-(7*z[0]+21*z[1]+28*z[2]+7*z[3])>-1e-9:
            best=max(best,exps(z[:4],n,x).min())
    return best
def thresh(n):
    lo,hi=0.3,min(n-1.00001,1.0)
    if maxmin(n,n-hi)<=0: return None
    for _ in range(30):
        mid=(lo+hi)/2
        if maxmin(n,n-mid)>0: hi=mid
        else: lo=mid
    return hi
if __name__=="__main__":
    for n in [1.76,1.78,1.8,1.9,2.0,2.2,2.5,3.0,4.0,5.0,7.0,10.0,20.0]:
        print(f"n={n}: static Fano typed-Janson threshold tau = {thresh(n):.4f}",flush=True)
