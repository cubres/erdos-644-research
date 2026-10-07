"""Exact one-step survivor after deleting the whole known outside cloud."""
from fractions import Fraction as F
import json
from pathlib import Path
from p644_agent_global_mask_check import verify

def main():
 input_path=Path('outputs/agent_global_distant_outside_survivor.json')
 data=json.loads(input_path.read_text());old=data['atoms'];w=[F(a['mass']) for a in old]
 r=list(map(F,['21/100','1/25','1/5','31/200','1/8','0','0','2/25','0','0','0','3/40','21/200','1/100','0']))
 s=[v-x if i!=14 else F(0) for i,(v,x) in enumerate(zip(w,r))]
 caps=w.copy()
 for i in [5,6,9,10,14]:caps[i]=0
 caps[4]=F(1,8)
 assert sum(v-u for v,u in zip(w,caps))==F(3,4)
 assert all(x<=u for x,u in zip(r,caps))
 assert sum(r)==sum(s)==1
 assert r[14]==s[14]==0
 atoms=[]
 for i,(o,v,x,y) in enumerate(zip(old,w,r,s)):
  assert x+y<=v
  for z,mask,label in [(x,o['mask']|1<<12,'newR'),(y,o['mask']|1<<13,'newS'),(v-x-y,o['mask'],'neither')]:
   if z:atoms.append((mask,z,f'{i}:{label}'))
 checks=verify(atoms,7)
 assert checks['minimum_all_six_endpoint_mass']=='183/200'
 newq=[F(q['Q']) for q in checks['paired_Q'] if 7 in q['pairs'] and len(set(q['pairs']))==3]
 assert min(newq)==F(257,1000)
 out={'status':'Exact targeted outside-control survivor, not a large-transversal family',
      'input':str(input_path),'c':'6/25','deletion_mass':'3/4',
      'deletion_description':'Entire old outside part, C union D, and half of B_H intersect oldR',
      'remaining_old_atom_capacities':list(map(str,caps)),
      'newR_old_atom_masses':list(map(str,r)),'newS_old_atom_masses':list(map(str,s)),
      'new_outside_mass':'0','minimum_new_distinct_paired_Q':str(min(newq)),
      'atoms':[{'mask':m,'mass':str(v),'label':label} for m,v,label in atoms],
      **checks}
 path=Path('outputs/agent_global_outside_control_survivor.json');path.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ['atoms','paired_Q']},indent=2));print(path)

if __name__=='__main__':main()
