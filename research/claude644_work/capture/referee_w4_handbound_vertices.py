# Referee: independent EXACT vertex-enumeration check of Proposition 10 (handbound), r=1, T=beta.
# Every case region is a polytope in (m,y,z); every lemma condition is "convex piecewise-linear <= const"
# (or linear >= const for split lower bounds), so checking all vertices of the closure is a proof.
from fractions import Fraction as F
from itertools import combinations
b=F(173,200); e=1-b
def solve3(A,B):
    # Cramer
    def det(M): return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
    D=det(A)
    if D==0: return None
    out=[]
    for i in range(3):
        M=[row[:] for row in A]
        for j in range(3): M[j][i]=B[j]
        out.append(det(M)/D)
    return out
def verts(cons):
    V=set()
    for c3 in combinations(cons,3):
        s=solve3([list(c[0]) for c in c3],[c[1] for c in c3])
        if s is None: continue
        if all(sum(a*x for a,x in zip(c[0],s))<=c[1] for c in cons): V.add(tuple(s))
    return V
# constraint a.(m,y,z) <= rhs
base=[((0,0,-1),0),((0,-1,1),0),((-1,1,0),0),((1,0,0),F(23,50)),((1,2,0),2-b)]
def L1(m,y,z): return max((3+m)/4,(2+2*m)/3)<=b
def L2(x,y,z):
    S=x+y+z; return max(S,1-x+z,1-y+z,1-x+y/2,1-y+x/2,(1+2*x+2*y+z)/3)<=b
def L3(x,y,z):
    S=x+y+z; return max(S,F(1,2)+y,(1+2*x-y+z)/2,(1+2*x+y+3*z)/3)<=b
def L4(x,y,z):
    S=x+y+z
    return max(x+y,F(1,2)+x,F(1,2)+y,1+x-y-z,1-x+y-z,1-S/3,(3+S)/5,(1+x+y+2*z)/3,(2+3*z)/4)<=b
def L6(x,y,z,T=b):
    P=max(0,1+y-x-z-T); Q=max(0,1+x-y-z-T)
    return x<=T and y<=T and T>=1-x+z+P+Q and T>=y+z+Q and 2*T>=1+y+2*z+P+2*Q
def L5(m,y,z,opt):
    u=m+y
    if opt=='A': m1=(e+y+z-m)/2; y1=(e+m+z-y)/2; z1=(e+m+y-z)/2
    else: z1=z; y1=e+m-z; m1=e+y-z
    return (0<=m1<=m and 0<=y1<=y and 0<=z1<=z and m1+y1+z1<=b and y1+z1>=1+m-b and m1+z1>=1+y-b and m1+y1>=1+z-b)
S3=(1,1,1)
cases={
 'a':(base+[((1,0,0),F(119,400))], lambda m,y,z:L1(m,y,z)),
 'b2':(base+[((-1,0,0),-F(119,400)),((0,1,0),F(73,200)),((1,-1,1),e)], lambda m,y,z:L3(m,y,z)),
 'b3':(base+[((-1,0,0),-F(119,400)),((0,1,0),F(73,200)),((-1,1,-1),-e),(S3,F(81,200))], lambda m,y,z:L3(z,y,m)),
 'b1':(base+[((-1,0,0),-F(119,400)),((0,1,0),F(73,200)),((-1,1,-1),-e),((-1,-1,-1),-F(81,200))], lambda m,y,z:L4(z,y,m)),
 'c1':(base+[((0,-1,0),-F(73,200)),((2,2,1),F(319,200))], lambda m,y,z:L2(m,y,z)),
 'c2':(base+[((0,-1,0),-F(73,200)),((-2,-2,-1),-F(319,200)),((1,-1,1),e)], lambda m,y,z:L6(y,m,z)),
 'c3':(base+[((0,-1,0),-F(73,200)),((-2,-2,-1),-F(319,200)),((-1,1,-1),-e),((0,1,2),F(146,200))], lambda m,y,z:L6(m,y,z)),
 'c4A':(base+[((0,-1,0),-F(73,200)),((-2,-2,-1),-F(319,200)),((-1,1,-1),-e),((0,-1,-2),-F(146,200)),((1,1,-3),-e)], lambda m,y,z:L5(m,y,z,'A')),
 'c4B':(base+[((0,-1,0),-F(73,200)),((-2,-2,-1),-F(319,200)),((-1,1,-1),-e),((0,-1,-2),-F(146,200)),((-1,-1,3),e)], lambda m,y,z:L5(m,y,z,'B')),
}
allok=True
for k,(cons,ok) in cases.items():
    V=verts(cons); bad=[v for v in V if not ok(*v)]
    print(k,len(V),'vertices; failures:',[tuple(map(float,v)) for v in bad][:4]); allok&= not bad
# L6 conditions involve max(0,.) -> convex; splits linear; L1-L4 max of linear: convex. Vertex check is exact.
# coverage: union of case closures = region? check random exact points fall in some case (using handbound's order)
import random
random.seed(1); miss=0
for _ in range(200000):
    m=F(random.randint(0,4600),10000); y=m*F(random.randint(0,10**4),10**4); z=y*F(random.randint(0,10**4),10**4)
    if m+2*y>2-b: continue
    inside=False
    for k,(cons,ok) in cases.items():
        if all(sum(a*x for a,x in zip(c[0],(m,y,z)))<=c[1] for c in cons): inside=True;break
    if not inside: miss+=1
print('uncovered random pts',miss); print('ALL VERTEX CHECKS PASS' if allok else 'FAIL')
