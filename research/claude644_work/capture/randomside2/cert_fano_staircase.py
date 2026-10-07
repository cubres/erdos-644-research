# CERTIFICATE: static Fano typed-Janson criterion on the region R = {(n,x): x>=1, n-x>=3/4, x<=XMAX}.
# Symmetric type y_S = a_{|S|} (a1+6a2+12a3+4a4 = 1 exactly, a0 = n - 7a1-21a2-28a3-7a4 >= 0 exactly).
# E_J(y,n,x) = n ln n - sum_T m_T ln m_T - |J| psi(x)  for all 127 nonempty J (m = marginal of y on J).
# MONOTONICITY (hand): adding mass d to the empty cell (n -> n+d) raises every E_J (dE/dd = ln(n/m_empty^J) >= 0);
# E_J decreases in x.  Hence certifying E_J(y_i, n_i, x_i) > 0 for all J at n_i = x_{i-1}+3/4 covers the cell
# {x in [x_{i-1}, x_i], n >= x + 3/4} (use y_i + (n-n_i) e_empty).  Interval arithmetic (mpmath iv).
import numpy as np, itertools, sys
from fractions import Fraction as F
from mpmath import iv
from fano_janson_sym import SAFE, Js, maxmin, exps, SZ
from scipy.optimize import minimize
iv.dps=30
# counts[j] = list of (T-cell) -> vector of multiplicities c_s (s=0..4) so m_T = sum_s c_s a_s
COUNTS=[]
for J in Js:
    keys={}
    for S in SAFE:
        T=tuple(sorted(set(S)&set(J))); v=keys.setdefault(T,[0]*5); v[len(S)]+=1
    COUNTS.append((len(J),list(keys.values())))
def I(q): return iv.mpf(q.numerator)/iv.mpf(q.denominator)
def xlnx(v): return iv.mpf(0) if v.b<=0 else v*iv.log(v)
def best_a(n,x):
    cons=[{'type':'eq','fun':lambda z: z[0]+6*z[1]+12*z[2]+4*z[3]-1},
          {'type':'ineq','fun':lambda z: n-(7*z[0]+21*z[1]+28*z[2]+7*z[3])},
          {'type':'ineq','fun':lambda z: exps(z[:4],n,x)-z[4]}]
    best=None
    for a0 in [(0.1,0.05,0.03,0.05),(0.02,0.02,0.02,0.15),(0.2,0.05,0.02,0.02),(0.001,0.001,0.001,0.247)]:
        a0=np.array(a0); a0=a0/(a0[0]+6*a0[1]+12*a0[2]+4*a0[3])
        z0=np.concatenate([a0,[-1.0]])
        r=minimize(lambda z:-z[4],z0,constraints=cons,bounds=[(0,None)]*4+[(None,None)],method='SLSQP',options={'maxiter':500,'ftol':1e-13})
        if best is None or r.x[4]>best[4]: best=r.x
    return best[:4]
def certify_point(nq,xq,a):
    a2,a3,a4=[F(float(max(v,0))).limit_denominator(10**9) for v in a[1:4]]
    a1=1-6*a2-12*a3-4*a4
    A=[None,a1,a2,a3,a4]
    if a1<0: return None
    a0=nq-(7*a1+21*a2+28*a3+7*a4)
    if a0<0: return None
    A[0]=a0; AI=[I(v) for v in A]
    nI=I(nq); xI=I(xq); psi=xI*iv.log(xI)-(xI-1)*iv.log(xI-1) if xq>1 else iv.mpf(0)
    worst=None
    for L,cells in COUNTS:
        s=iv.mpf(0)
        for c in cells:
            m=sum(c[t]*AI[t] for t in range(5) if c[t]); s+=xlnx(m)
        e=nI*iv.log(nI)-s-L*psi
        if worst is None or e.a<worst: worst=e.a
    return worst
if __name__=="__main__":
    XMAX=F(sys.argv[1]) if len(sys.argv)>1 else F(9,2)
    xprev=F(1); h=F(1,20); cells=0; minmarg=None
    while xprev<XMAX:
        while True:
            xi=min(xprev+h,XMAX); ni=xprev+F(3,4)
            a=best_a(float(ni),float(xi))
            w=certify_point(ni,xi,a)
            if w is not None and w>1e-4: break
            h=h*F(4,5)
            if h<F(1,10**6): print("FAIL at x=",float(xprev)); sys.exit(1)
        cells+=1; minmarg=w if minmarg is None else min(minmarg,w)
        print(f"cell x in [{float(xprev):.5f},{float(xi):.5f}], n>=x+3/4: certified at (n={float(ni):.5f},x={float(xi):.5f}) min_J E_J >= {float(w):.5f}",flush=True)
        xprev=xi; h=min(h*2,F(7,10))
    print(f"CERTIFIED region x in [1,{float(XMAX)}], n-x>=3/4: {cells} cells, min margin {float(minmarg):.5f}")
