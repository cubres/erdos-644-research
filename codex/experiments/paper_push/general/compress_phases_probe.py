"""Fresh exact-cover discovery for coarse chronological phases."""
import sys,json,time
from pathlib import Path
from fractions import Fraction as F
from itertools import product
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt')
from p644_astra_one_trace_check import static_region,adaptive_regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_regions,partial_regions,padded_regions,padded_dominant_regions,gap_regions,partial_gap_regions,one_trace_regions,two_triple_regions,remaining
from p644_spectrum_fast import certify_box
src=json.loads(Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/paper_push/general/six_sevenths_short_prefix.json').read_text());beta=F(6,7)
base=[static_region(t) for t in src['static_templates']]+adaptive_regions()+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_regions()+partial_regions()+padded_regions()+padded_dominant_regions()

def attempt(name,a,b,exc,capchoices):
 rs=list(base)
 for ell,h in exc:rs+=gap_regions(h,ell)+partial_gap_regions(beta,h,ell)+one_trace_regions(beta,h,ell)+two_triple_regions(beta,h,ell)
 for u in capchoices:
  v=2-beta-a-u
  if not(1-beta<=u<=1-b and b-a<=v<=1-a):continue
  boxes=[];failed=None;start=time.monotonic()
  for yi,zi in product(remaining(u,exc),remaining(v,exc)):
   proof=certify_box(rs,beta,(a,yi[0],zi[0]),(b,yi[1],zi[1]),limit=40000,depth_limit=90,split_planes=[(-beta,F(1),F(1),F(1))])
   if proof['status']!='COVERED':failed=proof;break
   boxes.append({'y':list(map(str,yi)),'z':list(map(str,zi)),'proof':proof})
  print(name,'cap',str(u),'status',failed or 'COVERED','nodes',sum(len(q['proof']['nodes']) for q in boxes),'sec',time.monotonic()-start,flush=True)
  if failed is None:
   step={'interval':list(map(str,(a,b))),'u':str(u),'v_at_left':str(v),'boxes':boxes,'prior_gaps':[[str(x),str(y)] for x,y in exc],'two_triples':True,'maximum_small':None}
   Path(__file__).with_name(name+'.json').write_text(json.dumps(step,separators=(',',':')));return True
 return False
if __name__=='__main__':
 attempt('coarse_middle_after_upper',F(263,1000),F(357,1000),[(F(429,1000),F(119,250))],[F(119,250),F(9,20),F(2,5)])
 attempt('coarse_middle_seed',F(29,100),F(357,1000),[(F(429,1000),F(119,250))],[(2-beta-F(29,100))/2])
 attempt('coarse_unconditional_upper',F(429,1000),F(119,250),[],[(2-beta-F(429,1000))/2])
 attempt('coarse_unconditional_middle',F(263,1000),F(357,1000),[],[(2-beta-F(263,1000))/2,F(119,250),F(9,20)])
 attempt('coarse_seed_extend',F(24,125),F(107,500),[(F(191,1000),F(24,125)),(F(263,1000),F(357,1000)),(F(429,1000),F(119,250))],[(2-beta-F(24,125))/2])
 attempt('coarse_bridge',F(107,500),F(263,1000),[(F(191,1000),F(107,500)),(F(263,1000),F(357,1000)),(F(3,7),F(119,250))],[(2-beta-F(107,500))/2])
 attempt('coarse_upper',F(119,250),F(1,2),[(F(191,1000),F(357,1000)),(F(3,7),F(119,250))],[(2-beta-F(119,250))/2])
 attempt('coarse_lower',F(191,1000),F(263,1000),[(F(263,1000),F(357,1000)),(F(429,1000),F(119,250))],[(2-beta-F(191,1000))/2,F(119,250),F(47,100),F(9,20)])
