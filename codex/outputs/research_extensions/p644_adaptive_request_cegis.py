"""Synthesize a partially filled request before two simultaneous final requests.

Exact rational counterexamples exclude proposed first requests. A completed
UNSAT outer search is a finite obstruction certificate; an UNSAT response
search is a candidate strategy certificate. Both need independent replay.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import json
import sys
import time
sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3
from p644_two_finish_adaptive import response_graph,concepts


def run(example=0,limit=1000,seconds=30,project=False,affine=False):
    source=Path('logs/astra_two_finish_adaptive_%d_gaps/summary.json'%example)
    state=json.loads(source.read_text())['results'][0]
    masses=list(map(F,state['masses']));masks=state['masks'];n=len(masses);budget=F(state['budget'])
    root=Path('logs/astra_adaptive_request_cegis_%d_%s'%(example,'affine' if affine else 'project' if project else 'v2'));root.mkdir(exist_ok=True)
    z3.set_param(proof=True);outer=z3.SolverFor('QF_LRA');oracle=z3.SolverFor('QF_LRA')
    outer.set(timeout=int(seconds*1000));oracle.set(timeout=int(seconds*1000))
    d=z3.Reals(' '.join('d%d'%i for i in range(n)));h=z3.Reals(' '.join('h%d'%i for i in range(n)))
    for i,m in enumerate(masses):outer.add(d[i]>=0,d[i]<=str(m));oracle.add(h[i]>=0,h[i]<=str(m))
    outer.add(z3.Sum(*d)<=str(budget));oracle.add(z3.Sum(*h)<=500)
    traces=[z3.Sum(*[h[i] for i,m in enumerate(masks) if m>>j&1]) for j in range(4)]
    for t in traces:
        for lo,hi in ((98,106),(F(267,2),178),(216,237)):oracle.add(z3.Or(t<str(lo),t>str(hi)))
    for j,k in combinations(range(4),2):
        pair=sum(v for v,m in zip(masses,masks) if m>>j&1 and m>>k&1)
        triple=z3.Sum(*[h[i] for i,m in enumerate(masks) if m>>j&1 and m>>k&1])
        oracle.add(z3.Or(triple>0,traces[j]+traces[k]+str(pair)>=429))
    labels,adj=response_graph(masks,0);menu=concepts(adj);full=(1<<len(labels))-1
    raw=[h[i] if inside else z3.RealVal(str(masses[i]))-h[i] for i,inside,m in labels]
    weights=[z3.If(z3.Sum(*[raw[j] for j in range(len(labels)) if adj[i]>>j&1])>0,raw[i],0)
             for i in range(len(labels))]
    mass=lambda bits:z3.Sum(*[v for i,v in enumerate(weights) if bits>>i&1]) if bits else z3.RealVal(0)
    for a,b in menu:
        c=full^(a|b)
        oracle.add(z3.Or(mass(c|(a&~b))>str(budget),mass(c|(b&~a))>str(budget),mass(full)+mass(c)>str(2*budget)))
    base_assertions=list(oracle.assertions())
    rows=[];started=time.time();status='ITERATION_LIMIT'
    for step in range(limit):
        result=outer.check()
        if result!=z3.sat:
            status='NO_REQUEST' if result==z3.unsat else 'OUTER_UNKNOWN'
            if result==z3.unsat:
                (root/'outer.smt2').write_text(outer.to_smt2());(root/'outer.proof').write_text(outer.proof().sexpr())
            break
        model=outer.model();request=[F(str(model.eval(q,model_completion=True))) for q in d]
        assert sum(request)<=budget and all(0<=q<=m for q,m in zip(request,masses))
        oracle.push()
        for i in range(n):oracle.add(h[i]<=str(masses[i]-request[i]))
        answer=oracle.check()
        if answer!=z3.sat:
            status='WINNING_REQUEST' if answer==z3.unsat else 'ORACLE_UNKNOWN'
            if answer==z3.unsat:
                (root/'winner.smt2').write_text(oracle.to_smt2());(root/'winner.proof').write_text(oracle.proof().sexpr())
                rows.append({'winning_request':list(map(str,request))})
            oracle.pop();break
        model=oracle.model();response=[F(str(model.eval(q,model_completion=True))) for q in h]
        chosen_model=model
        oracle.pop()
        assert all(0<=q<=m-r for q,m,r in zip(response,masses,request)) and sum(response)<=500
        point_cut=z3.Or(*[d[i]>str(masses[i]-response[i]) for i in range(n)])
        record={'request':list(map(str,request)),'response':list(map(str,response))}
        if project or affine:
            guards=[]
            def linearize(expr):
                if z3.is_app_of(expr,z3.Z3_OP_ITE):
                    cond,yes,no=expr.children();truth=z3.is_true(chosen_model.eval(cond,model_completion=True))
                    guards.append(cond if truth else z3.Not(cond));return linearize(yes if truth else no)
                if z3.is_or(expr):
                    child=next(q for q in expr.children() if z3.is_true(chosen_model.eval(q,model_completion=True)))
                    return linearize(child)
                if not expr.children():return expr
                return expr.decl()(*[linearize(q) for q in expr.children()])
            selected=[linearize(q) for q in base_assertions]+guards
            selected += [h[i]+d[i]<=str(masses[i]) for i in range(n)]
            poly=z3.simplify(z3.And(*selected))
            if affine:
                from p644_affine_bad_region import learn
                try:
                    projected,certificate=learn(poly,h,d,request)
                    outer.add(z3.Not(projected));record['projection']='AFFINE_RESPONSE_EXACT_LOCAL_SUBSTITUTION'
                    (root/('affine_%d.json'%step)).write_text(json.dumps(certificate,indent=2))
                    audit=z3.Solver();audit.add(poly);(root/('poly_%d.smt2'%step)).write_text(audit.to_smt2())
                    rows.append(record)
                    print('affine step',step,'rows',certificate['rows_before_projection'],'seconds',round(time.time()-started,2),flush=True)
                    continue
                except (AssertionError,ValueError) as error:
                    record['affine_fallback']=str(error)
                    outer.add(point_cut);rows.append(record);continue
            try:
                goal=z3.Goal();goal.add(z3.Exists(h,poly))
                result=z3.TryFor(z3.Tactic('qe'),5000)(goal)
                projected=z3.simplify(result.as_expr())
                assert not any(z3.is_quantifier(q) for q in [projected]+list(projected.children()))
                outer.add(z3.Not(projected));record['projection']='DISCOVERY_REQUIRES_INDEPENDENT_QE_AUDIT'
                audit=z3.Solver();audit.add(poly);(root/('poly_%d.smt2'%step)).write_text(audit.to_smt2())
                audit=z3.Solver();audit.add(projected);(root/('projection_%d.smt2'%step)).write_text(audit.to_smt2())
            except (z3.Z3Exception,AssertionError) as error:
                outer.add(point_cut);record['projection_fallback']=str(error)
        else:outer.add(point_cut)
        rows.append(record)
        if step%10==0:
            (root/'progress.json').write_text(json.dumps({'state':state,'steps':rows,'status':'RUNNING','elapsed':time.time()-started},indent=2))
            print('step',step,'seconds',round(time.time()-started,2),flush=True)
    report={'state':state,'steps':rows,'status':status,'elapsed':time.time()-started,'independent_verification':'PENDING'}
    (root/'result.json').write_text(json.dumps(report,indent=2))
    print('FINISHED',status,'steps',len(rows),'seconds',round(report['elapsed'],2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--example',type=int,default=0,choices=range(3))
    parser.add_argument('--limit',type=int,default=1000);parser.add_argument('--seconds',type=float,default=30)
    parser.add_argument('--project',action='store_true')
    parser.add_argument('--affine',action='store_true')
    args=parser.parse_args();run(args.example,args.limit,args.seconds,args.project,args.affine)
