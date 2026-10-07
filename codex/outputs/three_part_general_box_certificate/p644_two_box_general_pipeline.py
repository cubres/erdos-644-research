"""Discovery for two three-part boxes without intersectingness.

Uses sufficient constructions with full hand or rational capacity proofs.
Every new UNSAT outcome still requires independent input/proof auditing.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import json
import multiprocessing
import time
import p644_box_dimension_pipeline as pipeline
import p644_two_box_outer as outer
z3=pipeline.z3


def worker(task):
    case,seconds,mixed=task;p=3;key=''.join(map(str,case));root=Path('logs/astra_two_box_general_3'+('_mixed' if mixed else ''));root.mkdir(exist_ok=True)
    z3.set_param(proof=True);started=time.time()
    single,groups=pipeline.system(3,nonline=True,homogeneous=True,tetra=True)
    # 36 transversal groups, then self/midpoint groups for the two boxes.
    # The next group asserts cross-intersectingness, which is not assumed.
    assert len(groups[40])==len(outer.failure_facets([(1,1,1)]))
    groups=groups[:40]+groups[41:]
    if mixed:single += [outer.mul(-1,a) for a in outer.failure_facets([(1,1,1)])]
    margin=outer.var(outer.GAMMA)
    menus=[[(6,5,5)],[(5,6,6),(4,3,4),(4,0,3)],[(2,5,4),(1,1,1)]]
    for menu in menus:
        for flip in (False,True):groups.append([outer.sub(a,margin) for a in outer.failure_facets(menu,flip)])
    names=['x0','x1','x2','a0','a1','a2','A0','A1','A2','b0','b1','b2','B0','B1','B2','gamma'];v=z3.Reals(' '.join(names))
    af=lambda a:z3.simplify(z3.Sum(*[z3.RealVal(str(q))*v[i] for i,q in enumerate(a[:-1]) if q],z3.RealVal(str(a[-1]))))
    s=z3.SolverFor('QF_LRA');s.set(timeout=int(seconds*1000))
    for i,w in enumerate(v):s.add(w>=0,w<=(2 if i<3 else F(1,4) if i==15 else 1))
    s.add(v[-1]>0)
    for a in single:s.add(af(a)>=0)
    for group in groups:s.add(z3.Or(*(af(a)>=0 for a in group)))
    for i,state in enumerate(case):
        for k in range(2):s.add(v[3+6*k+i]>0 if state>>k&1 else v[3+6*k+i]==0)
    for i in range(2):
        if case[i]==case[i+1]:s.add(v[i]<=v[i+1])
    text=s.to_smt2();stem=root/key;stem.with_suffix('.smt2').write_text(text);begin=time.time();answer=s.check()
    result={'case':case,'mixed_disjoint_witness':mixed,'answer':str(answer),'seconds':time.time()-begin,'setup_seconds':begin-started,
            'input_sha256':hashlib.sha256(text.encode()).hexdigest(),'group_sizes':[len(q) for q in groups],
            'independent_verification':'PENDING'}
    if answer==z3.unsat:
        proof=s.proof().sexpr();stem.with_suffix('.proof').write_text(proof);result['proof_sha256']=hashlib.sha256(proof.encode()).hexdigest()
    elif answer==z3.sat:
        m=s.model();point=[F(str(m.eval(w,model_completion=True))) for w in v]
        value=lambda a:sum(q*t for q,t in zip(a[:-1],point))+a[-1]
        assert point[-1]>0 and all(value(a)>=0 for a in single) and all(any(value(a)>=0 for a in group) for group in groups)
        result['point']=list(map(str,point));result['exact_model_checked']=True
    else:result['reason']=s.reason_unknown()
    stem.with_suffix('.json').write_text(json.dumps(result,indent=2));return result


def main(seconds=60,workers=4,mixed=False):
    root=Path('logs/astra_two_box_general_3'+('_mixed' if mixed else ''));root.mkdir(exist_ok=True)
    cases=sorted({pipeline.representative(q) for q in itertools.product(range(4),repeat=3)})
    tasks=[]
    for case in cases:
        path=root/(''.join(map(str,case))+'.json')
        if path.exists() and json.loads(path.read_text())['answer'] in ('sat','unsat'):continue
        tasks.append((case,seconds,mixed))
    print('General two-box cases',len(tasks),flush=True)
    with multiprocessing.get_context('spawn').Pool(workers,maxtasksperchild=1) as pool:
        for r in pool.imap_unordered(worker,tasks):print(r['case'],r['answer'],'seconds',round(r['seconds'],2),'setup',round(r['setup_seconds'],2),flush=True)
    print('FINISHED; new universal claims need independent auditing.',flush=True)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--seconds',type=float,default=60);parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--mixed',action='store_true')
    args=parser.parse_args();main(args.seconds,args.workers,args.mixed)
