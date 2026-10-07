# Exact rational check of the step-1 hand decision procedure (as written in the proof), beta=173/200.
from fractions import Fraction as Fr
import sys, random
b=Fr(173,200); h=Fr(23,50); l=Fr(43,200); H=Fr(1,2)
def L18ok(M): return max((3+M)/4,(2+2*M)/3)<=b
def L31ok(x,y,z):
    S=x+y+z
    return max(x+y,H+x,H+y,1+x-y-z,1-x+y-z,1-S/3,(3+S)/5,(1+x+y+2*z)/3,(2+3*z)/4)<=b and b<=1
def L32ok(x,y,z):
    S=x+y+z; return max(S,H+y,(1+2*x-y+z)/2,(1+2*x+y+3*z)/3)<=b
def L26ok(x,y,z):
    S=x+y+z; return max(S,1-x+z,1-y+z,1-x+y/2,1-y+x/2,(1+2*(x+y)+z)/3)<=b
def P0ok(x,y,z,T=b):
    P=max(0,1+y-x-z-T); Q=max(0,1+x-y-z-T)
    return T>=1-x+z+P+Q and T>=y+z+Q and 2*T>=1+y+2*z+P+2*Q and T>=x and T>=y
def P4split(m,y,z):
    u=m+y
    if z>=(Fr(27,200)+u)/3:
        m1=(Fr(27,200)+y+z-m)/2; y1=(Fr(27,200)+m+z-y)/2; z1=(Fr(27,200)+m+y-z)/2
    else:
        z1=z; y1=Fr(27,200)+m-z; m1=Fr(27,200)+y-z
    ok=(0<=m1<=m and 0<=y1<=y and 0<=z1<=z and m1+y1+z1<=b and y1+z1>=1+m-b and m1+z1>=1+y-b and m1+y1>=1+z-b)
    return ok
def decide(m,y,z):
    S=m+y+z
    if m<=Fr(119,400): return 'a',L18ok(m)
    if y<=Fr(73,200):
        if y-z>m-Fr(27,200): return 'b2',L32ok(m,y,z)
        if S<Fr(81,200): return 'b3',L32ok(z,y,m)
        return 'b1',L31ok(z,y,m)
    u=m+y; d=m-y
    if z<=Fr(319,200)-2*u: return 'c1',L26ok(m,y,z)
    if z<Fr(27,200)-d: return 'c2',P0ok(y,m,z)
    if z<=(Fr(146,200)-y)/2: return 'c3',P0ok(m,y,z)
    return 'c4',(z>=max(Fr(27,200)+d,u-Fr(119,200)) and P4split(m,y,z))
N=int(sys.argv[1]); cnt={}; bad=[]
def region_pts():
    for i in range(N+1):
        m=l+(h-l)*Fr(i,N); w=min(m,1-(b+m)/2)
        for j in range(N+1):
            for k in range(j+1):
                yield m,w*Fr(j,N),w*Fr(k,N)
    random.seed(7)
    for _ in range(200000):
        m=l+(h-l)*Fr(random.randint(0,10**6),10**6); w=min(m,1-(b+m)/2)
        y=w*Fr(random.randint(0,10**6),10**6); z=y*Fr(random.randint(0,10**6),10**6)
        yield m,y,z
for m,y,z in region_pts():
    c,ok=decide(m,y,z); cnt[c]=cnt.get(c,0)+1
    if not ok: bad.append((c,float(m),float(y),float(z)))
print(cnt); print('FAIL',len(bad),bad[:5])
