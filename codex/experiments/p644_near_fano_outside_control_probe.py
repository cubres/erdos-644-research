"""Upper residual potential for all495 four-defect allowances after denseG."""
from itertools import combinations
import json
from pathlib import Path
import numpy as np
s=json.loads(Path('outputs/agent_near_fano_optimized_dense_response.json').read_text());w=np.array(s['weights']);m=np.array(s['masks']);n=len(w);G=set(s['found'][0]['G']);g=np.array([i in G for i in range(n)])
P={i for i,l in enumerate(s['labels'])if 'line'in l and 0 in l['line']}|{35}
Bdef=[i for i in P if i<35 and s['labels'][i]['extra']is not None]
A=set(range(n))-P-{36}
oldrows=[1,2,5,6];oldmask=sum(1<<j for j in oldrows)
adj=(((m[:,None]|m[None,:])&oldmask)==oldmask)&(g[:,None]|g[None,:])
pairw=w[:,None]*w[None,:];pairw[np.diag_indices(n)]=w*(w-1)
results=[]
for C in combinations(Bdef,4):
 h=np.array([i in A or i in C for i in range(n)])
 a=adj&(h[:,None]|h[None,:]);aa=a.copy();aa[35,35]=False
 pp=int(w[np.any(aa,axis=1)].sum());qq=int(np.sum(a*pairw)//2)
 results.append({'C':list(C),'endpoint_upper':pp,'pair_upper':qq})
results.sort(key=lambda z:(z['endpoint_upper'],z['pair_upper']))
Path('outputs/agent_near_fano_outside_control_probe.json').write_text(json.dumps({'oldrows':oldrows,'results':results},indent=2))
print('choices',len(results));print(json.dumps(results[:12],indent=2))
