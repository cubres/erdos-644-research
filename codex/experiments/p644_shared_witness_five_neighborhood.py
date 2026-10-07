"""Fresh five-row neighborhood discovery for the new shared witness."""
from collections import defaultdict
from pathlib import Path
import json
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
src=json.loads(Path('outputs/agent_shared_witness_transport_discovery.json').read_text());p=11100;out=[]
for omitted in range(6):
 kept=[j for j in range(6)if j!=omitted];cells=defaultdict(int)
 for cell in src['cells']:
  mask=sum(bool(cell['witness_mask']&(1<<j))<<q for q,j in enumerate(kept));cells[mask]+=cell['weight']
 masks=sorted(cells);w=np.array([cells[m]for m in masks],dtype=np.int64);n=len(w)
 adj=np.array([[s|t==31 for t in masks]for s in masks]);elig=np.any(adj,axis=1);p5=int(w[elig].sum());h=p5-p+1
 rows=[];lo=[];hi=[]
 def add(row,l,u):rows.append(row);lo.append(l);hi.append(u)
 add({n+i:1 for i in range(n)if elig[i]},h,np.inf)
 for i in range(n):
  add({n+i:1,i:-int(w[i])},-np.inf,0);add({2*n+i:1,n+i:-1},0,np.inf)
  for j in range(n):
   if adj[i,j]:add({2*n+j:1,i:-int(w[j])},0,np.inf)
 mat=lil_matrix((len(rows),3*n))
 for r,row in enumerate(rows):
  for j,v in row.items():mat[r,j]=v
 res=milp(np.r_[np.zeros(2*n),np.ones(n)],integrality=np.r_[np.ones(n),np.zeros(2*n)],bounds=Bounds(np.zeros(3*n),np.r_[elig.astype(int),w,w]),constraints=LinearConstraint(mat.tocsr(),lo,hi),options={'time_limit':20})
 r={'omitted':omitted,'masks':[format(v,'05b')for v in masks],'weights':w.tolist(),'p5':p5,'threshold':h,'objective':res.fun,'message':res.message,'gap':res.get('mip_gap')}
 if res.x is not None:r.update(selected=res.x[n:2*n].tolist(),cover=res.x[2*n:].tolist())
 out.append(r);print({k:v for k,v in r.items()if k not in ['selected','cover','weights','masks']},flush=True)
Path('outputs/agent_shared_witness_five_neighborhood_discovery.json').write_text(json.dumps(out,indent=2))
