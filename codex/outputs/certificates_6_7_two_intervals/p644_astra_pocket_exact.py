"""Discover exact branch-and-LP certificates for the asymmetric pocket.

The target is d=1/4-e, c=7/10+e, 0<e<=1/1000. Every bad tuple
has at most one occurrence of either anchor, and repetitions of nonanchor
edges pad shorter bad tuples to seven. We enumerate all 28 type multisets.
All infeasible leaves need rational Farkas certificates valid on this whole
half-open interval. Numerical LP statuses alone are never accepted.
"""
import argparse
import itertools as it
import json
import time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


FULL=127
EPS=F(1,1000)


def maximal_triples():
    triples=[sum(1<<j for j in a) for a in it.combinations(range(7),3)]
    adj=[sum(1<<j for j,b in enumerate(triples) if a&b and a!=b) for a in triples]
    out=[]
    def bk(R,P,X):
        if not P and not X:
            out.append(tuple(triples[j] for j in range(35) if R>>j&1));return
        union=P|X;u=max((j for j in range(35) if union>>j&1),key=lambda j:bin(P&adj[j]).count('1'))
        todo=P&~adj[u]
        while todo:
            bit=todo&-todo;v=bit.bit_length()-1
            bk(R|bit,P&adj[v],X&adj[v]);P^=bit;X|=bit;todo^=bit
    bk(0,(1<<35)-1,0)
    return out


def root_representatives(types):
    groups=[[j for j,t in enumerate(types) if t==name] for name in dict.fromkeys(types)]
    permutations=[]
    for images in it.product(*(list(it.permutations(g)) for g in groups)):
        p=list(range(7))
        for g,image in zip(groups,images):
            for a,b in zip(g,image):p[a]=b
        permutations.append([sum(1<<p[j] for j in range(7) if m>>j&1) for m in range(128)])
    maximal=maximal_triples();seen=set();reps=[]
    for T in maximal:
        T=tuple(sorted(T))
        if T in seen:continue
        reps.append(T)
        for p in permutations:seen.add(tuple(sorted(p[m] for m in T)))
    assert len(seen)==len(maximal)==6127
    return reps


def build(types,e):
    val={'A1':(F(1),F(0)),'A2':(F(0),F(1)),
         's':(F(1,4)-e,F(3,4)+e),'t':(F(7,10)+e,F(3,10)-e)}
    cols=[];tags=[]
    for side in (0,1):
        for mask in range(FULL):
            if any(t=='A1' and bool(mask>>j&1)!=(side==0) or
                   t=='A2' and bool(mask>>j&1)!=(side==1) for j,t in enumerate(types)):continue
            # Nonanchor edges intersect (d+c=19/20). The sole possible
            # disjoint pair is A1,A2. A point in five edges leaves at most
            # two edges; they cannot be this pair since A1 union A2 is V.
            # Thus degree >=5 always gives a two-point transversal.
            if bin(mask).count('1')>4:continue
            v=[0]*16;v[side*8]=1
            for j in range(7):v[side*8+1+j]=int(bool(mask>>j&1))
            cols.append(v);tags.append((side,mask))
    b=[]
    for side in (0,1):b.extend([F(1)]+[val[t][side] for t in types])
    return np.array(cols,dtype=float).T,tags,b


