"""Independent (7,2) check by MILP: minimum number of edges avoiding-covering all pairs (u<=v). (7,2) iff min >= 8."""
import itertools, time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from build import EDGES, V
t0=time.time(); m=len(EDGES)
P=list(itertools.combinations_with_replacement(V,2))
A=lil_matrix((len(P),m))
for r,(u,v) in enumerate(P):
    for i,E in enumerate(EDGES):
        if u not in E and v not in E: A[r,i]=1
res=milp(c=np.ones(m),constraints=LinearConstraint(A.tocsr(),np.ones(len(P)),np.inf),integrality=np.ones(m),
         bounds=Bounds(0,1),options={'disp':False,'time_limit':3000})
print('status',res.status,res.message,'obj',res.fun,'bound',getattr(res,'mip_dual_bound',None),f'{time.time()-t0:.0f}s')
