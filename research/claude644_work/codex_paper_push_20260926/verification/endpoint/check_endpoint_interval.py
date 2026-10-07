"""Independent standard-library replay of the quantified interval certificate.

At each endpoint, nonnegative masses on pairwise noncovering cells cover the
seven row demands within the part capacity. Their convex interpolation does
so for every t in[0,1/100], since demands and capacities are affine in t.
Membership deletions give exact row demands and preserve pair noncovering.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys
from endpoint_interval_model import family,boxes,retained,bound,PARENTS,ASSIGNMENTS,END
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('endpoint_interval_certificate.json')
d=json.loads(p.read_text());assert d['interval']==['0',str(END)]
assert [F(e['t']) for e in d['endpoints']]==[F(0),END]
count=0
for endpoint in d['endpoints']:
 t=F(endpoint['t']);x,T=family(t);B=boxes(t)
 assert all(sum(row)==1 and all(0<=v<=x[i] for i,v in enumerate(row)) for row in T)
 assert len(endpoint['boxes'])==4
 for k,(cap,parents,asg) in enumerate(zip(B,PARENTS,ASSIGNMENTS)):
  assert all(0<=cap[i]<=x[i] for i in range(3))
  assert all(a|b!=127 for a in parents for b in parents)
  assert all(any(S>>j&1 for S in parents) for j in range(7))
  rows=[(T+(cap,))[j] for j in asg];parts=endpoint['boxes'][k]['parts'];assert len(parts)==3
  for i,masses in enumerate(parts):
   y=list(map(F,masses));assert len(y)==len(parents)
   assert all(v>=0 for v in y) and sum(y)<=x[i]
   assert all(sum(y[c] for c,S in enumerate(parents) if S>>j&1)>=rows[j][i] for j in range(7));count+=1
 # All following inequalities are affine: endpoint verification proves them
 # throughout the interval. Their strict escape implications are the hand
 # four-box covering argument in the accompanying report.
 R,S,P,Q=B;u=retained(t)
 assert R[0]==x[0] and S[1]==x[1]
 assert all(u[2]<=cap[2] for cap in B)
 assert P[0]+R[1]>=1 and Q[1]+S[0]>=1 and P[1]+Q[0]>=1
 assert sum(x)-sum(u)==bound(t)
print('PASS',count,'rational endpoint part certificates; convex interpolation covers 0<=t<=1/100; tau*<=3/4−1047t/1000')
