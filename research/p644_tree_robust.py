"""Robust fixed-template bounds for the partial-core fourth response.

The response polytope is a box cut by q+a+b+c<=1. Its linear support
function is computed by the exact finite dual candidates gamma=0 or a
positive objective coefficient. Discovery uses floats to choose a template;
exported affine regions are built with Fraction arithmetic.
"""
from fractions import Fraction as F
from pathlib import Path
import json,numpy as np
from p644_triple_tree import model


def robust(x,y,z,T):
    ants,templates,vertices,arr=model();f=arr.astype(float)/12
    const=f[:,:,4]+(f[:,:,1]-f[:,:,4])*float(x)+(f[:,:,2]-f[:,:,4])*float(y)+f[:,:,7]*float(z)
    d=np.stack((f[:,:,0]-f[:,:,7],f[:,:,6],f[:,:,5],f[:,:,3]-f[:,:,4]),axis=-1)
    caps=np.array([max(0,float(x+y+z-T)),float(1-x-z),float(1-y-z),float(1-x-y)])
    gamm=np.concatenate([np.zeros((*d.shape[:2],1)),np.maximum(d,0)],axis=-1)
    val=gamm+np.sum(np.maximum(d[:,:,:,None]-gamm[:,:,None,:],0)*caps[None,None,:,None],axis=2)
    scores=np.max(const+np.min(val,axis=-1),axis=-1);i=int(np.argmin(scores))
    return {'index':i,'score':float(scores[i]),'template':[list(ants[k]) for k in templates[i]],
            'selectors':[int(a) for a in np.argmin(val[i],axis=-1)]}


def region(template,selectors):
    from p644_matching_three import blockers
    ants,ts,vertices,arr=model();labs=[tuple(L) for L in template]
    labs += [blockers(labs[0]),blockers(labs[1]),blockers(labs[2]),blockers(labs[3])]
    forms={(F(0),F(1),F(1),F(0))} # T>=x+y: initial two whole cells
    for p,choice in zip(vertices,selectors):
        f=[min(sum(p[j] for j in range(3) if mask>>j&1) for mask in L) for L in labs]
        const=(f[4],f[1]-f[4],f[2]-f[4],f[7])
        d=[f[0]-f[7],f[6],f[5],f[3]-f[4]]
        gamma=F(0) if choice==0 else max(F(0),d[choice-1])
        lq,la,lb,lc=[max(F(0),v-gamma) for v in d]
        # Caps a<=1-x-z, b<=1-y-z, c<=1-x-y.
        g=(const[0]+gamma+la+lb+lc,const[1]-la-lc,const[2]-lb-lc,const[3]-la-lb)
        forms.add(g)
        forms.add(tuple((v+(lq if j else 0))/(1+lq) for j,v in enumerate(g)))
    return sorted(forms)


def main():
    base=[F(89,200),F(42,125),F(49,250)];T=F(31,36);out=[]
    for leftover in range(3):
        x,y=[base[j] for j in range(3) if j!=leftover];z=base[leftover]
        q=robust(x,y,z,T);fs=region(q['template'],q['selectors'])
        bound=max(f[0]+f[1]*x+f[2]*y+f[3]*z for f in fs)
        q.update({'triple':list(map(str,(x,y,z))),'forms':[list(map(str,f)) for f in fs],'sufficient_budget':str(bound)})
        out.append(q);print(q,flush=True)
    Path('logs/astra_tree_robust.json').write_text(json.dumps(out,indent=1))

if __name__=='__main__':main()
