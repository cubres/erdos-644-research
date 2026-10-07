"""Discovery LPs for the Z-example  H = C(U1,k) u C(U2,k) u C(Z,k), Zi = Z n Ui.
Normalise k=1.  n=|Z| (<7/4), m0=n-1 (complement size of a Z-edge in Z), z1,z2, delta.
Case X (a,b>=1, j=7-a-b Z-edges): cross-intersecting labels on A'=A n Z1 (mass z1-a*d) and B' (mass z2-b*d).
Case Y (a>=1,b=0, j=7-a): labels on A' (mass z1-a*d) from intersecting family cA, rest of Z (mass n-(z1-a d))
   from cB, cA x cB cross-intersecting, all labels nonempty.  (and symmetric b>=1,a=0)
Tuple is 2-pierceable (good) iff min max-load > m0.  Report margins."""
import itertools, sys
import numpy as np
from scipy.optimize import linprog
from crossload import antichains

def lp_minmax(m, fams_masses):
    # fams_masses: list of (family list of masks, mass)
    cols=[]; 
    for g,(fam,mass) in enumerate(fams_masses):
        for S in fam: cols.append((g,S))
    nv=len(cols)+1
    c=np.zeros(nv); c[-1]=1
    Aub=[];bub=[]
    for i in range(m):
        row=np.zeros(nv)
        for idx,(g,S) in enumerate(cols):
            if S>>i&1: row[idx]=1
        row[-1]=-1; Aub.append(row); bub.append(0)
    Aeq=[];beq=[]
    for g,(fam,mass) in enumerate(fams_masses):
        row=np.zeros(nv)
        for idx,(gg,S) in enumerate(cols):
            if gg==g: row[idx]=1
        Aeq.append(row); beq.append(mass)
    r=linprog(c,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*nv,method='highs')
    return r.fun if r.status==0 else np.inf

_AC={}
def ac(m):
    if m not in _AC: _AC[m]=antichains(m)
    return _AC[m]

def caseX(m, alpha, beta):
    if alpha<=0 or beta<=0: return -np.inf
    allS=range(1,1<<m); best=np.inf
    for gen in ac(m):
        A=[S for S in allS if any(S&g==g for g in gen)]
        B=[S for S in allS if all(S&g for g in gen)]
        if not B: continue
        best=min(best, lp_minmax(m,[(A,alpha),(B,beta)]))
    return best

def caseY(m, alpha, n):
    # cA intersecting upset, cB = all nonempty sets meeting every member of cA ; cA subset cB automatically
    if alpha<=0: alpha=0
    allS=range(1,1<<m); best=np.inf
    for gen in ac(m):
        A=[S for S in allS if any(S&g==g for g in gen)]
        if any((S&T)==0 for S in gen for T in gen): continue  # generators pairwise intersecting => A intersecting
        B=[S for S in allS if all(S&g for g in gen)]
        best=min(best, lp_minmax(m,[(A,alpha),(B,n-alpha)]))
    return best

def check(n, z1, d, verbose=True):
    z2=n-z1; m0=n-1; worst=np.inf; rep=[]
    for a in range(1,7):
        for b in range(1,7-a+1):
            j=7-a-b
            if j<1: continue
            v=caseX(j, z1-a*d, z2-b*d); rep.append(('X',a,b,v-m0)); worst=min(worst,v-m0)
    for a in range(1,7):
        j=7-a
        v=caseY(j, z1-a*d, n); rep.append(('Y1',a,v-m0)); worst=min(worst,v-m0)
        v=caseY(j, z2-a*d, n); rep.append(('Y2',a,v-m0)); worst=min(worst,v-m0)
    if verbose:
        for r in rep: print(r)
    return worst

if __name__=='__main__':
    n=float(sys.argv[1]); z1=float(sys.argv[2]); d=float(sys.argv[3])
    print('worst margin', check(n,z1,d))
