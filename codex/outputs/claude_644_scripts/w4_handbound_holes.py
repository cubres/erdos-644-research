import sys
from w4_handbound_explore import *
beta=float(sys.argv[1]); names=sys.argv[2].split(',')
N=int(sys.argv[3]) if len(sys.argv)>3 else 40
lo=(3*beta-2)/2
holes=[]
for i in range(N+1):
    m=lo+(0.5-lo)*i/N
    w=min(m,1-(beta+m)/2)
    for j in range(N+1):
        for k in range(j+1):
            y=w*j/N; z=w*k/N
            v,a=best(m,y,z,m,beta,names)
            if v>beta+1e-12: holes.append((round(m,3),round(y,3),round(z,3),round(v,4),a))
print(len(holes))
import collections
byM=collections.defaultdict(list)
for h in holes: byM[h[0]].append(h)
for mm in sorted(byM):
    hs=byM[mm]
    ys=[h[1] for h in hs]; zs=[h[2] for h in hs]
    print(mm,len(hs),'y',min(ys),max(ys),'z',min(zs),max(zs),'worst',max(h[3] for h in hs))
