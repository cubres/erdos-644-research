"""Multi-type request tests (discovery): rows assigned to supplied types or 'R' (requested)."""
import itertools, json
import numpy as np
from scipy.optimize import linprog
from w4_typeclosed_single import FANO_CELLS

def multi_test(parents, assign, types, x):
    """assign[j] = index into types, or None for requested. returns min max request cost."""
    p=len(x); P=list(parents); nc=len(P)
    R=[j for j in range(7) if assign[j] is None]
    nv=p*nc+1; A=[]; b=[]
    for i in range(p):
        row=np.zeros(nv); row[i*nc:(i+1)*nc]=1; A.append(row); b.append(x[i])
        for j in range(7):
            if assign[j] is None: continue
            row=np.zeros(nv)
            for k,C in enumerate(P):
                if C>>j&1: row[i*nc+k]=-1
            A.append(row); b.append(-types[assign[j]][i])
    for j in R:
        row=np.zeros(nv); row[-1]=-1; const=0.0
        for i in range(p):
            const+=x[i]
            for k,C in enumerate(P):
                if C>>j&1: row[i*nc+k]-=1
        A.append(row); b.append(-const)
    c=np.zeros(nv); c[-1]=1
    res=linprog(c,A_ub=np.array(A),b_ub=np.array(b),bounds=[(0,None)]*nv,method='highs')
    if res.status!=0: return None
    return res.fun if R else 0.0

if __name__=='__main__':
    T79=[(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
    types=[[v/80 for v in t] for t in T79]; x=[513/640]*3; tau=483/640
    best=(9,None)
    for a,b in itertools.combinations_with_replacement(range(9),2):
        for pattern in itertools.product([0,1,2],repeat=7):  # 0->a,1->b,2->request
            if 2 not in pattern: continue
            assign=[(a if s==0 else b) if s<2 else None for s in pattern]
            t=multi_test(FANO_CELLS,assign,types,x)
            if t is not None and t<best[0]: best=(t,(a,b,pattern))
    print('best Fano pair+request cost',best,'tau*',tau)
