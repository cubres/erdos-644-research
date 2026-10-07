"""Hand-proved near-core closing regions using the complete maximum-small gap.
Every form must be <= beta. Discovery-module region encoder.
"""
from fractions import Fraction as F
from itertools import permutations

def regions(beta,m):
 beta,m=map(F,(beta,m))
 out=[]
 for high in (True,):
  base=[(0,0,1,1), (m,0,0,1), (1,0,1,-1), (1,F(1,2),0,-1),
        ((2+m)/3,F(1,3),0,F(-1,3)), (m,1,0,0)]
  if high:
   base += [(F(1,2),0,1,F(1,2)),
      (F(2,3),F(-1,3),F(1,3),F(2,3)), (F(2,3),F(1,3),F(1,3),0),
      (F(3,4),0,0,F(1,4)),
      (1,-1,1,0), (1,-1,0,F(1,2)), (1,0,0,F(-1,2)), (1,F(-1,3),F(-1,3),0)]
  else:
   base += [(0,1,1,1), (1,-1,1,0), (1,-1,0,F(1,2)),
      (1,0,0,F(-1,2)), (1,F(-1,3),F(-1,3),0)]
  for perm in permutations(range(3)):
   fs=[]
   for form in base:
    row=[F(form[0]),F(0),F(0),F(0)]
    for j,k in enumerate(perm):row[k+1]=F(form[j+1])
    fs.append(tuple(row))
   out.append(fs)
 return out

def gap_regions(beta,m,ell,h):
 beta,m,ell,h=map(F,(beta,m,ell,h))
 base=[(beta+1-h,-1,0,-1), (1-h,0,1,0),
       (m,0,0,1), (1,0,1,-1), (1,F(1,2),0,-1),
       ((2+m)/3,F(1,3),0,F(-1,3)), (m,1,0,0),
       (ell,0,1,1), ((1+ell)/2,F(-1,2),0,1),
       ((1+ell)/2,F(1,2),0,0), ((2+ell)/3,0,F(-1,3),F(1,3))]
 out=[]
 for perm in permutations(range(3)):
  fs=[]
  for form in base:
   row=[F(form[0]),F(0),F(0),F(0)]
   for j,k in enumerate(perm):row[k+1]=F(form[j+1])
   fs.append(tuple(row))
  out.append(fs)
 return out

def strengthened_regions(beta,m,ell=None,h=None):
 beta,m=map(F,(beta,m))
 if ell is None:
  rs=regions(beta,m)
  drop=(F(1),F(1,2),F(0),F(-1))
  # Create in the canonical orientation before applying permutations.
  canonical=rs[0]
 else:
  ell,h=map(F,(ell,h));canonical=gap_regions(beta,m,ell,h)[0]
  drop=(F(1),F(1,2),F(0),F(-1))
 canonical=[row for row in canonical if row!=drop]
 canonical += [(F(1,3),F(2,3),F(2,3),F(1,3)), (0,1,1,0),
      (F(1,2),F(1,2),F(3,4),0), (F(1,2),1,0,F(-1,2)),
      (F(3,5),F(3,5),F(2,5),F(-1,5))]
 out=[]
 for perm in permutations(range(3)):
  fs=[]
  for form in canonical:
   row=[F(form[0]),F(0),F(0),F(0)]
   for j,k in enumerate(perm):row[k+1]=F(form[j+1])
   fs.append(tuple(row))
  out.append(fs)
 return out

def fullcore_regions(beta,m,strong=False):
 beta,m=map(F,(beta,m))
 canonical=[(0,1,1,1), (m,0,0,1), (1,0,1,-1), (1,F(1,2),0,-1),
       ((2+m)/3,F(1,3),0,F(-1,3)), (m,1,0,0),
       (1,-1,1,0), (1,-1,0,F(1,2))]
 if strong:
  canonical=[r for r in canonical if r!=(1,F(1,2),0,-1)]
  canonical += [(F(1,3),F(2,3),F(2,3),F(1,3)), (0,1,1,0),
      (F(1,2),F(1,2),F(3,4),0), (F(1,2),1,0,F(-1,2)),
      (F(3,5),F(3,5),F(2,5),F(-1,5))]
 out=[]
 for perm in permutations(range(3)):
  fs=[]
  for form in canonical:
   row=[F(form[0]),F(0),F(0),F(0)]
   for j,k in enumerate(perm):row[k+1]=F(form[j+1])
   fs.append(tuple(row))
  out.append(fs)
 return out
