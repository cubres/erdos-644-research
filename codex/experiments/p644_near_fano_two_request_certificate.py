"""Exact symbolic certificate for a two-request near-Fano improvement.
Standard library only. This verifies a feasible strategy, not the MILP's
numerical optimum. Coefficients represent a,b,h,e, respectively.
"""
from collections import defaultdict
from itertools import combinations
from fractions import Fraction

def add(*vs):return tuple(sum(v[j] for v in vs) for j in range(4))
def neg(v):return tuple(-x for x in v)
def unit(a=0,b=0,h=0,e=0):return (a,b,h,e)

def main():
 lines=[frozenset(t) for t in combinations(range(7),3)
        if (t[0]+1)^(t[1]+1)^(t[2]+1)==0]
 rows=[2,4,5,6]; cells=defaultdict(lambda:unit())
 for line in lines:
  mask=sum(1<<j for j,r in enumerate(rows) if r not in line)
  cells[mask]=add(cells[mask],unit(a=1))
  for r in set(range(7))-line:
   mask=sum(1<<j for j,s in enumerate(rows) if s not in line|{r})
   cells[mask]=add(cells[mask],unit(b=1))
 assert 15 not in cells
 # q=0 outside both requests; q=1,2 in just that request; q=3 in both.
 allocation={
  0:{0:unit(b=1)},1:{0:unit(b=2)},
  2:{1:unit(h=1),2:unit(b=2,h=-1)},
  3:{1:unit(a=1,b=3)},4:{0:unit(b=2)},
  5:{0:unit(a=1,b=3)},6:{2:unit(a=1,b=3)},
  8:{0:unit(a=1,b=3)},9:{3:unit(b=2)},
  10:{2:unit(b=2)},11:{2:unit(a=1,b=1)},
  12:{1:unit(b=1,e=-1),3:unit(b=1,e=1)},
  13:{3:unit(a=1,b=1)},14:{1:unit(a=1,b=1)},
 }
 assert set(cells)==set(allocation)
 for s in cells:assert add(*allocation[s].values())==cells[s]
 req=[add(*(v for opts in allocation.values() for q,v in opts.items() if q&d)) for d in [1,2]]
 assert req==[unit(a=3,b=9,h=1),unit(a=3,b=12,h=-1,e=1)]
 parts=[(s,q,v) for s,opts in allocation.items() for q,v in opts.items()]
 active=[]
 for s,q,v in parts:
  if any(s|t==15 and q&r==0 for t,r,w in parts):active.append((s,q,v))
 endpoint=add(*(v for s,q,v in active))
 assert endpoint==unit(a=3,b=12,e=-1),endpoint
 # At integer e=1, choose h nearest (3b+1)/2. Each capacity constraint
 # holds for every b>=1; declared zero parts merely overcount endpoints.
 for b in range(1,101):
  h=(3*b+1)//2
  assert 0<=h<=2*b and 0<=b-1<=2*b
  budget=max(9*b+h,12*b+1-h)
  assert budget==(21*b+2)//2
 print('EXACT_PASS: four rows [2,4,5,6] have empty common intersection')
 print('EXACT_PASS: D1=3a+9b+h; D2=3a+12b+e-h')
 print('EXACT_PASS: residual endpoint upper bound=3a+12b-e')
 print('EXACT_PASS: e=1, h=floor((3b+1)/2), max budget=3a+ceil((21b+1)/2)')
 print('Active (old mask, request membership):',[(format(s,'04b'),q) for s,q,v in active])

if __name__=='__main__':main()
