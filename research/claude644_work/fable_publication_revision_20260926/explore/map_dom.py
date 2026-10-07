import numpy as np, sys
from lemmas import ALL
t=6/7
def run(name, xs, ymax, zmax_fn=None, use=None, N=14):
    use = use or list(ALL)
    fails=0; cnt={}
    for x in xs:
        for y in np.linspace(0,ymax,N+1):
            for z in np.linspace(0,ymax,N+1):
                if z>y: continue
                vals={k:ALL[k](x,y,z) for k in use}
                ok=[k for k in use if vals[k]<=t+1e-9]
                if not ok: fails+=1; 
                for k in ok: cnt[k]=cnt.get(k,0)+1
    print(name,'fails',fails,'counts',cnt)
run('stage1', np.linspace(3/7+1e-6,10/21,6), 5/14)
run('stage1 no-sym-s0', np.linspace(3/7+1e-6,10/21,6), 5/14, use=['s0','sym'])
run('finisher', [3/7,0.4,0.35,0.3], 3/7)
run('finisher s0+sym', [3/7,0.4,0.35,0.3], 3/7, use=['s0','sym'])
run('stage2', np.linspace(4/21,5/14,6), 3/7)
run('stage2 s0+sym', np.linspace(4/21,5/14,6), 3/7, use=['s0','sym'])
run('stage3', np.linspace(10/21,1/2,6), 4/21-1e-6)
run('stage3 nogap all', np.linspace(10/21,1/2,6), 4/21-1e-6)
