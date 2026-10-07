"""Independent standard-library exact check of the finite b100 certificate.
No MILP, floating point, positive-cell cutoff, or claimed asymptotic scaling.
"""
from itertools import combinations
from pathlib import Path
import json

src=json.loads(Path('outputs/agent_shared_witness_transport_discovery.json').read_text())
old=json.loads(Path('outputs/agent_near_fano_outside_control_certificate.json').read_text())
b=src['b'];assert b==100
cells=src['cells'];assert all(isinstance(c['weight'],int)and c['weight']>0 for c in cells)
I=set(old['G'])&set(old['H']);X={1,7,11,12,13};J0=set(range(len(old['weights'])))-(I|X|{37})
oldweights=[a*b+d for a,d in old['weights']]
for i in range(len(oldweights)):
 group=[c for c in cells if c['source']==i or(i==0 and c['source']==38)]
 assert sum(c['weight']for c in group)==oldweights[i]
 for c in group:assert c['old_mask']==old['masks'][i]
for c in cells:
 assert c['Q']==(c['source']in J0 and c['source']!=38)
assert sum(c['weight']for c in cells)==26000
assert sum(c['weight']for c in cells if c['Q'])==14399
assert len([c for c in cells if c['label']=='x'])==1
assert len([c for c in cells if c['label']=='z'])==1
assert all(c['weight']==1 for c in cells if c['label']in['x','z'])
R=[i for i,c in enumerate(cells)if c['label']=='R'];assert len(R)==1 and cells[R[0]]['weight']==800
base_masks=[c['old_mask']|(c['witness_mask']<<9)for c in cells]
for row in range(15):
 expected=14401 if row==0 else 14400
 assert sum(c['weight']for c,m in zip(cells,base_masks)if m&(1<<row))==expected

class PairGraph:
 def __init__(self,m,w,nrows):
  self.m=m;self.w=w;self.all=(1<<len(m))-1
  self.rowsets=[sum(1<<i for i,v in enumerate(m)if v&(1<<r))for r in range(nrows)]
  self.cache={0:self.all};self.masscache={0:0}
 def partners(self,demand):
  value=self.cache.get(demand)
  if value is None:
   bit=demand&-demand;value=self.partners(demand^bit)&self.rowsets[bit.bit_length()-1];self.cache[demand]=value
  return value
 def mass(self,bits):
  value=self.masscache.get(bits)
  if value is None:
   value=0;bb=bits
   while bb:
    bit=bb&-bb;value+=self.w[bit.bit_length()-1];bb^=bit
   self.masscache[bits]=value
  return value
 def endpoint(self,S):return sum(ww for mm,ww in zip(self.m,self.w)if self.partners(S&~mm))
 def pairs(self,S):
  ordered=sum(ww*self.mass(self.partners(S&~mm))for mm,ww in zip(self.m,self.w))
  ordered-=sum(ww for mm,ww in zip(self.m,self.w)if mm&S==S)
  assert ordered%2==0
  return ordered//2
 def has_pair(self,S):
  # A zero demand has all26000 points as partners, so distinctness is automatic.
  return any(self.partners(S&~mm)for mm in self.m)

# The shared witnesses have the exact required endpoint set and pair count.
g=PairGraph(base_masks,[c['weight']for c in cells],15)
Wmask=sum(1<<j for j in range(9,15))
ep=[i for i,m in enumerate(base_masks)if g.partners(Wmask&~m)]
assert sum(cells[i]['weight']for i in ep)==11100
assert all(not cells[i]['Q']for i in ep)and set(R)<=set(ep)
assert set(ep)=={i for i,c in enumerate(cells)if c['label']in['B','R']}
assert g.pairs(Wmask)==36690000
# Q together with the six witnesses is a MINIMAL bad seven-tuple.
q_masks=[c['witness_mask']|(int(c['Q'])<<6)for c in cells]
qg=PairGraph(q_masks,[c['weight']for c in cells],7)
assert not qg.has_pair(127)
for omitted in range(7):assert qg.has_pair(127^(1<<omitted))

results=[];ties=[]
for q in range(8):
 clonebits=((1<<q)-1)<<15;m=[];w=[]
 for c,mm in zip(cells,base_masks):
  if c['label']=='R':
   m.append(mm);w.append(c['weight']-q)
   for j in range(q):m.append(mm|(1<<(15+j)));w.append(1)
  else:m.append(mm|(clonebits if c['Q']else 0));w.append(c['weight'])
 assert min(w)>0
 pg=PairGraph(m,w,15+q);count6=count7=0;minp=None
 if q<=6:
  for rows in combinations(range(15),6-q):
   S=clonebits|sum(1<<j for j in rows);p=pg.endpoint(S)
   assert p>=11100,(q,rows,p)
   if p==11100:
    pairs=pg.pairs(S);assert pairs>=36690000,(q,rows,pairs)
    ties.append({'selected_clones':q,'base_rows':rows,'pairs':pairs})
   minp=p if minp is None else min(minp,p);count6+=1
 for rows in combinations(range(15),7-q):
  S=clonebits|sum(1<<j for j in rows);assert pg.has_pair(S),(q,rows);count7+=1
 results.append({'selected_clones':q,'six_cases':count6,'seven_cases':count7,'minimum_endpoint':minp})
 print(results[-1],flush=True)
# Find a three-point cover of ALL815 rows: one selected point inQ hits everyclone.
full=(1<<15)-1;cover=None
for i,j in combinations(range(len(cells)),2):
 need=full&~(base_masks[i]|base_masks[j]);possible=g.partners(need)&~((1<<i)|(1<<j))
 if not(cells[i]['Q']or cells[j]['Q']):possible&=sum(1<<h for h,c in enumerate(cells)if c['Q'])
 if possible:
  k=(possible&-possible).bit_length()-1;cover=(i,j,k);break
assert cover is not None
assert base_masks[cover[0]]|base_masks[cover[1]]|base_masks[cover[2]]==full
assert any(cells[i]['Q']for i in cover)
# No pair hits even the oldnine plus one clone, proving tau>=3.
oneclone_masks=[c['old_mask']|(int(c['Q'])<<9)for c in cells]
# Designate one point ofR as theclone activator and leave799 old-identical points.
onew=[c['weight']for c in cells];onew[R[0]]-=1
oneclone_masks.append(oneclone_masks[R[0]]|(1<<9));onew.append(1)
assert not PairGraph(oneclone_masks,onew,10).has_pair((1<<10)-1)
assert sum(r['six_cases']for r in results)==9949
assert sum(r['seven_cases']for r in results)==16384
out={'status':'EXACT_PASS','b':100,'rank':14401,'actual_rows':815,'old_rows':9,'new_witness_rows':6,'clone_rows':800,'ground_points':26000,'Q_size':14399,'R_size':800,'witness_endpoint_size':11100,'witness_pair_count':36690000,'Q_plus_witnesses':'minimal bad7','all_actual_at_most7':'2-pierceable','global_six_potential':[11100,36690000],'family_tau':3,'inside_original_ground':True,'unsplit_singletons':['x','z','each selected clone activator'],'six_symmetry_cases':9949,'seven_symmetry_cases':16384,'results':results,'endpoint_minimum_ties':ties,'three_cover_cell_indices':cover,'three_cover_cells':[cells[i]for i in cover]}
Path('outputs/agent_shared_witness_transport_certificate.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items()if k not in ['results','endpoint_minimum_ties','three_cover_cells']},indent=2))
