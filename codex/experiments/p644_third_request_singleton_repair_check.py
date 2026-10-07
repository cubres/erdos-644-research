"""Exact third-response template failure and its singleton repair.
Only new six/seven subfamilies are checked; the unchanged nine-row input
was already independently certified. Standard library, all integer b>=1.
"""
from itertools import combinations
from pathlib import Path
import json

src=json.loads(Path('outputs/agent_near_fano_outside_control_certificate.json').read_text())
w=[tuple(v)for v in src['weights']];old=list(src['masks'])
G=set(src['G']);H=set(src['H']);I=G&H;R={37};M=set(range(len(w)))-(I|R)
X={1,7,11,12,13};D=I|X;J0=M-X

def mass(ids,ww):return tuple(sum(ww[i][j]for i in ids)for j in range(2))
def graph(rows,masks,ww):
 full=sum(1<<r for r in rows)
 ep={v for i in range(len(ww))for j in range(i+1,len(ww))if(masks[i]|masks[j])&full==full for v in (i,j)}
 return ep,mass(ep,ww)
assert mass(X,w)==(37,0) and mass(D,w)==(108,0) and mass(J0,w)==(144,0)
base=[m|(int(i in J0)<<9)for i,m in enumerate(old)]
critical=(1,2,6,7,8,9)
ep0,p0=graph(critical,base,w)
assert p0==(104,0)
# Existing five rows have empty common intersection. Thus arbitrary new
# points outside the old union V cannot supply an endpoint for this core.
five_mask=sum(1<<r for r in critical if r!=9)
assert not any(m&five_mask==five_mask for m in old)
# Split one point from a retained base cell and one from discarded R.
w[0]=(w[0][0],w[0][1]-1);w.append((0,1));old.append(old[0]);removed=38
w[37]=(w[37][0],w[37][1]-1);w.append((0,1));old.append(old[37]);added=39
J=J0|{added}
masks=[m|(int(i in J)<<9)for i,m in enumerate(old)]
assert all(a>=0 and a+d>0 for a,d in w)
assert mass(J,w)==(144,0) and mass(D,w)==(108,0) and not(J&D)
assert removed not in J and added in J and not(37 in J)
assert graph(critical,masks,w)[1]==(142,1)
# Exactly38b other endpoints become active from the one R-point.
new_neighbors={j for j in range(len(w))if j!=added and (old[added]|old[j])&five_mask==five_mask}
assert mass(new_neighbors,w)==(38,0)
new_six=[]
for rows in combinations(range(9),5):
 ep,value=graph(rows+(9,),masks,w)
 assert value[0]>=111 and value[0]+value[1]>111,(rows,value)
 new_six.append({'old_rows':rows,'endpoint_affine_b':value})
new_seven=[]
for rows in combinations(range(9),6):
 ep,value=graph(rows+(9,),masks,w)
 assert ep
 new_seven.append(rows)
assert len(new_six)==126 and len(new_seven)==84
out={'status':'EXACT_PASS','valid_for':'every integer b>=1','request_size':'108b','response_rank':'144b','failed_template_endpoint':'104b','repaired_critical_endpoint':'142b+1','activated_neighbor_mass':'38b','new_six_tuples':126,'new_seven_tuples':84,'old_nine_row_certificate':'agent_near_fano_outside_control_certificate.json','D3':sorted(D),'X':sorted(X),'J':sorted(J),'weights_affine_b':w,'masks':masks,'six_table':new_six}
Path('outputs/root_third_request_singleton_repair_certificate.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items()if k not in ['D3','X','J','weights_affine_b','masks','six_table']},indent=2))
