# RIGOROUS certificate (interval arithmetic on exact rational strategies) that V(n) >= psi(n-3/4) on [NA, NB],
# fixed line order 0..6.  Uses: V_order concave in n (convex combinations of feasible y), psi concave (tangent bound).
# For consecutive certified points (n_a, m_a), (n_b, m_b) with m = min_j e_j(y) (interval lower bound):
#   need m_a >= psi(n_a - 3/4)  and  m_b >= psi(n_a-3/4) + psi'(n_a-3/4) (n_b - n_a).
import numpy as np, sys, itertools, pickle
from fractions import Fraction as F
from mpmath import iv
from seqgame2 import solve
from seqgame import SAFE as SAFE_f, step_data
iv.dps=30
def I(x):
    if isinstance(x,F): return iv.mpf(x.numerator)/iv.mpf(x.denominator)
    return iv.mpf(x)
SAFE=[tuple(S) for S in SAFE_f]
QI=[i for i,S in enumerate(SAFE) if len(S)==4]; E0=SAFE.index(())
import sympy
M=sympy.Matrix([[1 if l in SAFE[i] else 0 for i in QI] for l in range(7)]); Minv=M.inv()
order=(0,1,2,3,4,5,6)
GROUPS=[]
for j in range(7):
    prev=set(order[:j]); lj=order[j]; G={}
    for i,S in enumerate(SAFE): G.setdefault(frozenset(set(S)&prev),[]).append(i)
    GROUPS.append((lj,list(G.values())))
def rationalize(y,den=10**9):
    Y=[F(int(round(v*den)),den) if (i not in QI and i!=E0) else F(0) for i,v in enumerate(y)]
    Y=[max(v,F(0)) for v in Y]
    rhs=sympy.Matrix([1-sum(Y[i] for i,S in enumerate(SAFE) if l in S) for l in range(7)])
    sol=Minv*rhs
    for k,i in enumerate(QI): Y[i]=F(int(sympy.fraction(sol[k])[0]),int(sympy.fraction(sol[k])[1]))
    assert all(Y[i]>=0 for i in QI)
    Y[E0]=max(F(0),F(int(round(y[E0]*den)),den))
    for l in range(7): assert sum(Y[i] for i,S in enumerate(SAFE) if l in S)==1
    return Y, sum(Y)
def xlog(x):
    if x.b<=0: return iv.mpf(0)
    return x*iv.log(x)
def minent(Y):
    vals=[]
    for lj,groups in GROUPS:
        tot=iv.mpf(0)
        for mem in groups:
            z=sum(Y[i] for i in mem); w=sum(Y[i] for i in mem if lj in SAFE[i])
            if z==0 or w==0 or w==z: continue
            tot+= xlog(I(z))-xlog(I(w))-xlog(I(z-w))
        vals.append(tot.a)
    return min(vals)
def psi(x): x=I(x); return x*iv.log(x)-(x-1)*iv.log(x-1)
def dpsi(x): x=I(x); return iv.log(x/(x-1))
if __name__=="__main__":
    NA=F(sys.argv[1]); NB=F(sys.argv[2])
    pts=[]; y0=None
    n=NA; h=F(1,100)
    def cert_point(nf,y0):
        b=solve(float(nf),order,starts=2 if y0 is not None else 4,y0=y0)
        Y,ntot=rationalize(b[1])
        return b[1],Y,ntot,minent(Y)
    ya,Ya,na,ma=cert_point(n,None)
    assert na<=n+F(1,10**6)
    # use actual total na (V monotone: V(n)>=V(na) for n>=na) -- we certify at na
    ok=ma>=psi(na-F(3,4)).b
    print(f"start n={float(na):.6f} m={float(ma):.6f} psi={float(psi(na-F(3,4)).b):.6f} ok={ok}",flush=True)
    while na<NB and ok:
        while True:
            nbt=na+h
            yb,Yb,nb,mb=cert_point(nbt,ya)
            need=(psi(na-F(3,4))+dpsi(na-F(3,4))*(I(nb)-I(na))).b
            if mb>=need and mb>=psi(nb-F(3,4)).b and nb>na:
                break
            h=h/2
            if h<F(1,10**5): print("FAIL at",float(na)); sys.exit(1)
        pts.append((float(na),float(nb),float(mb)))
        print(f"[{float(na):.6f},{float(nb):.6f}] m_b={float(mb):.6f} need={float(need):.6f} h={float(h):.5f}",flush=True)
        ya,Ya,na,ma=yb,Yb,nb,mb
        h=min(h*F(3,2),F(1,4))
    print("CERTIFIED [%s, %s]"%(float(NA),float(na)))
