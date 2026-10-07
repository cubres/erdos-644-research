"""Bounded lexicographic discovery at a maximum-imbalance triple.

Target v=(1/8,1/8,3/8-M,3/8-M), t=M. Exactly one retained old pair
has extremal allowed correlation h=M-1/4; it alone contributes the entire
old minority variance. A replacement retaining that pair cannot improve
the variance. We test whether the other two replacements can both have
strictly smaller imbalance, which also evades the lexicographic test.
Numerical LP results are discovery only.
"""
from itertools import product
import numpy as np
from scipy.optimize import linprog
from p644_agent_alternative_core_gap import state, vertices, ROWS, OPPOSITE
import json


def response(w,u,M,T=.75):
    u=np.clip(u,0,w)
    a=OPPOSITE@w/2
    strict=np.array([abs(z-.5)<1e-8 for z in a],float)
    A=np.r_[np.c_[OPPOSITE,strict],np.c_[-OPPOSITE,strict]]
    rhs=np.r_[a+M,M-a]
    bands=[(0,M),(T-M,1-T+M),(1-M,1)]
    lower=ROWS@u;upper=np.minimum(ROWS@w,lower+1-T)
    allowed=[[j for j,(lo,hi) in enumerate(bands)
              if lo<=upper[i]+1e-9 and hi>=lower[i]-1e-9] for i in range(3)]
    best=None
    for modes in product(*allowed):
        lo=[bands[j][0] for j in modes];hi=[bands[j][1] for j in modes]
        r=linprog(np.r_[np.zeros(8),-1],
                  A_ub=np.r_[A,np.c_[ROWS,np.zeros(3)],np.c_[-ROWS,np.zeros(3)]],
                  b_ub=np.r_[rhs,hi,-np.array(lo)],A_eq=[np.r_[np.ones(8),0]],b_eq=[1],
                  bounds=list(zip(u,w))+[(0,M)],method='highs')
        if r.success and (best is None or r.x[-1]>best['slack']):
            best={'slack':float(r.x[-1]),'g':r.x[:8].tolist(),'modes':modes}
        elif not r.success and r.status!=2:raise RuntimeError(r.message)
    return best


def check(M=.32,random=200):
    v=[.125,.125,.375-M,.375-M];w=state(v,M)
    menu=list(vertices(w));rng=np.random.default_rng(644)
    for _ in range(random):
        ids=rng.integers(len(menu),size=3)
        menu.append(np.clip(rng.dirichlet(np.ones(3))@np.array([menu[j] for j in ids]),0,w))
    worst=None
    for count,u in enumerate(menu,1):
        r=response(w,u,M)
        if r is None:return {'M':M,'count':count,'bad':u.tolist()}
        if worst is None or r['slack']<worst['response']['slack']:
            worst={'u':u.tolist(),'response':r}
    return {'M':M,'count':len(menu),'worst':worst}


if __name__=='__main__':
    print(json.dumps(check()),flush=True)
