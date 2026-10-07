"""Targeted discovery model for three disjoint pairs.

Continuous masses on the 26 nonempty ternary types. Exact pairing graph,
rank bounds, full-antipodal endpoint mass, all 16-mode quantitative
neighborhood profiles, connected seed bounds, small-overlap triangle
exclusion, and the global high-m inequality. Numerical MILP outputs are
DISCOVERY, not theorem certificates. No claim of realizable full H.
"""
from itertools import product,combinations,permutations
from pathlib import Path
import json
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import lil_matrix

TYPES=[p for p in product([-1,0,1],repeat=3) if p!=(-1,-1,-1)]
MASKS=[sum(1<<(2*j+b) for j,b in enumerate(p) if b>=0) for p in TYPES]
FULL=[i for i,p in enumerate(TYPES) if -1 not in p]
OPP={i:TYPES.index(tuple(1-b for b in TYPES[i])) for i in FULL}
CROSS=[(i,j) for i in range(3) for j in range(3) if i!=j]

def graph_edges(code):
 return {(2*i,2*i+1) for i in range(3)}|{tuple(sorted((2*i,2*j+1))) for b,(i,j) in enumerate(CROSS) if code>>b&1}

def graph_representatives():
 reps={}
 for code in range(64):
  D={CROSS[b] for b in range(6) if code>>b&1}
  codes=[]
  for p in permutations(range(3)):
   for transpose in [False,True]:
    DD={(p[j],p[i]) if transpose else (p[i],p[j]) for i,j in D}
    codes.append(sum(1<<CROSS.index(edge) for edge in DD))
  reps.setdefault(min(codes),[]).append(code)
 return reps

class Builder:
 def __init__(self):self.names=[];self.lb=[];self.ub=[];self.integrality=[];self.rows=[];self.lo=[];self.hi=[]
 def var(self,name,lo=0,hi=1,binary=False):
  index=len(self.names);self.names.append(name);self.lb.append(lo);self.ub.append(hi);self.integrality.append(int(binary));return index
 def add(self,row,lo=-np.inf,hi=np.inf):self.rows.append(row);self.lo.append(lo);self.hi.append(hi)
 def solve(self,objective,seconds):
  A=lil_matrix((len(self.rows),len(self.names)))
  for i,row in enumerate(self.rows):
   for j,value in row.items():A[i,j]=value
  c=np.zeros(len(self.names))
  for i,value in objective.items():c[i]=value
  return milp(c,integrality=self.integrality,bounds=Bounds(self.lb,self.ub),
     constraints=LinearConstraint(A.tocsr(),self.lo,self.hi),
     options={'time_limit':seconds,'mip_rel_gap':0})

def combine(*terms):
 result={}
 for coef,row in terms:
  for i,value in row.items():result[i]=result.get(i,0)+coef*value
 return {i:v for i,v in result.items() if v}

