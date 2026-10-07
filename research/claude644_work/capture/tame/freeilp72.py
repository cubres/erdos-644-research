"""CATALOGUE-FREE exact (7,2) test for type-closed families (independent of the 715-support catalogue).
A 7-tuple of edges <-> vertex types sigma(v) subset [7] (which rows contain v); no 2-transversal iff for all vertices
x,y (x=y allowed) sigma(x) u sigma(y) != [7].  ILP: n[P][s] = #vertices of part P with type s (s in 0..127),
used[s] binary >= n[P][s]/|P|, used[s]+used[s'] <= 1 whenever s|s' = 127 (s=s' allowed -> used[127]=0 etc.),
row i profile r_iP = sum_{s: i in s} n[P][s] must equal a type in T (binary choice; rank<=k types, equality).
Feasible <=> NOT (7,2).  usage: python3 freeilp72.py n1,n2,.. 'T json' [time_limit]"""
import sys, json, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
def free_ilp(n, T, time_limit=3600):
    p=len(n); nt=len(T); FULL=127
    NV=p*128; UV=128; ZV=7*nt; nv=NV+UV+ZV
    Nn=lambda P,s: P*128+s; Uu=lambda s: NV+s; Zz=lambda i,t: NV+UV+i*nt+t
    rows=[];lo=[];hi=[]
    def add(coefs,l,h): rows.append(coefs); lo.append(l); hi.append(h)
    for P in range(p): add({Nn(P,s):1 for s in range(128)},n[P],n[P])
    for P in range(p):
        for s in range(128): add({Nn(P,s):1,Uu(s):-n[P]},-np.inf,0)
    for s in range(128):
        for s2 in range(s,128):
            if s|s2==FULL:
                if s==s2: add({Uu(s):1},0,0)
                else: add({Uu(s):1,Uu(s2):1},-np.inf,1)
    for i in range(7):
        add({Zz(i,t):1 for t in range(nt)},1,1)
        for P in range(p):
            c={Nn(P,s):1 for s in range(128) if s>>i&1}
            for t in range(nt): c[Zz(i,t)]=c.get(Zz(i,t),0)-T[t][P]
            add(c,0,0)
    A=lil_matrix((len(rows),nv))
    for r,c in enumerate(rows):
        for j,v in c.items(): A[r,j]=v
    ub=np.ones(nv)
    for P in range(p):
        for s in range(128): ub[Nn(P,s)]=n[P]
    res=milp(c=np.zeros(nv),constraints=LinearConstraint(A.tocsr(),lo,hi),integrality=np.ones(nv),
             bounds=Bounds(np.zeros(nv),ub),options={'time_limit':time_limit,'disp':False})
    if res.status==0:
        sol={(P,s):int(round(res.x[Nn(P,s)])) for P in range(p) for s in range(128) if res.x[Nn(P,s)]>0.5}
        return True, sol
    if res.status==2: return False, None
    return None, res.message
if __name__=='__main__':
    n=[int(x) for x in sys.argv[1].split(',')]; T=[tuple(t) for t in json.loads(sys.argv[2])]
    tl=float(sys.argv[3]) if len(sys.argv)>3 else 3600
    t0=time.time(); r,info=free_ilp(n,T,tl)
    print({True:'BAD TUPLE (not (7,2))',False:'INFEASIBLE: (7,2) holds',None:'UNDECIDED'}[r], info if r else '', f'{time.time()-t0:.0f}s')
