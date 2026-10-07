"""Search three static requests followed by the full adaptive core request.

This is a discovery program. Recovered allocation masses and any claimed
core upper bound are checked exactly. Failed searches imply no optimality.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import linprog
from p644_strategy_lp import recover

PAIRS=[(0,1),(0,2),(1,2),(0,5),(1,4),(2,3)]


def core(allocation,r=F(100)):
    active=[(p,m,a) for p,L in enumerate(allocation) for m,a in enumerate(L) if a>0]
    adjacent={p:{q for a,b in PAIRS for q in ([b] if a==p else ([a] if b==p else []))} for p in range(6)}
    cols=[]
    for k,(p,m,a) in enumerate(active):
        for v in range(8):
            if m&v:continue
            endpoint=any(q in adjacent[p] and (n&v)==n for q,n,b in active)
            cols.append((k,v,endpoint))
    Ae=np.zeros((len(active),len(cols)));Au=np.zeros((3,len(cols)))
    for j,(k,v,end) in enumerate(cols):
        Ae[k,j]=1
        for h in range(3):Au[h,j]=(v>>h)&1
    q=linprog([-int(end) for k,v,end in cols],A_eq=Ae,b_eq=[float(a) for p,m,a in active],
              A_ub=Au,b_ub=[float(r)]*3,bounds=(0,None),method='highs')
    assert q.status==0
    ye=recover(q.eqlin.marginals);yu=recover(q.ineqlin.marginals)
    if any(x>0 for x in yu) or any(ye[k]+sum(yu[h] for h in range(3) if v>>h&1)>-int(end) for k,v,end in cols):return None
    bound=-sum((e*a for e,(p,m,a) in zip(ye,active)),F(0))-r*sum(yu)
    return {'upper':str(bound),'dual_eq':list(map(str,ye)),'dual_ub':list(map(str,yu))}


def run(trials=2000):
    weights=list(map(F,[50,10,10,40,40,80]));T=F(87);rng=np.random.default_rng(644)
    Ae=np.zeros((6,48));Au=np.zeros((3,48))
    for p,m in product(range(6),range(8)):
        Ae[p,p*8+m]=1
        for h in range(3):Au[h,p*8+m]=(m>>h)&1
    sources=json.loads(Path('logs/astra_static_four.json').read_text())
    src=next(q for q in sources if q['triple']==['1/2','1/10','1/10'])
    seeds=[]
    for removed in range(4):
        keep=[i for i in range(4) if i!=removed]
        seeds.append([{sum(1<<j for j,h in enumerate(keep) if int(m)>>h&1) for m in part} for part in src['parts']])
    best=F(10000);log=[];start=time.monotonic()
    for step in range(trials):
        seed=seeds[step%4]
        if step%5:
            costs=np.array([min(bin(m^s).count('1') for s in seed[p]) for p,m in product(range(6),range(8))],dtype=float)
            costs+=rng.normal(0,0.4 if step%2 else 1,48)
        else:costs=rng.normal(0,1,48)
        q=linprog(costs,A_eq=Ae,b_eq=np.array(weights,dtype=float),A_ub=Au,b_ub=[float(T)]*3,bounds=(0,None),method='highs')
        assert q.status==0
        v=recover(q.x);alloc=[v[p*8:(p+1)*8] for p in range(6)]
        if any(a<0 for a in v) or any(sum(a)!=w for a,w in zip(alloc,weights)):continue
        budgets=[sum(v[p*8+m] for p,m in product(range(6),range(8)) if m>>h&1) for h in range(3)]
        if max(budgets)>T:continue
        b=core(alloc)
        if b is None:continue
        if F(b['upper'])<best:
            best=F(b['upper']);row={'trial':step,'core_bound':b,'allocation':[[str(a) for a in L] for L in alloc],
                                  'request_budgets':list(map(str,budgets))}
            log.append(row);print('BEST',step,str(best),'seconds',round(time.monotonic()-start,1),flush=True)
            Path('logs/astra_core_static_search.json').write_text(json.dumps({'trials':step+1,'target':str(T),'best_history':log},indent=1))
        if best<=T:print('EXACT WIN',flush=True);break
        if (step+1)%500==0:print('PROGRESS',step+1,'best',str(best),flush=True)
    Path('logs/astra_core_static_search.json').write_text(json.dumps({'trials':step+1,'target':str(T),'best_history':log},indent=1))
    print('DONE',step+1,'best',str(best),'seconds',round(time.monotonic()-start,1),flush=True)


if __name__=='__main__':run()
