"""Targeted numerical max-min Q discovery for one complementary response.

This is nonconvex numerical optimization. Failure to find a response is
not an infeasibility certificate. Rational successful responses can be
checked separately with the standard-library interval checker.
"""
import argparse
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from p644_agent_global_interval_survivor import base_atoms,with_a_flip,with_seventh_pair


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--stage',choices=['five_max_common','seven_small_P','seven_mixed_P','loaded'],required=True)
    ap.add_argument('--leave-a',type=int,default=0)
    ap.add_argument('--input')
    ap.add_argument('--delete-indices')
    ap.add_argument('--starts',type=int,default=30)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    c=F(6,25)
    atoms=base_atoms(c)
    if args.stage in ('seven_small_P','seven_mixed_P'):
        atoms=with_seventh_pair(with_a_flip(atoms))
    if args.stage=='loaded':
        data=json.loads(Path(args.input).read_text())
        atoms=[(tuple(v['bits']),F(v['mass'])) for v in data['atoms']]
    n=len(atoms); npairs=len(atoms[0][0]); weights=np.array([float(w) for s,w in atoms])
    deletion=np.zeros(n)
    if args.stage=='five_max_common':
        for i,(s,w) in enumerate(atoms):
            old=s[:3]
            if (old==(0,0,0) and s[3]==0) or old==(1,1,1) or \
               (old==(0,1,1) and s[3:5]==(0,0)) or \
               (old==(1,0,0) and s[3:5]==(1,1)) or \
               (old in ((1,0,1),(1,1,0)) and s[3]==1):
                deletion[i]=float(w)
    elif args.stage=='seven_small_P':
        for i,(s,w) in enumerate(atoms):
            if s[:3] in ((0,0,0),(1,0,0)):
                deletion[i]=float(w)
        # A prescribed 1/10000 portion of 111 excludes the old rows
        # missing A union C while preserving a legal total budget.
        i=next(i for i,(s,w) in enumerate(atoms) if s[:3]==(1,1,1))
        deletion[i]=.0001
    elif args.stage=='seven_mixed_P':
        for i,(s,w) in enumerate(atoms):
            if (s[:3]==(0,0,0) and i!=args.leave_a) or \
               (s[:3]==(0,1,1) and s[3]==0) or \
               (s[:3]==(1,0,0) and s[4]==0):
                deletion[i]=float(w)
    else:
        for i in map(int,args.delete_indices.split(',')):
            deletion[i]=weights[i]
    assert deletion.sum()<=.75+1e-9
    caps=weights-deletion
    active=np.flatnonzero(caps>1e-10)
    mats=[]
    for ps in itertools.combinations(range(npairs),2):
        a=np.zeros((4,n))
        for i,(s,w) in enumerate(atoms):a[2*s[ps[0]]+s[ps[1]],i]=1
        mats.append((ps,a[:,active],a@weights))
    def qs(x):
        g=x[:-1]
        values=[]
        for ps,a,m in mats:
            z=a@g
            values.append(z[0]*m[3]+z[3]*m[0]-2*z[0]*z[3]+
                          z[1]*m[2]+z[2]*m[1]-2*z[1]*z[2])
        return np.array(values)
    def jac(x):
        rows=[]
        for ps,a,m in mats:
            z=a@x[:-1]
            grad=np.array([m[3]-2*z[3],m[2]-2*z[2],m[1]-2*z[1],m[0]-2*z[0]])@a
            rows.append(np.r_[grad,-1])
        return np.array(rows)
    constraints=[{'type':'eq','fun':lambda x:x[:-1].sum()-1,
                  'jac':lambda x:np.r_[np.ones(len(active)),0]},
                 {'type':'ineq','fun':lambda x:qs(x)-x[-1],'jac':jac}]
    rng=np.random.default_rng(644)
    best=None
    for j in range(args.starts):
        if j==0:g=caps[active]/caps.sum()
        else:
            g=caps[active]*rng.uniform(.2,1,len(active))
            # Normalize by capped water filling.
            lo,hi=0.,100.
            for _ in range(60):
                mid=(lo+hi)/2
                if np.minimum(caps[active],mid*g).sum()<1:lo=mid
                else:hi=mid
            g=np.minimum(caps[active],hi*g)
        x=np.r_[g,0.]
        res=minimize(lambda x:-x[-1],x,jac=lambda x:np.r_[np.zeros(len(active)),-1],
                     method='SLSQP',bounds=[(0,float(v)) for v in caps[active]]+[(0,1)],
                     constraints=constraints,options={'ftol':1e-12,'maxiter':1500})
        if abs(res.x[:-1].sum()-1)<1e-7 and np.min(qs(res.x)-res.x[-1])>=-1e-7:
            if best is None or res.x[-1]>best.x[-1]:best=res
    out={'stage':args.stage,'status':'numerical nonconvex discovery only',
         'deletion_mass':float(deletion.sum()),'starts':args.starts,
         'old_atoms':[{'bits':list(s),'mass':str(w),'deleted_mass':float(deletion[i])}
                      for i,(s,w) in enumerate(atoms)]}
    if best is not None:
        g=np.zeros(n);g[active]=best.x[:-1]
        out.update({'max_min_new_Q_found':float(best.x[-1]),'solver_success':bool(best.success),
                    'response_masses':g.tolist(),
                    'new_triples':[{'retained_pairs':[p+1 for p in ps],'Q':float(q)}
                                   for (ps,a,m),q in zip(mats,qs(best.x))]})
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('old_atoms','new_triples')},indent=2))


if __name__=='__main__':main()
