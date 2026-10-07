"""Three-request cover of the candidate-pair tree after a partial-core cut.

Parts are Q,X,Y,C,D,B,A,ZminusQ. Edges are Q-X,Q-Y,Q-C,Q-D,
X-B,Y-A,C-ZminusQ. All 16527 positive-part antichain templates are
included. The dual arrangement on three request prices has ten vertices.
Numerical response optimization is discovery only.
"""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import numpy as np
from p644_matching_three import model as matching_model,blockers


@lru_cache(None)
def model():
    mm=matching_model();ants=sorted({L for t in mm[0] for L in t});vertices=mm[1]
    idx={L:i for i,L in enumerate(ants)}
    price=np.array([[int(12*min(sum(p[j] for j in range(3) if m>>j&1) for m in L)) for p in vertices] for L in ants],dtype=np.int8)
    blocks=[idx[blockers(L)] for L in ants]
    compatible=[[j for j,M in enumerate(ants) if all(a&b for a in L for b in M)] for L in ants]
    templates=[];lab_indices=[]
    for q in range(len(ants)):
        for x,y,c in product(compatible[q],repeat=3):
            templates.append((q,x,y,c))
            lab_indices.append((q,x,y,c,blocks[q],blocks[x],blocks[y],blocks[c]))
    assert len(templates)==16527
    coeff=price[np.array(lab_indices)].transpose(0,2,1)
    return ants,templates,vertices,coeff


def best(weights,exact=False):
    ants,ts,vs,coeff=model();w=np.array([float(F(x)) if isinstance(x,str) else float(x) for x in weights])
    costs=np.max(np.einsum('ijk,k->ij',coeff,w),axis=1)/12
    i=int(np.argmin(costs))
    if not exact:return float(costs[i]),i
    w=list(map(F,weights));vals=[sum(F(int(a),12)*b for a,b in zip(row,w)) for row in coeff[i]]
    return {'template':[list(ants[j]) for j in ts[i]],'index':i,'budget':str(max(vals))}


def probe():
    from scipy.optimize import differential_evolution
    from pathlib import Path
    import json,time
    model();T=F(31,36);base=[F(89,200),F(42,125),F(49,250)];rows=[];start=time.monotonic()
    for leftover in range(3):
        x,y=[base[j] for j in range(3) if j!=leftover];z=base[leftover]
        qcap=x+y+z-T;a0=1-x-z;b0=1-y-z;c0=1-x-y
        def unpack(v):
            q=float(qcap)*v[0];a=min(float(a0),1-q)*v[1]
            b=min(float(b0),1-q-a)*v[2];c=min(float(c0),1-q-a-b)*v[3]
            return q,a,b,c
        def fun(v):
            q,a,b,c=unpack(v)
            return -best([q,x,y,c,float(c0)-c,b,a,float(z)-q])[0]
        res=differential_evolution(fun,[(0,1)]*4,seed=644,popsize=8,maxiter=80,tol=1e-6)
        q,a,b,c=unpack(res.x)
        weights=[F(float(v)).limit_denominator(10**6) for v in [q,x,y,c,float(c0)-c,b,a,float(z)-q]]
        row={'triple':list(map(str,(x,y,z))),'response':[q,a,b,c],'budget':-res.fun,'selected':best(weights,True)}
        rows.append(row);print(row,'seconds',round(time.monotonic()-start,1),flush=True)
    Path('logs/astra_triple_tree_probe.json').write_text(json.dumps(rows,indent=1))

if __name__=='__main__':probe()
