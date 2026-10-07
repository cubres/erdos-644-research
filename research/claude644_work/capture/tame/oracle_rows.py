"""ORACLE-ROW COMPLEXITY of bad tuples in type-closed families.
A row of a bad placement is an ORACLE row if its window has size >= alpha+1 = N - tau + 1 (then SOME edge lies in it,
by tau alone -- the row can be served by the tau-oracle), otherwise a FOUND row (needs an actual type <= window).
max_oracle(n,T,k,alpha) = max number of oracle rows over all bad placements (all 715 supports); -1 if (7,2).
Library + CLI.  Exact modulo HiGHS MILP (status checked; time limits reported)."""
import sys, itertools, json, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/tame')
from tc_lib import SUPPORTS, order_supports

def oracle_ilp(n, T, cells, athr, min_oracle=0, time_limit=120, maximize=True):
    """variables: y (p*m), z (7*nt) found-row type choice, o (7) oracle flags.
    row l: sum_t z_lt + o_l = 1; sum_t z_lt T_t[i] <= w^l_i; sum_i w^l_i >= athr * o_l."""
    p=len(n); m=len(cells); nt=len(T)
    ny=p*m; nz=7*nt; nv=ny+nz+7
    Y=lambda i,j:i*m+j; Z=lambda l,t: ny+l*nt+t; O=lambda l: ny+nz+l
    rows=[];lo=[];hi=[]
    for i in range(p):
        r=np.zeros(nv); r[[Y(i,j) for j in range(m)]]=1; rows.append(r); lo.append(n[i]); hi.append(n[i])
    for l in range(7):
        r=np.zeros(nv); r[[Z(l,t) for t in range(nt)]]=1; r[O(l)]=1; rows.append(r); lo.append(1); hi.append(1)
        for i in range(p):
            r=np.zeros(nv)
            for t in range(nt): r[Z(l,t)]=T[t][i]
            for j in range(m):
                if cells[j]>>l&1: r[Y(i,j)]=-1
            rows.append(r); lo.append(-np.inf); hi.append(0)
        r=np.zeros(nv); r[O(l)]=athr
        for i in range(p):
            for j in range(m):
                if cells[j]>>l&1: r[Y(i,j)]-=1
        rows.append(r); lo.append(-np.inf); hi.append(0)
    r=np.zeros(nv); r[[O(l) for l in range(7)]]=1; rows.append(r); lo.append(min_oracle); hi.append(7)
    ub=np.zeros(nv)
    for i in range(p):
        for j in range(m): ub[Y(i,j)]=n[i]
    ub[ny:]=1
    c=np.zeros(nv)
    if maximize: c[[O(l) for l in range(7)]]=-1
    res=milp(c=c,constraints=LinearConstraint(np.array(rows),lo,hi),integrality=np.ones(nv),
             bounds=Bounds(np.zeros(nv),ub),options={'time_limit':time_limit,'disp':False})
    if res.status==0:
        y=[[int(round(res.x[Y(i,j)])) for j in range(m)] for i in range(p)]
        o=[int(round(res.x[O(l)])) for l in range(7)]
        W=[tuple(sum(y[i][j] for j in range(m) if cells[j]>>l&1) for i in range(p)) for l in range(7)]
        return sum(o), (y,o,W)
    if res.status==2: return -1, None
    return None, res.status   # time limit (res.x may hold incumbent)

def tau_of(n,T):
    N=sum(n); best=-1; Ta=np.array(T)
    for w in itertools.product(*[range(x+1) for x in n]):
        s=sum(w)
        if s<=best: continue
        if not np.any(np.all(Ta<=np.array(w),axis=1)): best=s
    return N-best

def max_oracle(n,T,tau=None,time_limit=120,verbose=False):
    N=sum(n)
    if tau is None: tau=tau_of(n,T)
    athr=N-tau+1
    best=-1; arg=None; und=[]
    for idx in order_supports():
        v,info=oracle_ilp(n,T,SUPPORTS[idx],athr,min_oracle=best+1,time_limit=time_limit)
        if v is None: und.append(idx); continue
        if v>best: best=v; arg=(idx,info)
        if verbose and v>=0: print('support',idx,'oracle rows',v,flush=True)
        if best==7: break
    return best,arg,und,tau

if __name__=='__main__':
    k=int(sys.argv[1]); n=[int(x) for x in sys.argv[2].split(',')]; T=json.loads(sys.argv[3])
    if isinstance(T[0],int): T=[(j,k-j) for j in T]
    T=[tuple(t) for t in T]
    b,arg,und,tau=max_oracle(n,T,verbose=True)
    print(f"k={k} n={n} tau={tau} max_oracle_rows={b} (min found rows {7-b if b>=0 else None}) undecided={und}")
    if arg: print('support',arg[0],'windows',arg[1][2],'oracle flags',arg[1][1])
