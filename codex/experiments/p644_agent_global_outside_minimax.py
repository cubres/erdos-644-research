"""Numerical discovery for a forced response with an arbitrary disjoint partner.

The old rows are complementary cuts of U. Both new rows may have fresh
private points outside U. No numerical optimum is a proof certificate.
"""
import argparse
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--delete-indices',required=True)
    ap.add_argument('--target',type=float,default=.242)
    ap.add_argument('--starts',type=int,default=30)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    data=json.loads(Path(args.input).read_text())
    atoms=[(tuple(v['bits']),float(F(v['mass']))) for v in data['atoms']]
    weights=np.array([w for s,w in atoms]);n=len(atoms);npairs=len(atoms[0][0])
    deleted=set(map(int,args.delete_indices.split(',')))
    active=np.array([i for i in range(n) if i not in deleted]);ng=len(active)
    assert weights[list(deleted)].sum()<=.75+1e-9
    mats=[]
    for ps in itertools.combinations(range(npairs),2):
        mat=np.zeros((4,n))
        for i,(s,w) in enumerate(atoms):mat[2*s[ps[0]]+s[ps[1]],i]=1
        mats.append((ps,mat[:,active],mat))
    def qvalues(x):
        out=[]
        for ps,ag,ah in mats:
            g,h=ag@x[:ng],ah@x[ng:]
            out.append(g@h[[3,2,1,0]])
        return np.array(out)
    def qjac(x):
        out=[]
        for ps,ag,ah in mats:
            g,h=ag@x[:ng],ah@x[ng:]
            out.append(np.r_[h[[3,2,1,0]]@ag,g[[3,2,1,0]]@ah])
        return np.array(out)
    sumg=np.r_[np.ones(ng),np.zeros(n)];sumh=np.r_[np.zeros(ng),np.ones(n)]
    overlap=np.zeros((n,ng+n));overlap[:,ng:]=np.eye(n)
    for j,i in enumerate(active):overlap[i,j]=1
    cons=[{'type':'ineq','fun':lambda x:1-sumg@x[:-1],'jac':lambda x:np.r_[-sumg,0]},
          {'type':'ineq','fun':lambda x:1-sumh@x[:-1],'jac':lambda x:np.r_[-sumh,0]},
          {'type':'ineq','fun':lambda x:weights-overlap@x[:-1],'jac':lambda x:np.c_[-overlap,np.zeros(n)]},
          {'type':'ineq','fun':lambda x:qvalues(x[:-1])-x[-1],'jac':lambda x:np.c_[qjac(x[:-1]),-np.ones(len(mats))]}]
    bounds=[(0,weights[i]) for i in active]+[(0,w) for w in weights]+[(0,1)]
    rng=np.random.default_rng(644);best=None
    for j in range(args.starts):
        g=weights[active]*rng.uniform(.3,.8,ng);g*=min(1,.95/g.sum())
        fullg=np.zeros(n);fullg[active]=g
        h=(weights-fullg)*rng.uniform(.3,.8,n);h*=min(1,.95/h.sum())
        res=minimize(lambda x:-x[-1],np.r_[g,h,0],jac=lambda x:np.r_[np.zeros(ng+n),-1],
                     method='SLSQP',bounds=bounds,constraints=cons,
                     options={'ftol':1e-12,'maxiter':2000})
        if min(float(np.min(c['fun'](res.x))) for c in cons)>=-1e-7:
            if best is None or res.fun<best.fun:
                best=res
                print('discovery',j,-best.fun,flush=True)
    out={'status':'nonconvex numerical discovery; no infeasibility claim',
         'target_Q':args.target,'deletion_mass':float(weights[list(deleted)].sum()),
         'input':args.input,'delete_indices':sorted(deleted)}
    if best is not None:
        g=np.zeros(n);g[active]=best.x[:ng];h=best.x[ng:-1]
        out.update({'g':g.tolist(),'h':h.tolist(),
                    'outside_g':float(1-g.sum()),'outside_h':float(1-h.sum()),
                    'minimum_new_Q':float(qvalues(best.x[:-1]).min()),'solver_success':bool(best.success),
                    'Q_profile':[{'pairs':[a+1,b+1],'Q':float(q)} for ((a,b),ag,ah),q in zip(mats,qvalues(best.x[:-1]))]})
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
