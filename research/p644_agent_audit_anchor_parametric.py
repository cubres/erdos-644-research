"""New symbolic-q attempt at a two-anchor coefficient approaching 23/32.

This file only generates/tests the parametric candidate.  It does not import
or change the already certified concrete construction.
"""
from pathlib import Path
import argparse,json,sys,time
WORK=Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work')
sys.path.insert(0,str(WORK/'research_dependencies'))
import z3
ROOT=Path(__file__).parent/'logs/astra_agent_audit_anchor_parametric'

def generate():
    s=z3.Solver();q=z3.Real('q');R=z3.RealVal
    s.add(q>=R('87/100'),q<R('7/8'))
    delta=q-R('6/7');eps=(R('7/8')-q)/10
    p=R('3/7')-R('5/4')*delta-eps
    end=3-3*q-eps/2
    midlo=q/2+eps/2;midhi=q/2+3*eps/2
    central=R('3/7')+R('9/4')*delta+3*eps/2
    intervals=[(1-q,end),(p,p),(midlo,midhi),(central,1-central),
               (1-midhi,1-midlo),(1-p,1-p),(1-end,q)]
    am=[m for m in range(1,64)if bin(m).count('1')>=3]
    bm=[m for m in range(1,64)if bin(m).count('1')>=2]
    a={m:z3.Real('a_%d'%m)for m in am};b={m:z3.Real('b_%d'%m)for m in bm}
    for v in list(a.values())+list(b.values()):s.add(v>=0)
    s.add(z3.Sum(list(a.values()))==q,z3.Sum(list(b.values()))==q)
    for i,m in enumerate(am):
        for n in am[i+1:]:
            if m&n==0:s.add(z3.Or(a[m]==0,a[n]==0))
        for n in bm:
            if m&n==0:s.add(z3.Or(a[m]==0,b[n]==0))
    traces=[]
    for j in range(6):
        da=z3.Sum([v for m,v in a.items()if m>>j&1]);db=z3.Sum([v for m,v in b.items()if m>>j&1])
        s.add(da+db==2*q-1);tr=q-da;traces.append(tr)
        s.add(z3.Or(*[z3.And(tr>=lo,tr<=hi)for lo,hi in intervals]))
    for j in range(5):s.add(traces[j]<=traces[j+1])
    ROOT.mkdir(exist_ok=True);(ROOT/'parametric.smt2').write_text(s.to_smt2())
    return s,q,traces

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=60)
    p.add_argument('--solver',choices=['cvc5','z3','generate'],default='z3');args=p.parse_args()
    s,q,traces=generate()
    if args.solver=='cvc5':
        from p644_box_case_cvc5 import worker
        print(json.dumps(worker(('parametric',args.seconds,str(ROOT))),indent=2))
    elif args.solver=='z3':
        s.set(timeout=int(1000*args.seconds));start=time.time();r=s.check()
        out={'status':str(r),'seconds':time.time()-start}
        if r==z3.sat:
            m=s.model();out.update(q=str(m.eval(q)),traces=[str(m.eval(t))for t in traces],model=str(m))
        if r==z3.unknown:out['reason']=s.reason_unknown()
        (ROOT/'parametric_z3.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
