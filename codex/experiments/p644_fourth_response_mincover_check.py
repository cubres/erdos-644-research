"""Exact fourth response avoidingr and a minimum transversal, all b>=1."""
from itertools import combinations
from pathlib import Path
import json
src=json.loads(Path('outputs/root_third_request_singleton_repair_certificate.json').read_text())
w=[tuple(v)for v in src['weights_affine_b']];m=list(src['masks']);J=set(src['J']);D3=set(src['D3'])
# q0,q3 are ordinary common-core points, outside the restored singletonx.
w[0]=(33,-3);w.append((0,1));m.append(m[0]);q0=40
w[3]=(33,-1);w.append((0,1));m.append(m[3]);q3=41
# Three fresh points ofR, disjoint from the activatingr=index39.
w[37]=(8,-4);w.append((0,3));m.append(m[37]);fresh=42
K=(J-{39})|{fresh}
m=[v|(int(i in K)<<10)for i,v in enumerate(m)]
def mass(ids):return tuple(sum(w[i][j]for i in ids)for j in range(2))
def graph(rows):
 mask=sum(1<<j for j in rows);ep={v for i in range(len(w))for j in range(i+1,len(w))if(m[i]|m[j])&mask==mask for v in(i,j)}
 return mass(ep),ep
assert all(a>=0 and a+c>0 for a,c in w)
assert mass(K)==(144,0) and not(K&D3) and not(K&{39,q0,q3})
# D4 removes3 arbitrary points of original cell4 fromD3 and adjoinsr,q0,q3.
assert mass(D3)==(108,0) and 4 in D3 and w[4]==(33,0)
assert m[q0]|m[1]|m[q3]==(1<<10)-1 # min cover of the tenold rows
# no old two-point transversal, certified directly from actual positive types
oldfull=(1<<10)-1
assert not any((m[i]|m[j])&oldfull==oldfull for i in range(len(w))for j in range(i+1,len(w)))
new6=[]
for rows in combinations(range(10),5):
 p,ep=graph(rows+(10,));assert p[0]>=111 and p[0]+p[1]>111,(rows,p)
 new6.append({'old_rows':rows,'endpoint':p})
for rows in combinations(range(10),6):assert graph(rows+(10,))[1]
for item in new6:
 p=item['endpoint'];assert p[0]>=142 and (p[0]-142)+(p[1]-3)>=0
minimum=min(p['endpoint'][0]*100+p['endpoint'][1]for p in new6)
closest=[p for p in new6 if p['endpoint'][0]*100+p['endpoint'][1]==minimum]
out={'status':'EXACT_PASS','valid_for':'every integer b>=1','D4':'D3 minus3 points of cell4, plusr,q0,q3','D4_size':'108b','K_rank':'144b','excluded_activator':39,'excluded_minimum_cover_cells':[40,1,41],'old_family_tau':3,'fresh_R_points':3,'new_six_tuples':252,'new_seven_tuples':210,'closest_new_six':closest,'weights_affine_b':w,'masks':m,'K':sorted(K)}
Path('outputs/agent_fourth_response_mincover_certificate.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items()if k not in ['weights_affine_b','masks','K']},indent=2))
