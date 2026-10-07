# LP for the O(1/L) correction xi1: maximize min_j (a_j.xi1 + beta_j(xi0)) s.t. sum (4-|S|) xi1 = 0,
# xi1 >= 0 off supp(xi0) (and we restrict xi1 to supp(xi0) U small set optionally), |xi1| bounded.
import numpy as np, itertools
from fractions import Fraction as F
from scipy.optimize import linprog
exec(open('cert_near.py').read().split("# classify steps")[0])
binding=[3,4,5,6]
# beta_j(xi0) as floats
import math
def Hf(p): return 0 if p in (0,1) else -(p*math.log(p)+(1-p)*math.log(1-p))
beta={}; arow={}
for j in binding:
    lj,G=groups(j); A=0.0; bj=0.0; row={S:0 for S in SAFE}
    for key,mem in G.items():
        quads=[S for S in mem if len(S)==4]
        if quads:
            side=(lj in quads[0])
            opp=[S for S in mem if len(S)<4 and (lj in S)!=side]
            s=float(sum(b[S] for S in opp))
            for S in opp: row[S]=1
            if s>0: A+=s*(1-math.log(4*s))
        else:
            si=float(sum(b[S] for S in mem if lj in S)); so=float(sum(b[S] for S in mem if lj not in S))
            if si>0 and so>0: bj+=(si+so)*Hf(si/(si+so))
    beta[j]=A+bj; arow[j]=row
print({j:round(v,5) for j,v in beta.items()})
NQ=[S for S in SAFE if len(S)<4]
supp=[S for S in NQ if S in xi]
for restrict in [True,False]:
    cells=supp if restrict else NQ
    nv=len(cells)+1
    c=np.zeros(nv); c[-1]=-1
    A_ub=[];b_ub=[]
    for j in binding:
        A_ub.append([-arow[j][S] for S in cells]+[1]); b_ub.append(beta[j])
    A_eq=[[4-len(S) for S in cells]+[0]]; b_eq=[0]
    bnds=[((-1,1) if S in xi else (0,1)) for S in cells]+[(None,None)]
    r=linprog(c,A_ub=A_ub,b_ub=b_ub,A_eq=A_eq,b_eq=b_eq,bounds=bnds,method='highs')
    print('restrict to supp(xi0):',restrict,' second-order value',-r.fun)
    print({S:round(v,4) for S,v in zip(cells,r.x) if abs(v)>1e-9})
