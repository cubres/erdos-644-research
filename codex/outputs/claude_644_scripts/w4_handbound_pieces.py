import sys, itertools
from fractions import Fraction as Fr
beta=Fr(173,200); h=Fr(23,50); l=2-beta-2*h
def L31o(a,b,c): S=a+b+c; return max(a+b,Fr(1,2)+a,Fr(1,2)+b,1+a-b-c,1-a+b-c,1-S/3,(3+S)/5,(1+a+b+2*c)/3,(2+3*c)/4)
def L32o(a,b,c): S=a+b+c; return max(S,Fr(1,2)+b,(1+2*a-b+c)/2,(1+2*a+b+3*c)/3)
def L26o(a,b,c): S=a+b+c; return max(S,1-a+c,1-b+c,1-a+b/2,1-b+a/2,(1+2*(a+b)+c)/3)
N=int(sys.argv[1])
lo=(3*beta-2)/2
unc=[]
for i in range(N+1):
    m=lo+(h-lo)*Fr(i,N)
    w=min(m,1-(beta+m)/2)
    for j in range(N+1):
        for k in range(j+1):
            y=w*Fr(j,N); z=w*Fr(k,N)
            if y>beta-Fr(1,2): continue   # spot A handled separately
            if L31o(z,y,m)<=beta or L32o(m,y,z)<=beta: continue
            unc.append((float(m),float(y),float(z)))
print(len(unc))
for u in unc: print(tuple(round(t,4) for t in u), 'S',round(sum(u),4))
