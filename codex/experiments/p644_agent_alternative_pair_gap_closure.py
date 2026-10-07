"""Discovery-only propagation of a global pair-overlap restriction.

An actual pair of half-cuts with overlap a has four quadrant masses
(a,1-a,1-a,a). Every prescribed .75-set must extend to an actual half-cut,
whose two new overlaps obey the same global allowed intervals and whose
triple imbalance is at most M. Failure eliminates a globally. Passing a
finite request sample does not prove full containment cofinality.
"""
from itertools import product
import numpy as np
from scipy.optimize import linprog
import json

ROWS = np.array([[0,0,1,1], [0,1,0,1]], float)
DIAG = np.array([1,0,0,1], float)


def response(a, u, M, bands, T=.75):
    w=np.array([a,1-a,1-a,a])
    u=np.clip(u,0,w)
    lower=ROWS@u
    upper=np.minimum(ROWS@w,lower+1-T)
    choices=[[i for i,(lo,hi) in enumerate(bands)
              if lo<=upper[j]+1e-9 and hi>=lower[j]-1e-9] for j in range(2)]
    for modes in product(*choices):
        lo=[bands[i][0] for i in modes]
        hi=[bands[i][1] for i in modes]
        r=linprog(np.zeros(4),A_ub=np.r_[ROWS,-ROWS,[DIAG],[-DIAG]],
                  b_ub=np.r_[hi,-np.array(lo),a+M,M-a],A_eq=[[1]*4],b_eq=[1],
                  bounds=list(zip(u,w)),method='highs')
        if r.success:return r.x
        if r.status!=2:raise RuntimeError(r.message)
    return None


def requests(w,T=.75,random=100,seed=44):
    seen={}
    for bits in product((0,1),repeat=4):
        u=w*bits
        for j in range(4):
            z=u.copy();z[j]=T-sum(z[i] for i in range(4) if i!=j)
            if z[j]<-1e-8 or z[j]>w[j]+1e-8:continue
            z=np.clip(z,0,w);key=tuple(np.round(z,10))
            if key not in seen:seen[key]=z.copy();yield z
    rng=np.random.default_rng(seed)
    for _ in range(random):
        # Mixtures of legal box-simplex vertices sample genuine interior requests.
        vs=list(seen.values());ids=rng.integers(len(vs),size=4)
        yield np.clip(rng.dirichlet(np.ones(4))@np.array([vs[i] for i in ids]),0,w)


def check(a,M,bands=None,random=100):
    if bands is None:bands=[(0,M),(.75-M,.25+M),(1-M,1)]
    count=0
    for u in requests(np.array([a,1-a,1-a,a]),random=random):
        count+=1
        if response(a,u,M,bands) is None:
            return {'M':M,'a':a,'count':count,'bad':u.tolist()}
    return {'M':M,'a':a,'count':count,'bad':None}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--M',type=float,default=.3)
    p.add_argument('--random',type=int,default=100)
    args=p.parse_args()
    for a in np.r_[np.linspace(0,args.M,7),np.linspace(.75-args.M,.5,7)]:
        print(json.dumps(check(a,args.M,random=args.random)),flush=True)
