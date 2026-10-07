"""Probe the final two adaptive requests using global gaps and triple minimality.

Starts from an exact five-edge response state. The penultimate request is a
whole-cell union; an exact SMT countermodel maximizes the surviving pair core
subject to the global restrictions. UNSAT outcomes require separate audits.
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


def state(example,index):
    data=json.loads(Path('logs/astra_two_finish_adaptive_%d_gaps_v2/summary.json'%example).read_text())
    items=sorted(data['results'],key=lambda q:F(q['exact_final_budget']))
    item=items[index];cells=[]
    for mask,m,h in zip(item['masks'],map(F,item['masses']),map(F,item['response'])):
        if m-h>0:cells.append((mask,m-h))
        if h>0:cells.append((mask|16,h))
    outside=500-sum(map(F,item['response']))
    if outside>0:cells.append((16,outside))
    return item,cells


def run(example=0,index=0,seconds=3,limit=3000):
    source,cells=state(example,index);n=len(cells);T=F(428);rank=F(500)
    root=Path('logs/astra_gap_core_finisher_%d_%d'%(example,index));root.mkdir(exist_ok=True)
    adj=[sum(1<<j for j,(other,w) in enumerate(cells) if i!=j and mask|other==31) for i,(mask,v) in enumerate(cells)]
    legal=[];full=(1<<n)-1
    mass=lambda bits:sum(v for i,(m,v) in enumerate(cells) if bits>>i&1)
    for request in range(1<<n):
        cost=mass(request)
        if cost>T:continue
        remaining=full^request;neighbors=0
        for i in range(n):
            if remaining>>i&1:neighbors|=adj[i]
        isolated_response=remaining&~neighbors
        # Ignore old cells with no candidate-pair edges in this score.
        isolated_response &= sum(1<<i for i,a in enumerate(adj) if a)
        score=mass(neighbors)+min(rank,mass(isolated_response))
        legal.append((score,-cost,request))
    legal.sort();z3.set_param(proof=True);solver=z3.SolverFor('QF_LRA');solver.set(timeout=int(seconds*1000))
    h=z3.Reals(' '.join('h%d'%i for i in range(n)))
    for i,(mask,m) in enumerate(cells):solver.add(h[i]>=0,h[i]<=str(m))
    solver.add(z3.Sum(*h)<=500)
    traces=[z3.Sum(*[h[i] for i,(mask,m) in enumerate(cells) if mask>>j&1]) for j in range(5)]
    for t in traces:
        for lo,hi in ((98,106),(F(267,2),178),(216,237)):solver.add(z3.Or(t<str(lo),t>str(hi)))
    for j,k in combinations(range(5),2):
        common=z3.Sum(*[h[i] for i,(mask,m) in enumerate(cells) if mask>>j&1 and mask>>k&1])
        old=sum(m for mask,m in cells if mask>>j&1 and mask>>k&1)
        solver.add(z3.Or(common>0,traces[j]+traces[k]+str(old)>=429))
    core=[]
    for i,(mask,m) in enumerate(cells):
        if not adj[i]:continue
        neighbors=z3.Sum(*[h[j] for j in range(n) if adj[i]>>j&1])
        core.append(z3.If(neighbors>0,z3.RealVal(str(m)),h[i]))
    solver.add(z3.Sum(*core)>428)
    started=time.time();results=[];winner=None
    print('Five-edge cells',n,'legal requests',len(legal),'initial source request',source['request'],flush=True)
    for count,(_,negcost,request) in enumerate(legal[:limit]):
        solver.push()
        for i in range(n):
            if request>>i&1:solver.add(h[i]==0)
        begin=time.time();answer=solver.check();result={'request':request,'cost':str(-negcost),'answer':str(answer),'seconds':time.time()-begin}
        if answer==z3.unsat:
            winner=request;(root/'winner.smt2').write_text(solver.to_smt2());(root/'winner.proof').write_text(solver.proof().sexpr())
            result['independent_verification']='PENDING';results.append(result);solver.pop();break
        if answer==z3.sat:
            model=solver.model();point=[F(str(model.eval(q,model_completion=True))) for q in h]
            assert all(0<=v<=m for v,(mask,m) in zip(point,cells)) and sum(point)<=500
            assert all(point[i]==0 for i in range(n) if request>>i&1)
            core_mass=sum(m if any(point[j]>0 for j in range(n) if adj[i]>>j&1) else point[i]
                          for i,(mask,m) in enumerate(cells) if adj[i])
            assert core_mass>428;result.update(response=list(map(str,point)),core=str(core_mass))
        else:result['reason']=solver.reason_unknown()
        results.append(result);solver.pop()
        if count%100==0:print('tested',count+1,'seconds',round(time.time()-started,2),flush=True)
    report={'example':example,'index':index,'source':source,'cells':[[mask,str(m)] for mask,m in cells],
            'legal_requests':len(legal),'results':results,'winner':winner,'elapsed':time.time()-started}
    (root/'result.json').write_text(json.dumps(report,indent=2))
    print('FINISHED tested',len(results),'winner',winner,'seconds',round(report['elapsed'],2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--example',type=int,default=0,choices=range(3));parser.add_argument('--index',type=int,default=0)
    parser.add_argument('--seconds',type=float,default=3);parser.add_argument('--limit',type=int,default=3000)
    args=parser.parse_args();run(args.example,args.index,args.seconds,args.limit)
