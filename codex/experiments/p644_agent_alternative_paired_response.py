"""Full new disjoint-pair discovery for the six-cell ternary survivor.
Checks all seven-row subfamilies, paired endpoint minima, and small-overlap
triangle exclusion for all eight rows. Floating-point discovery only.
"""
from itertools import combinations
import numpy as np
from p644_agent_alternative_paired_ternary import Builder,combine

TYPES=['000','011','100','101','110','111']
WEIGHTS=[.5,.5,.25,.25,.25,.25]
MASKS=[sum(1<<(2*j+int(bit)) for j,bit in enumerate(t)) for t in TYPES]

class Model:
 def __init__(self,epsilon=1e-4,quarter=.2501):
  b=self.b=Builder();n=6;self.g=[b.var('g'+t,hi=w) for t,w in zip(TYPES,WEIGHTS)];self.h=[b.var('h'+t,hi=w) for t,w in zip(TYPES,WEIGHTS)]
  self.sg=[b.var('sg'+t,binary=True) for t in TYPES];self.sh=[b.var('sh'+t,binary=True) for t in TYPES]
  self.margin=b.var('margin',lo=-2,hi=2)
  b.add({v:1 for v in self.g},hi=1);b.add({v:1 for v in self.h},hi=1)
  for i,w in enumerate(WEIGHTS):
   b.add({self.g[i]:1,self.h[i]:1},hi=w)
   for vs,zs in [(self.g,self.sg),(self.h,self.sh)]:
    b.add({vs[i]:1,zs[i]:-w},hi=0);b.add({vs[i]:1,zs[i]:-epsilon},lo=0)
  self.graphs=[]
  for retained in combinations(range(3),2):
   mask=sum((3<<(2*j)) for j in retained)
   graph=[[j for j in range(n) if i!=j and ((MASKS[i]|MASKS[j])&mask)==mask] for i in range(n)]
   self.graphs.append(graph);terms={self.margin:-1}
   for i,w in enumerate(WEIGHTS):
    for vs,zs in [(self.g,self.sh),(self.h,self.sg)]:
     e=b.var('ep'+str(retained)+str(i)+str(vs[0]),hi=w)
     b.add({e:1,vs[i]:-1},hi=0)
     b.add(combine((1,{e:1}),(-w,{zs[j]:1 for j in graph[i]})),hi=0)
     terms[e]=1
   b.add(terms,lo=1.5)
  # Six old plus each new row.
  for support in [self.sg,self.sh]:b.add({support[i]:1 for i in [0,1,2,5]},lo=1)
  # Five old plus both new rows.
  for omit in range(6):
   mask=63^(1<<omit);zs=[]
   for i,j in ((i,j) for i in range(n) for j in range(n) if i!=j and ((MASKS[i]|MASKS[j])&mask)==mask):
    z=b.var('seven'+str((omit,i,j)),binary=True);zs.append(z)
    b.add({z:1,self.sg[i]:-1},hi=0);b.add({z:1,self.sh[j]:-1},hi=0)
   b.add({z:1 for z in zs},lo=1)
  intersections={}
  for i,j in combinations(range(8),2):
   if j<6:intersections[i,j]=sum(w for mask,w in zip(MASKS,WEIGHTS) if mask>>i&1 and mask>>j&1)
   elif i<6:intersections[i,j]={vs[c]:1 for c,mask in enumerate(MASKS) if mask>>i&1 for vs in [self.g if j==6 else self.h]}
   else:intersections[i,j]=0.
  for row in range(6):
   for vs in [self.g,self.h]:b.add({vs[c]:1 for c,mask in enumerate(MASKS) if mask>>row&1},lo=epsilon)
  for triple in combinations(range(8),3):
   candidates=[intersections[p] for p in combinations(triple,2)]
   if any(isinstance(v,(int,float)) and v>=quarter for v in candidates):continue
   candidates=[v for v in candidates if isinstance(v,dict)]
   zs=[]
   for q,expr in enumerate(candidates):
    z=b.var('triangle'+str((triple,q)),binary=True);zs.append(z)
    b.add(combine((1,expr),(-quarter,{z:1})),lo=0)
   b.add({z:1 for z in zs},lo=1)

 def solve(self,deletion,seconds=10):
  old=list(self.b.ub)
  for i,t in enumerate(TYPES):self.b.ub[self.g[i]]=WEIGHTS[i]-deletion.get(t,0)
  r=self.b.solve({self.margin:-1},seconds);self.b.ub=old
  ans={'deletion':deletion,'cost':sum(deletion.values()),'status':int(r.status),'message':r.message,'margin':None}
  if r.x is not None:
   ans['margin']=float(r.x[self.margin]);ans['g']={t:float(r.x[v]) for t,v in zip(TYPES,self.g) if r.x[v]>1e-8};ans['h']={t:float(r.x[v]) for t,v in zip(TYPES,self.h) if r.x[v]>1e-8}
  return ans

if __name__=='__main__':
 import json
 m=Model();best=None
 for mask in range(1<<6):
  D={t:w for i,(t,w) in enumerate(zip(TYPES,WEIGHTS)) if mask>>i&1}
  if sum(D.values())>.75:continue
  out=m.solve(D)
  if out['margin'] is None or best is None or out['margin']<best['margin']:
   best=out;print(json.dumps(out),flush=True)
 print('BEST',json.dumps(best))
