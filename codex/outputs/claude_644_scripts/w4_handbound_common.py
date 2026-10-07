import sys, itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
import w4_handbound_chain as C
from w4_handbound_pat import cells_of, EDGES, pat_budget
beta=float(sys.argv[1]); h=float(sys.argv[2]); N=int(sys.argv[3]); names=sys.argv[4].split(','); K=int(sys.argv[5])
lo=2-beta-2*h
pts=[]
for i in range(N+1):
    m=lo+(h-lo)*i/N
    w=min(m,1-(beta+m)/2)
    for j in range(N+1):
        for k in range(j+1):
            y=w*j/N; z=w*k/N
            if C.bestg(m,y,z,m,h,beta,names,False)[0]>beta+1e-12: pts.append((m,y,z))
print('hard',len(pts))
sample=pts[::max(1,len(pts)//K)]
nreq=4
labels=[frozenset(s) for k in range(1,nreq+1) for s in itertools.combinations(range(nreq),k)]
cells=['X','Y','Z','PA','PB','PC']
# orientation: we fix orientation (m,y,z)->(X,Y,Z)=(y,m,z)? try all 3 distinct hub choices
def solve(orient):
    nv=0; U={}
    for c in cells:
        for L in labels: U[c,L]=nv; nv+=1
    W={}
    for p in range(len(sample)):
        for c in cells:
            for L in labels: W[p,c,L]=nv; nv+=1
    A=[];lb=[];ub=[]
    def row(d,l,u):
        r=np.zeros(nv)
        for k,v in d.items(): r[k]+=v
        A.append(r);lb.append(l);ub.append(u)
    for (c,d) in EDGES:
        for L in labels:
            for M in labels:
                if not (L&M): row({U[c,L]:1,U[d,M]:1},-np.inf,1)
    for p,pt in enumerate(sample):
        v=[pt[t] for t in orient]
        cm=cells_of(*v)
        for c in cells:
            row({W[p,c,L]:1 for L in labels},cm[c],cm[c])
            for L in labels: row({W[p,c,L]:1,U[c,L]:-1},-np.inf,0)
        for i in range(nreq):
            row({W[p,c,L]:1 for c in cells for L in labels if i in L},-np.inf,beta)
    cost=np.zeros(nv)
    for k in U.values(): cost[k]=1
    integ=np.zeros(nv)
    for k in U.values(): integ[k]=1
    hi=np.full(nv,np.inf)
    for k in U.values(): hi[k]=1
    res=milp(cost,constraints=LinearConstraint(np.array(A),lb,ub),integrality=integ,bounds=Bounds(0,hi),options={'time_limit':120})
    if res.x is None: return None
    return {c:[tuple(sorted(L)) for L in labels if res.x[U[c,L]]>0.5] for c in cells}
for orient in [(0,1,2),(1,0,2),(0,2,1),(2,1,0)]:
    pat=solve(orient)
    print(orient,pat)
    if pat:
        bad=[p for p in pts if pat_budget(pat,*[p[t] for t in orient])>beta+1e-9]
        print(' fails on',len(bad),'of',len(pts))
