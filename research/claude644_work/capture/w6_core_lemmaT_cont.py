"""Continuum test of the lazy TETRAHEDRAL lemma (Lemma T, oracle B-rows) on a type set.
Four A-types; cells C subset [4], 1<=|C|<=3 (no point in all four A-rows); per part masses.
Minimise  |I6| + |I7| + |U_A \\ (I5 u I6)|   s.t. |I5|,|I6|,|I7| <= tau*.
Lemma T kills the family (at large scale) if the minimum is < 2 tau*  (rank normalised to 1)."""
import itertools, numpy as np
from scipy.optimize import linprog
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
CELLS=[C for C in range(1,16) if bin(C).count('1')<=3]
def inI(C,mi): return any((C>>a&1) and (C>>b&1) for (a,b) in MATCH[mi])
def lemmaT(quad, X, ts):
    p=len(X); nC=len(CELLS); nv=p*nC; best=None
    for order in itertools.permutations(range(3)):
        m5,m6,m7=order
        obj=np.zeros(nv); I5=np.zeros(nv); I6=np.zeros(nv); I7=np.zeros(nv)
        for i in range(p):
            for c,C in enumerate(CELLS):
                k=i*nC+c
                I5[k]=inI(C,m5); I6[k]=inI(C,m6); I7[k]=inI(C,m7)
                obj[k]=I6[k]+I7[k]+(0 if (inI(C,m5) or inI(C,m6)) else 1)
        Aeq=[];beq=[]
        for i in range(p):
            for j in range(4):
                r=np.zeros(nv)
                for c,C in enumerate(CELLS):
                    if C>>j&1: r[i*nC+c]=1
                Aeq.append(r); beq.append(quad[j][i])
        Aub=[];bub=[]
        for i in range(p):
            r=np.zeros(nv); r[i*nC:(i+1)*nC]=1; Aub.append(r); bub.append(X[i])
        for v in (I5,I6,I7): Aub.append(v); bub.append(ts)
        res=linprog(obj,A_ub=np.array(Aub),b_ub=bub,A_eq=np.array(Aeq),b_eq=beq,bounds=(0,None),method='highs')
        if res.status==0 and (best is None or res.fun<best[0]): best=(res.fun,order)
    return best
if __name__=='__main__':
    for x,s in [(1.25,.15),(1.285,.142),(1.2,.19)]:
        a=(s,1-s); b=(1-s,s); A=[a,b]; ts=min(x-s,2*x-2+2*s)
        res=[(lemmaT(q,[x,x],ts),q) for q in itertools.combinations_with_replacement(A,4)]
        res=[r for r in res if r[0]]
        bst=min(res,key=lambda r:r[0][0])
        print(f"x={x} s={s} tau*={ts:.3f}: min LemmaT value {bst[0][0]:.4f} vs 2tau*={2*ts:.4f} quad={bst[1]}")
