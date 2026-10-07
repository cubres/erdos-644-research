"""Exact fourth response excluding entire activating reservoirR, all b>=1."""
from itertools import combinations
from pathlib import Path
import json
s=json.loads(Path('outputs/root_third_request_singleton_repair_certificate.json').read_text());nine=json.loads(Path('outputs/agent_near_fano_outside_control_certificate.json').read_text())
w=[tuple(v)for v in s['weights_affine_b']];m=list(s['masks']);I=set(nine['G'])&set(nine['H']);T={9,15,22,24};D=(I-T)|{1,37,39}
# Omit8b ordinary points of base012 but retain25b-2 points of that sameoldtype.
w[0]=(25,-2);w.append((8,0));m.append(m[0]);cut=40
K=set(range(40))-D
m=[v|(int(i in K)<<10)for i,v in enumerate(m)]
def mass(ids):return tuple(sum(w[i][j]for i in ids)for j in range(2))
def graph(rows):
 mask=sum(1<<j for j in rows);ep={v for i in range(len(w))for j in range(i+1,len(w))if(m[i]|m[j])&mask==mask for v in(i,j)}
 return mass(ep),ep
assert all(a>=0 and a+c>0 for a,c in w)
assert mass(D)==(108,0) and mass(K)==(144,0) and not(K&D)
assert 39 in D and {37,39}<=D and 1 in D and 20 in D
assert(m[1]|m[20]|m[39])&((1<<10)-1)==(1<<10)-1
new6=[]
for rows in combinations(range(10),5):
 p,ep=graph(rows+(10,));assert p[0]>=111 and p[0]+p[1]>111,(rows,p)
 new6.append({'old_rows':rows,'endpoint':p})
for rows in combinations(range(10),6):assert graph(rows+(10,))[1]
for item in new6:
 p=item['endpoint'];assert p[0]>=177 and (p[0]-177)+p[1]>=0
minimum=min(r['endpoint'][0]*100+r['endpoint'][1]for r in new6)
closest=[r for r in new6 if r['endpoint'][0]*100+r['endpoint'][1]==minimum]
out={'status':'EXACT_PASS','valid_for':'every integer b>=1','D4':'R union base034 union (I minus T)','T':[9,15,22,24],'D4_size':'108b','K_rank':'144b','all_R_excluded':True,'excluded_minimum_cover_cells':[1,20,39],'trimmed_base012_mass':'8b','retained_same_type_mass':'25b-2','new_six_tuples':252,'new_seven_tuples':210,'closest_new_six':closest,'weights_affine_b':w,'masks':m,'D4':sorted(D),'K':sorted(K)}
Path('outputs/agent_fourth_response_full_R_certificate.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items()if k not in ['weights_affine_b','masks','D4','K']},indent=2))
