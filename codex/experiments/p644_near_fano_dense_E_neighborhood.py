"""Discovery on NEW four-old-row-plus-G graphs; no infeasibility certificate."""
from itertools import combinations
import json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
src = json.loads(Path('outputs/agent_near_fano_optimized_dense_response.json').read_text())
w = np.array(src['weights'], dtype=np.int64)
masks = np.array(src['masks'], dtype=np.int64)
g = np.array([i in src['found'][0]['G'] for i in range(len(w))])
p = src['p']; n = len(w); outputs=[]
for keep in combinations(range(7),4):
    if 0 not in keep: continue
    oldmask=sum(1<<j for j in keep)
    if np.any((masks & oldmask)==oldmask):
        continue
    adj=(((masks[:,None]|masks[None,:])&oldmask)==oldmask)&(g[:,None]|g[None,:])
    eligible=np.any(adj,axis=1)
    p5=int(w[eligible].sum()); h=p5-p+1
    rows=[]; lo=[]; hi=[]
    def add(row,l,u):rows.append(row);lo.append(l);hi.append(u)
    add({n+i:1 for i in range(n) if eligible[i]},h,np.inf)
    for i in range(n):
        add({n+i:1,i:-int(w[i])},-np.inf,0)
        add({2*n+i:1,n+i:-1},0,np.inf)
        for j in range(n):
            if adj[i,j]:add({2*n+j:1,i:-int(w[j])},0,np.inf)
    matrix=lil_matrix((len(rows),3*n))
    for r,row in enumerate(rows):
        for j,v in row.items():matrix[r,j]=v
    res=milp(np.r_[np.zeros(2*n),np.ones(n)],integrality=np.r_[np.ones(n),np.zeros(2*n)],bounds=Bounds(np.zeros(3*n),np.r_[eligible.astype(int),w,w]),constraints=LinearConstraint(matrix.tocsr(),lo,hi),options={'time_limit':15})
    out={'keep':keep,'p5':p5,'h':h,'objective':res.fun,'message':res.message,'gap':res.get('mip_gap')}
    if res.x is not None:out.update(selected=res.x[n:2*n].tolist(),cover=res.x[2*n:].tolist())
    outputs.append(out)
    print({k:v for k,v in out.items() if k not in ['selected','cover']},flush=True)
    Path('outputs/agent_near_fano_dense_E_neighborhood.json').write_text(json.dumps(outputs,indent=2))
