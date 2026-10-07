"""CONTINUOUS oracle-row complexity for closed type sets given by finitely many rank-1 types (up-closure implicit).
Capacities x (p parts), types T (vectors, |t|=1), alpha* = N - tau*.  For each support: MILP with continuous cell
masses y, binary row roles (type t or ORACLE: window mass >= alpha* + margin).  Returns max #oracle rows."""
import sys, json
import numpy as np
from fractions import Fraction
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/tame')
from tc_lib import SUPPORTS, order_supports
def cont_ilp(x, T, cells, athr, min_oracle=0, time_limit=60):
    p=len(x); m=len(cells); nt=len(T)
    ny=p*m; nz=7*nt; nv=ny+nz+7
    Y=lambda i,j:i*m+j; Z=lambda l,t: ny+l*nt+t; O=lambda l: ny+nz+l
    rows=[];lo=[];hi=[]
    for i in range(p):
        r=np.zeros(nv); r[[Y(i,j) for j in range(m)]]=1; rows.append(r); lo.append(x[i]); hi.append(x[i])
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
    ub=np.full(nv,1.0); integ=np.ones(nv); integ[:ny]=0
    for i in range(p):
        for j in range(m): ub[Y(i,j)]=x[i]
    c=np.zeros(nv); c[[O(l) for l in range(7)]]=-1
    res=milp(c=c,constraints=LinearConstraint(np.array(rows),lo,hi),integrality=integ,
             bounds=Bounds(np.zeros(nv),ub),options={'time_limit':time_limit,'disp':False})
    if res.status==0:
        o=[int(round(res.x[O(l)])) for l in range(7)]
        role=[('O' if o[l] else 'T%d'%int(np.argmax([res.x[Z(l,t)] for t in range(nt)]))) for l in range(7)]
        return sum(o), role
    if res.status==2: return -1, None
    return None, None
def max_oracle_cont(x,T,tau,margin=1e-7,verbose=False):
    athr=sum(x)-tau+margin; best=-1; arg=None; und=[]
    for idx in order_supports():
        v,role=cont_ilp(x,T,SUPPORTS[idx],athr,min_oracle=best+1)
        if v is None: und.append(idx); continue
        if v>best: best=v; arg=(idx,role); 
        if verbose and v>=0: print('support',idx,'oracle',v,role,flush=True)
        if best==7: break
    return best,arg,und
if __name__=='__main__':
    x=json.loads(sys.argv[1]); T=json.loads(sys.argv[2]); tau=float(sys.argv[3])
    print(max_oracle_cont(x,T,tau,verbose=True))
