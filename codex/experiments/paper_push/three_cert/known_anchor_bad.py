"""Exact integer checks for bad tuples on exactly three rational anchor types."""
import itertools,json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from fano_v4_partner_oracle import PENCILS
ASG=np.array(list(itertools.product(range(3),repeat=7)),dtype=np.int64)
VROLES=np.array(list(itertools.product(range(3),repeat=4)),dtype=np.int64)
P=json.loads(Path('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy/astra_support_capacity_minimal.json').read_text())['minimal_functions']
PAIR=[]
for p in P:
 v=[[F(a),F(b)] for a,b in p['vertices']];den=math.lcm(*(q.denominator for row in v for q in row));PAIR.append((den,np.array([[int(q*den) for q in row] for row in v],dtype=np.int64)))

def known_bad(x,types):
 den=math.lcm(*(F(q).denominator for row in [x]+list(types) for q in row))
 xx=np.array([int(F(q)*den) for q in x],dtype=np.int64)
 T=np.array([[int(F(q)*den) for q in row] for row in types],dtype=np.int64)
 assert np.max(abs(T))*1000000<2**63
 rows=T[ASG];ok=(rows.sum(axis=1)<=4*xx).all(axis=1)
 for p in PENCILS:ok&=(rows[:,p,:].sum(axis=1)<=2*xx).all(axis=1)
 if ok.any():return {'kind':'FANO','assignment':ASG[np.flatnonzero(ok)[0]].tolist()}
 A,B,C,D=[T[VROLES[:,i]] for i in range(4)]
 cost=np.maximum.reduce([4*A,4*B,4*C,2*(A+B+C),4*D+2*(B+C),4*D+A+B+C])
 ok=(cost<=4*xx).all(axis=1)
 if ok.any():return {'kind':'V4','roles_a_b_c_d':VROLES[np.flatnonzero(ok)[0]].tolist()}
 for a,b in itertools.product(range(3),repeat=2):
  for k,(d,v) in enumerate(PAIR):
   load=v[:,0,None]*T[a]+v[:,1,None]*T[b]
   if (load<=d*xx).all():return {'kind':'PAIR','function':k,'roles':[a,b]}
 return None
