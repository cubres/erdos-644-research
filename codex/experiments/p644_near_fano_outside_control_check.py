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
weights=w+[(8,0)];weights[6]=(25,0)
oldm=old+[old[6]]
G=set(range(len(old)))-D1
P={i for i,(_,L,_,_)in enumerate(T)if 0 in L}|{35}
A=set(range(len(weights)))-P-{36}
C={9,10,15,16}
D2=(P-C)|{36}
H=(A-{37})|C
masks=[m|(int(i in G)<<7)|(int(i in H)<<8)for i,m in enumerate(oldm)]
assert sumw(D2,weights)==(108,0) and sumw(H,weights)==(144,0)
assert not(H&D2) and 36 not in H
certify_response(masks,weights,G,9)
new=[]
for rows in combinations(range(9),6):
 if 8 in rows:
  ep,q=graph(rows,masks,weights);new.append({'rows':list(rows),'endpoint':ep,'pairs':[str(v)for v in q]})
closest=min(sum(r['endpoint'][i]*[100,1][i]for i in range(2))for r in new)
closest_rows=[r for r in new if r['endpoint'][0]*100+r['endpoint'][1]==closest]
safe=graph([1,2,5,6,7,8],masks,weights)
result={'status':'EXACT_PASS','valid_for':'every integer b>=1','rank':'144b+1','D1_size':'108b','D2_size':'108b','G_outside':'Y of b points','H_outside':'empty','six_tuples':84,'seven_tuples':36,'global_minimum':['111b','3669b^2'],'weights':weights,'masks':masks,'G':sorted(G),'H':sorted(H),'D1':sorted(D1),'D2':sorted(D2),'C':sorted(C),'closest_new_six_tuples':closest_rows,'safe_core_endpoint':safe[0]}
Path('outputs/agent_near_fano_outside_control_certificate.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items()if k not in ['weights','masks','G','H','D1','D2']},indent=2))
