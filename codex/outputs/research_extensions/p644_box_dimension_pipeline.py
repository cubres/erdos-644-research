"""Exact discovery across dimensions for two sliced-box components.

No UNSAT status in this file alone is a theorem certificate: new dimensions
need independent input reconstruction and external proof checking. SAT points
are rationally rechecked and fed back into the complete Fano realization LP.
Existing three-part artifacts are not changed.
"""
from fractions import Fraction as F
import hashlib
import itertools
import json
import multiprocessing
from pathlib import Path
import sys
import time

sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3
import p644_two_box_outer as outer


def configure(p):
    outer.P=p;outer.DIM=5*p+1;outer.GAMMA=5*p
    outer.X=[outer.var(i) for i in range(p)]
    outer.LO=[[outer.var(p+2*p*k+i) for i in range(p)] for k in range(2)]
    outer.HI=[[outer.var(2*p+2*p*k+i) for i in range(p)] for k in range(2)]


def system(p,nonline=False,homogeneous=False):
    configure(p)
    add,sub,mul,const=outer.add,outer.sub,outer.mul,outer.const
    X,L,U=outer.X,outer.LO,outer.HI;g=outer.var(outer.GAMMA)
    single=[sub(sub(add(*X),const(F(7,4))),g)];groups=[]
    for k in range(2):
        for i in range(p):
            single += [sub(U[k][i],L[k][i]),sub(X[i],U[k][i]),
                       sub(add(L[k][i],*(U[k][j] for j in range(p) if j!=i)),const(1)),
                       sub(const(1),add(U[k][i],*(L[k][j] for j in range(p) if j!=i)))]
        single += [sub(const(1),add(*L[k])),sub(add(*U[k]),const(1))]
    pools=[outer.blockers(k)[:p]+[q for q in outer.blockers(k)[p:] if 1<bin(q[0]).count('1')<p] for k in range(2)]
    for (s,r,a),(t,q,b) in itertools.product(*pools):
        cap=add(*(X[i] for i in range(p) if (s&t)>>i&1)) if s&t else const()
        groups.append([mul(-1,r),mul(-1,q)]+[sub(sub(c,const(F(3,4))),g) for c in (a,b,sub(add(a,b),cap))])
    for k in range(2):
        failures=[sub(mul(2,L[k][i]),X[i]) for i in range(p)]
        for mask in range(1<<p):
            failures.append(sub(const(2),add(*(mul(2,U[k][i]) if mask>>i&1 else X[i] for i in range(p)))))
        groups.append([sub(a,g) for a in failures])
        if homogeneous:
            # A homogeneous Fano realization already proves the desired
            # conclusion, so a counterexample must fail it in each box.
            failures=[sub(mul(7,L[k][i]),mul(4,X[i])) for i in range(p)]
            for mask in range(1<<p):
                failures.append(sub(const(7),add(*(mul(7,U[k][i]) if mask>>i&1 else mul(4,X[i]) for i in range(p)))))
            groups.append([sub(a,g) for a in failures])
    groups.append([sub(a,g) for a in outer.failure_facets([(1,1,1)])])
    menu=[[(1,6,4)],[(3,0,2),(5,2,4),(1,2,2)],[(0,3,2),(4,3,4)]]
    if nonline:menu.append([(3,0,2),(4,3,4),(1,2,2)])
    for couplings in menu:
        for reverse in (False,True):groups.append([sub(a,g) for a in outer.failure_facets(couplings,reverse)])
    return single,groups


def representative(q):
    return min(tuple(sorted(q)),tuple(sorted({0:0,1:2,2:1,3:3}[v] for v in q)))


