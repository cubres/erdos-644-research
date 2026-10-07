import sys, itertools
from w4_handbound_explore import perms
beta=float(sys.argv[1]); h=float(sys.argv[2]); N=int(sys.argv[3])
def L32o(a,b,c): S=a+b+c; return max(S,.5+b,(1+2*a-b+c)/2,(1+2*a+b+3*c)/3)
def L31o(a,b,c): S=a+b+c; return max(a+b,.5+a,.5+b,1+a-b-c,1-a+b-c,1-S/3,(3+S)/5,(1+a+b+2*c)/3,(2+3*c)/4)
lo=(3*beta-2)/2
bad=[]; used=set()
for i in range(N+1):
    m=lo+(h-lo)*i/N
    w=min(m,1-(beta+m)/2)
    for j in range(N+1):
        for k in range(j+1):
            y=w*j/N; z=w*k/N
            S=m+y+z
            f=L32o if S<=beta else L31o
            best=min((f(*p),p) for p in [(m,y,z),(m,z,y),(y,m,z),(z,m,y),(y,z,m),(z,y,m)])
            # record orientation role of m
            if best[0]>beta+1e-12: bad.append((round(m,3),round(y,3),round(z,3),round(best[0],4),'L32' if S<=beta else 'L31'))
            else:
                p=best[1]; used.add(('L32' if S<=beta else 'L31', p.index(m) if p.count(m)==1 else 'tie'))
print(len(bad),bad[:10]); print(used)
