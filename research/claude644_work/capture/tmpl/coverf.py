import itertools
import numpy as np
from scipy.optimize import linprog
from lib2 import FUNCS
def tfacets(k):
    out=[]
    for u,v in FUNCS[k-1]:
        out.append(([1,0,-float(u),-float(v)],0.0)); out.append(([0,1,float(u),float(v)],-float(u+v)))
    return out
def maxeps_f(cons, viol, n=4):
    # max eps s.t. cons>=0, f<=-eps ; vars z (n), eps<=1
    A=[];b=[]
    for c,k in cons: A.append([-float(a) for a in c]+[0.0]); b.append(float(k))
    for c,k in viol: A.append([float(a) for a in c]+[1.0]); b.append(-float(k))
    cobj=[0.0]*n+[-1.0]
    r=linprog(cobj,A_ub=A,b_ub=b,bounds=[(None,None)]*n+[(None,1)],method='highs')
    if r.status!=0: return None
    return -r.fun
def covered_f(cons,S,n=4,first=True):
    fac=[tfacets(k) for k in S]; bad=[]
    for combo in itertools.product(*[range(len(f)) for f in fac]):
        m=maxeps_f(cons,[fac[i][j] for i,j in enumerate(combo)],n)
        if m is not None and m>1e-9:
            bad.append(combo)
            if first: return False,bad
    return not bad,bad
