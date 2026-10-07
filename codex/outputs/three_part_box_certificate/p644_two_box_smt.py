"""Exact-rational SMT encoding of the three-part, two-box candidate theorem.

This exports the whole decision problem. A solver result remains a discovery
result until the mathematical encoding and any proof artifact are audited.
"""
import argparse,json,sys,time
from pathlib import Path
from fractions import Fraction as F

DEPS=Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
sys.path.insert(0,str(DEPS))
import z3
from p644_two_box_outer import base_system,DIM,GAMMA


def main(seconds=120,proof=False,seed=0,compact=False):
    z3.set_param(proof=proof)
    v=z3.Reals('x0 x1 x2 a0 a1 a2 A0 A1 A2 b0 b1 b2 B0 B1 B2 gamma')
    def affine(a):
        return z3.Sum(*[z3.RealVal(str(c))*v[i] for i,c in enumerate(a[:-1]) if c],z3.RealVal(str(a[-1])))
    single,groups=base_system(tight=True,compact=compact)
    s=z3.SolverFor('QF_LRA');s.set(timeout=int(seconds*1000),random_seed=seed)
    for i,w in enumerate(v):
        s.add(w>=0,w<=(2 if i<3 else F(1,4) if i==GAMMA else 1))
    s.add(v[GAMMA]>0)
    for a in single:s.add(affine(a)>=0)
    for g in groups:s.add(z3.Or(*(affine(a)>=0 for a in g)))
    stem=Path('logs/astra_two_box_smt_%s%s'%(seed,'_compact' if compact else ''))
    stem.with_suffix('.smt2').write_text(s.to_smt2())
    print('Prepared exact QF_LRA problem:',len(s.assertions()),'assertions;',len(groups),'disjunctions.',flush=True)
    start=time.time();answer=s.check()
    out={'answer':str(answer),'elapsed':time.time()-start,'solver':z3.get_version_string(),'proof_enabled':proof,'seed':seed,'compact':compact}
    if answer==z3.sat:
        model=s.model();point=[F(str(model.eval(w,model_completion=True))) for w in v]
        # Exact numerical validation independent of Z3 evaluation.
        ev=lambda a:sum(c*w for c,w in zip(a[:-1],point))+a[-1]
        assert point[GAMMA]>0
        assert all(ev(a)>=0 for a in single)
        assert all(any(ev(a)>=0 for a in g) for g in groups)
        out['point']=list(map(str,point));out['point_rechecked']=True
    elif answer==z3.unsat and proof:
        proof_text=s.proof().sexpr();stem.with_suffix('.proof').write_text(proof_text)
        out['proof_bytes']=len(proof_text)
    elif answer==z3.unknown:out['reason']=s.reason_unknown()
    out['statistics']=str(s.statistics())
    stem.with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=120)
    ap.add_argument('--proof',action='store_true');ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--compact',action='store_true')
    a=ap.parse_args();main(a.seconds,a.proof,a.seed,a.compact)
