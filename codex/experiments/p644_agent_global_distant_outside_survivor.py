"""Exact outside survivor of the B x (C union D) endpoint request.

All checks use row masks and Fractions, allowing points in neither member
of a designated pair and genuinely new outside points.
"""
from fractions import Fraction as F
import itertools,json
from pathlib import Path

def main():
 types=['00001','00011','01100','01110','10011','11111','10100','10111','11000','11011']
 weights=list(map(F,['1/4','1/4','1/4','1/4','6/25','6/25','1/4','1/100','1/4','1/100']))
 r=list(map(F,['21/100','1/4','0','1/4','0','2/25','0','0','3/40','1/100']))
 h=list(map(F,['1/25','0','1/4','0','23/200','4/25','1/4','1/100','7/40','0']))
 deletion=[2,4,6,7]
 assert sum(weights[i] for i in deletion)==F(3,4)
 assert all(r[i]==0 for i in deletion)
 atoms=[]
 for i,(s,w,x,y) in enumerate(zip(types,weights,r,h)):
  assert x+y<=w
  old=sum(1<<(2*j+int(b)) for j,b in enumerate(s))
  for mass,mask,label in [(x,old|(1<<10),'R'),(y,old|(1<<11),'H'),(w-x-y,old,'neither')]:
   if mass:atoms.append((mask,mass,f'{i}:{label}'))
 assert sum(h)==1
 atoms.append((1<<10,1-sum(r),'outsideR'))
 ranks=[sum(w for m,w,l in atoms if m>>i&1) for i in range(12)]
 assert ranks==[F(1)]*12
 disjoint=[]
 for i,j in itertools.combinations(range(12),2):
  if not any((m>>i&1) and (m>>j&1) for m,w,l in atoms):disjoint.append((i,j))
 assert disjoint==[(2*i,2*i+1) for i in range(6)]
 unions=[(i,j,atoms[i][0]|atoms[j][0]) for i in range(len(atoms)) for j in range(i,len(atoms))]
 profiles=[]
 for ps in itertools.combinations_with_replacement(range(6),3):
  target=sum(3<<(2*i) for i in set(ps))
  q=sum(atoms[i][1]*atoms[j][1] for i,j,m in unions if i!=j and m&target==target)
  assert q>=F(6,25)
  profiles.append({'pairs':[i+1 for i in ps],'Q':str(q)})
 for rows in itertools.combinations(range(12),7):
  target=sum(1<<i for i in rows)
  assert any(m&target==target for i,j,m in unions)
 best=F(3);bestrows=None;bestpairs=None
 for rows in itertools.combinations(range(12),6):
  target=sum(1<<i for i in rows);pairs=[(i,j) for i,j,m in unions if m&target==target]
  eligible={i for p in pairs for i in p};p=sum(atoms[i][1] for i in eligible)
  if p<best:best,bestrows,bestpairs=p,rows,pairs
 assert best==F(183,200)
 full=(1<<12)-1;cover=None
 for size in range(1,5):
  for cc in itertools.combinations(range(len(atoms)),size):
   m=0
   for i in cc:m|=atoms[i][0]
   if m==full:cover=cc;break
  if cover is not None:break
 out={'status':'Exact local outside survivor; not a large-transversal family',
      'c':'6/25','deletion_old_atom_indices':deletion,'deletion_mass':'3/4',
      'old_types':types,'old_masses':list(map(str,weights)),
      'R_old_masses':list(map(str,r)),'H_old_masses':list(map(str,h)),
      'outside_R':str(1-sum(r)),'outside_H':'0',
      'atoms':[{'mask':m,'mass':str(w),'label':l} for m,w,l in atoms],
      'paired_Q':profiles,'seven_subsets_checked':792,
      'minimum_all_six_endpoint_mass':str(best),
      'minimizing_six_rows':[i+1 for i in bestrows],
      'minimizing_six_pair_graph':bestpairs,
      'transversal_number':len(cover),'cover_atoms':cover}
 path=Path('outputs/agent_global_distant_outside_survivor.json')
 path.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ['paired_Q','atoms']},indent=2))
 print(path)

if __name__=='__main__':main()
