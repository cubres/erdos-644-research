"""Numerical discovery for a union of two convex type segments.

No numerical LP status here is by itself a certificate. Endpoint vectors have
equal sum (rank). The Fano test allows a separate segment parameter per row.
"""
import itertools,json,random,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from p644_two_boxes import COLOURS,PARENTS


def blockers(segment):
    a,b=segment;d=[v-u for u,v in zip(a,b)];p=len(a);out=[]
    for i in range(p):
        q=min(a[i],b[i])
        if q>0:
            w=[0]*p;w[i]=1;out.append((w,q))
    for i in range(p):
        for j in range(p):
            if d[i]>0 and d[j]<0:
                w=[0]*p;w[i]=-d[j];w[j]=d[i]
                q=d[i]*a[j]-d[j]*a[i]
                if q>0:out.append((w,q))
    return out


def tau_segments(x,segments):
    best=sum(x);active=None
    for (w,b),(v,c) in itertools.product(*(blockers(s) for s in segments)):
        # Maximize surviving mass subject to one strict blocking halfspace
        # per segment. The closure is valid since b,c>0 and u=0 is strict.
        res=linprog(-np.ones(len(x)),A_ub=[w,v],b_ub=[b,c],bounds=[(0,a) for a in x],method='highs')
        assert res.status==0
        val=sum(x)+res.fun
        if val<best:best=val;active=(w,b,v,c,res.x.tolist())
    return best,active


def disjoint(x,first,second):
    a,b=map(np.array,first);c,d=map(np.array,second)
    res=linprog([0,0],A_ub=np.column_stack([b-a,d-c]),b_ub=np.array(x)-a-c,
                bounds=[(0,1)]*2,method='highs')
    assert res.status in (0,2)
    return res.status==0


def homogeneous(x,segment):
    a,b=map(np.array,segment)
    res=linprog([0],A_ub=(7*(b-a)).reshape(-1,1),b_ub=4*np.array(x)-7*a,
                bounds=[(0,1)],method='highs')
    assert res.status in (0,2)
    return res.status==0


def fano_system(x,segments,colour):
    p=len(x);n=7*p+7;A=[];rhs=[]
    for i in range(p):
        row=np.zeros(n);row[7*i:7*i+7]=1;A.append(row);rhs.append(x[i])
        for j in range(7):
            a,b=segments[int(bool(colour>>j&1))]
            row=np.zeros(n);row[7*p+j]=b[i]-a[i]
            for k,mask in enumerate(PARENTS):
                if mask>>j&1:row[7*i+k]=-1
            A.append(row);rhs.append(-a[i])
    return A,rhs,[(0,None)]*(7*p)+[(0,1)]*7


def fano(x,segments,colour):
    A,rhs,bounds=fano_system(x,segments,colour)
    res=linprog([1]*(7*len(x))+[0]*7,A_ub=A,b_ub=rhs,bounds=bounds,method='highs')
    assert res.status in (0,2)
    return res


def search(count=3000,seed=6442027):
    rank=1000;rng=random.Random(seed);started=time.time()
    seeds=[([400,1390,990],[[[200,0,800],[200,0,800]],[[0,800,200],[0,800,200]]]),
           ([500,740,744],[[[0,740,260],[119,141,740]],[[336,664,0],[336,0,664]]])]
    pool=seeds[:];stats={'draws':0,'valid':0,'intersecting':0,'nonhomogeneous':0,'high_tau':0,'fano_found':0,'colours':{}}
    best=None;candidates=[]
    for it in range(count):
        stats['draws']+=1;sx,ss=rng.choice(pool);x=sx[:];segs=[[a[:],b[:]] for a,b in ss]
        amp=rng.choice([1,5,20,50,150])
        for _ in range(rng.randint(1,4)):
            if rng.random()<.25:
                i=rng.randrange(3);x[i]=max(1,x[i]+rng.randint(-amp,amp))
            else:
                vec=segs[rng.randrange(2)][rng.randrange(2)]
                i,j=rng.sample(range(3),2);delta=rng.randint(-amp,amp)
                vec[i]+=delta;vec[j]-=delta
        if any(not 0<=v<=x[i] for s in segs for a in s for i,v in enumerate(a)):continue
        stats['valid']+=1
        if any(homogeneous(x,s) for s in segs):continue
        stats['nonhomogeneous']+=1
        if sum(x)>=2*rank and any(disjoint(x,a,b) for a,b in itertools.combinations_with_replacement(segs,2)):continue
        stats['intersecting']+=1;tau,active=tau_segments(x,segs)
        if tau<=750+1e-7:continue
        stats['high_tau']+=1;found=None
        for colour in [1,63,3,31,7,11,15,30,0,127]:
            res=fano(x,segs,colour)
            if res.status==0:found=colour;break
        example={'x':x,'segments':segs,'rank':rank,'tau_numerical':tau,'colour':found}
        if found is None:
            print('FANO METHOD OBSTRUCTION CANDIDATE',example,flush=True);candidates.append(example)
            if len(candidates)>=3:break
        else:
            stats['fano_found']+=1;stats['colours'][str(found)]=stats['colours'].get(str(found),0)+1
        if best is None or tau>best['tau_numerical']:best=example
        if rng.random()<.25:
            if len(pool)<150:pool.append((x,segs))
            else:pool[rng.randrange(2,len(pool))]=(x,segs)
        if stats['high_tau']%100==0:print(stats,'elapsed',round(time.time()-started,2),flush=True)
    out={'stats':stats,'seed':seed,'elapsed':time.time()-started,'best':best,'candidates':candidates}
    Path('logs/astra_two_segments_%s.json'%seed).write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2),flush=True);return out


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--count',type=int,default=3000);ap.add_argument('--seed',type=int,default=6442027)
    ar=ap.parse_args();search(ar.count,ar.seed)
