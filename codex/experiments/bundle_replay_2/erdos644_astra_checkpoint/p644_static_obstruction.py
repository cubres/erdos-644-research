"""Exact certificate discovery for a four-static-request obstruction.

Every positive-mass Venn part is labelled by subsets of four requests.
Upward closures of the labels have nonempty antichains on [4]. Adjacent
parts' label families must cross-intersect. Leaves can use the blocker of
their triangle neighbour. Minimal labels suffice for minimising budgets.
Request permutations and swapping Y,Z preserve the target weights.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import json,time


def enumeration():
    families=[]
    for bits in range(1,1<<15):
        a=tuple(m for m in range(1,16) if bits>>(m-1)&1)
        if all(x&y!=x and x&y!=y for x,y in combinations(a,2)):families.append(a)
    ups=[sum(1<<m for m in range(1,16) if any(m&a==a for a in f)) for f in families]
    blocks=[tuple(m for m in range(1,16) if all(m&a for a in f) and not any(
        h!=m and h&m==h and all(h&a for a in f) for h in range(1,16))) for f in families]
    compatible=[{j for j,g in enumerate(families) if all(a&b for a in f for b in g)} for f in families]
    idx={f:i for i,f in enumerate(families)};maps=[]
    for p in permutations(range(4)):
        pm={m:sum(1<<p[q] for q in range(4) if m>>q&1) for m in range(1,16)}
        maps.append([idx[tuple(sorted(pm[m] for m in f))] for f in families])
    seen=set();reps=[];raw=0
    for i in range(len(families)):
        for j in sorted(compatible[i]):
            for k in sorted(compatible[i]&compatible[j]):
                if j>k:continue
                raw+=1;t=(i,j,k)
                if t in seen:continue
                orbit={(pm[i],min(pm[j],pm[k]),max(pm[j],pm[k])) for pm in maps}
                reps.append(min(orbit));seen.update(orbit)
    assert len(seen)==raw
    return families,blocks,sorted(reps),raw


def labels(families,blocks,triple):
    i,j,k=triple
    # X,Y,Z,U,V,W, with pendant neighbours Z,Y,X respectively.
    return [families[i],families[j],families[k],blocks[k],blocks[j],blocks[i]]


def valid_dual(labs,dual,weights,target):
    ye,yu=dual[:6],dual[6:]
    return (all(v<=0 for v in yu) and -sum(yu)<=1 and
            all(ye[p]+sum(yu[j] for j in range(4) if m>>j&1)<=0 for p,L in enumerate(labs) for m in L) and
            sum(a*b for a,b in zip(ye,weights))>=target)


def run():
    import numpy as np
    from scipy.optimize import linprog
    from p644_strategy_lp import recover
    families,blocks,reps,raw=enumeration();print('ENUM',len(families),len(reps),raw,flush=True)
    weights=list(map(F,[5,1,1,4,4,8]));target=F(35,4);duals=[];cases=[];start=time.monotonic()
    for t in reps:
        labs=labels(families,blocks,t)
        found=next((j for j,d in enumerate(duals) if valid_dual(labs,d,weights,target)),None)
        if found is None:
            cols=[(p,m) for p,L in enumerate(labs) for m in L];n=len(cols)
            Ae=np.zeros((6,n+1));Au=np.zeros((4,n+1));Au[:,-1]=-1
            for col,(p,m) in enumerate(cols):
                Ae[p,col]=1
                for j in range(4):Au[j,col]=(m>>j)&1
            c=np.zeros(n+1);c[-1]=1
            q=linprog(c,A_ub=Au,b_ub=np.zeros(4),A_eq=Ae,b_eq=np.array(weights,dtype=float),bounds=(0,None),method='highs')
            assert q.status==0,q.message
            d=recover(list(q.eqlin.marginals)+list(q.ineqlin.marginals))
            if not valid_dual(labs,d,weights,target):
                point=recover(q.x)
                if all(v>=0 for v in point) and all(sum(point[c] for c,(pp,m) in enumerate(cols) if pp==p)==w for p,w in enumerate(weights)):
                    assert all(sum(point[c] for c,(p,m) in enumerate(cols) if m>>j&1)<=point[-1] for j in range(4))
                    print('LOWER WITNESS',t,str(point[-1]),labs,point,flush=True)
                raise RuntimeError(('exact obstruction not proved',t,q.fun))
            found=len(duals);duals.append(d)
        cases.append({'triple':t,'dual':found})
        if len(cases)%500==0:print('PROGRESS',len(cases),'duals',len(duals),'seconds',round(time.monotonic()-start,1),flush=True)
    out={'weights':list(map(str,weights)),'target':str(target),'raw_templates':raw,
         'cases':cases,'duals':[list(map(str,d)) for d in duals]}
    Path('logs/astra_static_obstruction.json').write_text(json.dumps(out,separators=(',',':')))
    print('DONE',len(cases),'cases',len(duals),'duals',round(time.monotonic()-start,1),'seconds',flush=True)


if __name__=='__main__':run()
