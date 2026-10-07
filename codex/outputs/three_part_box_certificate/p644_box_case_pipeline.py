"""Resumable exact-SMT case pipeline for the structured two-box question.

Support cases are exhaustive up to permutations of parts and exchange of the
two components. UNKNOWN is retained as an open leaf. Only explicitly UNSAT
leaves carry solver proof files; these still need an independent proof audit.
No result from this pipeline is a proof of the unrestricted Erdos problem.
"""
import itertools,json,multiprocessing,sys,time,hashlib
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3
from p644_two_box_outer import base_system,DIM,GAMMA

ROOT=Path('logs/astra_box_case_pipeline')


def representative(q):
    a=tuple(sorted(q));b=tuple(sorted({0:0,1:2,2:1,3:3}[x] for x in q))
    return min(a,b)


def cases():
    reps=sorted({representative(q) for q in itertools.product(range(4),repeat=3)})
    assert all(representative(q) in reps for q in itertools.product(range(4),repeat=3))
    return reps


def worker(task):
    q,seconds,line_template=task;key=''.join(map(str,q))+('_line' if line_template else '');stem=ROOT/key
    history=[]
    if stem.with_suffix('.json').exists():
        previous=json.loads(stem.with_suffix('.json').read_text())
        history=previous.get('previous_attempts',[])+[{k:previous[k] for k in ('answer','elapsed','limit','reason') if k in previous}]
    z3.set_param(proof=True)
    v=z3.Reals('x0 x1 x2 a0 a1 a2 A0 A1 A2 b0 b1 b2 B0 B1 B2 gamma')
    single,groups=base_system(tight=True,compact=True,symmetry=False,line_template=line_template)
    def af(a):return z3.simplify(z3.Sum(*[z3.RealVal(str(c))*v[i] for i,c in enumerate(a[:-1]) if c],z3.RealVal(str(a[-1]))))
    s=z3.SolverFor('QF_LRA');s.set(timeout=int(seconds*1000))
    for i,w in enumerate(v):s.add(w>=0,w<=(2 if i<3 else F(1,4) if i==GAMMA else 1))
    s.add(v[GAMMA]>0)
    for a in single:s.add(af(a)>=0)
    for g in groups:s.add(z3.Or(*(af(a)>=0 for a in g)))
    for i,state in enumerate(q):
        for k in range(2):
            w=v[3+6*k+i]
            s.add(w>0 if state>>k&1 else w==0)
    # Part-order symmetry remains available within equal support states.
    for i in range(2):
        if q[i]==q[i+1]:s.add(v[i]<=v[i+1])
    text=s.to_smt2();stem.with_suffix('.smt2').write_text(text)
    started=time.time();ans=s.check()
    out={'case':list(q),'answer':str(ans),'elapsed':time.time()-started,'limit':seconds,
         'solver':z3.get_version_string(),'input_sha256':hashlib.sha256(text.encode()).hexdigest(),'line_template':line_template}
    if history:out['previous_attempts']=history
    if ans==z3.unsat:
        proof=s.proof().sexpr();stem.with_suffix('.proof').write_text(proof)
        out['proof_bytes']=len(proof);out['proof_sha256']=hashlib.sha256(proof.encode()).hexdigest()
    elif ans==z3.sat:
        model=s.model();point=[F(str(model.eval(w,model_completion=True))) for w in v]
        ev=lambda a:sum(c*w for c,w in zip(a[:-1],point))+a[-1]
        assert point[GAMMA]>0 and all(ev(a)>=0 for a in single)
        assert all(any(ev(a)>=0 for a in g) for g in groups)
        out['point']=list(map(str,point));out['rational_model_rechecked']=True
    else:out['reason']=s.reason_unknown()
    out['statistics']=str(s.statistics())
    stem.with_suffix('.json').write_text(json.dumps(out,indent=2));return out


def main(seconds=60,workers=3,line_template=False):
    ROOT.mkdir(parents=True,exist_ok=True)
    reps=cases();tasks=[];results=[]
    for q in reps:
        original=(ROOT/''.join(map(str,q))).with_suffix('.json')
        if line_template and original.exists():
            old=json.loads(original.read_text())
            if old['answer']=='unsat':results.append(old);continue
        path=(ROOT/(''.join(map(str,q))+('_line' if line_template else ''))).with_suffix('.json')
        if path.exists():
            old=json.loads(path.read_text())
            if old['answer'] in ('sat','unsat'):results.append(old);continue
        tasks.append((q,seconds,line_template))
    coverage={''.join(map(str,q)):''.join(map(str,representative(q))) for q in itertools.product(range(4),repeat=3)}
    (ROOT/'support_orbits.json').write_text(json.dumps(coverage,indent=2))
    print('Support orbits:',len(reps),'jobs:',len(tasks),'workers:',workers,flush=True)
    with multiprocessing.get_context('spawn').Pool(workers,maxtasksperchild=1) as pool:
        for out in pool.imap_unordered(worker,tasks):
            results.append(out)
            print(out['case'],out['answer'],'seconds',round(out['elapsed'],2),flush=True)
            (ROOT/('status_line.json' if line_template else 'status.json')).write_text(json.dumps({'cases':len(reps),'completed':len(results),
                'results':[{k:v for k,v in r.items() if k!='statistics'} for r in results]},indent=2))
    print('Finished batch.',flush=True)


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--workers',type=int,default=3)
    ap.add_argument('--line-template',action='store_true')
    a=ap.parse_args();main(a.seconds,a.workers,a.line_template)
