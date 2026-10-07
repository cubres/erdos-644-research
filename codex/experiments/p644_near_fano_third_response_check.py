"""Exact third actual response, all even b>=2. Standard library only.
Input is the previously certified nine-row family; this independently
rechecks every six/seven subfamily after adjoining the new response.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

src=json.loads(Path('outputs/agent_near_fano_outside_control_certificate.json').read_text())
# Normalize b=2c, c>=1. No fractional point cardinalities remain.
w=[(2*a,d)for a,d in src['weights']];m=list(src['masks'])
I={i for i,v in enumerate(m)if v&(1<<7)and v&(1<<8)}
cut=[0,3]
for i in cut:
    a,d=w[i];w[i]=(a-37,d)
    w.append((37,0));m.append(m[i])
D3=I|{38,39};R={37}
J=set(range(len(w)))-D3-R
m=[v|(int(i in J)<<9)for i,v in enumerate(m)]

def add(u,v):return tuple(a+b for a,b in zip(u,v))
def total(ids):return tuple(sum(w[i][j]for i in ids)for j in range(2))
def graph(rows):
    mask=sum(1<<j for j in rows);n=len(w);ends=set();q=(F(0),F(0),F(0))
    for i in range(n):
        a,d=w[i]
        for j in range(i+1,n):
            if(m[i]|m[j])&mask==mask:
                ends.add(i);ends.add(j);b,e=w[j];q=add(q,(a*b,a*e+b*d,d*e))
        if m[i]&mask==mask:q=add(q,(F(a*a,2),F(2*a*d-a,2),F(d*d-d,2)))
    return total(ends),q

assert all(a>=0 and a+d>0 for a,d in w)
assert total(I)==(142,0)
assert total(D3)==(216,0) and total(J)==(288,0)
assert not(D3&J) and 35 in J and 36 in J and 37 not in J
assert not any(v&(1<<7)and v&(1<<8)and v&(1<<9)for v in m)
assert total(i for i,v in enumerate(m)if v&(1<<7)and v&(1<<9))==(109,0)
assert total(i for i,v in enumerate(m)if v&(1<<8)and v&(1<<9))==(109,0)
six=[]
for rows in combinations(range(10),6):
    ep,q=graph(rows);delta=(ep[0]-222,ep[1])
    assert delta[0]>=0 and sum(delta)>=0,(rows,ep)
    if delta==(0,0):
        dq=add(q,(-14676,0,0));assert min(dq[0],2*dq[0]+dq[1],sum(dq))>=0,(rows,q)
    elif sum(delta)==0:assert sum(q)>=14676
    six.append((rows,ep,q))
for rows in combinations(range(10),7):
    ep,q=graph(rows);assert min(q[0],2*q[0]+q[1])>=0 and sum(q)>0,(rows,q)
assert graph(range(1,7))==((222,0),(14676,0,0))
new_min=min(ep[0]*50+ep[1]for rows,ep,q in six if 9 in rows)
closest=[{'rows':rows,'endpoint_in_c':ep,'pair_coefficients_in_c':[str(x)for x in q]}for rows,ep,q in six if 9 in rows and ep[0]*50+ep[1]==new_min]
out={'status':'EXACT_PASS','parameter':'b=2c for every integer c>=1','six_tuples':210,'seven_tuples':120,'rank':'144b+1','J_rank':'144b','D3_size':'108b','G_H_J_intersection':0,'G_J_intersection':'109c=54.5b','H_J_intersection':'109c=54.5b','minimum_endpoint':'111b','minimum_pair_at_endpoint_minimum':'3669b^2','weights_affine_c':w,'masks':m,'D3':sorted(D3),'J':sorted(J),'closest_six_with_J':closest}
Path('outputs/agent_near_fano_third_response_certificate.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items()if k not in ['weights_affine_c','masks','D3','J']},indent=2))
