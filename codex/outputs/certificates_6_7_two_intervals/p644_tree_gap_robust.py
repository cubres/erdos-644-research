"""Discovery only: robust three-request tree templates using gap trace bounds."""
from fractions import Fraction as F
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
from p644_triple_tree import model


def robust(x,y,z,T,ell):
    ants,templates,vertices,arr=model()
    f=arr.astype(float)/12
    const=f[:,:,4]+(f[:,:,1]-f[:,:,4])*float(x)+(f[:,:,2]-f[:,:,4])*float(y)+f[:,:,7]*float(z)
    # Variables q, d=a+q, b, c. The gap bounds d and c by ell.
    d=np.stack((arr[:,:,0]-arr[:,:,6]-arr[:,:,7],arr[:,:,6],arr[:,:,5],arr[:,:,3]-arr[:,:,4]),axis=-1)
    flat=d.reshape((-1,4));uniq,inv=np.unique(flat,axis=0,return_inverse=True)
    caps=[max(0,float(x+y+z-T)),float(ell),float(1-y-z),min(float(ell),float(1-x-y))]
    A=[[1,-1,0,0],[0,1,1,1],[-1,1,0,0]];b=[0,1,float(1-x-z)]
    scores=[]
    for row in uniq:
        ans=linprog(-row.astype(float)/12,A_ub=A,b_ub=b,bounds=[(0,cap) for cap in caps],method='highs')
        assert ans.success
        scores.append(-ans.fun)
    support=np.array(scores)[inv].reshape(const.shape)
    vals=np.max(const+support,axis=-1);i=int(np.argmin(vals))
    return {'index':i,'score':float(vals[i]),'template':[list(ants[k]) for k in templates[i]],'unique_objectives':len(uniq)}


if __name__=='__main__':
    import json
    from pathlib import Path
    p=[F('91561/183200'),F('49059/229000'),F('383541/1832000')]
    out=[]
    for i in range(3):
        x,y=[p[j] for j in range(3) if j!=i];z=p[i]
        q=robust(x,y,z,F(43,50),F(219,1000));q['point']=list(map(str,[x,y,z]));out.append(q);print(q,flush=True)
    Path('logs/astra_tree_gap_robust.json').write_text(json.dumps(out,indent=2))
