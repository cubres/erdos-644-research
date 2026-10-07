"""New discovery probe: minimum ground mass of a bad seven-row family
whose first three rows have empty intersection and cover the whole ground.
This does not replay any earlier support catalogue.
"""
import json,time,argparse
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix

def run(seconds=30):
    cells=[c for c in range(1,127)if bin(c&7).count('1')in(1,2)]
    n=len(cells);rows=[];lo=[];hi=[]
    def add(row,l=-np.inf,h=np.inf):rows.append(row);lo.append(l);hi.append(h)
    for i in range(7):add({j:1 for j,c in enumerate(cells)if c>>i&1},1,1)
    for j in range(n):add({j:1,n+j:-1},h=0)
    for j,c in enumerate(cells):
        for h,d in enumerate(cells[:j]):
            if c|d==127:add({n+j:1,n+h:1},h=1)
    matrix=lil_matrix((len(rows),2*n))
    for r,row in enumerate(rows):
        for j,v in row.items():matrix[r,j]=v
    started=time.time()
    result=milp(np.array([1]*n+[0]*n),integrality=np.array([0]*n+[1]*n),
                bounds=Bounds(np.zeros(2*n),np.ones(2*n)),constraints=LinearConstraint(matrix.tocsr(),lo,hi),
                options={'time_limit':seconds,'mip_rel_gap':0})
    out={'status':result.message,'elapsed_seconds':time.time()-started,'N_upper':result.fun,
         'N_lower':getattr(result,'mip_dual_bound',None),'scope':'Numerical discovery only, new96-cell support model.'}
    if result.x is not None:out['cells']={str(c):float(result.x[j])for j,c in enumerate(cells)if result.x[j]>1e-8}
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=30);a=p.parse_args()
    print(json.dumps(run(a.seconds),indent=2))
