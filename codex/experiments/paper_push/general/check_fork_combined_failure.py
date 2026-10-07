"""Exact diagnostic for the bounded fork-menu failure and its V5 repair."""
from fractions import Fraction as F
from pathlib import Path
import json
p=Path(__file__).with_name('fork_combined_failure_exact.json')
d=json.loads(p.read_text()); den=d['denominator']
def vec(key): return [F(v,den) for v in d[key]]
x=vec('capacities');a=vec('a');b=vec('b');c=vec('c');types=[a,b,c]
s=[a[0],b[1],c[2]];e=[x[i]-s[i] for i in range(3)]
assert all(sum(t)==1 for t in types)
assert all(xi>=F(3,4) for xi in x)
assert all(0<=types[j][i]<=x[i] for i in range(3) for j in range(3))
assert all(s[i]>2*e[i] for i in range(3))
assert sum(e)>F(3,4) and all(e[i]+e[j]<F(3,4) for i in range(3) for j in range(i))
arrows={(j,i) for j in range(3) for i in range(3) if i!=j and types[j][i]>e[i]}
assert arrows=={(0,2),(1,2)}
assert a[2]>s[2]/2+e[2] and b[2]<=s[2]/2+e[2]
assert b[0]>e[0]/2
lines=[{0,1,2},{0,3,4},{0,5,6},{1,3,5},{1,4,6},{2,3,6},{2,4,5}]
def cap(assignment):
 residual=x.copy()
 for point in range(7):
  rows=[i for i,L in enumerate(lines) if point in L]
  count=sum(assignment[i] is None for i in rows)
  for j in range(3):
   known=sum(types[assignment[i]][j] for i in rows if assignment[i] is not None)
   if count:residual[j]=min(residual[j],(2*x[j]-known)/count)
   else:assert known<=2*x[j]
 count=assignment.count(None)
 for j in range(3):
  known=sum(types[t][j] for t in assignment if t is not None)
  residual[j]=min(residual[j],(4*x[j]-known)/count)
 assert all(v>=0 for v in residual)
 return residual
for assignment,cost in zip([(0,1,1,1,None,2,None),(0,0,1,1,None,None,2)],d['fano_costs']):
 assert sum(x)-sum(cap(assignment))==F(cost)>F(3,4)
R=[min(x[i],2*x[i]-2*a[i]-b[i],4*x[i]-5*a[i]-b[i]) for i in range(3)]
S=[min(x[i],2*x[i]-2*b[i]-a[i],4*x[i]-5*b[i]-a[i]) for i in range(3)]
assert R==vec('R') and S==vec('S')
u=vec('retained')
assert R[0]+S[1]>1
assert u[0]<=S[0] and u[1]<=R[1] and u[2]<=min(R[2],S[2])
assert sum(x)-sum(u)==F(d['exchange_cost'])<F(3,4)
print('PASS: strict fork witness, both Fano costs, failed simplified exchange criterion, exact two-V5 repair')
