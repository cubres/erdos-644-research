"""Exact optimized-request branches: one closed, one neighborhood survivor.
Includes continuous partial masses; standard library only.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

lines=[frozenset(t) for t in combinations(range(7),3)if(t[0]+1)^(t[1]+1)^(t[2]+1)==0]
T=[(L,L,None,(33,0))for L in lines]+[(L|{h},L,h,(1,0))for L in lines for h in sorted(set(range(7))-L)]
xline=frozenset((0,1,2));w=[];old=[]
for typ,L,h,ww in T:
    old.append(127^sum(1<<j for j in typ));w.append((33,-1)if L==xline and h is None else ww)
old += [(127^sum(1<<j for j in xline))|1,0];w += [(0,1),(1,0)]
D1={i for i,m in enumerate(old)if sum(bool(m&(1<<j))<<q for q,j in enumerate([2,4,5,6]))in[2,6,9,11,13]}

def sumw(ids,weights):return tuple(sum(weights[i][j]for i in ids)for j in range(2))
def add(u,v):return tuple(a+b for a,b in zip(u,v))
def graph(rows,masks,weights):
    mask=sum(1<<j for j in rows);n=len(weights)
    edges=[(i,j)for i in range(n)for j in range(i+1,n)if(masks[i]|masks[j])&mask==mask]
    ends={i for pair in edges for i in pair};q=(F(0),F(0),F(0))
    for i,j in edges:
        a,c=weights[i];b,d=weights[j];q=add(q,(a*b,a*d+b*c,c*d))
    for i in range(n):
        if masks[i]&mask==mask:
            assert i in ends
            a,c=weights[i];q=add(q,(F(a*a,2),F(2*a*c-a,2),F(c*c-c,2)))
    return sumw(ends,weights),q

def certify_response(masks,weights,G,family_size=8):
    assert sumw(G,weights)==(144,0)
    assert not(G&D1)
    for rows in combinations(range(family_size),6):
        ep,q=graph(rows,masks,weights);d=(ep[0]-111,ep[1])
        assert d[0]>=0 and sum(d)>=0,(rows,ep)
        if d==(0,0):
            q=add(q,(-3669,0,0));assert min(q[0],2*q[0]+q[1],sum(q))>=0
        elif sum(d)==0:assert sum(q)>=3669
    for rows in combinations(range(family_size),7):
        ep,q=graph(rows,masks,weights);assert min(q[0],2*q[0]+q[1])>=0 and sum(q)>0
    assert graph(range(1,7),masks,weights)==((111,0),(3669,0,0))

assert sumw(D1,w)==(108,0)
# Sparse response from the numerical discovery, now reconstructed exactly.
sparseG={0,2,4,6,20,22,23,24,25,26,29,31,32,33,34,35,36}
sparsem=[m|(int(i in sparseG)<<7)for i,m in enumerate(old)]
certify_response(sparsem,w,sparseG)
rows=(2,4,5,6,7);mask=sum(1<<j for j in rows)
Sfull={1,2,8,11,12,13,17,18,22};Spart=26
selected={i:w[i]for i in Sfull};selected[Spart]=(0,1)
assert add(sumw(Sfull,w),(0,1))==(73,1)
N={j for i in selected for j in range(len(w))if(sparsem[i]|sparsem[j])&mask==mask}
D=sumw(N,w)
for i,ww in selected.items():
    if i not in N:D=add(D,ww)
assert D==(108,1)
assert graph(rows,sparsem,w)[0]==(184,0)

# Dense response: move all8b of rank deficit to the four-row nonendpoint base245.
densew=w+[(8,0)];densew[6]=(25,0)
denseold=old+[old[6]]
denseG=set(range(len(old)))-D1
densem=[m|(int(i in denseG)<<7)for i,m in enumerate(denseold)]
certify_response(densem,densew,denseG)
# The optimizer's static second request also has an actual compatible response.
D2={i for i,m in enumerate(denseold)if sum(bool(m&(1<<j))<<q for q,j in enumerate([2,4,5,6]))in[3,10,12,13,14]}
denseH=set(range(len(old)))-D2
dense9=[m|(int(i in denseH)<<8)for i,m in enumerate(densem)]
assert sumw(D2,densew)==(108,0) and sumw(denseH,densew)==(144,0)
assert not(denseH&D2)
certify_response(dense9,densew,denseG,9)
results=[]
for keep in combinations(range(1,7),4):
    oldmask=sum(1<<j for j in keep)
    if any(m&oldmask==oldmask for m in denseold):continue
    cells=defaultdict(lambda:(0,0))
    for i,m in enumerate(densem):
        typ=sum(bool(m&(1<<j))<<q for q,j in enumerate(keep))|((i in denseG)<<4)
        cells[typ]=add(cells[typ],densew[i])
    masks=sorted(s for s in cells if any(s|t==31 for t in cells))
    assert all(cells[s][1]==0 for s in masks)
    weights=[cells[s][0]for s in masks]
    neighbors=[sum(1<<j for j,t in enumerate(masks)if s|t==31)for s in masks]
    assert all(not(neighbors[i]&(1<<i))for i in range(len(masks)))
    size=1<<len(masks);mass=[0]*size;nb=[0]*size
    for z in range(1,size):
        bit=z&-z;i=bit.bit_length()-1;prev=z^bit
        mass[z]=mass[prev]+weights[i];nb[z]=nb[prev]|neighbors[i]
    p5=sum(weights);threshold=p5-111;best=None;arg=None
    for z in range(size):
        if mass[z]<threshold:continue
        nz=nb[z]
        # Exact lower envelope allowing arbitrary continuous partial masses.
        value=mass[nz]+max(0,threshold-mass[z&nz])
        if best is None or value<best:best=value;arg=z
    assert best>=111,(keep,best)
    result={'old_rows':list(keep),'p5_over_b':p5,'weak_threshold_over_b':threshold,'merged_types':len(masks),'supports_checked':size,'weak_optimum_over_b':best,'best_declared_support':[format(masks[i],'05b')for i in range(len(masks))if arg&(1<<i)],'cells':[(format(s,'05b'),v)for s,v in zip(masks,weights)]}
    results.append(result)
    print({k:v for k,v in result.items()if k not in ['cells','best_declared_support']},flush=True)
    del mass,nb
assert len(results)==12
assert min(r['weak_optimum_over_b']for r in results)==111
out={'status':'EXACT_PASS','valid_for':'every integer b>=1','sparse_response_cover':'108b+1','dense_response_rank':'144b','dense_D1_size':'108b','dense_six_tuples':84,'dense_seven_tuples':36,'dense_neighborhood_graphs':results,'total_supports_checked':sum(r['supports_checked']for r in results),'dense_weights':densew,'dense_masks':dense9,'dense_H':sorted(denseH),'D2':sorted(D2),'sparse_G':sorted(sparseG),'dense_G':sorted(denseG),'D1':sorted(D1)}
Path('outputs/agent_near_fano_optimized_response_certificate.json').write_text(json.dumps(out,indent=2))
print('PASS total supports',out['total_supports_checked'])
