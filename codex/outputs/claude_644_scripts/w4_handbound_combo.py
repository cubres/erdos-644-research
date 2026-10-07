import sys, time
from w4_handbound_explore import *
from w4_handbound_static import triple
beta=float(sys.argv[1]); names=sys.argv[2].split(','); N=int(sys.argv[3])
lo=(3*beta-2)/2
worst=[]
for i in range(N+1):
    m=lo+(0.5-lo)*i/N
    w=min(m,1-(beta+m)/2)
    for j in range(N+1):
        for k in range(j+1):
            y=w*j/N; z=w*k/N
            v,a=best(m,y,z,m,beta,names)
            if v>beta:
                s,_=triple(m,y,z)
                if s>beta: worst.append((round(m,4),round(y,4),round(z,4),round(v,4),a,round(s,4)))
print(len(worst))
for w_ in worst: print(w_)
