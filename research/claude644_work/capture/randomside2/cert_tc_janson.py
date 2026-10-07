# CERTIFICATE (pointwise): typed-Janson criterion for the Two-Colour Lemma in H_rho at (n, x, tau').
# Find y (32 TC cells) by SLSQP (tc_janson.solve), rationalise, repair the 5 edge-size equalities exactly
# (adjust the outside-only cells {B1},{B2},{C1},{C2} and the E-only cell of quarter 1), set the empty cell to
# n - sum; check exactly: y>=0, TC constraints |X|+max(e1+e4,e2+e3) <= tau'; then evaluate all 31 marginal
# exponents  n ln n - sum m ln m - |J| psi(x)  in mpmath interval arithmetic; PASS iff all lower ends > 0.
import numpy as np, sys, itertools
from fractions import Fraction as F
from mpmath import iv
from window2 import TCP, quarter, Xrow, r14, r23
from tc_janson import solve, Js
iv.dps=40
def I(q): return iv.mpf(q.numerator)/iv.mpf(q.denominator)
def xlnx(v): return v*iv.log(v) if v.a>0 else iv.mpf(0)
def cert(n,x,taup):
    b=solve(float(n),float(n-x),tries=6)     # nominal tau = n-x
    s,y=b
    Y=[F(float(v)).limit_denominator(10**7) for v in y]
    # repair: role sizes exactly 1 using single-role cells
    single={r: next(c for c,S in enumerate(TCP) if S==(r,) and (r!=0 or quarter[c]==1)) for r in range(5)}
    for r in range(5):
        tot=sum(Y[c] for c,S in enumerate(TCP) if r in S)
        Y[single[r]]+=1-tot
    empty=next(c for c,S in enumerate(TCP) if S==())
    Y[empty]=0; Y[empty]=F(n)-sum(Y)
    assert all(v>=0 for v in Y), min(Y)
    for r in range(5): assert sum(Y[c] for c,S in enumerate(TCP) if r in S)==1
    assert sum(Y)==F(n)
    X=sum(Y[c] for c in range(len(TCP)) if Xrow[c]); a=sum(Y[c] for c in range(len(TCP)) if r14[c]); bb=sum(Y[c] for c in range(len(TCP)) if r23[c])
    assert X+max(a,bb)<=taup, (float(X+max(a,bb)),float(taup))
    xI=I(F(x)); psi=xI*iv.log(xI)-(xI-1)*iv.log(xI-1); nI=I(F(n))
    worst=None
    for J in Js:
        m={}
        for c,S in enumerate(TCP):
            key=tuple(sorted(set(S)&set(J))); m[key]=m.get(key,F(0))+Y[c]
        e=nI*iv.log(nI)-sum(xlnx(I(v)) for v in m.values())-len(J)*psi
        if worst is None or e.a<worst[0]: worst=(e.a,J)
    return float(s), float(X+max(a,bb)), worst
if __name__=="__main__":
    for (n,x,taup) in [(F('2.6'),F('1.84'),F('0.755')),(F('1.8'),F('1.04'),F('0.755')),(F('4'),F('3.24'),F('0.755')),(F('10'),F('9.24'),F('0.755'))]:
        s,used,worst=cert(n,x,taup)
        print(f"n={float(n)} x={float(x)} tau'={float(taup)}: float maxmin {s:+.4f}; exact TC load {used:.6f}<=tau'; certified min_J exponent >= {float(worst[0]):+.5f} at J={worst[1]} ->", "PASS" if worst[0]>0 else "FAIL",flush=True)
