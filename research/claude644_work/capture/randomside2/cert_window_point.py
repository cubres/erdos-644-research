# CERTIFICATE (interval arithmetic) for Proposition W: at n=2.6, x=1.84 (rho=1/C(1.84k,k)), union bound 2*0.765:
#   n ln n + max{-sum y ln y : GT patterns, edge sizes 1, total n, union<=1.53} - 3 psi(1.84) < 0.
# Weak duality: for ANY nu=(mu (eq, free), lam>=0 (ineq)), max <= sum_S exp(-1 - a_S.nu) + b.nu.  We evaluate the
# dual function at a rationalised nu with mpmath interval arithmetic.
import numpy as np, sys
from fractions import Fraction as F
from mpmath import iv, mpf
from maxent import maxent_dual
from window2 import GTP
iv.dps=40
def certify(n,x,U):
    P=GTP
    Aeq=np.array([[1.0 if i in S else 0 for S in P] for i in range(3)]+[[1.0]*len(P)]); beq=np.array([1,1,1,n],float)
    Aub=np.array([[1.0 if len(S)>0 else 0 for S in P]]); bub=np.array([U])
    val,y,viol,nu=maxent_dual(Aeq,beq,Aub,bub)
    nuq=[F(v).limit_denominator(10**8) for v in nu]
    if nuq[-1]<0: nuq[-1]=F(0)
    A=np.vstack([Aeq,Aub]); b=[F(n).limit_denominator(10**6) if i==3 else None for i in range(4)]
    bq=[F(1),F(1),F(1),F(str(n)),F(str(U))]
    I=lambda q: iv.mpf(q.numerator)/iv.mpf(q.denominator)
    g=sum(I(bq[i])*I(nuq[i]) for i in range(5))
    for s in range(len(P)):
        z=-1-sum(int(A[i,s])*I(nuq[i]) for i in range(5))
        g+=iv.exp(z)
    nI=I(F(str(n))); xI=I(F(str(x)))
    psi=xI*iv.log(xI)-(xI-1)*iv.log(xI-1)
    expo=nI*iv.log(nI)+g-3*psi
    return val, expo
if __name__=="__main__":
    for (n,x,U) in [(2.6,1.84,1.53),(2.55,1.79,1.53),(2.7,1.94,1.53)]:
        val,expo=certify(n,x,U)
        print(f"n={n} x={x} union<={U}: float dual {val:.6f}; CERTIFIED exponent interval [{float(expo.a):.6f},{float(expo.b):.6f}] ->", "NEGATIVE (PASS)" if expo.b<0 else "FAIL")
