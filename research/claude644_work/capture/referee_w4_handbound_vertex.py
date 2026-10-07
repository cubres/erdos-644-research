# Referee: exact vertex-enumeration proof of the Prop 10 case cover (independent of the author's grid).
# Every sufficient condition used is a convex piecewise-linear function <= beta (L18,L26,L31,L32,P0),
# or (P4 with the explicit split) linear on each split branch; so checking the vertices of each
# closed case polytope (and each split-branch polytope) is an exact proof of coverage.
from fractions import Fraction as Fr
from itertools import combinations
b=Fr(173,200); H=Fr(1,2)
def solve3(A,B):
    import copy
    M=[list(A[i])+[B[i]] for i in range(3)]
    for c in range(3):
        p=next((r for r in range(c,3) if M[r][c]!=0),None)
        if p is None: return None
        M[c],M[p]=M[p],M[c]
        for r in range(3):
            if r!=c and M[r][c]!=0:
                f=M[r][c]/M[c][c]; M[r]=[M[r][k]-f*M[c][k] for k in range(4)]
    return tuple(M[i][3]/M[i][i] for i in range(3))
def vertices(cons):
    V=set()
    for tri in combinations(cons,3):
        s=solve3([t[:3] for t in tri],[t[3] for t in tri])
        if s is None: continue
        if all(a*s[0]+bb*s[1]+c*s[2]<=d for a,bb,c,d in cons): V.add(s)
    return V
# base region: coordinates (m,y,z); constraint a*m+b*y+c*z <= d
base=[(0,0,-1,0),(0,-1,1,0),(-1,1,0,0),(1,0,0,Fr(23,50)),(1,2,0,Fr(227,200))]
def L18(m,y,z): return max((3+m)/4,(2+2*m)/3)
def L31(x,y,z):
    S=x+y+z; return max(x+y,H+x,H+y,1+x-y-z,1-x+y-z,1-S/3,(3+S)/5,(1+x+y+2*z)/3,(2+3*z)/4)
def L32(x,y,z):
    S=x+y+z; return max(S,H+y,(1+2*x-y+z)/2,(1+2*x+y+3*z)/3)
def L26(x,y,z):
    S=x+y+z; return max(S,1-x+z,1-y+z,1-x+y/2,1-y+x/2,(1+2*(x+y)+z)/3)
def P0need(x,y,z,T=b):
    P=max(0,1+y-x-z-T); Q=max(0,1+x-y-z-T)
    return T>=1-x+z+P+Q and T>=y+z+Q and 2*T>=1+y+2*z+P+2*Q and T>=x and T>=y
def P4feas(m,y,z,m1,y1,z1):
    return (0<=m1<=m and 0<=y1<=y and 0<=z1<=z and m1+y1+z1<=b and y1+z1>=1+m-b and m1+z1>=1+y-b and m1+y1>=1+z-b)
c27=Fr(27,200)
cases={
 'a':  base+[(1,0,0,Fr(119,400))],
 'b2': base+[(-1,0,0,-Fr(119,400)),(0,1,0,Fr(73,200)),(1,-1,1,c27)],            # y-z>=m-27/200
 'b3': base+[(-1,0,0,-Fr(119,400)),(0,1,0,Fr(73,200)),(-1,1,-1,-c27),(1,1,1,Fr(81,200))],
 'b1': base+[(-1,0,0,-Fr(119,400)),(0,1,0,Fr(73,200)),(-1,1,-1,-c27),(-1,-1,-1,-Fr(81,200))],
 'c1': base+[(0,-1,0,-Fr(73,200)),(2,2,1,Fr(319,200))],
 'c2': base+[(0,-1,0,-Fr(73,200)),(-2,-2,-1,-Fr(319,200)),(1,-1,1,c27)],         # z<=27/200-(m-y)
 'c3': base+[(0,-1,0,-Fr(73,200)),(-2,-2,-1,-Fr(319,200)),(-1,1,-1,-c27),(0,1,2,Fr(146,200))],
 'c4': base+[(0,-1,0,-Fr(73,200)),(-2,-2,-1,-Fr(319,200)),(-1,1,-1,-c27),(0,-1,-2,-Fr(146,200))],
}
test={'a':lambda m,y,z:L18(m,y,z)<=b,'b2':lambda m,y,z:L32(m,y,z)<=b,'b3':lambda m,y,z:L32(z,y,m)<=b,
      'b1':lambda m,y,z:L31(z,y,m)<=b,'c1':lambda m,y,z:L26(m,y,z)<=b,'c2':lambda m,y,z:P0need(y,m,z),
      'c3':lambda m,y,z:P0need(m,y,z)}
allok=True
for k,cons in cases.items():
    V=vertices(cons)
    if k=='c4':
        # branch A: z >= (27/200+u)/3  <=> 3z - m - y >= 27/200
        for name,extra in [('A',[(1,1,-3,-c27)]),('B',[(-1,-1,3,c27)])]:
            VV=vertices(cons+extra); bad=[]
            for (m,y,z) in VV:
                u=m+y
                if name=='A':
                    m1=(c27+y+z-m)/2; y1=(c27+m+z-y)/2; z1=(c27+m+y-z)/2
                else:
                    z1=z; y1=c27+m-z; m1=c27+y-z
                if not P4feas(m,y,z,m1,y1,z1): bad.append((m,y,z,m1,y1,z1))
            print('c4',name,len(VV),'vertices; bad',len(bad),[tuple(map(str,t)) for t in bad[:3]]); allok&=not bad
    else:
        bad=[v for v in V if not test[k](*v)]
        print(k,len(V),'vertices; bad',len(bad),[tuple(map(str,t)) for t in bad[:3]]); allok&=not bad
# covering: every base point lies in some case closure (by construction of the if-chain) -- check a random sample
import random
random.seed(1)
def incase(p,cons): return all(a*p[0]+bb*p[1]+c*p[2]<=d for a,bb,c,d in cons)
miss=0
for _ in range(100000):
    m=Fr(random.randint(0,46000),100000); y=m*Fr(random.randint(0,10**5),10**5); z=y*Fr(random.randint(0,10**5),10**5)
    if not incase((m,y,z),base): continue
    if not any(incase((m,y,z),c) for c in cases.values()): miss+=1
print('uncovered sample points',miss)
print('ALL OK' if allok else 'FAILURES')
