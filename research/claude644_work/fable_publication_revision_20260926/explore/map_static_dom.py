import numpy as np, sys
from oracle import triple_static
from lemmas import ALL
t=6/7
dom = sys.argv[1]
N=10
if dom=='s1': xs=np.linspace(3/7+1e-6,10/21,4); ym=5/14
if dom=='s2': xs=np.linspace(4/21,5/14,4); ym=3/7
if dom=='s3': xs=np.linspace(10/21,1/2,3); ym=4/21-1e-6
if dom=='fin': xs=[3/7,0.4,0.35,0.3]; ym=None
for x in xs:
    print('x=%.4f'%x)
    yM = ym if ym is not None else x
    for y in np.linspace(0,yM,N+1):
        line=[]
        for z in np.linspace(0,yM,N+1):
            if z>y+1e-12: continue
            st=triple_static(x,y,z)
            f={k:ALL[k](x,y,z) for k in ALL}
            b=min(f,key=f.get)
            line.append('%.3f%s%s'%(st,'s' if st<=t+1e-9 else ' ', b[:2] if f[b]<=t+1e-9 else '--'))
        print(' y=%.3f '%y+' '.join(line),flush=True)
