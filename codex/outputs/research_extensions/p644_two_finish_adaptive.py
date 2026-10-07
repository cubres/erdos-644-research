"""Exact discovery for one response followed by two final pair-cover requests.

The current candidate-pair graph is a complete blow-up on weighted cells.
A first request takes whole cells. The adversary splits each remaining cell
and puts its unused rank in fresh points. Maximal bicliques in the complement
describe EVERY two-request pair cover, including arbitrary splits of cells.
Solver proofs require independent auditing before a universal result is used.
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


def concepts(adj):
    """All maximal anticomplete ordered pairs, quotient exchanging sides."""
    n=len(adj);full=(1<<n)-1;non=[full^a for a in adj]
    common=[full]*(1<<n)
    for m in range(1,1<<n):
        bit=m&-m;j=bit.bit_length()-1;common[m]=common[m^bit]&non[j]
    found=set()
    for a in range(1<<n):
        b=common[a];aa=common[b]
        if a==aa:found.add(tuple(sorted((a,b))))
    return sorted(found)


def response_graph(old_masks,request):
    labels=[]
    for i,m in enumerate(old_masks):
        labels.append((i,False,m))
        if not request>>i&1:labels.append((i,True,m|16))
    edges=[(i,j) for i,j in combinations(range(len(labels)),2) if labels[i][2]|labels[j][2]==31]
    used=sorted(set(j for e in edges for j in e));new={j:i for i,j in enumerate(used)}
    adj=[0]*len(used)
    for a,b in edges:
        i,j=new[a],new[b];adj[i]|=1<<j;adj[j]|=1<<i
    return [labels[j] for j in used],adj


def run(example=0,budget=F(428),seconds=15,gaps=False,stop_on_win=False):
    examples=[([200,43,186],[F(1),F(2893,12),F(347,12),F(229)]),
              ([43,200,186],[F(1),F(2893,12),F(3095,12)-F(1,100),F(1,100)]),
              ([186,200,43],[F(1),F(347,12),F(2725,12),F(243)])]
    if gaps:
        examples=[([200,43,186],[F(1),F(2893,12),F(239,12),F(238)]),
                  ([43,200,186],[F(1),F(2893,12),F(237),F(251,12)]),
                  ([186,200,43],[F(1),F(19),F(237),F(243)])]
    (x,y,z),(p,e,f,g)=examples[example]
    masses=[p,x-p,F(y),F(z),e,f,g,500-y-z-g]
    masks=[11,3,5,6,9,10,12,4]
    if gaps:
        masks += [1,2,8]
        masses += [500-x-y-e,500-x-z-f,500-p-e-f-g]
        assert all(m>=0 for m in masses)
    length=len(masks)
    legal=[s for s in range(1<<length) if sum(m for i,m in enumerate(masses) if s>>i&1)<=budget
           and all(masses[i]>0 for i in range(length) if s>>i&1)]
    legal.sort(key=lambda s:-sum(m for i,m in enumerate(masses) if s>>i&1))
    root=Path('logs/astra_two_finish_adaptive_%d%s_v2'%(example,'_gaps' if gaps else ''));root.mkdir(exist_ok=True)
    started=time.time();results=[]
    z3.set_param(proof=True)
    for request in legal:
        key=str(request);saved=root/(key+'.json')
        if saved.exists():
            old=json.loads(saved.read_text())
            if old.get('budget')==str(budget) and old['status'] in ('sat','unsat'):
                results.append(old);continue
        solver=z3.SolverFor('QF_LRA');solver.set(timeout=int(seconds*1000))
        h=z3.Reals(' '.join('h%d'%i for i in range(length)))
        for i in range(length):solver.add(h[i]>=0,h[i]<=str(masses[i]))
        for i in range(length):
            if request>>i&1:solver.add(h[i]==0)
        solver.add(z3.Sum(*h)<=500)
        if gaps:
            traces=[z3.Sum(*[h[i] for i,m in enumerate(masks) if m>>j&1]) for j in range(4)]
            for t in traces:
                for lo,hi in ((98,106),(F(267,2),178),(216,237)):
                    solver.add(z3.Or(t<str(lo),t>str(hi)))
            for j,k in combinations(range(4),2):
                pair=sum(mass for mass,m in zip(masses,masks) if m>>j&1 and m>>k&1)
                triple=z3.Sum(*[h[i] for i,m in enumerate(masks) if m>>j&1 and m>>k&1])
                solver.add(z3.Or(triple>0,traces[j]+traces[k]+str(pair)>=429))
        labels,adj=response_graph(masks,request);menu=concepts(adj);n=len(labels);full=(1<<n)-1
        raw=[h[i] if inside else z3.RealVal(str(masses[i]))-h[i] for i,inside,m in labels]
        # A cell has no pair-cover obligation when every neighbor has zero
        # mass. Retaining its mass would give false obstructions at boundaries.
        w=[z3.If(z3.Sum(*[raw[j] for j in range(n) if adj[i]>>j&1])>0,raw[i],0)
           for i in range(n)]
        mass=lambda bits:z3.Sum(*[w[i] for i in range(n) if bits>>i&1]) if bits else z3.RealVal(0)
        allmass=mass(full)
        for a,b in menu:
            common=full^(a|b)
            # A-only and B-only must fit their respective requests. Cells
            # allowed on either side can be distributed into residual space.
            ca=mass(common|(a&~b));cb=mass(common|(b&~a))
            solver.add(z3.Or(ca>str(budget),cb>str(budget),allmass+mass(common)>str(2*budget)))
        begin=time.time();answer=solver.check()
        item={'request':request,'budget':str(budget),'status':str(answer),'cells':n,'concepts':len(menu),
              'seconds':time.time()-begin,'masses':list(map(str,masses)),'masks':masks}
        if answer==z3.sat:
            model=solver.model();point=[F(str(model.eval(v,model_completion=True))) for v in h]
            assert all(0<=v<=m for v,m in zip(point,masses)) and sum(point)<=500
            assert all(point[i]==0 for i in range(length) if request>>i&1)
            raw_weights=[point[i] if inside else masses[i]-point[i] for i,inside,m in labels]
            weights=[v if any(raw_weights[j]>0 for j in range(n) if adj[i]>>j&1) else F(0)
                     for i,v in enumerate(raw_weights)]
            sm=lambda bits:sum(weights[i] for i in range(n) if bits>>i&1)
            best=min(max(sm((full^(a|b))|(a&~b)),sm((full^(a|b))|(b&~a)),(sm(full)+sm(full^(a|b)))/2) for a,b in menu)
            assert best>budget
            item.update(response=list(map(str,point)),exact_final_budget=str(best))
        elif answer==z3.unsat:
            (root/(key+'.smt2')).write_text(solver.to_smt2())
            (root/(key+'.proof')).write_text(solver.proof().sexpr())
            item['independent_proof_check']='PENDING'
        else:item['reason']=solver.reason_unknown()
        saved.write_text(json.dumps(item,indent=2));results.append(item)
        print('request',request,'status',answer,'cells',n,'concepts',len(menu),'seconds',round(item['seconds'],3),flush=True)
        if stop_on_win and answer==z3.unsat:break
    report={'example':example,'budget':str(budget),'legal_requests':len(legal),'results':results,'elapsed':time.time()-started}
    (root/'summary.json').write_text(json.dumps(report,indent=2))
    print('FINISHED',len(legal),{s:sum(q['status']==s for q in results) for s in ('sat','unsat','unknown')},'seconds',round(report['elapsed'],2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--example',type=int,default=0,choices=range(3))
    parser.add_argument('--budget',default='428');parser.add_argument('--seconds',type=float,default=15)
    parser.add_argument('--gaps',action='store_true');parser.add_argument('--stop-on-win',action='store_true')
    args=parser.parse_args();run(args.example,F(args.budget),args.seconds,args.gaps,args.stop_on_win)
