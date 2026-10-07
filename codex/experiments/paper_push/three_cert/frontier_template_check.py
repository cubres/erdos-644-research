"""Check a discovered V4 tuple at the exact parent witness and its whole region."""
import os
for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import sys,json,pickle
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
import search6 as s
import exactcert,fast_duals
from strict_types import strict_system
from v4_templates import CELLS
prefix=Path(sys.argv[1]);diag=json.load(open(str(prefix)+'.diagnostic.json'))
f=pickle.load(open(str(prefix)+'.frontier.pkl','rb'));nt=f['nt'];n=s.nv(nt)
C=f['cons'][:-diag['removed_tail_constraints']];E=f['eqs']
z=list(map(F,diag['point']))
asg=[7,2,1,1,1,1,0];tp=['S',[CELLS,asg]]
ineq=s.template_ineqs(tp)
margins=[h-sum(v*z[j] for j,v in d.items()) for d,h in ineq]
assert min(margins)>=0
proved=[];unproved=[]
for idx,(d,h) in enumerate(ineq):
    cert=fast_duals.prove_max(C,E,d,h,n)
    if cert is not None:
        assert exactcert.check_max(cert,C,E,d,h);proved.append([idx,'plain',s.enc(cert)]);continue
    C2,E2,d2,h2=strict_system(C,E,d,h,n)
    cert=fast_duals.prove_max(C2,E2,d2,h2,n+1)
    if cert is not None:
        assert exactcert.check_max(cert,C2,E2,d2,h2);proved.append([idx,'strict',s.enc(cert)])
    else:unproved.append(idx)
out={'template':tp,'exact_point_fits':True,'point_min_margin':str(min(margins)),
     'point_margins':list(map(str,margins)),'whole_region_closes':not unproved,
     'proved_inequalities':proved,'unproved_inequalities':unproved}
Path(str(prefix)+'.template_check.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k not in ('proved_inequalities','point_margins')},indent=2))
