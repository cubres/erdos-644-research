"""Bounded all-support discovery for the endpoint anchors plus U*.
An infeasible floating MILP is recorded as numerical evidence, not an exact
certificate. Any BAD witness is reconstructed and checked over rationals.
"""
import os
for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import sys,time,json
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
from w4_typeclosed_lib import bad_tuple_milp,support_min_mass
p=Path('outputs/paper_push_endpoint_counterstate.json');d=json.loads(p.read_text());x=list(map(F,d['capacities']));T=[list(map(F,t)) for t in d['types']]+[[F(249,500),F(251,500),F(0)]]
start=time.process_time();st,asg,cells=bad_tuple_milp(T,x,time_limit=60,verbose=False)
r={'status':st,'capacities':x,'types':T,'assignment':asg,'cpu_seconds':time.process_time()-start,'time_limit':60}
if st=='BAD':
 support=sorted({S for i,S in cells});assert all(a|b!=127 for a in support for b in support)
 mass=[support_min_mass(support,[T[k][i] for k in asg]) for i in range(3)]
 r['support']=support;r['exact_mass']=mass;r['exact_bad_tuple_verified']=all(v is not None and v<=x[i] for i,v in enumerate(mass))
 r['cell_masses_float']=[[i,S,v] for (i,S),v in cells.items()]
else:r['solver_message']=cells;r['scope']='Numerical MILP status only; no exact P7 certificate.'
out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(r,default=str,indent=2));print(json.dumps(r,default=str),flush=True)
