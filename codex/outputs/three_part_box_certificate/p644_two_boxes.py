"""Discovery for two convex box components. Numerical statuses are not certificates.

All parameters in the random search are integer units, with edge rank 100.
The exact continuous tau formula uses only integer arithmetic. Fano LPs allow
each row an independent type within its assigned component.
"""
import itertools, json, random, time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
LINESET = {frozenset(q) for q in LINES}
PARENTS = [127-sum(1<<j for j in q) for q in LINES]


def colour_orbits():
    group=[p for p in itertools.permutations(range(7))
           if {frozenset(p[j] for j in q) for q in LINES} == LINESET]
    todo=set(range(128));reps=[]
    while todo:
        q=min(todo);reps.append(q)
        todo.difference_update(sum(1<<p[j] for j in range(7) if q>>j&1) for p in group)
    assert len(group)==168 and len(reps)==10
    return reps


COLOURS=colour_orbits()


def canonical_box(x, lo, hi, rank):
    """Tight coordinate bounds for a nonempty box sliced by sum a=rank."""
    lo=list(lo);hi=[min(v,w) for v,w in zip(hi,x)]
    if any(a>b for a,b in zip(lo,hi)) or sum(lo)>rank or sum(hi)<rank:return None
    return ([max(lo[i],rank-sum(hi)+hi[i]) for i in range(len(x))],
            [min(hi[i],rank-sum(lo)+lo[i]) for i in range(len(x))])


def blockers(x, box, rank):
    """Pairs (coordinate subset, deletion threshold); strict exceedance blocks.

    Edge containment in residual u is equivalent to u>=lo and
    sum min(u_i,hi_i)>=rank. Only positive residual thresholds are usable.
    """
    lo,hi=box;p=len(x);out=[]
    for i in range(p):
        if lo[i]>0:out.append((1<<i,x[i]-lo[i]))
    for mask in range(1,1<<p):
        rhs=rank-sum(hi[i] for i in range(p) if not mask>>i&1)
        if rhs>0:
            out.append((mask,sum(x[i] for i in range(p) if mask>>i&1)-rhs))
    return list(set(out))


def tau_two_boxes(x, boxes, rank):
    """Exact infimum transversal cost in the continuous model."""
    ans=sum(x)
    for (s,a),(t,b) in itertools.product(*(blockers(x,q,rank) for q in boxes)):
        cap=sum(x[i] for i in range(len(x)) if (s&t)>>i&1)
        ans=min(ans,max(0,a,b,a+b-cap))
    return ans


def homogeneous(x, box, rank):
    lo,hi=box
    upper=[min(7*h,4*c) for h,c in zip(hi,x)]
    return all(7*l<=u for l,u in zip(lo,upper)) and sum(upper)>=7*rank


def intersecting(x, boxes, rank):
    if sum(x)<2*rank:return True
    p=len(x)
    eq=np.zeros((2,2*p));eq[0,:p]=1;eq[1,p:]=1
    ub=np.concatenate([np.eye(p),np.eye(p)],axis=1)
    for a,b in itertools.combinations_with_replacement(boxes,2):
        res=linprog(np.zeros(2*p),A_ub=ub,b_ub=x,A_eq=eq,b_eq=[rank]*2,
                    bounds=list(zip(*a))+list(zip(*b)),method='highs')
        if res.status==0:return False
        if res.status!=2:raise RuntimeError(('intersection unknown',res.message))
    return True


def fano_lp(x, boxes, rank, colour):
    """7 parent masses per part, then 7 row loads per part; trim afterwards."""
    p=len(x);n=14*p;A=[];rhs=[]
    for i in range(p):
        row=np.zeros(n);row[7*i:7*i+7]=1;A.append(row);rhs.append(x[i])
        for j in range(7):
            row=np.zeros(n);row[7*p+7*i+j]=1
            for k,mask in enumerate(PARENTS):
                if mask>>j&1:row[7*i+k]=-1
            A.append(row);rhs.append(0)
    eq=np.zeros((7,n))
    for i in range(p):
        for j in range(7):eq[j,7*p+7*i+j]=1
    bounds=[(0,None)]*(7*p)
    for i in range(p):
        for j in range(7):
            lo,hi=boxes[int(bool(colour>>j&1))];bounds.append((lo[i],hi[i]))
    c=np.concatenate([np.ones(7*p),np.zeros(7*p)])
    res=linprog(c,A_ub=A,b_ub=rhs,A_eq=eq,b_eq=[rank]*7,bounds=bounds,method='highs')
    return res


def draw(rng,p,rank):
    x=[rng.randint(15,155) for _ in range(p)]
    if not 175<sum(x)<360:return None
    boxes=[]
    for k in range(2):
        # Mix narrow and broad boxes; substantial endpoint mass is important.
        cuts=sorted([0,rank]+[rng.randint(0,rank) for _ in range(p-1)])
        a=[cuts[i+1]-cuts[i] for i in range(p)];rng.shuffle(a)
        if any(v>w for v,w in zip(a,x)):return None
        width=rng.choice([0,3,10,25,60,100])
        lo=[max(0,v-rng.randint(0,width)) for v in a]
        hi=[min(c,v+rng.randint(0,width)) for v,c in zip(a,x)]
        box=canonical_box(x,lo,hi,rank)
        if box is None:return None
        boxes.append(box)
    return x,boxes


