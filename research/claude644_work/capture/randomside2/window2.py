# First-moment exponents per k (nats) in H_rho, N=nk, tau=tau_*k, x=n-tau, rho=1/C(xk,k):
#   rule R with j found edges and pattern constraints: exponent = [n ln n + maxent] - j*psi(x).
#   Upper bound via dual (rigorous up to float); 'infeasible' detected by dual unboundedness (g -> -inf).
import numpy as np, itertools, sys, warnings; warnings.filterwarnings("ignore")
from maxent import maxent_dual
def psi(x): return x*np.log(x)-(x-1)*np.log(x-1) if x>1 else 0.0
def subsets(m): return [S for r in range(m+1) for S in itertools.combinations(range(m),r)]
def rule_exp(pats, j, extra_ub, n, tau):
    # pats: list of patterns (tuples of found-edge indices); each found edge has size 1; total mass n
    P=len(pats)
    Aeq=np.array([[1.0 if i in S else 0 for S in pats] for i in range(j)]+[[1.0]*P]); beq=np.array([1.0]*j+[n])
    Aub=np.array([row for row,_ in extra_ub]) if extra_ub else None
    bub=np.array([rhs(tau) for _,rhs in extra_ub]) if extra_ub else None
    val,y,viol,nu=maxent_dual(Aeq,beq,Aub,bub)
    if val<-1e6 or viol>1e-4: return None   # infeasible / not converged
    return n*np.log(n)+val - j*psi(n-tau)
# --- GT*: 3 found, no common point, union <= 2 tau
GTP=[S for S in subsets(3) if len(S)<3]
GT_ub=[([1.0 if len(S)>0 else 0 for S in GTP], lambda tau: 2*tau)]
# --- Lemma Q: 4 found; I(mu) masses; I5<=tau, I6+I7<=2tau-1 (orientation: all 3 choices of mu5 equivalent by symmetry)
QP=subsets(4); MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def inI(S,mu): return any(set(p)<=set(S) for p in mu)
Irow=[[1.0 if inI(S,mu) else 0 for S in QP] for mu in MATCH]
Q_ub=[(Irow[0],lambda tau: tau),([a+b for a,b in zip(Irow[1],Irow[2])],lambda tau:2*tau-1)]
# --- TC: found E(0),B1(1),B2(2),C1(3),C2(4). inside-E patterns: E1:{B2,C2},E2:{B2,C1},E3:{B1,C2},E4:{B1,C1}
allowed={1:(2,4),2:(2,3),3:(1,4),4:(1,3)}
TCP=[]; quarter=[]
for qd,(a,b) in allowed.items():
    for S in subsets(2):
        TCP.append(tuple(sorted((0,)+tuple((a,b)[i] for i in S)))); quarter.append(qd)
for S in subsets(4):
    TCP.append(tuple(i+1 for i in S)); quarter.append(0)
def isX(S,q): return q==0 and (1 in S or 2 in S) and (3 in S or 4 in S)
Xrow=[1.0 if isX(S,q) else 0 for S,q in zip(TCP,quarter)]
r14=[1.0 if q in (1,4) else 0 for q in quarter]; r23=[1.0 if q in (2,3) else 0 for q in quarter]
TC_ub=[([a+b for a,b in zip(Xrow,r14)],lambda tau:tau),([a+b for a,b in zip(Xrow,r23)],lambda tau:tau)]
# TC patterns may repeat as tuples for different quarters? inside patterns all contain 0 and quarter-specific pairs; E-only pattern (0,) repeats 4x -> fine (distinct cells)
if __name__=="__main__":
    taus=[float(a) for a in sys.argv[1].split(',')]
    for tau in taus:
        print("tau",tau)
        for n in np.round(np.arange(tau+1.1,tau+2.4,0.05),3):
            g=rule_exp(GTP,3,GT_ub,n,tau); q=rule_exp(QP,4,Q_ub,n,tau); c=rule_exp(TCP,5,TC_ub,n,tau)
            f=lambda v: ' infeas' if v is None else f"{v:+.4f}"
            surv = (g is None or g<0) and (q is None or q<0)
            print(f"  n={n:.3f} x={n-tau:.3f} GT {f(g)}  Q {f(q)}  TC {f(c)}  {'<-- GT&Q dead' if surv else ''}",flush=True)
