# First-order (delta ln 1/delta) LP near the complete family n=7/4+delta.
import numpy as np, pickle, itertools
from scipy.optimize import linprog
from seqgame import SAFE, LINES
reps=pickle.load(open('order_reps.pkl','rb'))
QUAD=[i for i,S in enumerate(SAFE) if len(S)==4]
def analyse(order):
    binding=[]; rows=[]
    for j in range(7):
        prev=set(order[:j]); lj=order[j]
        groups={}
        for i,S in enumerate(SAFE):
            groups.setdefault(frozenset(set(S)&prev),[]).append(i)
        # entropy at y0 zero iff every group has all quads on one side
        zero=True; coef=np.zeros(len(SAFE))
        for key,mem in groups.items():
            qs=[i for i in mem if i in QUAD]
            sides=set(lj in SAFE[i] for i in qs)
            if len(sides)>1: zero=False
            if len(sides)==1:
                side=sides.pop()
                for i in mem:
                    if i not in QUAD and (lj in SAFE[i])!=side: coef[i]=1
        if zero: binding.append(j); rows.append(coef)
    # LP: max s  s.t. coef.xi >= s for binding; line sums of xi = 0; sum xi=1; xi>=0 off quads, free on quads
    nv=len(SAFE)+1
    c=np.zeros(nv); c[-1]=-1
    A_ub=[]; b_ub=[]
    for r in rows: A_ub.append(np.concatenate([-r,[1]])); b_ub.append(0)
    A_eq=[]; b_eq=[]
    for l in range(7): A_eq.append(np.concatenate([[1.0 if l in S else 0 for S in SAFE],[0]])); b_eq.append(0)
    A_eq.append(np.concatenate([np.ones(len(SAFE)),[0]])); b_eq.append(1)
    bounds=[(None,None) if i in QUAD else (0,None) for i in range(len(SAFE))]+[(None,None)]
    r=linprog(c,A_ub=np.array(A_ub),b_ub=b_ub,A_eq=np.array(A_eq),b_eq=b_eq,bounds=bounds,method='highs')
    return binding, (-r.fun if r.status==0 else r.status), r
out=[]
for o in reps:
    b,v,r=analyse(o)
    out.append((v,o,b))
out.sort(key=lambda t:-t[0] if isinstance(t[0],float) else 0)
for v,o,b in out: print(''.join(map(str,o)), 'binding steps',b,'LP value',v)
