"""Positive actual H after dense G, with no shared outside points."""
from itertools import combinations
import json
from pathlib import Path
import numpy as np
s=json.loads(Path('outputs/agent_near_fano_optimized_dense_response.json').read_text());w=np.array(s['weights']);m=np.array(s['masks']);n=len(w);G=set(s['found'][0]['G']);m|=np.array([i in G for i in range(n)],dtype=np.int64)<<7
P={i for i,l in enumerate(s['labels'])if 'line'in l and 0 in l['line']}|{35};A=set(range(n))-P-{36}
Cs=json.loads(Path('outputs/agent_near_fano_outside_control_probe.json').read_text())['results'];pw=w[:,None]*w[None,:];pw[np.diag_indices(n)]=w*(w-1)
keeps6=list(combinations(range(8),5));keeps7=list(combinations(range(8),6))
def graph(keep):
 mask=sum(1<<j for j in keep);return((m[:,None]|m[None,:])&mask)==mask
adj6=np.array([graph(k)for k in keeps6]);adj7=np.array([graph(k)for k in keeps7])
found=[]
for candidate in Cs:
 C=set(candidate['C']);H=(A-{37})|C;h=np.array([i in H for i in range(n)]);touch=h[:,None]|h[None,:]
 assert sum(w[i]for i in H)==144*s['b']
 aa=adj6&touch;aa[:,35,35]=False
 ep=np.sum(np.any(aa,axis=2)*w,axis=1);qq=np.sum((adj6&touch)*pw,axis=(1,2))//2
 if np.any(ep<s['p'])or np.any((ep==s['p'])&(qq<s['Q'])):continue
 q7=np.sum((adj7&touch)*pw,axis=(1,2))//2
 if np.any(q7==0):continue
 found={'C':sorted(C),'D2':sorted((P-C)|{36}),'G':sorted(G),'H':sorted(H),'weights':w.tolist(),'masks':(m|(h.astype(np.int64)<<8)).tolist(),'min_new_endpoint':int(ep.min()),'min_new_seven_pairs':int(q7.min()),'rank_H':int(w[h].sum())}
 print(json.dumps({k:v for k,v in found.items()if k not in ['weights','masks','G','H','D2']},indent=2));break
Path('outputs/agent_near_fano_outside_control_response.json').write_text(json.dumps({'found':found,'p':s['p'],'Q':s['Q'],'b':s['b']},indent=2));print('found',bool(found))
