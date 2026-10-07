"""Four-role non-Fano support learned from balanced residual points.

Role assignment a,b,b,c,d,d,b. Projected vertices were computed exactly from
the original support-polytope enumerator; final proofs retain ordinary S nodes.
"""
import itertools
import numpy as np
from b4core import TOFF
CELLS=[15,23,56,77,78,85,86,91,99]
WEIGHTS=np.array([[0,0,1,0],[0,1,0,1],[1/6,1/2,0,1],
                 [1/6,1/2,1/2,1/2],[1/6,3/4,1/4,3/4],
                 [1/3,1,0,0],[1/2,0,0,1],[1/2,0,1/2,1/2],
                 [1/2,1/4,1/4,3/4],[1,0,0,0]])
_roles={}
def candidates(Z,nt,top=15):
    if nt not in _roles:_roles[nt]=np.array(list(itertools.product(range(nt),repeat=4)),dtype=int)
    roles=_roles[nt];scores=[]
    for z in Z:
        tt=z[TOFF:TOFF+3*nt].reshape(nt,3)
        load=np.einsum('wv,rvp->rwp',WEIGHTS,tt[roles]).max(axis=1)
        scores.append((z[:3]-load).min(axis=1))
    scores=np.array(scores);mins=scores.min(axis=0)
    def template(j):
        a,b,c,d=map(int,roles[j]);return ['S',[CELLS,[a,b,b,c,d,d,b]]]
    good=np.flatnonzero(mins>=-1e-9);ordered=good[np.argsort(-mins[good])][:top]
    cands=[(template(j),float(mins[j])) for j in ordered]
    ok=scores>1e-7;count=ok.sum(axis=0);m=np.where(ok,scores,9.0).min(axis=0)
    rank=count+np.minimum(m,1)*.5;j=int(rank.argmax())
    best=(template(j),float(rank[j])) if count[j]>0 else None
    return cands,best
