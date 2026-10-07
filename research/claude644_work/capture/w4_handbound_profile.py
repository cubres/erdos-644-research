import sys
from w4_handbound_explore import *
ALL=['L18','L29','L33','L26','L20','L23','L25','L31','L32','GT']
def worst_q(q,beta,u,v,names=ALL,N=50,excl=None):
    worst=(0,None)
    for j in range(N+1):
        for k in range(N+1):
            y=u*j/N; z=v*k/N
            if excl and (excl(y) or excl(z)): continue
            vv,a=best(q,y,z,None,beta,names)
            if vv>worst[0]: worst=(vv,(round(y,3),round(z,3),a))
    return worst
beta=float(sys.argv[1])
for i in range(0,26):
    q=0.0+0.02*i
    s=2-beta-q
    # best cap split
    res=[]
    for t in range(0,11):
        u=s*t/20; v=s-u
        if u>1-q or v>1-q: continue
        res.append((worst_q(q,beta,u,v,N=24),round(u,3),round(v,3)))
    res.sort(key=lambda r:r[0][0])
    print(round(q,3),res[0])
