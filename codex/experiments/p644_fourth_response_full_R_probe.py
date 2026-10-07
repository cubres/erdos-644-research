"""Structured fourth request: allR+base034+I minus four defect classes.
Positive witnesses/forcing upper graphs only; no solver infeasibility claims.
"""
from itertools import combinations
from pathlib import Path
import json
import numpy as np
s=json.loads(Path('outputs/root_third_request_singleton_repair_certificate.json').read_text());nine=json.loads(Path('outputs/agent_near_fano_outside_control_certificate.json').read_text());w=np.array([a*100+c for a,c in s['weights_affine_b']]);m=np.array(s['masks']);n=len(w)
I=set(nine['G'])&set(nine['H']);Id=sorted(I-{4,6});R={37,39};B={1};baseD=I|R|B
keeps=[];graphs=[]
for rows in combinations(range(10),5):
 mask=sum(1<<j for j in rows)
 if np.any(m&mask==mask):continue
 keeps.append(rows);graphs.append(((m[:,None]|m[None,:])&mask)==mask)
graphs=np.array(graphs);elig=np.any(graphs,axis=2);results=[]
for T in combinations(Id,4):
 D=baseD-set(T);k=np.array([i not in D for i in range(n)])
 ends=np.any(graphs[:,:,k],axis=2)|(k&elig);pp=np.sum(ends*w,axis=1);j=int(np.argmin(pp))
 results.append({'T':T,'D':sorted(D),'min_max_endpoint':int(pp[j]),'old_five':keeps[j]})
results.sort(key=lambda x:x['min_max_endpoint']);Path('outputs/agent_fourth_response_full_R_probe.json').write_text(json.dumps({'candidates':len(results),'finite_five_cores':len(keeps),'results':results},indent=2));print(json.dumps({'count':len(results),'finite_cores':len(keeps),'best':results[:6]},indent=2))
