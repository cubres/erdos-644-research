"""General finite type sets over p parts: H_T = {k-sets with profile in T} (T a list of integer profiles, |u|=k).
Exact (7,2) via 715 supports, rows choose a type by binaries (u^l = sum_t z^l_t t <= window)."""
import itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from tc_lib import SUPPORTS, order_supports
def gen_ilp(n, T, cells, time_limit=60):
    p=len(n); m=len(cells); nt=len(T)
    ny=p*m; nz=7*nt; nv=ny+nz
    Y=lambda i,j:i*m+j; Z=lambda l,t: ny+l*nt+t
    rows=[];lo=[];hi=[]
    for i in range(p):
        r=np.zeros(nv); r[[Y(i,j) for j in range(m)]]=1; rows.append(r); lo.append(n[i]); hi.append(n[i])
    for l in range(7):
        r=np.zeros(nv); r[[Z(l,t) for t in range(nt)]]=1; rows.append(r); lo.append(1); hi.append(1)
        for i in range(p):   # sum_t z t_i - window_i <= 0
            r=np.zeros(nv)
            for t in range(nt): r[Z(l,t)]=T[t][i]
            for j in range(m):
                if cells[j]>>l&1: r[Y(i,j)]=-1
            rows.append(r); lo.append(-np.inf); hi.append(0)
    ub=np.zeros(nv)
    for i in range(p):
        for j in range(m): ub[Y(i,j)]=n[i]
    ub[ny:]=1
    res=milp(c=np.zeros(nv),constraints=LinearConstraint(np.array(rows),lo,hi),integrality=np.ones(nv),
             bounds=Bounds(np.zeros(nv),ub),options={'time_limit':time_limit,'disp':False})
    if res.status==0: return True
    if res.status==2: return False
    return None
def is72_gen(n,T):
    for idx in order_supports():
        r=gen_ilp(n,T,SUPPORTS[idx])
        if r is None: return None, idx
        if r: return False, idx
    return True, None
def tau_gen(n,T):
    """alpha = max |w| with no t in T, t<=w."""
    N=sum(n); best=-1
    Ta=np.array(T)
    for w in itertools.product(*[range(x+1) for x in n]):
        s=sum(w)
        if s<=best: continue
        if not np.any(np.all(Ta<=np.array(w),axis=1)): best=s
    return N-best
