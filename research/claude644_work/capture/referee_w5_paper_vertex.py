# Independent exact check of Prop 4.1 (paper_0865) at r=1, T=beta.
# Every hypothesis used is concave in (m,y,z) (min of linear), so it suffices to check vertices
# of the CLOSURE of each (convex) case polytope. Hypotheses are re-typed from the LEMMA statements
# (not from the case text), with the role assignment applied mechanically.
from fractions import Fraction as F
from itertools import combinations
b=F(173,200); e=1-b
def R(a): return F(a)
# constraints as (coeffs(m,y,z), const): c.m + c.y + c.z + const >= 0
def ge(cm,cy,cz,c0): return (F(cm),F(cy),F(cz),F(c0))
base=[ge(0,0,1,0), ge(0,1,-1,0), ge(1,-1,0,0), ge(-1,0,0,F(92,200)), ge(-1,-2,0,F(227,200))]
def solve3(rows):
    A=[[r[0],r[1],r[2],-r[3]] for r in rows]
    n=3
    for i in range(n):
        p=next((k for k in range(i,n) if A[k][i]!=0),None)
        if p is None: return None
        A[i],A[p]=A[p],A[i]
        for k in range(n):
            if k!=i and A[k][i]!=0:
                f=A[k][i]/A[i][i]; A[k]=[A[k][j]-f*A[i][j] for j in range(4)]
    return tuple(A[i][3]/A[i][i] for i in range(n))
def verts(cons):
    V=set()
    for tri in combinations(cons,3):
        p=solve3(tri)
        if p is None: continue
        if all(c[0]*p[0]+c[1]*p[1]+c[2]*p[2]+c[3]>=0 for c in cons): V.add(p)
    return V
def pos(v): return v if v>0 else F(0)
# Lemma hypotheses at r=1,T=b; x,y,z are ROLE sizes
def L32(x,y,z):
    S=x+y+z; return [b-S, b-(1-x+z), b-(1-y+z), b-(1-x+y/2), b-(1-y+x/2), 3*b-(1+2*x+2*y+z)]
def L33(x,y,z):
    S=x+y+z; return [1-b, b-S, b-(F(1,2)+y), 2*b-(1+2*x-y+z), 3*b-(1+2*x+y+3*z)]
def L34(x,y,z):
    S=x+y+z; return [1-b, b-(x+y), b-(F(1,2)+x), b-(F(1,2)+y), b-(1+x-y-z), b-(1-x+y-z),
                     b-(1-S/3), 5*b-(3+S), 3*b-(1+x+y+2*z), 4*b-(2+3*z)]
def L36(x,y,z):
    P=pos(1+y-x-z-b); Q=pos(1+x-y-z-b)
    return [b-x, b-y, b-(1-x+z)-P-Q, b-(y+z)-Q, 2*b-(1+y+2*z)-P-2*Q]
def L35(x,y,z,x1,y1,z1):
    return [x1,x-x1,y1,y-y1,z1,z-z1,b-(x1+y1+z1),(y1+z1)-(1+x-b),(x1+z1)-(1+y-b),(x1+y1)-(1+z-b)]
def splitA(m,y,z): return ((e+y+z-m)/2,(e+m+z-y)/2,(e+m+y-z)/2)
def splitB(m,y,z): return (e+y-z, e+m-z, z)
# case constraints (closures). u=m+y, d=m-y
notA=[ge(1,0,0,-F(119,400))]
Bc=[ge(0,-1,0,F(73,200))]; Cc=[ge(0,1,0,-F(73,200))]
b2=[ge(-1,1,-1,e)]            # y-z >= m-e (closure of >)
nb2=[ge(1,-1,1,-e)]           # y-z <= m-e
b3=[ge(-1,-1,-1,F(81,200))]   # S <= 81/200
nb3=[ge(1,1,1,-F(81,200))]
c1=[ge(-2,-2,-1,F(319,200))]; nc1=[ge(2,2,1,-F(319,200))]
c2=[ge(-1,1,-1,e)]            # z <= e-d = e-m+y
nc2=[ge(1,-1,1,-e)]
c3=[ge(0,-F(1,2),-1,F(73,200))]; nc3=[ge(0,F(1,2),1,-F(73,200))]
A4=[ge(-1,-1,3,-e)]; B4=[ge(1,1,-3,e)]
cases={
 'a':  (base+[ge(-1,0,0,F(119,400))], None),
 'b2': (base+notA+Bc+b2, lambda m,y,z: L33(m,y,z)),
 'b3': (base+notA+Bc+nb2+b3, lambda m,y,z: L33(z,y,m)),
 'b1': (base+notA+Bc+nb2+nb3, lambda m,y,z: L34(z,y,m)),
 'c1': (base+Cc+c1, lambda m,y,z: L32(m,y,z)),
 'c2': (base+Cc+nc1+c2, lambda m,y,z: L36(y,m,z)),
 'c3': (base+Cc+nc1+nc2+c3, lambda m,y,z: L36(m,y,z)),
 'c4A':(base+Cc+nc1+nc2+nc3+A4, lambda m,y,z: L35(m,y,z,*splitA(m,y,z))),
 'c4B':(base+Cc+nc1+nc2+nc3+B4, lambda m,y,z: L35(m,y,z,*splitB(m,y,z))),
}
ok=True
for name,(cons,f) in cases.items():
    V=verts(cons)
    if name=='a':
        for (m,y,z) in V:
            Bv=max((3+m)/4,(2+2*m)/3)
            if Bv>b or m>F(1,2): ok=False; print('FAIL a',m,y,z)
        print(name,len(V),'verts ok'); continue
    bad=[(v,i,val) for v in V for i,val in enumerate(f(*v)) if val<0]
    print(name,len(V),'verts', 'FAIL '+str(bad[:3]) if bad else 'ok',
          'min slack',min(min(f(*v)) for v in V))
    ok&=not bad
# exhaustiveness sanity on a fine rational grid of the base region
import random
random.seed(1)
def cls(m,y,z):
    u=m+y; d=m-y; S=m+y+z
    if m<=F(119,400): return 'a'
    if y<=F(73,200):
        if y-z>m-e: return 'b2'
        if S<F(81,200): return 'b3'
        return 'b1'
    if z<=F(319,200)-2*u: return 'c1'
    if z<e-d: return 'c2'
    if z<=(F(146,200)-y)/2: return 'c3'
    return 'c4A' if 3*z>=e+u else 'c4B'
cnt={}
N=0
while N<200000:
    m=F(random.randint(0,4600),10000); y=F(random.randint(0,4600),10000); z=F(random.randint(0,4600),10000)
    if not(z<=y<=m and m+2*y<=F(227,200)): continue
    N+=1; c=cls(m,y,z); cnt[c]=cnt.get(c,0)+1
    if c!='a':
        f=cases[c][1]
        if min(f(m,y,z))<0: ok=False; print('RANDOM FAIL',c,m,y,z)
    else:
        if max((3+m)/4,(2+2*m)/3)>b: ok=False; print('RANDOM FAIL a')
print(cnt); print('ALL PASS' if ok else 'SOME FAIL')
