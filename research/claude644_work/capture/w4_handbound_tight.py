import sys
from w4_handbound_explore import *
beta=float(sys.argv[1]); names=sys.argv[2].split(','); thr=float(sys.argv[3]); N=int(sys.argv[4])
lo=(3*beta-2)/2
for i in range(N+1):
    m=lo+(0.5-lo)*i/N
    w=min(m,1-(beta+m)/2)
    for j in range(N+1):
        for k in range(j+1):
            y=w*j/N; z=w*k/N
            v,a=best(m,y,z,m,beta,names)
            if v>=thr: 
                # also per-lemma values
                vals={n:(round(LEM[n](m,y,z,m) if n in('L35','L15','L26') else (L37(m,y,z,m,beta) if n=='L37' else LEM[n](m,y,z)),4)) for n in names}
                print(round(m,4),round(y,4),round(z,4),round(v,4),a,vals)
