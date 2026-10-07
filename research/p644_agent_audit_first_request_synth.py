"""Bounded minimax discovery for a first request on a minimum-sum triple.

Prover cuts use exact rational bad-response lower bounds. Winning templates
use three-bin mask supports and the ten price vertices. No result here is a
general upper bound. The all-allocations search initially requires that at
least one old pair core be deleted in full, to activate minimum-sum exchange.
"""
from fractions import Fraction as F
from itertools import permutations, combinations, product
from pathlib import Path
import argparse
import json
import sys
import time
sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3
from p644_agent_audit_four_seed_bins import solve, graph

PRICES=sorted(set(permutations((12,0,0)))|set(permutations((6,6,0)))|
              set(permutations((6,3,3)))|{(4,4,4)})


def clique_templates(n):
    ants=[a for size in range(1,8)for a in combinations(range(1,8),size)
          if not any(u!=v and u&v==u for u in a for v in a)]
    costs={a:[min(sum(q[j]for j in range(3)if m>>j&1)for m in a)for q in PRICES]for a in ants}
    forms=set()
    for labels in product(ants,repeat=n):
        if any(not(u&v)for i,j in combinations(range(n),2)for u in labels[i]for v in labels[j]):continue
        forms.add(tuple(sorted(set(tuple(costs[labels[i]][q]for i in range(n))for q in range(10)))))
    return sorted(forms)


CLIQUE_FORMS={n:clique_templates(n)for n in (2,3)}


def clique_lower(a,x,y,T):
    weights,active,edges=exact_graph(a,x,y);es={frozenset(e)for e in edges}
    best=F(0);certificate=None
    for n in (2,3):
        for vertices in combinations(active,n):
            if not all(frozenset(e)in es for e in combinations(vertices,2)):continue
            w=[weights[i]for i in vertices]
            value=min(max(sum(v*c for v,c in zip(w,row))for row in forms)for forms in CLIQUE_FORMS[n])/12
            if value>best:best=value;certificate={'clique':list(vertices),'weights':list(map(str,w)),'templates':len(CLIQUE_FORMS[n]),'lower_bound':str(value)}
            if best>T:return best,certificate
    return best,certificate


def biclique_lower(a,x,y,T):
    weights,active,edges=exact_graph(a,x,y)
    neigh={i:{v if u==i else u for u,v in edges if i in (u,v)}for i in active}
    best=F(0);certificate=None;seen=set()
    for n in (1,2):
        for left in combinations(active,n):
            right=set.intersection(*(neigh[i]for i in left))
            if not right:continue
            w=tuple(sorted((sum(weights[i]for i in left),sum(weights[i]for i in right))))
            if w in seen:continue
            seen.add(w)
            value=min(max(sum(v*c for v,c in zip(w,row))for row in forms)for forms in CLIQUE_FORMS[2])/12
            if value>best:best=value;certificate={'left':list(left),'right':sorted(right),'weights':list(map(str,w)),'templates':len(CLIQUE_FORMS[2]),'lower_bound':str(value)}
            if best>T:return best,certificate
    return best,certificate


def exact_graph(a,x,y):
    p=[1-a[(i+1)%3]-a[(i+2)%3] for i in range(3)]
    _,_,edges=graph(list(map(float,a)),list(map(float,x)),list(map(float,y)))
    weights=list(x)+[a[i]-x[i] for i in range(3)]+list(y)+[p[i]-y[i] for i in range(3)]
    active=[i for i,w in enumerate(weights) if w>0 and any((i==u and weights[v]>0)or(i==v and weights[u]>0)for u,v in edges)]
    return weights,active,[(i,j)for i,j in edges if i in active and j in active]


def duplication_lower(a,x,y,T):
    weights,active,edges=exact_graph(a,x,y)
    neigh={i:{v if u==i else u for u,v in edges if i in (u,v)}for i in active}
    forced={i for i in active if sum(weights[j]for j in neigh[i])>=T}
    conflicts=[(i,j)for i,j in edges if sum(weights[v]for v in neigh[i]|neigh[j])>T]
    remaining=[i for i in active if i not in forced]
    best=None;cover=None
    for mask in range(1<<len(remaining)):
        chosen=forced|{v for j,v in enumerate(remaining)if mask>>j&1}
        if not all(i in chosen or j in chosen for i,j in conflicts):continue
        cost=sum(weights[i]for i in chosen)
        if best is None or cost<best:best=cost;cover=sorted(chosen)
    bound=(sum(weights[i]for i in active)+best)/3
    return bound,{'forced':sorted(forced),'conflicts':conflicts,'minimum_extra':str(best),'minimizing_cover':cover,'lower_bound':str(bound)}


def forms_from_solution(a,x,y,result,T):
    names,_,_=graph(list(map(float,a)),list(map(float,x)),list(map(float,y)))
    weights,active,edges=exact_graph(a,x,y)
    labels={i:[int(m)for m in result.get('assignments',{}).get(names[i],{})]for i in active}
    if any(not labels[i] for i in active):return None
    if any(not(u&v)for i,j in edges for u in labels[i]for v in labels[j]):return None
    forms=[]
    for price in PRICES:
        row=[0]*12
        for i in active:row[i]=min(sum(price[b]for b in range(3)if m>>b&1)for m in labels[i])
        forms.append(tuple(row))
    forms=sorted(set(forms))
    if max(sum(w*c for w,c in zip(weights,row))for row in forms)>12*T:return None
    return {'zeros':[i for i,w in enumerate(weights)if not w],
            'labels':{str(i):m for i,m in labels.items()},'forms':[list(r)for r in forms]}


