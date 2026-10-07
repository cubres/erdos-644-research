import sys
from fractions import Fraction as Fr
beta=Fr(173,200); h=Fr(23,50); l=2-beta-2*h; half=Fr(1,2)
def mx(*a): return max(a)
def L18(m): return mx((3+m)/4,(2+2*m)/3)
def L31o(a,b,c): S=a+b+c; return mx(a+b,half+a,half+b,1+a-b-c,1-a+b-c,1-S/3,(3+S)/5,(1+a+b+2*c)/3,(2+3*c)/4)
def L32o(a,b,c): S=a+b+c; return mx(S,half+b,(1+2*a-b+c)/2,(1+2*a+b+3*c)/3)
def L26o(a,b,c): S=a+b+c; return mx(S,1-a+c,1-b+c,1-a+b/2,1-b+a/2,(1+2*(a+b)+c)/3)
def P4c(x,y,z):
    S=x+y+z
    return mx((3+S)/5,(1+x)/2,(1+y)/2,(1+z)/2,1+x-y-z,1+y-x-z,1+z-x-y,(2+x+y-z)/3,(2+x+z-y)/3,(2+y+z-x)/3)
def P0ok(x,y,z,T):
    P=max(0,1+y-x-z-T); Q=max(0,1+x-y-z-T)
    return T>=1-x+z+P+Q and T>=y+z+Q and 2*T>=1+y+2*z+P+2*Q and T>=x and T>=y
N=int(sys.argv[1])
fails=[];stats={}
for i in range(N+1):
    m=l+(h-l)*Fr(i,N)
    w=min(m,1-(beta+m)/2)
    for j in range(N+1):
        for k in range(j+1):
            y=w*Fr(j,N); z=w*Fr(k,N)
            if m<=(3*beta-2)/2:
                t='L18' if L18(m)<=beta else None
            elif y<=beta-half:
                t=('L31zym' if L31o(z,y,m)<=beta else 'L32myz' if L32o(m,y,z)<=beta else 'L32zym' if L32o(z,y,m)<=beta else None)
            else:
                t=('L26' if L26o(m,y,z)<=beta else 'P0' if P0ok(y,m,z,beta) else 'P4' if P4c(m,y,z)<=beta else None)
            stats[t]=stats.get(t,0)+1
            if t is None: fails.append((float(m),float(y),float(z)))
print(stats); print(fails[:10])
