"""Exact finite positive-witness search for two fixed budget-108b requests."""
from itertools import combinations
import json
from pathlib import Path
import numpy as np
src=json.loads(Path('outputs/agent_near_fano_first_response_discovery.json').read_text())
w=np.array(src['weights'],dtype=np.int64);m=np.array(src['old_masks'],dtype=np.int64);n=len(w)
labels=src['labels'];gset=set(src['found'][0]['selected']);m|=np.array([i in gset for i in range(n)],dtype=np.int64)<<7
p,Q=src['p'],src['Q'];pw=w[:,None]*w[None,:];pw[np.diag_indices(n)]=w*(w-1)
A=[i for i,l in enumerate(labels) if 'line'in l and 0 not in l['line']]
Ad=[i for i in A if labels[i]['extra'] is not None]
P=[i for i,l in enumerate(labels) if 'line'in l and 0 in l['line']]+[35]
Cspecs=[({0,1,2},4),({0,3,4},6),({0,5,6},2)]
C2=[i for i,l in enumerate(labels) if 'line'in l and(set(l['line']),l['extra'])in Cspecs]
assert len(C2)==3 and not(set(C2)&set(src['allowed']))
keeps6=list(combinations(range(8),5));keeps7=list(combinations(range(8),6))
def basegraph(keep):
 mask=sum(1<<j for j in keep)
 return ((m[:,None]|m[None,:])&mask)==mask
adj6=np.array([basegraph(keep) for keep in keeps6]);adj7=np.array([basegraph(keep) for keep in keeps7])
assert all(np.any(basegraph(keep)*pw) for keep in combinations(range(8),7))
found=None
for count,rem in enumerate(combinations(Ad,8),1):
 hset=(set(A)-set(rem))|set(C2)|{36};h=np.array([i in hset for i in range(n)])
 touch=h[:,None]|h[None,:]
 aa=adj6&touch
 # No common point in any old five-row graph here, but still handle singleton diagonal.
 aa[:,35,35]=False
 endpoints=np.sum(np.any(aa,axis=2)*w,axis=1)
 if np.any(endpoints<p):continue
 pairs=np.sum((adj6&touch)*pw,axis=(1,2))//2
 if np.any((endpoints==p)&(pairs<Q)):continue
 sevenpairs=np.sum((adj7&touch)*pw,axis=(1,2))//2
 if np.any(sevenpairs==0):continue
 found={'removed':list(rem),'H':sorted(hset),'G':sorted(gset),'C1':src['allowed'],'C2':C2,'D1':sorted(set(P)-set(src['allowed'])),'D2':sorted(set(P)-set(C2)),'weights':w.tolist(),'masks':(m|(h.astype(np.int64)<<8)).tolist(),'minimum_new_endpoint':int(endpoints.min()),'minimum_new_pairs':int(pairs.min()),'minimum_new_seven_pairs':int(sevenpairs.min())}
 print({k:v for k,v in found.items() if k not in ['weights','masks','G','H','D1','D2']},flush=True)
 break
out={'b':src['b'],'a':src['a'],'k':src['k'],'p':p,'Q':Q,'tried':count,'found':found,'labels':labels}
Path('outputs/agent_near_fano_two_response_pair.json').write_text(json.dumps(out,indent=2))
print('tried',count,'found',found is not None)
