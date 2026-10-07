"""Finite two-response probe for global minimum piercing-pair count.

The first seven-edge state is the three-level six-row construction plus a
specified balanced response. Seek a small next request forcing a violation
of (7,2) or of minimum Q on a six-subtuple. This is discovery only; a solver
contradiction needs an independent input/proof audit before a theorem claim.
"""
from itertools import combinations
from pathlib import Path
import argparse
import json
import time
from pysat.card import CardEnc,EncType
from pysat.solvers import Glucose3


def build(scale,mode='balanced'):
    labels=[sum(1<<j for j in S) for S in combinations(range(6),3)]
    assert scale%2==0
    points=[s|(64 if (copy<scale//2 if mode=='balanced' else 7<=atom<17) else 0)
            for atom,s in enumerate(labels) for copy in range(scale)]
    k=10*scale;minimum=10*scale*scale;n=len(points)
    assert all(sum(bool(s>>j&1) for s in points)==k for j in range(7))
    for omit in range(7):
        mask=127^(1<<omit)
        assert not any(s&mask==mask for s in points)
        assert sum((a|b)&mask==mask for a,b in combinations(points,2))>=minimum
    clauses=[];pairs=list(combinations(range(n),2));ids={pair:n+1+j for j,pair in enumerate(pairs)};top=n+len(pairs)
    for (i,j),z in ids.items():clauses.extend([[-i-1,z],[-j-1,z],[-z,i+1,j+1]])
    card=CardEnc.equals(list(range(1,n+1)),bound=k,top_id=top,encoding=EncType.seqcounter);clauses.extend(card.clauses);top=card.nv
    for rows in combinations(range(7),5):
        mask=sum(1<<j for j in rows);assert not any(s&mask==mask for s in points)
        relevant=[ids[i,j] for i,j in pairs if (points[i]|points[j])&mask==mask]
        card=CardEnc.atleast(relevant,bound=minimum,top_id=top,encoding=EncType.seqcounter);clauses.extend(card.clauses);top=card.nv
    for rows in combinations(range(7),6):
        mask=sum(1<<j for j in rows)
        eligible=sorted({v+1 for i,j in pairs if (points[i]|points[j])&mask==mask for v in (i,j)})
        clauses.append(eligible)
    return points,k,minimum,clauses


def valid(points,k,minimum,chosen):
    assert len(chosen)==k
    updated=[mask|(128 if i in chosen else 0) for i,mask in enumerate(points)]
    for rows in combinations(range(8),6):
        mask=sum(1<<j for j in rows)
        assert not any(s&mask==mask for s in updated)
        assert sum((a|b)&mask==mask for a,b in combinations(updated,2))>=minimum
    for rows in combinations(range(8),7):
        mask=sum(1<<j for j in rows)
        assert any((a|b)&mask==mask for a,b in combinations(updated,2))


def run(scale=2,budget=None,limit=1000,mode='balanced'):
    started=time.time();points,k,minimum,clauses=build(scale,mode);n=len(points)
    budget=3*k//4 if budget is None else budget
    root=Path('logs/astra_pair_exchange_probe');root.mkdir(exist_ok=True);key='m%d_T%d'%(scale,budget)+('_block' if mode=='block' else '')
    dc=CardEnc.atmost(list(range(1,n+1)),bound=budget,encoding=EncType.seqcounter)
    print('START',key,'points',n,'rank',k,'minimum',minimum,'response clauses',len(clauses),flush=True)
    responses=[];requests=[];status='ITERATION_LIMIT';witness=None
    with Glucose3(bootstrap_with=dc.clauses) as request_solver,Glucose3(bootstrap_with=clauses) as response_solver:
        for step in range(limit):
            if not request_solver.solve():status='EVERY_REQUEST_HAS_RESPONSE_FINITE_UNAUDITED';break
            deletion=[v-1 for v in request_solver.get_model() if 0<v<=n];assert len(deletion)<=budget
            requests.append(deletion)
            if not response_solver.solve(assumptions=[-i-1 for i in deletion]):
                status='WINNING_REQUEST_FINITE_UNAUDITED';witness=deletion;break
            chosen=[v-1 for v in response_solver.get_model() if 0<v<=n]
            assert not set(chosen)&set(deletion);valid(points,k,minimum,set(chosen))
            responses.append(chosen);request_solver.add_clause([i+1 for i in chosen])
            if step%50==0:
                print('STEP',step,'responses',len(responses),'seconds',round(time.time()-started,2),flush=True)
                (root/(key+'_progress.json')).write_text(json.dumps({'points':points,'rank':k,'minimum':minimum,'budget':budget,'requests':requests,'responses':responses}))
    report={'points':points,'rank':k,'minimum':minimum,'budget':budget,'requests':requests,'responses':responses,
            'status':status,'witness':witness,'elapsed':time.time()-started}
    (root/(key+'.json')).write_text(json.dumps(report,indent=2));print('FINISHED',status,'seconds',round(time.time()-started,2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--scale',type=int,default=2);p.add_argument('--budget',type=int);p.add_argument('--limit',type=int,default=1000)
    p.add_argument('--mode',choices=['balanced','block'],default='balanced')
    a=p.parse_args();run(a.scale,a.budget,a.limit,a.mode)
