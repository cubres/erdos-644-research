"""Positive finite witness for a singleton-P second request, assuming p=t."""
from itertools import combinations
import json
from pathlib import Path
import numpy as np
src=json.loads(Path('outputs/agent_near_fano_first_response_discovery.json').read_text())
p=src['p'];Q=src['Q'];basew=src['weights'];basem=src['old_masks'];gset=set(src['found'][0]['selected']);removed=src['found'][0]['removed']
found=[]
for zsource in src['allowed']:
    w=np.array(basew+[1],dtype=np.int64);w[zsource]-=1
    masks=np.array(basem+[basem[zsource]],dtype=np.int64)
    g=np.array([i in gset for i in range(len(basew))]+[True])
    masks |= g.astype(np.int64)<<7
    n=len(w);pairw=w[:,None]*w[None,:];pairw[np.diag_indices(n)]=w*(w-1)
    def potential(mask):
        adj=((masks[:,None]|masks[None,:])&mask)==mask
        aa=adj.copy()
        for i in range(n):
            if w[i]==1:aa[i,i]=False
        return int(w[np.any(aa,axis=1)].sum()),int(np.sum(adj*pairw)//2)
    assert all(potential(sum(1<<j for j in keep))[1]>0 for keep in combinations(range(8),7))
    for added in combinations(removed,3):
        hset=(gset-set(src['allowed']))|set(added)|{len(basew)}
        h=np.array([i in hset for i in range(n)])
        masks=(masks&255)|(h.astype(np.int64)<<8)
        val6=[potential(sum(1<<j for j in keep)) for keep in combinations(range(9),6)]
        if not all(pp>=p and(pp>p or qq>=Q) for pp,qq in val6):continue
        val7=[potential(sum(1<<j for j in keep)) for keep in combinations(range(9),7)]
        if not all(qq>0 for pp,qq in val7):continue
        new6=[potential(sum(1<<j for j in keep)) for keep in combinations(range(9),6) if 7 in keep and 8 in keep]
        found.append({'zsource':zsource,'added':added,'weights':w.tolist(),'masks':masks.tolist(),'G':sorted(gset|{len(basew)}),'H':sorted(hset),'minimum_double_replacement_endpoint':min(pp for pp,qq in new6),'minimum_double_replacement_pairs':min(qq for pp,qq in new6),'min_seven_pair_count':min(qq for pp,qq in val7),'all_six_potentials':val6})
        print({k:v for k,v in found[-1].items() if k not in ['weights','masks','all_six_potentials','G','H']},flush=True)
        break
out={'source':'agent_near_fano_first_response_discovery.json','k':src['k'],'p':p,'Q':Q,'b':src['b'],'found':found}
Path('outputs/agent_near_fano_two_response_singleton.json').write_text(json.dumps(out,indent=2))
print('found',len(found))
