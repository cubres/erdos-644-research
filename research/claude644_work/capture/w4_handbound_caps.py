import sys
from w4_handbound_explore import *
beta=float(sys.argv[1]); names=sys.argv[2].split(','); N=int(sys.argv[3]); M=int(sys.argv[4])
lo=(3*beta-2)/2
def vals(cap,m,N):
    # admissible intersection values in [0,cap] given gap (m,1/2]
    out=[cap*j/N for j in range(N+1)]
    return [t for t in out if t<=m or t>0.5]+([m] if m<=cap else [])
tot=0
for i in range(M+1):
    m=lo+(0.5-lo)*i/M
    s=2-beta-m
    best_u=None
    for t in range(0,41):
        u=s*t/80  # u<=v
        v=s-u
        if v>1-m: continue
        worst=0
        for y in vals(u,m,N):
            for z in vals(v,m,N):
                vv,a=best(m,y,z,m,beta,names)
                worst=max(worst,vv)
        if best_u is None or worst<best_u[0]: best_u=(worst,round(u,3),round(v,3))
    print(round(m,4),best_u)
