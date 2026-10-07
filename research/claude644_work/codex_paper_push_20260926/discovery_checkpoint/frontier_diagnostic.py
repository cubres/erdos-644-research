"""Extract and exactly verify a rational witness from a checkpoint frontier.
This is a diagnostic, never a proof of a hypothetical family's existence.
"""
import os
for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import sys,pickle,json,itertools
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import sympy as sp
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
import search6 as s
from strict_types import strict_forms
from strong_blocker import optimal_request
import fast_duals,exactcert
prefix=Path(sys.argv[1]);d=pickle.load(open(str(prefix)+'.frontier.pkl','rb'))
C,E=d['cons'],d['eqs'];nt=d['nt'];n=s.nv(nt)
original_C=list(C)
forms=strict_forms(C,n)
Cp=list(C)
for row,rhs in forms:
    q={j:-v for j,v in row.items()};q[n]=F(1);Cp.append((q,-rhs))
Cp.append(({n:F(1)},F(1)))
A,b=s.tomat(Cp,n+1);Ae,be=s.tomat(E,n+1)
obj=np.zeros(n+1);obj[-1]=-1
r=s.lp(obj,(A,b,Ae,be),n+1)
relaxed=0;empty_cert=None
if r.status==2:
    empty_cert=fast_duals.prove_empty(C,E,n)
    assert empty_cert is not None and exactcert.check_empty(empty_cert,C,E)
    while r.status!=0 and relaxed<8:
        relaxed+=1;C=original_C[:-relaxed];Cp=list(C)
        for row,rhs in forms:
            q={j:-v for j,v in row.items()};q[n]=F(1);Cp.append((q,-rhs))
        Cp.append(({n:F(1)},F(1)))
        A,b=s.tomat(Cp,n+1);Ae,be=s.tomat(E,n+1)
        r=s.lp(obj,(A,b,Ae,be),n+1)
assert r.status==0, r.message
out={'path':d['path'],'nt':nt,'nreq':d['nreq'],'strict_margin_float':float(r.x[-1]),
     'removed_tail_constraints':relaxed,'original_frontier_exactly_empty':empty_cert is not None,
     'original_frontier_farkas':s.enc(empty_cert) if empty_cert else None,
     'removed_constraints':s.enc(original_C[len(C):])}
print('strict_margin',r.x[-1],flush=True)
if r.x[-1]<=1e-9:
    out['status']='NO_STRICT_WITNESS';Path(str(prefix)+'.diagnostic.json').write_text(json.dumps(out,indent=2));raise SystemExit
active=[i for i,v in enumerate(b-A@r.x) if abs(v)<1e-8]
rows=E+[Cp[i] for i in active]
M=sp.Matrix([[sp.Rational(v.get(j,0)) for j in range(n+1)]+[sp.Rational(h)] for v,h in rows])
rr,pivs=M.rref()
assert pivs==tuple(range(n+1)), ('nonunique/inconsistent',pivs)
z=[F(rr[i,n+1]) for i in range(n+1)]
def dot(q):return sum(F(v)*z[j] for j,v in q.items())
assert all(dot(q)<=h for q,h in Cp)
assert all(dot(q)==h for q,h in E)
assert z[-1]>0
out['exact_region_witness']=True;out['strict_margin']=str(z[-1]);out['point']=[str(v) for v in z[:-1]]
x=z[:3];tau=z[6];T=[z[s.TOFF+3*k:s.TOFF+3*k+3] for k in range(nt)]
out['capacities']=[str(v) for v in x];out['global_tau_parameter']=str(tau)
out['types']=[[str(v) for v in t] for t in T];out['types_float']=[[float(v) for v in t] for t in T]
# Every maximal free-box supremum is a corner at a coordinate of a known
# positive type or the full capacity. A threshold is approached from below.
opts=[[('N',x[i])]+[(k,t[i]) for k,t in enumerate(T) if t[i]>0] for i in range(3)]
best=None
for ch in itertools.product(*opts):
    if not all(any(q[0]!='N' and t[i]>=q[1] for i,q in enumerate(ch)) for t in T):continue
    cap=[q[1] for q in ch];cost=sum(x)-sum(cap)
    if best is None or cost<best[0]:best=(cost,ch,cap)
cost,ch,cap=best
out['finite_tau_star']=str(cost);out['finite_tau_float']=float(cost)
out['free_box_supremum']=[str(v) for v in cap];out['free_box_choices']=[q[0] for q in ch]
slack=tau-cost;retain=[v*(1-slack/sum(cap)) for v in cap]
assert all(0<=retain[i]<=x[i] for i in range(3))
assert sum(x)-sum(retain)==tau
margins=[max(t[i]-retain[i] for i in range(3)) for t in T]
assert min(margins)>0
out['next_legal_retained_box']=[str(v) for v in retain]
out['next_legal_retained_box_float']=[float(v) for v in retain]
out['next_delete_vector']=[str(x[i]-retain[i]) for i in range(3)]
out['next_request_exact_cost']=str(sum(x)-sum(retain))
out['min_exclusion_margin']=str(min(margins));out['min_exclusion_margin_float']=float(min(margins))
out['status']='EXACT_REGION_WITNESS_AND_CHEAP_BLOCKER'
Path(str(prefix)+'.diagnostic.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k not in ('point','types','next_legal_retained_box','next_delete_vector')},indent=2))
