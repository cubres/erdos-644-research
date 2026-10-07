"""Standard-library exact checks for finite paired states with outside atoms."""
from fractions import Fraction as F
import itertools

def verify(atoms,npairs,c=F(6,25)):
 """Atoms are (row-mask, positive Fraction mass, descriptive label)."""
 nrows=2*npairs
 assert all(w>0 and m>0 and m<(1<<nrows) for m,w,label in atoms)
 assert all(sum(w for m,w,label in atoms if m>>i&1)==1 for i in range(nrows))
 disjoint=[]
 for i,j in itertools.combinations(range(nrows),2):
  if not any(m>>i&1 and m>>j&1 for m,w,label in atoms):disjoint.append((i,j))
 assert disjoint==[(2*i,2*i+1) for i in range(npairs)],disjoint
 unions=[(i,j,atoms[i][0]|atoms[j][0]) for i in range(len(atoms)) for j in range(i,len(atoms))]
 profiles=[]
 for ps in itertools.combinations_with_replacement(range(npairs),3):
  target=sum(3<<(2*i) for i in set(ps))
  q=sum(atoms[i][1]*atoms[j][1] for i,j,m in unions if i!=j and m&target==target)
  assert q>=c,(ps,q)
  profiles.append({'pairs':[i+1 for i in ps],'Q':str(q)})
 seven_count=0
 for rows in itertools.combinations(range(nrows),7):
  target=sum(1<<i for i in rows)
  assert any(m&target==target for i,j,m in unions),rows
  seven_count+=1
 best=F(10);bestrows=None;bestpairs=None
 for rows in itertools.combinations(range(nrows),6):
  target=sum(1<<i for i in rows);pairs=[(i,j) for i,j,m in unions if m&target==target]
  eligible={i for p in pairs for i in p};p=sum(atoms[i][1] for i in eligible)
  if p<best:best,bestrows,bestpairs=p,rows,pairs
 assert best>F(3,4),(best,bestrows)
 full=(1<<nrows)-1;cover=None
 for size in range(1,5):
  for cc in itertools.combinations(range(len(atoms)),size):
   m=0
   for i in cc:m|=atoms[i][0]
   if m==full:cover=cc;break
  if cover is not None:break
 assert cover is not None
 return {'paired_Q':profiles,'seven_subsets_checked':seven_count,
         'minimum_all_six_endpoint_mass':str(best),
         'minimizing_six_rows':[i+1 for i in bestrows],
         'minimizing_six_pair_graph':bestpairs,
         'transversal_number':len(cover),'cover_atoms':cover}