def run(seconds=90,steps=30,T=F(19,25),whole=True):
    a=[F(49,100),F(49,100),F(6,25)]
    p=[1-a[(i+1)%3]-a[(i+2)%3]for i in range(3)];caps=a+p
    d=z3.Reals('d0 d1 d2 d3 d4 d5');prover=z3.Solver();prover.set(timeout=5000)
    prover.add(*[z3.And(v>=0,v<=str(c))for v,c in zip(d,caps)],z3.Sum(d)==str(T))
    if whole:prover.add(z3.Or(*[d[i]==str(a[i])for i in range(3)]))
    templates=[];bad=[];events=[];started=time.time();status='LIMIT'
    def locals_result():
        return {'status':status,'a':list(map(str,a)),'T':str(T),'whole_core_required':whole,'elapsed_seconds':time.time()-started,'templates':templates,'bad_responses':bad,'events':events,'prover_smt2':prover.to_smt2()}
    for outer in range(steps):
        if time.time()-started>seconds:break
        pr=prover.check()
        if pr==z3.unsat:status='EXACT_RATIONAL_CUT_SYSTEM_UNSAT';break
        if pr!=z3.sat:status='PROVER_UNKNOWN';break
        pm=prover.model();deletion=[F(str(pm.eval(v)))for v in d]
        adversary=z3.Solver();adversary.set(timeout=5000)
        x=z3.Reals('x0 x1 x2');y=z3.Reals('y0 y1 y2')
        for i in range(3):
            adversary.add(x[i]>=0,x[i]<=str(a[i]-deletion[i]),y[i]>=0,y[i]<=str(p[i]-deletion[3+i]))
            adversary.add(z3.Or(x[i]>0,z3.RealVal(str(a[i]))+z3.Sum([x[j]+y[j]for j in range(3)if j!=i])>=str(sum(a))))
        adversary.add(z3.Sum(x+y)<=1)
        weights=list(x)+[z3.RealVal(str(a[i]))-x[i]for i in range(3)]+list(y)+[z3.RealVal(str(p[i]))-y[i]for i in range(3)]
        def exclude(temp):
            adversary.add(z3.Or(*([weights[i]>0 for i in temp['zeros']]+[
                z3.Sum([c*w for c,w in zip(row,weights)if c])>str(12*T)for row in temp['forms']])))
        for temp in templates:exclude(temp)
        event={'step':outer,'deletion':list(map(str,deletion))}
        while time.time()-started<seconds:
            ar=adversary.check()
            if ar==z3.unsat:
                status='WINNING_FIRST_REQUEST_REQUIRES_REPLAY';event['status']=status
                events.append(event);return locals_result()
            if ar!=z3.sat:status='ADVERSARY_UNKNOWN';event['status']=status;break
            am=adversary.model();xp=[F(str(am.eval(v,model_completion=True)))for v in x];yp=[F(str(am.eval(v,model_completion=True)))for v in y]
            lower,cert=duplication_lower(a,xp,yp,T)
            if lower<=T:
                clower,ccert=clique_lower(a,xp,yp,T)
                if clower>lower:lower=clower;cert={'clique_certificate':ccert,'lower_bound':str(lower)}
            if lower<=T:
                clower,ccert=biclique_lower(a,xp,yp,T)
                if clower>lower:lower=clower;cert={'biclique_certificate':ccert,'lower_bound':str(lower)}
            if lower>T:
                witness={'x':list(map(str,xp)),'y':list(map(str,yp)),'certificate':cert}
                bad.append(witness)
                prover.add(z3.Or(*[d[i]>str(a[i]-xp[i])for i in range(3)],
                                 *[d[i+3]>str(p[i]-yp[i])for i in range(3)]))
                event.update(status='EXACT_BAD_RESPONSE',witness=witness)
                break
            result=solve(list(map(float,a)),list(map(float,xp)),list(map(float,yp)),seconds=min(5,max(1,seconds-(time.time()-started))))
            template=forms_from_solution(a,xp,yp,result,T)
            if template is None:
                status='UNRESOLVED_RESPONSE';event.update(status=status,x=list(map(str,xp)),y=list(map(str,yp)),q_upper=result['q_upper'],q_lower=result['q_lower'],duplication_lower=str(lower));break
            templates.append(template);exclude(template)
        events.append(event)
        print(json.dumps(event),flush=True)
        if status not in ('LIMIT',):break
    return locals_result()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--seconds',type=int,default=90);parser.add_argument('--steps',type=int,default=30)
    parser.add_argument('--budget',default='19/25');parser.add_argument('--allow-no-whole-core',action='store_true');parser.add_argument('--tag',default='latest')
    args=parser.parse_args()
    result=run(args.seconds,args.steps,F(args.budget),not args.allow_no_whole_core)
    target=Path('logs/astra_agent_audit_first_request_synth_'+args.tag+'.json');target.write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items()if k not in ('templates','bad_responses','events','prover_smt2')},indent=2))
