"""Discovery of checked one-response strategies using two partner boxes.

Preconditions are affine inequalities on three known minima. They are split
explicitly into ordinary SPLIT nodes; terminal responses use ordinary REQ and
TMPL nodes. The checker is unchanged. Each failed precondition forbids only the
same discovery recipe on that branch, preventing equality-boundary loops.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement,product
import json,hashlib
import numpy as np
import search6 as lib
from b4core import X,T,TAU
from fano_v4_partner_oracle import candidates,maximal_boxes
from anchor_pair_request import outside_pair
from v4_templates import CELLS

def add(*rows):
 d={}
 for row in rows:
  for j,v in row.items():d[j]=d.get(j,0)+v
 return {j:F(v) for j,v in d.items() if v}
def scale(row,v):return {j:q*v for j,q in row.items() if q*v}
def neg(row):return scale(row,F(-1))
def val(row,z):return sum(float(v)*z[j] for j,v in row.items())
def canon(row):
 row={j:v for j,v in row.items() if v}
 if not row:return row
 f=abs(row[min(row)]);return {j:v/f for j,v in row.items()}
def token(row):return tuple(sorted((j,str(v)) for j,v in canon(row).items()))
def template(info,nt):
 if info['kind']=='FANO':return ['F',list(info['assignment'])+[nt]]
 d,a,b=info['roles'];return ['S',[CELLS,[b,nt,d,d,d,d,a]]]

def derive(tp,z,nt):
 inequalities=lib.template_ineqs(tp);caps=[]
 for i in range(3):
  opts=[{X(i):F(1)}]
  for d,h in inequalities:
   assert h==0
   a=d.get(T(nt,i),0)
   if a:
    assert a>0
    opts.append(scale({j:v for j,v in d.items() if j!=T(nt,i)},F(-1)/a))
  caps.append(min(opts,key=lambda q:val(q,z)))
 conditions=[]
 for d,h in inequalities:
  q={j:v for j,v in d.items() if j<lib.nv(nt)}
  for i in range(3):q=add(q,scale(caps[i],d.get(T(nt,i),0)))
  conditions.append(q)
 conditions +=[neg(q) for q in caps]
 return caps,conditions

def exact_sample(z):
 x=tuple(F(float(v)).limit_denominator(10**7) for v in z[:3]);rows=[]
 for k in range(3):
  t=[F(float(v)).limit_denominator(10**7) for v in z[lib.TOFF+3*k:lib.TOFF+3*k+3]]
  j=max(range(3),key=lambda i:t[i]);t[j]=1-sum(t[i] for i in range(3) if i!=j)
  if any(v<0 or v>x[i] for i,v in enumerate(t)):return None
  rows.append(tuple(t))
 return x,rows

def recipes(Z,nt):
 z=Z[0];sample=exact_sample(z)
 if sample is None:return []
 x,rows=sample;boxes=maximal_boxes(candidates(x,rows));out=[]
 derived={i:(template(info,nt),)+derive(template(info,nt),z,nt) for i,(cap,info) in enumerate(boxes)}
 one={T(0,i):F(1) for i in range(3)}
 for r,s in combinations_with_replacement(range(len(boxes)),2):
  R,Si=boxes[r][0],boxes[s][0]
  choices=[[(F(x[i]),('X',i))]+[(v,(j,i)) for j,v in ((r,R[i]),(s,Si[i])) if 0<=v<=x[i]] for i in range(3)]
  for choices_u in product(*choices):
   u=tuple(q[0] for q in choices_u)
   if sum(u)<1 or sum(x)-sum(u)>F(float(z[TAU])).limit_denominator(10**7):continue
   if outside_pair(x,u,R,Si):continue
   tpR,rforms,rc=derived[r];tpS,sforms,sc=derived[s]
   uf=[{X(i):F(1)} if key[0]=='X' else derived[key[0]][1][i] for i,(v,key) in enumerate(choices_u)]
   w=[add({X(i):F(1)},neg(uf[i])) for i in range(3)]
   cond=list(rc)+list(sc)+[neg(q) for q in w]+[add(w[i],{X(i):F(-1)}) for i in range(3)]+[add(*w,{TAU:F(-1)})]
   for i,j in product(range(3),repeat=2):
    options=[add(uf[i],neg(rforms[i])),add(uf[j],neg(sforms[j]))]
    if i!=j:options.append(add(one,neg(rforms[i]),neg(sforms[j])))
    valid=[q for q in options if val(q,z)<=1e-7]
    if not valid:break
    # Identity/guaranteed cuts first, then the largest sampled slack.
    cond.append(min(valid,key=lambda q:(bool(q),val(q,z))))
   else:
    unique={token(q):canon(q) for q in cond if q};cond=list(unique.values())
    rid=hashlib.sha256(json.dumps([tpR,tpS,[token(q) for q in uf]],sort_keys=True).encode()).hexdigest()
    coverage=sum(all(val(q,zz)<=1e-8 for q in cond) for zz in Z)
    out.append({'id':rid,'w':w,'R':rforms,'tpR':tpR,'tpS':tpS,'conditions':cond,'score':(coverage,float(sum(u)))})
 unique={q['id']:q for q in out}
 return sorted(unique.values(),key=lambda q:q['score'],reverse=True)

def response_tree(s,C,E,nt,recipe):
 n=lib.nv(nt+1);M=s.mats(C,E,n)
 # Split only R inequalities not already implied by the retained box. At a
 # failure Ui>=Ri, the pair-cover preconditions imply every S bound by rank1.
 pending=[add({T(nt,i):F(1)},neg(recipe['R'][i])) for i in range(3)]
 def walk(C,rest):
  M=s.mats(C,E,n)
  if s.empty_check(M,n):return {'k':'EMPTY'}
  while rest and s.maxlin(rest[0],M,n)<=lib.TOL:rest=rest[1:]
  if not rest:return {'k':'TMPL','t':recipe['tpR']}
  h=rest[0]
  # Exact certification later checks both leaves; this floating check only
  # catches a defective discovery construction early.
  badC=C+[(neg(h),F(0))]
  bm=s.mats(badC,E,n)
  if s.empty_check(bm,n):bad={'k':'EMPTY'}
  else:
   assert s.tmpl_ok(recipe['tpS'],bm,n),'response implication failed'
   bad={'k':'TMPL','t':recipe['tpS']}
  return {'k':'SPLIT','h':h,'kids':[walk(C+[(h,F(0))],rest[1:]),bad]}
 return walk(C,pending)

def terminal(s,C,E,nt,recipe):
 tc,te=lib.bc.type_region(nt);rc=lib.bc.request_region(nt,recipe['w']);kids=[]
 for pat in lib.PATS:
  c=C+tc+rc+lib.bc.pattern_region(nt,pat);e=E+te
  # Templates do not require new strictness assumptions. Temporarily clear
  # the parent's strict forms from numeric checks involving the added row.
  kids.append([list(pat),response_tree(s,c,e,nt,recipe)])
 s.cnt('PARTNER_TERMINAL')
 return {'k':'REQ','w':recipe['w'],'kids':kids}

def attempt(s,C,E,nt,nreq,path,Z):
 if nt!=3:return None
 taboo={q[1] for q in s.info if q[0]=='PARTNER_FORBID'}
 choices=[q for q in recipes(Z,nt) if q['id'] not in taboo]
 if not choices:return None
 recipe=choices[0];s.cnt('PARTNER_RECIPE');n=lib.nv(nt)
 def chain(C,conditions):
  M=s.mats(C,E,n)
  if s.empty_check(M,n):return {'k':'EMPTY'}
  pending=[q for q in conditions if (s.maxlin(q,M,n) or 0)>lib.TOL]
  if not pending:return terminal(s,C,E,nt,recipe)
  # Separate the largest possible violation first; all selected conditions
  # hold at the discovery point, but may fail elsewhere in the polyhedron.
  h=max(pending,key=lambda q:s.maxlin(q,M,n));rest=[q for q in pending if q!=h]
  good=chain(C+[(h,F(0))],rest)
  s.info.append(('PARTNER_FORBID',recipe['id']))
  try:bad=s.solve(C+[(neg(h),F(0))],E,nt,0,nreq,path+'v')
  finally:s.info.pop()
  return {'k':'SPLIT','h':h,'kids':[good,bad]}
 return chain(C,recipe['conditions'])
