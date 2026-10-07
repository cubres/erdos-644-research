import sys; sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from adv_req2 import *
# minimiser-only, force single-class minimisers
rng=np.random.default_rng(int(sys.argv[1])); NR=int(sys.argv[2]); ITS=int(sys.argv[3]); bal=sys.argv[4]!='unbal'
def build(st):
    x,sg=base_decode(st['z'])
    if base_pen(x,sg,bal)>0: return None
    T=[]
    for i in range(3):
        pp=tuple(1 if l==i else 0 for l in range(3))
        t=mktype(x,sg,np.zeros(3),pp,st['f'][i],fixed=(i,sg[i]))
        if t is None: return None
        T.append(t)
    return x,sg,np.array(T)
def score(st):
    b=build(st)
    if b is None: return 99,None
    x,sg,T=b; fm,fa=fano_marg(x,T); pm,pa=pair_marg(x,T)
    return max(fm,pm),(x,sg,T,fm,fa,pm,pa)
for rs in range(NR):
    for tries in range(100000):
        st={'z':np.concatenate([rng.uniform(0.01,1.5,3),rng.uniform(0,1,3)]),'f':rng.uniform(0,1,(3,3))}
        s,info=score(st)
        if s<99: break
    step=0.2
    for it in range(ITS):
        st2={'z':st['z']+rng.normal(0,step,6)*(rng.random(6)<0.4),'f':st['f']+rng.normal(0,step,(3,3))*(rng.random((3,3))<0.3)}
        s2,i2=score(st2)
        if s2<=s: st,s,info=st2,s2,i2
        if it%400==399: step*=0.7
    x,sg,T,fm,fa,pm,pa=info
    print(rs,'score',round(s,4),'x',np.round(x,3),'e',np.round(x-sg,3),'fano',round(fm,4),'pair',round(pm,4),np.round(T,3).tolist(),flush=True)
