"""Heuristic response search with all three trace gaps, without theorem claims."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
from scipy.optimize import differential_evolution
from p644_triple_tree import best


def run(x,y,z,T,intervals):
    x,y,z,T=map(float,(x,y,z,T));qcap=max(0,x+y+z-T)
    def allowed(cap): return [(a,min(b,cap)) for a,b in intervals if a<=cap]
    rows=[]
    for di,ei,ci in product(allowed(1-x-z+qcap),allowed(1-y-z+qcap),allowed(1-x-y)):
        def unpack(v):
            q,d,e,c=v
            return [q,x,y,c,1-x-y-c,e-q,d-q,z-q]
        def violation(v):
            q,d,e,c=v
            return sum(max(0,t) for t in [q-d,q-e,d-q-(1-x-z),e-q-(1-y-z),d+e+c-q-1])
        def fun(v):
            vbad=violation(v)
            if vbad>1e-10:return 10*vbad
            return -best(unpack(v))[0]
        res=differential_evolution(fun,[(0,qcap),di,ei,ci],seed=644,popsize=8,maxiter=140,tol=1e-7)
        row={'trace_intervals':[di,ei,ci],'value':-res.fun,'violation':violation(res.x),'q_d_e_c':list(res.x)}
        if row['violation']<1e-9:
            weights=[F(float(v)).limit_denominator(10**7) for v in unpack(res.x)]
            row['selected_template']=best(weights,True);row['weights']=list(map(str,weights))
        print(row,flush=True);rows.append(row)
    return rows


if __name__=='__main__':
    rows=run(F(19,50),F(11,50),F(19,50),F(43,50),[(0,.224),(.369,.402),(.480,1.)])
    Path('logs/astra_pairgap_probe.json').write_text(json.dumps(rows,indent=2))
