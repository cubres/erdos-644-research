"""Exact Fano/V4 partner boxes permitting the new TYPE in multiple rows.

This distinguishes one new family query from exactly one occurrence of its
answer in the resulting seven-tuple. Fano assignments use the previously
verified complete264 four-color row-automorphism orbit representatives.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys
import numpy as np
from fano_v4_partner_oracle import PENCILS
from v4_escape_boxes import maximal_boxes,escape_orthants,best_free_box
REPFILE=Path('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy/reps4.npy')
REPS=np.load(REPFILE);assert REPS.shape==(264,7)
VROWS=((4,0,0,0),(0,4,0,0),(0,0,4,0),(2,2,2,0),(0,2,2,4),(1,1,1,4))

def cap_from_forms(x,T,roles,forms):
 U=len(T);bounds=[x[i] for i in range(3)]
 for coeff,rhs in forms:
  count=sum(q for q,k in zip(coeff,roles) if k==U)
  for i in range(3):
   fixed=sum(q*T[k][i] for q,k in zip(coeff,roles) if k!=U)
   if not count:
    if fixed>rhs*x[i]:return None
   else:bounds[i]=min(bounds[i],(rhs*x[i]-fixed)/count)
 return tuple(bounds)

def fano_cap(x,T,assignment):
 assert len(assignment)==7 and len(T) in assignment
 forms=[(tuple(int(j in p) for j in range(7)),2) for p in PENCILS]+[((1,)*7,4)]
 return cap_from_forms(x,T,assignment,forms)

def v4_cap(x,T,roles):return cap_from_forms(x,T,roles,[(c,4) for c in VROWS])

PAIR=json.loads((REPFILE.parent/'astra_support_capacity_minimal.json').read_text())['minimal_functions']
MIX=json.loads(Path(__file__).with_name('balanced_1321_template.json').read_text())['projected_vertices']
MIXFORMS=[(tuple(map(F,row)),1) for row in MIX]

def analyse(x,T,all_known=False,with_223=False):
 x=tuple(map(F,x));T=[tuple(map(F,t)) for t in T];assert len(T)==3
 assert all(sum(t)==1 and all(0<=t[i]<=x[i] for i in range(3)) for t in T)
 cand={}
 for asg in REPS:
  asg=tuple(map(int,asg))
  if 3 not in asg:continue
  cap=fano_cap(x,T,asg)
  if cap is not None and min(cap)>=0 and sum(cap)>=1:cand.setdefault(cap,{'kind':'FANO_REPEAT','assignment':asg})
 for roles in product(range(4),repeat=4):
  if 3 not in roles:continue
  cap=v4_cap(x,T,roles)
  if cap is not None and min(cap)>=0 and sum(cap)>=1:cand.setdefault(cap,{'kind':'V4_REPEAT','roles_a_b_c_d':roles})
 if all_known:
  for k,p in enumerate(PAIR):
   forms=[(tuple(map(F,row)),1) for row in p['vertices']]
   for a in range(3):
    for roles in [(a,3),(3,a)]:
     cap=cap_from_forms(x,T,roles,forms)
     if cap is not None and min(cap)>=0 and sum(cap)>=1:cand.setdefault(cap,{'kind':'PAIR','function':k,'roles':roles})
  for roles in product(range(4),repeat=4):
   if 3 not in roles:continue
   cap=cap_from_forms(x,T,roles,MIXFORMS)
   if cap is not None and min(cap)>=0 and sum(cap)>=1:cand.setdefault(cap,{'kind':'MIXED1321','roles':roles})
 if with_223:
  forms223=[(tuple(map(F,row)),1) for row in json.loads(Path(__file__).with_name('endpoint_new_template.template.json').read_text())['projected_vertices']]
  for roles in product(range(4),repeat=3):
   if 3 not in roles:continue
   cap=cap_from_forms(x,T,roles,forms223)
   if cap is not None and min(cap)>=0 and sum(cap)>=1:cand.setdefault(cap,{'kind':'NEW223','roles':roles})
 boxes=maximal_boxes(cand);corners=escape_orthants(x,boxes);cost,u,closed=best_free_box(x,corners)
 if cost>sum(x)-1:cost=sum(x)-1;u=None;closed=False
 r={'capacities':x,'types':T,'boxes':boxes,'escape_corners':corners,'request_cost':cost,'retained_box':u,'closed_box_free':closed,'scope':'New type may repeat; menu includes Fano,V4'+(',42pair functions,and mixed1321 support.' if all_known else '.')}
 for cap,info in boxes:
  if info['kind']=='FANO_REPEAT':expected=fano_cap(x,T,info['assignment'])
  elif info['kind']=='V4_REPEAT':expected=v4_cap(x,T,info['roles_a_b_c_d'])
  elif info['kind']=='PAIR':expected=cap_from_forms(x,T,info['roles'],[(tuple(map(F,row)),1) for row in PAIR[info['function']]['vertices']])
  elif info['kind']=='MIXED1321':expected=cap_from_forms(x,T,info['roles'],MIXFORMS)
  else:expected=cap_from_forms(x,T,info['roles'],forms223)
  assert cap==expected
 if u is not None:
  assert cost==sum(x)-sum(u)
  if closed:assert all(any(v<low or(v==low and strict) for v,(low,strict) in zip(u,c)) for c in corners)
 return r
if __name__=='__main__':
 p=Path(sys.argv[1]);d=json.loads(p.read_text());r=analyse(d['capacities'],d['types'],all_known='--all-known' in sys.argv or '--with-223' in sys.argv,with_223='--with-223' in sys.argv);out=p.with_name(p.stem+('.repeated_with223.json' if '--with-223' in sys.argv else '.repeated_full_menu.json' if '--all-known' in sys.argv else '.repeated_response.json'));out.write_text(json.dumps(r,default=str,indent=2)+'\n')
 print('EXACT repeated-response cost',r['request_cost'],'retained',r['retained_box'],'boxes',len(r['boxes']),'escape orthants',len(r['escape_corners']),'closed',r['closed_box_free']);print(out)
