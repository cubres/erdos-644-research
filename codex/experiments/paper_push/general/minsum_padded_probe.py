"""Discovery: global minimal good-triple sum plus global maximal-small gap.
A full-core fourth response permits matching allocation or closing ANY good triple.
"""
import sys,json,time
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt')
sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3,numpy as np
from p644_case_cover import regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_pair_regions,partial_core_regions,padded_pair_regions,padded_dominant_regions,gap_regions,partial_gap_regions
from p644_gap_one_trace import regions as one
from p644_gap_two_triples import regions as two
from p644_gap_trace_dichotomy import regions as dich
from p644_interval_finish_one_trace import constant_regions
from p644_matching_three import model
from nearcore_maxsmall import regions as nc,gap_regions as ng,strengthened_regions as ns,fullcore_regions as nf
B=F(107,125);M=F(137,320);S0=F(137,320)+F(179,500)
EXC=[(F(49,250),F(53,250)),(F(267,1000),F(89,250)),(F(54,125),F(237,500))]
data=json.loads(Path('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_static_template_facets_v3.json').read_text())
rs=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_pair_regions()+partial_core_regions()+padded_pair_regions()+padded_dominant_regions()+constant_regions(M)+nc(B,M)+ns(B,M)+nf(B,M)+nf(B,M,True)+two(B,F(1,2),M)
for ell,h in EXC:rs+=gap_regions(h,ell)+partial_gap_regions(B,h,ell)+one(B,h,ell)+two(B,h,ell)+dich(B,h,ell,M)+ng(B,M,ell,h)+ns(B,M,ell,h)
s=z3.SolverFor('QF_LRA');s.set(timeout=120000)
x,y,z,a,b,c=z3.Reals('x y z a b c');vs=[x,y,z,a,b,c]
for v in vs:
 s.add(v>=0,v<=1,z3.Or(v<=str(M),v>F(1,2)))
 for lo,hi in EXC:s.add(z3.Or(v<str(lo),v>str(hi)))
s.add(x>=y,y>=z,x+y+z<=str(S0),x+y<=1,x+z<=1,y+z<=1)
s.add(a<=1-x-y,b<=1-x-z,c<=1-y-z,a+b+c<=1)
s.add(a+b>=y+z,a+c>=x+z,b+c>=x+y)
s.add(b<=1-z3.RealVal(str(B))+y)
def val(f,p):return z3.RealVal(str(f[0]))+sum(z3.RealVal(str(q))*v for q,v in zip(f[1:],p))
for triple in ((x,y,z),(x,a,b),(y,a,c),(z,b,c)):
 for reg in rs:s.add(z3.Or(*[val(f,triple)>str(B) for f in reg]))
print('SETUP',len(rs),'regions',len(s.assertions()),'S0',str(S0),flush=True)
templates,prices,arr,den=model()
raww=[x,c,y,b,z,a]
w=[z3.If(raww[i^1]>0,raww[i],0) for i in range(6)]
selected=[];t0=time.time()
for step in range(200):
 ans=s.check()
 if ans!=z3.sat:
  print('RESULT',str(ans),'steps',step,'seconds',time.time()-t0,flush=True)
  Path(__file__).with_suffix('.smt2').write_text(s.to_smt2());break
 md=s.model();point=[F(str(md.eval(v))) for v in vs]
 rw=[point[0],point[5],point[1],point[4],point[2],point[3]]
 pw=[rw[i] if rw[i^1]>0 else F(0) for i in range(6)]
 costs=np.max(np.einsum('ijk,k->ij',arr,np.array(list(map(float,pw)))),axis=1)/den
 win=None
 for j in np.argsort(costs):
  ex=max(sum(int(q)*v for q,v in zip(row,pw)) for row in arr[j])/F(den)
  if ex<=B:win=int(j);break
  if costs[j]>float(B)+1e-7:break
 if win is None:
  allcost=[max(sum(int(q)*v for q,v in zip(row,pw)) for row in fs)/F(den) for fs in arr]
  result={'status':'MATCHING_MENU_HOLE','point':list(map(str,point)),'budget':str(min(allcost)),'selected':selected,'S0':str(S0),'M':str(M)}
  Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2));print('RESULT',result,flush=True);break
 selected.append(win)
 s.add(z3.Or(*[sum(int(q)*v for q,v in zip(row,w))>str(den*B) for row in arr[win]]))
 print('STEP',step,'point',list(map(str,point)),'template',win,'cost',str(ex),'seconds',time.time()-t0,flush=True)
