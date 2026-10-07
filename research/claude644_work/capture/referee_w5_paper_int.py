# Integer-level exhaustive check of Prop 4.1: for each r, T=ceil(beta r+3) (minimal allowed; all hyps
# are monotone in T), every integer (m,y,z), classify by the paper's chain (exact rational), then check
# the INTEGER hypotheses of the cited lemma at (r,T) directly (no scaling), incl. c4 rounded splits.
import sys
from fractions import Fraction as F
from math import ceil, floor
b=F(173,200); e=F(27,200)
def pos(v): return v if v>0 else 0
def L32(r,T,x,y,z):
    S=x+y+z; return min(T-S, T-(r-x+z), T-(r-y+z), 2*T-(2*r-2*x+y), 2*T-(2*r-2*y+x), 3*T-(r+2*x+2*y+z))
def L33(r,T,x,y,z):
    S=x+y+z; return min(r-T, T-S, 2*T-(r+2*y), 2*T-(r+2*x-y+z), 3*T-(r+2*x+y+3*z))
def L34(r,T,x,y,z):
    S=x+y+z; return min(r-T, T-(x+y), 2*T-(r+2*x), 2*T-(r+2*y), T-(r+x-y-z), T-(r-x+y-z),
                        3*T-(3*r-S), 5*T-(3*r+S), 3*T-(r+x+y+2*z), 4*T-(2*r+3*z))
def L36(r,T,x,y,z):
    P=pos(r+y-x-z-T); Q=pos(r+x-y-z-T)
    return min(T-x, T-y, T-(r-x+z)-P-Q, T-(y+z)-Q, 2*T-(r+y+2*z)-P-2*Q)
def L35(r,T,x,y,z,x1,y1,z1):
    return min(x1,x-x1,y1,y-y1,z1,z-z1,T-(x1+y1+z1),(y1+z1)-(r+x-T),(x1+z1)-(r+y-T),(x1+y1)-(r+z-T))
def run(r):
    T=ceil(b*r+3)
    if T>r: return 0,0
    bad=0; n=0
    M=floor(F(23,50)*r)
    for m in range(0,M+1):
        for y in range(0,m+1):
            if 200*(m+2*y)>227*r: break
            for z in range(0,y+1):
                n+=1
                mm,yy,zz=F(m,r),F(y,r),F(z,r)
                u=mm+yy; d=mm-yy; S=mm+yy+zz
                if mm<=F(119,400):
                    B=ceil(max(F(3*r+m,4),F(2*r+2*m,3)))
                    v = T-B if 2*m<=r else -1
                    c='a'
                elif yy<=F(73,200):
                    if yy-zz>mm-e: c='b2'; v=L33(r,T,m,y,z)
                    elif S<F(81,200): c='b3'; v=L33(r,T,z,y,m)
                    else: c='b1'; v=L34(r,T,z,y,m)
                else:
                    if zz<=F(319,200)-2*u: c='c1'; v=L32(r,T,m,y,z)
                    elif zz<e-d: c='c2'; v=L36(r,T,y,m,z)
                    elif zz<=(F(146,200)-yy)/2: c='c3'; v=L36(r,T,m,y,z)
                    else:
                        if 3*zz>=e+u: s=((e+yy+zz-mm)/2,(e+mm+zz-yy)/2,(e+mm+yy-zz)/2); c='c4A'
                        else: s=(e+yy-zz,e+mm-zz,zz); c='c4B'
                        x1,y1,z1=[ceil(t*r) for t in s]
                        v=L35(r,T,m,y,z,x1,y1,z1)
                if v<0:
                    bad+=1
                    if bad<5: print('FAIL r',r,'T',T,(m,y,z),c,v)
    return n,bad
rs=list(range(23,121))+[150,200,257,333,401,512]
tot=0;tb=0
for r in rs:
    n,bd=run(r); tot+=n; tb+=bd
print('triples',tot,'fails',tb)