def worker(task):
    p,case,seconds,nonline,homogeneous=task;key=''.join(map(str,case))
    root=Path('logs/astra_box_dimension_%d%s%s'%(p,'_all' if nonline else '_three','_hom' if homogeneous else ''));stem=root/key
    root.mkdir(parents=True,exist_ok=True)
    z3.set_param(proof=True)
    start=time.time();single,groups=system(p,nonline,homogeneous)
    names=['x%d'%i for i in range(p)]
    for label in ['a','A','b','B']:names += ['%s%d'%(label,i) for i in range(p)]
    names += ['gamma'];v=z3.Reals(' '.join(names))
    def af(a):return z3.simplify(z3.Sum(*[z3.RealVal(str(c))*v[i] for i,c in enumerate(a[:-1]) if c],z3.RealVal(str(a[-1]))))
    s=z3.SolverFor('QF_LRA');s.set(timeout=int(seconds*1000))
    for i,w in enumerate(v):s.add(w>=0,w<=(2 if i<p else F(1,4) if i==5*p else 1))
    s.add(v[-1]>0)
    for a in single:s.add(af(a)>=0)
    for group in groups:s.add(z3.Or(*(af(a)>=0 for a in group)))
    for i,state in enumerate(case):
        for k in range(2):s.add(v[p+2*p*k+i]>0 if state>>k&1 else v[p+2*p*k+i]==0)
    for i in range(p-1):
        if case[i]==case[i+1]:s.add(v[i]<=v[i+1])
    text=s.to_smt2();stem.with_suffix('.smt2').write_text(text);setup=time.time()-start
    started=time.time();answer=s.check()
    result={'parts':p,'case':list(case),'nonline_template':nonline,'homogeneous_excluded':homogeneous,'answer':str(answer),
            'solver':z3.get_version_string(),'seconds':time.time()-started,'setup_seconds':setup,
            'input_sha256':hashlib.sha256(text.encode()).hexdigest(),'group_sizes':[len(g) for g in groups]}
    if answer==z3.unsat:
        proof=s.proof().sexpr();stem.with_suffix('.proof').write_text(proof)
        result['proof_sha256']=hashlib.sha256(proof.encode()).hexdigest();result['proof_bytes']=len(proof)
        result['independent_verification']='PENDING'
    elif answer==z3.sat:
        model=s.model();point=[F(str(model.eval(w,model_completion=True))) for w in v]
        value=lambda a:sum(c*q for c,q in zip(a[:-1],point))+a[-1]
        assert point[-1]>0 and all(value(a)>=0 for a in single)
        assert all(any(value(a)>=0 for a in group) for group in groups)
        result['point']=list(map(str,point));result['rational_model_rechecked']=True
    else:result['reason']=s.reason_unknown()
    stem.with_suffix('.json').write_text(json.dumps(result,indent=2));return result


def main(p,seconds,workers,nonline,selected=None,homogeneous=False):
    root=Path('logs/astra_box_dimension_%d%s%s'%(p,'_all' if nonline else '_three','_hom' if homogeneous else ''));root.mkdir(parents=True,exist_ok=True)
    reps=sorted({representative(q) for q in itertools.product(range(4),repeat=p)})
    tasks=[]
    for case in reps:
        key=''.join(map(str,case))
        if selected and key not in selected:continue
        old=root/(key+'.json')
        if old.exists() and json.loads(old.read_text())['answer'] in ('sat','unsat'):continue
        tasks.append((p,case,seconds,nonline,homogeneous))
    (root/'support_orbits.json').write_text(json.dumps({''.join(map(str,q)):''.join(map(str,representative(q))) for q in itertools.product(range(4),repeat=p)},indent=2))
    print('Dimension',p,'orbits',len(reps),'jobs',len(tasks),'seconds per solver',seconds,flush=True)
    with multiprocessing.get_context('spawn').Pool(workers,maxtasksperchild=1) as pool:
        for result in pool.imap_unordered(worker,tasks):
            print(result['case'],result['answer'],'seconds',round(result['seconds'],2),'setup',round(result['setup_seconds'],2),flush=True)
    print('Batch finished; every new dimension still requires independent proof verification.',flush=True)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--parts',type=int,default=4)
    parser.add_argument('--seconds',type=float,default=60);parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--nonline',action='store_true');parser.add_argument('--cases',nargs='*')
    parser.add_argument('--homogeneous',action='store_true')
    args=parser.parse_args();main(args.parts,args.seconds,args.workers,args.nonline,args.cases,args.homogeneous)
