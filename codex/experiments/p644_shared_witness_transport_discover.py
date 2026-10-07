"""Bounded structured positive witness search with exact integer cell masses.
Witnesses stay insideV. All old singleton points are kept unsplit.
"""
from itertools import combinations
from pathlib import Path
import json
import numpy as np

b=100
src=json.loads(Path('outputs/agent_near_fano_outside_control_certificate.json').read_text())
oldw=[a*b+c for a,c in src['weights']];oldm=src['masks']
I=set(src['G'])&set(src['H']);X={1,7,11,12,13};D3=I|X
J0=set(range(len(oldw)))-(D3|{37})
lines=[frozenset(t)for t in combinations(range(7),3)if(t[0]+1)^(t[1]+1)^(t[2]+1)==0]
Al=[L for L in lines if 0 not in L];Bl=[L for L in lines if 0 in L]
At=[(L,36*b)for L in Al]
Bt=[(L,33*b)for L in Bl]+[(L|{h},b)for L in Bl for h in sorted(set(range(7))-L)]

def witnessmask(t):return sum(1<<(j-1)for j in range(1,7)if j not in t)

def transport(rows,cols):
    # Every cell positive; then an integer proportional allocation followed
    # by exact residual filling. Fixed singleton rows are handled separately.
    nr,nc=len(rows),len(cols);rr=[v-nc for v in rows];cc=[v-nr for v in cols]
    assert min(rr)>=0 and min(cc)>=0 and sum(rr)==sum(cc)
    total=sum(rr);mat=[[1+(r*c//total if total else 0)for c in cc]for r in rr]
    rleft=[rows[i]-sum(mat[i])for i in range(nr)]
    cleft=[cols[j]-sum(mat[i][j]for i in range(nr))for j in range(nc)]
    i=j=0
    while i<nr and j<nc:
        v=min(rleft[i],cleft[j]);mat[i][j]+=v;rleft[i]-=v;cleft[j]-=v
        if rleft[i]==0:i+=1
        if cleft[j]==0:j+=1
    assert not any(rleft)and not any(cleft)
    return mat

cells=[]
def emit(weight,old,wm,Q,source,label):
    if weight:cells.append({'weight':weight,'old_mask':old,'witness_mask':wm,'Q':Q,'source':source,'label':label})
# z is split from ordinary base012; x stays a separate singleton.
aw=oldw[:];aw[0]-=1
arows=sorted(J0-{35})
acol=[36*b-2]+[36*b]*3
amat=transport([aw[i]for i in arows],acol)
for r,i in enumerate(arows):
 for c,(typ,_)in enumerate(At):emit(amat[r][c],oldm[i],witnessmask(typ),True,i,'A')
emit(1,oldm[35],witnessmask(Al[0]),True,35,'x')
emit(1,oldm[0],witnessmask(Al[0]),False,38,'z')
# Reserve allR for one base endpoint type, and omit5b oldbase034 points.
brows=sorted(D3);bw=[oldw[i]-(5*b if i==1 else 0)for i in brows]
bcols=[25*b]+[33*b]*2+[b]*12
bmat=transport(bw,bcols)
for r,i in enumerate(brows):
 for c,(typ,_)in enumerate(Bt):emit(bmat[r][c],oldm[i],witnessmask(typ),False,i,'B')
emit(5*b,oldm[1],0,False,1,'unused')
emit(8*b,oldm[37],witnessmask(Bl[0]),False,37,'R')
assert sum(c['weight']for c in cells)==260*b
assert sum(c['weight']for c in cells if c['Q'])==144*b-1
base_masks=[c['old_mask']|(c['witness_mask']<<9)for c in cells]
for row in range(9,15):assert sum(c['weight']for c,m in zip(cells,base_masks)if m&(1<<row))==144*b

def transform_superset(a,n):
    for bit in range(n):
        step=1<<bit;block=a.reshape(-1,2*step);block[:,:step]+=block[:,step:]
    return a

def evaluate(q):
    clonefull=((1<<q)-1)<<15
    weights=[];masks=[]
    for c,mm in zip(cells,base_masks):
        if c['label']=='R':
            weights.append(c['weight']-q);masks.append(mm)
            for j in range(q):weights.append(1);masks.append(mm|(1<<(15+j)))
        else:
            weights.append(c['weight']);masks.append(mm|(clonefull if c['Q'] else 0))
    # Merge identical complete memberships exactly.
    merge={}
    for ww,mm in zip(weights,masks):merge[mm]=merge.get(mm,0)+ww
    masks=np.array(list(merge),dtype=np.int64);weights=np.array(list(merge.values()),dtype=np.int64)
    n=15+q;universe=1<<n
    point=np.zeros(universe,dtype=np.int64);point[masks]=weights
    transform_superset(point,n)
    pair=np.zeros(universe,dtype=np.int64)
    for i in range(len(masks)):
        pair[masks[i]]+=weights[i]*(weights[i]-1)//2
        if i+1<len(masks):np.add.at(pair,masks[i]|masks[i+1:],weights[i]*weights[i+1:])
    transform_superset(pair,n)
    clonebits=((1<<q)-1)<<15
    sixm=[sum(1<<j for j in rows)|clonebits for rows in combinations(range(15),6-q)]if q<=6 else[]
    minp=10**12;bad6=[]
    for start in range(0,len(sixm),256):
        ss=np.array(sixm[start:start+256],dtype=np.int64)
        ep=np.sum((point[ss[:,None]&~masks[None,:]]>0)*weights,axis=1)
        for mm,pp in zip(ss,ep):
            minp=min(minp,int(pp))
            if pp<111*b or(pp==111*b and pair[mm]<3669*b*b):bad6.append({'mask':int(mm),'endpoint':int(pp),'pairs':int(pair[mm])})
    sevenm=[sum(1<<j for j in rows)|clonebits for rows in combinations(range(15),7-q)]
    bad7=[int(mm)for mm in sevenm if pair[mm]==0]
    result={'selected_clones':q,'positive_types':len(masks),'six_cases':len(sixm),'seven_cases':len(sevenm),'minimum_endpoint':minp if sixm else None,'bad6':bad6[:10],'bad6_count':len(bad6),'bad7':bad7[:10],'bad7_count':len(bad7)}
    print(result,flush=True)
    return result

out={'b':b,'scope':'insideV260b;oldnine+sixwitnesses+all8bclones','cells':cells,'results':[]}
for q in range(8):
    rr=evaluate(q);out['results'].append(rr)
    Path('outputs/agent_shared_witness_transport_discovery.json').write_text(json.dumps(out,indent=2))
    if rr['bad6_count']or rr['bad7_count']:break
