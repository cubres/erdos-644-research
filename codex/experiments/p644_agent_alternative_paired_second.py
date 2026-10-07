"""Second disjoint-pair exploration; independent support validation required.

All seven-row subfamilies, all new paired triples, rank, and the small-
overlap-triangle exclusion are imposed. Numerical discovery, not a theorem.
"""
from itertools import combinations
from fractions import Fraction
import json
from p644_agent_alternative_paired_ternary import Builder, combine

def mask_of(s):
 return sum(1<<(2*j+int(x)) for j,x in enumerate(s) if x!='*')

def state(which='outside'):
 if which=='outside':
  data={'0001':16,'0110':13,'0111':3,'1000':7,'1001':1,
        '1010':6,'1011':2,'1100':6,'1101':2,'1111':5,'111*':3,'***1':3}
  return [(s,mask_of(s),Fraction(w,32)) for s,w in data.items()]
 e=Fraction(1,16)
 data={'0001':Fraction(1,2),'0110':Fraction(1,2)-e,'0111':e,
       '1000':Fraction(1,4)-e,'1001':e,'1010':Fraction(1,8)+e,
       '1011':Fraction(1,8)-e,'1100':Fraction(1,8)+e,
       '1101':Fraction(1,8)-e,'1111':Fraction(1,4)}
 return [(s,mask_of(s),w) for s,w in data.items()]

def inspect(atoms,pairs):
 rows=2*pairs;out={'ranks':[],'paired':[],'bad_sevens':[],'bad_triangles':[]}
 for i in range(rows):out['ranks'].append(str(sum(w for s,m,w in atoms if m>>i&1)))
 for js in combinations(range(pairs),3):
  mask=sum(3<<(2*j) for j in js)
  edges=[(i,j) for i,j in combinations(range(len(atoms)),2) if (atoms[i][1]|atoms[j][1])&mask==mask]
  ends=set(i for ij in edges for i in ij)
  out['paired'].append({'pairs':js,'m':str(sum(atoms[i][2] for i in ends)),
   'q':str(sum(atoms[i][2]*atoms[j][2] for i,j in edges))})
 for js in combinations(range(rows),7):
  mask=sum(1<<j for j in js)
  if not any((u|v)&mask==mask for (_,u,_),(_,v,_) in combinations(atoms,2)):out['bad_sevens'].append(js)
 for js in combinations(range(rows),3):
  best=max(sum(w for s,m,w in atoms if m>>u&1 and m>>v&1) for u,v in combinations(js,2))
  if best<=Fraction(1,4):out['bad_triangles'].append((js,str(best)))
 return out

