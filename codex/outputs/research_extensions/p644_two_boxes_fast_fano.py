"""Discovery LPs using the exactly classified sixteen Fano inequalities.

Numerical LP statuses here are discovery only. Universal input classification
is checked separately by p644_fano_capacity_check.py with rational arithmetic.
"""
import itertools
import json
from pathlib import Path
import random
import time
import numpy as np
from scipy.optimize import linprog
from p644_two_boxes import canonical_box,tau_two_boxes,homogeneous,intersecting,LINES


def fano(x, boxes, rank, colour):
    p = len(x)
    eq = np.zeros((7,7*p))
    for j in range(7):
        eq[j,j*p:(j+1)*p] = 1
    ub=[];rhs=[]
    for i in range(p):
        row=np.zeros(7*p);row[i::p]=1;ub.append(row);rhs.append(4*x[i])
        for line in LINES:
            row=np.zeros(7*p)
            for j in line:row[j*p+i]=1
            ub.append(row);rhs.append(2*x[i])
    bounds=[]
    for j in range(7):
        lo,hi=boxes[int(bool(colour>>j&1))]
        bounds.extend(zip(lo,hi))
    res=linprog(np.zeros(7*p),A_ub=ub,b_ub=rhs,A_eq=eq,b_eq=[rank]*7,
                bounds=bounds,method='highs')
    if res.status not in (0,2):raise RuntimeError(res.message)
    return res


def search(count=20000, seed=6442028):
    rank=1000;p=4;rng=random.Random(seed);started=time.time()
    seed1=([190,590,690,690],[([0,400,0,0],[0,400,600,600]),([0,0,0,0],[190,0,690,690])])
    pool=[(seed1[0],[canonical_box(seed1[0],*b,rank) for b in seed1[1]])]
    stats={'draws':0,'valid':0,'high_tau':0,'nonhomogeneous':0,'intersecting':0,'fano_found':0,'colours':{}}
    candidates=[];best=None;hardest=None;order=[1,63,3,31,7,30,11,15,0,127]
    for step in range(count):
        stats['draws']+=1;sx,sb=rng.choice(pool);x=sx[:];boxes=[(lo[:],hi[:]) for lo,hi in sb]
        amp=rng.choice([1,5,20,50,150,300])
        for _ in range(rng.randint(1,6)):
            q=rng.randrange(5*p);delta=rng.randint(-amp,amp)
            if q<p:x[q]=max(1,x[q]+delta)
            else:
                q-=p;k=q//(2*p);side=(q%(2*p))//p;i=q%p
                boxes[k][side][i]=max(0,min(rank,boxes[k][side][i]+delta))
        boxes=[canonical_box(x,*b,rank) for b in boxes]
        if any(b is None for b in boxes):continue
        stats['valid']+=1;tau=tau_two_boxes(x,boxes,rank)
        if tau<=750:continue
        stats['high_tau']+=1
        if any(homogeneous(x,b,rank) for b in boxes):continue
        stats['nonhomogeneous']+=1
        if not intersecting(x,boxes,rank):continue
        stats['intersecting']+=1;found=None
        for colour in order:
            if fano(x,boxes,rank,colour).status==0:found=colour;break
        obj={'x':x,'boxes':boxes,'rank':rank,'tau':tau,'colour':found}
        if found is None:
            candidates.append(obj);print('OBSTRUCTION CANDIDATE',obj,flush=True)
        else:
            stats['fano_found']+=1;stats['colours'][str(found)]=stats['colours'].get(str(found),0)+1
            if hardest is None or order.index(found)>order.index(hardest['colour']):hardest=obj
        if best is None or tau>best['tau']:best=obj
        if rng.random()<.25:
            if len(pool)<600:pool.append((x,boxes))
            else:pool[rng.randrange(1,len(pool))]=(x,boxes)
        if stats['intersecting']%1000==0:print(stats,'seconds',round(time.time()-started,1),flush=True)
        if len(candidates)>=3:break
    out={'stats':stats,'seed':seed,'elapsed':time.time()-started,'best':best,'hardest':hardest,'candidates':candidates}
    Path('logs/astra_four_boxes_fast_%s.json'%seed).write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2),flush=True)
    return out


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--count',type=int,default=20000)
    parser.add_argument('--seed',type=int,default=6442028);args=parser.parse_args()
    search(args.count,args.seed)
