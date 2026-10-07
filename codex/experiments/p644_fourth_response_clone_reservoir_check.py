"""Exact clone-reservoir mechanism, not a high-transversal counterexample.
All8b choices of the activating R point coexist. Symmetry reduces every
six/seven-row subfamily to at most seven selected clone rows.
"""
from itertools import combinations
from fractions import Fraction as F
from pathlib import Path
import json
src=json.loads(Path('outputs/agent_near_fano_outside_control_certificate.json').read_text())
oldw=[tuple(v)for v in src['weights']];oldm=src['masks'];I=set(src['G'])&set(src['H']);X={1,7,11,12,13};D3=I|X
J0=set(range(len(oldw)))-(I|{37}|X)

def add(u,v):return tuple(a+b for a,b in zip(u,v))
def mass(ids,w):return tuple(sum(w[i][j]for i in ids)for j in range(2))
def graph(rows,m,w):
 full=sum(1<<j for j in rows);ep=set();Q=(F(0),F(0),F(0))
 for i in range(len(w)):
  a,c=w[i]
  for j in range(i+1,len(w)):
   if(m[i]|m[j])&full==full:
    ep|={i,j};d,e=w[j];Q=add(Q,(a*d,a*e+c*d,c*e))
  if m[i]&full==full:Q=add(Q,(F(a*a,2),F(2*a*c-a,2),F(c*c-c,2)))
 return mass(ep,w),Q

def state(q):
 w=oldw[:];m=oldm[:]
 # z is excluded from every clone; singletonx stays in the common core.
 w[0]=(33,-2);w.append((0,1));m.append(m[0])
 w[37]=(8,-q)
 for _ in range(q):w.append((0,1));m.append(oldm[37])
 for t in range(q):
  for i in J0|{39+t}:m[i]|=1<<(9+t)
 return w,m
six=[];seven=[]
for q in range(1,8):
 w,m=state(q);assert all(a>=0 and a+c>0 for a,c in w)
 clones=tuple(range(9,9+q))
 for row in clones:assert mass((i for i,v in enumerate(m)if v&(1<<row)),w)==(144,0)
 if q<=6:
  for rows in combinations(range(9),6-q):
   p,Q=graph(rows+clones,m,w);d=(p[0]-111,p[1])
   assert d[0]>=0 and sum(d)>=0,('six',q,rows,p)
   if d==(0,0):
    dQ=add(Q,(-3669,0,0));assert min(dQ[0],2*dQ[0]+dQ[1],sum(dQ))>=0
   elif sum(d)==0:assert sum(Q)>=3669
   six.append({'clones':q,'old_rows':rows,'endpoint':p})
 for rows in combinations(range(9),7-q):
  p,Q=graph(rows+clones,m,w)
  assert Q[0]>=0 and 2*Q[0]+Q[1]>=0 and sum(Q)>0,('seven',q,rows,Q)
  seven.append({'clones':q,'old_rows':rows})
 print('PASS selected clones',q,flush=True)
# Three cells yield a minimum cover with any specified clone point.
w,m=state(1);full=(1<<10)-1
assert m[1]|m[9]|m[39]==full
assert not any((m[i]|m[j])==full for i in range(len(m))for j in range(i+1,len(m)))
# Uniform three-point cover of the ENTIRE clone family, independent ofr.
w,m=state(7);full=(1<<16)-1
fixed=next(z for z in combinations(range(len(w)),3)if(m[z[0]]|m[z[1]]|m[z[2]])==full)
assert all(i<39 for i in fixed)
result={'status':'EXACT_PASS','valid_for':'all integer b>=1, family contains all8b distinct clone rows','clone_common_core':'J0 minus one fixed point z','clone_rows':'Q union {r}, r in R','rank':'144b+1','reservoir_size':'8b','new_six_symmetry_cases':len(six),'new_seven_symmetry_cases':len(seven),'minimum_endpoint':'111b','pair_minimum_at_endpoint_minimum':'3669b^2','ten_row_cover_indices_with_r':[1,9,39],'uniform_family_cover_indices':list(fixed),'family_tau':3,'six':six}
Path('outputs/agent_fourth_response_clone_reservoir_certificate.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items()if k!='six'},indent=2))
