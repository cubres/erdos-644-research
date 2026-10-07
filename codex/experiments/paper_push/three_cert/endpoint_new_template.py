"""Exact certificate and projected capacity facets of the new2,2,3 support."""
import os
for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import sys,json,time
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from supports import maximal_extension,is_bad
import b4core as bc
p=Path(__file__).with_name('endpoint_u_all_support.json');d=json.loads(p.read_text());x=list(map(F,d['capacities']));T=[list(map(F,t)) for t in d['types']];asg=d['assignment'];parents=maximal_extension(d['support']);assert is_bad(parents)
out={'parents':parents,'assignment':asg,'assignment_roles':[0,0,1,1,2,2,2],'capacities':x,'types':T,'parts':[]}
for i in range(3):
 loads=[T[k][i] for k in asg];A=np.array([[-float(bool(S>>j&1)) for S in parents] for j in range(7)])
 r=linprog(np.ones(len(parents)),A_ub=A,b_ub=-np.array(list(map(float,loads))),bounds=(0,None),method='highs');assert r.status==0
 cert=None
 for den in [1000,100000,10000000,1000000000]:
  y=[F(float(v)).limit_denominator(den) for v in r.x];w=[F(float(-v)).limit_denominator(den) for v in r.ineqlin.marginals]
  if any(v<0 for v in y+w):continue
  if any(sum(y[k] for k,S in enumerate(parents) if S>>j&1)<loads[j] for j in range(7)):continue
  if any(sum(w[j] for j in range(7) if S>>j&1)>1 for S in parents):continue
  value=sum(y)
  if value!=sum(w[j]*loads[j] for j in range(7)):continue
  assert value<=x[i];cert={'primal':y,'dual':w,'mass':value,'loads':loads};break
 assert cert is not None;out['parts'].append(cert)
Path(__file__).with_suffix('.certificate.json').write_text(json.dumps(out,default=str,indent=2))
print('PRIMAL_DUAL_PASS',parents,[c['mass'] for c in out['parts']],flush=True)
start=time.process_time();V=bc.support_vertices(parents)
roles=out['assignment_roles'];P=sorted({tuple(sum(w[j] for j in range(7) if roles[j]==k) for k in range(3)) for w in V})
maximal=[v for v in P if not any(v!=w and all(a<=b for a,b in zip(v,w)) for w in P)]
template={'parents':parents,'assignment_roles':roles,'vertices':V,'projected_vertices':P,'maximal_projected':maximal,'vertex_cpu_seconds':time.process_time()-start}
Path(__file__).with_suffix('.template.json').write_text(json.dumps(template,default=str,indent=2))
print('CAPACITY',len(V),'vertices',len(P),'projected',len(maximal),'dominant',maximal,'CPU',time.process_time()-start,flush=True)
