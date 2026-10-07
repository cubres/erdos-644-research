"""Standard-library exact obstruction to three simultaneous final requests.
New rank-64000 state, with full maximum-small gap, previous gaps, global
minimum-good-triple-sum inequalities, and the specified padded first request.
No numerical solver or discovery module is imported.
"""
from itertools import combinations, permutations, product
from fractions import Fraction as F
K,T,M=64000,54784,27400
x,y,z,a,b,c=27400,22786,2,4597,32001,27400
S=x+y+z
assert S<=T
assert a<=K-x-y and b<=K-x-z and c<=K-y-z
assert a+b+c<=K
assert b<=K-T+y # all unused budget pads the F-private part
assert a+b>=y+z and a+c>=x+z and b+c>=x+y
for v in (x,y,z,a,b,c):
 assert v<=M or v>K//2
 for lo,hi in ((12544,13568),(17088,22784),(27648,30336)):
  assert not lo<=v<=hi
# Pair-cell masks in the four original rows E,F,G,H.
cells={3:x,5:y,6:z,9:a,10:b,12:c}
for row in range(4):
 current=sum(v for mask,v in cells.items() if mask>>row&1)
 cells[1<<row]=K-current
assert min(cells.values())>=0
assert sum(cells[v] for v in (3,5,6))==S
# No cell belongs to three rows. Actual candidate graph is exactly matching.
pairs=[(u,v) for u,v in combinations(cells,2) if cells[u]>0 and cells[v]>0 and u|v==15]
assert set(map(frozenset,pairs))=={frozenset(q) for q in ((3,12),(5,10),(6,9))}
# The padded first request consists of the 3 old pair cells plus T-S
# points from F's old private cell. H takes b of the remaining old cell.
assert T-S<=K-x-z and b+(T-S)<=K-x-z

def minimal(L):
 L=tuple(L)
 return tuple(m for m in sorted(set(L)) if not any(n!=m and n&m==n for n in L))
def blocker(L):
 return minimal(m for m in range(1,8) if all(m&n for n in L))
ants=[q for n in range(1,8) for q in combinations(range(1,8),n) if minimal(q)==q]
assert len(ants)==18
prices=sorted(set(permutations((12,0,0)))|set(permutations((6,6,0)))|set(permutations((6,3,3)))|{(4,4,4)})
assert len(prices)==10
cost={L:tuple(min(sum(p[j] for j in range(3) if mask>>j&1) for mask in L) for p in prices) for L in ants}
weights=(x,c,y,b,z,a)
best=None;count=0;chosen=None
for tri in product(ants,repeat=3):
 labs=[q for L in tri for q in (L,blocker(L))]
 lower=max(sum(w*cost[L][j] for w,L in zip(weights,labs)) for j in range(10))
 assert lower>=12*54787
 if best is None or lower<best:best=lower;chosen=tri
 count+=1
assert count==5832 and best==12*54787
print('PASS: all four ranks, full maximum-small gap, three old gaps, minimum-good-triple sum, and padded first request')
print('PASS:',count,'complete matching label templates each have an exact price lower bound >= 54787 > budget 54784')
print('Smallest certified lower bound:',F(best,12),'at antichains',chosen)
