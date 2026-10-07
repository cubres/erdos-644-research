"""Can a single k-set F be added to a type-closed family H_T without creating a bad tuple?
Parts are refined by F (part i splits into i_in (inside F) and i_out).  Row 0 must be exactly F; rows 1..6 use T
(types on the coarse parts).  Bad tuple through F exists iff some support/row-assignment ILP is feasible.
By S7 symmetry of each support orbit we must try every choice of which row is F (7 choices per orbit)."""
import numpy as np, itertools
from scipy.optimize import milp, LinearConstraint, Bounds
from tc_lib import SUPPORTS
def ilp_through_F(n_in, n_out, T, cells, frow, time_limit=60):
    p=len(n_in); m=len(cells); nt=len(T)
    # fine parts: 2p (i_in, i_out); y[f][j]
    nf=2*p; ny=nf*m; rows7=[l for l in range(7) if l!=frow]; nz=6*nt; nv=ny+nz
    Y=lambda f,j:f*m+j; Z=lambda r,t: ny+r*nt+t
    sizes=[n_in[i] for i in range(p)]+[n_out[i] for i in range(p)]
    A=[];lo=[];hi=[]
    for f in range(nf):
        r=np.zeros(nv); r[[Y(f,j) for j in range(m)]]=1; A.append(r); lo.append(sizes[f]); hi.append(sizes[f])
    ub=np.zeros(nv)
    for f in range(nf):
        for j in range(m):
            inF = f<p
            ok = (cells[j]>>frow&1)==1 if inF else (cells[j]>>frow&1)==0
            ub[Y(f,j)] = sizes[f] if ok else 0
    for ri,l in enumerate(rows7):
        r=np.zeros(nv); r[[Z(ri,t) for t in range(nt)]]=1; A.append(r); lo.append(1); hi.append(1)
        for i in range(p):  # coarse part i window = in+out cells containing l
            r=np.zeros(nv)
            for t in range(nt): r[Z(ri,t)]=T[t][i]
            for j in range(m):
                if cells[j]>>l&1: r[Y(i,j)]=-1; r[Y(p+i,j)]=-1
            A.append(r); lo.append(-np.inf); hi.append(0)
    ub[ny:]=1
    res=milp(c=np.zeros(nv),constraints=LinearConstraint(np.array(A),lo,hi),integrality=np.ones(nv),
             bounds=Bounds(np.zeros(nv),ub),options={'time_limit':time_limit,'disp':False})
    return {0:True,2:False}.get(res.status,None)
def can_add(n, T, Fprof):
    n_in=list(Fprof); n_out=[n[i]-Fprof[i] for i in range(len(n))]
    for cells in SUPPORTS:
        for frow in range(7):
            if not any(c>>frow&1 for c in cells): continue
            r=ilp_through_F(n_in,n_out,T,cells,frow)
            if r is None: return None
            if r: return False
    return True
if __name__=='__main__':
    import sys
    kp=int(sys.argv[1]); k=4*kp; n=[4*kp,3*kp+1]
    T=[(j,k-j) for j in range(1,k+1,2) if k-j<=n[1]]
    for j in range(0,k+1,2):
        if k-j>n[1]: continue
        print("parity k=%d: add F with |F cap P|=%d -> addable=%s"%(k,j,can_add(n,T,(j,k-j))),flush=True)
