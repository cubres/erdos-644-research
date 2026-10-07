# Sub-2k regime (n = eta k < 2k, all edges inside V): static ONE-ANCHOR bad-tuple LP over all 715 maximal
# bad supports. Units of k. V = E (mass 1) u R (mass r = eta-1). Types sigma (subset of [7] allowed edges).
# Index i served by the anchor (i in I0): every E-point has i in its type.  Otherwise the avoidance set
# T_i = {x: i not in sigma(x)} must have mass <= theta (oracle, tau >= theta k).  Minimise theta.
import json, itertools, numpy as np, sys
from scipy.optimize import linprog
cat=json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_full_support_catalog.json'))
def downclosure(maxcells):
    S=set()
    for m in maxcells:
        sub=m
        while True:
            S.add(sub)
            if sub==0: break
            sub=(sub-1)&m
    return sorted(S)
SUPP=[downclosure(o['maximal_cells']) for o in cat['orbits']]
def solve(supp,I0,r):
    nE=[s for s in supp if all((s>>i)&1 for i in I0)]
    nR=supp
    NE,NR=len(nE),len(nR); nv=NE+NR+1  # last = theta
    c=np.zeros(nv); c[-1]=1
    Aeq=np.zeros((2,nv)); Aeq[0,:NE]=1; Aeq[1,NE:NE+NR]=1; beq=[1,r]
    Aub=[];bub=[]
    for i in range(7):
        if i in I0: continue
        row=np.zeros(nv)
        for j,s in enumerate(nE):
            if not (s>>i)&1: row[j]=1
        for j,s in enumerate(nR):
            if not (s>>i)&1: row[NE+j]=1
        row[-1]=-1; Aub.append(row); bub.append(0)
    res=linprog(c,A_ub=np.array(Aub) if Aub else None,b_ub=bub if bub else None,A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*nv,method='highs')
    return res.fun if res.status==0 else None
if __name__=='__main__':
    for r in [0.75,0.8,0.875,0.95,0.999]:
        best=(9,None)
        for j,supp in enumerate(SUPP):
            for m in range(0,8):
                for I0 in itertools.combinations(range(7),m):
                    v=solve(supp,I0,r)
                    if v is not None and v<best[0]-1e-12: best=(v,(j,I0))
        print("eta=%.3f  best theta=%.6f  via %s   LemmaD=(eta+1/2)/3=%.6f  Fano=3eta/7=%.6f"%(1+r,best[0],best[1],(1+r+0.5)/3,3*(1+r)/7)); sys.stdout.flush()
