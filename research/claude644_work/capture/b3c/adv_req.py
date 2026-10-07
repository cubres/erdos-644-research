import sys; sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from advlib import *
rng=np.random.default_rng(int(sys.argv[1])); NR=int(sys.argv[2]); ITS=int(sys.argv[3]) if len(sys.argv)>3 else 2500
strategy=sys.argv[4] if len(sys.argv)>4 else 'S6'
def requests(x,sg,M):
    e=x-sg; W=[]
    if strategy in ('S6','S3'):
        for j in range(3):
            for i in range(3):
                if i==j: continue
                if strategy=='S3' and i!=(j+1)%3: continue
                w=np.zeros(3); w[j]=e[j]; w[i]=0.75-e[j]; W.append(w)
    return W
def evaluate(z,verbose=False):
    x,sg=base_decode(z); p=base_pen(x,sg)
    T=[]; off=6
    for i in range(3):
        v=z[off:off+3]; off+=3; t=type_from(v,x); 
        # minimiser: force t_i=sg_i by penalty
        p+=abs(t[i]-sg[i]); p+=np.maximum(0,t-x).sum(); p+=class_pen(t,x,sg)
        T.append(t)
    for w in requests(x,sg,T):
        v=z[off:off+3]; off+=3; t=type_from(v,x)
        p+=np.maximum(0,t-(x-w)).sum(); p+=class_pen(t,x,sg); T.append(t)
    if p>1e-9: return 10+p, None
    T=np.array(T); fm,fa=fano_marg(x,T); pm,pa=pair_marg(x,T)
    if verbose: return max(fm,pm),(x,sg,T,fm,fa,pm,pa)
    return max(fm,pm), None
nvar=6+3*3+3*len(requests(np.ones(3),np.ones(3)*0.6,None))
for rs in range(NR):
    z=np.concatenate([rng.uniform(0.2,1.5,3),rng.uniform(0,1,3),rng.uniform(0,1,nvar-6)])
    s,_=evaluate(z); step=0.3
    for it in range(ITS):
        z2=z+rng.normal(0,step,nvar)*(rng.random(nvar)<0.3)
        s2,_=evaluate(z2)
        if s2<=s: z,s=z2,s2
        if it%400==399: step*=0.7
    s,info=evaluate(z,True)
    if info:
        x,sg,T,fm,fa,pm,pa=info
        print(rs,'score',round(s,4),'x',np.round(x,3),'e',np.round(x-sg,3),'fano',round(fm,4),'pair',round(pm,4),flush=True)
        print('   T',np.round(T,3).tolist(),flush=True)
    else: print(rs,'infeasible',round(s,3),flush=True)
