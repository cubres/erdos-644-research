"""Numerical search only for a worst gap-constrained fourth response."""
from fractions import Fraction as F
from pathlib import Path
from scipy.optimize import differential_evolution
import json
from p644_triple_tree import best


def run(x,y,z,T,ell):
    x,y,z,T,ell=map(float,(x,y,z,T,ell))
    def unpack(v):
        q=max(0,x+y+z-T)*v[0]
        d=q+(min(ell,q+1-x-z)-q)*v[1]
        c=min(ell,1-x-y,1-d)*v[2]
        b=min(1-y-z,1-d-c)
        return [q,x,y,c,1-x-y-c,b,d-q,z-q]
    def fun(v): return -best(unpack(v))[0]
    res=differential_evolution(fun,[(0,1)]*3,seed=644,popsize=10,maxiter=180,tol=1e-8)
    weights=[F(v).limit_denominator(10**7) for v in unpack(res.x)]
    return {'parameters':list(map(str,(x,y,z,T,ell))),'budget':-res.fun,'response_weights':list(map(str,weights)),'selected_template':best(weights,True)}


if __name__=='__main__':
    p=[F('91561/183200'),F('49059/229000'),F('383541/1832000')]
    rows=[]
    for x,y,z in [p,[p[0],p[2],p[1]]]:
        q=run(x,y,z,F(43,50),F(219,1000));rows.append(q);print(q,flush=True)
    Path('logs/astra_tree_gap_probe.json').write_text(json.dumps(rows,indent=2))