class Model:
 def __init__(self,code=0,epsilon=1e-5,quarter=.25):
  self.code=code;self.epsilon=epsilon;self.quarter=quarter;self.edges=graph_edges(code);self.b=Builder();b=self.b
  self.w=[b.var('w:'+''.join('*' if z<0 else str(z) for z in p)) for p in TYPES]
  self.t=b.var('tau',hi=2);self.m=b.var('endpoint_mass',hi=2)
  self.support={i:b.var('present:'+str(i),binary=True) for i in FULL}
  self.eligible={i:b.var('eligible:'+str(i)) for i in FULL}
  def inter(mask):return {self.w[i]:1 for i,s in enumerate(MASKS) if s&mask==mask}
  self.inter=inter
  for i,mask in enumerate(MASKS):
   if any(mask>>u&1 and mask>>v&1 for u,v in self.edges):b.ub[self.w[i]]=0
  for i in FULL:
   w,z,y=self.w[i],self.support[i],self.eligible[i];zo=self.support[OPP[i]]
   b.add({w:1,z:-1},hi=0);b.add({w:1,z:-epsilon},lo=0)
   if b.ub[w]==0:b.ub[z]=0
   b.add({y:1,w:-1},hi=0);b.add({y:1,zo:-1},hi=0)
   b.add({y:1,w:-1,zo:-1},lo=-1)
  b.add(combine((1,{self.m:1}),(-1,{y:1 for y in self.eligible.values()})),lo=0,hi=0)
  b.add({self.t:1,self.m:-1},hi=0)
  b.add({self.t:1,self.m:1.5},hi=3.5)
  for r in range(6):b.add(inter(1<<r),hi=1)
  for u,v in combinations(range(6),2):
   if (u,v) not in self.edges:b.add(inter((1<<u)|(1<<v)),lo=epsilon)
  # Each actual triple has some pair intersection at least quarter.
  for triple in combinations(range(6),3):
   choices=[pair for pair in combinations(triple,2) if pair not in self.edges]
   if len(choices)==1:b.add(inter(sum(1<<i for i in choices[0])),lo=quarter)
   else:
    zs=[]
    for pair in choices:
     z=b.var('triangle:'+str(triple)+':'+str(pair),binary=True);zs.append(z)
     b.add(combine((1,inter(sum(1<<i for i in pair))),(-quarter,{z:1})),lo=0)
    b.add({z:1 for z in zs},lo=1)
  self.profile_data=[]
  for retained in combinations(range(3),2):
   quads=[]
   for bits in product([0,1],repeat=2):
    pair=tuple(sorted(2*j+bit for j,bit in zip(retained,bits)))
    quads.append({} if pair in self.edges else inter(sum(1<<r for r in pair)))
   # Opposite quadrant has to exist to be eligible.
   for q in [0,1]:
    if not quads[q] or not quads[3-q]:quads[q]=quads[3-q]={}
   total=combine(*[(1,q) for q in quads]);delta=combine((1,total),(-1,{self.m:1}))
   b.add(delta,lo=0)
   for modes in product(range(4),repeat=2):
    if modes==(0,0):continue
    cap={};fixed={};full={}
    for mode,(u,v) in zip(modes,[(quads[0],quads[3]),(quads[1],quads[2])]):
     if mode==1:cap=combine((1,cap),(1,u));fixed=combine((1,fixed),(1,v))
     if mode==2:cap=combine((1,cap),(1,v));fixed=combine((1,fixed),(1,u))
     if mode==3:
      uv=combine((1,u),(1,v));cap=combine((1,cap),(1,uv));fixed=combine((1,fixed),(1,uv));full=combine((1,full),(1,uv))
    # cap<=delta OR t<=fixed OR t<=fixed+delta-full.
    conditions=[combine((1,cap),(-1,delta)),combine((1,{self.t:1}),(-1,fixed)),
                combine((1,{self.t:1}),(-1,fixed),(-1,delta),(1,full))]
    zs=[b.var('profile:'+str(retained)+':'+str(modes)+':'+str(case),binary=True) for case in range(3)]
    for z,row in zip(zs,conditions):b.add(combine((1,row),(8,{z:1})),hi=8)
    b.add({z:1 for z in zs},lo=1,hi=1)
    self.profile_data.append((retained,modes,cap,fixed,full,delta))
  self.seed_count=0
  for s in range(2,7):
   for rows in combinations(range(6),s):
    reached={rows[0]}
    while True:
     more={v for u in reached for v in rows if tuple(sorted((u,v))) in self.edges}
     if more<=reached:break
     reached|=more
    if len(reached)!=s:continue
    left=[r for r in rows if r%2==0];right=[r for r in rows if r%2]
    X=inter(sum(1<<r for r in left));Y=inter(sum(1<<r for r in right));den=7-s
    b.add(combine((1,{self.t:1}),(-1,X),(-1/den,Y)),hi=0)
    b.add(combine((1,{self.t:1}),(-1,Y),(-1/den,X)),hi=0)
    self.seed_count+=1

 def solve(self,seconds=30):
  r=self.b.solve({self.t:-1},seconds)
  out={'graph_code':self.code,'status':int(r.status),'message':r.message,'seed_count':self.seed_count,
       'variables':len(self.b.names),'constraints':len(self.b.rows),'tau':None,'upper_bound':None}
  if getattr(r,'mip_dual_bound',None) is not None:out['upper_bound']=-float(r.mip_dual_bound)
  if r.x is not None:
   out['tau']=float(r.x[self.t]);out['m']=float(r.x[self.m]);out['cells']={''.join('*' if z<0 else str(z) for z in TYPES[i]):float(r.x[w]) for i,w in enumerate(self.w) if r.x[w]>1e-8}
   out['intersections']={str((u,v)):sum(r.x[i]*value for i,value in self.inter((1<<u)|(1<<v)).items()) for u,v in combinations(range(6),2)}
  return out

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--code',type=int,default=0);p.add_argument('--seconds',type=float,default=30);p.add_argument('--epsilon',type=float,default=1e-5);p.add_argument('--quarter',type=float,default=.25);p.add_argument('--all',action='store_true');a=p.parse_args()
 records=[]
 for code in (graph_representatives() if a.all else [a.code]):
  out=Model(code,a.epsilon,a.quarter).solve(a.seconds);records.append(out);print(json.dumps(out),flush=True)
  (Path(__file__).resolve().parents[1]/'outputs'/'agent_paired_ternary_discovery.json').write_text(json.dumps(records,indent=2)+'\n')