def search(count=200000,seed=6442026,p=3):
    rng=random.Random(seed);rank=100;started=time.time()
    stats={'draws':0,'valid':0,'high_tau':0,'nonhomogeneous':0,'intersecting':0,'fano_found':0}
    examples=[];best=None
    for it in range(count):
        stats['draws']+=1;obj=draw(rng,p,rank)
        if obj is None:continue
        stats['valid']+=1;x,boxes=obj;tau=tau_two_boxes(x,boxes,rank)
        if tau<=75:continue
        stats['high_tau']+=1
        if any(homogeneous(x,b,rank) for b in boxes):continue
        stats['nonhomogeneous']+=1
        if not intersecting(x,boxes,rank):continue
        stats['intersecting']+=1
        found=None
        for colour in COLOURS:
            res=fano_lp(x,boxes,rank,colour)
            if res.status==0:found=colour;break
            if res.status!=2:raise RuntimeError(res.message)
        example={'x':x,'boxes':boxes,'rank':rank,'tau':tau,'colour':found}
        if found is None:
            print('FANO METHOD OBSTRUCTION CANDIDATE',example,flush=True)
            examples.append(example)
            if len(examples)>=3:break
        else:stats['fano_found']+=1
        if best is None or tau>best['tau']:best=example
        if stats['intersecting']%100==0:print(stats,'elapsed',round(time.time()-started,2),flush=True)
    out={'stats':stats,'seed':seed,'p':p,'elapsed':time.time()-started,'best':best,'candidates':examples}
    path=Path('logs/astra_two_boxes_search_%s_%s.json'%(p,seed));path.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2),flush=True)
    return out


def local_search(count=10000,seed=6442026):
    rng=random.Random(seed);rank=1000;started=time.time()
    seeds=[([500,740,744],[([0,0,0],[119,740,744]),([336,0,0],[336,740,744])]),
           ([400,1390,990],[([200,0,800],[200,0,800]),([0,800,200],[0,800,200])])]
    seeds=[(x,[canonical_box(x,*b,rank) for b in boxes]) for x,boxes in seeds]
    pool=list(seeds);stats={'draws':0,'valid':0,'high_tau':0,'nonhomogeneous':0,
                          'intersecting':0,'fano_found':0,'colours':{}}
    candidates=[];best=None;hardest=None
    for it in range(count):
        stats['draws']+=1
        sx,sboxes=rng.choice(pool)
        x=list(sx);boxes=[(list(lo),list(hi)) for lo,hi in sboxes]
        amp=rng.choice([1,5,10,30,100])
        for _ in range(rng.randint(1,4)):
            q=rng.randrange(15);delta=rng.randint(-amp,amp)
            if q<3:x[q]=max(1,x[q]+delta)
            else:
                q-=3;k=q//6;side=(q%6)//3;i=q%3
                boxes[k][side][i]=max(0,min(rank,boxes[k][side][i]+delta))
        boxes=[canonical_box(x,*b,rank) for b in boxes]
        if any(b is None for b in boxes):continue
        stats['valid']+=1;tau=tau_two_boxes(x,boxes,rank)
        if tau<=750:continue
        stats['high_tau']+=1
        if any(homogeneous(x,b,rank) for b in boxes):continue
        stats['nonhomogeneous']+=1
        if not intersecting(x,boxes,rank):continue
        stats['intersecting']+=1
        order=[1,63,3,31,7,11,15,30,0,127];found=None
        for colour in order:
            res=fano_lp(x,boxes,rank,colour)
            if res.status==0:found=colour;break
            if res.status!=2:raise RuntimeError(res.message)
        example={'x':x,'boxes':boxes,'rank':rank,'tau':tau,'colour':found}
        if found is None:
            print('FANO METHOD OBSTRUCTION CANDIDATE',example,flush=True);candidates.append(example)
            if len(candidates)>=3:break
        else:
            stats['fano_found']+=1
            stats['colours'][str(found)]=stats['colours'].get(str(found),0)+1
            if hardest is None or order.index(found)>order.index(hardest['colour']):hardest=example
        if best is None or tau>best['tau']:best=example
        if rng.random()<.15:
            if len(pool)<500:pool.append((x,boxes))
            else:pool[rng.randrange(2,len(pool))]=(x,boxes)
        if stats['intersecting']%500==0:print(stats,'elapsed',round(time.time()-started,2),flush=True)
    out={'stats':stats,'seed':seed,'elapsed':time.time()-started,'best':best,'hardest':hardest,'candidates':candidates}
    Path('logs/astra_two_boxes_local_%s.json'%seed).write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2),flush=True)
    return out


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--count',type=int,default=200000)
    ap.add_argument('--seed',type=int,default=6442026);ap.add_argument('--parts',type=int,default=3)
    ap.add_argument('--local',action='store_true')
    ar=ap.parse_args()
    if ar.local:local_search(ar.count,ar.seed)
    else:search(ar.count,ar.seed,ar.parts)
