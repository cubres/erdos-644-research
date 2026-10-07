"""Find rational primal certificates at the two interval endpoints."""
import json
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
from endpoint_interval_model import family,boxes,PARENTS,ASSIGNMENTS,END
out={'interval':['0',str(END)],'endpoints':[]}
for t in (F(0),END):
 x,T=family(t);ends={'t':t,'boxes':[]}
 for cap,parents,asg in zip(boxes(t),PARENTS,ASSIGNMENTS):
  rows=[(T+(cap,))[j] for j in asg];parts=[]
  for i in range(3):
   loads=[row[i] for row in rows];A=np.array([[-float(bool(S>>j&1)) for S in parents] for j in range(7)])
   r=linprog(np.ones(len(parents)),A_ub=A,b_ub=-np.array(list(map(float,loads))),bounds=(0,None),method='highs');assert r.status==0
   cert=None
   for den in (1000,100000,10000000,1000000000):
    y=[F(float(v)).limit_denominator(den) for v in r.x]
    if any(v<0 for v in y) or sum(y)>x[i]:continue
    if any(sum(y[k] for k,S in enumerate(parents) if S>>j&1)<loads[j] for j in range(7)):continue
    cert=y;break
   assert cert is not None,(t,cap,i);parts.append(cert)
  ends['boxes'].append({'parts':parts})
 out['endpoints'].append(ends)
p=Path(__file__).with_name('endpoint_interval_certificate.json');p.write_text(json.dumps(out,default=str,indent=2));print(p)
