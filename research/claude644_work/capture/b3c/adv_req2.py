import sys; sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from advlib import *
import itertools
PATS=[p for p in itertools.product([0,1],repeat=3) if any(p)]
def fill(lo,hi,f):
    if lo.sum()>1+1e-12 or hi.sum()<1-1e-12: return None
    f=0.05+np.abs(f)
    a,b=0.0,10.0
    for _ in range(60):
        mu=(a+b)/2; t=np.clip(lo+mu*f,lo,hi)
        if t.sum()<1: a=mu
        else: b=mu
    t=np.clip(lo+b*f,lo,hi); return t
def mktype(x,sg,w,pat,f,fixed=None):
    lo=np.zeros(3); hi=np.minimum(x, x-w)
    for l in range(3):
        if pat[l]: lo[l]=sg[l]
        else: hi[l]=min(hi[l],2*x[l]/3)
    if fixed is not None:
        i,v=fixed; lo[i]=hi[i]=v if (lo[i]<=v+1e-12 and v<=hi[i]+1e-12) else np.nan
        if np.isnan(lo[i]): return None
    if (lo>hi+1e-12).any(): return None
    return fill(lo,hi,f)
def requests(x,sg,M,strategy):
    e=x-sg; W=[]
    if strategy in ('S6','S3'):
        for j in range(3):
            for i in range(3):
                if i==j: continue
                if strategy=='S3' and i!=(j+1)%3: continue
                w=np.zeros(3); w[j]=e[j]; w[i]=0.75-e[j]; W.append(w)
    return W
class Adv:
    def __init__(s,strategy,balanced=True): s.st=strategy; s.bal=balanced
    def build(s,st):
        x,sg=base_decode(st['z'])
        if base_pen(x,sg,s.bal)>0: return None
        T=[]
        for i in range(3):
            k0=PATS.index(st['pat'][i]); t=None
            for dk in range(7):
                pp=PATS[(k0+dk)%7]
                if not pp[i]: continue
                t=mktype(x,sg,np.zeros(3),pp,st['f'][i],fixed=(i,sg[i]))
                if t is not None: break
            if t is None: return None
            T.append(t)
        for r,w in enumerate(requests(x,sg,T,s.st)):
            k0=PATS.index(st['pat'][3+r]); t=None
            for dk in range(7):
                t=mktype(x,sg,w,PATS[(k0+dk)%7],st['f'][3+r])
                if t is not None: break
            if t is None: return None
            T.append(t)
        return x,sg,np.array(T)
    def score(s,st):
        b=s.build(st)
        if b is None: return 99,None
        x,sg,T=b; fm,fa=fano_marg(x,T); pm,pa=pair_marg(x,T)
        return max(fm,pm),(x,sg,T,fm,fa,pm,pa)
def run(seed,NR,ITS,strategy,bal=True):
    rng=np.random.default_rng(seed); A=Adv(strategy,bal)
    nt=3+len(requests(np.ones(3),np.ones(3)*.7,None,strategy))
    res=[]
    for rs in range(NR):
        for tries in range(20000):
            st={'z':np.concatenate([rng.uniform(0.01,1.5,3),rng.uniform(0,1,3)]),
                'pat':[PATS[rng.integers(7)] for _ in range(nt)],'f':rng.uniform(0,1,(nt,3))}
            for i in range(3):
                p=list(st['pat'][i]); p[i]=1; st['pat'][i]=tuple(p)
            s,info=A.score(st)
            if s<99: break
        else:
            print(rs,'no feasible start',flush=True); continue
        step=0.2
        for it in range(ITS):
            st2={'z':st['z']+rng.normal(0,step,6)*(rng.random(6)<0.4),'pat':list(st['pat']),'f':st['f']+rng.normal(0,step,(nt,3))*(rng.random((nt,3))<0.3)}
            if rng.random()<0.05:
                k=rng.integers(3,nt) if nt>3 else 0
                if k>=3: st2['pat'][k]=PATS[rng.integers(7)]
            s2,i2=A.score(st2)
            if s2<=s: st,s,info=st2,s2,i2
            if it%400==399: step*=0.7
        x,sg,T,fm,fa,pm,pa=info
        print(rs,'score',round(s,4),'x',np.round(x,3),'e',np.round(x-sg,3),'fano',round(fm,4),'pair',round(pm,4),flush=True)
        print('   T',np.round(T,3).tolist(),flush=True)
        res.append((s,info))
    return res
if __name__=='__main__':
    run(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),sys.argv[4], sys.argv[5]!='unbal' if len(sys.argv)>5 else True)
