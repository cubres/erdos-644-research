# Sub-2k regime: static TWO-ANCHOR bad-tuple LP. Anchors E, F with |E cap F| = x (adversarial).
# Regions A=E∩F (x), B=E\F (1-x), C=F\E (1-x), D=V\(E∪F) (r-1+x), r = eta-1.
# Indices served by E (I_E): all A,B points have i in type. Served by F (I_F): all A,C points.
# Other indices: mass of {x: i not in type} <= theta.  LP(x) = min theta.
import json, itertools, numpy as np, sys
from scipy.optimize import linprog
from anchor1_lp import SUPP
def lp2(supp,IE,IF,x,r):
    masses=[x,1-x,1-x,r-1+x]
    allowed=[[s for s in supp if all((s>>i)&1 for i in IE+IF)],   # A: in E and F
             [s for s in supp if all((s>>i)&1 for i in IE)],       # B
             [s for s in supp if all((s>>i)&1 for i in IF)],       # C
             supp]                                                 # D
    idx=[];off=0
    for a in allowed: idx.append(off); off+=len(a)
    nv=off+1; c=np.zeros(nv); c[-1]=1
    Aeq=np.zeros((4,nv)); 
    for g in range(4): Aeq[g,idx[g]:idx[g]+len(allowed[g])]=1
    Aub=[]
    for i in range(7):
        if i in IE or i in IF: continue
        row=np.zeros(nv)
        for g in range(4):
            for j,s in enumerate(allowed[g]):
                if not (s>>i)&1: row[idx[g]+j]=1
        row[-1]=-1; Aub.append(row)
    res=linprog(c,A_ub=np.array(Aub) if Aub else None,b_ub=np.zeros(len(Aub)) if Aub else None,
                A_eq=Aeq,b_eq=masses,bounds=[(0,None)]*nv,method='highs')
    return res.fun if res.status==0 else 9.0
# symmetry reduce: IE, IF disjoint subsets of [7]; enumerate up to size 3 each (more anchors per edge unlikely useful)
PAIRS=[]
for a in range(0,3):
    for IE in itertools.combinations(range(7),a):
        rest=[i for i in range(7) if i not in IE]
        for b in range(0,3):
            for IF in itertools.combinations(rest,b):
                PAIRS.append((IE,IF))
def best_at(x,r,shapes=None):
    best=(9,None)
    for j,supp in enumerate(SUPP if shapes is None else [SUPP[s] for s in shapes]):
        for IE,IF in PAIRS:
            v=lp2(supp,IE,IF,x,r)
            if v<best[0]-1e-12: best=(v,(j,IE,IF))
    return best
if __name__=='__main__':
    r=float(sys.argv[1])
    for x in np.linspace(max(0,1-r),0.3,7):
        b=best_at(x,r)
        print("eta=%.3f x=%.4f LP=%.6f via %s"%(1+r,x,b[0],b[1])); sys.stdout.flush()
