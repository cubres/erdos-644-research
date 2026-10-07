"""Positive responses to the coupled-optimization first request."""
from itertools import combinations
import json
from pathlib import Path
import numpy as np
s=json.loads(Path('outputs/agent_near_fano_first_response_discovery.json').read_text())
w=np.array(s['weights'],dtype=np.int64);m=np.array(s['old_masks'],dtype=np.int64);n=len(w)
rows=[2,4,5,6];trace=np.array([sum(int(bool(v&(1<<j)))<<q for q,j in enumerate(rows))for v in m])
D1={i for i in range(35+1)if trace[i]in [2,6,9,11,13]};available=set(range(n))-D1
removable=[i for i in available if i<35 and s['labels'][i]['extra']is not None]
print('D1',sum(w[i]for i in D1),'available',sum(w[i]for i in available),'removable',len(removable),flush=True)
pw=w[:,None]*w[None,:];pw[np.diag_indices(n)]=w*(w-1)
base=[];keeps=list(combinations(range(7),5))
for keep in keeps:
 mask=sum(1<<j for j in keep);base.append(((m[:,None]|m[None,:])&mask)==mask)
base=np.array(base)
base7=[]
for keep in combinations(range(7),6):
 mask=sum(1<<j for j in keep);base7.append(((m[:,None]|m[None,:])&mask)==mask)
base7=np.array(base7)
found=[]
for count,removed in enumerate(combinations(removable,8),1):
 G=available-set(removed);g=np.array([i in G for i in range(n)])
 adj=base&(g[:,None]|g[None,:]);aa=adj.copy();aa[:,35,35]=False
 ep=np.sum(np.any(aa,axis=2)*w,axis=1);pair=np.sum(adj*pw,axis=(1,2))//2
 if np.any(ep<s['p'])or np.any((ep==s['p'])&(pair<s['Q'])):continue
 pair7=np.sum((base7&(g[:,None]|g[None,:]))*pw,axis=(1,2))//2
 if np.any(pair7==0):continue
 found.append({'removed':list(removed),'G':sorted(G),'minimum_endpoint':int(ep.min()),'minimum_pairs':int(pair.min()),'minimum_seven_pairs':int(pair7.min())})
 if len(found)>=8:break
out={'b':s['b'],'p':s['p'],'Q':s['Q'],'k':s['k'],'weights':w.tolist(),'masks':m.tolist(),'labels':s['labels'],'D1':sorted(D1),'tried':count,'found':found}
Path('outputs/agent_near_fano_optimized_first_response.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'tried':count,'found':found},indent=2))