def discover(types,seconds,maximal=False):
    A,tags,b=build(types,EPS);_,_,b0=build(types,F(0));bf=np.array(list(map(float,b)))
    start=time.monotonic();nodes=[];cache={};leaves=[];calls=0
    # Each dual can also certify descendants for which its negative columns
    # have all been forbidden.
    def dual(allowed):
        AA=A[:,allowed]
        q=linprog(np.zeros(16),A_ub=np.vstack([-AA.T,np.array(list(map(float,b0)))]),
                  b_ub=np.zeros(len(allowed)+1),A_eq=bf[None,:],b_eq=[-1.0],
                  bounds=[(None,None)]*16,method='highs')
        if q.status!=0:raise ValueError('No interval dual; the branch needs parameter refinement')
        for den in (1000,1000000,1000000000):
            y=[F(float(v)).limit_denominator(den) for v in q.x]
            if sum(x*v for x,v in zip(y,b))>=0 or sum(x*v for x,v in zip(y,b0))>0:continue
            costs=[sum(y[j]*int(A[j,i]) for j in range(16)) for i in range(A.shape[1])]
            if all(costs[i]>=0 for i in allowed):
                required=sum(1<<m for m in set(tags[i][1] for i,z in enumerate(costs) if z<0))
                return y,required
        raise ValueError('Could not rationalize dual exactly')

    def rec(banned):
        nonlocal calls
        if time.monotonic()-start>seconds:raise TimeoutError
        if banned in cache:return cache[banned]
        for required,leaf in leaves:
            if required & banned==required:return leaf
        allowed=[i for i,(_,m) in enumerate(tags) if not banned>>m&1]
        q=linprog(np.zeros(len(allowed)),A_eq=A[:,allowed],b_eq=bf,
                  bounds=(0,None),method='highs');calls+=1
        if q.status==2:
            y,required=dual(allowed);idx=len(nodes);nodes.append({'dual':list(map(str,y))})
            leaves.append((required,idx));cache[banned]=idx;return idx
        if q.status!=0:raise ValueError(q.message)
        weights={}
        for i,x in zip(allowed,q.x):
            if x>1e-8:weights[tags[i][1]]=weights.get(tags[i][1],0)+x
        conflicts=[(min(weights[a],weights[b]),a,b) for a,b in it.combinations(weights,2) if a|b==FULL]
        if not conflicts:raise ValueError('Possible bad tuple or numerical degeneracy: requires exact primal check')
        _,a,b=max(conflicts)
        left=rec(banned | 1<<a);right=rec(banned | 1<<b)
        idx=len(nodes);nodes.append({'pair':[a,b],'children':[left,right]});cache[banned]=idx
        if calls%1000==0:print('progress',''.join(types),'LP calls',calls,'leaves',len(leaves),flush=True)
        return idx
    try:
        if maximal:
            roots=[]
            reps=root_representatives(types)
            for i,T in enumerate(reps):
                banned=sum(1<<m for m in range(128) if bin(m).count('1')==4 and (FULL^m) not in T)
                root=rec(banned);roots.append({'triples':T,'root':root})
                if i%10==0:print('maximal roots',i+1,'/',len(reps),'calls',calls,flush=True)
            extra={'maximal_roots':roots}
        else:extra={'root':rec(0)}
        return {'status':'EXACT_INTERVAL_CERTIFICATE','types':types,'nodes':nodes,**extra,
                'lp_calls':calls,'elapsed':time.monotonic()-start}
    except (ValueError,TimeoutError) as e:
        return {'status':'INCOMPLETE','types':types,'reason':str(e) or 'time limit',
                'lp_calls':calls,'leaves':len(leaves),'elapsed':time.monotonic()-start}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=int,default=60)
    ap.add_argument('--out',default='logs/astra_pocket_interval.json');ap.add_argument('--case',type=int)
    ap.add_argument('--maximal',action='store_true')
    args=ap.parse_args();results=[];cases=[]
    for a,b in [(0,0),(1,0),(0,1),(1,1)]:
        for s in range(8-a-b):cases.append(['A1']*a+['A2']*b+['s']*s+['t']*(7-a-b-s))
    for i,types in enumerate(cases):
        if args.case is not None and i!=args.case:continue
        r=discover(types,args.seconds,maximal=args.maximal);results.append(r)
        print(i,{k:v for k,v in r.items() if k not in ('nodes','maximal_roots')},flush=True)
        Path(args.out).write_text(json.dumps({'epsilon':str(EPS),'cases':results},indent=1))


if __name__=='__main__':main()
