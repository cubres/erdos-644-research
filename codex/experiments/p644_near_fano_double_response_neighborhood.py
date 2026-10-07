"""MILP discovery only on genuinely new G,H+three-old five-row graphs."""
from itertools import combinations
import json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
s=json.loads(Path('outputs/agent_near_fano_outside_control_certificate.json').read_text());b=100
w=np.array([a*b+c for a,c in s['weights']],dtype=np.int64);m=np.array(s['masks'],dtype=np.int64);n=len(w);p=111*b
triples=sorted(combinations(range(7),3),key=lambda t:(bool((t[0]+1)^(t[1]+1)^(t[2]+1)),t));out=[]
for oldrows in triples:
 keep=oldrows+(7,8);mask=sum(1<<j for j in keep)
 if np.any(m&mask==mask):continue
 adj=((m[:,None]|m[None,:])&mask)==mask;eligible=np.any(adj,axis=1);p5=int(w[eligible].sum());h=p5-p+1
 rows=[];lo=[];hi=[]
 def add(row,l,u):rows.append(row);lo.append(l);hi.append(u)
 add({n+i:1 for i in range(n)if eligible[i]},h,np.inf)
 for i in range(n):
  add({n+i:1,i:-int(w[i])},-np.inf,0);add({2*n+i:1,n+i:-1},0,np.inf)
  for j in range(n):
   if adj[i,j]:add({2*n+j:1,i:-int(w[j])},0,np.inf)
 mat=lil_matrix((len(rows),3*n))
 for r,row in enumerate(rows):
  for j,v in row.items():mat[r,j]=v
 res=milp(np.r_[np.zeros(2*n),np.ones(n)],integrality=np.r_[np.ones(n),np.zeros(2*n)],bounds=Bounds(np.zeros(3*n),np.r_[eligible.astype(int),w,w]),constraints=LinearConstraint(mat.tocsr(),lo,hi),options={'time_limit':15})
 rr={'oldrows':oldrows,'p5':p5,'threshold':h,'objective':res.fun,'message':res.message,'gap':res.get('mip_gap')}
 if res.x is not None:rr.update(selected=res.x[n:2*n].tolist(),cover=res.x[2*n:].tolist())
 out.append(rr);print({k:v for k,v in rr.items()if k not in ['selected','cover']},flush=True)
 Path('outputs/agent_near_fano_double_response_neighborhood.json').write_text(json.dumps(out,indent=2))
