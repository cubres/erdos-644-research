"""R_3 (3 found edges + 4 tau-oracle rows, ANY bad support) against random families H_rho.  NUMERICAL (SLSQP).
N = n k, rho = 1/C(xk,k)  (alpha ~ xk, tau ~ (n-x)k).  For a support (maximal cells) and a choice F of 3 found rows:
  z[J,M] >= 0  (J subset F, M a cell with J subset M): mass of vertices lying in exactly the found edges J and in cell M.
  r_J = sum_M z[J,M];  sum_{J ni f} r_J = 1 (f in F);  sum r_J = n;  oracle row l: sum_{J, M ni l} z[J,M] >= x + margin.
  Janson (Lemma TJ, notes_randomside c9): need, for every nonempty J' subset F,
      E_J'(r) = n ln n - sum_{A subset J'} m_A ln m_A  -  |J'| psi(x)  > 0,   m_A = sum_{J : J cap J' = A} r_J.
Maximise the min exponent; bisection on x gives x_max(n) and the R_3 threshold tau_R3(n) = n - x_max(n).
usage: python3 r3_random.py n [margin]"""
import sys, itertools, math, time
import numpy as np
from scipy.optimize import linprog, minimize
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/tame')
from tc_lib import SUPPORTS
def psi(x): return x*math.log(x)-(x-1)*math.log(x-1) if x>1 else 0.0
SUBS=[J for J in range(8)]            # subsets of {0,1,2} (found-row indices)
def setup(cells, F):
    O=[l for l in range(7) if l not in F]
    var=[]
    for J in SUBS:
        rowsJ={F[i] for i in range(3) if J>>i&1}
        for mi,M in enumerate(cells):
            if all(M>>l&1 for l in rowsJ): var.append((J,mi))
    return O,var
def lin_constraints(cells,F,O,var,n,x):
    nv=len(var)
    Aeq=[];beq=[]
    for i in range(3):
        a=np.zeros(nv)
        for v,(J,mi) in enumerate(var):
            if J>>i&1: a[v]=1
        Aeq.append(a); beq.append(1.0)
    Aeq.append(np.ones(nv)); beq.append(n)
    Aub=[];bub=[]
    for l in O:
        a=np.zeros(nv)
        for v,(J,mi) in enumerate(var):
            if cells[mi]>>l&1: a[v]=-1
        Aub.append(a); bub.append(-x)
    return np.array(Aeq),np.array(beq),np.array(Aub),np.array(bub)
def exponents(zv,var,n,x):
    r=np.zeros(8)
    for v,(J,mi) in enumerate(var): r[J]+=zv[v]
    out=[]
    for Jp in range(1,8):
        m={}
        for J in range(8):
            A=J&Jp; m[A]=m.get(A,0)+r[J]
        ent=n*math.log(n)-sum(mm*math.log(mm) for mm in m.values() if mm>1e-15)
        out.append(ent-bin(Jp).count('1')*psi(x))
    return out
def best_exponent(cells,F,n,x,starts=4,seed=0):
    O,var=setup(cells,F); nv=len(var)
    Aeq,beq,Aub,bub=lin_constraints(cells,F,O,var,n,x)
    lp=linprog(np.zeros(nv),A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*nv,method='highs')
    if lp.status!=0: return None
    rng=np.random.default_rng(seed); best=-1e9; bestz=None
    for s in range(starts):
        # random feasible start: LP with random objective
        c=rng.normal(size=nv)
        lp2=linprog(c,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*nv,method='highs')
        z0=0.5*lp.x+0.5*(lp2.x if lp2.status==0 else lp.x)
        # variables: z (nv) and t
        def obj(w): return -w[-1]
        cons=[{'type':'eq','fun':lambda w,A=Aeq,b=beq: A@w[:-1]-b},
              {'type':'ineq','fun':lambda w,A=Aub,b=bub: b-A@w[:-1]},
              {'type':'ineq','fun':lambda w: np.array(exponents(np.maximum(w[:-1],1e-12),var,n,x))-w[-1]}]
        w0=np.append(z0,min(exponents(np.maximum(z0,1e-12),var,n,x)))
        res=minimize(obj,w0,constraints=cons,bounds=[(0,None)]*nv+[(None,None)],method='SLSQP',options={'maxiter':300,'ftol':1e-10})
        w=res.x; z=np.maximum(w[:-1],0)
        # feasibility check
        if np.max(np.abs(Aeq@z-beq))<1e-6 and np.all(Aub@z<=bub+1e-6):
            val=min(exponents(np.maximum(z,1e-15),var,n,x))
            if val>best: best=val; bestz=z
    return best,bestz,var
def scan(n,x,margin=1e-3,verbose=False):
    """max over supports and found-row triples of the best min exponent at (n,x)."""
    best=(-1e9,None)
    for idx,cells in enumerate(SUPPORTS):
        for F in itertools.combinations(range(7),3):
            r=best_exponent(cells,list(F),n,x+margin,starts=2)
            if r is None: continue
            if r[0]>best[0]:
                best=(r[0],(idx,F));
                if verbose: print(f'  n={n} x={x:.4f} support {idx} F={F} exponent {r[0]:.4f}',flush=True)
    return best
if __name__=='__main__':
    n=float(sys.argv[1]); t0=time.time()
    x=n-0.75   # tau = 3/4 exactly: is R_3 feasible with positive Janson exponents here?
    b=scan(n,x,verbose=True)
    print(f'n={n}: at tau=3/4 (x={x}) best min exponent {b[0]:.4f} via {b[1]}  ({time.time()-t0:.0f}s)',flush=True)
