"""Exact-SMT discovery for arbitrary closed two-part type sets.

Only necessary consequences of a hypothetical high-transversal family
without any two-type bad tuple are asserted. Interval lengths supply
constraints that do not require the admissible set itself to be convex.
UNSAT needs an independent mathematical-input and proof audit.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import multiprocessing
import sys
import time
sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3


def worker(task):
    pure_low,pure_high,seconds,central=task;key='%d%d'%(pure_low,pure_high)
    root=Path('logs/astra_two_part_gap'+('_central' if central else ''));root.mkdir(exist_ok=True)
    raw=json.loads(Path('logs/astra_support_capacity_minimal.json').read_text())['minimal_functions']
    menu=[[tuple(map(F,v)) for v in row['vertices']] for row in raw]
    z3.set_param(proof=True);s=z3.SolverFor('QF_LRA');s.set(timeout=int(seconds*1000))
    x,y,l,c,g=z3.Reals('x y l c gamma');delta=x+y-z3.RealVal('7/4')
    q=lambda v:z3.RealVal(str(v))
    s.add(x>=0,y>=0,x<=q(F(7,4)),y<=q(F(7,4)),l>=0,c<=1,l<=c,c<=x,1-l<=y,g>0,g<=1)
    s.add(delta>=g,2*delta-(c-l)>=g)
    if pure_low:s.add(l==0)
    else:s.add(l>=g,x-l>=q(F(3,4))+g)
    if pure_high:s.add(c==1)
    else:s.add(1-c>=g,y-1+c>=q(F(3,4))+g)
    actual=[l,c]
    if central:
        a,b=z3.Reals('a b');actual=[l,a,b,c]
        s.add(l<=a,a<=b,b<=c,1-q(F(4,7))*y-a>=g,b-q(F(4,7))*x>=g,delta-(b-a)>=g)
    for shape in menu:
        # Actual endpoint pairs cannot realize a bad tuple.
        for a in actual:
            for b in actual:
                s.add(z3.Or(*[f>=g for u,v in shape for f in (q(u)*a+q(v)*b-x,q(u)*(1-a)+q(v)*(1-b)-y)]))
        # Any forbidden interval of possible partner types has length <delta
        # when clipped to [l,c], since every genuine type gap is <delta.
        for t in actual:
            lows=[l];highs=[c];empty=[]
            for u,v in shape:
                if u:
                    lows.append((q(u+v)-y-q(v)*t)/q(u))
                    highs.append((x-q(v)*t)/q(u))
                else:
                    empty.extend([q(v)*t-x,q(v)*(1-t)-y])
            if any(u for u,v in shape):
                empty += [delta-hi+lo for hi in highs for lo in lows]
            s.add(z3.Or(*[f>=g for f in empty]))
    text=s.to_smt2();(root/(key+'.smt2')).write_text(text);start=time.time();answer=s.check()
    result={'case':key,'answer':str(answer),'seconds':time.time()-start,'input_sha256':hashlib.sha256(text.encode()).hexdigest(),
            'independent_verification':'PENDING'}
    if answer==z3.unsat:(root/(key+'.proof')).write_text(s.proof().sexpr())
    elif answer==z3.sat:
        model=s.model();result['point']={str(v):str(model.eval(v,model_completion=True)) for v in [x,y,g]+actual}
    else:result['reason']=s.reason_unknown()
    (root/(key+'.json')).write_text(json.dumps(result,indent=2));return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--seconds',type=float,default=120);parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--central',action='store_true')
    args=parser.parse_args()
    with multiprocessing.get_context('spawn').Pool(args.workers,maxtasksperchild=1) as pool:
        for row in pool.imap_unordered(worker,[(i,j,args.seconds,args.central) for i in (0,1) for j in (0,1)]):print(row,flush=True)