class Model:
 def __init__(self,atoms,epsilon=1e-3,quarter=.251):
  self.atoms=atoms;self.b=b=Builder();self.n=n=len(atoms);self.oldrows=rows=8
  self.g=[b.var('g'+s,hi=float(w)) for s,m,w in atoms]
  self.h=[b.var('h'+s,hi=float(w)) for s,m,w in atoms]
  self.sg=[b.var('sg'+s,binary=True) for s,m,w in atoms]
  self.sh=[b.var('sh'+s,binary=True) for s,m,w in atoms]
  self.margin=b.var('margin',lo=-2,hi=2)
  for vs in [self.g,self.h]:b.add({v:1 for v in vs},hi=1)
  for i,(s,m,ww) in enumerate(atoms):
   w=float(ww);b.add({self.g[i]:1,self.h[i]:1},hi=w)
   for vs,zs in [(self.g,self.sg),(self.h,self.sh)]:
    b.add({vs[i]:1,zs[i]:-w},hi=0);b.add({vs[i]:1,zs[i]:-epsilon},lo=0)
  self.graph=lambda mask:[(i,j) for i,j in combinations(range(n),2) if (atoms[i][1]|atoms[j][1])&mask==mask]
  for retained in combinations(range(4),2):
   graph=self.graph(sum(3<<(2*j) for j in retained));terms={self.margin:-1}
   for i,(s,m,ww) in enumerate(atoms):
    nei=[j if u==i else u for u,j in graph if u==i or j==i]
    for vs,zs in [(self.g,self.sh),(self.h,self.sg)]:
     e=b.var('end'+str((retained,i,vs[0])),hi=float(ww))
     b.add({e:1,vs[i]:-1},hi=0)
     b.add(combine((1,{e:1}),(-float(ww),{zs[j]:1 for j in nei})),hi=0)
     terms[e]=1
   b.add(terms,lo=1.5)
  for six in combinations(range(rows),6):
   graph=self.graph(sum(1<<j for j in six));ends=set(i for ij in graph for i in ij)
   for zs in [self.sg,self.sh]:b.add({zs[i]:1 for i in ends},lo=1)
  for five in combinations(range(rows),5):
   graph=self.graph(sum(1<<j for j in five));zz=[]
   for i,j in graph:
    for u,v in [(i,j),(j,i)]:
     z=b.var('seven'+str((five,u,v)),binary=True);zz.append(z)
     b.add({z:1,self.sg[u]:-1},hi=0);b.add({z:1,self.sh[v]:-1},hi=0)
   b.add({z:1 for z in zz},lo=1)
  intersections={}
  for i,j in combinations(range(rows+2),2):
   if j<rows:intersections[i,j]=float(sum(w for s,m,w in atoms if m>>i&1 and m>>j&1))
   elif i<rows:intersections[i,j]={vs[c]:1 for c,(s,m,w) in enumerate(atoms) if m>>i&1 for vs in [self.g if j==rows else self.h]}
   else:intersections[i,j]=0.
  for row in range(rows):
   for vs in [self.g,self.h]:b.add({vs[c]:1 for c,(s,m,w) in enumerate(atoms) if m>>row&1},lo=epsilon)
  for triple in combinations(range(rows+2),3):
   cand=[intersections[p] for p in combinations(triple,2)]
   if any(isinstance(v,float) and v>=quarter for v in cand):continue
   zz=[]
   for q,expr in enumerate(v for v in cand if isinstance(v,dict)):
    z=b.var('triangle'+str((triple,q)),binary=True);zz.append(z)
    b.add(combine((1,expr),(-quarter,{z:1})),lo=0)
   b.add({z:1 for z in zz},lo=1)

 def solve(self,deletion,seconds=10):
  old=list(self.b.ub)
  for i,(s,m,w) in enumerate(self.atoms):self.b.ub[self.g[i]]=float(w)-float(deletion.get(s,0))
  r=self.b.solve({self.margin:-1},seconds);self.b.ub=old
  out={'deletion':{s:float(w) for s,w in deletion.items()},'status':int(r.status),'margin':None}
  if r.x is None:return out
  out['margin']=float(r.x[self.margin]);new=[];gg={};hh={}
  for i,(s,m,w) in enumerate(self.atoms):
   g=Fraction(float(r.x[self.g[i]])).limit_denominator(1000000);h=Fraction(float(r.x[self.h[i]])).limit_denominator(1000000)
   gg[s]=str(g);hh[s]=str(h)
   for z,t,bit in [(g,'0',256),(h,'1',512),(w-g-h,'*',0)]:
    if z>Fraction(1,10**7):new.append((s+t,m|bit,z))
  for v,t,bit in [(gg,'0',256),(hh,'1',512)]:
   z=1-sum(Fraction(x) for x in v.values())
   if z>Fraction(1,10**7):new.append(('****'+t,bit,z))
  out['g']=gg;out['h']=hh;out['validation']=inspect(new,5)
  return out

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--state',choices=['outside','inside'],default='outside');p.add_argument('--seconds',type=int,default=15);a=p.parse_args()
 atoms=state(a.state);print('INITIAL',json.dumps(inspect(atoms,4)),flush=True);m=Model(atoms)
 # One heavy cell plus available cells, followed by complementary unions.
 requests=[]
 for mask in range(1<<len(atoms)):
  D={s:w for i,(s,mm,w) in enumerate(atoms) if mask>>i&1}
  if sum(D.values())==Fraction(3,4):requests.append(D)
 best=None
 for D in requests:
  out=m.solve(D,a.seconds)
  if best is None or out['margin'] is None or out['margin']<best['margin']:
   best=out;print('BEST',json.dumps(out),flush=True)
  if out['status']==2:break
 print('DONE',len(requests),json.dumps(best),flush=True)
