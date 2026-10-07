import itertools, numpy as np, sys
from scipy.optimize import milp, LinearConstraint, Bounds
def static_opt(cells, edges, nreq=4):
    # cells: dict name->mass ; edges: list of (c,d) candidate pair products (c may equal d? no)
    labels=[frozenset(s) for k in range(1,nreq+1) for s in itertools.combinations(range(nreq),k)]
    names=list(cells)
    nv=0; W={}; U={}
    for c in names:
        for L in labels:
            W[c,L]=nv; nv+=1
    for c in names:
        for L in labels:
            U[c,L]=nv; nv+=1
    Tv=nv; nv+=1
    A=[];lb=[];ub=[]
    def row(d,l,u):
        r=np.zeros(nv)
        for k,v in d.items(): r[k]+=v
        A.append(r);lb.append(l);ub.append(u)
    for c in names:
        row({W[c,L]:1 for L in labels},cells[c],cells[c])
        for L in labels:
            row({W[c,L]:1,U[c,L]:-cells[c]},-np.inf,0)
    for (c,d) in edges:
        for L in labels:
            for M in labels:
                if not (L&M): row({U[c,L]:1,U[d,M]:1},-np.inf,1)
    for i in range(nreq):
        d={W[c,L]:1 for c in names for L in labels if i in L}; d[Tv]=-1
        row(d,-np.inf,0)
    cost=np.zeros(nv); cost[Tv]=1
    integrality=np.zeros(nv); 
    for k in U.values(): integrality[k]=1
    lo=np.zeros(nv); hi=np.full(nv,np.inf)
    for k in U.values(): hi[k]=1
    res=milp(cost,constraints=LinearConstraint(np.array(A),lb,ub),integrality=integrality,bounds=Bounds(lo,hi))
    sol={}
    if res.x is not None:
        for c in names:
            for L in labels:
                if res.x[W[c,L]]>1e-9: sol.setdefault(c,[]).append((tuple(sorted(L)),round(res.x[W[c,L]],4)))
    return res.fun, sol
def triple(x,y,z):
    # X=E&G? use X=E&F? generic: X=AB, Y=AC, Z=BC ; privates PA,PB,PC
    cells={'X':x,'Y':y,'Z':z,'PA':1-x-y,'PB':1-x-z,'PC':1-y-z}
    # candidate pairs: X(AB)-needs C: Y,Z,PC ; Y(AC)-needs B: X,Z,PB ; Z(BC)-needs A: X,Y,PA
    edges=[('X','Y'),('X','Z'),('Y','Z'),('X','PC'),('Y','PB'),('Z','PA')]
    cells={k:v for k,v in cells.items() if v>1e-12}
    edges=[e for e in edges if e[0] in cells and e[1] in cells]
    return static_opt(cells,edges)
if __name__=="__main__":
    for t in [(0.375,0.375,0.125),(0.375,0.375,0.25),(0.375,0.375,0.375),(0.5,0.315,0.315),(0.5,0.1,0.1),(0.5,0.2,0.2)]:
        print(t,triple(*t))
