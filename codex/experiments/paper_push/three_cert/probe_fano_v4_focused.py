"""Remaining50 CPU-second focused probe, separating known-anchor contradictions."""
import time,random,json
from fractions import Fraction as F
from pathlib import Path
from fano_v4_partner_oracle import analyse,encoded
from known_anchor_bad import known_bad
rng=random.Random(644075);start=time.process_time();limit=50.;prefix=Path(__file__).with_name('fano_v4_partner_focused')
records=[];attempts=0;known=0;genuine=0;worst=None;stop='BOUNDED_NO_COUNTERSTATE'
while time.process_time()-start<limit:
 attempts+=1;xs=[rng.randint(7500,7650) for _ in range(3)]
 lower=[2*v//3+1 for v in xs];maxe=sum(xs)-sum(lower)
 if maxe<7501:continue
 E=rng.randint(7501,min(7550,maxe));budget=sum(xs)-E-sum(lower)
 cuts=sorted([0,rng.randint(0,budget),rng.randint(0,budget),budget]);inc=[cuts[i+1]-cuts[i] for i in range(3)];rng.shuffle(inc)
 gs=[lower[i]+inc[i] for i in range(3)];rows=[]
 for i in range(3):
  rem=10000-gs[i];off=[j for j in range(3) if j!=i];q=rng.choice([0,rem,rng.randint(0,min(50,rem)),rem-rng.randint(0,min(50,rem))]);t=[0,0,0];t[i]=gs[i];t[off[0]]=q;t[off[1]]=rem-q;rows.append(t)
 x=tuple(F(v,10000) for v in xs);T=[tuple(F(v,10000) for v in t) for t in rows];bad=known_bad(x,T)
 rec={'capacities':list(map(str,x)),'types':[list(map(str,t)) for t in T],'slack_sum':str(F(E,10000)),'existing_bad_tuple':bad}
 if bad:known+=1;records.append(rec);continue
 genuine+=1;r=analyse(x,T);rec['request_cost']=str(r['request_cost']);rec['closed_box_free']=r['closed_box_free'];records.append(rec)
 if worst is None or r['request_cost']>worst['request_cost']:worst=r;prefix.with_suffix('.worst.json').write_text(encoded(r)+'\n')
 if not r['closes_at_three_quarters']:
  stop='EXACT_MENU_COUNTERSTATE';prefix.with_suffix('.counterstate.json').write_text(encoded(r)+'\n');break
 if genuine%50==0:
  print('PROGRESS genuine',genuine,'already_bad',known,'CPU',round(time.process_time()-start,2),'worst',worst['request_cost'],flush=True)
  prefix.with_suffix('.partial.json').write_text(json.dumps({'records':records,'attempts':attempts,'already_bad':known,'genuine':genuine},indent=2))
out={'status':stop,'attempts':attempts,'states':len(records),'already_bad':known,'genuine_terminal_cases':genuine,'cpu_seconds':round(time.process_time()-start,3),'worst_cost':str(worst['request_cost']) if worst else None,'seed':644075,'domain':'Every capacity .7500 to .7650; total own slack .7501 to .7550; off-traces zero or within .0050 of a simplex edge.','records':records}
prefix.with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='records'}),flush=True)
