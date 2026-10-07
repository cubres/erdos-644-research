"""Exact certificate: every37b redistribution preserves the seven-row property.
Input: the previously verified nine-row actual outside-control instance.
No floating point or positive-occupancy cutoff. This does NOT certify
six-row endpoint minimality for all redistributions.
Also checks the larger domain M=B union E, including removal from B.
"""
from pathlib import Path
from itertools import combinations
import json

src=json.loads(Path('outputs/agent_near_fano_outside_control_certificate.json').read_text())
w=[tuple(v)for v in src['weights']]; masks=src['masks']
G=set(src['G']); H=set(src['H']); I=G&H; E=G^H; R={37}
B=set(range(len(w)))-(G|H|R)
def mass(ids):return tuple(sum(w[i][j]for i in ids)for j in range(2))
assert mass(I)==(71,0) and mass(E)==(146,0) and mass(B)==(35,0)
assert mass(R)==(8,0) and not(R&(G|H))
assert all(a>=0 and a+d>0 for a,d in w)
M=B|E
assert mass(M)==(181,0)
records=[]; exceptions=[]; enlarged=[]
for rows in combinations(range(9),6):
 full=sum(1<<r for r in rows)
 ends=set()
 for i in range(len(w)):
  for j in range(i+1,len(w)):
   if (masks[i]|masks[j])&full==full:ends.update((i,j))
 # If a cell is a common point it has a partner in any other positive
 # cell, so the distinct-cell loop above already includes its endpoints.
 available=mass(ends&M)
 assert available[0]>=39 and available[0]-39+available[1]>=0
 enlarged.append({'rows':list(rows),'M_endpoint_mass':available})
 fixed=ends&B
 if fixed:
  method='fixed endpoint in B'; remaining=mass(fixed)
 else:
  method='endpoint mass in E exceeds37b'; remaining=mass(ends&E)
  assert remaining[0]>37 and remaining[0]-37+remaining[1]>0
  exceptions.append({'rows':list(rows),'E_endpoint_mass':remaining})
 records.append({'rows':list(rows),'method':method,'mass_affine_b':remaining})
assert len(exceptions)==10
assert sorted(set(tuple(e['E_endpoint_mass'])for e in exceptions))==[(107,0),(108,0),(143,0)]
result={'status':'EXACT_PASS','valid_for':'every integer b>=1 and every actual X subset M=B union E with cardinality37b','old_six_tuples':len(records),'tuples_hitting_fixed_B':len(records)-len(exceptions),'B_free_tuples':exceptions,'D3_size':'108b','J_size':'144b','new_seven_row_property':'verified uniformly in X','six_row_minimum':'NOT ASSERTED','minimum_M_endpoint_mass':'39b','enlarged_domain_checks':enlarged,'partition':{'I':sorted(I),'E':sorted(E),'B':sorted(B),'R':sorted(R)}}
Path('outputs/root_third_request_seven_robust.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items()if k not in ['partition','B_free_tuples','enlarged_domain_checks']},indent=2))
