"""Four-type V support supplied by the independent theory agent.

Row order b,c,d,d,d,d,a. The exact per-part support cost is
max(a,b,c,(a+b+c)/2,d+(b+c)/2,d+(a+b+c)/4).
The original exact support-vertex checker independently verifies every use.
"""
import itertools
import numpy as np
from b4core import TOFF
CELLS=[3,60,77,86,92,106,108,113,116,120]
_roles={}
def candidates(Z,nt,top=15):
    if nt not in _roles:
        _roles[nt]=np.array([(a,b,c,d) for a in range(nt) for b in range(nt)
                            for c in range(b,nt) for d in range(nt)],dtype=int)
    roles=_roles[nt];scores=[]
    for z in Z:
        tt=z[TOFF:TOFF+3*nt].reshape(nt,3)
        a,b,c,d=[tt[roles[:,i]] for i in range(4)]
        load=np.maximum.reduce([a,b,c,(a+b+c)/2,d+(b+c)/2,d+(a+b+c)/4])
        scores.append((z[:3]-load).min(axis=1))
    scores=np.array(scores);mins=scores.min(axis=0)
    def template(j):
        a,b,c,d=map(int,roles[j])
        return ['S',[CELLS,[b,c,d,d,d,d,a]]]
    good=np.flatnonzero(mins>=-1e-9)
    ordered=good[np.argsort(-mins[good])][:top]
    cands=[(template(j),float(mins[j])) for j in ordered]
    ok=scores>1e-7;count=ok.sum(axis=0)
    m=np.where(ok,scores,9.0).min(axis=0)
    rank=count+np.minimum(m,1)*.5
    j=int(rank.argmax())
    best=(template(j),float(rank[j])) if count[j]>0 else None
    return cands,best
